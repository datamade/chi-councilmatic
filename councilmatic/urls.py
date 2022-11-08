from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
# from haystack.query import SearchQuerySet
from chicago.views import *
from chicago.feeds import *

patterns = ([
    url(r'^search/rss/',
        ChicagoCouncilmaticFacetedSearchFeed(), name='councilmatic_search_feed'),
    url(r'^search/', ChicagoCouncilmaticFacetedSearchView.as_view(), name='search'),
    url(r'^$', ChicagoIndexView.as_view(), name='index'),
    url(r'^about/$', ChicagoAboutView.as_view(), name='about'),
    url(r'^legislation/(?P<substitute_ordinance_slug>s[^/]+)/*$', substitute_ordinance_redirect, name='substitute_ordinance_redirect'),
    url(r'^legislation/(?P<slug>[^/]+)/$', ChicagoBillDetailView.as_view(), name='bill_detail'),
    url(r'^legislation/(?P<slug>[^/]+)/rss/$', ChicagoBillDetailActionFeed(), name='bill_detail_action_feed'),
    url(r'^council-members/$', ChicagoCouncilMembersView.as_view(), name='council_members'),
    url(r'^members/$', RedirectView.as_view(url='/council-members/', permanent=True), name='council_members'),
    url(r'^person/(?P<slug>[^/]+)/$', ChicagoPersonDetailView.as_view(), name='person'),
    url(r'^events/$', ChicagoEventsView.as_view(), name='events'),
], 'chicago')

urlpatterns = [
    url(r'', include(patterns)),
    url(r'^admin/', admin.site.urls),
    url(r'', include('councilmatic_core.urls')),
]