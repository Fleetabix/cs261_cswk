from django.contrib import admin
from chatbot.models import Company, Trader, CompanyHitCount
# Register your models here.
admin.site.register(Company)
admin.site.register(Trader)
admin.site.register(CompanyHitCount)