from django.core.management.base import BaseCommand, CommandError
from chatbot.models import *
from random import random
import datetime

class Command(BaseCommand):
    help =  'alters the percentage difference for each company' + \
            'to a random amount under -10%'

    def add_arguments(self, parser):
        parser.add_argument('ticker', nargs='+', type=str)

        parser.add_argument(
                    '--delete-alerts',
                    action='store_true',
                    dest='delete-alerts',
                    help='Delete all alerts for the companies so users can be notified',
                )

    def handle(self, *args, **options):
        for c in Company.objects.all():
            if c.ticker in options['ticker']:
                try:
                    c = Company.objects.get(ticker=c.ticker)
                except Company.DoesNotExist:
                    raise CommandError('Company "%s" does not exist' % c.ticker)

                # set the price drop so that the system will be able to detect it
                r = -(random() * 30 + 11)
                
                c.stockinformation.percent_difference = r
                c.stockinformation.retrieved = datetime.datetime.now() + datetime.timedelta(minutes=1)
                c.stockinformation.save()
                c.save()

                self.stdout.write(self.style.SUCCESS("{0}'s price difference is now {1}%".format(c.ticker, "%.2f" % r)))

                # remove any alerts associated with the company so that the system is
                # cleared to notify the user
                if options["delete-alerts"]:
                    comp_alerts = Alert.objects.filter(company=c)
                    for a in comp_alerts:
                        a.delete()
                    self.stdout.write("All alerts for %s have been deleted" % c.ticker)
            else:
                # set the price drop so that the system will be able to detect it
                r = random() * 15 -7.5
                info = c.stockinformation
                info.percent_difference = r
                info.retrieved = datetime.datetime.now() + datetime.timedelta(minutes=1)
                info.save()
            