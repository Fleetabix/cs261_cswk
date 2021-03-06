from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from chatbot.models import *

def create_industry(name, aliases=[]):
    """
        method to create an industry along with its aliases.
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
        industry.companies.add(c)
    # add all the aliases
    for alias in aliases:
        CompanyAlias.objects.create(company=c, alias=alias)


class Command(BaseCommand):
    help = 'Populates the database with companies, industries and other stuff'

    def handle(self, *args, **options):
        # List of industries
        # For each industry you can optionaly add
        # aliases so that florin can check for its other names when the user asks
        # example: leis = create_industry('leisure', ['alias1', 'alias2'])
        aero = create_industry(name = 'aerospace & defense', aliases=['aerospace', 'defense'])
        auto = create_industry(name = 'automobiles & parts', aliases=['automobiles'])
        bank = create_industry(name = 'banks', aliases=['bank'])
        beve = create_industry(name = 'beverages', aliases=['drinks'])
        chem = create_industry(name = 'chemicals')
        cons = create_industry(name = 'construction & materials', aliases=['construction'])
        elec = create_industry(name = 'electricity')
        eleq = create_industry(name = 'electronic & electrical equipment', aliases=['electronics'])
        equi = create_industry(name = 'equity investment instruments')
        fina = create_industry(name = 'financial services')
        tele = create_industry(name = 'fixed line telecommunications')
        fdre = create_industry(name = 'food & drug retailers', aliases=['food retailer', 'drug retailer'])
        fpro = create_industry(name = 'food producers', aliases=['food producer'])
        fore = create_industry(name = 'forestry & paper', aliases=['forestry', 'paper'])
        util = create_industry(name = 'gas, water & multiutilities', aliases=['gas', 'water', 'utilities'])
        geni = create_industry(name = 'general industrials')
        genr = create_industry(name = 'general retailers')
        heal = create_industry(name = 'healthcare equipment & services', aliases=['healthcare', 'healthcare equipment', 'healthcare services'])
        home = create_industry(name = 'household goods & home construction', aliases=['household goods', 'home construction'])
        inme = create_industry(name = 'industrial metals')
        life = create_industry(name = 'life insurance')
        medi = create_industry(name = 'media')
        mine = create_industry(name = 'mining')
        mobi = create_industry(name = 'mobile telecommunications')
        insu = create_industry(name = 'nonlife insurance')
        ogpr = create_industry(name = 'oil & gas producers', aliases=['oil producers', 'gas producers'])
        pers = create_industry(name = 'personal goods')
        phar = create_industry(name = 'pharmaceuticals & biotechnology', aliases=['pharmaceuticals', 'biotechnology'])
        reit = create_industry(name = 'real estate investment trusts', aliases=['real estate'])
        soft = create_industry(name = 'software & computer services', aliases=['software', 'computer services'])
        supp = create_industry(name = 'support services')
        tech = create_industry(name = 'technology hardware & equipment', aliases=['hardware', 'technical equipment'])
        toba = create_industry(name = 'tobacco')
        trav = create_industry(name = 'travel & leisure', aliases=['travel', 'leisure'])



        # List of FTSE100 companies.
        # Make sure the industries (even if it's just one) is in
        # a list - this applies to aliases to.
        create_company('AAL', 'Anglo American', [mine], ['Anglo American Plc'])
        create_company('ABF', 'Associated British Foods', [fpro], ['Associated British Foods Plc'])
        create_company('ADM', 'Admiral Group', [insu], ['Admiral Group Plc', 'Admiral'])
        create_company('AHT', 'Ashtead Group', [supp], ['Ashtead Group Plc', 'Ashtead'])
        create_company('ANTO', 'Antofagasta', [mine], ['Antofagasta Plc'])
        create_company('AV.', 'Aviva', [life], ['Aviva Plc', 'Aviva Insurance'])
        create_company('AZN', 'AstraZeneca', [phar], ['AstraZeneca Plc'])
        create_company('BA.', 'BAE Systems', [aero], ['BAE', 'BAE Systems Plc'])
        create_company('BARC', 'Barclays', [bank])
        create_company('BATS', 'British American Tobacco', [toba], ['BAT', 'British American Tobacco Plc'])
        create_company('BDEV', 'Barratt Developments', [home], ['Barratt', 'Barratt Developments Plc'])
        create_company('BKG', 'Berkeley Group Holdings', [home], ['Berkeley Group', 'Berkeley', 'Berkeley Group Holdings Plc'])
        create_company('BLND', 'British Land Co', [reit], ['British Land', 'British Land Company', 'British Land Co Plc', 'British Land Company Plc'])
        create_company('BLT', 'BHP Billiton', [mine], ['BHP Billiton Plc', 'BHP'])
        create_company('BNZL', 'Bunzl', [supp], ['Bunzl Plc'])
        create_company('BP.', 'BP', [ogpr], ['BP Plc', 'British Petroleum'])
        create_company('BRBY', 'Burberry Group', [pers], ['Burberry'])
        create_company('BT.A', 'BT Group', [tele], ['BT', 'BT Plc'])
        create_company('CCH', 'Coca-Cola HBC', [beve], ['Coca-Cola', 'Coca Cola'])
        create_company('CCL', 'Carnival', [trav], ['Carnival Corporation', 'Carnical Corporation & Plc', 'Carnival Cruise Line'])
        create_company('CNA', 'Centrica', [util], ['Centrica Plc'])
        create_company('CPG', 'Compass Group', [trav], ['Compass Group UK', 'Compass Group Plc'])
        create_company('CRDA', 'Croda International', [chem], ['Croda', 'Croda International Plc'])
        create_company('CRH', 'CRH', [cons], ['CRH Plc', 'Cement Roadstone Holdings'])
        create_company('DCC', 'DCC', [supp], ['DCC Plc', 'Development Capital Corporation'])
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
        create_company('HSBA', 'HSBC Holdings', [bank], ['HSBC'])
        create_company('IAG', 'International Consolidated Airlines Group', [trav])
        create_company('IHG', 'InterContinental Hotels Group', [trav], ['InterContinental'])
        create_company('III', '3i Group', [fina], ['3i'])
        create_company('IMB', 'Imperial Brands', [toba])
        create_company('INF', 'Informa', [medi])
        create_company('ITRK', 'Intertek Group', [supp], ['Intertek'])
        create_company('ITV', 'ITV', [medi])
        create_company('JE.', 'Just Eat', [genr])
        create_company('JMAT', 'Johnson Matthey', [chem])
        create_company('KGF', 'Kingfisher', [genr])
        create_company('LAND', 'Land Securities Group', [reit])
        create_company('LGEN', 'Legal & General Group', [life])
        create_company('LLOY', 'Lloyds Banking Group', [bank], ['Lloyds', 'Lloyds Bank'])
        create_company('LSE', 'London Stock Exchange Group', [fina], ['London Stock Exchange'])
        create_company('MCRO', 'Micro Focus International', [soft], ['Micro Focus'])
        create_company('MDC', 'Mediclinic International', [heal])
        create_company('MKS', 'Marks & Spencer Group', [genr], ['Marks and Spencer', 'Marks & Spencer', 'M & S', 'M and S'])
        create_company('MNDI', 'Mondi', [fore])
        create_company('MRW', 'Morrison Supermarkets', [fdre], ['Morrison', 'Morrisons'])
        create_company('NG.', 'National Grid', [util])
        create_company('NMC', 'NMC Health', [heal])
        create_company('NXT', 'Next', [genr])
        create_company('OML', 'Old Mutual Group', [life])
        create_company('PPB', 'Paddy Power Betfair', [trav], ['Paddy Power'])
        create_company('PRU', 'Prudential', [life])
        create_company('PSN', 'Persimmon', [home])
        create_company('PSON', 'Pearson', [medi])
        create_company('RB.', 'Reckitt Benckiser Group', [home], ['Reckitt Banckiser'])
        create_company('RBS', 'Royal Bank of Scotland Group', [bank], ['Royal Bank of Scotland'])
        create_company('RDSA', 'Royal Dutch Shell', [ogpr], ['Royal Dutch Shell A'])
        create_company('RDSB', 'Royal Dutch Shell', [ogpr], ['Royal Dutch Shell B'])
        create_company('REL', 'RELX', [medi])
        create_company('RIO', 'Rio Tinto', [mine])
        create_company('RR.', 'Rolls-Royce Group', [aero], ['RR', 'Rolls-Royce', 'Rolls Royce'])
        create_company('RRS', 'Randgold Resources', [mine])
        create_company('RSA', 'RSA Insurance Group', [insu], ['RSA Group Plc', 'RSA Group'])
        create_company('RTO', 'Rentokil Initial', [supp], ['Rentokil', 'Rentokil Initial Plc'])
        create_company('SBRY', "Sainsbury's", [fdre])
        create_company('SDR', 'Schroders', [fina], ['Schroders Plc'])
        create_company('SGE', 'Sage Group', [soft], ['Sage'])
        create_company('SGRO', 'Segro', [reit], ['Segro Plc'])
        create_company('SHP', 'Shire', [phar], ['Shire Plc'])
        create_company('SKG', 'Smurfit Kappa Group', [geni], ['Smurfit Kappa', 'Smurfit Kappa Corporate', 'Smurfit Kappa Group Plc'])
        create_company('SKY', 'Sky', [medi], ['Sky TV', 'Sky Television', 'Sky UK', 'Sky Plc'])
        create_company('SLA', 'Standard Life Aberdeen', [fina], ['Standard Life Aberdeen Plc'])
        create_company('SMDS', 'Smith, D.S.', [geni], ['DS Smith', 'DS Smith Plc'])
        create_company('SMIN', 'Smiths Group', [geni])
        create_company('SMT', 'Scottish Mortgage Investment Trust', [equi])
        create_company('SN.', 'Smith & Nephew', [heal], ['Smith and Nephew', 'Smith & Nephew Plc', 'Smith and Nephew Plc'])
        create_company('SSE', 'SSE', [elec])
        create_company('STAN', 'Standard Chartered', [bank], ['Standard Chartered Bank', 'Standard Chartered Plc'])
        create_company('STJ', "St James's Place", [life])
        create_company('SVT', 'Severn Trent', [util])
        create_company('TSCO', 'Tesco', [fdre], ['Tesco Plc'])
        create_company('TUI', 'TUI AG', [trav], ['TUI Group'])
        create_company('TW.', 'Taylor Wimpey', [home], ['Taylor Wimpey Plc'])
        create_company('ULVR', 'Unilever', [fpro])
        create_company('UU.', 'United Utilities Group', [util], ['United Utilities'])
        create_company('VOD', 'Vodafone Group', [mobi], ['Vodafone'])
        create_company('WPP', 'WPP Group', [medi])
        create_company('WTB', 'Whitbread', [trav], ['Whitbread Plc', 'Whitbread Group'])

        john = User.objects.create_user('johnsmith', email='john@mail.com', password='qwertyuiop')
        # add to portfolio
        for ticker in ['RR.', 'LLOY']:
            john.traderprofile.c_portfolio.add(Company.objects.get(ticker=ticker))
        john.traderprofile.i_portfolio.add(fina)
        # add hit counts
        company_hits = [(10, 'EZJ'), (12, 'BARC'), (27, 'RR.'), (7, 'LLOY'), (3, 'BA.'), (1, 'AAL')]
        for t in company_hits:
            c = Company.objects.get(ticker=t[1])
            CompanyHitCount.objects.create(company=c, trader=john.traderprofile, hit_count=t[0])
        IndustryHitCount.objects.create(industry=aero, trader=john.traderprofile, hit_count=3)
