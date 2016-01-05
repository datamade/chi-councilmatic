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
    'color': "#54afe8",
    'highlight_color': "#C00000",
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
    "committee-on-aviation" : "The Committee on Aviation has jurisdiction over matters relating to aviation and airports.",
    "committee-on-budget-and-government-operations" : "The Committee on the Budget and Government Operations has jurisdiction over the expenditure of all funds appropriated and expended by the City of Chicago. The Committee also has jurisdiction over all matters concerning the organization, reorganization and efficient management of City government, and federal and state legislation and administrative regulations in which the City may have an interest.",
    "committee-on-committees-rules-and-ethics" : "The Committee on Committees, Rules and Ethics has jurisdiction over the Rules of Order and Procedure, the procedures of the Council and its committees, including disputes over committee jurisdiction and referrals, ward redistricting, elections and referenda, committee assignments, the conduct of Council members, the provision of services to the City Council body; the City Clerk and council service agencies including the City Council Legislative Reference Bureau. The Committee is also responsible for the enforcement of the provisions of Chapter 2-156 and Section 2-56-050 of the Municipal Code of Chicago. The Committee also has jurisdiction with regard to all corrections to the Journal of the Proceedings of the City Council.",
    "committee-on-economic-capital-and-technology-development" : "The Committee on Economic, Capital and Technology Development has jurisdiction over those matters which directly affect the economic and technological expansion and development of the City and economic attraction to the City; and shall work with those public and private organizations that are similarly engaged. The Committee also has jurisdiction over the consideration, identification, goals, plan and approach to the annual and five year Capital Improvement Programs. The Committee may hold community hearings to determine the priorities to be considered in the formulation of such programs.",
    "committee-on-education-and-child-development" : "The Committee on Education and Child Development shall have jurisdiction over matters generally related to the City's Department of Family and Support Services, the development of children and adolescents, the education of the residents of the City of Chicago and matters generally affecting the Chicago Board of Education and Community College District Number 508.",
    "committee-on-energy-environmental-protection-and-public-utilities" : "",
    "committee-on-finance" : "The Committee on Finance has jurisdiction over tax levies, industrial revenue bonds, general obligation bonds and revenue bond programs, revenue orders, ordinances and resolutions, the financing of municipal services and capital developments; and matters generally affecting the Department on Finance, the City Comptroller, City Treasurer and Department of Revenue; and the solicitation of funds for charitable or other purposes on the streets and other public places. The Committee has jurisdiction over all matters pertaining to the audit and review of expenditures of funds appropriated by the Council or under the custody of the City Treasurer, all claims under the Illinois Workers' Compensation Act, the condominium refuse rebate program and all other pecuniary claims against the City or against funds over the custody of the City Treasurer. The Committee also has jurisdiction over all personnel matters relating to City Government.",
    "committee-on-health-and-environmental-protection" : "The Committee on Health and Environmental Protection shall have jurisdiction over health and sanitation matters affecting general health care, control of specific diseases, mental health, alcoholism and substance abuse, food, nutrition, and medical care of senior citizens and persons with disabilities, the Department of Health, the Bureau of Rodent Control and the Commission on Animal Care and Control. The Committee shall also have jurisdiction over all legislation relating to the abatement of air, water and noise pollution; solid waste collection and disposal; recycling and reuse of wastes; conservation of natural resources; and with all other matters not specifically included dealing with the improvement of the quality of the environment and the conservation of energy. The Committee shall also have jurisdiction over all ordinances, orders, resolutions and matters affecting public utilities with the exception of those matters over which jurisdiction is conferred herein upon the Committee on Transportation and Public Way.",
    "committee-on-housing-and-real-estate" : "The Committee on Housing and Real Estate has jurisdiction over all housing, redevelopment and neighborhood conservation matters and programs (except Zoning and Building Codes), City planning activities, development and conservation, matters generally affecting the Chicago Plan Commission, the City's housing agencies and the Department of Planning, City and Community Development. It also has jurisdiction over all acquisitions and dispositions of interest in real estate by the City, its agencies and departments. The Committee's jurisdiction includes all other acquisitions and dispositions of interest in real estate which the City Council is required to approve under state or federal law. The Committee has jurisdiction over all leases of real estate, or of space within buildings to which the City or any of its agencies, departments or offices, is a party.",
    "committee-on-human-relations" : "The Committee on Human Relations has jurisdiction over all matters relating to human rights and the Commission on Human Relations, and all matters generally affecting veterans of the Armed Forces of the United States of America.",
    "committee-on-license-and-consumer-protection" : "The Committee on License and Consumer Protection has jurisdiction over the licensing of persons, property, businesses and occupations and all matters relating to consumer protection, products liability, consumer fraud and all matters relating to the Department of Consumer Services.",
    "committee-on-pedestrian-and-traffic-safety" : "The Committee on Pedestrian and Traffic Safety shall have jurisdiction over all orders, ordinances, resolutions and matters relating to regulating vehicular, bicycle and pedestrian traffic, on or off street parking, public safety, highways, grade separations, protected bicycle lanes, Chicago bicycle and pedestrian plans and studies, Chicago metropolitan area traffic studies and highway development, and matters generally affecting the Bureau of Street Traffic and the Bureau of Parking, the Police Traffic Bureau, and public and private organizations dealing with traffic and bicycle and pedestrian safety.",
    "committee-on-public-safety" : "The Committee on Public Safety shall have jurisdiction over all matters relating to the Police Department, the Fire Department, the Office of Emergency Management and Communications, the Independent Police Review Authority, and matters affecting emergency city services generally (other than operation of emergency medical facilities), except those matters affecting collective bargaining agreements, employee benefits and pensions",
    "committee-on-special-events-cultural-affairs-and-recreation" : "The Committee on Special Events, Cultural Affairs and Recreation shall have jurisdiction over all special events and related programs of the City, including parades, fests, tastes, and community and neighborhood fairs. The Committee shall also have jurisdiction over those matters which affect the cultural growth of the City and its cultural institutions including matters generally affecting the Cultural Center of the Chicago Public Library. The Committee shall also have jurisdiction over all matters relating to the park system within the City, all matters generally affecting the Chicago Park District and all matters relating to the provision of recreational facilities within the City and shall work with those agencies, both public and private, that are similarly engaged.",
    "committee-on-transportation-and-public-way" : "The Committee on Transportation and Public Way has jurisdiction over all matters relating to the Chicago Transit Authority, the subways and the furnishing of public transportation within the City by any and all means of conveyance. The Committee has jurisdiction over all orders, ordinances and resolutions affecting street naming and layout, the City map, privileges in public ways, special assessments and matters generally affecting the Bureau of Maps and Plats or other agencies dealing with street and alley patterns and elevations, and the Board of Local Improvements.",
    "committee-on-workforce-development-and-audit" : "The Committee on Workforce Development and Audit shall have jurisdiction over the audit and review of expenditures of funds appropriated by the Council or under the custody of the City Treasurer, as well as management audits and other audits intended to examine the effectiveness or propriety of City operational procedures. The Committee's jurisdiction shall also include collective bargaining agreements regardless of bargaining unit and regardless of department; employee benefits; matters affecting pensions of city employees, regardless of pension fund; and all other personnel matters generally relating to the City government, excepting claims under the Workers' Compensation Act. The Committee's jurisdiction shall also include efforts intended to expand the city's private workforce and to create increased job opportunities in the city's private sector through business attraction efforts, business retention efforts, relocation services, incentive programs, training and retraining programs, or any other means.",
    "committee-on-zoning-landmarks-and-building-standards" : "The Committee on Zoning, Landmarks and Building Standards shall have jurisdiction over all zoning matters and the operation of the Zoning Board of Appeals and the office of the Zoning Administrator; land use policy generally and land use recommendations of the Chicago Plan Commission and the Department of Planning and Development; building code ordinances and matters generally affecting the Department of Buildings; and designation, maintenance and preservation of historical and architectural landmarks. The Committee shall work in cooperation with those public and private organizations similarly engaged in matters affecting landmarks.",
}

MANUAL_HEADSHOTS = {
    'oconnor-patrick':      'manual-headshots/oconnor-patrick.jpg',
    'austin-carrie-m':      'manual-headshots/austin-carrie-m.jpg',
    'burnett-jr-walter':    'manual-headshots/burnett-jr-walter.jpg',
    'solis-daniel':         'manual-headshots/solis-daniel.jpg',
    'munoz-ricardo':        'manual-headshots/munoz-ricardo.jpg',
    'burke-edward-m':       'manual-headshots/burke-edward-m.jpg',
    'cardenas-george-a':    'manual-headshots/cardenas-george-a.jpg',
    'beale-anthony':        'manual-headshots/beale-anthony.jpg',
    'moreno-proco-joe':     'manual-headshots/moreno-proco-joe.jpg',
    'emanuel-rahm':         'manual-headshots/emanuel-rahm.jpg',
    'hopkins-brian':        'manual-headshots/hopkins-brian.jpg',
    'burns-william-d':      'manual-headshots/burns-william-d.jpg',
    'sawyer-roderick-t':    'manual-headshots/sawyer-roderick-t.jpg',
    'mitchell-gregory-i':   'manual-headshots/mitchell-gregory-i.jpg',
    'sadlowski-garza-susan':'manual-headshots/sadlowski-garza-susan.jpg',
    'thompson-patrick-d':   'manual-headshots/thompson-patrick-d.jpg',
    'quinn-marty':          'manual-headshots/quinn-marty.jpg',
    'lopez-raymond-a':      'manual-headshots/lopez-raymond-a.jpg',
    'moore-david-h':        'manual-headshots/moore-david-h.jpg',
    'curtis-derrick-g':     'manual-headshots/curtis-derrick-g.jpg',
    'oshea-matthew-j':      'manual-headshots/oshea-matthew-j.jpg',
    'scott-jr-michael':     'manual-headshots/scott-jr-michael.jpg',
    'ervin-jason-c':        'manual-headshots/ervin-jason-c.jpg',
    'taliaferro-chris':     'manual-headshots/taliaferro-chris.jpg',
    'santiago-milagros-s':  'manual-headshots/santiago-milagros-s.jpg',
    'mell-deborah':         'manual-headshots/mell-deborah.jpg',
    'ramirez-rosa-carlos':  'manual-headshots/ramirez-rosa-carlos.jpg',
    'villegas-gilbert':     'manual-headshots/villegas-gilbert.jpg',
    'sposato-nicholas':     'manual-headshots/sposato-nicholas.jpg',
    'napolitano-anthony-v': 'manual-headshots/napolitano-anthony-v.jpg',
    'smith-michele':        'manual-headshots/smith-michele.jpg',
    'arena-john':           'manual-headshots/arena-john.jpg',
    'cappleman-james':      'manual-headshots/cappleman-james.jpg',
    'pawar-ameya':          'manual-headshots/pawar-ameya.jpg',
    'osterman-harry':       'manual-headshots/osterman-harry.jpg',
    'silverstein-debra-l':  'manual-headshots/silverstein-debra-l.jpg',
}
