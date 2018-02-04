$(document).ready(function() {
    $("#message-form").submit(function(e) {
        e.preventDefault();
        var $form = $(this);
        var data = {
            query: $form.find("input[name='query']").val()
        }
        outputData({response: data.query});
        $.ajax({
            url: 'ask_chatbot/',
            data: data,
            dataType: "json",
            method: "post"
        }).done(function(response) {
            outputData(response);
        }).fail(function(response) {
            console.log("-----Fail-------");
            console.log(response);
        });
    });
});

function outputData(data) {
    var messageBox = "<div class='message'>";
    messageBox += "<p>"+data.response+"</p>";
    messageBox += "</div>";
    $("#messages").append(messageBox);
    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    $("#message-txt").val("");
}