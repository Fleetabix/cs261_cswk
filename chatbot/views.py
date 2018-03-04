"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import datetime
import calendar
from random import randint

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


@login_required
def get_alerts(request):
    """
        Finds the following alert worthy information and returns it
        back to the user.
        - Drops in stock price
        - Breaking news in portfolio
        //TODO  not sure how to mark off a breaking news story as read so it doesn't
                appear all the time 
                Also not sure how to mark of a price drop so it doesn't keep appearing
    """
    user = request.user
    response = []
    perc_change = [(c, c.getSpotPercentageDifference()) for c in Company.objects.all()]
    for t in perc_change:
        if t[1] <= -10:
            response.append({
                "type": "price_drop",
                "msg": {
                    "ticker": t[0].ticker,
                    "name": t[0].name,
                    "price": t[0].getSpotPrice(),
                    "change": t[1]
                }
            })
    return JsonResponse(respond_to_request)


@login_required
def get_welcome_briefing(request):
    """
        Given a time sice the user's last login, this will look at the user's
        favourite companies and industries and give them information they
        might find useful and news since they were last logged in.
    """
    time_stamp = int(request.GET.get("last_login"))
    time_since = datetime.datetime.fromtimestamp(time_stamp)
    user = request.user
    briefing = {
        "name": "FLORIN",
        "messages": []
    }
    # get some news from user's favourite companies/industry and print of some
    # stock prices
    c_hit_counts = user.traderprofile.companyhitcount_set.order_by("-hit_count")
    i_hit_counts = user.traderprofile.industryhitcount_set.order_by("-hit_count")
    if len(c_hit_counts) == 0 and len(i_hit_counts) == 0:
        briefing["messages"].append({
            "type": "text",
            "body": "You appear not to have show interest in any companies " +
                    "or industries yet. Once you have, I can give you a brief " +
                    "summary on they're performance since you last logged in",
            "caption": ""
        })
    else:
        briefing["messages"].append({
            "type": "text",
            "body": "Welcome back! Here's your up to date briefing:",
            "caption": ""
        })

        if len(c_hit_counts) > 0:
            briefing["messages"].append(companyBriefing(c_hit_counts, 2))

        # get a briefing on favourite industries if the user has some
        if len(i_hit_counts) > 0:
            inds = get_from_weigted_probability([(i.industry, i.hit_count) for i in i_hit_counts], 2)
            price1 = inds[0].getSpotPrice()
            i_msg = ""
            i_msg +=    ("The " + inds[0].name + " industry has a current price of £" + 
                        str(price1) + " " +
                        "with a percentage change of " + 
                        ("%.2f" % inds[0].getSpotPercentageDifference()) +
                        "%. ")
            if 1 < len(inds):
                price2 = inds[1].getSpotPrice()
                i_msg +=    (inds[1].name + 
                            (" is looking better " if price1 < price2 else "is behind ") +
                            "with a combined stock price of £" + str(price2) +
                            ", and has a change of " + 
                            ("%.2f" % inds[1].getSpotPercentageDifference()) + 
                            "%.")
            briefing["messages"].append({
                "type": "text",
                "body": i_msg,
                "caption": ""
            })

        # get 3 articles from favourite companies and industries since last login
        favourite_hits = list(set().union(
            [(c.company, c.hit_count) for c in c_hit_counts],
            [(i.industry, i.hit_count) for i in i_hit_counts]
        ))
        sorted(favourite_hits, key=lambda x: -x[1])
        best_entities = get_from_weigted_probability(favourite_hits, 3)
        articles = []
        for e in best_entities:
            ns = e.getNewsFrom(time_since, datetime.datetime.now())
            if len(ns)> 0:
                articles.append(ns[0])

        if len(articles) > 0:
            news_json = []
            for n in articles:
                news_json.append({
                    "url": n.url,
                    "title": n.headline,
                    "pic_url": n.image,
                    "description": n.get_str_date()
                })
            briefing["messages"].append({
                "type": "news",
                "articles": news_json
            })
        else:
            briefing["messages"].append({
                "type": "text",
                "body": "There hasn't been any major news since you last logged in."
            })

    return JsonResponse(briefing)

def companyBriefing(c_hit_counts, max_companies):
    """
        Given the user's company hit counts, get a maximum of max_companies
        companies, and return a message to display to the user. Assumes
        the size of c_hit_counts is greater than 0
    """
    # returns a max of two companies with a probability proportional to their hit count
    # over the total hit counts for the user
    cs = get_from_weigted_probability(
            [(c.company, c.hit_count) for c in c_hit_counts], 
            max_companies
        )
    c_msg = ""
    for c in cs:
        c_msg +=    (c.name + " currently has a price of £" + str(c.getSpotPrice()) + " " +
                    "with a percentage change of " + 
                    ("%.2f" % c.getSpotPercentageDifference()) + 
                    "%. ")
    # for the most liked company out of the randomly chosen, get their spot history
    best_company = cs[0]
    c_msg += "The chart shows stock history of " + best_company.name + " for the last week."
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)
    chart = Chart()
    df = best_company.getStockHistory(last_week, now)
    chart.add_from_df(df=df, label=best_company.ticker +" - "+best_company.name)
    return {
        "type": "chart",
        "description": c_msg,
        "chart_object": chart.toJson()
    }



def get_from_weigted_probability(ls, max):
    """
        Takes in a sorted list of tuples (object, score) and returns a maximum of
        max items such that the probabilty of picking them is proportional
        to the score of the object over the total score of the list
    """
    rtn_ls = []
    for i in range(max):
        total_score = sum(map(lambda x: x[1], ls))
        rnd = randint(0, total_score)
        for j in range(len(ls)):
            rnd -= ls[j][1]
            # if the random number gets below zero, pop the current item 
            # from the list and append it to the return list
            if rnd <= 0:
                rtn_ls.append(ls.pop(j))
                break
    # return a list of the first item in the tuples, sorted in descending order by the
    # second item in the tuple
    return list(map(lambda x: x[0], sorted(rtn_ls, key=lambda x: -x[1])))


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
        if len(request["companies"]) == 0:
            return nl.turnIntoResponse("To get to the other side.")
        elif len(request["companies"])>1:
            return nl.turnIntoResponse("To buy stock in " + nl.makeList(request["companies"]) + ".")
        else:
            return nl.turnIntoResponse("To buy stock in " + request["companies"][0] + ".")
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
        df  = Company.objects.get(ticker = company).getStockHistory(start, end)
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
            #for each data frame, alter the chart by adding the new valus
            if len(dfs) > 0:
                chart = Chart()
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