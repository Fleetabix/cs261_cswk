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
#Still examples
create_company('GOOGL', 'Google', tech)
create_company('AAPL', 'Apple', tech)
create_company('BA.', 'BAE Systems PLC', aero)
