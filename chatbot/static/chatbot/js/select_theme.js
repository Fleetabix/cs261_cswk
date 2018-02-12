var theme1 = {
    'name': 'Default',
    '--header-bg-colour': "#17252A",
    '--header-fg-colour': "#FEFFFF",
    '--body-bg-colour': "#3AAfA9",
    '--body-fg-colour': "#DEF2F1",
    '--accent-colour': "#2B7A78"
}

var theme2 = {
    'name': 'Pink',
    '--header-bg-colour': "#FFF",
    '--header-fg-colour': "#4A4A4A",
    '--body-bg-colour': "#CFC5DD",
    '--body-fg-colour': "#000",
    '--accent-colour': "#E0DFFF",
}

var theme3 = {
    'name': 'Light',
    '--header-bg-colour': "#FFF",
    '--header-fg-colour': "#000",
    '--body-bg-colour': "#FFF",
    '--body-fg-colour': "#000",
    '--accent-colour': "#44DDFF",
}

$(document).ready(function () {
    var themeCookie = Cookies.get("theme");
    if (themeCookie == null) {
        Cookies.set("theme", "theme-1");
    } else {
        setTheme(themeCookie);
        console.log(themeCookie);
    }
});

$(".theme-btn").click(function () {
    var theme = $(this).attr("id");
    Cookies.set("theme", theme);
    setTheme(theme);
});

function setTheme(theme) {
    switch (theme) {
        case "theme-1":
            document.documentElement.style.setProperty('--header-bg-colour', "#17252A");
            document.documentElement.style.setProperty('--header-fg-colour', "#FEFFFF");
            document.documentElement.style.setProperty('--body-bg-colour', "#3AAfA9");
            document.documentElement.style.setProperty('--body-fg-colour', "#DEF2F1");
            document.documentElement.style.setProperty('--accent-colour', "#2B7A78");
            break;
        case "theme-2":
            document.documentElement.style.setProperty('--header-bg-colour', "#FFF");
            document.documentElement.style.setProperty('--header-fg-colour', "#4A4A4A");
            document.documentElement.style.setProperty('--body-bg-colour', "#CFC5DD");
            document.documentElement.style.setProperty('--body-fg-colour', "#000");
            document.documentElement.style.setProperty('--accent-colour', "#E0DFFF");
    }
}