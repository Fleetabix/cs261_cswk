$(document).ready(function() {
    if(annyang) {
        // if the user's browser support voice recognition, 
        // add a mmicrophone button
        $("#message-form").append
            (
                "<button id='speech-btn' class='btn msg-form-btn'>"
                + "<i class='fas fa-microphone fa-lg'></i>"
                + "</button>"
            );

        var command = {
            'ok flooring *query': function(query) {
                outputQuery(query);
            }
        }
        annyang.addCommands(command);

        annyang.start({ autoRestart: false });
    }
});
