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
        getBriefing(lastOnline);
    }

    // every checkInterval seconds, look for big price drops or
    // any breaking news
    var checkInterval = 60 * second;
    setInterval(function() {
        getAlerts(checkInterval);
    }, checkInterval);
});

function getBriefing(since) {
    console.log("getting briefing");
    outputResponse("FLORIN", {
        type: "text",
        body: "Welcome back! Here is your up to date briefing...",
        caption: ""
    }, 500);
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
        var delay = 800;
        for (i in response["messages"]) {
            var message = response["messages"][i];
            outputResponse(name, message, delay * i);
        }
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
    });
}

/** Gets any alerts the user might want to know that have popped up since
 *  the last time this function was called
 * @param {integer} checkInterval the number of seconds since the last check
 */
function getAlerts(checkInterval) {
    console.log("getting alerts");
    var data = {
        check_interval: checkInterval
    }
    $.ajax({
        url: 'get_alerts/',
        data: data,
        dataType: "json",
        method: "get"
    }).done(function(response) {
        var name = response["name"];
        for (key in response["price-drops"]) {
            drop = response["price-drops"][key];
            popup(
                "<h1>Price Drop Alert</h1>" +
                "<h2>"+drop.ticker+" - "+drop.name+"</h2>" +
                "<p>"+drop.name+" has had a price drop of</p>" +
                "<h3>"+drop.change+"%</h3>" +
                "<p>leaving it with a price of " +
                "£"+drop.price+"</p>"
            );
        }
        /*
        var delay = 800;
        for (i in response["messages"]) {
            var message = response["messages"][i];
            outputResponse(name, message, delay * i);
        }
        */
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
    });
}