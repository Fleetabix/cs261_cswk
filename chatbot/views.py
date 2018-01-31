"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render

# Create your views here.

def index(request):
    """
        Returns the html for the chatbot
    """
    return render(request, 'chatbot/index.html')
