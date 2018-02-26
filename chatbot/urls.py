"""
    This is where the urls are mapped to view for the
    chabot app.
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask_chatbot/', views.ask_chatbot, name='ask_chatbot'),
    path('get_entities/', views.get_entities, name='get_entities')
]
