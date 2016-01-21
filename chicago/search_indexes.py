from councilmatic_core.haystack_indexes import BillIndex
from haystack import indexes
from chicago.models import ChicagoBill
from datetime import datetime
from django.conf import settings
import pytz

app_timezone = pytz.timezone(settings.TIME_ZONE)

class ChicagoBillIndex(BillIndex, indexes.Indexable):

    topics = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return ChicagoBill

    def prepare(self, obj):
        data = super(ChicagoBillIndex, self).prepare(obj)
        
        boost = 0
        if obj.last_action_date:
            now = app_timezone.localize(datetime.now())
            weeks_passed = (now - obj.last_action_date).days / 7 + 1
            boost = 1 + 1.0 / max(weeks_passed, 1)

        data['boost'] = boost

        return data

    def prepare_topics(self, obj):
        return obj.topics
