import pytz
from datetime import datetime

from django.conf import settings
from haystack import indexes

from councilmatic_core.templatetags.extras import clean_html
from chicago.models import ChicagoBill


app_timezone = pytz.timezone(settings.TIME_ZONE)


class BillIndex(indexes.SearchIndex):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="search/indexes/councilmatic_core/bill_text.txt",
    )
    slug = indexes.CharField(model_attr="slug", indexed=False)
    id = indexes.CharField(model_attr="id", indexed=False)
    bill_type = indexes.CharField(faceted=True)
    identifier = indexes.CharField(model_attr="identifier")
    description = indexes.CharField(model_attr="title", boost=1.25)
    source_url = indexes.CharField(model_attr="sources__url", indexed=False)
    source_note = indexes.CharField(model_attr="sources__note")
    abstract = indexes.CharField(
        model_attr="abstracts__abstract", boost=1.25, default=""
    )

    friendly_name = indexes.CharField()
    sort_name = indexes.CharField()
    sponsorships = indexes.MultiValueField(faceted=True)
    actions = indexes.MultiValueField()
    controlling_body = indexes.MultiValueField(faceted=True)
    full_text = indexes.CharField(model_attr="full_text", default="")
    ocr_full_text = indexes.CharField(model_attr="ocr_full_text", default="")
    last_action_date = indexes.DateTimeField()
    inferred_status = indexes.CharField(faceted=True)
    legislative_session = indexes.CharField(faceted=True)
    topics = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return ChicagoBill

    def prepare(self, obj):
        data = super().prepare(obj)

        boost = 0

        if data["last_action_date"]:
            today = app_timezone.localize(datetime.now()).date()

            # data['last_action_date'] can be in the future
            weeks_passed = (today - data["last_action_date"]).days / 7 + 1

            boost = 1 + 1.0 / max(weeks_passed, 1)

        data["boost"] = boost

        return data

    def prepare_topics(self, obj):
        return obj.topics

    def prepare_last_action_date(self, obj):
        if not obj.last_action_date:
            action_dates = [a.date for a in obj.actions.all()]

            if action_dates:
                last_action_date = max(action_dates)
                return datetime.strptime(last_action_date, "%Y-%m-%d").date()

        else:
            return obj.last_action_date

    def prepare_sponsorships(self, obj):
        return [
            str(sponsorship.person)
            for sponsorship in obj.sponsorships.filter(primary=True)
        ]

    def prepare_actions(self, obj):
        return [str(action) for action in obj.actions.all()]

    def prepare_friendly_name(self, obj):
        return obj.friendly_name

    def prepare_sort_name(self, obj):
        return obj.friendly_name.replace(" ", "")

    def prepare_bill_type(self, obj):
        return obj.bill_type.lower()

    def prepare_controlling_body(self, obj):
        if obj.controlling_body:
            return [org.name for org in obj.controlling_body]

    def prepare_full_text(self, obj):
        return clean_html(obj.full_text)

    def prepare_inferred_status(self, obj):
        return obj.inferred_status

    def prepare_legislative_session(self, obj):
        return obj.legislative_session.identifier

    def prepare_ocr_full_text(self, obj):
        return clean_html(obj.ocr_full_text)

    def get_updated_field(self):
        return "updated_at"
