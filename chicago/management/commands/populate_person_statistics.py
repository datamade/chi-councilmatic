from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from chicago.models import ChicagoPerson, ChicagoPersonStatistic


class Command(BaseCommand):
    help = "populate statistics for Chicago Aldermen"

    def handle(self, *args, **options):
        ChicagoPersonStatistic.objects.all().delete()

        people = (
            ChicagoPerson.objects.filter(
                memberships__organization__name=settings.OCD_CITY_COUNCIL_NAME
            )
            .filter(memberships__end_date__gt=datetime.now())
            .distinct()
        )

        for person in people:
            print("saving stats for", person.name)
            p = ChicagoPersonStatistic(
                person=person,
                attendance_percent=person.attendance_percent,
                legislation_count=person.legislation_count,
            )
            p.save()
