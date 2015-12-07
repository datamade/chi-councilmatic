def topic_classifier(title) :
    title = title.lower()

    # Ward Matters

    ## Residents

    tags = ['Ward Matters', 'Residents']

    if title.startswith('senior citizen sewer') :
        return tags + ['Senior citizen sewer refund']

    if title.startswith(('handicapped parking', 
                         'handicapped permit')) :
        return tags + ['Routine', 'Handicapped Parking Permit']

    if title.startswith(('condominium claim',
                         'denial of condo',
                         'denials of condo',
                         'denials condo',
                         'denied condo',
                         'condominium refuse')) :
        return tags + ['Routine', 'Condo Refuse Claim']


    if title.startswith(('residential permit',
                         'residential parking',
                         'amendment of residential', 
                         'buffer zone')) :
        return tags + ['Routine', 'Residential permit parking']

    ## Business Permits and Privileges

    tags = ["Ward Matters", "Business Permits and Privileges"]

    if title.startswith(('sidewalk cafe',)) :
        return tags + ['Routine', 'Sidewalk cafe']

    if title.startswith(('grant(s) of privilege',
                         'grant(s) of priviledge',
                         'grant of privilege',
                         'grants of privilege',
                         'grant of privlage',
                         'grant of priviege',
                         'amendment of grant(s) of privilege')) :
        return tags + ['Routine', 'Grant of privilege in public way']

    if title.startswith('awning(s)') :
        return tags + ['Routine', 'Awnings']

    if (any(s in title for s in ('issuance of permits for sign(s)/signboard(s)',
                      'install signs')) or title.startswith('sign(s)')) :
        return tags + ['Routine', 'Sign permits']

    if title.startswith('canopy(s)') :
        return tags + ['Routine', 'Canopy']


    if title.startswith(('exemption from', 'exemption for physical')) :
        return tags + ['Routine', 'Physical barrier exemption']

    if title.startswith(('conduct of sidewalk sale', 
                         'sidewalk sale')) : 
        return tags + ['Non-Routine', 'Sidewalk Sale']


    if title.startswith(('industrial permit parking',)) :
        return tags + ['Non-Routine', 'Industrial Permit Parking']




    ## Land Use

    tags = ["Ward Matters", "Land Use"]

    if '4-244-140' in title :
        return tags + ['Non-Routine', 'Restrict Peddling']

    if title.startswith('zoning reclassification') :
        return tags + ['Routine', 'Zoning Reclassification']

    if any(s in title for s in ('4-60-022', '4-60-023')):
        return tags + ['Non-Routine', 'Liquor and Package Store Restrictions']

    if any(s in title for s in ('pedestrian street', 'pedestrian retail street')):
        return tags + ['Non-Routine', 'Pedestrian Street']

    if title.startswith(('historical landmark designation',
                         'correction to chicago landmark designation')) :
        return tags + ['Non-Routine', 'Historical Landmark']


    if 'subdivision' in title or 'resubdivision' in title:
        return tags + ['Non-Routine', 'Subdivison']



    ## Economic Development

    tags = ["Ward Matters", "Economic Development"]

    if title.startswith(('support of class 6(b)',
                         'support of class l',
                         'class c',
                         'class l',
                         'designation of class 7',
                         'support of class c',
                         'expression of consent for class 7')) :
        return tags + ['Non-Routine', 'Tax Incentives']

    if 'tax increment' in title :
        return tags + ['Non-Routine', 'Tax Increment Financing']

    if 'redevelopment project area' in title :
        return tags + ['Non-Routine', 'Tax Increment Financing']

    if 'redevelopment plan' in title :
        return tags + ['Non-Routine', 'Tax Increment Financing']

    if ('transfer of tif funds' in title 
        or ('allocation of' in title and 'tif funds' in title)):
        return tags + ['Non-Routine', 'Tax Increment Financing']

    if (title.startswith("tif ") 
        or title.endswith( "tif") 
        or " tif " in title) :
        return tags + ['Non-Routine', "Tax Increment Financing"]


    if 'tifworks' in title :
        return tags + ['Non-Routine', 'Tax Increment Financing']

    if ('neighborhood improvement program' in title.lower() 
        or 'neighborhood investment program' in title.lower()
        or 'tif-nip' in title.lower() ) :
        return tags + ['Non-Routine', 'Tax Increment Financing']


    if title.startswith('amendment') and 'tif' in title and 'budget' in title  :
        return tags + ['Non-Routine', 'Tax Increment Financing']

    if any(s in title for s in ('s.s.a.', 
                              ' ssa', 
                              'special service no', 
                              'special service area')):
        return tags + ['Non-Routine', 'Special Service Area']




#                         'Issue Special Event',
#                         'waiver of permit fees',

    ## Special Events

    if title.startswith(('permission to hold', 
                         'permission to hold',
                         'issue special event',
                         'issuance of special event license')) :
        return tags + ['Non-Routine', 'Special Events']



    ## Free Permits

    tags = ["Ward Matters"]

    if title.startswith(('waiver of annual public assembly fee',
                         'wavier of special event tent',
                         'waiver of special event',
                         'waiver of annual fire pump',
                         'waiver street closure',
                         'waiver of street closure permit fee' )) :
        return tags + ['Non-Routine', 'Fee Waiver']

    if title.lower().startswith(('cancellation of warrants',)) :
        return tags + ['Non-Routine', 'Fee Waiver']

    if title.lower().startswith(('issuance of permit',
                                 'issuance of tent permit',
                                 'issuance of license')) :
        return tags + ['Non-Routine', 'Fee Waiver']

    if title.startswith(('waiver of special event raffle license',)) :
        return tags + ['Non-Routine', 'Fee Waiver']


    if title.startswith(('free permit', 
                         'fee exemption',
                         'waiver of public way use permit fee',
                         'waiver of community identifier sign permit fee',
                         'waiver of fee',
                         'exemption of public way use',
                         'cancellation of public way use permit fee', 
                         'waiver of permit fee',
                         'waiver of public use permit fee',
                         'license fee exemption')) :
        return tags + ['Non-Routine', 'Fee Waiver']

    if title.startswith(('historical landmark fee',
                         'landmark fee waiver')) :
        return tags + ['Non-Routine', 'Fee Waiver']



    ## Churches and Non Profits

    tags = ["Ward Matters", "Churches and Non-Profits"]

    if title.startswith(('not-for-profit fee exemption',
                         'sewer refund',
                         'refund of fee',
                         'cancellation of water',
                         'canecellation of warrants for water')) :
        return tags + ['Non-Routine', 'Free Water and Sewer for Non Profit Organizations']


    if title.startswith(('tag day',)) :
        return tags + ['Non-Routine', 'Tag Day Permits']

    ## Parking
    tags = ["Ward Matters", "Parking"]

    if title.startswith(('parking prohibit',
                         'amendment of parking',
                         'parking limit',
                         'parking restrict'
                         )) :
        return tags + ['Routine', 'Parking Restriction']

    if title.startswith(('parking meters', 
                         'amendment of parking meters',
                         'installation and removal of parking meters',
                         'removal and relocation of parking meters')) :
        return tags + ['Non-Routine', 'Parking Meters']

    if title.startswith(('loading/standing/tow',
                         'amendment of loading',
                         'repeal loading',
                         'tow zone',
                         'traffic lane',
                         'loading zone')) :
        return tags + ['Routine', 'Loading/Standing/Tow Zone']


    if title.startswith(('removal of taxicab stand',
                         'repeal of taxicab stand',
                         'taxicab stand',
                         'amendment of taxicab',
                         'establish taxicab',
                         'establishment of taxicab')) :
        return tags + ['Non-Routine', 'Taxicab Stand']


    if 'pilot parking program' in title :
        return tags + ['Non-Routine', 'Pilot Parking Program']

    



    ## Traffic

    tags = ["Ward Matters", "Traffic"]

    if title.startswith(('traffic direction',
                         'single direction',
                         'one way traffic',
                         'one-way traffic',
                         'repeal one-way')) :
        return tags + ['Non-Routine', 'Traffic Direction']

    if title.startswith(('speed hump',)) :
        return tags + ['Non-Routine', 'Speed Hump']

    if title.startswith(('no cruising',)) :
        return tags + ['Non-Routine', 'No Cruising Zone']

    if title.startswith(('traffic sign', 
                         'traffic warning sign',
                         'miscellaneous signs')) :
        return tags + ['Routine', 'Traffic signs and signals']

    if title.startswith(('limited local access')) :
        return tags + ['Non-Routine', 'Limited Local Access']

    if title.startswith(('speed limitation',)) : 
        return tags + ['Non-Routine', 'Speed Limits']

    if title.startswith(('closed to', 
                         'close to', 
                         'closure to vehic', 
                         'traffic closure')) :
        return tags + ['Non-Routine', 'Traffic Closure']

    if title.startswith(('vehicle weigh',
                         'weight limitation',
                         'weigh limitation')) :
        return tags + ['Non-Routine', 'Vehicle Weight Limitation']

    if title.startswith('construction of traffic circle') :
        return tags + ['Non-Routine', 'Traffic Circle']

    if title.startswith(('traffic regulations',
                         'failed to pass traffic regulation',
                         'various traffic regulations')) :
        return tags + ['Non-Routine', 'Traffic Regulation']

    if title.startswith(('service drive',)) :
        return tags + ['Non-Routine', 'Service Drive/Diagonal Parking']


    ## Wrigley Field

    tags = ["Ward Matters"]

    if title.startswith(('one time exception to wrigley field',
                         'amendment of wrigley field',
                         'amendment of night game',
                         'one time exception to night game',
                         'amendment of wrigley adjacent area')) :
        return tags + ['Non-Routine', 'Wrigley Field']


    # Small Claims

    tags = ["Small Claims"]

    if any(s in title for s in ('damage to vehicle', 'damage to vhicle')):
        return tags + ['Routine', 'Damage to vehicle claim']

    if 'damage to property claim' in title :
        return tags +['Routine', 'Damage to property claim']

    if title.startswith(('payment of',
                         'payments of',
                         'payment for various',
                         'denying payment',
                         'denied various claims',
                         'various small claims',
                         'small claims',
                         'adelman',
                         'denials of various',
                         'denial of various')) :
        return tags + ['Non-Routine', 'Settlement of Claims']

    if 'excessive water rate claim' in title :
        return tags + ['Routine', 'Excessive water rate claim']

    # Honorifics

    tags = ["Honorifics"]

    if title.startswith(('congratulation', 
                         'congradulation',
                         'congraulations',
                         'proclamation',
                         'recognition', 
                         'recoginition',
                         'commemoration of', 
                         'tribute to', 
                         'declaraton',
                         'posthumous gratitude',
                         'posthumous congratulations',
                         'commendations extended to',
                         'gratitude',
                         'grattitude',
                         'best wishes extended',
                         'condolences extended',
                         'expression of condolence',
                         'expression sympathy',
                         'honoring',
                         'welcome extended')) or 'declaration' in title  :
        return tags + ['Routine', 'Honorific Resolution']

    if 'commemorative' in title :
        return tags + ['Routine', 'Honorific Marker']

    if title.startswith(('honorary street designation',
                         'designation of "ed and betty gardner street"',
                         'dedication of',
                         'commermoration of dedication')) :
        return tags + ['Routine', 'Honorary street']

    # City

    tags = ["City Matters"]

    ## Settlement Agreements

    if title.startswith(('settlement agreement', 
                         'sylwia marcincryk v.',
                         'setttlement order',
                         'settlement order',
                         'judgement and settlement',
                         'judgements or settlement',
                         'judgment and settlement',
                         'judgement or settlment',
                         'judgement or settlement')) : 
        return tags + ['Non-Routine', 'Settlement Agreement']

    ## Appointments


    if 'standing committee' in title :
        return ['Council Matters', 'Non-Routine', 'Committe Appointments']


    if title.startswith(('appointment', 'reappointment')) :
        return tags + ['Non-Routine', 'Appointment']

    ## Airports

    if any(s in title for s in ("o'hare", 
                              "midway international", 
                              "terminal use", 
                              "off airport",
                              "cargo facility", 
                              "aviation services")):
        return tags + ["Non-Routine", "Airports"]

    ## Special Funds

    tags = ["City Matters", "Special Funds"]

    if 'human infrastructure fund' in title :
        return tags + ["Non-Routine", "Human Infrastructure Fund"]

    ## Open Space Impact Funds

    if title.startswith(('expenditure of open space',)) :
        return tags + ['Non-Routine', 'Open Space Impact Funds']


    ## Small Business Improvement Fund

    if 'small business improvement fund' in title :
        return tags + ['Non-Routine', 'Small Business Improvement Fund']


    # Motor Fuel Tax Fund

    if 'motor fuel tax funds' in title.lower() :
        return tags + ['Non-Routine', 'Motor Fuel Tax Funds']

    # Inspector General

    if title.startswith(('inspector general')) :
        return tags + ['Non-Routine', "Inspector General"]

    tags = ["City Matters"]

    ## Municipal Code


    if title.startswith(('amendment of section',
                         'amendment of subsection',
                         'amendment of title',
                         'amendment of various provisions of municipal',
                         'amendment of various sections of municipal code',
                         'amendment to various sections of municipal code',
                         'repeal of section',
                         'amendment of municipal code',
                         'amendment to municipal code',
                         'amendment of chapter')) :
        return tags + ['Non-Routine', 'Municipal Code']

    if title.startswith(('pay rate of hospital', 
                         'payment of hospital and med')) :
        return tags + ['Routine', 'Police and Firefighter Medical Bills']

    if title.startswith(('independent police review',
                         'police review authority',
                         'police board')) :
        return tags + ['Non-Routine', 'Police Oversight']


    # Neighborhood Stabilization Program

    if 'neighborhood stabilization program' in title.lower() :
        return tags + ['Non-Routine', 'Neighborhood Stabilization Program']


    ## Oaths of Office

    if title.startswith(('oath',)) :
        return tags + ['Non-Routine', 'Oath of Office']

    ## Annual Appropriations

    if 'annual appropriation' in title :
        return tags + ['Non-Routine', 'Annual Appropriation']

    # Pensions

    if title.startswith(("laborers' and retirement board",
                         'retirement board')) : 
        return tags + ['Non-Routine', 'Pensions']

    ## Affordable Housing

    if title.startswith(('affordable housing plan')) :
        return tags + ['Non-Routine', 'Affordable Housing']

    ## Labor Agreement

    if title.startswith(('collective bargaining')) or 'labor agreement' in title:
        return tags + ['Non-Routine', 'Labor Agreement']

    ## CDBG 

    if 'cdbg' in title or 'community development block grant ordinance' in title:
        return tags + ['Non-Routine', 'Community Development Block Grant']


    # Elections

    if any(s in title for s in ('referenda', 
                              'election return', 
                              'submission of public question',
                              "aldermanic election")):
        return tags + ['Non-Routine', 'Elections']


    ## Finances

    tags = ["City Matters", "Finances"]

    if any(s in title for s in ('tax levy', 
                              'tax levied', 
                              'levy of real estate tax', 
                              'tax levies')):
        return tags + ['Non-Routine', 'Taxes']

    if any(s in title for s in (' bonds', 
                              ' bond issuance ', 
                              ' bond proceeds ',
                              'general obligation note',
                              'general obligation tender notes',
                              'multi-family housing revenue note')):
        return tags + ['Non-Routine', 'Bonds']

    if 'commercial paper' in title :
        return tags

    if title.startswith(('city comptroller',
                         'city of chicago annual financial analysis',
                         'comprehensive annual financial report')) :
        return tags + ['Non-Routine', 'Financial Reports']





    ## City Business

    tags = ["City Matters", "City Business"] 

    if title.startswith(('vacation', 
                         'amendment of vacation')) :
        return tags + ['Non-Routine', 'Vacation of Public Street']

    if title.startswith(('sale of city-owned propert',
                         'amendment of acquisition of propert',
                         'conveyance of city', 
                         'approval of land sale',
                         'acceptance of bid for property',
                         'land transfer',
                         'transfer of merchant park property',
                         'amendment to terms of previously authorized land transactions',
                         'transfer of parcels',
                         'transfer of property',
                         'acceptance of propert',
                         'conveyance of propert',
                         'amendment of land sale',
                         'conveyance of open space land',
                         'negotiated sale of city-owned property',
                         'acquisition')) :
        return tags + ['Non-Routine', 
                       'Getting and Giving Land']


    if title.startswith(('lease agreement', 
                         'lease ageement',
                         'sub-lease agreement',
                         'amendment of lease',
                         'amendment to lease')) :
        return tags + ['Non-Routine', 'Lease Agreement']

    if title.startswith(('donation', 'donate')) :
        return tags + ['Non-Routine', 'Donation of City Property']

    if 'easement' in title :
        return tags + ['Non-Routine', 'Easements']

    if title.startswith(('intergovernmental agreement', 
                         'renewal of intergovernment',
                         'intergovernment agreement',
                         'amendment of intergovernmental agreement')) :
        return tags + ['Non-Routine', 'Intergovernmental Agreement']

    if title.startswith(('loan agreement', 
                         'multi-family loan agreement',
                         'loan assumption',
                         'amendment of terms',
                         'loan modification',
                         'amendment of loan agreement',
                         'loan restructure')) :
        return tags + ['Non-Routine', 'Loan Agreement']

    # Council Matters

    tags = ["Council Matters"]

    if title.startswith(('fixed for next city council meeting',
                         'time fixed',
                         'time fixed for next city council meeting',
                         'amending city council meeting time')) :
        return tags + ['Routine', 'Next Meeting']


    if title.startswith(('correction of city council journal',
                         'correction of journal')) :
        return tags + ['Non-Routine', 'Correction of City Council Journal']


    if title.startswith(('call for hearing',)) :
        return tags + ['Non-Routine', 'Call for Hearing']

    if title.startswith(('transfer of funds to committee',
                         'transfer of funds within committee',
                         'transfer of funds within the city council committee',
                         'transfer of funds within city council committee',
                         'transfer of funds within the committee',
                         'transfer of year 2013 funds within committee',
                         'transfer of funds to committee')) :
        return tags + ['Non-Routine', 'Transfer of Committee Funds']

    if 'city council committee' in title and 'budget' in title : 
        return tags + ['Non-Routine', 'Committee Budgets']

    if 'fail to pass all legislation' in title :
        return tags + ['Non-Routine', 'Fail to Pass All Legislation']

    if title.startswith(('call for',
                         'call upon',
                         'call to',
                         'expression of support',
                         'support of',
                         'expression of opposition',
                         'denouncement',
                         'condemnation of')) :
        return tags + ['Non-Routine', 'Call for Action']

    if (title.startswith(('city council rule',
                         'amendment of rule')) or
        'rules of order and procedure' in title):
        return tags + ['Non-Routine', 'City Council Rules']

    if any(s in title for s in ('elected vice-mayor', 'president pro tempore')):
        return tags + ['Non-Routine', 'City Council Positions']


    

    tags = []







    if title.startswith(('redevelopment agreement',
                         'amendment to previous redevelopment agreement',
                         'amendment of redevelopment agreement',
                         'first amendment to redevelopment agreement',
                         )) or 'associated redevelopment agreement' in title :
        return tags + ['Non-Routine', 'Redevelopment Agreement']






    if title.startswith(('system test', 'test')) :
        return tags + ['Routine', 'Test']
    

    if title == '':
        return tags + ['No Info']





    return ['Non-Routine', 'Unclassified']
