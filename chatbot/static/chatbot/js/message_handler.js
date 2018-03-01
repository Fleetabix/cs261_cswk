$(document).ready(function () {
    $("#javascript-warning").hide()
    $("#message-form").submit(function (e) {
        e.preventDefault();
        var $form = $(this);
        askChatbot($form.find("input[name='query']").val());
    });
});

/** Sends a query to the server and prints the response.
 * @param {string} query what you want to ask FLORIN
 */
function askChatbot(query) {
    var data = {
        query: query
    }
    //make sure the message isn't empty
    if (data.query != "") {
        outputQuery(data.query);
        $.ajax({
            url: 'ask_chatbot/',
            data: data,
            dataType: "json",
            method: "post"
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
}

/** Calls outputMessage but after waiting a set amount of time.
 *  Used so that name and message data are stored and not overwritten
 * @param {string} name the name of the user that is sending it
 * @param {object} message the data that the message contains
 * @param {integer} delay  the amount of milliseconds to delay the output
 */
function outputResponse(name, message, delay) {
    setTimeout(function() {
        outputMessage(name, message)
    }, delay);
}

/** Outputs a message in certain styles defined by the message.
 *  Usually used to print the bot's response
 * @param {*} name the name of the sender
 * @param {*} message the message content
 */
function outputMessage(name, message) {
    var chartId;
    var messageBox = "<div class='message-holder row'>";
    messageBox += "<div class='florin-message message col-10'>";
    messageBox += "<h3>" + name + "</h3>";
    switch (message.type) {
        case "text":
            if (message.body)
                messageBox += "<p>" + message.body + "</p>";
            if (data.caption)
                messageBox += "<h4>" + message.caption + "</h4>";
            break;
        case "chart":
            chartId = getNextChartID();
            messageBox += "<div class='row'>";
            messageBox += "<div class='col-md-7 chart-holder'>";
            messageBox += "<canvas id='" + chartId + "'></canvas>";
            messageBox += "</div>";
            messageBox += "<div class='col-md-5'>";
            messageBox += "<p>" + message.description + "</p>";
            messageBox += "</div>";
            messageBox += "</div>";
            break;
        case "news":
            for (articleKey in message.articles) {
                var article = message.articles[articleKey];
                messageBox += "<div class='row news-holder'>";
                messageBox += "<div class='col-12'>";
                messageBox += "<a href='" + article.url + "' target='_blank'><h4>" + article.title + "</h4></a>";
                messageBox += "</div>";
                messageBox += "<div class='col-sm-3 news-img-holder'>";
                messageBox += "<a href='" + article.url + "' target='_blank'>";
                messageBox += "<img class='news-img' src='" + article.pic_url + "'></img>";
                messageBox += "</a>";
                messageBox += "</div>";
                messageBox += "<div class='col-sm-9 news-desc'>";
                messageBox += "<p>" + article.description + "</p>";
                messageBox += "</div>";
                messageBox += "</div>";
            }
            break;
        default:
            messageBox += "<h4>Response type not found</h4>"
    }
    messageBox += "</div>";
    messageBox += "</div>";
    $("#messages").append(messageBox);
    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    $("#message-txt").val("");

    if (message.type == "chart") {
        createChart(chartId, message.chart_object);
    }
}

/*
    has a static variable which is incremented each time a chart is added
*/
function getNextChartID() {
    if (typeof getNextChartID.id == 'undefined') {
        getNextChartID.id = 0;
    }
    return getNextChartID.id++;
}

/*
    Creates a chart given the chart object and the chart id
*/
function createChart(chartId, chartObject) {
    var ctx = document.getElementById(chartId).getContext('2d');
    var dataSets = chartObject.data.datasets;
    for (key in dataSets) {
        var dataset = dataSets[key];
        var colour = getRandomColor();
        //add the following properties to the dataset
        dataset["backgroundColor"] = colour;
        dataset["borderColor"] = colour;
        dataset["fill"] = "none";
    }
    new Chart(ctx, chartObject);
}

/* 
    Generates a random colour (can't do black though, black is yucky)
*/
function getRandomColor() {
    var letters = '68ACE';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * letters.length)];
    }
    return color;
}

function outputQuery(query) {
    var messageBox = 
        "<div class='message-holder row justify-content-end'>" +
            "<div class='message user-message col-10'>" +
                "<h3>"+username+"</h3>" +
                "<p>"+query+"</p>" +
            "</div>" +
        "</div>";
    $("#messages").append(messageBox);
    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    $("#message-txt").val("");
}