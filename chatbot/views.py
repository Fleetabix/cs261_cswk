"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def index(request):
    """
        Returns the html for the chatbot
    """
    return render(request, 'chatbot/index.html')

def ask_chatbot(request):
    query = request.POST.get('query')
    data = {
        "response": "FLORIN: you said '" + query + "'?"
    }
    return JsonResponse(data);