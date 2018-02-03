$(document).ready(function() {
    $("#message-form").submit(function(e) {
        e.preventDefault();
        var $form = $(this);
        var data = {
            message: $form.find("input[name='message']").val()
        }
        //just a placeholder for now
        outputData(data);
    });
});

function outputData(data) {
    var messageBox = "<div class='message'>";
    messageBox += "<p>"+data.message+"</p>";
    messageBox += "</div>";
    $("#messages").append(messageBox);
    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    $("#message-txt").val("");
}