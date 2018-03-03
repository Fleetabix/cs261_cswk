$(document).ready(function() {
    $("body").on("click", ".close-popup", function() {
        $(this).closest(".popup").remove();
    });
});

function popup(id, body) {
    var popupStr = 
        "<div id='"+id+"' class='popup'>" +
            "<div class='popup-header'>" +
                "<button class='close-popup'><i class='fas fa-times'></i></button>" +
            "</div>" +
            "<div class='popup-body'>" +
                body +
            "</div>" +
    "</div>";
    $("body").append(popupStr);
}