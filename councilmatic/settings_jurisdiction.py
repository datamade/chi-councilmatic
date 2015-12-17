# These are all the settings that are specific to a jurisdiction

###############################
# These settings are required #
###############################

OCD_CITY_COUNCIL_ID = 'ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a'
CITY_COUNCIL_NAME = 'Chicago City Council'
OCD_JURISDICTION_ID = 'ocd-jurisdiction/country:us/state:il/place:chicago/government'
LEGISLATIVE_SESSIONS = ['2011', '2015'] # the last one in this list should be the current legislative session
CITY_NAME = 'Chicago'
CITY_NAME_SHORT = 'Chicago'

APP_NAME = 'chicago'


#########################
# The rest are optional #
#########################

LEGISTAR_URL = 'https://chicago.legistar.com/Legislation.aspx'

SITE_META = {
    'site_name' : 'Chicago Councilmatic',
    'site_desc' : 'Chicago City Council, demystified. Keep tabs on what your local representatives are up to.',
    'site_author' : 'PPF & DataMade',
    'site_url' : 'http://chicago.councilmatic.org',
    'twitter_site': '@ppolitics',
    'twitter_creator': '@DataMadeCo',
}

FOOTER_CREDITS = [
    {
        'name':     'DataMade',
        'url':      'http://datamade.us/',
        'image':    'datamade-logo.png',
    },
]

SEARCH_PLACEHOLDER_TEXT = "Taxi, Resolution 815-2015, etc."

LEGISLATION_TYPE_DESCRIPTIONS = [
    {
        'name': 'Ordinance',
        'search_term': 'Ordinance',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': '',

    },
]

# by default, councilmatic will refer to a municipal district as 'District'
MUNICIPAL_DISTRICT_NAME = 'Ward'

# this is the name of the meetings where the entire city council meets
CITY_COUNCIL_MEETING_NAME = 'City Council'

# this is the name of the role of committee chairs, e.g. 'CHAIRPERSON' or 'Chair'
# if this is set, committees will display chairs
COMMITTEE_CHAIR_TITLE = 'Chairman'

COMMITTEE_MEMBER_TITLE = 'Member'

# these keys should match committee slugs
COMMITTEE_DESCRIPTIONS = {
    "committee" :                  "committee description",
}
