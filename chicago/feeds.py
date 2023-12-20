import urllib

from haystack.query import SearchQuerySet

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse, reverse_lazy
from django.conf import settings

from .models import Person, Bill, Organization, Event
from .utils import to_datetime


class FacetedSearchFeed(Feed):
    title_template = "feeds/search_item_title.html"
    description_template = "feeds/search_item_description.html"
    bill_model = Bill

    all_results = None
    sqs = (
        SearchQuerySet()
        .facet("bill_type")
        .facet("sponsorships", sort="index")
        .facet("controlling_body")
        .facet("inferred_status")
    )
    query = None

    def url_with_querystring(self, path, **kwargs):
        return path + "?" + urllib.parse.urlencode(kwargs)

    def get_object(self, request):
        self.queryDict = request.GET

        all_results = SearchQuerySet().all()
        facets = None

        if "selected_facets" in request.GET:
            facets = request.GET.getlist("selected_facets")

        if "q" in request.GET:
            self.query = request.GET["q"]
            results = all_results.filter(content=self.query)

            if facets:
                for facet in facets:
                    (facet_name, facet_value) = facet.split(":")
                    facet_name = facet_name.rsplit("_exact")[0]
                    results = results.narrow("%s:%s" % (facet_name, facet_value))
        elif facets:
            for facet in facets:
                (facet_name, facet_value) = facet.split(":")
                facet_name = facet_name.rsplit("_exact")[0]
                results = all_results.narrow("%s:%s" % (facet_name, facet_value))

        return results.order_by("-last_action_date")

    def title(self, obj):
        if self.query:
            title = (
                settings.SITE_META["site_name"]
                + ": Search for '"
                + self.query.capitalize()
                + "'"
            )
            # XXX: create a nice title based on all search parameters
        else:
            title = settings.SITE_META["site_name"] + ": Filtered Search"

        return title

    def link(self, obj):
        # return the main non-RSS search URL somehow
        # XXX maybe "quargs" - evz
        # return reverse('councilmatic_search', args=(searchqueryset=self.sqs,))
        url = self.url_with_querystring(
            reverse("{}:councilmatic_search_feed".format(settings.APP_NAME)),
            q=self.query,
        )
        return url

    def item_link(self, bill):
        return reverse("bill_detail", args=(bill.slug,))

    def item_pubdate(self, bill):
        return to_datetime(bill.last_action_date)

    def description(self, obj):
        return "Bills returned from search"

    def items(self, query):
        l_items = query[:20]
        pks = [i.pk for i in l_items]
        bills = self.bill_model.objects.filter(pk__in=pks).order_by("-last_action_date")
        return bills


class PersonDetailFeed(Feed):
    """The PersonDetailFeed provides an RSS feed for a given committee member,
    returning the most recent 20 bills for which they are the primary sponsor;
    and for each bill, the list of sponsores and the action history.
    """

    title_template = "feeds/person_detail_item_title.html"
    description_template = "feeds/person_detail_item_description.html"
    feed_type = Rss201rev2Feed
    NUM_RECENT_BILLS = 20

    def get_object(self, request, slug):
        o = Person.objects.get(slug=slug)
        return o

    def title(self, obj):
        return (
            settings.SITE_META["site_name"]
            + ": "
            + settings.CITY_VOCAB["COUNCIL_MEMBER"]
            + " %s: Recently Sponsored Bills" % obj.name
        )

    def link(self, obj):
        return reverse("person", args=(obj.slug,))

    def item_link(self, bill):
        # return the Councilmatic URL for the bill
        return reverse("bill_detail", args=(bill.slug,))

    def item_pubdate(self, bill):
        return to_datetime(bill.last_action_date)

    def description(self, obj):
        return "Recent sponsored bills from " + obj.name + "."

    def items(self, person):
        sponsored_bills = [s.bill for s in person.primary_sponsorships][:10]
        recent_sponsored_bills = sponsored_bills[: self.NUM_RECENT_BILLS]
        return recent_sponsored_bills


class CommitteeDetailEventsFeed(Feed):
    """The CommitteeDetailEventsFeed provides an RSS feed for a given committee,
    returning the most recent 20 events.
    """

    title_template = "feeds/committee_events_item_title.html"
    description_template = "feeds/committee_events_item_description.html"
    feed_type = Rss201rev2Feed
    NUM_RECENT_COMMITTEE_EVENTS = 20

    def get_object(self, request, slug):
        o = Organization.objects.get(slug=slug)
        return o

    def title(self, obj):
        return settings.SITE_META["site_name"] + ": " + obj.name + ": Recent Events"

    def link(self, obj):
        # return the Councilmatic URL for the committee
        return reverse("committee_detail", args=(obj.slug,))

    def item_link(self, event):
        # return the Councilmatic URL for the event
        return reverse("event_detail", args=(event.slug,))

    def item_pubdate(self, event):
        return event.start_time

    def description(self, obj):
        return "Events for committee %s" % obj.name

    def items(self, obj):
        return obj.recent_events.all()[: self.NUM_RECENT_COMMITTEE_EVENTS]


class CommitteeDetailActionFeed(Feed):
    """The CommitteeDetailActionFeed provides an RSS feed for a given committee,
    returning the most recent 20 actions on legislation.
    """

    # instead of defining item_title() or item_description(), use templates
    title_template = "feeds/committee_actions_item_title.html"
    description_template = "feeds/committee_actions_item_description.html"
    feed_type = Rss201rev2Feed
    NUM_RECENT_COMMITTEE_ACTIONS = 20

    def get_object(self, request, slug):
        o = Organization.objects.get(slug=slug)
        return o

    def title(self, obj):
        return settings.SITE_META["site_name"] + ": " + obj.name + ": Recent Actions"

    def link(self, obj):
        # return the Councilmatic URL for the committee
        return reverse("committee_detail", args=(obj.slug,))

    def item_link(self, action):
        # return the Councilmatic URL for the bill
        return reverse("bill_detail", args=(action.bill.slug,))

    def item_pubdate(self, action):
        return to_datetime(action.date_dt)

    def description(self, obj):
        return "Actions for committee %s" % obj.name

    def items(self, obj):
        return obj.recent_activity[: self.NUM_RECENT_COMMITTEE_ACTIONS]


class BillDetailActionFeed(Feed):
    """
    Return the last 20 actions for a given bill.
    """

    # instead of defining item_title() or item_description(), use templates
    title_template = "feeds/bill_actions_item_title.html"
    description_template = "feeds/bill_actions_item_description.html"
    feed_type = Rss201rev2Feed
    NUM_RECENT_BILL_ACTIONS = 20

    def get_object(self, request, slug):
        o = Bill.objects.get(slug=slug)
        return o

    def title(self, obj):
        return (
            settings.SITE_META["site_name"]
            + ": "
            + obj.friendly_name
            + ": Recent Actions"
        )

    def link(self, obj):
        # return the Councilmatic URL for the committee
        return reverse("bill_detail", args=(obj.slug,))

    def item_link(self, action):
        # Bill actions don't have their own pages, so just link to the Bill page (?)
        return reverse("bill_detail", args=(action.bill.slug,))

    def item_pubdate(self, action):
        return to_datetime(action.date_dt)

    def description(self, obj):
        return "Actions for bill %s" % obj.friendly_name

    def items(self, obj):
        return obj.ordered_actions[: self.NUM_RECENT_BILL_ACTIONS]


class EventsFeed(Feed):
    """
    Return the last 20 announced events as per, e.g.,
    https://nyc.councilmatic.org/events/
    """

    title_template = "feeds/events_item_title.html"
    description_template = "feeds/events_item_description.html"
    feed_type = Rss201rev2Feed
    NUM_RECENT_EVENTS = 20

    title = settings.CITY_COUNCIL_NAME + " " + "Recent Events"
    link = reverse_lazy("events")
    description = "Recently announced events."

    def item_link(self, event):
        # return the Councilmatic URL for the event
        return reverse("event_detail", args=(event.slug,))

    def item_pubdate(self, event):
        return event.start_time

    def description(self, obj):
        return "Events"

    def items(self, obj):
        return Event.objects.all()[: self.NUM_RECENT_EVENTS]
