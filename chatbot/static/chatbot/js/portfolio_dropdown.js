$(document).ready(function () {
    // if the background attribute of the html tag is black, then its being
    // viewed on a desktop
    var mobile = ($('html').css("background-color") == "rgb(0, 0, 0)") ? false : true;
    var open_chevron = "", close_chevron = "";

    // assign the correct type of chevrons depending on the device
    // (side to side on desktop, up and down on mobile)
    if (mobile) {
        open_chevron = "fa-chevron-down";
        close_chevron = "fa-chevron-up"
    } else {
        open_chevron = "fa-chevron-right";
        close_chevron = "fa-chevron-left"
    }

    // if the device is mobile, the tab is closed by default
    var open = !mobile;
    var nextWidth = "100%";
    var fastSpeed = 600, slowSpeed = 800;
    // the function that opens or closes the portfolio tab when 
    // the portfolio-btn is clicked (also handles the change of
    // the button symbol)
    $(".portfolio-btn").click(function () {
        if (mobile) {
            $("#portfolio-tab").animate({height: "toggle"}, fastSpeed);
        } else {
            if (open) {
                $("#portfolio-tab").animate({width: "toggle"}, fastSpeed);
                $("#message-board").animate({width: nextWidth}, slowSpeed);
                toggleButton(mobile, close_chevron, open_chevron);
            } else {
                $("#message-board").animate({width: nextWidth}, fastSpeed);
                $("#portfolio-tab")
                    .delay(100)
                    .animate({width: "toggle"}, slowSpeed);
                toggleButton(mobile, open_chevron, close_chevron);
            }
        }
        // change the button icon
        // toggle properties for next click
        nextWidth = (nextWidth == "100%") ? "65%" : "100%";
        open = (open) ? false : true;
    });

    //makes the chevron grey when being clicked
    $("#portfolio-btn").mousedown(function () {
        $(this).css("color", "grey");
    });

    //reverts the chevron to the right colour after being clicked
    $("#portfolio-btn").mouseup(function () {
        $(this).css("color", "var(--header-fg-colour)");
    });
})

// switched the button icon given the viewing mode, the type of 
// chevron the button is now and the type you want it to be.
function toggleButton(mobile, class_to_remove, class_to_add) {
    var device = (mobile) ? "mobile" : "desktop";
    $("#"+device+"-portfolio-btn").find($("svg"))
        .removeClass(class_to_remove)
        .addClass(class_to_add);
}