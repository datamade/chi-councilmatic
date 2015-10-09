from councilmatic_core.haystack_indexes import BillIndex
from haystack import indexes
from chicago.models import ChicagoBill

class ChicagoBillIndex(BillIndex, indexes.Indexable):
    model = ChicagoBill
