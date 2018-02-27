from django.test import TestCase
from chatbot.models import Company, Industry

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
        mine = Industry.objects.create(name='Mining')
        mine.save()
        Company.objects.create(ticker='AAL', name='Anglo American')
        angloAmerican = Company.objects.get(name='Anglo American')
        angloAmerican.industries.add(mine)

        fake = Industry.objects.create(name='Fake companies')
        fake.save()
        Company.objects.create(ticker='NOPE', name='No exist')
        nonExistent = Company.objects.get(name='No exist')
        nonExistent.industries.add(fake)



    def test_get_company_spot_price(self):
        """
            Just check if a companies spot price can be retrieved
            and is in a valid format
        """        
        angloAmerican = Company.objects.get(name='Anglo American')
        
        print(angloAmerican.getSpotPrice())
        self.assertTrue(angloAmerican.getSpotPrice() != '')

    def test_get_non_existent_company_spot_price(self):
        """
            Test for whatever should be returned if the company does
            not exist. (could be an error that is thrown on purpose
            or a value that is specified as an error number)
        """
        nonExistent = Company.objects.get(name='No exist')
        self.assertIsNone(nonExistent.getSpotPrice())

    def test_get_company_percentage_change(self):
        """
            Make sure you can get a companies % change. Test for
            the format as well to make sure it's correct.
        """

        angloAmerican = Company.objects.get(name='Anglo American')

        self.assertTrue(angloAmerican.getSpotPercentageDifference() != '')

    def test_get_non_existent_company_percentage_change(self):
        """
            Test if the method handles when you ask for the % change
            of a company that doesn't exist.
        """
        nonExistent = Company.objects.get(name='No exist')
        self.assertIsNone(nonExistent.getSpotPercentageDifference())

        # self.assertTrue()

    def test_get_company_spot_price_over_time(self):
        """
            Can you get the spot price of a company over a period of 
            time? Make sure the list is of the right type etc.
        """


        self.assertTrue(False)

    def test_get_non_existent_company_spot_price_over_time(self):
        """
            Check what happens when you request the stock change
            of a company that doesn't exist.
        """
        self.assertTrue(False)

    def test_get_company_spot_price_for_the_future(self):
        """
            A test to see what happens if you request a company's data
            for a time period in the future (like next week?)
        """
        self.assertTrue(False)

    def test_get_company_spot_price_for_distant_past(self):
        """
            A test to see what happens if you request a company's data
            for a time period we can't access (e.g. 1950 or something)
        """
        self.assertTrue(False)

    def test_get_company_news_from_specified_time(self):
        """
            A test to see if we can get news of a company from a specific
            time period (e.g. in the last week)
        """
        self.assertTrue(False)

    def test_get_non_existent_company_news_from_specified_time(self):
        """
            Test what happens when you ask for news of a company that
            doesn't exists. Again, look to catch a specified error 
            or look for output that means an error.
        """
        self.assertTrue(False)

    def test_get_company_recent_news(self):
        """
            Test if it returns valid output and that they are all in
            the right time frame (probably defined in the method you're)
            testing.
        """
        self.assertTrue(False)

    def test_get_non_existent_company_recent_news(self):
        """
            Check what happens when we look for news of a 
            company that doesn't exist.
        """
        self.assertTrue(False)


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
        # tech = Industry.objects.create(name='Technology')
        # Company.objects.create(ticker='GOOGL', name='Google', industry=tech)

    def test_can_identify_ticker(self):
        """
            Can it get a ticker from a sentence.
        """
        self.assertTrue(False)

    def test_can_identify_multiple_tickers(self):
        """
            Can it get a tickers from a sentence containing many
            of them.
        """
        self.assertTrue(False)

    def test_can_identify_company_name(self):
        """
            Input a sentence containing a company name, check if
            it can identify it.
        """
        self.assertTrue(False)

    def test_can_identify_multiple_company_names(self):
        """
            Input a sentence containing multiple company name, check if
            it can identify it.
        """
        self.assertTrue(False)

    def test_can_identify_comparative_in_query(self):
        """
            Make sure to check for all the common compararives
            here such as 'more', 'greater', 'less than', 'better',
            'worse' etc.
        """
        self.assertTrue(False)

    def test_can_identify_industry_in_query(self):
        """
            Just looking for a single industry here.
        """
        self.assertTrue(False)

    def test_can_identify_multiple_industries_in_query(self):
        """
            Have multiple industries in the query and make sure it
            gets them all.
        """
        self.assertTrue(False)

    def test_can_identify_time_phrase(self):
        """
            Try different formats such as
                - '26 January 2017'
                - '02/12'
                - '2018'
            etc
        """
        self.assertTrue(False)

    def test_can_identify_relative_time_phrase(self):
        """
            Here test for things such as 'last week', 'today', 
            'this month' etc.
            
        """
        self.assertTrue(False)

    def test_can_identify_stock_price_query(self):
        """
            Does it give the correct response for a properly
            formatted stock price query?
        """
        self.assertTrue(False)

    def test_can_identify_news_query(self):
        """
            Can it identify the user asking for the news of a
            specific company. Try and test different things such as
            'recent news', 'news this week', 'news last month'
        """
        self.assertTrue(False)

    def test_can_identify_news_for_multiple_companies_query(self):
        """
            Same as above but make sure it can do it for more than
            one company. (Maybe doesn't have to be as rigourus as above
            in terms of the number of different phrases)
        """
        self.assertTrue(False)

    def test_gets_correct_keywords_from_comparative_phrase(self):
        """
            Check if it works with 2 and more companies, try it with
            different functions (compare spot price, % change, news)
        """
        self.assertTrue(False)

    def test_correct_response_from_nonesense_phrase(self):
        """
            Does it speak rubbish? Try a few examples.
        """
        self.assertTrue(False)
