from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import chatbot.data.news_handler as nh
import chatbot.data.stock_handler as sh

import datetime

# Create your models here.
class Company(models.Model):
    """
        The company model which will be stored in the database.
        The ticker is the primary key.
    """
    ticker = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=40)

    def getSpotPrice(self):
        """
            Returns spot price for specified company as a float
        """
        string_price = sh.getStockInformation(self.ticker).spot_price
        return float(string_price.replace(",", ""))

    def getSpotPriceDifference(self):
        """
            Returns difference between current and last spot price for
            specified company as a float
        """
        pc = sh.getStockInformation(self.ticker).price_difference
        return float(pc.replace(",", ""))

    def getSpotPercentageDifference(self):
        """
            Returns percentage difference between current and last spot
            price for specified company as a string
        """
        pc = sh.getStockInformation(self.ticker).percent_difference
        return float(pc.replace("%", ""))

    def getStockHistory(self, start, end):
        """
            Returns a pandas DataFrame for historical prices for specified
            company between a start and end date, will include the high and
            low for that day and opening price
        """
        return sh.getHistoricalStockInformation(self.ticker, start, end)

    def getNews(self):
        """
            Returns a list of NewsInformation objects of articles related to
            specified company from the last week
        """
        now = datetime.datetime.now()
        return self.getNewsFrom(now - datetime.timedelta(days=7), now)

    def getNewsTopic(self, topic):
        """
            Returns a list of NewsInformation objects of articles related to
            specified company and topic from the last week
        """
        now = datetime.datetime.now()
        return self.getNewsFrom(now - datetime.timedelta(days=7), now, topic)

    def getNewsFrom(self, start, end, topic = None):
        """
            Returns news published within the given start and end dates with
            optional topic
        """
        if topic is None:
            news = nh.getNews(self.name + ' plc')
        else:
            news = nh.getNews(self.name + ' plc', topic)
        in_range = lambda x: start <= x.date_published <= end
        return list(filter(in_range, news))


    def __str__(self):
        return self.ticker + " - " + self.name


class Industry(models.Model):
    """
        A model to store all various industries. The reason this
        exists rather than just have it as a field in the company
        model is so it's easier for whoever is mainting the db.
    """
    name = models.CharField(max_length=40)
    companies = models.ManyToManyField(Company)

    def getSpotPrice(self):
        """
            Gets the total spot price of all companies in the sector
        """
        return sum([float(c.getSpotPrice()) for c in self.companies.all()])

    def getSpotPriceDifference(self):
        """
            Returns sum of difference between current and last spot price for each
            company in the sector.
        """
        return sum([float(c.getSpotPriceDifference()) for c in self.companies.all()])

    def getSpotPercentageDifference(self):
        """
            Returns sum of percentage difference for all companies
            for all companies in the sector
        """
        total = sum([float(c.getSpotPercentageDifference()) for c in self.companies.all()])
        return total / len(self.companies.all())

    def getStockHistory(self, start, end):
        """
            Returns a pandas DataFrame for historical prices for specified company between a start and end date,
            will include the high and low for that day and opening price
        """
        return None

    def getNews(self):
        """
            Returns a list of NewsInformation objects of articles related to
            specified sector from the last week
        """
        now = datetime.datetime.now()
        return self.getNewsFrom(now - datetime.timedelta(days=7), now)

    def getNewsTopic(self, topic):
        """
            Returns a list of NewsInformation objects of articles related to
            specified company and topic from the last week
        """
        now = datetime.datetime.now()
        return self.getNewsFrom(now - datetime.timedelta(days=7), now, topic)

    def getNewsFrom(self, start, end, topic = None):
        """
            Returns news published within the given start and end dates, with
            optional topic
        """
        if topic is None:
            news = nh.getNews(self.name + ' sector')
        else:
            news = nh.getNews(self.name + ' sector', topic)

        in_range = lambda x: start <= x.date_published <= end
        return list(filter(in_range, news))

    def __str__(self):
            return self.name


@receiver(post_save, sender=Industry)
def create_industry(sender, instance, created, **kwargs):
    """
        If an industry is created create an alias for the
        industry with its name as the alias.
    """
    if created:
        IndustryAlias.objects.create(industry=instance, alias=instance.name)


@receiver(post_save, sender=Company)
def create_company(sender, instance, created, **kwargs):
    """
        If a company is created, create an aliases for the
        company with its name and the ticker as the alias.
    """
    if created:
        CompanyAlias.objects.create(company=instance, alias=instance.name)
        CompanyAlias.objects.create(company=instance, alias=instance.ticker)


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
    c_portfolio = models.ManyToManyField(Company)
    i_portfolio = models.ManyToManyField(Industry)

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
