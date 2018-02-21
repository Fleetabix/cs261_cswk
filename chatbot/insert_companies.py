from chatbot.models import Industry, Company

def create_company(ticker, name, industry):
    """
        Method to create a company and save it in the database
    """
    c = Company(ticker=ticker, name=name, industry=industry)
    c.save()

# these are just examples
tech = Industry(name='technology')
fin = Industry(name='financial')
aero = Industry(name='aerospace')

create_company('GOOGL', 'Google', tech)
create_company('AAPL', 'Apple', tech)
create_company('BA.', 'BAE Systems PLC', aero)