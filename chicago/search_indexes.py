from councilmatic_core.haystack_indexes import BillIndex
from haystack import indexes
from chicago.models import ChicagoBill

class ChicagoBillIndex(BillIndex, indexes.Indexable):

	topics = indexes.MultiValueField(faceted=True)

	def get_model(self):
		return ChicagoBill

	def prepare_topics(self, obj):
		return obj.topics
