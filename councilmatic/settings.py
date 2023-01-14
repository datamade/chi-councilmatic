"""
Django settings for councilmatic project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import dj_database_url
from chicago.logging import before_send

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False if os.getenv("DJANGO_DEBUG", True) == "False" else True
allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", [])
ALLOWED_HOSTS = allowed_hosts.split(",") if allowed_hosts else []
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if DEBUG:
    # Add dynamically generated Docker IP
    # Don't do this in production!
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1"]

# Configure Sentry for error logging
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        before_send=before_send,
        integrations=[DjangoIntegration()],
    )

DATABASES = {}

DATABASES["default"] = dj_database_url.parse(
    os.getenv(
        "DATABASE_URL", "postgis://postgres:postgres@postgres:5432/chi_councilmatic"
    ),
    conn_max_age=600,
    engine="django.contrib.gis.db.backends.postgis",
    ssl_require=True if os.getenv("POSTGRES_REQUIRE_SSL") else False,
)

HAYSTACK_CONNECTIONS = {}
HAYSTACK_CONNECTIONS["default"] = {
    "ENGINE": "haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine",
    "URL": os.getenv("HAYSTACK_URL", "http://elasticsearch:9200"),
    "INDEX_NAME": "chicago",
    "SILENTLY_FAIL": False,
    "BATCH_SIZE": 10,
}

cache_backend = "dummy.DummyCache" if DEBUG is True else "db.DatabaseCache"
CACHES = {
    "default": {
        "BACKEND": f"django.core.cache.backends.{cache_backend}",
        "LOCATION": "site_cache",
    }
}


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "haystack",
    "chicago",
    "councilmatic_core",
    "opencivicdata.core",
    "opencivicdata.legislative",
    "notifications",
    "django_rq",
    "password_reset",
)

try:
    INSTALLED_APPS += EXTRA_APPS
except NameError:
    pass

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "councilmatic.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "councilmatic_core.views.city_context",
            ],
        },
    },
]


WSGI_APPLICATION = "councilmatic.wsgi.application"


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_ETAGS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Preserve default loggers
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}


RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 1,
        "PASSWORD": "",
        "DEFAULT_TIMEOUT": 360,
    }
}

# Enforce SSL in production
# if DEBUG is False:
#     SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
#     SECURE_SSL_REDIRECT = True

# These are all the settings that are specific to a jurisdiction

OCD_CITY_COUNCIL_NAME = "Chicago City Council"
CITY_COUNCIL_NAME = "Chicago City Council"
OCD_JURISDICTION_IDS = ["ocd-jurisdiction/country:us/state:il/place:chicago/government"]
LEGISLATIVE_SESSIONS = [
    "2007",
    "2011",
    "2015",
    "2019",
]  # the last one in this list should be the current legislative session
CITY_NAME = "Chicago"
CITY_NAME_SHORT = "Chicago"

# VOCAB SETTINGS FOR FRONT-END DISPLAY
CITY_VOCAB = {
    "MUNICIPAL_DISTRICT": "Ward",  # e.g. 'District'
    "SOURCE": "Chicago City Clerk",
    "COUNCIL_MEMBER": "Alderman",  # e.g. 'Council Member'
    "COUNCIL_MEMBERS": "Aldermen",  # e.g. 'Council Members'
    "EVENTS": "Meetings",  # label for the events listing, e.g. 'Events'
}

APP_NAME = "chicago"


#########################
# The rest are optional #

#########################

# this is for populating meta tags
SITE_META = {
    "site_name": "Chicago Councilmatic",
    "site_desc": "City Council, demystified. Keep tabs on Chicago legislation, aldermen, & meetings.",  # noqa
    "site_author": "DataMade",
    "site_url": "https://chicago.councilmatic.org",
    "twitter_site": "@DataMadeCo",
    "twitter_creator": "@DataMadeCo",
}

LEGISTAR_URL = "https://chicago.legistar.com/Legislation.aspx"


# this is for configuring a map of council districts using data from the posts
# set MAP_CONFIG = None to hide map
MAP_CONFIG = {
    "center": [41.8369, -87.6847],
    "zoom": 10,
    "color": "#54afe8",
    "highlight_color": "#C00000",
}

# this is the default text in search bars
SEARCH_PLACEHOLDER_TEXT = "police, zoning, O2015-7825, etc."


# THE FOLLOWING ARE VOCAB SETTINGS RELEVANT TO DATA MODELS, LOGIC
# (this is diff from VOCAB above, which is all for the front end)

# this is the name of the meetings where the entire city council meets
# as stored in legistar
CITY_COUNCIL_MEETING_NAME = "City Council"

# this is the name of the role of committee chairs, e.g. 'CHAIRPERSON' or 'Chair'
# as stored in legistar
# if this is set, committees will display chairs
COMMITTEE_CHAIR_TITLE = "Chairman"

# this is the anme of the role of committee members,
# as stored in legistar
COMMITTEE_MEMBER_TITLE = "Member"


COMMITTEE_VICE_CHAIR_TITLE = "Vice Chair"


# this is for convenience, & used to populate a table
# describing legislation types on the about page template
LEGISLATION_TYPE_DESCRIPTIONS = [
    {
        "name": "Ordinance",
        "search_term": "ordinance",
        "fa_icon": "file-text-o",
        "html_desc": True,
        "desc": "Ordinances are proposed changes to Chicago’s local laws. Some of these are changes to Chicago’s Municipal Code and others, called uncompiled statutes, are recorded in the Council’s Journal of Proceedings.",  # noqa
    },
    {
        "name": "Claim",
        "search_term": "claim",
        "fa_icon": "dollar",
        "html_desc": True,
        "desc": "If you are harmed by the City of Chicago, you can make a claim against the City for your costs. Minor harms, like personal injury or automotive damage, are settled through City Council as Claims. If you sue the City for harm and come to a settlement, the settlement must also be approved by the Council.",  # noqa
    },
    {
        "name": "Resolution",
        "search_term": "resolution",
        "fa_icon": "commenting-o",
        "html_desc": True,
        "desc": "Resolutions are typically symbolic, non-binding documents used for calling someone or some organization to take an action, statements announcing the City Council's intentions or honoring an individual.",  # noqa
    },
    {
        "name": "Order",
        "search_term": "order",
        "fa_icon": "file-text-o",
        "html_desc": True,
        "desc": "Orders direct a City Agency to do or not do something. They are typically used for ward matters like issuing business permits, designating parking zones and installing new signs and traffic signals.",  # noqa
    },
    {
        "name": "Appointment",
        "search_term": "appointment",
        "fa_icon": "user",
        "html_desc": True,
        "desc": "Used for appointing individuals to positions within various official City of Chicago and intergovernmental boards.",  # noqa
    },
    {
        "name": "Report",
        "search_term": "report",
        "fa_icon": "file-text-o",
        "html_desc": True,
        "desc": "Submissions of official reports by departments, boards and sister agencies. ",  # noqa
    },
    {
        "name": "Communication",
        "search_term": "communication",
        "fa_icon": "bullhorn",
        "html_desc": True,
        "desc": "Similar to reports and used for notifying City Council of intentions or actions.",  # noqa
    },
    {
        "name": "Oath Of Office",
        "search_term": "oath of office",
        "fa_icon": "user",
        "html_desc": True,
        "desc": "Official swearing in of individuals to leadership positions at the City of Chicago, including Aldermen and board members.",  # noqa
    },
]

# these keys should match committee slugs
COMMITTEE_DESCRIPTIONS = {
    "committee-on-aviation": "The Committee on Aviation has jurisdiction over matters relating to aviation and airports.",  # noqa
    "committee-on-budget-and-government-operations": "The Committee on the Budget and Government Operations has jurisdiction over the expenditure of all funds appropriated and expended by the City of Chicago. The Committee also has jurisdiction over all matters concerning the organization, reorganization and efficient management of City government, and federal and state legislation and administrative regulations in which the City may have an interest.",  # noqa
    "committee-on-committees-rules-and-ethics": "The Committee on Committees, Rules and Ethics has jurisdiction over the Rules of Order and Procedure, the procedures of the Council and its committees, including disputes over committee jurisdiction and referrals, ward redistricting, elections and referenda, committee assignments, the conduct of Council members, the provision of services to the City Council body; the City Clerk and council service agencies including the City Council Legislative Reference Bureau. The Committee is also responsible for the enforcement of the provisions of Chapter 2-156 and Section 2-56-050 of the Municipal Code of Chicago. The Committee also has jurisdiction with regard to all corrections to the Journal of the Proceedings of the City Council.",  # noqa
    "committee-on-economic-capital-and-technology-development": "The Committee on Economic, Capital and Technology Development has jurisdiction over those matters which directly affect the economic and technological expansion and development of the City and economic attraction to the City; and shall work with those public and private organizations that are similarly engaged. The Committee also has jurisdiction over the consideration, identification, goals, plan and approach to the annual and five year Capital Improvement Programs. The Committee may hold community hearings to determine the priorities to be considered in the formulation of such programs.",  # noqa
    "committee-on-education-and-child-development": "The Committee on Education and Child Development shall have jurisdiction over matters generally related to the City's Department of Family and Support Services, the development of children and adolescents, the education of the residents of the City of Chicago and matters generally affecting the Chicago Board of Education and Community College District Number 508.",  # noqa
    "committee-on-energy-environmental-protection-and-public-utilities": "",
    "committee-on-finance": "The Committee on Finance has jurisdiction over tax levies, industrial revenue bonds, general obligation bonds and revenue bond programs, revenue orders, ordinances and resolutions, the financing of municipal services and capital developments; and matters generally affecting the Department on Finance, the City Comptroller, City Treasurer and Department of Revenue; and the solicitation of funds for charitable or other purposes on the streets and other public places. The Committee has jurisdiction over all matters pertaining to the audit and review of expenditures of funds appropriated by the Council or under the custody of the City Treasurer, all claims under the Illinois Workers' Compensation Act, the condominium refuse rebate program and all other pecuniary claims against the City or against funds over the custody of the City Treasurer. The Committee also has jurisdiction over all personnel matters relating to City Government.",  # noqa
    "committee-on-health-and-environmental-protection": "The Committee on Health and Environmental Protection shall have jurisdiction over health and sanitation matters affecting general health care, control of specific diseases, mental health, alcoholism and substance abuse, food, nutrition, and medical care of senior citizens and persons with disabilities, the Department of Health, the Bureau of Rodent Control and the Commission on Animal Care and Control. The Committee shall also have jurisdiction over all legislation relating to the abatement of air, water and noise pollution; solid waste collection and disposal; recycling and reuse of wastes; conservation of natural resources; and with all other matters not specifically included dealing with the improvement of the quality of the environment and the conservation of energy. The Committee shall also have jurisdiction over all ordinances, orders, resolutions and matters affecting public utilities with the exception of those matters over which jurisdiction is conferred herein upon the Committee on Transportation and Public Way.",  # noqa
    "committee-on-housing-and-real-estate": "The Committee on Housing and Real Estate has jurisdiction over all housing, redevelopment and neighborhood conservation matters and programs (except Zoning and Building Codes), City planning activities, development and conservation, matters generally affecting the Chicago Plan Commission, the City's housing agencies and the Department of Planning, City and Community Development. It also has jurisdiction over all acquisitions and dispositions of interest in real estate by the City, its agencies and departments. The Committee's jurisdiction includes all other acquisitions and dispositions of interest in real estate which the City Council is required to approve under state or federal law. The Committee has jurisdiction over all leases of real estate, or of space within buildings to which the City or any of its agencies, departments or offices, is a party.",  # noqa
    "committee-on-human-relations": "The Committee on Human Relations has jurisdiction over all matters relating to human rights and the Commission on Human Relations, and all matters generally affecting veterans of the Armed Forces of the United States of America.",  # noqa
    "committee-on-license-and-consumer-protection": "The Committee on License and Consumer Protection has jurisdiction over the licensing of persons, property, businesses and occupations and all matters relating to consumer protection, products liability, consumer fraud and all matters relating to the Department of Consumer Services.",  # noqa
    "committee-on-pedestrian-and-traffic-safety": "The Committee on Pedestrian and Traffic Safety shall have jurisdiction over all orders, ordinances, resolutions and matters relating to regulating vehicular, bicycle and pedestrian traffic, on or off street parking, public safety, highways, grade separations, protected bicycle lanes, Chicago bicycle and pedestrian plans and studies, Chicago metropolitan area traffic studies and highway development, and matters generally affecting the Bureau of Street Traffic and the Bureau of Parking, the Police Traffic Bureau, and public and private organizations dealing with traffic and bicycle and pedestrian safety.",  # noqa
    "committee-on-public-safety": "The Committee on Public Safety shall have jurisdiction over all matters relating to the Police Department, the Fire Department, the Office of Emergency Management and Communications, the Independent Police Review Authority, and matters affecting emergency city services generally (other than operation of emergency medical facilities), except those matters affecting collective bargaining agreements, employee benefits and pensions",  # noqa
    "committee-on-special-events-cultural-affairs-and-recreation": "The Committee on Special Events, Cultural Affairs and Recreation shall have jurisdiction over all special events and related programs of the City, including parades, fests, tastes, and community and neighborhood fairs. The Committee shall also have jurisdiction over those matters which affect the cultural growth of the City and its cultural institutions including matters generally affecting the Cultural Center of the Chicago Public Library. The Committee shall also have jurisdiction over all matters relating to the park system within the City, all matters generally affecting the Chicago Park District and all matters relating to the provision of recreational facilities within the City and shall work with those agencies, both public and private, that are similarly engaged.",  # noqa
    "committee-on-transportation-and-public-way": "The Committee on Transportation and Public Way has jurisdiction over all matters relating to the Chicago Transit Authority, the subways and the furnishing of public transportation within the City by any and all means of conveyance. The Committee has jurisdiction over all orders, ordinances and resolutions affecting street naming and layout, the City map, privileges in public ways, special assessments and matters generally affecting the Bureau of Maps and Plats or other agencies dealing with street and alley patterns and elevations, and the Board of Local Improvements.",  # noqa
    "committee-on-workforce-development-and-audit": "The Committee on Workforce Development and Audit shall have jurisdiction over the audit and review of expenditures of funds appropriated by the Council or under the custody of the City Treasurer, as well as management audits and other audits intended to examine the effectiveness or propriety of City operational procedures. The Committee's jurisdiction shall also include collective bargaining agreements regardless of bargaining unit and regardless of department; employee benefits; matters affecting pensions of city employees, regardless of pension fund; and all other personnel matters generally relating to the City government, excepting claims under the Workers' Compensation Act. The Committee's jurisdiction shall also include efforts intended to expand the city's private workforce and to create increased job opportunities in the city's private sector through business attraction efforts, business retention efforts, relocation services, incentive programs, training and retraining programs, or any other means.",  # noqa
    "committee-on-zoning-landmarks-and-building-standards": "The Committee on Zoning, Landmarks and Building Standards shall have jurisdiction over all zoning matters and the operation of the Zoning Board of Appeals and the office of the Zoning Administrator; land use policy generally and land use recommendations of the Chicago Plan Commission and the Department of Planning and Development; building code ordinances and matters generally affecting the Department of Buildings; and designation, maintenance and preservation of historical and architectural landmarks. The Committee shall work in cooperation with those public and private organizations similarly engaged in matters affecting landmarks.",  # noqa
}

ABOUT_BLURBS = {
    "COMMITTEES": "<p>Most meaningful legislative activity happens in committee meetings, where committee members debate proposed legislation. These meetings are open to the public.</p><p>Each committee has a Chair, who controls the committee meeting agenda (and thus, the legislation to be considered).</p><p>Committee jurisdiction, memberships, and appointments all require City Council approval.</p>",  # noqa
    "EVENTS": "<p>There are two types of meetings: committee meetings and full city council meetings.</p><p>Most of the time, meaningful legislative debate happens in committee meetings, which occur several times a month.</p><p>Meetings of the entire City Council generally occur once a month at City Hall.</p><p>All City Council meetings are open to public participation.</p>",  # noqa
    "COUNCIL_MEMBERS": "",
}

# notable positions that aren't district representatives, e.g. mayor & city clerk
# keys should match person slugs
EXTRA_TITLES = {
    "mendoza-susana-a-a465109bd96a": "City Clerk",
    "emanuel-rahm-3af71de0e6ca": "Mayor",
    "lightfoot-lori-e-f6faf37c9643": "Mayor",
    "valencia-anna-m-257a68ccbc17": "City Clerk",
}

ALDER_EXTRAS = {
    "abarca-anabel": {"image": "abarca-anabel.jpg"},
    "arena-john": {"image": "arena-john.jpg"},
    "austin-carrie-m": {
        "image": "austin-carrie-m.jpg",
        "election-status": "Indicted, Retiring",
        "caucus": "Black Caucus",
    },
    "beale-anthony": {"image": "beale-anthony.jpg", "caucus": "Black Caucus"},
    "brookins-jr-howard": {"image": "brookins-jr-howard.jpg", "caucus": "Black Caucus"},
    "burke-edward-m": {
        "image": "burke-edward-m.jpg",
        "election-status": "Indicted, Retiring",
    },
    "burnett-jr-walter": {"image": "burnett-jr-walter.jpg", "caucus": "Black Caucus"},
    "burns-william-d": {"image": "burns-william-d.jpg"},
    "cappleman-james": {
        "image": "cappleman-james.jpg",
        "election-status": "Retiring",
        "caucus": "LGBT Caucus",
    },
    "cardenas-george-a": {"image": "cardenas-george-a.jpg", "caucus": "Latino Caucus"},
    "cardona-jr-felix": {
        "image": "cardona-jr-felix.jpg",
        "caucus": "Latino Caucus, Progressive Caucus",
    },
    "cochran-willie": {"image": "cochran-willie.jpg"},
    "coleman-stephanie-d": {
        "image": "coleman-stephanie-d.jpg",
        "caucus": "Black Caucus, Progressive Caucus",
    },
    "curtis-derrick-g": {"image": "curtis-derrick-g.jpg", "caucus": "Black Caucus"},
    "dowell-pat": {"image": "dowell-pat.jpg", "caucus": "Black Caucus"},
    "emanuel-rahm": {"image": "emanuel-rahm.jpg"},
    "ervin-jason-c": {"image": "ervin-jason-c.jpg", "caucus": "Black Caucus"},
    "foulkes-toni": {"image": "foulkes-toni.jpg"},
    "gardiner-james-m": {"image": "gardiner-james-m.jpg"},
    "hadden-maria-e": {
        "image": "hadden-maria-e.jpg",
        "caucus": "Black Caucus, Progressive Caucus, LGBT Caucus",
    },
    "hairston-leslie-a": {
        "image": "hairston-leslie-a.jpg",
        "election-status": "Retiring",
        "caucus": "Black Caucus, Progressive Caucus",
    },
    "harris-michelle-a": {"image": "harris-michelle-a.jpg", "caucus": "Black Caucus"},
    "hopkins-brian": {"image": "hopkins-brian.jpg"},
    "king-sophia": {
        "image": "king-sophia.jpg",
        "election-status": "Running for Mayor, not seeking re-election",
        "caucus": "Black Caucus, Progressive Caucus",
    },
    "knudsen-timothy-r": {"image": "knudsen-timothy-r.jpg", "caucus": "LGBT Caucus"},
    "la-spata-daniel": {
        "image": "la-spata-daniel.jpg",
        "caucus": "Democratic Socialist, Latino Caucus, Progressive Caucus",
    },
    "laurino-margaret": {"image": "laurino-margaret.jpg"},
    "lee-nicole-t": {"image": "lee-nicole-t.jpg"},
    "lopez-raymond-a": {"image": "lopez-raymond-a.jpg", "caucus": "LGBT Caucus"},
    "lightfoot-lori-e": {"image": "lightfoot-lori-e.jpg"},
    "maldonado-roberto": {
        "image": "maldonado-roberto.jpg",
        "election-status": "Retiring",
        "caucus": "Latino Caucus",
    },
    "martin-matthew-j": {
        "image": "martin-matthew-j.jpg",
        "caucus": "Black Caucus, Progressive Caucus",
    },
    "mell-deborah": {"image": "mell-deborah.jpg"},
    "mendoza-susana-a": {"image": "mendoza-susana-a.jpg"},
    "mitchell-gregory-i": {"image": "mitchell-gregory-i.jpg", "caucus": "Black Caucus"},
    "mitts-emma": {"image": "mitts-emma.jpg", "caucus": "Black Caucus"},
    "moore-david-h": {
        "image": "moore-david-h.jpg",
        "caucus": "Black Caucus, Progressive Caucus",
    },
    "moore-joseph": {"image": "moore-joseph.jpg"},
    "moreno-proco-joe": {"image": "moreno-proco-joe.jpg"},
    "munoz-ricardo": {"image": "munoz-ricardo.jpg"},
    "napolitano-anthony-v": {"image": "napolitano-anthony-v.jpg"},
    "nugent-samantha": {"image": "nugent-samantha.jpg"},
    "oconnor-patrick": {"image": "oconnor-patrick.jpg"},
    "oshea-matthew-j": {"image": "oshea-matthew-j.jpg"},
    "osterman-harry": {"image": "osterman-harry.jpg", "election-status": "Retiring"},
    "pawar-ameya": {"image": "pawar-ameya.jpg"},
    "quinn-marty": {"image": "quinn-marty.jpg"},
    "ramirez-rosa-carlos": {
        "image": "ramirez-rosa-carlos.jpg",
        "caucus": "Democratic Socialist, Latino Caucus, Progressive Caucus, LGBT Caucus",  # noqa
    },
    "reboyras-ariel": {
        "image": "reboyras-ariel.jpg",
        "caucus": "Latino Caucus",
        "election-status": "Retiring",
    },
    "reilly-brendan": {"image": "reilly-brendan.jpg"},
    "rodriguez-michael-d": {
        "image": "rodriguez-michael-d.jpg",
        "caucus": "Latino Caucus, Progressive Caucus",
    },
    "rodriguez-sanchez-rossana": {
        "image": "rodriguez-sanchez-rossana.jpg",
        "caucus": "Democratic Socialist, Latino Caucus, Progressive Caucus",
    },
    "sadlowski-garza-susan": {
        "image": "sadlowski-garza-susan.jpg",
        "election-status": "Retiring",
        "caucus": "Latino Caucus, Progressive Caucus",
    },
    "santiago-milagros-s": {"image": "santiago-milagros-s.jpg"},
    "sawyer-roderick-t": {
        "image": "sawyer-roderick-t.jpg",
        "election-status": "Running for Mayor, not seeking re-election",
        "caucus": "Black Caucus, Progressive Caucus",
    },
    "scott-jr-michael": {"image": "scott-jr-michael.jpg", "caucus": "Black Caucus"},
    "scott-monique-l": {"image": "scott-monique-l.jpg", "caucus": "Black Caucus"},
    "sigcho-lopez-byron": {
        "image": "sigcho-lopez-byron.jpg",
        "caucus": "Democratic Socialist, Latino Caucus, Progressive Caucus",
    },
    "silverstein-debra-l": {"image": "silverstein-debra-l.jpg"},
    "smith-michele": {"image": "smith-michele.jpg", "election-status": "Retiring"},
    "solis-daniel": {"image": "solis-daniel.jpg"},
    "sposato-nicholas": {"image": "sposato-nicholas.png"},
    "tabares-silvana": {"image": "tabares-silvana.jpg", "caucus": "Latino Caucus"},
    "taliaferro-chris": {
        "image": "taliaferro-chris.jpg",
        "caucus": "Progressive Caucus",
    },
    "taylor-jeanette-b": {
        "image": "taylor-jeanette-b.jpg",
        "caucus": "Black Caucus, Democratic Socialist, Progressive Caucus",
    },
    "thompson-patrick-d": {"image": "thompson-patrick-d.jpg"},
    "tunney-thomas": {
        "image": "tunney-thomas.jpg",
        "election-status": "Retiring",
        "caucus": "LGBT Caucus",
    },
    "valencia-anna-m": {"image": "valencia-anna-m.jpg"},
    "vasquez-jr-andre": {
        "image": "vasquez-jr-andre.jpg",
        "caucus": "Latino Caucus, Progressive Caucus",
    },
    "villegas-gilbert": {"image": "villegas-gilbert.jpg", "caucus": "Latino Caucus"},
    "waguespack-scott": {
        "image": "waguespack-scott.jpg",
        "caucus": "Progressive Caucus",
    },
    "zalewski-michael-r": {"image": "zalewski-michael-r.jpg"},
}

TOPIC_HIERARCHY = [
    {
        "name": "Citywide matters",
        "children": [
            {
                "name": "Municipal Code",
                "children": [],
            },
            {
                "name": "City Business",
                "children": [
                    {"name": "Getting and Giving Land"},
                    {"name": "Intergovernmental Agreement"},
                    {"name": "Lease Agreement"},
                    {"name": "Vacation of Public Street"},
                ],
            },
            {
                "name": "Finances",
                "children": [{"name": "Bonds"}],
            },
            {
                "name": "Appointment",
                "children": [],
            },
            {
                "name": "Oath of Office",
                "children": [],
            },
            {
                "name": "Airports",
                "children": [],
            },
            {
                "name": "Special Funds",
                "children": [{"name": "Open Space Impact Funds"}],
            },
            {
                "name": "Inspector General",
                "children": [],
            },
            {
                "name": "Council Matters",
                "children": [
                    {"name": "Call for Action"},
                    {"name": "Transfer of Committee Funds"},
                    {"name": "Correction of City Council Journal"},
                    {"name": "Next Meeting"},
                ],
            },
        ],
    },
    {
        "name": "Ward matters",
        "children": [
            {
                "name": "Business Permits and Privileges",
                "children": [
                    {"name": "Grant of privilege in public way"},
                    {"name": "Awnings"},
                    {"name": "Sign permits"},
                    {"name": "Physical barrier exemption"},
                    {"name": "Canopy"},
                ],
            },
            {
                "name": "Residents",
                "children": [
                    {"name": "Handicapped Parking Permit"},
                    {"name": "Residential permit parking"},
                    {"name": "Condo Refuse Claim"},
                    {"name": "Senior citizen sewer refund"},
                ],
            },
            {
                "name": "Land Use",
                "children": [
                    {"name": "Zoning Reclassification"},
                    {"name": "Liquor and Package Store Restrictions"},
                ],
            },
            {
                "name": "Parking",
                "children": [
                    {"name": "Loading/Standing/Tow Zone"},
                    {"name": "Parking Restriction"},
                ],
            },
            {
                "name": "Economic Development",
                "children": [
                    {"name": "Special Service Area"},
                    {"name": "Tax Incentives"},
                    {"name": "Tax Increment Financing"},
                ],
            },
            {
                "name": "Traffic",
                "children": [
                    {"name": "Traffic signs and signals"},
                    {"name": "Vehicle Weight Limitation"},
                ],
            },
            {
                "name": "Churches and Non-Profits",
                "children": [{"name": "Tag Day Permits"}],
            },
            {
                "name": "Redevelopment Agreement",
                "children": [],
            },
        ],
    },
    {
        "name": "Individual matters",
        "children": [
            {
                "name": "Small Claims",
                "children": [
                    {"name": "Damage to vehicle claim"},
                    {"name": "Damage to property claim"},
                    {"name": "Settlement of Claims"},
                    {"name": "Excessive water rate claim"},
                ],
            },
            {
                "name": "Honorifics",
                "children": [
                    {"name": "Honorific Resolution"},
                    {"name": "Honorary street"},
                ],
            },
        ],
    },
]

USING_NOTIFICATIONS = False
