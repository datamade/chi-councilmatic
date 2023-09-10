import re
from datetime import datetime
from operator import attrgetter

import pytz
from councilmatic_core.models import Bill, Event, Organization, Person
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.functional import cached_property
from opencivicdata.legislative.models import (BillSponsorship,
                                              EventRelatedEntity,
                                              LegislativeSession)

from .helpers import topic_classifier

app_timezone = pytz.timezone(settings.TIME_ZONE)


class ChicagoBill(Bill):
    class Meta:
        proxy = True
        app_label = "chicago"

    @property
    def friendly_name(self):
        nums = self.identifier.split(" ")[-1]
        return self.bill_type.title() + " " + nums

    @property
    def date_passed(self):
        return (
            self.actions.filter(classification="passage")
            .order_by("-order")
            .first()
            .date_dt
            if self.actions.all()
            else None
        )

    def _terminal_status(self, history, bill_type):

        # history is a list of actions, where each action a list of one
        if history:
            if bill_type.lower() in ["ordinance", "resolution"]:
                if ["passage"] in history:
                    return "Passed"
                elif ["failure"] in history or ["committe-failure"] in history:
                    return "Failed"
            if bill_type.lower() in ["order", "appointment", "resolution"]:
                if ["passage"] in history:
                    return "Approved"
                else:
                    return False

        return False

    def _is_stale(self, last_action_date):
        # stale = no action for 5 months
        if last_action_date:
            timediff = datetime.now().date() - last_action_date
            return timediff.days > 180
        else:
            return True

    @property
    def inferred_status(self):
        actions = self.actions.all().order_by("-order")
        classification_hist = [a.classification for a in actions]
        last_action_date = actions[0].date_dt if actions else None
        bill_type = self.bill_type

        if bill_type.lower() in ["communication", "oath of office"]:
            return None
        if self._terminal_status(classification_hist, bill_type):
            return self._terminal_status(classification_hist, bill_type)
        elif self._is_stale(last_action_date):
            return "Stale"
        else:
            return "Active"

    @property
    def listing_description(self):
        return self.title

    @property
    def topics(self):
        tags = topic_classifier(self.title)
        if "Routine" in tags:
            tags.remove("Routine")
            tags = ["Routine"] + tags
        elif "Non-Routine" in tags:
            tags.remove("Non-Routine")
            tags = ["Non-Routine"] + tags
        return tags

    @property
    def addresses(self):
        """
        returns a list of relevant addresses for a bill

        override this in custom subclass
        """
        if "Ward Matters" in self.topics or "City Matters" in self.topics:
            stname_pattern = r"(\S*[a-z]\S*\s){1,4}?"
            sttype_pattern = (
                r"(ave|blvd|cres|ct|dr|hwy|ln|pkwy|pl|plz|rd|row|sq|st|ter|way)"
            )
            st_pattern = stname_pattern + sttype_pattern

            # match 123 and 123-125, but not 123-125-127
            addr_pattern = r"((?<!-)\b\d{1,5}(-\d{1,5})?\s%s)" % st_pattern
            intersec_pattern = r"((?<=\sat\s)%s\s?and\s?%s)" % (
                st_pattern,
                st_pattern,
            )

            pattern = "(%s|%s)" % (addr_pattern, intersec_pattern)

            matches = re.findall(pattern, self.title, re.IGNORECASE)

            addresses = [m[0] for m in matches]
            return addresses

        return []

    @cached_property
    def full_text_doc_url(self):
        """
        override this if instead of having full text as string stored in
        full_text, it is a PDF document that you can embed on the page
        """
        if self.versions.all():
            most_recent = self.versions.first().links.first().url
            return f"https://corsproxy.bunkum.us/corsproxy/?apiurl={most_recent}"
        else:
            return None


class ChicagoOrganization(Organization):
    class Meta:
        proxy = True
        app_label = "chicago"

    @property
    def recent_events(self):
        # need to look up event participants by name
        events = ChicagoEvent.objects.filter(
            participants__entity_type="organization", participants__name=self.name
        )
        events = events.order_by("-start_date").all()
        return events


class ChicagoEvent(Event):
    class Meta:
        proxy = True
        app_label = "chicago"

    @property
    def attendance(self):
        return self.participants.filter(entity_type="person")

    @classmethod
    def most_recent_past_city_council_meeting(cls):
        if hasattr(settings, "CITY_COUNCIL_MEETING_NAME"):
            return (
                cls.objects.filter(name__icontains=settings.CITY_COUNCIL_MEETING_NAME)
                .filter(start_time__lt=datetime.now())
                .filter(status="passed")
                .latest("start_time")
            )
        else:
            return None

    @cached_property
    def video_vimeo_id(self):
        try:
            link = self.media.first().links.first().url
            vimeo_id = re.match(".*?([0-9]+)$", link).group(1)
            print(link, vimeo_id)
            return vimeo_id
        except AttributeError:
            return None


class ChicagoPerson(Person):
    class Meta:
        proxy = True
        app_label = "chicago"

    # this is a very expensive query - do not use on listing pages
    @cached_property
    def full_attendance(self):
        attendance = []
        events = []

        current_legislative_session = LegislativeSession.objects.get(
            start_date__lt=timezone.now(), end_date__gt=timezone.now()
        )

        # fetch all events for the current legislative session for committees they're on
        for membership in self.current_memberships.all():
            events.extend(
                ChicagoEvent.objects.filter(
                    participants__organization=membership.organization,
                    start_date__gte=membership.start_date,
                )
                .filter(start_date__gte=current_legislative_session.start_date)
                .filter(participants__entity_type="person")
                .distinct()
                .prefetch_related("participants")
            )

        for e in sorted(events, key=attrgetter("start_time"), reverse=True):
            attended = e.participants.filter(person_id=self.id).exists()
            attendance.append(
                {
                    "event": e,
                    "attended": attended,
                }
            )

        return attendance

    @property
    def attendance_percent(self):
        attendance = self.full_attendance
        if len(attendance) > 0:
            attended = [a for a in attendance if a["attended"]]
            return "{:.0%}".format(len(attended) / len(attendance))
        else:
            return 0

    @property
    def legislation_count(self):
        return ChicagoBill.objects.filter(
            sponsorships__person=self, sponsorships__primary=True
        ).count()

    @property
    def election_status(self):
        for p in settings.ALDER_EXTRAS:
            if (
                self.slug.startswith(p)
                and "election-status" in settings.ALDER_EXTRAS[p]
            ):
                return settings.ALDER_EXTRAS[p]["election-status"]

        return ""

    @property
    def caucus(self):
        for p in settings.ALDER_EXTRAS:
            if self.slug.startswith(p) and "caucus" in settings.ALDER_EXTRAS[p]:
                return settings.ALDER_EXTRAS[p]["caucus"]

        return ""

    @property
    def term_active(self):
        # older entries may not have a latest_council_membership
        if self.latest_council_membership is None:
            return False

        return self.latest_council_membership.end_date_dt > timezone.now()

    @property
    def years_in_office(self):
        if self.latest_council_membership is None:
            return ""

        years = 0
        if self.term_active:
            years = relativedelta(
                timezone.now(), self.latest_council_membership.start_date_dt
            ).years
        else:
            years = relativedelta(
                self.latest_council_membership.end_date_dt,
                self.latest_council_membership.start_date_dt,
            ).years

        if years == 0:
            return "< 1"
        else:
            return years


class ChicagoPersonStatistic(models.Model):
    person = models.OneToOneField(
        ChicagoPerson,
        related_name="statistics",
        on_delete=models.CASCADE,
        help_text="A link to the Person connected to this statistic record.",
    )

    attendance_list = models.JSONField(null=True)
    attendance_percent = models.CharField(max_length=10)
    legislation_count = models.IntegerField()
    legislation_success_rate = models.CharField(max_length=10, null=True)
