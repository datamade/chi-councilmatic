from django.db import models
from councilmatic_core.models import Bill

class ChicagoBill(Bill):

    class Meta:
        proxy = True

    @property
    def friendly_name(self):
        nums = self.identifier.split(' ')[-1]
        return self.bill_type.title() + ' ' + nums

    @property
    def terminal_status(self):
        actions = self.actions.all()
        if actions:
            if self.bill_type in ['order', 'appointment','resolution', 'ordinance']:
                if 'passage' in [a.classification for a in actions]:
                    return 'Approved'
                else:
                    return False

        return False

    @property
    def is_stale(self):
    # stale = no action for 2 months
        if self.current_action:
            timediff = datetime.now().replace(tzinfo=app_timezone) - self.current_action.date
            return (timediff.days > 60)
        else:
            return True

    @property
    def is_approved(self):
        return 'Approved!'

    @property
    def inferred_status(self):
        if self.bill_type:
            return 'Active'

    @property
    def listing_description(self):
        if self.abstract:
            return self.abstract
        else:
            return self.description
    
    