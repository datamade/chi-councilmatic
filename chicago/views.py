from django.shortcuts import render
from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.urls import reverse

from datetime import date, timedelta, datetime

from chicago.models import ChicagoBill, ChicagoEvent
from councilmatic_core.views import *

from haystack.generic_views import FacetedSearchView
from haystack.query import SearchQuerySet

from django.db.models import DateTimeField
from django.db.models.functions import Cast

class ChicagoIndexView(IndexView):
    template_name = 'chicago/index.html'
    bill_model = ChicagoBill
    event_model = ChicagoEvent

    def last_meeting(self):
        return ChicagoEvent.most_recent_past_city_council_meeting()

    def date_cutoff(self):
        return self.last_meeting().start_time.date()

    def council_bills(self):
        return ChicagoBill.objects\
                          .filter(actions__date=self.date_cutoff(), from_organization__name=settings.OCD_CITY_COUNCIL_NAME)\
                          .prefetch_related('actions')

    def topic_hierarchy(self):
        # getting topic counts for meeting bills
        topic_hierarchy = settings.TOPIC_HIERARCHY
        topic_tag_counts = {}

        for b in self.council_bills():
            for topic in b.topics:
                try:
                    topic_tag_counts[topic] += 1
                except KeyError:
                    topic_tag_counts[topic] = 1
        # put together data blob for topic hierarchy
        for parent_blob in topic_hierarchy:
            parent_blob['count'] = 0
            for child_blob in parent_blob['children']:
                child_name = child_blob['name']
                child_blob['count'] = topic_tag_counts[child_name] if child_name in topic_tag_counts else 0
                parent_blob['count'] += child_blob['count']
                for gchild_blob in child_blob['children']:
                    gchild_name = gchild_blob['name']
                    gchild_blob['count'] = topic_tag_counts[gchild_name] if gchild_name in topic_tag_counts else 0

        return topic_hierarchy

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # Find activity at last council meeting
        council_bills = self.council_bills()
        context['council_bills'] = council_bills
        context['nonroutine_council_bills'] = [bill for bill in council_bills if 'Non-Routine' in bill.topics]

        # Find recent activitiy (since last council meeting)
        recent_bills = ChicagoBill.objects.filter(actions__date__gt=self.date_cutoff())
        context['recent_bills'] = recent_bills
        context['nonroutine_recent_bills'] = [bill for bill in recent_bills if 'Non-Routine' in bill.topics]

        seo = {}
        seo.update(settings.SITE_META)
        seo['image'] = '/static/images/city_hall.jpg'
        context['seo'] = seo

        context['last_council_meeting'] = self.event_model.most_recent_past_city_council_meeting
        context['next_council_meeting'] = self.event_model.next_city_council_meeting
        context['upcoming_committee_meetings'] = self.event_model.upcoming_committee_meetings
        context['topic_hierarchy'] = self.topic_hierarchy
        
        return context

class ChicagoAboutView(AboutView):
    template_name = 'chicago/about.html'

def substitute_ordinance_redirect(request, substitute_ordinance_slug):
    return redirect('bill_detail', slug=substitute_ordinance_slug[1:], permanent=True)

class ChicagoBillDetailView(BillDetailView):
    template_name = 'chicago/legislation.html'

    model = ChicagoBill

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']

        try:
            bill = self.model.objects.get(slug=slug)
            return super().dispatch(request, *args, **kwargs)
        except ChicagoBill.DoesNotExist:
            bill = None

        if not bill: 
            '''
            Chicago Councilmatic requires redirects for several old bill slugs:
            (1) original Councilmatic slug, which used the Legistar GUID
            (2) a mangled form: an added space, e.g.,  o-2018-2302 (old slug) vs. o2018-2302
            '''
            try:
                pattern = '?ID=%s&GUID' % slug
                bill = ChicagoBill.objects.get(sources__url__contains=pattern)
                return HttpResponsePermanentRedirect(reverse('bill_detail', args=[bill.slug]))
            except ChicagoBill.DoesNotExist:
                try: 
                    added_space = r'^([A-Za-z]+)-([-\d]+)$'
                    match_added_space = re.match(added_space, slug)
                    if match_added_space:
                        prefix = match_added_space.group(1)
                        remainder = match_added_space.group(2)
                        repaired_slug = '{prefix}{remainder}'.format(prefix=prefix, remainder=remainder)
                        bill = self.model.objects.get(slug=repaired_slug)                        
                        return HttpResponsePermanentRedirect(reverse('bill_detail', args=[bill.slug]))
                except ChicagoBill.DoesNotExist:
                    raise Http404

        raise Http404


    def get_object(self, queryset=None):
        """
        Returns a bill based on slug. If no bill found,
        looks for bills based on legistar id (so that
        urls from old Chicago councilmatic don't break)
        """

        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        # Try looking up by slug
        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No bill found matching the query")

        return obj

    def get_context_data(self, **kwargs):
        context = super(ChicagoBillDetailView, self).get_context_data(**kwargs)
        bill_classification, = context['object'].classification
        bill_identifier = context['object'].identifier
        if bill_classification in {'claim'} or bill_identifier=='Or 2013-382':
            context['seo']['nofollow'] = True
        return context

class ChicagoCouncilMembersView(CouncilMembersView):

    def get_seo_blob(self):
        seo = {}
        seo.update(settings.SITE_META)
        seo['site_desc'] = "Look up your local Alderman, and see what they're doing in your ward & your city"
        seo['image'] = '/static/images/chicago_map.jpg'
        seo['title'] = 'Wards & Aldermen - Chicago Councilmatic'

        return seo


class ChicagoCouncilmaticFacetedSearchView(FacetedSearchView):

    form_class = CouncilmaticSearchForm
    facet_fields = (
        'sponsorships',
        'controlling_body',
        'inferred_status',
        'topics',
        'legislative_session',
    )

    def dispatch(self, *args, **kwargs):
        # Raise an error if Councilmatic cannot connect to Solr.
        # Most likely, Solr is down and needs restarting.
        try:
            solr_url = settings.HAYSTACK_CONNECTIONS['default']['URL']
            requests.get(solr_url)
        except requests.ConnectionError:
            raise Exception("ConnectionError: Unable to connect to Solr at {}. Is Solr running?".format(solr_url))

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['q_filters'] = self._get_query_parameters()
        context['selected_facets'] = self._get_selected_facets()

        context['user_subscribed'] = False

        if settings.USING_NOTIFICATIONS:
            if self.request.user.is_authenticated:
                user = self.request.user

                search_params = {
                    'term': self.request.GET.get('q'),
                    'facets': selected_facets
                }

                try:
                    user.billsearchsubscriptions.get(user=user,
                                                     search_params__exact=search_params)
                    context['user_subscribed'] = True
                except BillSearchSubscription.DoesNotExist:
                    context['user_subscribed'] = False

        return context

    def get_queryset(self):
        sqs = super().get_queryset()

        sort_field = self.request.GET.get('sort_by', None)

        if sort_field in ('date', 'title'):  # relevance is default
            sort_order = self.request.GET.get('order_by', 'asc')
            sqs_field = {'date': 'last_action_date', 'title': 'sort_name_exact'}[sort_field]

            sqs = sqs.order_by('{0}{1}'.format('' if sort_order == 'asc' else '-', sqs_field))

        return sqs

    def _get_selected_facets(self):
        selected_facets = {}

        for val in self.request.GET.getlist("selected_facets"):
            if val:
                # e.g., bill_type_exact:ordinance -> bill_type, ordinance
                k, v = val.split('_exact:', 1)
                try:
                    selected_facets[k].append(v)
                except KeyError:
                    selected_facets[k] = [v]

        return selected_facets

    def _get_query_parameters(self):
        excluded_parameters = (
            'page',
            'selected_facets',
            'amp',
            '_',
        )
        query_parameters = [
            (param, val) for (param, val) in self.request.GET.items()
            if param not in excluded_parameters
        ]
        query_parameters += [
            ('selected_facets', param) for param in self.request.GET.getlist('selected_facets')
        ]

        if query_parameters:
            return urllib.parse.urlencode(query_parameters)

        return ''

class ChicagoPersonDetailView(PersonDetailView):
    template_name = 'chicago/person.html'

    def get_context_data(self, **kwargs):
        context = super(ChicagoPersonDetailView, self).get_context_data(**kwargs)

        person = context['person']

        if person.latest_council_membership:
            context['tenure_start'] = person.latest_council_membership.start_date_dt.strftime("%B %d, %Y")

        context['chair_positions'] = person.chair_role_memberships

        if person.slug in settings.CONTACT_INFO:
            context['phone'] = settings.CONTACT_INFO[person.slug]['phone']
            context['address'] = settings.CONTACT_INFO[person.slug]['address']
            context['twitter_handle'] = settings.CONTACT_INFO[person.slug]['twitter']['handle']
            context['twitter_url'] = settings.CONTACT_INFO[person.slug]['twitter']['url']

        return context

class EventDetailView(DetailView):
    model = ChicagoEvent
