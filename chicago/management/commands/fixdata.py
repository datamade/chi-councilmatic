from django.core.management.base import BaseCommand
from councilmatic_core.models import Action, Bill

class Command(BaseCommand):
    help = 'custom data fixes for Chicago'

    def handle(self, *args, **options):

        self.fix_action_dates()

    def fix_action_dates(self):
        bad_year = 3013
        
        wrong_actions = Action.objects.filter(date__year=bad_year).all()
        wrong_actions.delete()

        bills_to_update = Bill.objects.filter(last_action_date__year=bad_year).all()
        for b in bills_to_update:
            # update bill last_action_date with most recent action
            b.last_action_date = b.get_last_action_date()
            b.save()