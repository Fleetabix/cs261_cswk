import datetime
from django.utils import timezone
import calendar
from random import randint

from chatbot.models import *
from chatbot.nl import nl
from chatbot.chart import Chart

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
    elif quality == "volume":
        return volume_response(request)
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
        #Special text response for just one industry:
        if len(areas) == 1:
            message = "Here's the current price of the " + areas[0] + " industry:"
            caption = Industry.objects.get(name = areas[0]).getSpotPrice()
            caption = nl.printAsSterling(caption)
            return nl.turnIntoResponseWithCaption(message, caption)
        elif len(areas) == 0:
            return nl.turnIntoResponse("You'll need to tell me the names of the companies you'd like the stock price of.")
    elif len(companies) == 1 and len(areas)==0:
        message = "Here's " + nl.posessive(companies[0]) + " current price:"
        caption = Company.objects.get(ticker = companies[0]).getSpotPrice()
        caption = nl.printAsSterling(caption)
        return nl.turnIntoResponseWithCaption(message, caption)
    #If no special conditions are met:
    return makeBarChartOf(companies, "Current Stock price", getSpotPrice, areas)

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
        return makeBarChartOf(companies, "Recent Percentage Difference", getPercentDiff, [], lambda x: "%.2f%%" % x)

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
        elif len(areas) == 0:
            #Response for no companies or industries being listed.
            return nl.turnIntoResponse("You'll need to tell me the names of the companies you'd like the price difference of.")
    elif len(companies) == 1:
        message = "Here's " + nl.posessive(companies[0]) + " most recent price difference:"
        caption = getPriceDiff(Company.objects.get(ticker = companies))
        caption = nl.printAsSterling(caption)
        return nl.turnIntoResponseWithCaption(message, caption)
    #If no special case is met
    return makeBarChartOf(companies, "Recent Price Difference", getPriceDiff)

def volume_response(request):
    companies = request["companies"]
    areas = request["areas"]
    comparative = request["comparative"]
    time = request["time"]
    if comparative is not None:
        group = companies
        for i in areas:
            group = union(group,companiesInIndustry(i))
        if len(group) == 0:
            group = allCompanies()
        return higherLower(comparative, group, "volume", lambda x: x.getVolume(), lambda x: x)
    if len(companies) == 0:
        if len(areas) == 1:
            message = "Here's the most recent sumed volume of the " + areas[0] + " industry:"
            caption = Industry.objects.get(name = areas[0]).getVolume()
            return nl.turnIntoResponseWithCaption(message, caption)
        elif len(areas) == 0:
            #Response for no companies or industries being listed.
            return nl.turnIntoResponse("You'll need to tell me the names of the industries you want the volume of.")
    elif len(companies) == 1:
        message = "Here's " + nl.posessive(companies[0]) + " most recent volume:"
        caption = Company.objects.get(ticker = companies[0]).getVolume()
        return nl.turnIntoResponseWithCaption(message, caption)
    #If no special case is met
    return makeBarChartOf(companies, "Recent Volume", lambda x: x.getVolume(), print_format=lambda x: str(x))

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
        l.append(Company.objects.get(ticker=company).name + " (" + company + ")")
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
        return nl.turnIntoResponse("You'll need to specify which companies you'd like news about.")
    for company in companies:
        if "now" in time:
            news = Company.objects.get(ticker = company).getNews()
        else:
            news = Company.objects.get(ticker = company).getNewsFrom(time["start"], time["end"])
        for story in news:
            articles.append(story.toJson())
    if len(articles) == 0:
        if "now" in time:
            return nl.turnIntoResponse(
                    "I'm sorry, I couldn't find any news for " +  \
                    nl.makeOrList(companies) + \
                    " for this week. You can specify earlier articles in your query if you wish."
                )
        else:
            return nl.turnIntoResponse(
                    "I'm sorry, I couldn't find any news for " +  \
                    nl.makeOrList(companies) + \
                    " from " + nl.printDate(time["start"])
                )
    return nl.turnIntoNews(articles)

def makeBarChartOf(companies, qualName, funct, industries = [], print_format=lambda x: nl.printAsSterling(x)):
    data = []
    caption = []
    counter = len(companies)
    for company in companies:
        price = funct(Company.objects.get(ticker = company))
        data.append({"label":company, "data":[price]})
        caption.append(nl.posessive(company) + " at " + print_format(price))
    for industry in industries:
        price = funct(Industry.objects.get(name = industry))
        data.append({"label":industry, "data":[price]})
        caption.append(nl.posessive(industry) + " at " + print_format(price))
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
