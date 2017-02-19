from django.shortcuts import render
from datetime import date, timedelta, datetime
from chicago.models import ChicagoBill, ChicagoEvent
from councilmatic_core.models import Action
from councilmatic_core.views import *
from django.conf import settings
from django.http import Http404

class ChicagoIndexView(IndexView):
    template_name = 'chicago/index.html'
    bill_model = ChicagoBill
    event_model = ChicagoEvent

    def last_meeting(self):
        return ChicagoEvent.objects\
                           .filter(name__exact=settings.CITY_COUNCIL_MEETING_NAME)\
                           .filter(start_time__lt=datetime.now())\
                           .latest('start_time')

    def date_cutoff(self):
        return self.last_meeting().start_time.date()

    def actions(self):
        return Action.actions_on_date(self.date_cutoff())

    def meeting_bills(self):
        return {a.bill for a in self.actions()}

    def meeting_bills_routine(self):
        return (b for b in self.meeting_bills() if 'Routine' in b.topics)

    def meeting_bills_nonroutine(self):
        return (b for b in self.meeting_bills() if 'Non-Routine' in b.topics)


    def new_bills(self):
        return ChicagoBill.new_bills_since(self.date_cutoff())

    def new_routine(self):
        return (b for b in self.new_bills() if 'Routine' in b.topics)

    def new_nonroutine(self):
        return (b for b in self.new_bills() if 'Non-Routine' in b.topics)

    def updated_bills(self):
        return ChicagoBill.updated_bills_since(self.date_cutoff())

    def updated_routine(self):
        return (b for b in self.updated_bills() if 'Routine' in b.topics)

    def updated_nonroutine(self):
        return (b for b in self.updated_bills() if 'Non-Routine' in b.topics)

    def topic_hierarchy(self):
        # getting topic counts for meeting bills
        topic_hierarchy = settings.TOPIC_HIERARCHY
        topic_tag_counts = {}
        for b in self.meeting_bills():
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
        
        # populating activity at last council meeting
        meeting_activity = {}
        meeting_activity['actions'] = self.actions
        meeting_activity['bills'] = self.meeting_bills
        meeting_activity['bills_routine'] = self.meeting_bills_routine
        meeting_activity['bills_nonroutine'] = self.meeting_bills_nonroutine
        

        # populating recent activitiy (since last council meeting)
        recent_activity = {}

        recent_activity['new'] = self.new_bills
        recent_activity['new_routine'] = self.new_routine
        recent_activity['new_nonroutine'] = self.new_nonroutine
        
        recent_activity['updated_routine'] = self.updated_routine
        recent_activity['updated_nonroutine'] = self.updated_nonroutine


        seo = {}
        seo.update(settings.SITE_META)
        seo['image'] = '/static/images/city_hall.jpg'

        return {
            'meeting_activity': meeting_activity,
            'recent_activity': recent_activity,
            'last_council_meeting': self.event_model.most_recent_past_city_council_meeting,
            'next_council_meeting': self.event_model.next_city_council_meeting,
            'upcoming_committee_meetings': self.event_model.upcoming_committee_meetings,
            'topic_hierarchy': self.topic_hierarchy,
            'seo': seo,
        }

class ChicagoAboutView(AboutView):
    template_name = 'chicago/about.html'

# this is for handling bill detail urls from the old chicago councilmatuc
def bill_detail_redirect(request, old_id):
    pattern = '?ID=%s&GUID' % old_id

    try:
        obj = ChicagoBill.objects.get(source_url__contains=pattern)
    except:
        raise Http404("No bill found matching the query")

    return redirect('bill_detail', slug=obj.slug, permanent=True)

def substitute_ordinance_redirect(request, substitute_ordinance_slug):
    return redirect('bill_detail', slug=substitute_ordinance_slug[1:], permanent=True)

class ChicagoBillDetailView(BillDetailView):
    template_name = 'chicago/legislation.html'
    
    model = ChicagoBill

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
        bill_classification = context['object'].classification
        if bill_classification in {'claim'}:
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
