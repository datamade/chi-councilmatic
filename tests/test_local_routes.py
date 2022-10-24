import logging

from django.urls import reverse
import pytest

from councilmatic_core.models import Person, Organization
from chicago.models import ChicagoBill, ChicagoEvent


logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="these shouldn't work on an empty db?")
@pytest.mark.parametrize('url_name', [
	'index',
	'about',
	'committees',
	'council_members',
	'events',
])
@pytest.mark.django_db
def test_listing_views(client, url_name):
	url = reverse(url_name)
	response = client.get(url)
	assert response.status_code == 200
	logger.info('{} OK'.format(url))


@pytest.mark.parametrize('url_name,model', [
	('person', Person),
	('committee_detail', Organization),
	('bill_detail', ChicagoBill),
	('event_detail', ChicagoEvent),
])
@pytest.mark.django_db
def test_detail_views(client, url_name, model):
	for p in model.objects.all():
		url = reverse(url_name, kwargs={'slug': p.slug})
		response = client.get(url)
		assert response.status_code == 200
		logger.info('{} OK'.format(url))


@pytest.mark.parametrize('url_name,model', [
	('committee_detail_events_feed', Organization),
	('committee_detail_action_feed', Organization),
	('bill_detail_action_feed', ChicagoBill),
	('person_feed', Person),
])
@pytest.mark.django_db
def test_feeds(client, url_name, model):
	for p in model.objects.all():
		url = reverse(url_name, kwargs={'slug': p.slug})
		response = client.get(url)
		assert response.status_code == 200
		logger.info('{} OK'.format(url))

