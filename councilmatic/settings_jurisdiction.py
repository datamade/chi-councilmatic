# These are all the settings that are specific to a jurisdiction

###############################
# These settings are required #
###############################

OCD_CITY_COUNCIL_ID = 'ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a'
CITY_COUNCIL_NAME = 'Chicago City Council'
OCD_JURISDICTION_ID = 'ocd-jurisdiction/country:us/state:il/place:chicago/government'
LEGISLATIVE_SESSIONS = ['2007', '2011', '2015'] # the last one in this list should be the current legislative session
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

APP_NAME = 'chicago'


#########################
# The rest are optional #
#########################

# this is for populating meta tags
SITE_META = {
    'site_name' : 'Chicago Councilmatic',
    'site_desc' : 'City Council, demystified. Keep tabs on Chicago legislation, aldermen, & meetings.',
    'site_author' : 'DataMade',
    'site_url' : 'https://chicago.councilmatic.org',
    'twitter_site': '@DataMadeCo',
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
    'zoom': 10,
    'color': "#54afe8",
    'highlight_color': "#C00000",
}


FOOTER_CREDITS = [
    {
        'name':     'DataMade',
        'url':      'http://datamade.us/',
        'image':    'datamade-logo.png',
    },
    {
        'name':     'Sunlight Foundation',
        'url':      'http://sunlightfoundation.org/',
        'image':    'sunlight-logo.png',
    },
]

# this is the default text in search bars
SEARCH_PLACEHOLDER_TEXT = "police, zoning, O2015-7825, etc."



# these should live in APP_NAME/static/
IMAGES = {
    'logo': 'images/logo.png',
}
# you can generate icons from the logo at http://www.favicomatic.com/
# & put them in APP_NAME/static/images/icons/




# THE FOLLOWING ARE VOCAB SETTINGS RELEVANT TO DATA MODELS, LOGIC
# (this is diff from VOCAB above, which is all for the front end)

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
        'desc': 'Ordinances are proposed changes to Chicago’s local laws. Some of these are changes to Chicago’s Municipal Code and others, called uncompiled statutes, are recorded in the Council’s Journal of Proceedings.',

    },
    {
        'name': 'Claim',
        'search_term': 'Claim',
        'fa_icon': 'dollar',
        'html_desc': True,
        'desc': "If you are harmed by the City of Chicago, you can make a claim against the City for your costs. Minor harms, like personal injury or automotive damage, are settled through City Council as Claims. If you sue the City for harm and come to a settlement, the settlement must also be approved by the Council.",

    },
    {
        'name': 'Resolution',
        'search_term': 'Resolution',
        'fa_icon': 'commenting-o',
        'html_desc': True,
        'desc': "Resolutions are typically symbolic, non-binding documents used for calling someone or some organization to take an action, statements announcing the City Council's intentions or honoring an individual.",

    },
    {
        'name': 'Order',
        'search_term': 'Order',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': "Orders direct a City Agency to do or not do something. They are typically used for ward matters like issuing business permits, designating parking zones and installing new signs and traffic signals.",

    },
    {
        'name': 'Appointment',
        'search_term': 'Appointment',
        'fa_icon': 'user',
        'html_desc': True,
        'desc': "Used for appointing individuals to positions within various official City of Chicago and intergovernmental boards.",

    },
    {
        'name': 'Report',
        'search_term': 'Report',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': "Submissions of official reports by departments, boards and sister agencies. ",

    },
    {
        'name': 'Communication',
        'search_term': 'Communication',
        'fa_icon': 'bullhorn',
        'html_desc': True,
        'desc': "Similar to reports and used for notifying City Council of intentions or actions.",

    },
    {
        'name': 'Oath Of Office',
        'search_term': 'Oath Of Office',
        'fa_icon': 'user',
        'html_desc': True,
        'desc': "Official swearing in of individuals to leadership positions at the City of Chicago, including Aldermen and board members.",

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

ABOUT_BLURBS = {
    "COMMITTEES" : "<p>Most meaningful legislative activity happens in committee meetings, where committee members debate proposed legislation. These meetings are open to the public.</p>\
                    <p>Each committee is has a Chair, who controls the committee meeting agenda (and thus, the legislation to be considered).</p>\
                    <p>Committee jurisdiction, memberships, and appointments all require City Council approval.</p>",
    "EVENTS":       "<p>There are two types of meetings: committee meetings and full city council meetings.</p>\
                    <p>Most of the time, meaningful legislative debate happens in committee meetings, which occur several times a month.</p>\
                    <p>Meetings of the entire City Council generally occur once a month at City Hall.</p>\
                    <p>All City Council meetings are open to public participation.</p>",
    "COUNCIL_MEMBERS": "" 
    
}

MANUAL_HEADSHOTS = {
    'arena-john':           {'source': '45th Ward Office', 'image': 'manual-headshots/arena-john.jpg' },
    'beale-anthony':        {'source': '@Alderman_Beale, Twitter', 'image': 'manual-headshots/beale-anthony.jpg' },
    'burns-william-d':      {'source': 'Masp360', 'image': 'manual-headshots/burns-william-d.jpg' },
    'cappleman-james':      {'source': 'james46.org', 'image': 'manual-headshots/cappleman-james.jpg' },
    'cochran-willie':       {'source': 'williebcochran.com', 'image': 'manual-headshots/cochran-willie.jpg' },
    'harris-michelle-a':    {'source': 'www.aldermanmichelleharris.net', 'image': 'manual-headshots/harris-michelle-a.jpg' },
    'mell-deborah':         {'source': 'www.33rdward.org', 'image': 'manual-headshots/mell-deborah.jpg' },
    'mitchell-gregory-i':   {'source': 'mitchellforalderman.com', 'image': 'manual-headshots/mitchell-gregory-i.jpg' },
    'moore-joseph':         {'source': 'participatorybudgeting49.wordpress.com', 'image': 'manual-headshots/moore-joseph.jpg' },
    'munoz-ricardo':        {'source': 'www.munoz22.com', 'image': 'manual-headshots/munoz-ricardo.jpg' },
    'napolitano-anthony-v': {'source': 'www.norwoodpark.org', 'image': 'manual-headshots/napolitano-anthony-v.jpg' },
    'oshea-matthew-j':      {'source': 'takebackchicago.org', 'image': 'manual-headshots/oshea-matthew-j.jpg' },
    'osterman-harry':       {'source': '48thward.org', 'image': 'manual-headshots/osterman-harry.jpg' },
    'ramirez-rosa-carlos':  {'source': 'www.aldermancarlosrosa.org', 'image': 'manual-headshots/ramirez-rosa-carlos.jpg' },
    'reboyras-ariel':       {'source': 'www.reboyras.com', 'image': 'manual-headshots/reboyras-ariel.jpg' },
    'sadlowski-garza-susan':{'source': 'calumetareaindustrial.com', 'image': 'manual-headshots/sadlowski-garza-susan.jpg' },
    'sawyer-roderick-t':    {'source': '@rodericktsawyer, Twitter', 'image': 'manual-headshots/sawyer-roderick-t.jpg' },
    'silverstein-debra-l':  {'source': 'ppiachicago.org', 'image': 'manual-headshots/silverstein-debra-l.jpg' },
    'solis-daniel':         {'source': 'ward25.com', 'image': 'manual-headshots/solis-daniel.jpg' },
    'taliaferro-chris':     {'source': 'Facebook', 'image': 'manual-headshots/taliaferro-chris.jpg' },
    'villegas-gilbert':     {'source': '@gilbert36ward, Twitter', 'image': 'manual-headshots/villegas-gilbert.jpg' },
    # 'moreno-proco-joe':     {'source': '', 'image': 'manual-headshots/moreno-proco-joe.jpg' },
    # 'waguespack-scott':     {'source': '', 'image': 'manual-headshots/waguespack-scott.jpg' },
    # 'zalewski-michael-r':   {'source': '', 'image': 'manual-headshots/zalewski-michael-r.jpg' },
    # 'austin-carrie-m':      {'source': '', 'image': 'manual-headshots/austin-carrie-m.jpg' },
    'thompson-patrick-d':   {'source': 'www.ward11.org', 'image': 'manual-headshots/thompson-patrick-d.jpg' },
    # 'tunney-thomas':        {'source': '', 'image': 'manual-headshots/tunney-thomas.jpg' },
    # 'brookins-jr-howard':   {'source': '', 'image': 'manual-headshots/brookins-jr-howard.jpg' },
    # 'burke-edward-m':       {'source': '', 'image': 'manual-headshots/burke-edward-m.jpg' },
    # 'burnett-jr-walter':    {'source': '', 'image': 'manual-headshots/burnett-jr-walter.jpg' },
    # 'cardenas-george-a':    {'source': '', 'image': 'manual-headshots/cardenas-george-a.jpg' },
    'curtis-derrick-g':     {'source': 'Chicago City Clerk', 'image': 'manual-headshots/curtis-derrick-g.jpg' },
    # 'dowell-pat':           {'source': '', 'image': 'manual-headshots/dowell-pat.jpg' },
    'ervin-jason-c':        {'source': '@aldermanervin, Twitter', 'image': 'manual-headshots/ervin-jason-c.jpg' },
    # 'foulkes-toni':         {'source': '', 'image': 'manual-headshots/foulkes-toni.jpg' },
    # 'hairston-leslie-a':    {'source': '', 'image': 'manual-headshots/hairston-leslie-a.jpg' },
    'hopkins-brian':        {'source': '@aldermanhopkins, Twitter', 'image': 'manual-headshots/hopkins-brian.jpg' },
    # 'laurino-margaret':     {'source': '', 'image': 'manual-headshots/laurino-margaret.jpg' },
    'lopez-raymond-a':      {'source': '@rlopez15thward, Twitter', 'image': 'manual-headshots/lopez-raymond-a.jpg' },
    # 'maldonado-roberto':    {'source': '', 'image': 'manual-headshots/maldonado-roberto.jpg' },
    # 'mitts-emma':           {'source': '', 'image': 'manual-headshots/mitts-emma.jpg' },
    'moore-david-h':        {'source': 'Chicago City Clerk', 'image': 'manual-headshots/moore-david-h.jpg' },
    # 'oconnor-patrick':      {'source': '', 'image': 'manual-headshots/oconnor-patrick.jpg' },
    'pawar-ameya':          {'source': 'chicago47.org', 'image': 'manual-headshots/pawar-ameya.jpg' },
    'quinn-marty':          {'source': 'Chicago City Clerk', 'image': 'manual-headshots/quinn-marty.jpg' },
    # 'reilly-brendan':       {'source': '', 'image': 'manual-headshots/reilly-brendan.jpg' },
    'santiago-milagros-s':  {'source': 'Chicago City Clerk', 'image': 'manual-headshots/santiago-milagros-s.jpg' },
    'scott-jr-michael':     {'source': 'citizensformichaelscottjr.com/', 'image': 'manual-headshots/scott-jr-michael.jpg' },
    'smith-michele':        {'source': '@aldermansmith43, Twitter', 'image': 'manual-headshots/smith-michele.jpg' },
    'sposato-nicholas':     {'source': 'aldermansposato.com', 'image': 'manual-headshots/sposato-nicholas.png' },
    'emanuel-rahm':         {'source': 'cityofchicago.org', 'image': 'manual-headshots/emanuel-rahm.jpg' },
    'mendoza-susana-a':     {'source': 'chicityclerk.com', 'image': 'manual-headshots/mendoza-susana-a.jpg' },
}


# notable positions that aren't district representatives, e.g. mayor & city clerk
# keys should match person slugs
EXTRA_TITLES = {
    'mendoza-susana-a': 'City Clerk',
    'emanuel-rahm': 'Mayor',
}


TOPIC_HIERARCHY = [
    {
        'name': 'Citywide matters',
        'children': [
            {
                'name': 'Municipal Code',
                'children': [],
            },
            {
                'name': 'City Business',
                'children': [   {'name': 'Getting and Giving Land'},
                                {'name': 'Intergovernmental Agreement'},
                                {'name': 'Lease Agreement'},
                                {'name': 'Vacation of Public Street'},],
            },
            {
                'name': 'Finances',
                'children': [ {'name': 'Bonds'} ],
            },
            {
                'name': 'Appointment',
                'children': [],
            },
            {
                'name': 'Oath of Office',
                'children': [],
            },
            {
                'name': 'Airports',
                'children': [],
            },
            {
                'name': 'Special Funds',
                'children': [   {'name': 'Open Space Impact Funds'} ],
            },
            {
                'name': 'Inspector General',
                'children': [],
            },
            {
                'name': 'Council Matters',
                'children': [   {'name': 'Call for Action'},
                                {'name': 'Transfer of Committee Funds'},
                                {'name': 'Correction of City Council Journal'},
                                {'name': 'Next Meeting'},],
            },
        ]

    },
    {
        'name': 'Ward matters',
        'children': [
            {
                'name': 'Business Permits and Privileges',
                'children': [   {'name': 'Grant of privilege in public way'},
                                {'name': 'Awnings'},
                                {'name': 'Sign permits'},
                                {'name': 'Physical barrier exemption'},
                                {'name': 'Canopy'}],
            },
            {
                'name': 'Residents',
                'children': [   {'name': 'Handicapped Parking Permit'},
                                {'name': 'Residential permit parking'},
                                {'name': 'Condo Refuse Claim'},
                                {'name': 'Senior citizen sewer refund'},],
            },
            {
                'name': 'Land Use',
                'children': [   {'name': 'Zoning Reclassification'},
                                {'name': 'Liquor and Package Store Restrictions'},],
            },
            {
                'name': 'Parking',
                'children': [   {'name': 'Loading/Standing/Tow Zone'},
                                {'name': 'Parking Restriction'},],
            },
            {
                'name': 'Economic Development',
                'children': [   {'name': 'Special Service Area'},
                                {'name': 'Tax Incentives'},
                                {'name': 'Tax Increment Financing'},],
            },
            {
                'name': 'Traffic',
                'children': [   {'name': 'Traffic signs and signals'},
                                {'name': 'Vehicle Weight Limitation'},],
            },
            {
                'name': 'Churches and Non-Profits',
                'children': [   {'name': 'Tag Day Permits'} ],
            },
            {
                'name': 'Redevelopment Agreement',
                'children': [],
            },
        ],
    },
    {
        'name': 'Individual matters',
        'children': [
            {
                'name': 'Small Claims',
                'children': [   {'name': 'Damage to vehicle claim'},
                                {'name': 'Damage to property claim'},
                                {'name': 'Settlement of Claims'},
                                {'name': 'Excessive water rate claim'},],
            },
            {
                'name': 'Honorifics',
                'children': [   {'name': 'Honorific Resolution'},
                                {'name': 'Honorary street'},],
            },
        ],
    }
]

