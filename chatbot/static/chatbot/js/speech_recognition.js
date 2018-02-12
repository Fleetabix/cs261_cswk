$(document).ready(function () {
    if (annyang) {
        var command = {
            '(ok) flooring *query': function (query) {
                askChatbot(query);
            }
        }
        annyang.addCommands(command);
        annyang.addCallback('soundstart', function () {
            console.log("adding speech box");
            var speechBox = "<div id='speech-box' class='message user-message'>";
            speechBox += "<br><p>";
            speechBox += " <i class='fas fa-circle' id='speech-dot-0'></i> ";
            speechBox += " <i class='fas fa-circle' id='speech-dot-1'></i> ";
            speechBox += " <i class='fas fa-circle' id='speech-dot-2'></i> ";
            speechBox += "</p>";
            speechBox += "</div>";
            $("#speech-box").remove();
            $("#messages").append(speechBox);
            $("#messages").scrollTop($("#messages").prop("scrollHeight"));
            animateDots();
        });
        annyang.addCallback('result', function () {
            console.log("removing speech box");
            $("#speech-box").remove();
        });

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

$("#speech-btn").click(function () {
    var microOn = Cookies.get("microphone");
    setListening(!(microOn == "true"));
    Cookies.set("microphone", (microOn == "true") ? false : true);
    console.log(Cookies.get("microphone"));
});

function setListening(on) {
    console.log("setting speech " + ((on) ? "on" : "off"));
    if (on) {
        $("#speech-btn").css("color", "red");
        annyang.start({ autoRestart: true, continuous: false });
        $("#message-txt").prop("placeholder", "Say (ok) FLORIN to start speech recognition");
    } else {
        $("#speech-btn").css("color", "var(--header-bg-colour");
        annyang.abort();
        $("#speech-box").remove();
        $("#message-txt").prop("placeholder", "Hi there, what would you like to know?");
    }
}

function animateDots() {
    if (animateDots.dot == undefined) {
        animateDots.dot = 0;
    }
    $("#speech-dot-" + animateDots.dot).css("color", "var(--header-bg-colour");
    $("#speech-dot-" + ((animateDots.dot + 2) % 3)).css("color", "var(--body-fg-colour");
    animateDots.dot = (animateDots.dot + 1) % 3;
    if ($("#speech-box").length) {
        setTimeout(animateDots, 500);
    }
}