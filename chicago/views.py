import re

import itertools
from operator import attrgetter
from django.db.models import Min
from dateutil import parser
from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.urls import reverse
from django.db.models import Max
from django.utils import timezone

from chicago.models import ChicagoBill, ChicagoEvent, ChicagoOrganization
from councilmatic_core.views import (
    IndexView,
    AboutView,
    BillDetailView,
    CouncilMembersView,
    PersonDetailView,
    EventsView,
    EventDetailView,
    CommitteesView,
    CommitteeDetailView,
    CouncilmaticSearchForm,
)
from councilmatic_core.models import Post

from haystack.generic_views import FacetedSearchView


class ChicagoIndexView(IndexView):
    template_name = "index.html"
    bill_model = ChicagoBill
    event_model = ChicagoEvent

    def last_meeting(self):
        return ChicagoEvent.most_recent_past_city_council_meeting()

    def date_cutoff(self):
        return self.last_meeting().start_time.date()

    def council_bills(self):
        return ChicagoBill.objects.filter(
            actions__date=self.date_cutoff(),
            from_organization__name=settings.OCD_CITY_COUNCIL_NAME,
        ).prefetch_related("actions")

    def topic_hierarchy(self):
        # getting topic counts for meeting bills
        topic_hierarchy = settings.TOPIC_HIERARCHY
        topic_tag_counts = {}

        for b in self.council_bills():
            for topic in b.topics:
                try:
                    topic_tag_counts[topic] += 1
                except KeyError:
                    topic_tag_counts[topic] = 1
        # put together data blob for topic hierarchy
        for parent_blob in topic_hierarchy:
            parent_blob["count"] = 0
            for child_blob in parent_blob["children"]:
                child_name = child_blob["name"]
                child_blob["count"] = (
                    topic_tag_counts[child_name]
                    if child_name in topic_tag_counts
                    else 0
                )
                parent_blob["count"] += child_blob["count"]
                for gchild_blob in child_blob["children"]:
                    gchild_name = gchild_blob["name"]
                    gchild_blob["count"] = (
                        topic_tag_counts[gchild_name]
                        if gchild_name in topic_tag_counts
                        else 0
                    )

        return topic_hierarchy

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # Find activity at last council meeting
        council_bills = self.council_bills()
        context["council_bills"] = council_bills
        context["nonroutine_council_bills"] = [
            bill for bill in council_bills if "Non-Routine" in bill.topics
        ]

        # Find recent activitiy (since last council meeting)
        recent_bills = ChicagoBill.objects.filter(actions__date__gt=self.date_cutoff())
        context["recent_bills"] = recent_bills
        context["nonroutine_recent_bills"] = [
            bill for bill in recent_bills if "Non-Routine" in bill.topics
        ]

        seo = {}
        seo.update(settings.SITE_META)
        seo["image"] = "/static/images/city_hall.jpg"
        context["seo"] = seo

        context[
            "last_council_meeting"
        ] = self.event_model.most_recent_past_city_council_meeting
        context["next_council_meeting"] = self.event_model.next_city_council_meeting
        context[
            "upcoming_committee_meetings"
        ] = self.event_model.upcoming_committee_meetings
        context["topic_hierarchy"] = self.topic_hierarchy

        return context


class ChicagoAboutView(AboutView):
    template_name = "about.html"


def substitute_ordinance_redirect(request, substitute_ordinance_slug):
    return redirect("bill_detail", slug=substitute_ordinance_slug[1:], permanent=True)


class ChicagoBillDetailView(BillDetailView):
    template_name = "legislation.html"

    model = ChicagoBill

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs["slug"]

        try:
            bill = self.model.objects.get(slug=slug)
            return super().dispatch(request, *args, **kwargs)
        except ChicagoBill.DoesNotExist:
            bill = None

        if not bill:
            """
            Chicago Councilmatic requires redirects for several old bill slugs:
            (1) original Councilmatic slug, which used the Legistar GUID
            (2) a mangled form: an added space, e.g.,  o-2018-2302 (old slug)
            vs. o2018-2302
            """
            try:
                pattern = "?ID=%s&GUID" % slug
                bill = ChicagoBill.objects.get(sources__url__contains=pattern)
                return HttpResponsePermanentRedirect(
                    reverse("bill_detail", args=[bill.slug])
                )
            except ChicagoBill.DoesNotExist:
                try:
                    added_space = r"^([A-Za-z]+)-([-\d]+)$"
                    match_added_space = re.match(added_space, slug)
                    if match_added_space:
                        prefix = match_added_space.group(1)
                        remainder = match_added_space.group(2)
                        repaired_slug = "{prefix}{remainder}".format(
                            prefix=prefix, remainder=remainder
                        )
                        bill = self.model.objects.get(slug=repaired_slug)
                        return HttpResponsePermanentRedirect(
                            reverse("bill_detail", args=[bill.slug])
                        )
                except ChicagoBill.DoesNotExist:
                    raise Http404

        raise Http404

    def get_object(self, queryset=None):
        """
        Returns a bill based on slug. If no bill found,
        looks for bills based on legistar id (so that
        urls from old Chicago councilmatic don't break)
        """

        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with "
                "either an object pk or a slug." % self.__class__.__name__
            )

        # Try looking up by slug
        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No bill found matching the query")

        return obj

    def get_context_data(self, **kwargs):
        context = super(ChicagoBillDetailView, self).get_context_data(**kwargs)
        (bill_classification,) = context["object"].classification
        bill_identifier = context["object"].identifier
        if bill_classification in {"claim"} or bill_identifier == "Or 2013-382":
            context["seo"]["nofollow"] = True
        return context


class ChicagoCouncilMembersView(CouncilMembersView):
    template_name = "council_members.html"

    def get_seo_blob(self):
        seo = {}
        seo.update(settings.SITE_META)
        seo[
            "site_desc"
        ] = "Look up your local Alderman, and see what they're \
          doing in your ward & your city"
        seo["image"] = "/static/images/chicago_map.jpg"
        seo["title"] = "Wards & Aldermen - Chicago Councilmatic"

        return seo


class ChicagoCouncilmaticFacetedSearchView(FacetedSearchView):

    form_class = CouncilmaticSearchForm
    facet_fields = [
        "bill_type",
        "sponsorships",
        "controlling_body",
        "inferred_status",
        "topics",
        "legislative_session",
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["q_filters"] = self._get_query_parameters()
        context["selected_facets"] = self._get_selected_facets()

        context["user_subscribed"] = False

        context["current_council_members"] = {
            p.current_member.person.name: p.label
            for p in Post.objects.all()
            if p.current_member
        }

        return context

    def get_queryset(self):
        sqs = super().get_queryset()
        sort_field = self.request.GET.get("sort_by", "date")

        # default facet list size is 10, but we want to show all
        options = {"size": 250}
        for field in self.facet_fields:
            sqs = sqs.facet(field, **options)

        if sort_field in ("date", "title"):  # relevance is default
            sort_order = self.request.GET.get("order_by", "desc")
            sqs_field = {"date": "last_action_date", "title": "sort_name_exact"}[
                sort_field
            ]

            sqs = sqs.order_by(
                "{0}{1}".format("" if sort_order == "asc" else "-", sqs_field)
            )

        return sqs

    def _get_selected_facets(self):
        selected_facets = {}

        for val in self.request.GET.getlist("selected_facets"):
            if val:
                # e.g., bill_type_exact:ordinance -> bill_type, ordinance
                k, v = val.split("_exact:", 1)
                try:
                    selected_facets[k].append(v)
                except KeyError:
                    selected_facets[k] = [v]

        return selected_facets

    def _get_query_parameters(self):
        excluded_parameters = (
            "page",
            "selected_facets",
            "amp",
            "_",
        )
        query_parameters = [
            (param, val)
            for (param, val) in self.request.GET.items()
            if param not in excluded_parameters
        ]
        query_parameters += [
            ("selected_facets", param)
            for param in self.request.GET.getlist("selected_facets")
        ]

        if query_parameters:
            return urlencode(query_parameters)

        return ""


class ChicagoPersonDetailView(PersonDetailView):
    template_name = "person.html"

    def get_context_data(self, **kwargs):
        context = super(ChicagoPersonDetailView, self).get_context_data(**kwargs)

        person = context["person"]

        if person.latest_council_membership:
            context[
                "tenure_start"
            ] = person.latest_council_membership.start_date_dt.strftime("%B %d, %Y")

        context["chair_positions"] = person.chair_role_memberships

        context["sponsored_legislation"] = (
            ChicagoBill.objects.filter(
                sponsorships__person=person, sponsorships__primary=True
            )
            .annotate(last_action=Max("actions__date"))
            .order_by("-last_action")[:10]
        )

        return context


class ChicagoCommitteesView(CommitteesView):
    template_name = "committees.html"


class ChicagoCommitteeDetailView(CommitteeDetailView):
    template_name = "committee.html"
    context_object_name = "committee"
    model = ChicagoOrganization

    def get_context_data(self, **kwargs):
        context = super(CommitteeDetailView, self).get_context_data(**kwargs)

        committee = context["committee"]
        context["memberships"] = committee.memberships.all()

        description = None

        if getattr(settings, "COMMITTEE_DESCRIPTIONS", None):
            for k in settings.COMMITTEE_DESCRIPTIONS:
                if committee.slug.startswith(k):
                    context["committee_description"] = settings.COMMITTEE_DESCRIPTIONS[
                        k
                    ]

        seo = {}
        seo.update(settings.SITE_META)

        if description:
            seo["site_desc"] = description
        else:
            seo["site_desc"] = "See what %s's %s has been up to!" % (
                settings.CITY_COUNCIL_NAME,
                committee.name,
            )

        seo["title"] = "%s - %s" % (committee.name, settings.SITE_META["site_name"])
        context["seo"] = seo

        return context


class ChicagoEventsView(EventsView):
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)

        # Get year range for datepicker.
        aggregates = ChicagoEvent.objects.aggregate(
            Min("start_time"), Max("start_time")
        )

        context["year_range_min"] = aggregates["start_time__min"].year
        context["year_range_max"] = aggregates["start_time__max"].year

        # Did the user set date boundaries?
        date_str = self.request.GET.get("form_datetime")
        day_grouper = lambda x: x.local_start_time.date  # noqa E731
        context["select_date"] = ""

        date_time = timezone.now()
        # If yes, then filter for dates.
        if date_str:
            context["date"] = date_str
            date_time = parser.parse(date_str)

            select_events = (
                ChicagoEvent.objects.filter(start_time__gt=date_time)
                .filter(start_time__lt=(date_time + relativedelta(months=1)))
                .order_by("start_time")
            )

            org_select_events = []

            for event_date, events in itertools.groupby(select_events, key=day_grouper):
                events = sorted(events, key=attrgetter("start_time"))
                org_select_events.append([event_date, events])

            context["select_events"] = org_select_events
            context["select_date"] = (
                date_time.strftime("%B") + " " + date_time.strftime("%Y")
            )

        # If no, then return upcoming events.
        else:
            # Upcoming events for the current month.
            upcoming_events = (
                ChicagoEvent.objects.filter(start_time__gt=timezone.now())
                .filter(start_time__lt=(timezone.now() + relativedelta(months=1)))
                .order_by("start_time")
            )

            if len(upcoming_events) < 3:
                # Upcoming events for the next month, plus two from previous months
                upcoming_events = (
                    ChicagoEvent.objects.filter(start_time__gt=timezone.now())
                    .filter(start_time__lt=(timezone.now() + relativedelta(months=2)))
                    .order_by("start_time")
                )

            org_upcoming_events = []

            for event_date, events in itertools.groupby(
                upcoming_events, key=day_grouper
            ):
                events = sorted(events, key=attrgetter("start_time"))
                org_upcoming_events.append([event_date, events])

            context["upcoming_events"] = org_upcoming_events

        context["prev_month"] = (
            date_time.replace(day=1) - relativedelta(months=1)
        ).strftime("%m-%d-%Y")
        context["next_month"] = (
            date_time.replace(day=1) + relativedelta(months=1)
        ).strftime("%m-%d-%Y")

        return context


class ChicagoEventDetailView(EventDetailView):
    model = ChicagoEvent
    template_name = "event.html"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event = context["event"]

        # getting expected attendees and actual attendees
        expected_attendees = set()
        event_orgs = event.participants.filter(entity_type="organization")
        for event_org in event_orgs:
            org_members = event_org.organization.memberships.filter(
                start_date__lte=event.start_time, end_date__gte=event.start_time
            )
            expected_attendees.update([m.person for m in org_members])

        attendees = set()
        for event_person in event.participants.filter(entity_type="person"):
            attendees.add(event_person.person_id)

        attendance = []
        for expected_attendee in sorted(expected_attendees, key=lambda x: x.name):
            attended = expected_attendee.id in attendees
            attendance.append(
                {
                    "attendee": expected_attendee.councilmatic_person,
                    "attended": attended,
                }
            )

        context["attendance_taken"] = len(attendees) > 0
        context["attendance"] = attendance
        context["attendance_present"] = len([a for a in attendance if a["attended"]])
        context["attendance_absent"] = len(
            [a for a in attendance if a["attended"] is False]
        )

        seo = {}
        seo.update(settings.SITE_META)
        seo["site_desc"] = "Public city council event on %s/%s/%s" % (
            event.start_time.month,
            event.start_time.day,
            event.start_time.year,
        )
        seo["title"] = "%s Event - %s" % (event.name, settings.SITE_META["site_name"])
        context["seo"] = seo

        return context
