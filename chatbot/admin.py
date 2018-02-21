from django.contrib import admin
from chatbot.models import Industry, Company, Trader, CompanyHitCount
# Register your models here.
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(Trader)
admin.site.register(CompanyHitCount)