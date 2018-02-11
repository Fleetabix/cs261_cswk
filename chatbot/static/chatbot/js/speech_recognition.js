$(document).ready(function() {
    if(annyang) {
        var command = {
            '(ok) (hey) flooring *query': function(query) {
                outputQuery(query);
            }
        }
        annyang.addCommands(command);

        //get the user's preferences about having the microphone on
        var microOn = Cookies.get("microphone");
        if (microOn == undefined) {
            Cookies.set("microphone", "false");
        } else {
            if (microOn == "true") {
                setListening(true);
            }
        }
    } else {
        //if the browser does not support speech recognition
        //turn it off
        $("#speech-btn").css("display", "none");
    }
});

$("#speech-btn").click(function() {
    var microOn = Cookies.get("microphone");
    setListening(!(microOn == "true"));
    Cookies.set("microphone", (microOn == "true") ? false : true);
    console.log(Cookies.get("microphone"));
});

function setListening(on) {
    console.log("setting speech " + ((on) ? "on" : "off"));
    if (on) {
        $("#speech-btn").css("color", "red");
        annyang.start();
    } else {
        $("#speech-btn").css("color", "var(--header-bg-colour");
        annyang.abort();
    }
}
