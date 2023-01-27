from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from chicago.models import ChicagoPerson, ChicagoPersonStatistic, ChicagoBill


class Command(BaseCommand):
    help = "populate statistics for Chicago Alders"

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

            bills = ChicagoBill.objects.filter(
                sponsorships__person=person, sponsorships__primary=True
            )

            non_routine_count = 0
            bills_passed = 0
            bills_failed = 0
            for b in bills:
                if "Non-Routine" in b.topics:
                    non_routine_count += 1

                if b.inferred_status == "Passed":
                    bills_passed += 1
                elif b.inferred_status == "Failed":
                    bills_failed += 1

            legislation_success_rate = "-"
            if bills_passed + bills_failed > 0:
                legislation_success_rate = "{:.0%}".format(
                    bills_passed / (bills_passed + bills_failed)
                )

            print(bills_passed, bills_failed, legislation_success_rate)
            p = ChicagoPersonStatistic(
                person=person,
                attendance_percent=person.attendance_percent,
                legislation_count=non_routine_count,
                legislation_success_rate=legislation_success_rate,
            )
            p.save()
