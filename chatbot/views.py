"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from chatbot.models import *
import datetime
import calendar

from chatbot.nl import nl

# Create your views here.

@login_required
def index(request):
    """
        Returns the html for the chatbot.
    """
    return render(request, 'chatbot/index.html')


@login_required
def ask_chatbot(request):
    """
        Given a query in the POST data, it will
        parse the message then return a valid response.
    """
    query = request.POST.get("query")
    data = {
        "name": "FLORIN",
        "messages": []
    }
    requests = nl.getRequests(query)
    if requests == [] or requests == None:
        data["messages"].append(nl.genericUnknownResponse())
    else:
        for request in requests:
            data["messages"].append(respond_to_request(request))
    return JsonResponse(data)

def respond_to_request(request):
    """
        Given a request object, find the relevant data
        and format it correctly.
    """
    quality = request["quality"]
    companies = request["companies"]
    if quality == "price":
        #return nl.turnIntoResponse("--Message about price--")
        if len(companies) == 1:
            return nl.turnIntoResponse("You told me one company")
        return nl.turnIntoBarChart(["one", "two"],[{"label":"TSCO", "data":[100,200]}], "Tesco stock price")
    elif quality == "news":
        return nl.turnIntoResponse("--Message about news--")
    elif quality == "priceDiff":
        return nl.turnIntoResponse("--Message about price difference--")
    elif quality == "percentDiff":
        return nl.turnIntoResponse("--Message about percentage difference--")
    elif quality == "stockHist":
        return nl.turnIntoResponse("--Message about stock history--")
    else:
        return nl.turnIntoResponse("ERROR: Cannot respond about " + quality)


@login_required
def get_entities(request):
    """
        Used to get a list of matching entities (at this
        moment just companies) given a query.
    """
    entity_type = request.GET.get('type')
    query = request.GET.get('query')
    user = request.user
    result_set = None
    # get all companies or industries (depending on the type) that have
    # aliases like the query but are not in the user's portfolio
    if entity_type == "industry":
        result_set = IndustryAlias.objects \
            .exclude(industry__in=user.traderprofile.i_portfolio.all()) \
            .filter(alias__contains=query)
    else:
        result_set = CompanyAlias.objects \
            .exclude(company__in=user.traderprofile.c_portfolio.all()) \
            .filter(alias__contains=query)

    # add all the companies we got to the data object to return
    data = {}
    for r in result_set:
        e = r.industry if (entity_type == "industry") else r.company
        key = e.id
        data[e.id] = {
            "name": e.name
        }
        # if we are searching for companies, add the ticker
        if entity_type == "company":
            data[e.id]["ticker"] = e.ticker
    return JsonResponse({"type": entity_type, "data": data})


@login_required
def add_to_portfolio(request):
    """
        Given a ticker in the request. Add the relevant company to the
        user's portfolio.
    """
    user = request.user
    entity_type = request.POST.get("type")
    if entity_type == "industry":
        i = Industry.objects.get(id=request.POST.get("id"))
        user.traderprofile.i_portfolio.add(i)
    else:
        c = Company.objects.get(id=request.POST.get("id"))
        user.traderprofile.c_portfolio.add(c)
    return JsonResponse({"status": "whooohoo!"})


@login_required
def get_portfolio(request):
    """
        Returns all the companies and industries the user has in
        their portfolio.
    """
    data = {}
    user = request.user
    include_historical = request.GET.get("historical")
    # get all the companies in the user's portfolio
    companies = user.traderprofile.c_portfolio.all()
    now = datetime.datetime.today()
    last_week = datetime.timedelta(days=7)
    for c in companies:
        data[c.id] = {
            "type": "company",
            "ticker": c.ticker,
            "name": c.name,
            "price": c.getSpotPrice(),
            "change": c.getSpotPercentageDifference(),
        }
        if include_historical == "true":
            df = c.getStockHistory(now - last_week, now)
            # for each entry in the dataframe, get the date, the
            # value and pass them to the create_simple_chart function
            dates = [df.iloc[i].name for i in range(len(df))]
            data[c.id]["historical"] = simple_line_chart \
                (
                    line_name=c.ticker + " - " + c.name,
                    labels=[calendar.day_name[x.weekday()][:3] for x in dates],
                    values=[df.iloc[i].Close for i in range(len(df))]
                )
    # get all the industries in the user's portfolio
    industries = user.traderprofile.i_portfolio.all()
    for i in industries:
        data[i.id] = {
            "type": "industry",
            "name": i.name,
            "price": i.getSpotPrice(),
            "change": i.getSpotPercentageDifference()
        }
        if include_historical == "true":
            data[i.id]["historical"] = simple_line_chart \
                (
                    i.name,
                    labels=[],
                    values=[]
                )
    return JsonResponse(data)


@login_required
def remove_from_portfolio(request):
    entity_type = request.POST.get("type")
    id = request.POST.get("id")
    user = request.user
    if entity_type == "industry":
        user.traderprofile.i_portfolio.remove(Industry.objects.get(id=id))
    else:
        user.traderprofile.c_portfolio.remove(Company.objects.get(id=id))
    return JsonResponse({"status": "yehhhhh!"})

def simple_line_chart(line_name, labels, values):
    """
        Creates a simple line graph with 1 line where labels is the
        x-axis and values is the y axis.
    """
    #TODO do this function
    return  {
                "type": "line",
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "label": line_name,
                            "data" : values,
                            "lineTension": 0
                        }
                    ]
                }
            }


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
