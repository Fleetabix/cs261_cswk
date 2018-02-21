from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Company(models.Model):
    """
        The company model which will be stored in the database.
        The ticker is the primary key.
    """
    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    industry = models.CharField(max_length=40)

    def __str__(self):
            return self.ticker + " - " + self.name


class Trader(models.Model):
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
        t = Trader(user=instance)
        t.save()


@receiver(post_save, sender=User)
def save_trader(sender, instance, **kwargs):
    """
        If a user's is saved, save the information of 
        the equivelent trader.
    """
    instance.trader.save()


class CompanyHitCount(models.Model):
    """
        This will store how many times a user has queried a company.
    """
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    hit_count = models.IntegerField()

    def __str__(self):
            return str(self.trader) +  \
            " | " + str(self.company) + \
            " | " + str(self.hit_count)