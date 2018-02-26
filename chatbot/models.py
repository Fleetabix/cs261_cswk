from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import chatbot.data.news_handler
import chatbot.data.stock_handler

# Create your models here.


class Industry(models.Model):
    """
        A model to store all various industries. The reason this
        exists rather than just have it as a field in the company
        model is so it's easier for whoever is mainting the db.
    """
    name = models.CharField(max_length=40)

    def __str__(self):
            return self.name


class Company(models.Model):
    """
        The company model which will be stored in the database.
        The ticker is the primary key.
    """
    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    industries = models.ManyToManyField(Industry)

    def getSpotPrice(self):
        """
            Returns spot price for specified company as a string
        """
        return chatbot.data.stock_handler.getStockInformation(self.ticker).spot_price

    def getSpotPriceDifference(self):
        """
            Returns difference between current and last spot price for specified company as a string
        """
        return chatbot.data.stock_handler.getStockInformation(self.ticker).price_difference

    def getSpotPercentageDifference(self):
        """
            Returns percentage difference between current and last spot price for specified company as a string
        """
        return chatbot.data.stock_handler.getStockInformation(self.ticker).percent_difference

    def getStockHistory(self, start, end):
        """
            Returns a pandas DataFrame for historical prices for specified company between a start and end date,
            will include the high and low for that day and opening price
        """
        return chatbot.data.stock_handler.getHistoricalStockInformation(self.ticker, start, end)

    def getNews(self):
        """
            Returns a list of NewsInformation objects of articles related to specified company
        """
        return chatbot.data.news_handler.getNews(self.ticker)
      
    def __str__(self):
        return self.ticker + " - " + self.name


class CompanyAlias(models.Model):
    """
        Stores aliases for the specified company.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    alias = models.CharField(max_length=40)

    def __str__(self):
            return self.company.ticker + " - " + self.alias


class IndustryAlias(models.Model):
    """
        Stores aliases for the specified company.
    """
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    alias = models.CharField(max_length=40)

    def __str__(self):
            return self.industry.name + " - " + self.alias



class TraderProfile(models.Model):
    """
        An extension to the user class so that we can store many
        to many relationships with the Compamy model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio = models.ManyToManyField(Company)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_trader(sender, instance, created, **kwargs):
    """
        If a user is created create the equivelent trader.
    """
    if created:
        t = TraderProfile(user=instance)
        t.save()


@receiver(post_save, sender=User)
def save_trader(sender, instance, **kwargs):
    """
        If a user's is saved, save the information of 
        the equivelent trader.
    """
    instance.traderprofile.save()


class CompanyHitCount(models.Model):
    """
        This will store how many times a user has queried a company.
    """
    trader = models.ForeignKey(TraderProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    hit_count = models.IntegerField()

    def __str__(self):
            return str(self.trader) +  \
                " | " + str(self.company) + \
                " | " + str(self.hit_count)
