from councilmatic_core.feeds import CouncilmaticFacetedSearchFeed, BillDetailActionFeed
from chicago.models import ChicagoBill

class ChicagoCouncilmaticFacetedSearchFeed(CouncilmaticFacetedSearchFeed):
    # same as CouncilmaticFacetedSearchFeed but have a better item name template which uses
    # NYCBill's friendly_name() as opposed to Bill's friendly_name()
    title_template = 'feeds/chicago_search_item_title.html'
    bill_model = ChicagoBill
    
class ChicagoBillDetailActionFeed(BillDetailActionFeed):
    title_template = 'feeds/chicago_bill_actions_item_title.html'
    
