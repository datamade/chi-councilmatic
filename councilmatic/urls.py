from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from chicago.feeds import (
    ChicagoBillDetailActionFeed,
    ChicagoCouncilmaticFacetedSearchFeed,
)
from chicago.views import (
    AboutView,
    BillDetailView,
    CommitteeDetailView,
    CommitteesView,
    CouncilmaticFacetedSearchView,
    CouncilMembersCompareView,
    CouncilMembersView,
    DividedVotesView,
    EventDetailView,
    EventsView,
    IndexView,
    PersonDetailView,
)

patterns = (
    [
        url(
            r"^search/rss/",
            ChicagoCouncilmaticFacetedSearchFeed(),
            name="councilmatic_search_feed",
        ),
        url(r"^search/", CouncilmaticFacetedSearchView.as_view(), name="search"),
        url(r"^$", IndexView.as_view(), name="index"),
        url(r"^about/$", AboutView.as_view(), name="about"),
        url(
            r"^legislation/(?P<slug>[^/]+)/$",
            BillDetailView.as_view(),
            name="bill_detail",
        ),
        url(
            r"^legislation/(?P<slug>[^/]+)/rss/$",
            ChicagoBillDetailActionFeed(),
            name="bill_detail_action_feed",
        ),
        url(
            r"^divided-votes/(?P<legislative_session>\w+)/$",
            DividedVotesView.as_view(),
            name="divided_votes",
        ),
        url(r"^divided-votes/$", RedirectView.as_view(url="/divided-votes/2023/")),
        url(
            r"^compare-council-members/$",
            CouncilMembersCompareView.as_view(),
            name="compare_council_members",
        ),
        url(
            r"^council-members/$",
            CouncilMembersView.as_view(),
            name="council_members",
        ),
        url(
            r"^members/$",
            RedirectView.as_view(url="/council-members/", permanent=True),
            name="council_members",
        ),
        url(
            r"^person/(?P<slug>[^/]+)/$",
            PersonDetailView.as_view(),
            name="person",
        ),
        url(
            r"^event/(?P<slug>[^/]+)/$",
            EventDetailView.as_view(),
            name="event_detail",
        ),
        url(r"^events/$", EventsView.as_view(), name="events"),
        url(
            r"^committee/(?P<slug>[^/]+)/$",
            CommitteeDetailView.as_view(),
            name="committee_detail",
        ),
        url(r"^committees/$", CommitteesView.as_view(), name="committees"),
    ],
    "chicago",
)

urlpatterns = [
    url(r"", include(patterns)),
    url(r"^admin/", admin.site.urls),
    url(r"", include("councilmatic_core.urls")),
]
