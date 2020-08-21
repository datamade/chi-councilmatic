from datetime import datetime

from councilmatic_core.haystack_indexes import BillIndex
from django.conf import settings
from haystack import indexes
import pytz

from chicago.models import ChicagoBill


app_timezone = pytz.timezone(settings.TIME_ZONE)


class ChicagoBillIndex(BillIndex, indexes.Indexable):

    topics = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return ChicagoBill

    def prepare(self, obj):
        data = super(ChicagoBillIndex, self).prepare(obj)

        boost = 0

        if data['last_action_date']:
            today = app_timezone.localize(datetime.now()).date()

            # data['last_action_date'] can be in the future
            weeks_passed = (today - data['last_action_date']).days / 7 + 1

            boost = 1 + 1.0 / max(weeks_passed, 1)

        data['boost'] = boost

        return data

    def prepare_topics(self, obj):
        return obj.topics

    def prepare_last_action_date(self, obj):
        if not obj.last_action_date:
            action_dates = [a.date for a in obj.actions.all()]

            if action_dates:
                last_action_date = max(action_dates)
                return datetime.strptime(last_action_date, '%Y-%m-%d').date()

        return obj.last_action_date.date()
