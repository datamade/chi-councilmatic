from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Populate SearchBill fulltext index"""

    help = "Populate SearchBill fulltext index"

    def handle(self, *args, **kwargs):

        self.stdout.write("SearchBill populated!")
