from haystack.backends.solr_backend import SolrEngine
from haystack.backends.solr_backend import SolrSearchBackend

class CouncilmaticSearchBackend(SolrSearchBackend):
    def build_search_kwargs(self, query_string, sort_by=None, start_offset=0, end_offset=None,
                            fields='', highlight=False, facets=None,
                            date_facets=None, query_facets=None,
                            narrow_queries=None, spelling_query=None,
                            within=None, dwithin=None, distance_point=None,
                            models=None, limit_to_registered_models=None,
                            result_class=None, stats=None, collate=None,
                            **extra_kwargs):

        kwargs = super().build_search_kwargs(query_string, sort_by=None, start_offset=0, end_offset=None,
                                             fields='', highlight=False, facets=None,
                                             date_facets=None, query_facets=None,
                                             narrow_queries=None, spelling_query=None,
                                             within=None, dwithin=None, distance_point=None,
                                             models=None, limit_to_registered_models=None,
                                             result_class=None, stats=None, collate=None,
                                             **extra_kwargs)

        kwargs['df'] = 'text'

        return kwargs

class CouncilmaticEngine(SolrEngine):
    backend = CouncilmaticSearchBackend
