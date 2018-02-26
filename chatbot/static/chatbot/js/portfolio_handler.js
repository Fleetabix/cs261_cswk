// Add the trim function to all strings
if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

$(document).ready(function() {
    $("#searchbox").keyup(function() {
        sendQuery($(this).val());
    });
    $("body").on('click', '.add-portfolio-btn', function() {
        var result = $(this).closest(".result");
        var ticker = result.attr("data-comp-ticker");
        addToPortfolio(ticker, result);
    });
});

function sendQuery(query) {
    $("#search-results").empty();
    if (query.trim() != "") {
        $("#search-results").css("display", "block");
        var data = {query: query};
        $.ajax({
            url: 'get_entities/',
            data: data,
            dataType: "json",
            method: "get"
        }).done(function (response) {
            // if there was a result, print it. otherwise say sorry.
            if (Object.keys(response).length > 0) {
                printSearchResults(response);
            } else {
                $("#search-results").append(
                    "<div class='result row' data_comp_ticker='"+ticker+"'>" +
                        "<div class='col-md-12'>" +
                            "<h5>Sorry - No results found</h5>" +
                        "</div>" +
                    "</div>"
                );
            }
        }).fail(function (response) {
            console.log("-----Fail-------");
            console.log(response);
        });
    } else {
        $("#search-results").css("display", "none");
    }
}

function addToPortfolio(ticker, result) {
    var data = {ticker: ticker};
    $.ajax({
        url: 'add_to_portfolio/',
        data: data,
        dataType: "json",
        method: "post"
    }).done(function (response) {
        result.css("background-color", "green");
        result.find("button").remove();
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
        result.css("background-color", "red");
    });
}

function printSearchResults(results) {
    for (ticker in results) {
        comp_info = results[ticker]
        $("#search-results").append(
            "<div class='result row' data-comp-ticker='"+ticker+"'>" +
                "<div class='col-md-9'>" +
                    "<h5>"+ticker+" - "+comp_info["name"]+"</h5>" +
                "</div>" +
                "<div class='col-md-3 add-comp-coll'>" +
                    "<button class='add-portfolio-btn btn'>" +
                        "<i class='fas fa-plus'></i>" +
                    "</button>" + 
                "</div>" +
            "</div>"
        );
    }
}