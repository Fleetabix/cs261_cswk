from django.test import TestCase
from chatbot.models import *

from chatbot.nl import nl

import datetime
import monthdelta

# Create your tests here. All test methods names should 
# start with the word 'test'

class DataTests(TestCase):
    """
        Tests for retreiving data for different companies.
        As you (probably) be able to build industry data from just
        querying all companies in that industry, we can only test
        getting data for companies
    """

    def setUp(self):
        """
            Insert companies into the data base here for
            NLP methods to use if the need them. These will not be saved
            as they are stored in a transaction, then dropped after the
            test class is done (so go wild).
        """
        self.mine = Industry.objects.create(name='Mining')
        self.aa = Company.objects.create(ticker='AAL', name='Anglo American')
        self.rr = Company.objects.create(ticker='RRS', name='Randgold Resources')
        self.mine.companies.add(self.aa)
        self.mine.companies.add(self.rr)
        # the non existent company
        self.ne = Company.objects.create(ticker='ZZZ', name='GiveUsYourMoney')
        # some datetime stuff to help with historical data
        self.now = datetime.datetime.now()
        self.delta_week = datetime.timedelta(days=7)
        self.the_past = datetime.timedelta(days=200000)

    def test_get_company_spot_price(self):
        """
            Just check if a companies spot price can be retrieved
            and is in a valid format
        """        
        price = self.aa.getSpotPrice()
        # checks price is not none (none is falsey)
        self.assertTrue(price)
        self.assertGreaterEqual(price,  0)
        self.assertIsInstance(price, float)

    def test_get_company_percentage_change(self):
        """
            Make sure you can get a companies % change. Test for
            the format as well to make sure it's correct.
        """
        change = self.rr.getSpotPercentageDifference()
        self.assertTrue(change)
        self.assertIsInstance(change, float)
        self.assertGreaterEqual(change, -500)
        self.assertLessEqual(change, 500)

    def test_get_company_spot_price_over_time(self):
        """
            Can you get the spot price of a company over a period of 
            time? Make sure the list is of the right type etc.
        """
        df = self.aa.getStockHistory(self.now - self.delta_week, self.now)
        self.assertIsNot(df, None)
        # there should be 5 entries (as markets are not open on the weekends)
        self.assertEqual(len(df), 5)
        # check all dates in the dataframe are within 7 days of today
        for date in [df.iloc[i].name for i in range(len(df))]:
            self.assertLessEqual((self.now - date).days, 7)

    def test_get_company_spot_price_for_the_future(self):
        """
            A test to see what happens if you request a company's data
            for a time period in the future (like next week?)
        """
        with self.assertRaisesMessage(ValueError, "This date range goes into the future!"):
            self.ne.getStockHistory(self.now, self.now + self.delta_week)

    def test_get_company_spot_price_for_distant_past(self):
        """
            A test to see what happens if you request a company's data
            for a time period we can't access (e.g. 1950 or something)
        """
        with self.assertRaisesMessage(ValueError, "Date range goes to far in the past!"):
            self.ne.getStockHistory(self.now - self.the_past, self.now)

    def test_get_company_news_from_specified_time(self):
        """
            A test to see if we can get news of a company from a specific
            time period (e.g. in the last week)
        """
        news = self.aa.getNewsFrom(self.now - self.delta_week, self.now)
        for article in news:
            self.assertGreaterEqual(article.date_published, self.now - self.delta_week)
            self.assertLessEqual(article.date_published, self.now)

    def test_get_company_recent_news(self):
        """
            Test if it returns valid output and that they are all in
            the right time frame (probably defined in the method you're)
            testing.
        """
        news = self.aa.getNews()
        for article in news:
            self.assertGreaterEqual(article.date_published, self.now - self.delta_week)
            self.assertLessEqual(article.date_published, self.now)


class NLPTests(TestCase):
    """
        Tests for the NLP functions.
    """

    def setUp(self):
        """
            Insert companies into the data base here for
            NLP methods to use if the need them. These will not be saved
            as they are stored in a transaction, then dropped after the
            test class is done (so go wild).
        """
        self.tech = self.create_industry(name='Technology')
        self.reta = self.create_industry(name='Retailers')
        self.mining = self.create_industry(name='Mining')

        self.goog = self.create_company(ticker='GOOGL', name='Google', industries=[self.tech], aliases=["Alphabet"])
        self.amaz = self.create_company(ticker='AMZ', name='Amazon', industries=[self.tech, self.reta])
        self.hans = self.create_company(ticker='HNS', name='Hanson', industries=[self.mining], aliases=['Hanson PLC'])


    def create_industry(self, name, aliases=[]):
        """
            method to create an industry along with its aliases.
        """
        i = Industry.objects.create(name=name)
        for alias in aliases:
            IndustryAlias.objects.create(industry=i, alias=alias)
        return i


    def create_company(self, ticker, name, industries, aliases=[]):
        """
            method to create a company and save it in the database
            along with it's industries and aliases.
        """
        c = Company.objects.create(ticker=ticker, name=name)
        # add all the industries
        for industry in industries:
            industry.companies.add(c)
        # add all the aliases
        for alias in aliases:
            CompanyAlias.objects.create(company=c, alias=alias)


    def test_can_identify_ticker(self):
        """
            Can it get a ticker from a sentence.
        """
        ticker = "AMZ"
        queries = [
            "what is the price of $", 
            "get me % change of $ blah",
            "$ blah sjh dsjjjh news change"
            ]
        responses = [nl.getRequests(x.replace("$", ticker)) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for r in rq: 
                self.assertTrue(ticker in r["companies"])

    def test_can_identify_multiple_tickers(self):
        """
            Can it get a tickers from a sentence containing many
            of them.
        """
        queries = [
            "what is the price of AMZ and GOOGL", 
            "get me % change of HNS & AMZ blah",
            "Is GOOGL doing as well as AMZ and HNS on stock price this week?"
            ]
        responses = [nl.getRequests(x) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for r in rq: 
                self.assertTrue(len(r["companies"]) > 1)

    def test_can_identify_company_name(self):
        """
            Input a sentence containing a company name, check if
            it can identify it.
        """
        ticker = "GOOGL"
        queries = [
            "what is the price of google", 
            "get me % change of Google blah",
            "Google blah sjh dsjjjh news change"
            ]
        responses = [nl.getRequests(x) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for r in rq: 
                self.assertTrue(ticker in r["companies"])

    def test_can_identify_multiple_company_names(self):
        """
            Input a sentence containing multiple company name, check if
            it can identify it.
        """
        queries = [
            "what is the price of amazon and google", 
            "get me % change of Hanson & Amazon blah",
            "Is Google doing as well as Amazon and Hanson on stock price this week?"
            ]
        responses = [nl.getRequests(x) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for r in rq: 
                self.assertTrue(len(r["companies"]) > 1)

    def test_can_identify_company_alias(self):
        """
            Tests to see if a company can be obtained with an alias
        """
        ticker = "GOOGL"
        queries = [
            "what is the price of alphabet", 
            ]
        responses = [nl.getRequests(x) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for r in rq: 
                self.assertTrue(ticker in r["companies"])
        
    def test_can_identify_multiple_company_aliases(self):
        """
            Tests to see if multiple companies can be obtained with their aliases
        """
        #TODO find out why second query fails
        queries = [
            "what is the price of amz and alphabet", 
            "What is the % change of PLC, google and amz",
            "Is google doing as well as amazon and hanson plc on stock price this week?"
            ]
        responses = [nl.getRequests(x) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for r in rq: 
                self.assertTrue(len(r["companies"]) > 1)

    def test_can_identify_comparative_in_query(self):
        """
            Make sure to check for all the common compararives
            here such as 'more', 'greater', 'less than', 'better',
            'worse' etc.
        """
        comparatives = ["higher", "highest", "worse"]
        queries = [
            "Is AMZ tock price greater than GOOGL", 
            "Who has the best percentage change out of HMS and amazon",
            "Is google doing worse than amazon?"
            ]
        responses = [nl.getRequests(x) for x in queries]
        self.assertIsNot(responses, None)
        for rq in responses:
            for i in range(len(rq)): 
                self.assertIsNot(rq[i]["comparative"], None)
                self.assertTrue(comparatives[i] in rq[i]["comparative"])

    def test_can_identify_industry_in_query(self):
        """
            Just looking for a single industry here.
        """
        queries = [
            "blah blah blah mining blAH PRICE",
            "what is the stock history of technology like",
            "what is the percentage change for mining?"
        ]
        requests = list(map(lambda x: nl.getRequests(x), queries))
        self.assertIsNot(requests, None)
        for r in requests:
            self.assertIsNotNone(r[0]["areas"])
            self.assertEqual(len(r[0]["areas"]), 1)

    def test_can_identify_multiple_industries_in_query(self):
        """
            Have multiple industries in the query and make sure it
            gets them all.
        """
        queries = [
            "blah blah technology blah mining blAH PRICE",
            "what is the stock history of technology and mining like",
            "what is the percentage change for mining, technology and blah?"
        ]
        requests = list(map(lambda x: nl.getRequests(x), queries))
        for r in requests:
            self.assertIsNotNone(r[0]["areas"])
            self.assertEqual(len(r[0]["areas"]), 2)

    def test_can_identify_time_phrase(self):
        """
            Try different formats such as
                - '26 January 2017'
                - '02/12'
                - '2018'
            etc
        """
        start_times = [
            datetime.datetime.strptime('26/01/2018', '%d/%m/%Y'),
            datetime.datetime.strptime('02/02/2018', '%d/%m/%Y'),
            datetime.datetime.strptime('01/01/2018', '%d/%m/%Y')
        ]
        queries = [
            "what has googles stock price been like from the 26th January?",
            "Give me news of amazon dated from 02/02",
            "Show me hanson's stock price in 2018"
        ]
        requests = list(map(lambda x: nl.getRequests(x), queries))
        for i in range(len(requests)):
            time = start_times[i]
            r = requests[i][0]
            self.assertEqual(time.year, r["time"]["start"].year)
            self.assertEqual(time.month, r["time"]["start"].month)
            self.assertEqual(time.day, r["time"]["start"].day)

    def test_can_identify_relative_time_phrase(self):
        """
            Here test for things such as 'last week', 'today', 
            'this month' etc.
            
        """
        start_times = [
            datetime.datetime.now() - datetime.timedelta(days=7),
            datetime.datetime.now() - monthdelta.monthdelta(1) - datetime.timedelta(days=1),
            datetime.datetime.now() 
                - datetime.timedelta(days=datetime.datetime.now().weekday())
                + datetime.timedelta(days=4, weeks=-1)
        ]
        queries = [
            "what has googles stock price been like for last week?",
            "Give me news of amazon from the last month",
            "Show me hanson's stock price from last friday"
        ]
        requests = list(map(lambda x: nl.getRequests(x), queries))
        for i in range(len(requests)):
            time = start_times[i]
            r = requests[i][0]["time"]["start"]
            self.assertEqual(time.year, r.year)
            self.assertEqual(time.month, r.month)
            self.assertEqual(time.day, r.day)

    def test_can_identify_stock_price_query(self):
        """
            Does it give the correct response for a properly
            formatted stock price query?
        """
        ticker = "HNS"
        industry = "Mining"
        queries = [
            "What is the spot price for hanson?",
            "Give me the current price for HNS",
            "mining price",
        ]
        requests = list(map(lambda x: nl.getRequests(x), queries))
        self.assertIsNot(requests, None)
        for r in requests:
            self.assertIsNot(r, None)
            self.assertTrue((ticker in r[0]["companies"]) or (industry in r[0]["areas"]))
            self.assertIn("price", r[0]["quality"])
            
    def test_can_identify_news_query(self):
        """
            Can it identify the user asking for the news of a
            specific company. Try and test different things such as
            'recent news', 'news this week', 'news last month'
        """
        entity = ["GOOGL", "AMZ", "Technology"]
        queries = [
            "give me the recent news of google",
            "news for AMZ since last wednesday",
            "is there any news about technology this week"
        ]
        requests = list(map(lambda x: nl.getRequests(x), queries))
        for i in range(len(requests)):
            r = requests[i][0]
            e = entity[i]
            self.assertIn("news", r["quality"])
            self.assertIn(e, set().union(r["companies"], r["areas"]))

    def test_can_identify_news_for_multiple_companies(self):
        """
            Same as above but make sure it can do it for more than
            one company. (Maybe doesn't have to be as rigourus as above
            in terms of the number of different phrases)
        """
        query = "give me the news for google, amazon and mining"
        r = nl.getRequests(query)[0]
        self.assertIsNot(r, None)
        self.assertIn("news", r["quality"])
        self.assertSetEqual(set(["GOOGL", "AMZ", "Mining"]), set().union(r["companies"], r["areas"]))

    def test_gets_correct_keywords_from_comparative_phrase(self):
        """
            Check if it works with 2 and more companies, try it with
            different functions (compare spot price, % change, news)
        """
        q1 = "get me the highest stock price out of amazon, google and hanson"
        q2 = "does mining have a worse % change than Technology"

        r1 = nl.getRequests(q1)
        r2 = nl.getRequests(q2)
        self.assertSetEqual(set(["GOOGL", "AMZ", "HNS"]), set(r1[0]["companies"]))
        self.assertIn("price", r1[0]["quality"])
        self.assertSetEqual(set(["Mining", "Technology"]), set(r2[0]["areas"]))
        self.assertIn("percentDiff", r2[0]["quality"])

    def test_correct_response_from_nonesense_phrase(self):
        """
            Does it speak rubbish? Try a few examples.
        """
        self.assertEqual([], nl.getRequests("sjkhd kahjd kjsahd kajshd jkas dk"))
