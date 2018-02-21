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

    def __str__(self):
            return self.ticker + " - " + self.name

class PortfolioItem(models.Model):
    """
        A link table that defines the relationship between a user and the
        multiple entities it can have in their portfolio
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    company_ticker = models.ForeignKey(Company, on_delete=models.CASCADE) 

class UserQueryData(models.Model):
    """
        This will store how many times a user has queried a company
        or industry.
        WARNING with the current model there will be no constraints on
        what you can put in here (as companies or industries will be able 
        to be search and stored here)
    """
    TYPE_CHOICES = (
        ('i', 'Industry'),
        ('c', 'Company')
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    entity_identifier = models.CharField(max_length=40)
    hit_count = models.IntegerField()