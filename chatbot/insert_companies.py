from chatbot.models import Industry, Company

def create_company(ticker, name, industry):
    """
        Method to create a company and save it in the database
    """
    c = Company(ticker=ticker, name=name, industry=industry)
    c.save()

#List of industries
aero = Industry(name = 'aerospace & defense')
auto = Industry(name = 'automobiles & parts')
bank = Industry(name = 'banks')
beve = Industry(name = 'beverages')
chem = Industry(name = 'chemicals')
cons = Industry(name = 'construction & materials')
elec = Industry(name = 'electricity')
eleq = Industry(name = 'electronic & electrical equipment')
equi = Industry(name = 'equity investment instruments')
fina = Industry(name = 'financial services')
tele = Industry(name = 'fixed line telecommunications')
fdre = Industry(name = 'food & drug retailers')
fpro = Industry(name = 'food producers')
fore = Industry(name = 'forestry & paper')
util = Industry(name = 'gas; water & multiutilities')
geni = Industry(name = 'general industrials')
genr = Industry(name = 'general retailers')
heal = Industry(name = 'healthcare equipment & services')
home = Industry(name = 'household goods & home construction')
inen = Industry(name = 'industrial engineering')
inme = Industry(name = 'industrial metals')
intr = Industry(name = 'industrial transportation')
life = Industry(name = 'life insurance')
medi = Industry(name = 'media')
mine = Industry(name = 'mining')
mobi = Industry(name = 'mobile telecommunications')
insu = Industry(name = 'nonlife insurance')
ogpr = Industry(name = 'oil & gas producers')
oesd = Industry(name = 'oil equipment; services & distribution')
pers = Industry(name = 'personal goods')
phar = Industry(name = 'pharmaceuticals & biotechnology')
reis = Industry(name = 'real estate investment & services')
reit = Industry(name = 'real estate investment trusts')
soft = Industry(name = 'software & computer services')
supp = Industry(name = 'support services')
tech = Industry(name = 'technology hardware & equipment')
toba = Industry(name = 'tobacco')
trav = Industry(name = 'travel & leisure')

#List of FTSE100 companies
create_company('AAL', 'Anglo American', mine)
create_company('ABF', 'Associated British Foods', fpro)
create_company('ADM', 'Admiral Group', insu)
create_company('AHT', 'Ashtead Group', supp)
create_company('ANTO', 'Antofagasta', mine)
create_company('AV.', 'Aviva', life)
create_company('AZN', 'AstraZeneca', phar)
create_company('BA.', 'BAE Systems', aero)
create_company('BARC', 'Barclays', bank)
create_company('BATS', 'British American Tobacco', toba)
create_company('BDEV', 'Barratt Developments', home)
create_company('BKG', 'Berkeley Group Holdings', home)
create_company('BLND', 'British Land Co', reit)
create_company('BLT', 'BHP Billiton', mine)
create_company('BNZL', 'Bunzl', supp)
create_company('BP.', 'BP', ogpr)
create_company('BRBY', 'Burberry Group', pers)
create_company('BT.A', 'BT Group', tele)
create_company('CCH', 'Coca-Cola HBC', beve)
create_company('CCL', 'Carnival', trav)
create_company('CNA', 'Centrica', util)
create_company('CPG', 'Compass Group', trav)
create_company('CRDA', 'Croda International', chem)
create_company('CRH', 'CRH', cons)
create_company('DCC', 'DCC', supp)
create_company('DGE', 'Diageo', beve)
create_company('DLG', 'Direct Line Insurance Group', insu)
create_company('EVR', 'Evraz', inme)
create_company('EXPN', 'Experian', supp)
create_company('EZJ', 'easyJet', trav)
create_company('FERG', 'Ferguson', supp)
create_company('FRES', 'Fresnillo', mine)
create_company('GFS', 'G4S', supp)
create_company('GKN', 'GKN', auto)
create_company('GLEN', 'Glencore', mine)
create_company('GSK', 'GlaxoSmithKline', phar)
create_company('HL.', 'Hargreaves Lansdown', fina)
create_company('HLMA', 'Halma', eleq)
create_company('HMSO', 'Hammerson', reit)
create_company('HSBA', 'HSBC Holdings', bank)
create_company('IAG', 'International Consolidated Airlines Group', trav)
create_company('IHG', 'InterContinental Hotels Group', trav)
create_company('III', '3i Group', fina)
create_company('IMB', 'Imperial Brands', toba)
create_company('INF', 'Informa', medi)
create_company('ITRK', 'Intertek Group', supp)
create_company('ITV', 'ITV', medi)
create_company('JE.', 'Just Eat', genr)
create_company('JMAT', 'Johnson Matthey', chem)
create_company('KGF', 'Kingfisher', genr)
create_company('LAND', 'Land Securities Group', reit)
create_company('LGEN', 'Legal & General Group', life)
create_company('LLOY', 'Lloyds Banking Group', bank)
create_company('LSE', 'London Stock Exchange Group', fina)
create_company('MCRO', 'Micro Focus International', soft)
create_company('MDC', 'Mediclinic International', heal)
create_company('MKS', 'Marks & Spencer Group', genr)
create_company('MNDI', 'Mondi', fore)
create_company('MRW', 'Morrison Supermarkets', fdre)
create_company('NG.', 'National Grid', util)
create_company('NMC', 'NMC Health', heal)
create_company('NXT', 'Next', genr)
create_company('OML', 'Old Mutual Group', life)
create_company('PPB', 'Paddy Power Betfair', trav)
create_company('PRU', 'Prudential', life)
create_company('PSN', 'Persimmon', home)
create_company('PSON', 'Pearson', medi)
create_company('RB.', 'Reckitt Benckiser Group', home)
create_company('RBS', 'Royal Bank of Scotland Group', bank)
create_company('RDSA', 'Royal Dutch Shell', ogpr)
create_company('RDSB', 'Royal Dutch Shell', ogpr)
create_company('REL', 'RELX', medi)
create_company('RIO', 'Rio Tinto', mine)
create_company('RR.', 'Rolls-Royce Group', aero)
create_company('RRS', 'Randgold Resources', mine)
create_company('RSA', 'RSA Insurance Group', insu)
create_company('RTO', 'Rentokil Initial', supp)
create_company('SBRY', "Sainsbury's", fdre)
create_company('SDR', 'Schroders', fina)
create_company('SGE', 'Sage Group', soft)
create_company('SGRO', 'Segro', reit)
create_company('SHP', 'Shire', phar)
create_company('SKG', 'Smurfit Kappa Group', geni)
create_company('SKY', 'Sky', medi)
create_company('SLA', 'Standard Life Aberdeen', fina)
create_company('SMDS', 'Smith, D.S.', geni)
create_company('SMIN', 'Smiths Group', geni)
create_company('SMT', 'Scottish Mortgage Investment Trust', equi)
create_company('SN.', 'Smith & Nephew', heal)
create_company('SSE', 'SSE', elec)
create_company('STAN', 'Standard Chartered', bank)
create_company('STJ', "St James's Place", life)
create_company('SVT', 'Severn Trent', util)
create_company('SKG', 'Smurfit Kappa Group', geni)
create_company('TSCO', 'Tesco', fdre)
create_company('TUI', 'TUI AG', trav)
create_company('TW.', 'Taylor Wimpey', home)
create_company('ULVR', 'Unilever', fpro)
create_company('UU.', 'United Utilities Group', util)
create_company('VOD', 'Vodafone Group', mobi)
create_company('WPP', 'WPP Group', medi)
create_company('WTB', 'Whitbread', trav)
