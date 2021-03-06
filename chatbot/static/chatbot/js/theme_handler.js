var themes = {
    Default: {
        '--header-bg-colour': "#17252A",
        '--header-fg-colour': "#FEFFFF",
        '--body-bg-colour': "#3AAfA9",
        '--body-fg-colour': "#DEF2F1",
        '--accent-colour': "#2B7A78",
        '--border-colour': "#000",
        '--canvas-colour': "#17252A",
        '--btn-colour': "#17252A"
    },
    Pink: {
        '--header-bg-colour': "#FFF",
        '--header-fg-colour': "#4A4A4A",
        '--body-bg-colour': "#CFC5DD",
        '--body-fg-colour': "#000",
        '--accent-colour': "#E0DFFF",
        '--border-colour': "#000",
        '--canvas-colour': "#444",
        '--btn-colour': "#FFF"
    },
    Light: {
        '--header-bg-colour': "#FFF",
        '--header-fg-colour': "#000",
        '--body-bg-colour': "#FFF",
        '--body-fg-colour': "#000",
        '--accent-colour': "#0C99C1",
        '--border-colour': "#000",
        '--canvas-colour': "#0f395E",
        '--btn-colour': "#44BBDD"
    },
    Lava: {
        '--header-bg-colour': "#000",
        '--header-fg-colour': "#FFF",
        '--body-bg-colour': "#222",
        '--body-fg-colour': "#FFF",
        '--accent-colour': "#C31",
        '--border-colour': "#C21",
        '--canvas-colour': "#555",
        '--btn-colour': "#C31"
    }
};

$(document).ready(function () {
    Chart.defaults.global.defaultFontColor = "#fff";
    for (name in themes) {
        var theme = themes[name];
        $("#themes").append(
            "<button id='"+name+"' class='dropdown-item theme-btn' type='button'>"
            +name
            +"</button>"
        );
    }

    $(".theme-btn").on('click', function () {
        var theme = $(this).attr("id");
        setTheme(theme);
    });

    var themeCookie = Cookies.get("theme");
    console.log(themeCookie);
    setTheme((themeCookie == null) ? "Default" : themeCookie);
});



function setTheme(themeName) {
    var theme = themes[themeName];
    for (varName in theme) {
        document.documentElement.style.setProperty(varName, theme[varName]);
    }
    Cookies.set("theme", themeName);
}