"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import datetime
import calendar

from chatbot.models import *
from chatbot.nl import nl
from chatbot.chart import Chart

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
            if request["quality"] == "joke":
                data["messages"].append(nl.turnIntoResponse("Why did the chicken cross the road?"))
            data["messages"].append(respond_to_request(request))
    return JsonResponse(data)

def respond_to_request(request):
    """
        Given a request object, find the relevant data
        and format it correctly.
    """
    quality = request["quality"]
    if quality == "price":
        #Responses to price
        return stock_price_response(request)
    elif quality == "news":
        return news_response(request)
    elif quality == "priceDiff":
        return price_difference_response(request)
    elif quality == "percentDiff":
        return percent_difference_response(request)
    elif quality == "stockHist":
        return stock_history_response(request)
    elif quality == "joke":
        if len(request["companies"]) == 0 and  len(request["areas"]) == 0:
            return nl.turnIntoResponse("To get to the other side.")
        else:
            companies = request["companies"]
            for i in request["areas"]:
                companies = union(companies, companiesInIndustry(i))
            return nl.turnIntoResponse("To buy stock in " + nl.makeList(companies) + ".")
    else:
        return nl.turnIntoResponse("ERROR: Cannot respond about " + quality)

def stock_price_response(request):
    companies = request["companies"]
    areas = request["areas"]
    comparative = request["comparative"]
    time = request["time"]
    if "now" not in time:
        return stock_history_response(request)
    if comparative is not None:
        group = companies
        for i in areas:
            group = union(group,companiesInIndustry(i))
        if len(group) == 0:
            group = allCompanies()
        return higherLower(comparative, group, "stock price", getSpotPrice, nl.printAsSterling)
    if len(companies) == 0:
        if len(areas) == 1:
            message = "Here's the current price of the " + areas[0] + " industry:"
            caption = Industry.objects.get(name = areas[0]).getSpotPrice()
            caption = nl.printAsSterling(caption)
            return nl.turnIntoResponseWithCaption(message, caption)
        #Response for no companies being listed.
        return nl.turnIntoResponse("You'll need to tell me the names of the companies you'd like the stock price of.")
    elif len(companies) == 1:
        message = "Here's " + nl.posessive(companies[0]) + " current price:"
        caption = Company.objects.get(ticker = companies[0]).getSpotPrice()
        caption = nl.printAsSterling(caption)
        return nl.turnIntoResponseWithCaption(message, caption)
    else:
        return makeBarChartOf(companies, "Current Stock price", getSpotPrice)

def percent_difference_response(request):
    companies = request["companies"]
    areas = request["areas"]
    comparative = request["comparative"]
    if comparative is not None:
        group = companies
        for i in areas:
            group = union(group,companiesInIndustry(i))
        if len(group) == 0:
            group = allCompanies()
        return higherLower(comparative, group, "percentage difference", getPercentDiff, nl.printAsPercent)
    if len(companies) == 0:
        if len(areas) == 1:
            message = "Here's the most recent percentage difference of the " + areas[0] + " industry:"
            caption = getPercentDiff(Industry.objects.get(name = areas[0]))
            caption = nl.printAsPercent(caption)
            return nl.turnIntoResponseWithCaption(message, caption)
        #Response for no companies being listed.
        return nl.turnIntoResponse("You'll need to tell me the names of the companies you'd like the percentage difference of.")
    elif len(companies) == 1:
        message = "Here's " + nl.posessive(companies[0]) + " most recent percentage difference:"
        caption = getPercentDiff(Company.objects.get(ticker = companies[0]))
        caption = nl.printAsPercent(caption)
        return nl.turnIntoResponseWithCaption(message, caption)
    else:
        return makeBarChartOf(companies, "Recent Percentage Difference", getPercentDiff)

def price_difference_response(request):
    companies = request["companies"]
    areas = request["areas"]
    comparative = request["comparative"]
    time = request["time"]
    if "now" not in time:
        return stock_history_response(request)
    if comparative is not None:
        group = companies
        for i in areas:
            group = union(group,companiesInIndustry(i))
        if len(group) == 0:
            group = allCompanies()
        return higherLower(comparative, group, "price difference", getPriceDiff, nl.printAsSterling)
    if len(companies) == 0:
        if len(areas) == 1:
            message = "Here's the most recent price difference of the " + areas[0] + " industry:"
            caption = getPriceDiff(Industry.objects.get(name = areas[0]))
            caption = nl.printAsSterling(caption)
            return nl.turnIntoResponseWithCaption(message, caption)
        #Response for no companies being listed.
        return nl.turnIntoResponse("You'll need to tell me the names of the companies you'd like the price difference of.")
    elif len(companies) == 1:
        message = "Here's " + nl.posessive(companies[0]) + " most recent price difference:"
        caption = getPriceDiff(Company.objects.get(ticker = companies[0]))
        caption = nl.printAsSterling(caption)
        return nl.turnIntoResponseWithCaption(message, caption)
    else:
        return makeBarChartOf(companies, "Recent Price Difference", getPriceDiff)

def stock_history_response(request):
    time = request["time"]
    start = time["start"]
    end = time["end"]
    if end > datetime.datetime.now():
        return nl.turnIntoResponse("Please provide a range of dates in the past.")
    if start == end:
        return nl.turnIntoResponse("Please provide a range of dates.")
    companies = request["companies"]
    for industry in request["areas"]:
        companies = union(companies, companiesInIndustry(industry))
    chart = Chart()
    desc = "Here's how the stock price of "
    l = []
    for company in companies:
        try:
            df = Company.objects.get(ticker = company).getStockHistory(start, end)
        except ValueError:
            return nl.turnIntoResponse("Please enter a more recent date.")
        chart.add_from_df(df, company)
        l.append(company)
    desc += nl.makeList(l)
    desc += " has changed between " + nl.printDate(start) + " and " + nl.printDate(end) + "."
    return nl.turnChartIntoChartResponse(chart.toJson(),desc)

def higherLower(comparative, companies, qualName, funct, formatFunct):
    caption = "Out of "
    companySet = []
    bestName = "???"
    bestPrice = -1
    higher = (comparative == "higher" or comparative == "highest")
    for company in companies:
        price = funct(Company.objects.get(ticker = company))
        if (price>bestPrice and higher) or (price<bestPrice and (not higher)) or bestPrice == -1:
            bestPrice = price
            bestName = company
        companySet.append(company)
    caption+=nl.makeList(companySet)
    if len(companies)>=100:
        caption = "Out of all companies"
    elif len(companies)>=8:
        caption = "Out of those companies"
    caption+=", " + bestName + " has the "
    if higher:
        caption+="highest "
    else:
        caption+="lowest "
    caption += qualName + ", at " + formatFunct(bestPrice) + "."
    return nl.turnIntoResponse(caption)

def news_response(request):
    time = request["time"]
    companies = request["companies"]
    articles = []
    for industry in request["areas"]:
        companies = union(companies, companiesInIndustry(industry))
    if len(companies) == 0:
        return nl.turnIntoResponse("Which companies would you like news about?")
    for company in companies:
        if "now" in time:
            news = Company.objects.get(ticker = company).getNews()
        else:
            news = Company.objects.get(ticker = company).getNewsFrom(time["start"], time["end"])
        for story in news:
            articles.append(nl.turnIntoArticle(story.headline, str(story.date_published), story.url, story.image))
    if len(articles) == 0:
        return nl.turnIntoResponse("I'm sorry, I couldn't find any news for "+ nl.makeOrList(companies))
    return nl.turnIntoNews(articles)

def makeBarChartOf(companies, qualName, funct):
    data = []
    caption = []
    counter = len(companies)
    for company in companies:
        price = funct(Company.objects.get(ticker = company))
        data.append({"label":company, "data":[price]})
        caption.append(nl.posessive(company) + " at " + nl.printAsSterling(price))
    return nl.turnIntoBarChart([qualName],data, nl.makeList(caption))

def getSpotPrice(obj):
    return obj.getSpotPrice()

def getPercentDiff(obj):
    return obj.getSpotPercentageDifference()

def getPriceDiff(obj):
    return obj.getSpotPriceDifference()

def union(list1, list2):
    return list1 + list(set(list2) - set(list1))

def companiesInIndustry(industryName):
    i = Industry.objects.get(name = industryName)
    return extractTickers(i.companies.all())

def allCompanies():
    return extractTickers(Company.objects.all())

def extractTickers(results):
    output = []
    for company in results:
        output.append(company.ticker)
    return output

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
            chart = Chart()
            chart.add_from_df(df=df, label=c.ticker + " - " + c.name)
            data[c.id]["historical"] = chart.toJson()
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
            # get the dataframes for each company in the industry
            dfs = i.getStockHistory(now - last_week, now)
            chart = Chart()
            #for each data frame, alter the chart by adding the new valus
            chart.add_from_df(df=dfs[0], label=i.name)
            for j in range(1, len(dfs)):
                df = dfs[j]
                chart.alter_from_df(df=df, rule=lambda x, y: x + y)
            data[i.id]["historical"] = chart.toJson()
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
