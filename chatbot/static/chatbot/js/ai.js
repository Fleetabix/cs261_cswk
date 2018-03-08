$(document).ready(function() {
    var second = 1000;
    var interval = 60 * second;
    setTimeout(function() {
        // wait for 60 seconds before updating the cookie
        setInterval(function() {
            //every 60 seconds, update the cookie that says when they we're last logged in
            Cookies.set("last-online", Math.round(Date.now() / 1000));
            console.log(Cookies.get("last-online"));
        }, interval);
    }, interval);

    //look for a get parameter to force the daily briefing to be true
    var url = new URL(window.location.href);
    var forceBriefing = url.searchParams.get("force-briefing");

    // get the time they were last logged in, and if it was more than minInterval
    // then ask for a briefing
    var lastOnline = Cookies.get("last-online");
    //set minimum interval to ask for a briefing to 10 minutes
    var minInterval = 10*60;
    if (
            forceBriefing == "true" ||
            lastOnline != undefined &&
            minInterval <= Math.round(Date.now() / 1000) - lastOnline
        ) {
        if (forceBriefing == "true") {
            getBriefing((lastOnline == undefined) ? 0 : lastOnline - 3 * 24 * 60 * 60);
        } else {
            getBriefing((lastOnline == undefined) ? 0 : lastOnline);
        }
    }

    // every checkInterval seconds, look for big price drops or
    // any breaking news
    var newsCheckInterval = 15 * 60 * second;
    setInterval(function() {
        getBreakingNews(newsCheckInterval);
    }, newsCheckInterval);

    //check for stock price drops every dropCheckInterval seconds
    var dropCheckInterval = 30 * second;
    setInterval(function() {
        getPriceDropAlerts();
    }, dropCheckInterval);
});

/** Gets a briefing of the user's favourite company.
 *  Outputs the results as messages from florin.
 * @param {integer} since the number of seconds since the user was last online 
 */
function getBriefing(since) {
    console.log("getting briefing");
    outputResponse("FLORIN", {
        type: "text",
        body: "Welcome back! Here is your up to date briefing...",
        caption: ""
    }, 300);
    var data = {
        last_login: since
    }
    $.ajax({
        url: 'get_welcome_briefing/',
        data: data,
        dataType: "json",
        method: "get"
    }).done(function(response) {
        var name = response["name"];
        var delay = 400;
        for (i in response["messages"]) {
            var message = response["messages"][i];
            outputResponse(name, message, delay * (i + 1));
        }
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
    });
}

/** Finds and ouptuts any companies that have a percentage difference of less
 *  than 10%.
*/
function getPriceDropAlerts() {
    console.log("getting price drops");
    $.ajax({
        url: 'get_price_drop_alerts/',
        method: "get"
    }).done(function(response) {
        console.log(response);
        var name = response["name"];
        for (key in response["price-drops"]) {
            drop = response["price-drops"][key];
            // popup for news article
            if (Object.keys(drop["article"]).length > 0) {
                var a = drop["article"];
                popup(
                    "<a href='"+a.url+"'><h3>"+a.title+"</h3></a>" +
                    "<div style='margin-top: 10px' class='row'>" +
                        "<div class='col-sm-4'><img style='max-width: 100%; margin-bottom: 20px;' src='"+a.pic_url+"'></div>" +
                        "<div class='col-sm-8' style='text-align: left'>" +
                            "<h4>"+a.date+"</h4>" + 
                            "<p>"+a.description+"</p>" +
                        "</div>" +
                    "</div>"
                );
            }
            // popup for price drop
            popup(
                "<h1>Price Drop Alert</h1>" +
                "<h2>"+drop.ticker+" - "+drop.name+"</h2>" +
                "<p>"+drop.name+" has had a price drop of</p>" +
                "<h3>"+drop.change+"%</h3>" +
                "<p>leaving it with a price of " +
                "£"+drop.price+"</p>"
            );
        }
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
    });
}

/** Gets any breaking news that have popped up since
 *  the last time this function was called
 * @param {integer} checkInterval the number of seconds since the last check
 */
function getBreakingNews(checkInterval) {
    console.log("getting breaking news");
    var data = {
        check_interval: checkInterval
    }
    $.ajax({
        url: 'get_breaking_news/',
        data: data,
        dataType: "json",
        method: "get"
    }).done(function(response) {
        console.log(response);
        var message = response["breaking-news"];
        if (message.articles.length > 0) {
            outputResponse(response["name"], message, 1000);
        }
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
    });
}