from django.db import models
from councilmatic_core.models import Bill

class ChicagoBill(Bill):

    class Meta:
        proxy = True

    @property
    def friendly_name(self):
        nums = self.identifier.split(' ')[-1]
        return self.bill_type.title() + ' ' + nums

    def _terminal_status(self, history, bill_type):
        if history:
            if bill_type == 'ordinance':
                if 'passage' in history:
                    return 'Passed'
                elif 'failure' in history or 'committe-failure' in history:
                    return 'Failed'
            if bill_type in ['order', 'appointment','resolution']:
                if 'passage' in history:
                    return 'Approved'
                else:
                    return False

        return False

    # def _is_stale(self):
    # # stale = no action for 2 months
    #     if self.current_action:
    #         timediff = datetime.now().replace(tzinfo=app_timezone) - self.current_action.date
    #         return (timediff.days > 60)
    #     else:
    #         return True

    # def _is_approved(self):
    #     return 'Approved!'

    @property
    def inferred_status(self):
        actions = self.actions.all().order_by('-order')
        classification_hist = [a.classification for a in actions]
        bill_type = self.bill_type

        if self._terminal_status(classification_hist, bill_type):
            return self._terminal_status(classification_hist, bill_type)
        else:
            return 'Active'

    @property
    def listing_description(self):
        if self.abstract:
            return self.abstract
        else:
            return self.description
    
    