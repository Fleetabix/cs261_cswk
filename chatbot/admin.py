from django.contrib import admin
from chatbot.models import *
# Register your models here.
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(TraderProfile)
admin.site.register(CompanyHitCount)
admin.site.register(IndustryHitCount)
admin.site.register(CompanyAlias)
admin.site.register(IndustryAlias)
admin.site.register(Alert)
admin.site.register(StockInformation)