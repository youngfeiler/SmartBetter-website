/**
 * Utility function to calculate the current theme setting.
 * Look for a local storage value.
 * Fall back to system setting.
 * Fall back to light mode.
 */
function calculateSettingAsThemeString({
  localStorageTheme,
  systemSettingDark,
}) {
  if (localStorageTheme !== null) {
    return localStorageTheme;
  }

  if (systemSettingDark.matches) {
    return "dark";
  }

  return "light";
}

/**
 * Utility function to update the button text and aria-label.
 */
function updateButton({ buttonEl, isDark }) {
  const lightIcon = `<i class="fa-solid fa-sun"></i>`;
  const darkIcon = `<i class="fa-solid fa-moon"></i>`;

  const newCta = isDark ? lightIcon : darkIcon;

  buttonEl.innerHTML = newCta;
}

/**
 * Utility function to update the theme setting on the html tag
 */
function updateThemeOnHtmlEl({ theme }) {
  document.querySelector("html").setAttribute("data-theme", theme);
}

function updateTable(data) {
  console.log(window.location.pathname);
  console.log(data);
  const footer_to_append_to = document.querySelector('.table-custom__footer');
  const footer_to_change_innerhtml= document.querySelector('.footer-to-make-innerhtml');
  footer_to_change_innerhtml.innerHTML = `<p>Showing ${data.length} Entries</p>`;


  const tableBody = document.querySelector('.table-custom__content');
  const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
  table_row_to_append_to.innerHTML = '';

  const tr = document.createElement('ul');

  boolin = true;
  if (!(data.length === 1 && data[0].update === false) && boolin) {
    const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
    table_row_to_append_to.innerHTML = '';
    data.forEach(row => {
      const tr = document.createElement('ul');
      tr.classList.add('table-custom__content__rows__row');
      tr.innerHTML = `
      <li class="mobile-no-display" style="display:none;" id="game-id">${row.game_id}</li>
      <li class="mobile-no-display" style="display:none;" id="avg-market-odds">${row.average_market_odds}</li>

      <li before-data="Team: " id ="team-bet-on"><p><b >${row.team} </b><br class = "mobile-no-display"> v. ${row.opponent} </p></li>

      <li class="sportsbook-li">
        <div class="tooltip" id="sportsbook">
                    <span class="tooltiptext"></span>
        </div>
      </li>
      <li before-data="Recommended Bet Size ($): " editable="true" id="rec-bet-size-number">$ ${row.bet_amount}</li>
      <li data-before="Min" id = "min-odds">${addSign(row.highest_acceptable_odds)}</li>
      <li data-before="Best" editable="true" id = "best-odds">${addSign(row.highest_bettable_odds)}</li>
      <li before-data="+EV%: " id="ev">${row.ev}%</li>
      <li id ="game-date">${row.game_date}</li>
      <li before-data="Time Since Odds Update: " id="time-dif">${row.time_difference_formatted}</li>
      <li data-title="button" onclick="editRow(this)" class="add-to-betslip-button" id="add-to-betslip-button" data-ev="${row.ev}" data-team="${row.team_1}" data-odds="${row.highest_bettable_odds}" style="display:flex; display: flex;
      align-items: center; justify-content: center;"><svg
      viewBox="0 0 20 20"
      width="20"
      height="20"
      version="1.1"
      id="svg1"
      sodipodi:docname="icons8-plus.svg"
      inkscape:version="1.3 (0e150ed, 2023-07-21)"
      xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
      xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:svg="http://www.w3.org/2000/svg">
     <defs
        id="defs1" />
     <sodipodi:namedview
        id="namedview1"
        pagecolor="#ffffff"
        bordercolor="#000000"
        borderopacity="0.25"
        inkscape:showpageshadow="2"
        inkscape:pageopacity="0.0"
        inkscape:pagecheckerboard="0"
        inkscape:deskcolor="#d1d1d1"
        inkscape:zoom="9.8333333"
        inkscape:cx="12"
        inkscape:cy="12"
        inkscape:window-width="1312"
        inkscape:window-height="449"
        inkscape:window-x="0"
        inkscape:window-y="25"
        inkscape:window-maximized="0"
        inkscape:current-layer="svg1" />
     <path
        d="M 10,0 C 4.477,0 0,4.477 0,10 0,15.523 4.477,20 10,20 15.523,20 20,15.523 20,10 20,4.477 15.523,0 10,0 Z m 4,11 h -3 v 3 c 0,0.552 -0.448,1 -1,1 v 0 C 9.448,15 9,14.552 9,14 V 11 H 6 C 5.448,11 5,10.552 5,10 v 0 C 5,9.448 5.448,9 6,9 H 9 V 6 C 9,5.448 9.448,5 10,5 v 0 c 0.552,0 1,0.448 1,1 v 3 h 3 c 0.552,0 1,0.448 1,1 v 0 c 0,0.552 -0.448,1 -1,1 z"
        id="path1"
        style="fill:var(--table-btn-bg)" />
   </svg></li>
      <li class="desktop-no-display" id ="rec-bet-size-text">Rec Bet Size</li>
      <li class="desktop-no-display" id="green">Moneyline</li>
      <li class="desktop-no-display" style="display:none;" id="team">${row.team}</li>
      <li style="display:none;" id="sportsbooks-used">${row.sportsbooks_used}</li>
      `;
      table_row_to_append_to.appendChild(tr);
      getImage(row.sportsbooks_used, tr);
    });
  }
  else
  {
    tr.innerHTML = `
  <li class="centered">
  No recommended bets available right now. This table populates when our AI finds profitable betting opportunities. Check again closer to game time and update table.
  </li>
  `;
  footer_to_change_innerhtml.innerHTML = `<p>Showing 0 Entries</p>`;
  table_row_to_append_to.appendChild(tr);
    console.log('No update');
  }
  footer_to_append_to.appendChild(footer_to_change_innerhtml);
}

function updatebankroll(data){
  const bankroll = document.querySelector('#bankroll');
  bankroll.innerHTML = 'These are +EV bets that our machine learning model, with predictive pattern recognition, has identified as having value for an increased hit rate and profitability in the long run.';
  // bankroll.innerHTML  += `${data[0].bankroll}`;
  console.log(data[0].bankroll);

}

function addSign(input) {
  console.log(input);
  const str = input.toString(); // Convert input to string
  return str.charAt(0) === '-' ? str : '+' + str;
}

function getCurrentTime() {
  const currentTime = new Date();
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const options = { timeZone: userTimezone, hour12: true, hour: 'numeric', minute: 'numeric', second: 'numeric'};
  const formattedTime = currentTime.toLocaleString(undefined, options);
  return `${formattedTime}`;
}

function convertToUserTimezone(inputTime) {
  console.log(inputTime)
  const dateObj = new Date(inputTime);
  if (isNaN(dateObj)) {
    return '';
  }
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const userTime = new Date(dateObj.toLocaleString('en-US', { timeZone: userTimezone }));
  const options = { timeZone: userTimezone, weekday: 'short', day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZoneName: 'short' };
  const formattedTime = userTime.toLocaleString('en-US', options);
  console.log('user_time_next')
  console.log(formattedTime)
  return formattedTime;
}

function convertToUserTimezoneUpdate(inputTime) {
  const dateObj = new Date(inputTime);
  if (isNaN(dateObj)) {
    return '';
  }
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const userTime = new Date(dateObj.toLocaleString('en-US', { timeZone: userTimezone }));
  const options = { timeZone: userTimezone, hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short' };
  const formattedTime = userTime.toLocaleString('en-US', options);
  return formattedTime;
}

function addToBetslip() {
  console.log('Adding bet to betslip:');

  $.ajax({
    url: '/add_to_betslip', // Flask endpoint
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function(response) {
      console.log(response.message); // Log the response from Flask
    },
    error: function(error) {
      console.error('Error adding bet to betslip:', error);
    }
  });
}

function resetRowView(){
  // var elements = document.querySelectorAll('.adding-to-bet-tracker');
  // console.log(resetRowView);
  // // Iterate through the NodeList and remove the class name
  // elements.forEach(function(element) {
  //   element.classList.remove('adding-to-bet-tracker');
  // });
  location.reload();
}

function saveRow(row) {
  var toggleButton = row.querySelector('.toggle-button');
  var modifiedNumber = toggleButton.innerText === "-" ? - + row.querySelector("#odds-taken-input").value : row.querySelector("#odds-taken-input").value;
  console.log(toggleButton.innerHTML);
  // make a dict with thte values of each cell in the right spot

  var rowDataDict = {
    'game_id':row.querySelector("#game-id").innerHTML,

    'average_market_odds':row.querySelector("#avg-market-odds").innerHTML,

    'team':row.querySelector("#team-bet-on").innerText.replace(/\n/g, ''),

    'sportsbooks_used': row.querySelector("#selected-option img").getAttribute('alt'),

    'bet_amount':row.querySelector("#bet-size-input").value,

    'highest_bettable_odds': modifiedNumber,

    'minimum_acceptable_odds':row.querySelector("#min-odds").innerHTML,

    'ev':row.querySelector("#ev").innerHTML.replace(/%/g, ''),

    'date':row.querySelector("#game-date").innerHTML,

    'time_difference_formatted':row.querySelector("#time-dif").innerHTML,
  }
  console.log(rowDataDict);

  $.ajax({
    url: '/add_saved_bet',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(rowDataDict), 
    success: function(response) {
      if (response.status_code === 'error') {
        console.log('Error saving bet:', response.message);
      } else {
        console.log('Bet saved successfully:', response.message);
        currentlyEditingRow = false;
        resetRowView();
      }
    },
    error: function(error) {
      console.error('Error saving bet:', error);
    }
  });
}

function displaySportsbookDropdown(row){
  
  var sportsbook = row.querySelector(".sportsbook-li");
  sportsbook.style.position = 'static';
  var sportsBooksStringElement = row.querySelector('#sportsbook p');

  if (sportsBooksStringElement) {
    sportsBooksStringElement.style.display = 'block';
    var sportsBooksString = sportsBooksStringElement.textContent;
    var firstSportsbook = sportsBooksString.split(', ')[0];
    var firstImageWithAlt = document.querySelector('img[alt="' + firstSportsbook + '"]');
    firstImageWithAlt.style.borderRadius = "10px";
    console.log(firstImageWithAlt);
    sportsBooksStringElement.style.display = 'none';
  }
  
  var dropdownOptions = document.getElementById('dropdown-options');
  var dropdownContainer = document.getElementById('dropdown-container');
  dropdownContainer.style.display = "flex";

  var dropdownBtn = dropdownContainer.querySelector('#show-dropdown-btn');
  var selectedOption = document.getElementById('selected-option');
  selectedOption.innerHTML = '';
  selectedOption.append(firstImageWithAlt);

  sportsbook.innerHTML = '';
  sportsbook.appendChild(dropdownContainer);
  
  dropdownBtn.addEventListener('click', function () {
    dropdownOptions.classList.add("adding-to-bet-tracker");
  });

  dropdownOptions.addEventListener('click', function (event) {
    var liElement = event.target.closest('li');
    var imgElement = liElement.querySelector('img')
    imgElement.height = 32;
    imgElement.width = 32;
    imgElement.style.borderRadius = '10px';
    if (liElement) {
      selectedOption.innerHTML = '';
      selectedOption.append(imgElement);
      dropdownOptions.classList.remove("adding-to-bet-tracker");


    }
  });

  // Close the dropdown if the user clicks outside of it
  window.addEventListener('click', function (event) {
    if (!event.target.matches('#show-dropdown-btn')) {
      var openDropdown = document.getElementById('dropdown-options');
      if (openDropdown.style.display === 'block') {
        openDropdown.style.display = 'none';
      }
    }
  });
  

}

function changeRowDisplay(row){
  //Change the "Recommened bet size" to "Placed bet size" on MOBILE
  const recBetSize = row.querySelector("#rec-bet-size-text");
  recBetSize.innerText = "Placed Bet Size"

  // Change the team name to "Placed Bet Odds" on MOBILE
  const team = row.querySelector("#team");
  team.innerHTML = "Placed Bet Odds";

  // Make the input for "Placed bet size"
  const recBetSizeNumber = row.querySelector("#rec-bet-size-number");

  // Make a class that changes the display on mobile and on desktop differently 
  recBetSizeNumber.classList.add("adding-to-bet-tracker");
  // Make an input that copies all the styles from the prev elment
  var recBetSizeNumberStyles = window.getComputedStyle(recBetSizeNumber);
  const betSizeInput = document.createElement('input');
  betSizeInput.id = "bet-size-input";
  betSizeInput.style.flex = "0 0 auto";

  betSizeInput.classList.add("adding-to-bet-tracker");

  for (var style in recBetSizeNumberStyles) {
    betSizeInput.style[style] = recBetSizeNumberStyles[style];
  }
  recBetSizeNumber.innerHTML = '';
  recBetSizeNumber.appendChild(betSizeInput);

  dollarUnit = document.createElement('div');
  dollarUnit.innerHTML = "$";
  recBetSizeNumber.appendChild(dollarUnit);
  recBetSizeNumber.appendChild(betSizeInput);


  const bestOddsNumber = row.querySelector("#best-odds");
  bestOddsNumber.classList.add("adding-to-bet-tracker");
  bestOddsNumber.setAttribute('data-before', '');

  bestOddsNumber.style.display = "flex";
  bestOddsNumber.style.alignItems = "center";
  bestOddsNumber.style.justifyContent = "center";

  // Remove display for Min odds li on MOBILE
  const minOdds = row.querySelector("#min-odds");
  minOdds.classList.add("adding-to-bet-tacker")

  // Make the input for the "Best odds taken"
  const oddsTakenInput = document.createElement('input');
  var recBetSizeStyles = window.getComputedStyle(recBetSize);
  for (var style in recBetSizeStyles) {
    oddsTakenInput.style[style] = recBetSizeStyles[style];
  }
  oddsTakenInput.id = "odds-taken-input";
  oddsTakenInput.classList.add("adding-to-bet-tracker");
  bestOddsNumber.innerHTML = '';
  test = document.createElement('div')
  test.setAttribute('class', "toggle-button");
  test.setAttribute('onclick', "toggleUnit()");
  test.innerHTML = "+";
  test.style.fontSize = "1.5rem";
  test.style.cursor = "pointer";
  bestOddsNumber.appendChild(test);
  bestOddsNumber.appendChild(oddsTakenInput);
}


function changePlusSignDisplay(row){
  buttonLi = row.querySelector("#add-to-betslip-button");
  buttonLi.innerHTML = '';
  buttonEl = document.createElement('button');
  buttonEl.id= ("save-button");
  buttonEl.innerHTML = "Save"
  buttonEl.classList.add("adding-to-bet-tracker");
  buttonLi.appendChild(buttonEl);
  buttonLi.onclick = function() {
    saveRow(row);
  }
}

var unitToggle = true;
function toggleUnit() {
  console.log("clicked");
  var li = document.getElementById('rec-bet-size-number');
  var input = li.querySelector('input')

  var toggleButton = document.querySelector('.toggle-button');
  unitToggle = !unitToggle;
  toggleButton.innerText = unitToggle ? '+' : '-';
}

function editRow(button) {
  currentlyEditingRow = true;
  const row = button.parentNode;
  displaySportsbookDropdown(row);
  changeRowDisplay(row);
  changePlusSignDisplay(row);
};


function getImage(sportsbook_string, row){

  var imageContainer = row.querySelector('#sportsbook');

  imageContainer.classList.add("tooltip");

  var sportsbookP = document.createElement('p');

  sportsbookP.innerText = sportsbook_string;
  sportsbookP.classList.add("tooltiptext_img");
  imageContainer.appendChild(sportsbookP);

  // Check if the image container exists before setting its style
  if (imageContainer) {

    var imageDictionary = {
      Pointsbetus: '/static/images/pointsbetus.webp',
      Barstool: '/static/images/barstool.webp',
      Draftkings: '/static/images/draftkings.webp',
      Fanduel: '/static/images/fanduel.webp',
      Betus: '/static/images/betus.webp',
      Wynnbet: '/static/images/wynnbet.webp',
      Mybookieag: '/static/images/mybookieag.webp',
      Betonlineag: '/static/images/betonlineag.webp',
      Betrivers: '/static/images/betrivers.webp',
      Unibet_Us: '/static/images/unibetus.webp',
      Pinnacle: '/static/images/pinnacle.webp',
      Betmgm: '/static/images/betmgm.webp',
      Williamhill_Us: '/static/images/williamhillus.webp',
    };

    var sportsBooks = sportsbook_string.split(', ');

    sportsBooks.forEach(sportsbook => {
    
      var imageUrl = imageDictionary[sportsbook];
      if (imageUrl) { // Check if the URL exists in the dictionary
        var imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.alt = sportsbook;
        imgElement.height = 32;
        imgElement.width = 32;
        imageContainer.appendChild(imgElement);
      } else {
        console.error('Image URL not found for:', sportsbook);
      }
    });
  } else {
    console.error('Image container not found.');
  }
}

function fetchDataAndUpdateTable() {
  var currentURL = window.location.href;
  var urlSegments = currentURL.split('/');
  // Get the last segment (element) of the URL
  var tabValue = urlSegments[urlSegments.length - 1].toUpperCase();
  const url = '/get_live_dash_data?';
  fetch(url,{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ sport_title: tabValue }),
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      updateTable(data);
      updatebankroll(data);
    })
    .catch(error => console.error('Error fetching data:', error));
}

function addToBankroll() {
  console.log('Editing bankroll:');
  const existingInput = bankrollP.querySelector('input');
  const existingSaveButton = bankrollP.querySelector('button');

  if (existingInput) {
    bankrollP.removeChild(existingInput);
  }

  if (existingSaveButton) {
    bankrollP.removeChild(existingSaveButton);
  }
    
  const input = document.createElement('input');
  input.type = 'number';
  input.placeholder = "Amount to add or subtract from bankroll";
  input.classList.add('bankroll-input'); // Add class to input

  bankrollP.appendChild(input);

  const saveButton = document.createElement('button');
  saveButton.innerText = 'Save';
  saveButton.classList.add('live-button'); // Add class to button
  bankrollP.appendChild(saveButton);

  saveButton.addEventListener("click", function() {
    const amount = parseFloat(input.value);
    console.log('Amount:', amount);

    fetch('/add_to_bankroll', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ amount }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Server response:', data);
      bankrollP.removeChild(input);
      bankrollP.removeChild(saveButton);
      fetchDataAndUpdateTable();
    });
  });
}

function toggleSport(){
  var currentURL = window.location.href;
  var urlSegments = currentURL.split('/');
  
  // Get the last segment (element) of the URL
  var targetSport = urlSegments[urlSegments.length - 1].toUpperCase();
  
  console.log("Last segment of the URL: " + targetSport);
  var elements = document.querySelectorAll('[data-sport="' + targetSport + '"]');

  if (elements.length > 0) {
    // Add the "active" class to the first matching element
    elements[0].classList.add('active');
}
}

$(document).ready(function(){
  // toggle sidebar
  const menuIcon = document.querySelector(".navbar-custom__left i");
  const closeIcon = document.querySelector(".sidebar-custom .close-icon");
  const logo = document.querySelector(".sidebar-custom__logo img");
  menuIcon.addEventListener("click", (e) => {
    document.querySelector(".sidebar-custom").classList.add("active");
  });

  closeIcon.addEventListener("click", (e) => {
    document.querySelector(".sidebar-custom").classList.remove("active");
  });

  const button = document.querySelector("[data-theme-toggle]");
  const localStorageTheme = localStorage.getItem("theme");
  const systemSettingDark = window.matchMedia("(prefers-color-scheme: dark)");

  /**
   * 2. Work out the current site settings
   */
  let currentThemeSetting = calculateSettingAsThemeString({
    localStorageTheme,
    systemSettingDark,
  });


  if (currentThemeSetting === "light") {
    logo.setAttribute("src", "static/images/whitelogo.png");
  } else {
    logo.setAttribute("src", "static/images/sidebar_logo.png");
  }
  /**
   * 3. Update the theme setting and button text accoridng to current settings
   */
  updateButton({ buttonEl: button, isDark: currentThemeSetting === "dark" });
  updateThemeOnHtmlEl({ theme: currentThemeSetting });

  /**
 * 4. Add an event listener to toggle the theme
 */
  button.addEventListener("click", (event) => {
    const newTheme = currentThemeSetting === "dark" ? "light" : "dark";
    if (newTheme === "light") {
      logo.setAttribute("src", "static/images/whitelogo.png");
    } else {
      logo.setAttribute("src", "static/images/sidebar_logo.png");
    }

    localStorage.setItem("theme", newTheme);
    updateButton({ buttonEl: button, isDark: newTheme === "dark" });
    updateThemeOnHtmlEl({ theme: newTheme });

    currentThemeSetting = newTheme;
  });
  

  toggleSport();



  /** 
   * 5. Add an event listener to update table and bankroll
   */
  document.getElementById('fetch-button').addEventListener('click', fetchDataAndUpdateTable);

  fetchDataAndUpdateTable();
});




