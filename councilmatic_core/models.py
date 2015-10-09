from django.db import models
from datetime import datetime
import pytz
from chi_city.city_config import TIMEZONE, OCD_CITY_COUNCIL_ID, CITY_COUNCIL_NAME

app_timezone = pytz.timezone(TIMEZONE)
now = datetime.now()

class Person(models.Model):
    ocd_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    headshot = models.CharField(max_length=255, blank=True)
    source_url = models.CharField(max_length=255)
    source_note = models.CharField(max_length=255, blank=True)
    website_url = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    @property
    def council_seat(self):
        return self.memberships.filter(organization__ocd_id=OCD_CITY_COUNCIL_ID).first().post.label

    @property
    def is_speaker(self):
        return True if self.memberships.filter(role='Speaker').first() else False   

    @property
    def headshot_url(self):
        if self.headshot:
            return '/static/images/' + self.ocd_id + ".jpg"
        else:
            return '/static/images/headshot_placeholder.png'

    @property
    def link_html(self):
        return '<a href="/person/'+self.slug+'" title="More on '+self.name+'">'+self.name+'</a>'

    @property
    def primary_sponsorships(self):
        return self.sponsorships.filter(is_primary=True)

class Bill(models.Model):
    ocd_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    identifier = models.CharField(max_length=50)
    bill_type = models.CharField(max_length=50)
    classification = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=None)
    date_updated = models.DateTimeField(default=None, null=True)
    source_url = models.CharField(max_length=255)
    source_note = models.CharField(max_length=255, blank=True)
    from_organization = models.ForeignKey('Organization', related_name='bills', null=True)
    full_text = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    last_action_date = models.DateTimeField(default=None, null=True)
    legislative_session = models.ForeignKey('LegislativeSession', related_name='bills', null=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.friendly_name

    @property
    def controlling_body(self):
        if self.current_action:
            related_orgs = self.current_action.related_entities.filter(entity_type='organization').all()
            if related_orgs:
                controlling_bodies = [Organization.objects.get(ocd_id=org.organization_ocd_id) for org in related_orgs]
                return controlling_bodies
            else:
                return [self.current_action.organization]
        else:
            return None

    @property
    def last_action_org(self):
        return self.current_action.organization if self.current_action else None

    @property
    def current_action(self):
        return self.actions.all().order_by('-order').first() if self.actions.all() else None

    @property
    def date_passed(self):
        return self.actions.filter(classification='executive-signature').order_by('-order').first().date if self.actions.all() else None

    @property
    def friendly_name(self):
        return None

    @property
    def primary_sponsor(self):
        return self.sponsorships.filter(is_primary=True).first()

    @property
    def committees_involved(self):
        if self.actions.all():
            orgs = set([a.organization.name for a in self.actions.all() if (a.organization.name !='Mayor' and a.organization.name != 'New York City Council')])
            if not orgs and self.controlling_body and self.controlling_body[0].name != CITY_COUNCIL_NAME:
                orgs = self.controlling_body
            return list(orgs)
        else:
            return None

    @property
    def inferred_status(self):
        return 'Active'

    @property
    def listing_description(self):
        if self.abstract:
            return self.abstract
        return self.description

    def get_last_action_date(self):
        return self.actions.all().order_by('-order').first().date if self.actions.all() else None

class Organization(models.Model):
    ocd_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    classification = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey('self', related_name='children', null=True)
    source_url = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def committees(cls):
        return cls.objects.filter(classification='committee').order_by('name').all()

    @property
    def recent_activity(self):
        return self.actions.order_by('-date', '-bill__identifier', '-order') if self.actions.all() else None

    @property
    def chairs(self):
        return self.memberships.filter(role='CHAIRPERSON')

    @property
    def link_html(self):
        # make link to committee if committee
        if self.classification == 'committee':
            return '<a href="/committee/'+self.slug+'">'+self.name+'</a>'
        # link to the council members page if its the council
        if self.classification == 'legislature':
            return '<a href="/council-members">'+self.name+'</a>'
        # just return text if executive
        else:
            return self.name

class Action(models.Model):
    date = models.DateTimeField(default=None)
    classification = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey('Organization', related_name='actions', null=True)
    bill = models.ForeignKey('Bill', related_name='actions', null=True)
    order = models.IntegerField()

    @property 
    def label(self):
        c = self.classification
        
        if c == 'committee-passage': return 'success'
        if c == 'passage': return 'success'
        if c == 'executive-signature': return 'success'
        if c == 'amendment-passage': return 'success'

        if c == 'amendment-introduction': return 'info'
        if c == 'introduction': return 'info'
        if c == 'committee-referral': return 'info'
        if c == 'filing': return 'info'
        if c == 'executive-received': return 'info'

        if c == 'deferred': return 'primary'

        else: return 'info'

class ActionRelatedEntity(models.Model):
    action = models.ForeignKey('Action', related_name='related_entities')
    entity_type = models.CharField(max_length=100)
    entity_name = models.CharField(max_length=255)
    organization_ocd_id = models.CharField(max_length=100, blank=True)
    person_ocd_id = models.CharField(max_length=100, blank=True)

class Post(models.Model):
    ocd_id = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    organization = models.ForeignKey('Organization', related_name='posts')

    @property
    def current_member(self):
        if self.memberships:
            most_recent_member = self.memberships.order_by('-start_date').first()
            if most_recent_member.end_date:
                return None
            else:
                return most_recent_member
        else:
            return None

class Membership(models.Model):
    organization = models.ForeignKey('Organization', related_name='memberships')
    person = models.ForeignKey('Person', related_name='memberships')
    post = models.ForeignKey('Post', related_name='memberships', null=True)
    label = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)

class Sponsorship(models.Model):
    bill = models.ForeignKey('Bill', related_name='sponsorships')
    person = models.ForeignKey('Person', related_name='sponsorships')
    classification = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return '{0} ({1})'.format(self.bill.identifier, self.person.name)

class Event(models.Model):
    ocd_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    classification = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    all_day = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    location_name = models.CharField(max_length=255)
    location_url = models.CharField(max_length=255, blank=True)
    source_url = models.CharField(max_length=255)
    source_note = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, unique=True)

    @property
    def event_page_url(self):
        return '/event/%s' %self.slug

    @property
    def clean_agenda_items(self):
        agenda_items = self.agenda_items.order_by('order').all()
        agenda_deduped = []
        for a in agenda_items:
            if a.description not in agenda_deduped:
                agenda_deduped.append(a.description)

        return agenda_deduped

    @classmethod
    def next_city_council_meeting(cls):
        return cls.objects.filter(name__icontains='City Council Stated Meeting').filter(start_time__gt=now).order_by('start_time').first()

    @classmethod
    def upcoming_committee_meetings(cls):
        return cls.objects.filter(start_time__gt=now).exclude(name='City Council Stated Meeting').exclude(name='City Council Stated Meeting ').order_by('start_time').all()[:3]

class EventParticipant(models.Model):
    event = models.ForeignKey('Event', related_name='participants')
    note = models.TextField()
    entity_name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=100)

class EventAgendaItem(models.Model):
    event = models.ForeignKey('Event', related_name='agenda_items')
    order = models.IntegerField()
    description = models.TextField()

class AgendaItemBill(models.Model):
    agenda_item = models.ForeignKey('EventAgendaItem', related_name='related_bills')
    bill = models.ForeignKey('Bill', related_name='related_agenda_items')
    note = models.CharField(max_length=255)

class Document(models.Model):
    note = models.TextField()
    url = models.TextField()

class BillDocument(models.Model):
    bill = models.ForeignKey('Bill', related_name='documents')
    document = models.ForeignKey('Document', related_name='bills')

class EventDocument(models.Model):
    event = models.ForeignKey('Event', related_name='documents')
    document = models.ForeignKey('Document', related_name='events')

class LegislativeSession(models.Model):
    identifier = models.CharField(max_length=255)
    jurisdiction_ocd_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

