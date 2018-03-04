$(document).ready(function() {
    getBriefing(Math.round(Date.now() / 1000))
});

function getBriefing(since) {
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