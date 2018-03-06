// Add the trim function to all strings
if(typeof(String.prototype.trim) === "undefined") {
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}


$(document).ready(function() {
    getPortfolio(true, outputPortfolio);

    // when the user types in a new character update the
    // search
    $("#searchbox").keyup(function() {
        var query = $(this).val();
        // make sure that there's something to look for
        if (query.trim() != "") {
            $("#clear-search-btn").find($("svg"))
                .removeClass("fa-sync")
                .addClass("fa-times");
            getSearchResults($("#query-type").val(), query);
        } else {
            $("#search-results").css("display", "none");
            $("#portfolios").css("display", "block");
            $("#clear-search-btn").find($("svg"))
                .removeClass("fa-times")
                .addClass("fa-sync");
            getPortfolio(true, outputPortfolio);
        }
    });

    //if the clear button is pressed, clear the search results and
    // search box
    $("#clear-search-btn").click(function() {
        getPortfolio(true, outputPortfolio);
        $("#clear-search-btn").find($("svg"))
            .removeClass("fa-times")
            .addClass("fa-sync");
        $("#search-results").empty();
        $("#search-results").css("display", "none");
        $("#portfolios").css("display", "block");
        $("#searchbox").val("");
    });

    // when a button signifying a user wants to add a company to a portfolio
    // is pressed do the following
    $("body").on('click', '.add-portfolio-btn', function() {
        var result = $(this).closest(".result");
        var id = result.attr("data-id");
        var type = result.attr("data-type");
        addToPortfolio(id, type, result);
    });

    // when a cross in a portfolio-item is clicked, remove that
    // company/industry from the portfolio
    $("body").on('click', '.rm-from-portfolio', function() {
        var item = $(this).closest(".portfolio-item");
        var data = {
            type: item.attr("data-type"),
            id: item.attr("data-id")
        };
        $.ajax({
            url: "remove_from_portfolio/",
            data: data,
            dataType: "json",
            method: "post"
        }).done(function(data) {
            item.remove();
        }).fail(function(data) {
            alert("Sorry, something went wrong");
            console.log("----FAIL----");
            console.log(data);
        });
    });

    //every 15 seconds, get updated prices and percentage changes for the
    //portfolio
    setInterval(function() {
        getPortfolio(false, updatePortfolio);
    }, 15 * 1000);
});


/** Sends a get request to the server to find entities that have similar
 *  aliases as the query. 
 * @param {string} type the type of entity to look for
 * @param {string} query the string that the alias should be similar to
 */
function getSearchResults(type, query) {
    $("#search-results").css("display", "block");
    $("#portfolios").css("display", "none");
    var data = {
        type: type,
        query: query
    };
    $.ajax({
        url: 'get_entities/',
        data: data,
        dataType: "json",
        method: "get"
    }).done(function (response) {
        // if there was a result, print it. otherwise say sorry.
        $("#search-results").empty();
        if (Object.keys(response.data).length > 0) {
            printSearchResults(response);
        } else {
            $("#search-results").append(
                "<div class='result row'>" +
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
}

/** Adds the selected entity to the user's portfolio.
 *  Done via an ajax call and when completed, turns the selected result green.
 * @param {string} key the primary key for the entity we want to add to our portfolio
 * @param {string} type the type of entity we want to add to our portfolio
 * @param {jquery object} result the jquery object representing the search result
 */
function addToPortfolio(id, type, result) {
    var data = {
        type: type,
        id: id 
    };
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

/** Prints results from searching for companies or industries.
 *  Adds all results to the search-results div.
 * @param {javascript object} results An object containing the type of entities returned
 * with a key, and related information for each one.
 */
function printSearchResults(results) {
    var resultsString = "";
    var data = results.data;
    for (id in data) {
        var info = data[id];
        resultsString += 
            "<div class='result row' data-type='"+results.type+"' data-id='"+id+"'>" +
                "<div class='col-md-9'>" +
                    "<h5>" +
                    ((results.type == "industry") ? "" : (info.ticker + " - ")) +
                    info["name"]+
                    "</h5>" +
                "</div>" +
                "<div class='col-md-3 add-comp-coll'>" +
                    "<button class='add-portfolio-btn btn'>" +
                        "<i class='fas fa-plus'></i>" +
                    "</button>" + 
                "</div>" +
            "</div>";
    }
    $("#search-results").append(resultsString);
}

/** Gets all the companies and industries in the user's portfolio
 *  and then adds them to the portfolio div.
 *  @param {boolen} historical whether to get historical data or not 
 *  @param {function} doSomething a function that uses the portfolio data
 */
function getPortfolio(historical, doSomething) {
    console.log("getting portfolios");
    data = {"historical": historical};
    $.ajax({
        url: 'get_portfolio/',
        data: data,
        dataType: "json",
        method: "get"
    }).done(function (response) {
        doSomething(response);
    }).fail(function (response) {
        console.log("-----Fail-------");
        console.log(response);
    });
}

/** Given an object that contains data of the companies and
 *  industries in the portfolio, output it to the portfolio
 *  tab.
 *  @param {portfolio object} portfolio 
 */
function outputPortfolio(portfolio) {
    $("#portfolios").empty();
    for (id in portfolio) {
        // add portfolio items here
        e = portfolio[id];
        $("#portfolios").append(
            "<div id='"+e.type+id+"' class='portfolio-item' data-type='"+e.type+"' data-id='"+id+"'>" +
                "<div class='row'>" + 
                    "<div class='col-9'>" +
                        "<h5>" + 
                            ((e.type == "industry") ? "" : e.ticker + " ") +
                            fstUp(e.name) +
                            " - £<span class='port-price'>" +
                            e.price + 
                            "</span> (<span class='port-change'>" +
                            e.change + "</span>%)" +
                        "</h5>" +
                    "</div>" +
                    "<div class='col-3 rm-prt'>" +
                        "<button class='btn rm-from-portfolio'>" +
                            "<i class='fas fa-times'></i>" +
                        "</button>" +
                    "</div>" +
                "</div>" +
                "<canvas id='" + e.type+id + "chart'></canvas>" +
            "</div>"
        );
        createChart(e.type+id+"chart", e.historical);
    }
}

function updatePortfolio(portfolio) {
    for (id in portfolio) {
        var e = portfolio[id];
        if ($("#"+e.type+id).length)  {
            $("#"+e.type+id).find(".port-price").text(e.price);
            $("#"+e.type+id).find(".port-change").text(e.change);
        }
    }
}

/** Returns the string but with the first character in upper case.
 *  Doesn't check for anything.
 *  @param {string} str 
 */
function fstUp(str) {
    return str.charAt(0).toUpperCase() + str.substring(1, str.length);
}