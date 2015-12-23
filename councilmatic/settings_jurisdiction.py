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

# this is for populating meta tags
SITE_META = {
    'site_name' : 'Chicago Councilmatic',
    'site_desc' : 'Chicago City Council, demystified. Keep tabs on what your local representatives are up to.',
    'site_author' : 'PPF & DataMade',
    'site_url' : 'http://chicago.councilmatic.org',
    'twitter_site': '@ppolitics',
    'twitter_creator': '@DataMadeCo',
}

LEGISTAR_URL = 'https://chicago.legistar.com/Legislation.aspx'


# this is for the boundaries of municipal districts, to add 
# shapes to posts & ultimately display a map with the council
# member listing. the boundary set should be the relevant
# slug from the ocd api's boundary service
# available boundary sets here: http://ocd.datamade.us/boundary-sets/
BOUNDARY_SET = 'chicago-wards-2015'

# this is for configuring a map of council districts using data from the posts
# set MAP_CONFIG = None to hide map
MAP_CONFIG = {
    'center': [41.8369, -87.6847],
    'zoom': 11,
    'color': "#54afe8"
}


FOOTER_CREDITS = [
    {
        'name':     'DataMade',
        'url':      'http://datamade.us/',
        'image':    'datamade-logo.png',
    },
]

# this is the default text in search bars
SEARCH_PLACEHOLDER_TEXT = "police, zoning, O2015-7825, etc."



# these should live in APP_NAME/static/
IMAGES = {
    'favicon': 'images/favicon.ico',
    'logo': 'images/logo.png',
}



# by default, councilmatic will refer to a municipal district as 'District'
MUNICIPAL_DISTRICT_NAME = 'Ward'



# this is the name of the meetings where the entire city council meets
# as stored in legistar
CITY_COUNCIL_MEETING_NAME = 'City Council'

# this is the name of the role of committee chairs, e.g. 'CHAIRPERSON' or 'Chair'
# as stored in legistar
# if this is set, committees will display chairs
COMMITTEE_CHAIR_TITLE = 'Chairman'

# this is the anme of the role of committee members,
# as stored in legistar
COMMITTEE_MEMBER_TITLE = 'Member'



# this is for convenience, & used to populate a table
# describing legislation types on the about page template
LEGISLATION_TYPE_DESCRIPTIONS = [
    {
        'name': 'Ordinance',
        'search_term': 'Ordinance',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': '',

    },
]

# these keys should match committee slugs
COMMITTEE_DESCRIPTIONS = {
    "committee" :                  "committee description",
}
