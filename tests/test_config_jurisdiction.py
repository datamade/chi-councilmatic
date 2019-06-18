# These are all the settings that are specific to a jurisdiction

###############################
# These settings are required #
###############################

OCD_CITY_COUNCIL_NAME = 'Chicago City Council'
CITY_COUNCIL_NAME = 'Chicago City Council'
OCD_JURISDICTION_ID = 'ocd-jurisdiction/country:us/state:il/place:chicago/government'
LEGISLATIVE_SESSIONS = ['2007', '2011', '2015', '2019'] # the last one in this list should be the current legislative session
CITY_NAME = 'Chicago'
CITY_NAME_SHORT = 'Chicago'

# VOCAB SETTINGS FOR FRONT-END DISPLAY
CITY_VOCAB = {
    'MUNICIPAL_DISTRICT': 'Ward',       # e.g. 'District'
    'SOURCE': 'Chicago City Clerk',
    'COUNCIL_MEMBER': 'Alderman',       # e.g. 'Council Member'
    'COUNCIL_MEMBERS': 'Aldermen',      # e.g. 'Council Members'
    'EVENTS': 'Meetings',               # label for the events listing, e.g. 'Events'
}

APP_NAME = 'councilmatic_core'

CITY_COUNCIL_MEETING_NAME = 'City Council'

SITE_META = {
    'site_name' : 'Chicago Councilmatic',
    'site_desc' : 'City Council, demystified. Keep tabs on Chicago legislation, aldermen, & meetings.',
    'site_author' : 'DataMade',
    'site_url' : 'https://chicago.councilmatic.org',
    'twitter_site': '@DataMadeCo',
    'twitter_creator': '@DataMadeCo',
}

MAP_CONFIG = {}
CONTACT_INFO = {}
