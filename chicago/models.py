from django.conf import settings
from django.db import models
from councilmatic_core.models import Bill
from datetime import datetime
import pytz
from .helpers import topic_classifier
import re

app_timezone = pytz.timezone(settings.TIME_ZONE)

class ChicagoBill(Bill):

    class Meta:
        proxy = True

    @property
    def friendly_name(self):
        nums = self.identifier.split(' ')[-1]
        return self.bill_type.title() + ' ' + nums

    @property
    def date_passed(self):
        return self.actions.filter(classification='passage').order_by('-order').first().date if self.actions.all() else None

    def _terminal_status(self, history, bill_type):
        if history:
            if bill_type.lower() == 'ordinance':
                if 'passage' in history:
                    return 'Passed'
                elif 'failure' in history or 'committe-failure' in history:
                    return 'Failed'
            if bill_type.lower() in ['order', 'appointment','resolution']:
                if 'passage' in history:
                    return 'Approved'
                else:
                    return False

        return False

    def _is_stale(self, last_action_date):
    # stale = no action for 5 months
        if last_action_date:
            timediff = datetime.now().replace(tzinfo=app_timezone) - last_action_date
            return (timediff.days > 180)
        else:
            return True

    @property
    def inferred_status(self):
        actions = self.actions.all().order_by('-order')
        classification_hist = [a.classification for a in actions]
        last_action_date = actions[0].date if actions else None
        bill_type = self.bill_type

        if bill_type.lower() in ['communication', 'oath of office']:
            return None
        if self._terminal_status(classification_hist, bill_type):
            return self._terminal_status(classification_hist, bill_type)
        elif self._is_stale(last_action_date):
            return 'Stale'
        else:
            return 'Active'

    @property
    def listing_description(self):
        if self.abstract:
            return self.abstract
        else:
            return self.description

    @property
    def topics(self):
        tags = topic_classifier(self.description)
        if 'Routine' in tags:
            tags.remove('Routine')
            tags = ['Routine'] + tags
        elif 'Non-Routine' in tags:
            tags.remove('Non-Routine')
            tags = ['Non-Routine'] + tags
        return tags

    @property
    def addresses(self):
        """
        returns a list of relevant addresses for a bill

        override this in custom subclass
        """
        if 'Ward Matters' in self.topics or 'City Matters' in self.topics:
            stname_pattern = "(\S*[a-z]\S*\s){1,4}?"
            sttype_pattern = "(ave|blvd|cres|ct|dr|hwy|ln|pkwy|pl|plz|rd|row|sq|st|ter|way)"
            st_pattern = stname_pattern + sttype_pattern

            addr_pattern = "(\d(\d|-)*\s%s)" %st_pattern
            intersec_pattern = exp = "((?<=\sat\s)%s\s?and\s?%s)" %(st_pattern, st_pattern)

            pattern = "(%s|%s)" %(addr_pattern, intersec_pattern)

            matches = re.findall(pattern, self.description, re.IGNORECASE)

            addresses = [m[0] for m in matches]
            return addresses

        return []

    @property
    def full_text_doc_url(self):
        """
        override this if instead of having full text as string stored in
        full_text, it is a PDF document that you can embed on the page
        """
        base_url = 'https://pic.datamade.us/chicago/document/?'
        legistar_doc_url = self.documents.filter(document_type='V').first().document.url
        return base_url+legistar_doc_url.split('?')[1]
