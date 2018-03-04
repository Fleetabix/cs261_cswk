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
});

function getBriefing(since) {
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
    }).done(function (response) {
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