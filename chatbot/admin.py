from django.contrib import admin
from chatbot.models import Industry, Company, TraderProfile, CompanyHitCount, Alias
# Register your models here.
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(TraderProfile)
admin.site.register(CompanyHitCount)
admin.site.register(Alias)