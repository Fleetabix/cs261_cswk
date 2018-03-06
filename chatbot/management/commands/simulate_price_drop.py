from django.core.management.base import BaseCommand, CommandError
from chatbot.models import *
from random import random
import datetime

class Command(BaseCommand):
    help =  'alters the percentage difference for each company' + \
            'to a random amount under -10%'

    def add_arguments(self, parser):
        parser.add_argument('ticker', nargs='+', type=str)

    def handle(self, *args, **options):
        for ticker in options['ticker']:
            try:
                c = Company.objects.get(ticker=ticker)
            except Poll.DoesNotExist:
                raise CommandError('Company "%s" does not exist' % ticker)

            r = -(random() * 30 + 11)
            info = c.stockinformation
            info.percent_difference = r
            info.retrieved = datetime.datetime.now() + datetime.timedelta(minutes=1)
            info.save()
            self.stdout.write(self.style.SUCCESS("{0}'s price difference is now {1}%".format(ticker, "%.2f" % r)))