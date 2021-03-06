"""
    This is where the urls are mapped to view for the
    chabot app.
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask_chatbot/', views.ask_chatbot, name='ask_chatbot'),
    path('get_entities/', views.get_entities, name='get_entities'),
    path('add_to_portfolio/', views.add_to_portfolio, name='add_to_portfolio'),
    path('get_portfolio/', views.get_portfolio, name='get_portfolio'),
    path('get_welcome_briefing/', views.get_welcome_briefing, name='get_welcome_briefing'),
    path('get_price_drop_alerts/', views.get_price_drop_alerts, name='get_price_drop_alerts'),
    path('get_breaking_news/', views.get_breaking_news, name='get_breaking_news'),
    path('remove_from_portfolio/', views.remove_from_portfolio, name='remove_from_portfolio')
]
