import datetime
import pytz

from django.conf import settings
from haystack.utils.highlighting import Highlighter


class ExactHighlighter(Highlighter):
    """
    This class customizes the Haystack Highlighter to allow for
    highlighting multi-word strings.
    https://django-haystack.readthedocs.io/en/master/highlighting.html#highlighter
    https://github.com/django-haystack/django-haystack/blob/master/haystack/utils/highlighting.py

    Use this class to build custom filters in `search_result.html`.
    See LA Metro as a model.
    """

    def __init__(self, query, **kwargs):
        super(Highlighter, self).__init__()
        self.query_words = self.make_query_words(query)

    def make_query_words(self, query):
        query_words = set()
        if query.startswith('"') and query.endswith('"'):
            query_words.add(query.strip('"'))
        else:
            query_words = set(
                [word.lower() for word in query.split() if not word.startswith("-")]
            )

        return query_words


def to_datetime(date, local=False):
    dt = datetime.datetime(date.year, date.month, date.day)

    if local:
        return pytz.timezone(settings.TIME_ZONE).localize(dt)

    else:
        return dt
