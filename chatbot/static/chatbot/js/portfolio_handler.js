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
        var query = $(this).val();
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
                console.log("success!");
                printSearchResults(response);
            }).fail(function (response) {
                console.log("-----Fail-------");
                console.log(response);
            });
        } else {
            $("#search-results").css("display", "none");
        }
    })
});

function printSearchResults(results) {
    for (ticker in results) {
        comp_info = results[ticker]
        $("#search-results").append(
            "<div class='result row' data_comp_ticker='"+ticker+"'>" +
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