from django.test import TestCase
from chatbot.models import Company

# Create your tests here. All test methods names should 
# start with the word 'test'

class DataTests(TestCase):

    """
        Tests for retreiving data for different companies.
        As you (probably) be able to build industry data from just
        querying all companies in that industry, we can only test
        getting data for companies
    """

    def test_get_company_spot_price(self):
        """
            Just check if a companies spot price can be retrieved
            and is in a valid format
        """
        self.assertIs(True, False)

    def test_get_non_existent_company_spot_price(self):
        """
            Test for whatever should be returned if the company does
            not exist. (could be an error that is thrown on purpose
            or a value that is specified as an error number)
        """
        self.assertIs(True, False)

    def test_get_company_percentage_change(self):
        """
            Make sure you can get a companies % change. Test for
            the format as well to make sure it's correct.
        """
        self.assertIs(True, False)

    def test_get_non_existent_company_percentage_change(self):
        """
            Test if the method handles when you ask for the % change
            of a company that doesn't exist.
        """
        self.assertIs(True, False)

    def test_get_company_spot_price_over_time(self):
        """
            Can you get the spot price of a company over a period of 
            time? Make sure the list is of the right type etc.
        """
        self.assertIs(True, False)

    def test_get_non_existent_company_spot_price_over_time(self):
        """
            Check what happens when you request the stock change
            of a company that doesn't exist.
        """
        self.assertIs(True, False)

    def test_get_company_spot_price_for_the_future(self):
        """
            A test to see what happens if you request a company's data
            for a time period in the future (like next week?)
        """
        self.assertIs(True, False)

    def test_get_company_spot_price_for_distant_past(self):
        """
            A test to see what happens if you request a company's data
            for a time period we can't access (e.g. 1950 or something)
        """
        self.assertIs(True, False)

    def test_get_company_news_from_specified_time(self):
        """
            A test to see if we can get news of a company from a specific
            time period (e.g. in the last week)
        """
        self.assertIs(True, False)

    def test_get_non_existent_company_news_from_specified_time(self):
        """
            Test what happens when you ask for news of a company that
            doesn't exists. Again, look to catch a specified error 
            or look for output that means an error.
        """
        self.assertIs(True, False)

    def test_get_company_recent_news(self):
        """
            Test if it returns valid output and that they are all in
            the right time frame (probably defined in the method you're)
            testing.
        """
        self.assertIs(True, False)

    def test_get_non_existent_company_recent_news(self):
        """
            Check what happens when we look for news of a 
            company that doesn't exist.
        """
        self.assertIs(True, False)
