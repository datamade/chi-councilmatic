from django.core.management.base import BaseCommand
from chicago.models import ChicagoBill
from chicago.search_indexes import BillIndex
import pprint


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""

    help = "Preview the text template that will be used in the search."

    def add_arguments(self, parser):
        parser.add_argument(
            "identifier",
            help=(
                "The identifier of the bill to preview"
            ),
        )



    def handle(self, *args, **kwargs):

            


        b = ChicagoBill.objects.get(identifier=kwargs['identifier'])

        self.stdout.write(pprint.pformat(BillIndex().prepare(b), indent=4))

