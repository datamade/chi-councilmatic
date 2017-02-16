from django.conf import settings
from django.db import models
from django.utils.html import mark_safe
from councilmatic_core.models import Bill, Event
from datetime import datetime
import pytz
from .helpers import topic_classifier
import re
from urllib.parse import quote

app_timezone = pytz.timezone(settings.TIME_ZONE)

class ChicagoBill(Bill):

    class Meta:
        proxy = True

    def friendly_name(self):
        nums = self.identifier.split(' ')[-1]
        return self.bill_type.title() + ' ' + nums

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

    def listing_description(self):
        return self.description

    def topics(self):
        tags = topic_classifier(self.description)
        if 'Routine' in tags:
            tags.remove('Routine')
            tags = ['Routine'] + tags
        elif 'Non-Routine' in tags:
            tags.remove('Non-Routine')
            tags = ['Non-Routine'] + tags
        return tags

    def addresses(self):
        """
        returns a list of relevant addresses for a bill

        override this in custom subclass
        """
        if 'Ward Matters' in self.topics or 'City Matters' in self.topics:
            stname_pattern = "(\S*[a-z]\S*\s){1,4}?"
            sttype_pattern = "(ave|blvd|cres|ct|dr|hwy|ln|pkwy|pl|plz|rd|row|sq|st|ter|way)"
            st_pattern = stname_pattern + sttype_pattern

            # match 123 and 123-125, but not 123-125-127
            addr_pattern = r"((?<!-)\b\d{1,5}(-\d{1,5})?\s%s)" %st_pattern
            intersec_pattern = exp = "((?<=\sat\s)%s\s?and\s?%s)" %(st_pattern, st_pattern)

            pattern = "(%s|%s)" %(addr_pattern, intersec_pattern)

            matches = re.findall(pattern, self.description, re.IGNORECASE)

            addresses = [m[0] for m in matches]
            return addresses

        return []

    def full_text_doc_url(self):
        """
        override this if instead of having full text as string stored in
        full_text, it is a PDF document that you can embed on the page
        """
        base_url = 'https://pic.datamade.us/chicago/document/'
        # base_url = 'http://127.0.0.1:5000/chicago/document/'
        
        if self.documents.filter(document_type='V').all():
            legistar_doc_url = self.documents.filter(document_type='V').first().url
            doc_url = '{0}?filename={2}&document_url={1}'.format(base_url, 
                                                                 legistar_doc_url, 
                                                                 self.identifier)
            
            return doc_url
        else:
            return None

    def linked_description(self):
        # Sections
        description = re.sub(r'((Section)*s* *(\d{1,2}-\d{1,3}-\d+)\S*)',
                             r"<a href='https://chicagocode.org/\3/'>\1</a>",
                             self.description)

        # Chapters
        # 8 and 16-13
        description = re.sub(r'(\d{1,2}-\d{1,3} and )((\d{1,2})-\d{1,3})',
                             r"\1<a href='https://chicagocode.org/\3/\2/'>\2</a>",
                             description)
        # , 14-3, 12-1, 5-17 and
        description = re.sub(r'(?<=\d, )((\d{1,2})-\d{1,3})(?=, \d| and )',
                             r"<a href='https://chicagocode.org/\2/\1/'>\1</a>",
                             description)
        description = re.sub(r'(Chapters* ((\d{1,2})-\d{1,3}))',
                             r"<a href='https://chicagocode.org/\3/\2/'>\1</a>",
                             description)

        # Titles
        # 8 and 9
        description = re.sub(r'(\d{1,2} and )(\d{1,2})',
                             r"\1<a href='https://chicagocode.org/\2/'>\2</a>",
                             description)
        # , 3, 4, 4 and
        description = re.sub(r'(?<=\d, )(\d{1,2})(?=, \d| and )',
                             r"<a href='https://chicagocode.org/\1/'>\1</a>",
                             description)
        description = re.sub(r'(Titles* (\d{1,2}))',
                             r"<a href='https://chicagocode.org/\2/'>\1</a>",
                             description)

        return mark_safe(description)

class ChicagoEvent(Event):

    class Meta:
        proxy = True

    @classmethod
    def most_recent_past_city_council_meeting(cls):
        if hasattr(settings, 'CITY_COUNCIL_MEETING_NAME'):
            return cls.objects.filter(name__icontains=settings.CITY_COUNCIL_MEETING_NAME)\
                  .filter(start_time__lt=datetime.now()).filter(description='').order_by('-start_time').first()
        else:
            return None
