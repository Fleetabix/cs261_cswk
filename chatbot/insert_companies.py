from chatbot.models import Industry, Company, CompanyAlias, IndustryAlias

def create_industry(name, aliases=[]):
    """
        Method to create an industry along with its aliases.
    """
    i = Industry.objects.create(name=name)
    for alias in aliases:
        IndustryAlias.objects.create(industry=i, alias=alias)
    return i


def create_company(ticker, name, industries, aliases=[]):
    """
        Method to create a company and save it in the database
        along with it's industries and aliases.
    """
    c = Company.objects.create(ticker=ticker, name=name)
    # add all the industries
    for industry in industries:
        c.industries.add(industry)
    # add all the aliases
    for alias in aliases:
        Alias.objects.create(company=c, alias=alias)


# List of industries
# For each industry you can optionaly add 
# aliases so that florin can check for it's other names when the user ask
# example: leis = create_industry('leisure', ['alias1', 'alias2'])
aero = create_industry(name = 'aerospace & defense')
auto = create_industry(name = 'automobiles & parts')
bank = create_industry(name = 'banks')
beve = create_industry(name = 'beverages', aliases=['drinks'])
chem = create_industry(name = 'chemicals')
cons = create_industry(name = 'construction & materials')
elec = create_industry(name = 'electricity')
eleq = create_industry(name = 'electronic & electrical equipment')
equi = create_industry(name = 'equity investment instruments')
fina = create_industry(name = 'financial services')
tele = create_industry(name = 'fixed line telecommunications')
fdre = create_industry(name = 'food & drug retailers')
fpro = create_industry(name = 'food producers')
fore = create_industry(name = 'forestry & paper')
util = create_industry(name = 'gas, water & multiutilities', aliases=['gas', 'water', 'utilities'])
geni = create_industry(name = 'general industrials')
genr = create_industry(name = 'general retailers')
heal = create_industry(name = 'healthcare equipment & services')
home = create_industry(name = 'household goods & home construction')
inme = create_industry(name = 'industrial metals')
life = create_industry(name = 'life insurance')
medi = create_industry(name = 'media')
mine = create_industry(name = 'mining')
mobi = create_industry(name = 'mobile telecommunications')
insu = create_industry(name = 'nonlife insurance')
ogpr = create_industry(name = 'oil & gas producers')
pers = create_industry(name = 'personal goods')
phar = create_industry(name = 'pharmaceuticals & biotechnology')
reit = create_industry(name = 'real estate investment trusts')
soft = create_industry(name = 'software & computer services')
supp = create_industry(name = 'support services')
tech = create_industry(name = 'technology hardware & equipment')
toba = create_industry(name = 'tobacco')
trav = create_industry(name = 'travel & leisure')



# List of FTSE100 companies.
# Make sure the industries (even if it's just one) is in
# a list - this applies to aliases to.
create_company('AAL', 'Anglo American', [mine])
create_company('ABF', 'Associated British Foods', [fpro])
create_company('ADM', 'Admiral Group', [insu])
create_company('AHT', 'Ashtead Group', [supp])
create_company('ANTO', 'Antofagasta', [mine])
create_company('AV.', 'Aviva', [life])
create_company('AZN', 'AstraZeneca', [phar])
create_company('BA.', 'BAE Systems', [aero])
create_company('BARC', 'Barclays', [bank])
create_company('BATS', 'British American Tobacco', [toba])
create_company('BDEV', 'Barratt Developments', [home])
create_company('BKG', 'Berkeley Group Holdings', [home])
create_company('BLND', 'British Land Co', [reit])
create_company('BLT', 'BHP Billiton', [mine])
create_company('BNZL', 'Bunzl', [supp])
create_company('BP.', 'BP', [ogpr])
create_company('BRBY', 'Burberry Group', [pers])
create_company('BT.A', 'BT Group', [tele])
create_company('CCH', 'Coca-Cola HBC', [beve])
create_company('CCL', 'Carnival', [trav])
create_company('CNA', 'Centrica', [util])
create_company('CPG', 'Compass Group', [trav])
create_company('CRDA', 'Croda International', [chem])
create_company('CRH', 'CRH', [cons])
create_company('DCC', 'DCC', [supp])
create_company('DGE', 'Diageo', [beve])
create_company('DLG', 'Direct Line Insurance Group', [insu])
create_company('EVR', 'Evraz', [inme])
create_company('EXPN', 'Experian', [supp])
create_company('EZJ', 'easyJet', [trav])
create_company('FERG', 'Ferguson', [supp])
create_company('FRES', 'Fresnillo', [mine])
create_company('GFS', 'G4S', [supp])
create_company('GKN', 'GKN', [auto])
create_company('GLEN', 'Glencore', [mine])
create_company('GSK', 'GlaxoSmithKline', [phar])
create_company('HL.', 'Hargreaves Lansdown', [fina])
create_company('HLMA', 'Halma', [eleq])
create_company('HMSO', 'Hammerson', [reit])
create_company('HSBA', 'HSBC Holdings', [bank])
create_company('IAG', 'International Consolidated Airlines Group', [trav])
create_company('IHG', 'InterContinental Hotels Group', [trav])
create_company('III', '3i Group', [fina])
create_company('IMB', 'Imperial Brands', [toba])
create_company('INF', 'Informa', [medi])
create_company('ITRK', 'Intertek Group', [supp])
create_company('ITV', 'ITV', [medi])
create_company('JE.', 'Just Eat', [genr])
create_company('JMAT', 'Johnson Matthey', [chem])
create_company('KGF', 'Kingfisher', [genr])
create_company('LAND', 'Land Securities Group', [reit])
create_company('LGEN', 'Legal & General Group', [life])
create_company('LLOY', 'Lloyds Banking Group', [bank])
create_company('LSE', 'London Stock Exchange Group', [fina])
create_company('MCRO', 'Micro Focus International', [soft])
create_company('MDC', 'Mediclinic International', [heal])
create_company('MKS', 'Marks & Spencer Group', [genr])
create_company('MNDI', 'Mondi', [fore])
create_company('MRW', 'Morrison Supermarkets', [fdre])
create_company('NG.', 'National Grid', [util])
create_company('NMC', 'NMC Health', [heal])
create_company('NXT', 'Next', [genr])
create_company('OML', 'Old Mutual Group', [life])
create_company('PPB', 'Paddy Power Betfair', [trav])
create_company('PRU', 'Prudential', [life])
create_company('PSN', 'Persimmon', [home])
create_company('PSON', 'Pearson', [medi])
create_company('RB.', 'Reckitt Benckiser Group', [home])
create_company('RBS', 'Royal Bank of Scotland Group', [bank])
create_company('RDSA', 'Royal Dutch Shell', [ogpr])
create_company('RDSB', 'Royal Dutch Shell', [ogpr])
create_company('REL', 'RELX', [medi])
create_company('RIO', 'Rio Tinto', [mine])
create_company('RR.', 'Rolls-Royce Group', [aero])
create_company('RRS', 'Randgold Resources', [mine])
create_company('RSA', 'RSA Insurance Group', [insu])
create_company('RTO', 'Rentokil Initial', [supp])
create_company('SBRY', "Sainsbury's", [fdre])
create_company('SDR', 'Schroders', [fina])
create_company('SGE', 'Sage Group', [soft])
create_company('SGRO', 'Segro', [reit])
create_company('SHP', 'Shire', [phar])
create_company('SKG', 'Smurfit Kappa Group', [geni])
create_company('SKY', 'Sky', [medi])
create_company('SLA', 'Standard Life Aberdeen', [fina])
create_company('SMDS', 'Smith, D.S.', [geni])
create_company('SMIN', 'Smiths Group', [geni])
create_company('SMT', 'Scottish Mortgage Investment Trust', [equi])
create_company('SN.', 'Smith & Nephew', [heal])
create_company('SSE', 'SSE', [elec])
create_company('STAN', 'Standard Chartered', [bank])
create_company('STJ', "St James's Place", [life])
create_company('SVT', 'Severn Trent', [util])
create_company('TSCO', 'Tesco', [fdre])
create_company('TUI', 'TUI AG', [trav])
create_company('TW.', 'Taylor Wimpey', [home])
create_company('ULVR', 'Unilever', [fpro])
create_company('UU.', 'United Utilities Group', [util])
create_company('VOD', 'Vodafone Group', [mobi])
create_company('WPP', 'WPP Group', [medi])
create_company('WTB', 'Whitbread', [trav])
