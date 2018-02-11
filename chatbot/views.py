"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def index(request):
    """
        Returns the html for the chatbot
    """
    return render(request, 'chatbot/index.html')

def ask_chatbot(request):
    query = request.POST.get('query')
    if (query == ":ex_chart"):
        data = getChartData()
    elif (query == ":ex_news"):
        data = getNewsData()
    else:
        data = getTextData(query)
    return JsonResponse(data)

def getTextData(query):
    """ 
        test for text response
    """
    return  {
                "name": "FLORIN",
                "type": "text",
                "body": "The current spot price of '" + query.split(" ")[0].upper() + "' is",
                "caption" : "£1,000,000"
            }
    
def getNewsData():
    """ 
        test for the news response
    """
    return  {
                "name": "FLORIN",
                "type": "news",
                "articles": [
                    {
                        "title": "Google says its AI can diagnose some eye diseases",
                        "description": "Uber settles with Google in tech theft lawsuit. Google's sister company Waymo sued Uber over the alleged theft of self-driving technology from it by a former employee. 17:09, UK, Friday 09 February 2018.",
                        "url": "https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=newssearch&cd=2&cad=rja&uact=8&ved=0ahUKEwjIv4_GsZnZAhXLKcAKHcZKCJMQqQIIKygAMAE&url=https%3A%2F%2Fnews.sky.com%2Fstory%2Fgoogle-says-its-ai-can-diagnose-some-eye-diseases-11237882&usg=AOvVaw1mAuYxK1tq29DQjK99ywmh",
                        "pic_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLpMwo-Fv6-An-FR73RDkqfPJH2oUOp9x1jELp3jdy8Kir40yHqWPA-otEadEmVYewxe1Wpic"
                    },
                    {
                        "title": "If you'd invested in: EasyJet and WPP",
                        "description": "In the first nine months, WPP's like-for-like revenue fell by 0.9% as huge customers cut marketing budgets after questioning the effectiveness of buying online advertisements through media firms, rather than turning to Google.", 
                        "url": "https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=newssearch&cd=3&cad=rja&uact=8&ved=0ahUKEwioo7zn1pnZAhUFJsAKHYE8CHoQqQIILigAMAI&url=https%3A%2F%2Fmoneyweek.com%2Fif-youd-invested-in-easyjet-and-wpp%2F&usg=AOvVaw2SGlOHd2vVPZVD8ZlDmwOP",
                        "pic_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZDtEeR1fMbghVy9LkwuVkJLADg9B7hagjaKRODMChHt6AHEeYQ5VzT3aFr0GSZUtNMnQuwwg"
                    }
                ]
            }

def getChartData():
    return  {
                "name": "FLORIN",
                "type": "chart",
                "chart_object": {
                    "type": "line",
                    "data": {
                        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                        "datasets": [
                            {
                                "label": "GOOG",
                                "data": [800, 1356, 1245, 1846, 2000]
                            },
                            {
                                "label": "AAPL",
                                "data": [650, 976, 1445, 1646, 2500]
                            }
                        ]
                    }
                },
                "description": "Google's spot price over the last week"
            }
