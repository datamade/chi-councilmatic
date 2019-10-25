from django.shortcuts import render
from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.urls import reverse

from datetime import date, timedelta, datetime

from chicago.models import ChicagoBill, ChicagoEvent
from councilmatic_core.views import *

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

class ChicagoCouncilmaticFacetedSearchView(CouncilmaticFacetedSearchView):

    def build_form(self, form_kwargs=None):
        form = super(CouncilmaticFacetedSearchView, self).build_form(form_kwargs=form_kwargs)

        # For faceted search functionality.
        if form_kwargs is None:
            form_kwargs = {}

        form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")

        # For remaining search functionality.
        data = None
        kwargs = {
            'load_all': self.load_all,
        }

        sqs = SearchQuerySet().facet('bill_type')\
                      .facet('sponsorships', sort='index')\
                      .facet('controlling_body')\
                      .facet('inferred_status')\
                      .facet('topics')\
                      .facet('legislative_session')\
                      .highlight()

        if form_kwargs:
            kwargs.update(form_kwargs)

        dataDict = {}
        if len(self.request.GET):
            data = self.request.GET
            dataDict = dict(data)

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = sqs

            if dataDict.get('sort_by'):
                for el in dataDict['sort_by']:
                    if el == 'date':
                        if dataDict.get('order_by') == ['asc']:
                            kwargs['searchqueryset'] = sqs.order_by('last_action_date')
                        else:
                            kwargs['searchqueryset'] = sqs.order_by('-last_action_date')
                    if el == 'title':
                        if dataDict.get('order_by') == ['desc']:
                            kwargs['searchqueryset'] = sqs.order_by('-sort_name')
                        else:
                            kwargs['searchqueryset'] = sqs.order_by('sort_name')
                    if el == 'relevance':
                        kwargs['searchqueryset'] = sqs

            elif dataDict.get('q'):
                kwargs['searchqueryset'] = sqs
            else:
                kwargs['searchqueryset'] = sqs.order_by('-last_action_date')

        return self.form_class(data, **kwargs)

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
