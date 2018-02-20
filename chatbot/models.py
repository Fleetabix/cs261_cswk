from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Company(models.Model):
    """
        The company model which will be stored in the database.
        The ticker is the primary key.
    """
    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    industry = models.CharField(max_length=40)

    def getStockPrice(self):
        return None

    def getPercentageDifference(self):
        return None

    def getPriceOverTime(self, time):
        return None

    def getNews(self):
        return None

    def __str__(self):
            return self.name

class PortfolioItem(models.Model):
    """
        A link table that defines the relationship between a user and the
        multiple entities it can have in their portfolio
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    company_ticker = models.ForeignKey(Company, on_delete=models.CASCADE) 