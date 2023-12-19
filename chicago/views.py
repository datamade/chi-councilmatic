import itertools
from datetime import datetime
from operator import attrgetter
from urllib.parse import urlencode

import pytz
import json
from councilmatic_core.models import BillAction, Organization, Post
from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models import Max, Min, Prefetch, Subquery
from django.http import Http404, HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView, DetailView, ListView
from haystack.generic_views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from opencivicdata.core.models import Membership
from opencivicdata.legislative.models import (
    BillSponsorship,
    EventAgendaItem,
    EventRelatedEntity,
    LegislativeSession,
    PersonVote,
)

from chicago.models import ChicagoBill, ChicagoEvent, ChicagoOrganization, ChicagoPerson


class ChicagoIndexView(TemplateView):
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
        context = super().get_context_data(**kwargs)
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


class ChicagoAboutView(TemplateView):
    template_name = "about.html"


class CouncilmaticSearchForm(FacetedSearchForm):
    def __init__(self, *args, **kwargs):
        self.load_all = True

        super().__init__(*args, **kwargs)

    def no_query_found(self):
        return self.searchqueryset.all()


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


class ChicagoBillDetailView(DetailView):
    model = ChicagoBill
    template_name = "legislation.html"
    context_object_name = "legislation"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # the new Clerk LMS minted new IDs for existing bills in Legistar
            # this handles redirects from old bill IDs to new ones
            slug = self.kwargs["slug"]
            try:
                bill = self.model.objects.get(
                    other_identifiers__identifier__iexact=slug
                )
                return HttpResponsePermanentRedirect(
                    reverse("bill_detail", args=[bill.slug])
                )

            except self.model.DoesNotExist:
                raise Http404

    def get_queryset(self):

        # Getting a handle on vote details
        actions_qs = (
            BillAction.objects.order_by("-order")
            .select_related("organization__councilmatic_organization")
            .select_related("vote")
            .prefetch_related(
                Prefetch(
                    "vote__votes",
                    queryset=PersonVote.objects.select_related(
                        "voter__councilmatic_person"
                    ),
                )
            )
            .prefetch_related("vote__counts")
        )

        return (
            super()
            .get_queryset()
            .prefetch_related(Prefetch("actions", queryset=actions_qs))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        bill = self.object

        alternate_identifiers = bill.other_identifiers.exclude(
            identifier=bill.identifier
        )

        # we have to  do the sponsors here, instead of in get_queryset
        # because we need a handle on the actual bill object in order
        # to get the council post as of the first action on the bill
        first_action_date_subquery = (
            BillAction.objects.filter(bill_id=bill).order_by("order").values("date")[:1]
        )

        sponsors = (
            bill.sponsorships.filter(person_id__isnull=False)
            .select_related("person__councilmatic_person")
            .prefetch_related(
                Prefetch(
                    "person__memberships",
                    queryset=Membership.objects.filter(
                        organization__name=settings.OCD_CITY_COUNCIL_NAME,
                        start_date__lte=Subquery(first_action_date_subquery),
                        end_date__gte=Subquery(first_action_date_subquery),
                    )
                    .order_by("-start_date", "-end_date")
                    .select_related("post"),
                    to_attr="council_posts",
                )
            )
        )

        context["sponsors_qs"] = sponsors
        context["alternate_identifiers"] = alternate_identifiers

        seo = {}
        seo.update(settings.SITE_META)
        seo["site_desc"] = bill.listing_description
        seo["title"] = "%s - %s" % (bill.friendly_name, settings.SITE_META["site_name"])
        context["seo"] = seo

        (bill_classification,) = bill.classification
        bill_identifier = bill.identifier
        if bill_classification in {"claim"} or bill_identifier == "Or 2013-382":
            context["seo"]["noindex"] = True

        return context


class ChicagoDividedVotesView(ListView):
    template_name = "divided_votes.html"
    context_object_name = "bills"

    def get_queryset(self):
        if self.kwargs["legislative_session"] not in settings.LEGISLATIVE_SESSIONS:
            raise Http404

        return (
            ChicagoBill.objects.filter(
                actions__vote__counts__option="no",
                actions__organization__name=settings.OCD_CITY_COUNCIL_NAME,
                legislative_session__identifier=self.kwargs["legislative_session"],
            )
            .filter(
                actions__vote__counts__option="yes",
            )
            .annotate(last_action=Max("actions__date"))
            .order_by("-last_action")
            .prefetch_related("actions__vote__counts")
        )

    def get_context_data(self, *args, **kwargs):
        context = super(ChicagoDividedVotesView, self).get_context_data(**kwargs)
        # remove 2007 - there is very little data
        context["legislative_session_options"] = settings.LEGISLATIVE_SESSIONS[1:]

        legislative_session = LegislativeSession.objects.get(
            identifier=self.kwargs["legislative_session"]
        )
        context["legislative_session"] = legislative_session
        return context


class ChicagoCouncilMembersView(ListView):
    template_name = "council_members.html"
    context_object_name = "posts"

    def map(self):
        map_geojson = {"type": "FeatureCollection", "features": []}

        for post in self.object_list:
            if post.shape:
                council_member = "Vacant"
                detail_link = ""
                if post.current_member:
                    council_member = post.current_member.person.name
                    detail_link = post.current_member.person.slug

                feature = {
                    "type": "Feature",
                    "geometry": json.loads(post.shape.json),
                    "properties": {
                        "district": post.label,
                        "council_member": council_member,
                        "detail_link": "/person/" + detail_link,
                        "select_id": "polygon-{}".format(slugify(post.label)),
                    },
                }

                map_geojson["features"].append(feature)

        return json.dumps(map_geojson)

    def get_queryset(self):
        get_kwarg = {"name": settings.OCD_CITY_COUNCIL_NAME}

        return Organization.objects.get(**get_kwarg).posts.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seo"] = self.get_seo_blob()
        context["map_geojson"] = self.map
        context["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

        return context

    def get_seo_blob(self):
        seo = {}
        seo.update(settings.SITE_META)
        seo[
            "site_desc"
        ] = "Enter your address or browse the map to find which of \
          Chicago's 50 Wards you live in and who your Alder is."
        seo["image"] = "/static/images/chicago_map.jpg"
        seo["title"] = "Find Your Ward and Alder - Chicago Councilmatic"

        return seo


class ChicagoPersonDetailView(DetailView):
    template_name = "person.html"
    model = ChicagoPerson
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        person = context["person"]

        if person.latest_council_membership:
            context[
                "tenure_start"
            ] = person.latest_council_membership.start_date_dt.strftime("%B %d, %Y")
            context[
                "tenure_end"
            ] = person.latest_council_membership.end_date_dt.strftime("%B %d, %Y")

        context["chair_positions"] = person.chair_role_memberships

        context["sponsored_legislation"] = (
            ChicagoBill.objects.filter(
                sponsorships__person=person, sponsorships__primary=True
            )
            .annotate(last_action=Max("actions__date"))
            .order_by("-last_action")[:10]
        )

        attendance = person.full_attendance
        context["committee_count"] = len(person.current_memberships) - 1
        context["attendance"] = attendance
        context["attendance_present"] = len([a for a in attendance if a["attended"]])
        context["attendance_absent"] = len(
            [a for a in attendance if a["attended"] is False]
        )

        if (
            person.latest_council_membership
            and person.latest_council_membership.post
            and person.latest_council_membership.post.shape
        ):
            map_geojson = {"type": "FeatureCollection", "features": []}

            feature = {
                "type": "Feature",
                "geometry": json.loads(
                    person.latest_council_membership.post.shape.json
                ),
                "properties": {
                    "district": person.latest_council_membership.post.label,
                },
            }

            map_geojson["features"].append(feature)

            context["map_geojson"] = json.dumps(map_geojson)
            context["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

        return context


class ChicagoCouncilMembersCompareView(ListView):
    template_name = "compare_council_members.html"
    context_object_name = "council_members"

    def get_queryset(self):
        return (
            ChicagoPerson.objects.filter(
                memberships__organization__name=settings.OCD_CITY_COUNCIL_NAME
            )
            .filter(memberships__end_date__gt=datetime.now())
            .distinct()
        )

    def get_context_data(self, *args, **kwargs):
        context = super(ChicagoCouncilMembersCompareView, self).get_context_data(
            **kwargs
        )
        return context


class ChicagoCommitteesView(ListView):
    template_name = "committees.html"
    context_object_name = "committees"

    def get_queryset(self):
        return Organization.committees()


class ChicagoCommitteeDetailView(DetailView):
    template_name = "committee.html"
    context_object_name = "committee"
    model = ChicagoOrganization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        committee = context["committee"]
        context["memberships"] = committee.memberships.all()

        description = None

        if getattr(settings, "COMMITTEE_DESCRIPTIONS", None):
            for k in settings.COMMITTEE_DESCRIPTIONS:
                if committee.slug.startswith(k):
                    description = context[
                        "committee_description"
                    ] = settings.COMMITTEE_DESCRIPTIONS[k]

        seo = {}
        seo.update(settings.SITE_META)
        seo["site_desc"] = "View members and meetings for %s's %s. " % (
            settings.CITY_COUNCIL_NAME,
            committee.name,
        )
        if description:
            seo["site_desc"] += description

        seo["title"] = "%s - %s" % (committee.name, settings.SITE_META["site_name"])
        context["seo"] = seo

        return context


class ChicagoEventsView(TemplateView):
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
            date_time = parser.parse(date_str).astimezone(pytz.timezone("US/Central"))

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


class ChicagoEventDetailView(DetailView):
    model = ChicagoEvent
    template_name = "event.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context["event"]

        # getting expected attendees and actual attendees
        expected_attendees = set()
        event_orgs = event.participants.filter(entity_type="organization")
        context["event_orgs"] = event_orgs
        for event_org in event_orgs:
            org_members = event_org.organization.memberships.filter(
                start_date__lte=event.start_time, end_date__gte=event.start_time
            ).select_related("person__councilmatic_person")
            expected_attendees.update([m.person for m in org_members])

        attendees = set()
        for event_person in event.attendance:
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

    def get_queryset(self):

        sponsors_qs = BillSponsorship.objects.filter(
            person_id__isnull=False
        ).select_related("person__councilmatic_person")

        related_bill_qs = (
            EventRelatedEntity.objects.filter(entity_type="bill")
            .select_related("bill__councilmatic_bill")
            .prefetch_related(
                Prefetch("bill__sponsorships", queryset=sponsors_qs, to_attr="sponsors")
            )
        )

        related_action_qs = EventRelatedEntity.objects.filter(
            entity_type="vote_event"
        ).select_related("vote_event__bill_action")

        agenda_items_qs = (
            EventAgendaItem.objects.extra(
                select={"order_numeric": 'CAST("order" as INTEGER)'}
            )
            .order_by("order_numeric")
            .prefetch_related(
                Prefetch("related_entities", queryset=related_bill_qs, to_attr="bills")
            )
            .prefetch_related(
                Prefetch(
                    "related_entities", queryset=related_action_qs, to_attr="actions"
                )
            )
        )

        return (
            super()
            .get_queryset()
            .prefetch_related(Prefetch("agenda", queryset=agenda_items_qs))
            .prefetch_related("documents")
        )


def flush(request, flush_key):
    try:
        if flush_key == settings.FLUSH_KEY:
            cache.clear()
    except AttributeError:
        print(
            "\n\n** NOTE: to use flush-cache, set FLUSH_KEY in settings_local.py **\n\n"
        )

    return redirect("index")


@xframe_options_exempt
def pdfviewer(request):
    return render(request, "pdfviewer.html")
