let userPermissionVar; 
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
  var img = document.createElement('img'); 
  if(theme == "dark"){
    img.src = "static/images/footer_logo_dark_mode.png"
  }
  else{
    img.src = "static/images/footer_logo_light_mode.png"

  }
  img.classList.add("footer-logo");
  document.querySelector(".talk-to-us").innerHTML = '';
  document.querySelector(".talk-to-us").appendChild(img);
}

function updateTable(data) {

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

      <li before-data="Team: " id ="team-bet-on"><p><b >${row.sport_title_display} </b><br class = "mobile-no-display"> ${row.sport_league_display} </p></li>

      <li before-data="Team: " id ="market" class="mobile-no-display" ><p><b>${row.market_display} </b><br>${row.wager_display}</p></li>

      <li before-data="Team: " id ="team-bet-on"><p><b >${row.away_team} </b><br class = "mobile-no-display"> @ ${row.home_team} </p></li>

      <li id ="game-date">${row.game_date}</li>

      <li class="sportsbook-li">
        <div class="tooltip" id="sportsbook">
                    <span class="tooltiptext"></span>
        </div>
      </li>

      <li before-data="Recommended Bet Size ($): " editable="true" id="rec-bet-size-number">$ ${row.bet_amount}</li>

      <li data-before="Min" id = "min-odds">${addSign(row.highest_acceptable_odds)}</li>

      <li data-before="Best" editable="true" id = "best-odds">${addSign(row.highest_bettable_odds)}</li>

      <li before-data="+EV%: " id="ev">${row.ev}%</li>

      <li before-data="Time Since Odds Update: " id="time-dif">${row.time_difference_formatted}</li>

      <li class="desktop-no-display" id ="rec-bet-size-text">Rec Bet Size</li>
      <li before-data="Team: " id ="market" class="desktop-no-display" >${row.market_display} </li>
      <li before-data="Team: " id ="market" class="desktop-no-display" >${row.wager_display} </li>`

      // <li class="desktop-no-display" style="display:none;" id="team">${row.team}</li>
      // <li style="display:none;" id="sportsbooks-used">${row.sportsbooks_used}</li>
      ;
      table_row_to_append_to.appendChild(tr);
      getImage(row.sportsbooks_used, tr);
    });
  }
  else
  {
    tr.innerHTML = `
  <li class="centered">
  No approved bets right now. Check back again soon.
  </li>
  `;
  footer_to_change_innerhtml.innerHTML = `<p>Showing 0 Entries</p>`;
  table_row_to_append_to.appendChild(tr);
    console.log('No update');
  }
  footer_to_append_to.appendChild(footer_to_change_innerhtml);
}

function updateTableFree(data) {
  console.log(data);

  const footer_to_append_to = document.querySelector('.table-custom__footer');
  const footer_to_change_innerhtml= document.querySelector('.footer-to-make-innerhtml');
  footer_to_change_innerhtml.innerHTML = `<p>Showing ${data.length} Entries</p>`;

  const tableBody = document.querySelector('.table-custom__content');
  const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
  table_row_to_append_to.innerHTML = '';

  const tr = document.createElement('ul');

  boolin = true;

  
  if (!(data.length === 1 && data[0].update === false) && boolin ) {
    const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
    table_row_to_append_to.innerHTML = '';

    var i = 0;

    data.forEach(row => {
      if(i==0){
      const tr = document.createElement('ul');
      tr.classList.add('table-custom__content__rows__row');
      tr.classList.add('no-bottom-border');
      tr.innerHTML = `
      <li class="mobile-no-display" style="display:none;" id="game-id">${row.game_id}</li>
      <li class="mobile-no-display" style="display:none;" id="avg-market-odds">${row.average_market_odds}</li>

      <li before-data="Team: " id ="team-bet-on"><p><b >${row.sport_title_display} </b><br class = "mobile-no-display"> ${row.sport_league_display} </p></li>

      <li before-data="Team: " id ="market" class="mobile-no-display" ><p><b>${row.market_display} </b><br>${row.wager_display}</p></li>

      <li before-data="Team: " id ="team-bet-on"><p><b >${data[0].away_team} </b><br class = "mobile-no-display"> @ ${row.home_team} </p></li>

      <li id ="game-date">${row.game_date}</li>

      <li class="sportsbook-li">
        <div class="tooltip" id="sportsbook">
                    <span class="tooltiptext"></span>
        </div>
      </li>

      <li before-data="Recommended Bet Size ($): " editable="true" id="rec-bet-size-number">$ ${row.bet_amount}</li>

      <li data-before="Min" id = "min-odds">${addSign(row.highest_acceptable_odds)}</li>

      <li data-before="Best" editable="true" id = "best-odds">${addSign(row.highest_bettable_odds)}</li>

      <li before-data="+EV%: " id="ev">${row.ev}%</li>

      <li before-data="Time Since Odds Update: " id="time-dif">${row.time_difference_formatted}</li>

      <li class="desktop-no-display" id ="rec-bet-size-text">Rec Bet Size</li>
      <li before-data="Team: " id ="market" class="desktop-no-display" >${row.market_display} </li>
      <li before-data="Team: " id ="market" class="desktop-no-display" >${row.wager_display} </li>`

      // <li class="desktop-no-display" style="display:none;" id="team">${row.team}</li>
      // <li style="display:none;" id="sportsbooks-used">${row.sportsbooks_used}</li>
      ;
      table_row_to_append_to.appendChild(tr);
      getImage(row.sportsbooks_used, tr);
      i+=1;
      }else if(i==1){
        tr.innerHTML = `
  <li class="free-view-login-sign-up-container">
        <div class = "free-view-login-sign-up-buttons-container">
          <div class = "free-view-login-container"><a class = "free-view-login-button" href = "/login">Login</a></div>
          <div class = "or">or</div>
          <div class = "free-view-sign-up-container"><a class = "free-view-sign-up-button"href = "/register">Sign Up</a></div>
        </div>
      <div><p>To see thousands of +EV bets refresh all day long...</p> <div>
  </li>
  `;
  footer_to_change_innerhtml.innerHTML = `<p>Showing 1 Entry</p>`;
  table_row_to_append_to.appendChild(tr);
    console.log('No update');
    i+=1;
  }else {
    const tr = document.createElement('ul');
    tr.classList.add('table-custom__content__rows__row');
    tr.classList.add('blurred');
    tr.innerHTML = `
    <li class="mobile-no-display" style="display:none;" id="game-id">${row.game_id}</li>
    <li class="mobile-no-display" style="display:none;" id="avg-market-odds">${row.average_market_odds}</li>

    <li before-data="Team: " id ="team-bet-on"><p><b >${row.sport_title_display} </b><br class = "mobile-no-display"> ${row.sport_league_display} </p></li>

    <li before-data="Team: " id ="market" class="mobile-no-display" ><p><b>${row.market_display} </b><br>${row.wager_display}</p></li>

    <li before-data="Team: " id ="team-bet-on"><p><b >${data[0].away_team} </b><br class = "mobile-no-display"> @ ${row.home_team} </p></li>

    <li id ="game-date">${row.game_date}</li>

    <li class="sportsbook-li">
      <div class="tooltip" id="sportsbook">
                  <span class="tooltiptext"></span>
      </div>
    </li>

    <li before-data="Recommended Bet Size ($): " editable="true" id="rec-bet-size-number">$ ${row.bet_amount}</li>

    <li data-before="Min" id = "min-odds">${addSign(row.highest_acceptable_odds)}</li>

    <li data-before="Best" editable="true" id = "best-odds">${addSign(row.highest_bettable_odds)}</li>

    <li before-data="+EV%: " id="ev">${row.ev}%</li>

    <li before-data="Time Since Odds Update: " id="time-dif">${row.time_difference_formatted}</li>

    <li class="desktop-no-display" id ="rec-bet-size-text">Rec Bet Size</li>
    <li before-data="Team: " id ="market" class="desktop-no-display" >${row.market_display} </li>
    <li before-data="Team: " id ="market" class="desktop-no-display" >${row.wager_display} </li>`

    // <li class="desktop-no-display" style="display:none;" id="team">${row.team}</li>
    // <li style="display:none;" id="sportsbooks-used">${row.sportsbooks_used}</li>
    ;
    table_row_to_append_to.appendChild(tr);
    getImage(row.sportsbooks_used, tr);
    i+=1;
    }
  footer_to_append_to.appendChild(footer_to_change_innerhtml);
      
    });

  }
  else
  {
    tr.innerHTML = `
  <li class="centered">
  No approved bets right now. Check back again soon.
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
  bankroll.innerHTML = 'These are +EV bets that our market scanning algorithm has identified. EV is calculated based on average implied odds from more than 50 international bookmakers including Pinnacle.';
  // bankroll.innerHTML  += `${data[0].bankroll}`;
  console.log(data[0].bankroll);
}

function addSign(input) {
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

  const dateObj = new Date(inputTime);
  if (isNaN(dateObj)) {
    return '';
  }
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const userTime = new Date(dateObj.toLocaleString('en-US', { timeZone: userTimezone }));
  const options = { timeZone: userTimezone, weekday: 'short', day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZoneName: 'short' };
  const formattedTime = userTime.toLocaleString('en-US', options);
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
  location.reload();
}

function saveRow(row) {
  var toggleButton = row.querySelector('.toggle-button');
  var modifiedNumber = toggleButton.innerText === "-" ? - + row.querySelector("#odds-taken-input").value : row.querySelector("#odds-taken-input").value;
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
      if (openDropdown.style.display === 'flex') {
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
  oddsTakenInput.style.display = "flex";


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

function toggleOverlay() {
  var overlay = document.getElementById('loom-container');
  overlay.style.display = 'none'
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
      Bovada: '/static/images/bovada.webp',
      Lowvig: '/static/images/lowvig.webp',
      Superbook: '/static/images/superbook.webp',
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

  // Retrieve elements with 'active' class
  var activeElements = document.querySelectorAll('.filter-dropdown-item.active');
  var innerTextDictionary = {};
  activeElements.forEach(function(element) {
    var parentId = element.closest('[id]').id;
    innerTextDictionary[parentId] = element.innerText;
  });

  var ascendingBool =  document.querySelectorAll('svg.sort-icon.active')[0].getAttribute("ascending");

  if(ascendingBool == null){
    ascendingBool = false;
  }else if(ascendingBool == 'true'){
    ascendingBool = true;
  }
  else if(ascendingBool == 'false'){
    ascendingBool = false;
  }

  innerTextDictionary['sort-by'] = [document.querySelectorAll('svg.sort-icon.active')[0].getAttribute("id"), ascendingBool]

  // Get the last segment (element) of the URL
  const url = '/get_positive_ev_dash_data?';

  const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
  table_row_to_append_to.innerHTML = '';
  const tr = document.createElement('ul');
  tr.classList.add('table-custom__content__rows__row');
  tr.innerHTML = '<li class="centered"> Updating........ </li>'
  table_row_to_append_to.appendChild(tr);

  fetch(url,{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({filters: innerTextDictionary}),
  })
    .then(response => response.json())
    .then(data => {
      console.log(userPermissionVar);
      if(userPermissionVar =='standard' || userPermissionVar == 'premium'){
        updateTable(data);
      }else{
        updateTableFree(data);
      }
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
    });
  });
}

function toggleSport(){
  var currentURL = window.location.href;
  var urlSegments = currentURL.split('/');
  
  // Get the last segment (element) of the URL
  var targetSport = urlSegments[urlSegments.length - 1];
  
  var elements = document.querySelectorAll('[data-sport="' + targetSport + '"]');

  if (elements.length > 0) {
    // Add the "active" class to the first matching element
    elements[0].classList.add('active');
}
}

function findAncestorWithClass(element, className) {
  while ((element = element.parentElement) && !element.classList.contains(className));
  return element;
}

function findCousinWithClass(element, className) {
  var ancestor = findAncestorWithClass(element, 'filter-container');
  if (ancestor) {
    var cousinElementSearchedFor = ancestor.querySelectorAll('.' + className);
    return cousinElementSearchedFor[0];
  }
}

function greenIfFiltered(event){
  var filterSVG = findCousinWithClass(event.target, 'dropbtn');

  if (filterSVG && event.target.innerText !== 'ALL') {
      var paths = filterSVG.querySelectorAll('path');
      paths.forEach(function(path) {
        path.style.fill = '#21ce99';
    })}
    else if (filterSVG && event.target.innerText == 'ALL') {
      var paths = filterSVG.querySelectorAll('path');
      paths.forEach(function(path) {
        path.style.fill = 'var(--table-thead-color)';
    });

}
}

function fillFilterValues(){
  fetch('/get_filter_dropdown_values',{
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(response => response.json())
    .then(data => {

      var sportLeagueFilterDiv = document.getElementById("sport-league-filter");
      data['sport_league_display'].forEach(function(league){
        var filterValue = document.createElement('a');
        filterValue.innerHTML = league
        filterValue.classList.add("filter-dropdown-item");
        if(league == "all"){
          filterValue.classList.add("active");
        }
        filterValue.addEventListener('click', greenIfFiltered);
        filterValue.addEventListener('click', fetchDataAndUpdateTable);

        filterValue.addEventListener('click', function(e) {
          var filterItems = sportLeagueFilterDiv.querySelectorAll('.filter-dropdown-item');
          filterItems.forEach(function(item) {
            item.classList.remove('active');
          });
          filterValue.classList.add('active');
        });

        sportLeagueFilterDiv.appendChild(filterValue)
      })

      var marketFilterDiv = document.getElementById("market-filter");
      data['market_display'].forEach(function(market){
        var filterValue = document.createElement('a');
        filterValue.classList.add("filter-dropdown-item");
        filterValue.innerHTML = market
        if(market == "all"){
          filterValue.classList.add("active");
        }
        filterValue.addEventListener('click', greenIfFiltered);
        filterValue.addEventListener('click', fetchDataAndUpdateTable);

        filterValue.addEventListener('click', function(e) {
          var filterItems = marketFilterDiv.querySelectorAll('.filter-dropdown-item');
          filterItems.forEach(function(item) {
            item.classList.remove('active');
          });
          filterValue.classList.add('active');
        });
        marketFilterDiv.appendChild(filterValue)
      })

      var gameDateFilterDiv = document.getElementById("game-date-filter");
      data['game_date'].forEach(function(league){
        var filterValue = document.createElement('a');
        filterValue.innerHTML = league
        
        filterValue.classList.add("filter-dropdown-item");
        if(league == "all"){
          filterValue.classList.add("active");
        }
        filterValue.addEventListener('click', greenIfFiltered);
        filterValue.addEventListener('click', fetchDataAndUpdateTable);


        filterValue.addEventListener('click', function(e) {
          var filterItems = gameDateFilterDiv.querySelectorAll('.filter-dropdown-item');
          filterItems.forEach(function(item) {
            item.classList.remove('active');
          });
          filterValue.classList.add('active');
        });
        gameDateFilterDiv.appendChild(filterValue)
      })

      var sportsbookFilterDiv = document.getElementById("sportsbook-filter");
      data['sportsbooks_used'].forEach(function(league){
        var filterValue = document.createElement('a');
        filterValue.innerHTML = league
        
        filterValue.classList.add("filter-dropdown-item");
        if(league == "all"){
          filterValue.classList.add("active");
        }
        filterValue.addEventListener('click', greenIfFiltered);
        filterValue.addEventListener('click', fetchDataAndUpdateTable);


        filterValue.addEventListener('click', function(e) {
          var filterItems = sportsbookFilterDiv.querySelectorAll('.filter-dropdown-item');
          filterItems.forEach(function(item) {
            item.classList.remove('active');
          });
          filterValue.classList.add('active');
        });
        sportsbookFilterDiv.appendChild(filterValue)
      })
    })
    .catch(error => console.error('Error fetching data:', error));
}


function getUserPermission() {
  return fetch('/get_user_permission', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      throw error; // Re-throw the error to handle it outside this function if needed
    });
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
    logo.setAttribute("src", "static/images/sidebar_logo.png");
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
      logo.setAttribute("src", "static/images/sidebar_logo.png");
    } else {
      logo.setAttribute("src", "static/images/sidebar_logo.png");
    }

    localStorage.setItem("theme", newTheme);
    updateButton({ buttonEl: button, isDark: newTheme === "dark" });
    updateThemeOnHtmlEl({ theme: newTheme });

    currentThemeSetting = newTheme;
  });
  
  toggleSport();

  var dropdownBtns = document.querySelectorAll('.dropbtn');

  dropdownBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      var container = this.closest('.filter-container'); 
      if (container) {
        var siblingElement = container.querySelector('.dropdown-content');
        if (siblingElement) {
          siblingElement.classList.toggle('show');
        }}
      })
  });

  window.addEventListener('click', function(event) {
    dropdownBtns.forEach(function(btn) {
      var container = btn.closest('.filter-container');
      if (container) {
        var siblingElement = container.querySelector('.dropdown-content');
        if (siblingElement && siblingElement.classList.contains("show") && !btn.contains(event.target)) {
          siblingElement.classList.remove('show');
        }
      }
    });
  });

  fillFilterValues();

    /** 
   * 5. Add an event listener to update table and bankroll
   */
    document.getElementById('fetch-button').addEventListener('click', fetchDataAndUpdateTable);

    var svgs = document.querySelectorAll('.sort-icon');

    svgs.forEach(function(svg) {
      svg.setAttribute('ascending', false);
      svg.addEventListener('click', fetchDataAndUpdateTable);
      svg.addEventListener('click', function() {
        var path = this.querySelector('.arrow-head');
        var isActive = this.classList.contains('active');
        if (isActive) {
          var currentD = path.getAttribute('d');
          var newD = currentD === 'm 2.4925484,13.778706 c -0.081574,0 -0.1599452,-0.03248 -0.2176345,-0.0902 L 0.20880797,11.622411 c -0.1202399,-0.120215 -0.1202399,-0.315079 0,-0.435292 0.1200713,-0.120215 0.31523142,-0.120215 0.43528867,0 l 1.84845456,1.848452 1.8482971,-1.848452 c 0.1200713,-0.120215 0.3150797,-0.120215 0.4352915,0 0.1202399,0.120212 0.1202399,0.315079 0,0.435292 l -2.0659429,2.066097 c -0.057746,0.05772 -0.1360602,0.0902 -0.2176345,0.0902 z' ? 'm 2.4925484,0.06306169 c -0.081574,0 -0.1599452,0.03248 -0.2176345,0.0902 L 0.20880797,2.2193567 c -0.1202399,0.120215 -0.1202399,0.315079 0,0.435292 0.1200713,0.120215 0.31523142,0.120215 0.43528867,0 L 2.4925512,0.80619669 4.3408483,2.6546487 c 0.1200713,0.120215 0.3150797,0.120215 0.4352915,0 0.1202399,-0.120212 0.1202399,-0.315079 0,-0.435292 L 2.7101969,0.15325969 c -0.057746,-0.05772 -0.1360602,-0.0902 -0.2176345,-0.0902 z' : 'm 2.4925484,13.778706 c -0.081574,0 -0.1599452,-0.03248 -0.2176345,-0.0902 L 0.20880797,11.622411 c -0.1202399,-0.120215 -0.1202399,-0.315079 0,-0.435292 0.1200713,-0.120215 0.31523142,-0.120215 0.43528867,0 l 1.84845456,1.848452 1.8482971,-1.848452 c 0.1200713,-0.120215 0.3150797,-0.120215 0.4352915,0 0.1202399,0.120212 0.1202399,0.315079 0,0.435292 l -2.0659429,2.066097 c -0.057746,0.05772 -0.1360602,0.0902 -0.2176345,0.0902 z';
          path.setAttribute('d', newD);
          this.setAttribute('ascending', this.getAttribute('ascending') === true ? false: true);
        } 
        else {
          svgs.forEach(function(s) {
            s.classList.remove('active');
            s.setAttribute('ascending', false);
        })
        this.classList.add('active');
        this.setAttribute('ascending', false);
      }
      });
    });

    getUserPermission()
    .then(userPermission => {
      console.log(userPermissionVar);
      userPermissionVar = userPermission.permission;
      fetchDataAndUpdateTable();
    })
    .catch(error => {
      console.log(error);
    });

    
});
