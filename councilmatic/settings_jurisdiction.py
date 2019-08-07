# These are all the settings that are specific to a jurisdiction

###############################
# These settings are required #
###############################

OCD_CITY_COUNCIL_NAME = 'Chicago City Council'
CITY_COUNCIL_NAME = 'Chicago City Council'
OCD_JURISDICTION_IDS = ['ocd-jurisdiction/country:us/state:il/place:chicago/government']
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


COMMITTEE_VICE_CHAIR_TITLE = 'Vice Chair'




# this is for convenience, & used to populate a table
# describing legislation types on the about page template
LEGISLATION_TYPE_DESCRIPTIONS = [
    {
        'name': 'Ordinance',
        'search_term': 'ordinance',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': 'Ordinances are proposed changes to Chicago’s local laws. Some of these are changes to Chicago’s Municipal Code and others, called uncompiled statutes, are recorded in the Council’s Journal of Proceedings.',

    },
    {
        'name': 'Claim',
        'search_term': 'claim',
        'fa_icon': 'dollar',
        'html_desc': True,
        'desc': "If you are harmed by the City of Chicago, you can make a claim against the City for your costs. Minor harms, like personal injury or automotive damage, are settled through City Council as Claims. If you sue the City for harm and come to a settlement, the settlement must also be approved by the Council.",

    },
    {
        'name': 'Resolution',
        'search_term': 'resolution',
        'fa_icon': 'commenting-o',
        'html_desc': True,
        'desc': "Resolutions are typically symbolic, non-binding documents used for calling someone or some organization to take an action, statements announcing the City Council's intentions or honoring an individual.",

    },
    {
        'name': 'Order',
        'search_term': 'order',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': "Orders direct a City Agency to do or not do something. They are typically used for ward matters like issuing business permits, designating parking zones and installing new signs and traffic signals.",

    },
    {
        'name': 'Appointment',
        'search_term': 'appointment',
        'fa_icon': 'user',
        'html_desc': True,
        'desc': "Used for appointing individuals to positions within various official City of Chicago and intergovernmental boards.",

    },
    {
        'name': 'Report',
        'search_term': 'report',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': "Submissions of official reports by departments, boards and sister agencies. ",

    },
    {
        'name': 'Communication',
        'search_term': 'communication',
        'fa_icon': 'bullhorn',
        'html_desc': True,
        'desc': "Similar to reports and used for notifying City Council of intentions or actions.",

    },
    {
        'name': 'Oath Of Office',
        'search_term': 'oath of office',
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
                    <p>Each committee has a Chair, who controls the committee meeting agenda (and thus, the legislation to be considered).</p>\
                    <p>Committee jurisdiction, memberships, and appointments all require City Council approval.</p>",
    "EVENTS":       "<p>There are two types of meetings: committee meetings and full city council meetings.</p>\
                    <p>Most of the time, meaningful legislative debate happens in committee meetings, which occur several times a month.</p>\
                    <p>Meetings of the entire City Council generally occur once a month at City Hall.</p>\
                    <p>All City Council meetings are open to public participation.</p>",
    "COUNCIL_MEMBERS": ""

}

MANUAL_HEADSHOTS = {
    'arena-john-d9a11334830d':           {'source': '45th Ward Office', 'image': 'manual-headshots/arena-john.jpg' },
    'beale-anthony-d125d27369f3':        {'source': '@Alderman_Beale, Twitter', 'image': 'manual-headshots/beale-anthony.jpg' },
    'burns-william-d-74409520db8c':      {'source': 'Masp360', 'image': 'manual-headshots/burns-william-d.jpg' },
    'cappleman-james-7b6638b78d83':      {'source': 'james46.org', 'image': 'manual-headshots/cappleman-james.jpg' },
    'cochran-willie-b6cc52d2933a':       {'source': 'williebcochran.com', 'image': 'manual-headshots/cochran-willie.jpg' },
    'harris-michelle-a-c9d7f4375894':    {'source': 'www.aldermanmichelleharris.net', 'image': 'manual-headshots/harris-michelle-a.jpg' },
    'mell-deborah-5fa778d13b51':         {'source': 'www.33rdward.org', 'image': 'manual-headshots/mell-deborah.jpg' },
    'mitchell-gregory-i-1d481a8e2acd':   {'source': 'mitchellforalderman.com', 'image': 'manual-headshots/mitchell-gregory-i.jpg' },
    'moore-joseph-3c9ae7316619':         {'source': 'participatorybudgeting49.wordpress.com', 'image': 'manual-headshots/moore-joseph.jpg' },
    'munoz-ricardo-79203ae83471':        {'source': 'www.munoz22.com', 'image': 'manual-headshots/munoz-ricardo.jpg' },
    'napolitano-anthony-v-7ab5df04527e': {'source': 'www.norwoodpark.org', 'image': 'manual-headshots/napolitano-anthony-v.jpg' },
    'oshea-matthew-j-5071e1c58184':      {'source': 'takebackchicago.org', 'image': 'manual-headshots/oshea-matthew-j.jpg' },
    'osterman-harry-550e6f30c87c':       {'source': '48thward.org', 'image': 'manual-headshots/osterman-harry.jpg' },
    'ramirez-rosa-carlos-b67e026bf1e5':  {'source': 'www.aldermancarlosrosa.org', 'image': 'manual-headshots/ramirez-rosa-carlos.jpg' },
    'reboyras-ariel-0ebeb178852e':       {'source': 'www.reboyras.com', 'image': 'manual-headshots/reboyras-ariel.jpg' },
    'sadlowski-garza-susan-ef8b7a07f272':{'source': 'calumetareaindustrial.com', 'image': 'manual-headshots/sadlowski-garza-susan.jpg' },
    'sawyer-roderick-t-a6e5d5f2bba5':    {'source': '@rodericktsawyer, Twitter', 'image': 'manual-headshots/sawyer-roderick-t.jpg' },
    'silverstein-debra-l-173bbaa057f6':  {'source': 'ppiachicago.org', 'image': 'manual-headshots/silverstein-debra-l.jpg' },
    'solis-daniel-b0bd981415f9':         {'source': 'ward25.com', 'image': 'manual-headshots/solis-daniel.jpg' },
    'taliaferro-chris-7646256e8079':     {'source': 'Facebook', 'image': 'manual-headshots/taliaferro-chris.jpg' },
    'villegas-gilbert-8c9f813ce0a9':     {'source': '@gilbert36ward, Twitter', 'image': 'manual-headshots/villegas-gilbert.jpg' },
    'thompson-patrick-d-aabd3b898af9':   {'source': 'www.ward11.org', 'image': 'manual-headshots/thompson-patrick-d.jpg' },
    'curtis-derrick-g-dc2702c16bce':     {'source': 'Chicago City Clerk', 'image': 'manual-headshots/curtis-derrick-g.jpg' },
    'ervin-jason-c-a6bd57bb3afe':        {'source': '@aldermanervin, Twitter', 'image': 'manual-headshots/ervin-jason-c.jpg' },
    'hopkins-brian-4b6246ecbbbe':        {'source': '@aldermanhopkins, Twitter', 'image': 'manual-headshots/hopkins-brian.jpg' },
    'lopez-raymond-a-22593624a716':      {'source': '@rlopez15thward, Twitter', 'image': 'manual-headshots/lopez-raymond-a.jpg' },
    'moore-david-h-788e5a5727aa':        {'source': 'Chicago City Clerk', 'image': 'manual-headshots/moore-david-h.jpg' },
    'pawar-ameya-9488bd421a51':          {'source': 'chicago47.org', 'image': 'manual-headshots/pawar-ameya.jpg' },
    'quinn-marty-c8eb35e12e92':          {'source': 'Chicago City Clerk', 'image': 'manual-headshots/quinn-marty.jpg' },
    'santiago-milagros-s-f4b095aa4479':  {'source': 'Chicago City Clerk', 'image': 'manual-headshots/santiago-milagros-s.jpg' },
    'scott-jr-michael-7f664e1708fe':     {'source': 'citizensformichaelscottjr.com/', 'image': 'manual-headshots/scott-jr-michael.jpg' },
    'smith-michele-1994841ecda3':        {'source': '@aldermansmith43, Twitter', 'image': 'manual-headshots/smith-michele.jpg' },
    'sposato-nicholas-7ac2aa1b1965':     {'source': 'aldermansposato.com', 'image': 'manual-headshots/sposato-nicholas.png' },
    'emanuel-rahm-3af71de0e6ca':         {'source': 'cityofchicago.org', 'image': 'manual-headshots/emanuel-rahm.jpg' },
    'mendoza-susana-a-a465109bd96a':     {'source': 'chicityclerk.com', 'image': 'manual-headshots/mendoza-susana-a.jpg' },
    'valencia-anna-m-ae119fe8c2e3':      {'source': 'chicityclerk.com', 'image': 'manual-headshots/valencia-anna.jpg'},
}

CONTACT_INFO = {
    'arena-john-d9a11334830d':              {'twitter': { 'handle': '@45thWardChicago', 'url': 'https://twitter.com/45thWardChicago?lang=en' }, 'phone': '(773) 286-4545', 'address': '4754 North Milwaukee Avenue', },

    'beale-anthony-d125d27369f3':           {'twitter': { 'handle': '@Alderman_Beale', 'url': 'https://twitter.com/alderman_beale?lang=en' }, 'phone': '(773) 785-1100', 'address': '34 East 112th Place', },

    'cappleman-james-7b6638b78d83':         {'twitter': { 'handle': '@JamesCappleman', 'url': 'https://twitter.com/JamesCappleman' }, 'phone': '(773) 878-4646', 'address': '4544 North Broadway' },

    'cochran-willie-b6cc52d2933a':          {'twitter': { 'handle': '@ALDERMANWBC', 'url': 'https://twitter.com/aldermanwbc' }, 'phone': '(773) 955-5610', 'address': '6357 South Cottage Grove Avenue' },

    'harris-michelle-a-c9d7f4375894':       {'twitter': { 'handle': '@AldermanHarris', 'url': 'https://twitter.com/aldermanharris' }, 'phone': '(773) 874-3300', 'address': '8539 South Cottage Grove Avenue' },

    'mell-deborah-5fa778d13b51':            {'twitter': { 'handle': '@debmell', 'url': 'https://twitter.com/debmell' }, 'phone': '(773) 478-8040', 'address': '3001 West Irving Park Road' },

    'mitchell-gregory-i-1d481a8e2acd':      {'twitter': { 'handle': '@AldGregMitchell', 'url': 'https://twitter.com/AldGregMitchell' }, 'phone': '(773) 731-7777', 'address': '2249 East 95th Street' },

    'moore-joseph-77b5cf102a3f':            {'twitter': { 'handle': '@JoeMoore49', 'url': 'https://twitter.com/joemoore49' }, 'phone': '(773) 338-5796', 'address': '7356 North Greenview Avenue' },

    'munoz-ricardo-79203ae83471':        {'twitter': { 'handle': '@AldermanMunoz22', 'url': 'https://twitter.com/aldermanmunoz22' }, 'phone': '(773) 762-1771', 'address': '2500 South St. Louis Avenue' },

    'napolitano-anthony-v-7ab5df04527e': {'twitter': { 'handle': '@aldnapolitano41', 'url': 'https://twitter.com/aldnapolitano41' }, 'phone': '(773) 631-2241', 'address': '7442 North Harlem Avenue' },

    'oshea-matthew-j-5071e1c58184':      {'twitter': { 'handle': '@mattoshea19', 'url': 'https://twitter.com/mattoshea19' }, 'phone': '(773) 238-8766', 'address': '10400 South Western Avenue' },

    'osterman-harry-550e6f30c87c':       {'twitter': { 'handle': '@48Ward', 'url': 'https://twitter.com/48Ward' }, 'phone': '(773) 784-5277', 'address': '5533 North Broadway' },

    'ramirez-rosa-carlos-b67e026bf1e5':  {'twitter': { 'handle': '@CDRosa', 'url': 'https://twitter.com/cdrosa' }, 'phone': '(773) 887-3772', 'address': '2710 North Sawyer Avenue' },

    'reboyras-ariel-0ebeb178852e':       {'twitter': { 'handle': '@Ald_Reboyras', 'url': 'https://twitter.com/ald_reboyras' }, 'phone': '(773) 794-3095', 'address': '3559 North Milwaukee Avenue' },

    'sadlowski-garza-susan-ef8b7a07f272':{'twitter': { 'handle': '@SSadlowskiGarza', 'url': 'https://twitter.com/ssadlowskigarza' }, 'phone': '(773) 768-8138', 'address': '10500 South Ewing Avenue, 1st Floor' },

    'sawyer-roderick-t-a6e5d5f2bba5':    {'twitter': { 'handle': '@RoderickTSawyer', 'url': 'https://twitter.com/rodericktsawyer' }, 'phone': '(773) 635-0006', 'address': '700 East 79th Street' },

    'silverstein-debra-l-173bbaa057f6':  {'twitter': { 'handle': '@Debra4Alderman', 'url': 'https://twitter.com/debra4alderman' }, 'phone': '(773) 262-1050', 'address': '2949 West Devon Avenue, Suite A' },

    'solis-daniel-b0bd981415f9':         {'twitter': { 'handle': '@AldermanSolis', 'url': 'https://twitter.com/aldermansolis' }, 'phone': '(773) 523-4100', 'address': '1800 South Blue Island Avenue' },

    'taliaferro-chris-7646256e8079':     {'twitter': { 'handle': '@chris29thward', 'url': 'https://twitter.com/chris29thward' }, 'phone': '(773) 237-6460', 'address': '6272 West North Avenue' },

    'villegas-gilbert-8c9f813ce0a9':     {'twitter': { 'handle': '@gilbert36ward', 'url': 'https://twitter.com/gilbert36ward'}, 'phone': '   (773) 745-4636', 'address': '6934 West Diversey Avenue' },

    'thompson-patrick-d-aabd3b898af9':   {'twitter': { 'handle': '@AldPatDThompson', 'url': 'https://twitter.com/aldpatdthompson' }, 'phone': '(773) 254-6677', 'address': '3659 South Halsted Street' },

    'curtis-derrick-g-dc2702c16bce':     {'twitter': { 'handle': '@aldcurtis18', 'url': 'https://twitter.com/aldcurtis18' }, 'phone': '(773) 284-5057', 'address': '8359 South Pulaski Road' },

    'ervin-jason-c-a6bd57bb3afe':        {'twitter': { 'handle': '@AldermanErvin', 'url': 'https://twitter.com/aldermanervin' }, 'phone': '(773) 533-0900', 'address': '2602 West 16th Street' },

    'hopkins-brian-4b6246ecbbbe':        {'twitter': { 'handle': '@AldermanHopkins', 'url': 'https://twitter.com/aldermanhopkins' }, 'phone': '(312) 643-2299', 'address': '    1400 North Ashland Avenue' },

    'lopez-raymond-a-22593624a716':      {'twitter': { 'handle': '@RLopez15thWard', 'url': 'https://twitter.com/rlopez15thward' }, 'phone': '(773) 306-0837', 'address': '1650 West 63rd Street' },

    'moore-david-h-788e5a5727aa':        {'twitter': { 'handle': '@17thWardChicago', 'url': 'https://twitter.com/17thwardchicago' }, 'phone': '(773) 783-3672', 'address': '1344 West 79th Street' },

    'pawar-ameya-9488bd421a51':          {'twitter': { 'handle': '@Ameya_Pawar_IL', 'url': 'https://twitter.com/Ameya_Pawar_IL' }, 'phone': '(773) 868-4747', 'address': '4243 North Lincoln Avenue' },

    'quinn-marty-c8eb35e12e92':          {'twitter': { 'handle': '', 'url': '' }, 'phone': '(773) 581-8000', 'address': '6500 South Pulaski Road' },

    'santiago-milagros-s-f4b095aa4479':  {'twitter': { 'handle': '@Aldmilly31', 'url': 'https://twitter.com/aldmilly31' }, 'phone': '(773) 278-0031', 'address': '2521 North Pulaski Road' },

    'scott-jr-michael-7f664e1708fe':     {'twitter': { 'handle': '@aldermanscott24', 'url': 'https://twitter.com/aldermanscott24' }, 'phone': '(773) 533-2400', 'address': '1158 South Keeler Street' },

    'smith-michele-1994841ecda3':        {'twitter': { 'handle': '@AldermanSmith43', 'url': 'https://twitter.com/aldermansmith43' }, 'phone': '(773) 348-9500', 'address': '    2523 North Halsted Street' },

    'sposato-nicholas-7ac2aa1b1965':     {'twitter': { 'handle': '', 'url': '' }, 'phone': '(773) 283-3838', 'address': '3821 North Harlem Avenue' },

    'emanuel-rahm-3af71de0e6ca':         {'twitter': { 'handle': '@RahmEmanuel', 'url': 'https://twitter.com/rahmemanuel' }, 'phone': '(312) 744-3300', 'address': '121 N. LA SALLE STREET' },

    'moreno-proco-joe-b1e0d8e0205d':     {'twitter': { 'handle': '@Alderman_Moreno', 'url': 'https://twitter.com/Alderman_Moreno' }, 'phone': '(773) 278-0101', 'address': '2740 West North Avenue' },

    'dowell-pat-77f09c5b056c':         {'twitter': { 'handle': '@AldPatDowell3rd', 'url': 'https://twitter.com/AldPatDowell3rd' }, 'phone': '(773) 373-9273', 'address': '5046 South State Street' },

    'hairston-leslie-a-fc1eb983a334':   {'twitter': { 'handle': '@5thWardChicago', 'url': 'https://twitter.com/5thwardchicago' }, 'phone': '(773) 324-5555', 'address': '2325 East 71st Street' },

    'cardenas-george-a-e7f3145cb0bf': {'twitter': { 'handle': '@aldcardenas', 'url': 'https://twitter.com/aldcardenas' }, 'phone': '(773) 523-8250', 'address': '3476 South Archer Avenue' },

    'burke-edward-m-10a51f9a148e': {'twitter': { 'handle': '', 'url': '' }, 'phone': '(773) 471-1414', 'address': '2650 West 51st Street' },

    'foulkes-toni-85ebd7895373': {'twitter': { 'handle': '@ToniFoulkes', 'url': 'https://twitter.com/tonifoulkes' }, 'phone': '(773) 863-0220', 'address': '1504 West 63rd Street' },

    'brookins-jr-howard-a2dedc827d3c': {'twitter': { 'handle': '', 'url': '' }, 'phone': '(773) 881-9300', 'address': '9011 South Ashland Avenue, Unit B' },

    'zalewski-michael-r-a9877e230b7c': {'twitter': { 'handle': '@ward23chicago', 'url': 'https://twitter.com/ward23chicago' }, 'phone': '(773) 582-4444', 'address': '6247 South Archer Avenue' },

    'maldonado-roberto-068e9f23cacf': {'twitter': { 'handle': '@MaldonadoR26', 'url': 'https://twitter.com/MaldonadoR26' }, 'phone': '(773) 395-0143', 'address': '2511 West Division Street' },

    'burnett-jr-walter-7d4c78ba47aa': {'twitter': { 'handle': '@AldermanBurnett', 'url': 'https://twitter.com/aldermanburnett' }, 'phone': '(312) 432-1995', 'address': '4 North Western Avenue' },

    'waguespack-scott-944c102c324e': {'twitter': { 'handle': '@ward32chicago', 'url': 'https://twitter.com/ward32chicago' }, 'phone': '(773) 248-1330', 'address': '2657 North Clybourn Avenue' },

    'austin-carrie-m-d64a7bfe03dd': {'twitter': { 'handle': '@TweetinIn34', 'url': 'https://twitter.com/tweetinin34' }, 'phone': '(773) 928-6961', 'address': '507 West 111th Street' },

    'tunney-thomas-93e563588d8a': {'twitter': { 'handle': '@AldTomTunney', 'url': 'https://twitter.com/aldtomtunney' }, 'phone': '(773) 525-6034', 'address': '3223 North Sheffield Avenue' },

    'reilly-brendan-248a45aa2e32': {'twitter': { 'handle': '@AldReilly', 'url': 'https://twitter.com/AldReilly' }, 'phone': '(312) 642-4242', 'address': '325 West Huron Street, Suite 510' },

    'mitts-emma-238d61a37942': {'twitter': { 'handle': '@bettyepearl3749', 'url': 'https://twitter.com/bettyepearl3749' }, 'phone': '(773) 379-0960', 'address': '4924 West Chicago Avenue' },

    'laurino-margaret-b238c7d2f668': {'twitter': { 'handle': '@LaurinoWard39', 'url': 'https://twitter.com/laurinoward39' }, 'phone': '(773) 736-5594', 'address': '4404 West Lawrence Avenue' },

    'valencia-anna-m-ae119fe8c2e3': {'twitter': { 'handle': '@AnnaValenciaIL', 'url': 'https://twitter.com/annavalenciail' }, 'phone': '(312) 742-5375', 'address': '121 North LaSalle St, Room 107' },
}


# notable positions that aren't district representatives, e.g. mayor & city clerk
# keys should match person slugs
EXTRA_TITLES = {
    'mendoza-susana-a-a465109bd96a': 'City Clerk',
    'emanuel-rahm-3af71de0e6ca': 'Mayor',
    'valencia-anna-m-ae119fe8c2e3': 'City Clerk',
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

USING_NOTIFICATIONS = True
