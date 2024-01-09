$(document).ready(function(){
const accountButton = document.getElementById("account");

var clickedElement = accountButton;

    while (clickedElement && clickedElement.tagName !== 'LI') {
        clickedElement = clickedElement.parentNode;
    }

    if (clickedElement) {
        clickedElement.classList.add("active");
    }
});

function calculateSettingAsThemeString({ localStorageTheme,systemSettingDark,}) {
      return "dark";
  }

  function updateThemeOnHtmlEl({ theme }) {
    document.querySelector("html").setAttribute("data-theme", theme);
  }