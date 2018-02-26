$(document).ready(function() {
    $("#searchbox").keyup(function() {
        var query = $(this).val();
        if (query != "") {
            var data = {query: query};
            $.ajax({
                url: 'get_entities/',
                data: data,
                dataType: "json",
                method: "get"
            }).done(function (response) {
                console.log("success!");
                outputData(response);
            }).fail(function (response) {
                console.log("-----Fail-------");
                console.log(response);
            });
        }
    })
});