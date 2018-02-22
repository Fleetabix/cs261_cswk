from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.

class DataTests(TestCase):
    """
        Tests for retreiving data for different companies.
        As you (probably) be able to build industry data from just
        querying all companies in that industry, we can only test
        getting data for companies
    """

    def get_company_spot_price(self):
        """
            Just check if a companies spot price can be retrieved
            and is in a valid format
        """
        self.assertIs(True, False)

    def get_non_existent_company_spot_price(self):
        """
            Test for whatever should be returned if the company does
            not exist. (could be an error that is thrown on purpose
            or a value that is specified as an error number)
        """
        self.assertIs(True, False)

    def get_company_percentage_change(self):
        self.assertIs(True, False)

    def get_non_existent_company_percentage_change(self):
        self.assertIs(True, False)

    def get_company_spot_price_over_time(self):
        self.assertIs(True, False)

    def get_non_existent_company_spot_price_over_time(self):
        self.assertIs(True, False)

    def get_company_spot_price_for_the_future(self):
        """
            A test to see what happens if you request a company's data
            for a time period in the future (like next week?)
        """
        self.assertIs(True, False)

    def get_company_spot_price_for_distant_past(self):
        """
            A test to see what happens if you request a company's data
            for a time period we can't access (e.g. 1950 or something)
        """
        self.assertIs(True, False)

    def get_company_news_from_specified_time(self):
        self.assertIs(True, False)

    def get_non_existent_company_news_from_specified_time(self):
        self.assertIs(True, False)

    def get_company_recent_news(self):
        self.assertIs(True, False)

    def get_non_existent_company_recent_news(self):
        self.assertIs(True, False)
