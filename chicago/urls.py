from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

import chicago.views as views
import chicago.feeds as feeds
from chicago.views_sitemaps import (
    EventSitemap,
    CommitteeSitemap,
    PersonSitemap,
    BillSitemap,
    StaticViewSitemap,
)

# to do: add static pages
sitemaps = {
    "meetings": EventSitemap,
    "committees": CommitteeSitemap,
    "people": PersonSitemap,
    "legislation": BillSitemap,
    "static": StaticViewSitemap,
}

patterns = [
    url(r"^search/", views.FacetedSearchView.as_view(), name="search"),
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^about/$", views.AboutView.as_view(), name="about"),
    url(
        r"^legislation/(?P<slug>[^/]+)/$",
        views.BillDetailView.as_view(),
        name="bill_detail",
    ),
    url(
        r"^divided-votes/(?P<legislative_session>\w+)/$",
        views.DividedVotesView.as_view(),
        name="divided_votes",
    ),
    url(r"^divided-votes/$", RedirectView.as_view(url="/divided-votes/2023/")),
    url(
        r"^compare-council-members/$",
        views.CouncilMembersCompareView.as_view(),
        name="compare_council_members",
    ),
    url(
        r"^council-members/$",
        views.CouncilMembersView.as_view(),
        name="council_members",
    ),
    url(
        r"^members/$",
        RedirectView.as_view(url="/council-members/", permanent=True),
        name="council_members",
    ),
    url(
        r"^person/(?P<slug>[^/]+)/$",
        views.PersonDetailView.as_view(),
        name="person",
    ),
    url(
        r"^event/(?P<slug>[^/]+)/$",
        views.EventDetailView.as_view(),
        name="event_detail",
    ),
    url(r"^events/$", views.EventsView.as_view(), name="events"),
    url(
        r"^committee/(?P<slug>[^/]+)/$",
        views.CommitteeDetailView.as_view(),
        name="committee_detail",
    ),
    url(r"^committees/$", views.CommitteesView.as_view(), name="committees"),
    url(r"^flush-cache/(.*)/$", views.flush, name="flush"),
    url(r"^pdfviewer/$", views.pdfviewer, name="pdfviewer"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        cache_page(86400)(sitemap_views.index),
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    path(
        "sitemap-<str:section>.xml",
        cache_page(86400)(sitemap_views.sitemap),
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
]

feed_patterns = [
    url(
        r"^search/rss/",
        feeds.FacetedSearchFeed(),
        name="councilmatic_search_feed",
    ),
    url(
        r"^legislation/(?P<slug>[^/]+)/rss/$",
        feeds.BillDetailActionFeed(),
        name="bill_detail_action_feed",
    ),
    url(
        r"^committee/(?P<slug>[^/]+)/events/rss/$",
        feeds.CommitteeDetailEventsFeed(),
        name="committee_detail_events_feed",
    ),
    url(
        r"^committee/(?P<slug>[^/]+)/actions/rss/$",
        feeds.CommitteeDetailActionFeed(),
        name="committee_detail_action_feed",
    ),
    url(r"^person/(?P<slug>[^/]+)/rss/$", feeds.PersonDetailFeed(), name="person_feed"),
    url(r"^events/rss/$", feeds.EventsFeed(), name="events_feed"),
]

urlpatterns = [
    url(r"", include(patterns)),
    url(r"", include(feed_patterns)),
    url(r"^admin/", admin.site.urls),
]
