from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from chicago.views import (
    ChicagoCouncilmaticFacetedSearchView,
    ChicagoIndexView,
    ChicagoAboutView,
    ChicagoBillDetailView,
    ChicagoDividedVotesView,
    ChicagoPersonDetailView,
    ChicagoEventDetailView,
    ChicagoEventsView,
    ChicagoCouncilMembersView,
    ChicagoCouncilMembersCompareView,
    ChicagoCommitteeDetailView,
    ChicagoCommitteesView,
)
from chicago.feeds import (
    ChicagoBillDetailActionFeed,
    ChicagoCouncilmaticFacetedSearchFeed,
)

patterns = (
    [
        url(
            r"^search/rss/",
            ChicagoCouncilmaticFacetedSearchFeed(),
            name="councilmatic_search_feed",
        ),
        url(r"^search/", ChicagoCouncilmaticFacetedSearchView.as_view(), name="search"),
        url(r"^$", ChicagoIndexView.as_view(), name="index"),
        url(r"^about/$", ChicagoAboutView.as_view(), name="about"),
        url(
            r"^legislation/(?P<slug>[^/]+)/$",
            ChicagoBillDetailView.as_view(),
            name="bill_detail",
        ),
        url(
            r"^legislation/(?P<slug>[^/]+)/rss/$",
            ChicagoBillDetailActionFeed(),
            name="bill_detail_action_feed",
        ),
        url(
            r"^divided-votes/(?P<legislative_session>\w+)/$",
            ChicagoDividedVotesView.as_view(),
            name="divided_votes",
        ),
        url(r"^divided-votes/$", RedirectView.as_view(url="/divided-votes/2023/")),
        url(
            r"^compare-council-members/$",
            ChicagoCouncilMembersCompareView.as_view(),
            name="compare_council_members",
        ),
        url(
            r"^council-members/$",
            ChicagoCouncilMembersView.as_view(),
            name="council_members",
        ),
        url(
            r"^members/$",
            RedirectView.as_view(url="/council-members/", permanent=True),
            name="council_members",
        ),
        url(
            r"^person/(?P<slug>[^/]+)/$",
            ChicagoPersonDetailView.as_view(),
            name="person",
        ),
        url(
            r"^event/(?P<slug>[^/]+)/$",
            ChicagoEventDetailView.as_view(),
            name="event_detail",
        ),
        url(r"^events/$", ChicagoEventsView.as_view(), name="events"),
        url(
            r"^committee/(?P<slug>[^/]+)/$",
            ChicagoCommitteeDetailView.as_view(),
            name="committee_detail",
        ),
        url(r"^committees/$", ChicagoCommitteesView.as_view(), name="committees"),
    ],
    "chicago",
)

urlpatterns = [
    url(r"", include(patterns)),
    url(r"^admin/", admin.site.urls),
    url(r"", include("councilmatic_core.urls")),
]
