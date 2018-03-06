"""
    This is where the views for the chatbot page are defined
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

import datetime
import calendar
from random import randint

from chatbot.models import *
from chatbot.nl import nl
from chatbot.chart import Chart
from chatbot.response import *

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
    trader = request.user.traderprofile
    data = {
        "name": "FLORIN",
        "messages": []
    }
    requests = nl.getRequests(query)
    if requests == [] or requests == None:
        data["messages"].append(nl.genericUnknownResponse())
    else:
        for request in requests:
            # for each company that was requested, incremenet the hit count
            for ticker in request["companies"]:
                try:
                    hc = CompanyHitCount.objects.get(company__ticker=ticker, trader=trader)
                    hc.hit_count += 1
                    hc.save()
                except ObjectDoesNotExist:
                    CompanyHitCount.objects.create(
                        company=Company.objects.get(ticker=ticker),
                        trader=trader,
                        hit_count=1
                    )
            # for each industry that was requested, incremenet the hit count
            for name in request["areas"]:
                try:
                    hc = IndustryHitCount.objects.get(industry__name=name, trader=trader)
                    hc.hit_count += 1
                    hc.save()
                except ObjectDoesNotExist:
                    IndustryHitCount.objects.create(
                        industry=Industry.objects.get(name=name),
                        trader=trader,
                        hit_count=1
                    )
            if request["quality"] == "joke":
                data["messages"].append(nl.turnIntoResponse("Why did the chicken cross the road?"))
            try:
                data["messages"].append(respond_to_request(request))
            except Exception:
                data["messages"].append({
                    "name": "FLORIN",
                    "type": "text",
                    "body": "Sorry, something went wrong with your " + request["quality"] + "query",
                    "caption": ""
                })
    return JsonResponse(data)


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
            "price": "%.2f" % c.getSpotPrice(),
            "change": "%.2f" % c.getSpotPercentageDifference(),
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
            "price": "%.2f" % i.getSpotPrice(),
            "change": "%.2f" % i.getSpotPercentageDifference()
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

def capName(name):
    exceptions = ['for', 'and']
    split = name.split(" ")
    capitalised = ""
    for s in split:
        if s in exceptions:
            capitalised += s + " "
        else:
            capitalised += s[:1].upper() + s[1:] + " "
    return capitalised.strip()


@login_required
def get_price_drop_alerts(request):
    """
        Finds any companies that have a price percentage change
        of less than -10% and returns them.
    """
    trader = request.user.traderprofile
    response = {
        "price-drops": []
    }
    # find any big price drops
    perc_change = [(c, c.getSpotPercentageDifference()) for c in Company.objects.all()]
    for t in perc_change:
        # if the price has dropped by more than x%, then...
        if t[1] <= -10:
            hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
            results = Alert.objects.filter(trader=trader, company=t[0])
            # if the company has a time less than an hour ago, update the time and
            # add the company to the alerts list
            if len(results) == 0 or results[0].date < hour_ago:
                now = datetime.datetime.now()
                yesterday = now - datetime.timedelta(days=1)
                try:
                    recent_article = t[0].getNewsFrom(yesterday, now)
                except RuntimeError:
                    recent_article = []
                response["price-drops"].append({
                    "ticker": t[0].ticker,
                    "name": t[0].name,
                    "price": "%.2f" % t[0].getSpotPrice(),
                    "change": "%.2f" % t[1],
                    "article": recent_article[0].toJson() if len(recent_article) > 0 else {}
                })
            # if the alert row for this user and company doesn't exist create it
            # otherwise alter the current record
            if len(results) == 0:
                Alert.objects.create(trader=trader, company=t[0], date=datetime.datetime.now())
            else:
                results[0].date = datetime.datetime.now()
                results[0].save()

    return JsonResponse(response)


@login_required
def get_breaking_news(request):
    """
        Given an integer representing the number of
        seconds old a breaking news story has to be to be included
        in the response, find at most 5 breaking news stories from
        the user's favourite companies
    """
    trader = request.user.traderprofile
    check_interval = int(request.GET.get("check_interval"))
    response = {
        "name": "FLORIN",
        "breaking-news": {
            "type": "news",
            "heading": "Breaking News",
            "articles": []
        }
    }
    # get all companies the user has shown interest in
    entities_with_score = list(
        set().union(
            [(c.hit_count, c.company) for c in trader.companyhitcount_set.all()],
            [(i.hit_count, i.industry) for i in trader.industryhitcount_set.all()],
        )
    )
    # sort it so that the companies/industries with the highest hit count are first
    sorted(entities_with_score, key=lambda x: -x[0])
    # remove the score and just keep the entities
    entities = list(map(lambda x: x[1], entities_with_score))
    # add in the portfolio companies if their not in the most searched
    for c in trader.c_portfolio.all():
        if not c in entities:
            entities.insert(0, c)
    # TODO change this as just picking max 5 companies then getting breaking news
    # isn't the best way to do it
    i = 0
    while len(response["breaking-news"]) <= 5 and i < len(entities):
        e = entities[i]
        last_check = datetime.datetime.now() - datetime.timedelta(seconds=check_interval)
        for n in e.getNewsFrom(start=last_check, end=datetime.datetime.now(), breaking=True):
            if len(response["breaking-news"] == 5):
                break
            else:
                response["breaking-news"]["articles"].append({
                    "type": "news",
                    "url": n.url,
                    "title": n.headline,
                    "pic_url": n.image,
                    "description": n.date_published
                })
        i += 1

    return JsonResponse(response)


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
            "body": "You appear not to have shown interest in any companies " +
                    "or industries yet. Once you have, I can give you a brief " +
                    "summary on their performance since you last logged in",
            "caption": ""
        })
    else:
        # if there is a company or industry they are interested in, proceed with
        # with the briefing
        if len(c_hit_counts) > 0:
            briefing["messages"].append(company_briefing(c_hit_counts, 2))

        # get a briefing on favourite industries if the user has some
        if len(i_hit_counts) > 0:
            briefing["messages"].append(industry_briefing(i_hit_counts, 2))

        # get 3 articles from favourite companies and industries since last login
        briefing["messages"].append(news_briefing(c_hit_counts, i_hit_counts, time_since, 3))



    return JsonResponse(briefing)


def company_briefing(c_hit_counts, max_companies):
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
        c_msg +=    (capName(c.name) + " currently has a price of £" + str(c.getSpotPrice()) + " " +
                    "with a percentage change of " +
                    ("%.2f" % c.getSpotPercentageDifference()) +
                    "%. ")
    # for the most liked company out of the randomly chosen, get their spot history
    best_company = cs[0]
    c_msg += "The chart shows stock history of " + capName(best_company.name) + " for the last week."
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)
    chart = Chart()
    df = best_company.getStockHistory(last_week, now)
    chart.add_from_df(df=df, label=best_company.ticker +" - "+capName(best_company.name))
    return {
        "type": "chart",
        "description": c_msg,
        "chart_object": chart.toJson()
    }


def industry_briefing(i_hit_counts, max_industries):
    """
        Given a list of industry hit counts and a number of how many industies
        to include in the briefing, choose some industries based on the
        number of hitcounts they have, and return a message to be displayed
    """
    inds = get_from_weigted_probability([(i.industry, i.hit_count) for i in i_hit_counts], 2)
    price1 = inds[0].getSpotPrice()
    i_msg = ""
    i_msg +=    ("The " + capName(inds[0].name) + " industry has a current price of £" +
                str(price1) + " " +
                "with a percentage change of " +
                ("%.2f" % inds[0].getSpotPercentageDifference()) +
                "%. ")
    if 1 < len(inds):
        price2 = inds[1].getSpotPrice()
        i_msg +=    (capName(inds[1].name) +
                    (" is looking better " if price1 < price2 else "is behind ") +
                    "with a combined stock price of £" + str(price2) +
                    ", and has a change of " +
                    ("%.2f" % inds[1].getSpotPercentageDifference()) +
                    "%.")
    return {
        "type": "text",
        "body": i_msg,
        "caption": ""
    }


def news_briefing(c_hit_counts, i_hit_counts, time_since, max_count):
    """
        Given industry and company hit counts, choose max_count of
        companies/industries, and get one article from each from the
        given time 'time_since'
    """
    # unions two lists of tuples of type (entity, hitcount)
    favourite_hits = list(set().union(
        [(c.company, c.hit_count) for c in c_hit_counts],
        [(i.industry, i.hit_count) for i in i_hit_counts]
    ))
    # sort it by descending order of the second element in the tuple
    sorted(favourite_hits, key=lambda x: -x[1])
    best_entities = get_from_weigted_probability(favourite_hits, max_count)
    articles = []
    for e in best_entities:
        ns = e.getNewsFrom(time_since, datetime.datetime.now())
        if len(ns)> 0:
            articles.append(ns[0])
    # generate a message with the given articles
    msg = {}
    if len(articles) > 0:
        news_json = []
        for n in articles:
            news_json.append({
                "url": n.url,
                "title": n.headline,
                "pic_url": n.image,
                "description": n.get_str_date()
            })
        msg = {
            "type": "news",
            "articles": news_json
        }
    else:
        msg = {
            "type": "text",
            "body": "There hasn't been any major news since you last logged in."
        }
    return msg


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


