from django.urls import reverse
from datetime import datetime
from django.conf import settings
from django.contrib.sitemaps import Sitemap

from councilmatic_core.models import Organization
from chicago.models import ChicagoBill, ChicagoEvent, ChicagoPerson


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ChicagoEvent.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("event_detail", args=[obj.slug])


class CommitteeSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Organization.committees()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("committee_detail", args=[obj.slug])


class PersonSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return (
            ChicagoPerson.objects.filter(
                memberships__organization__name=settings.OCD_CITY_COUNCIL_NAME
            )
            .filter(memberships__end_date__gt=datetime.now())
            .distinct()
        )

    def location(self, obj):
        return reverse("person", args=[obj.slug])


class BillSitemap(Sitemap):
    changefreq = "daily"
    priority = 1
    limit = 10000

    def items(self):
        return ChicagoBill.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("bill_detail", args=[obj.slug])


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["index", "about", "council_members", "chicago:compare_council_members"]

    def location(self, item):
        return reverse(item)
