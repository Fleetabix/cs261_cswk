from chatbot.models import Company

def create_company(ticker, name, industry):
    """
        Method to create a company and save it in the database
    """
    c = Company(ticker=ticker, name=name, industry=industry)
    c.save()

# these are just examples
create_company('GOOGL', 'Google', 'Technology')
create_company('AAPL', 'Apple', 'Technology')
create_company('BA.', 'BAE Systems PLC', 'Aerospace & Defence')