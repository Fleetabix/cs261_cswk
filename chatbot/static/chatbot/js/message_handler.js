$(document).ready(function () {
    $("#message-form").submit(function (e) {
        e.preventDefault();
        var $form = $(this);
        var data = {
            query: $form.find("input[name='query']").val()
        }
        outputData({ name: "USER", type: "text", body: data.query });
        $.ajax({
            url: 'ask_chatbot/',
            data: data,
            dataType: "json",
            method: "post"
        }).done(function (response) {
            outputData(response);
        }).fail(function (response) {
            console.log("-----Fail-------");
            console.log(response);
        });
    });
});

function outputData(data) {
    var chartId;
    var messageBox = "<div class='message'>";
    messageBox += "<h3>" + data.name + "</h3>";
    switch (data.type) {
        case "text":
            if (data.body)
                messageBox += "<p>" + data.body + "</p>";
            if (data.caption)
                messageBox += "<caption>" + data.caption + "</caption>";
            break;
        case "chart":
            chartId = getNextChartID();
            messageBox += "<div class='row'>";
            messageBox += "<div class='col-md-7 chart-holder'>";
            messageBox += "<canvas id='" + chartId + "'></canvas>";
            messageBox += "</div>";
            messageBox += "<div class='col-md-5'>";
            messageBox += "<p>" + data.description + "</p>";
            messageBox += "</div>";
            messageBox += "</div>";
            break;
        case "news":
            for (articleKey in data.articles) {
                var article = data.articles[articleKey];
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
    $("#messages").append(messageBox);
    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    $("#message-txt").val("");

    if (data.type == "chart") {
        createChart(chartId, data.chart_object);
    }
}

function getNextChartID() {
    if (typeof getNextChartID.id == 'undefined') {
        getNextChartID.id = 0;
    }
    return getNextChartID.id++;
}

function createChart(chartId, chartObject) {
    var ctx = document.getElementById(chartId).getContext('2d');
    var dataSets = chartObject.data.datasets;
    for (key in dataSets) {
        var dataset = dataSets[key];
        var colour = getRandomColor();
        dataset["backgroundColor"] = colour;
        dataset["borderColor"] = colour;
        dataset["fill"] = "none";
    }
    new Chart(ctx, chartObject);
}

function getRandomColor() {
    var letters = '3456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 13)];
    }
    return color;
  }