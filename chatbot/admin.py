from django.contrib import admin
from chatbot.models import Company, UserQueryData, PortfolioItem
# Register your models here.
admin.site.register(Company)
admin.site.register(UserQueryData)
admin.site.register(PortfolioItem)