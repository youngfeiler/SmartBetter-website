let userPermissionVar;
//container flex row, overflow scroll, time since update
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
  return "dark";
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


function updateTable(data) {
  console.log(data);
  const footer_to_append_to = document.querySelector('.table-custom__footer');
  const footer_to_change_innerhtml = document.querySelector('.footer-to-make-innerhtml');
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
        <p class = "desktop-no-display time-dif-carrot"> > </p>
      </li>

      <li before-data="Recommended Bet Size ($): " editable="true" id="rec-bet-size-number">$ ${row.bet_amount}</li>

      <li data-before="No Vig" id = "min-odds">${addSign(row.highest_acceptable_odds)}</li>

      <li data-before="Best" editable="true" id = "best-odds">${addSign(row.highest_bettable_odds)}</li>

      <li before-data="+EV%: " id="ev">${row.ev}%</li>

      <li before-data="Time Since Odds Update: " id="time-dif">
        <p id = "time-dif-formatted">${row.time_difference_formatted}</p>
      </li>

      <li class="desktop-no-display" id ="rec-bet-size-text">Rec Bet Size</li>
      <li before-data="Team: " id ="market" class="desktop-no-display" >${row.market_display} </li>
      <li before-data="Team: " id ="market" class="desktop-no-display" >${row.wager_display} </li>`


        // <li class="desktop-no-display" style="display:none;" id="team">${row.team}</li>
        // <li style="display:none;" id="sportsbooks-used">${row.sportsbooks_used}</li>
        ;
      table_row_to_append_to.appendChild(tr);

      const marketViewDiv = document.createElement("ul");

      marketViewDiv.classList.add("hidden");
      marketViewDiv.classList.add("market-view-div");

      marketViewDiv.appendChild(returnMarketView(row));

      table_row_to_append_to.appendChild(marketViewDiv);

      tr.addEventListener('click', toggleAllBooksView);

      getImage(row.sportsbooks_used, tr);
    });
  }
  else {
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
  // console.log(data);
  const footer_to_append_to = document.querySelector('.table-custom__footer');
  const footer_to_change_innerhtml = document.querySelector('.footer-to-make-innerhtml');
  footer_to_change_innerhtml.innerHTML = `<p>Showing ${data.length} Entries</p>`;

  const tableBody = document.querySelector('.table-custom__content');
  const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
  table_row_to_append_to.innerHTML = '';

  const tr = document.createElement('ul');

  boolin = true;


  if (!(data.length === 1 && data[0].update === false) && boolin) {
    const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
    table_row_to_append_to.innerHTML = '';

    var i = 0;

    data.forEach(row => {
      if (i == 0) {
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

      <li data-before="No Vig" id = "min-odds">${addSign(row.highest_acceptable_odds)}</li>

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
        i += 1;
      } else if (i == 1) {
        tr.innerHTML = `
  <li class="free-view-login-sign-up-container">
        <div class = "free-view-login-sign-up-buttons-container">
          <div class = "free-view-login-container"><a class = "free-view-login-button" href = "/login">Login</a></div>
          <div class = "or">or</div>
          <div class = "free-view-sign-up-container"><a class = "free-view-sign-up-button"href = "/register">Sign Up</a></div>
        </div>
      <div><p>This is a standard feature. Subscribe to see thousands of +EV bets refresh all day long.</p> <div>
  </li>
  `;
        footer_to_change_innerhtml.innerHTML = `<p>Showing 1 Entry</p>`;
        table_row_to_append_to.appendChild(tr);
        console.log('No update');
        i += 1;
      } else {
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
        i += 1;
      }
      footer_to_append_to.appendChild(footer_to_change_innerhtml);

    });

  }
  else {
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

function returnMarketView(data) {

  const sportsbooksForDisplay = ['betclic', 'betfair_ex_au', 'betfair_ex_eu', 'betfair_ex_uk', 'betfair_sb_uk', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betsson', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'livescorebet', 'livescorebet_eu', 'lowvig', 'marathonbet', 'matchbook', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'onexbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

  const sportsbooksAlreadyDisplayed = []

  const returnDiv = document.createElement("div");
  // returnDiv.classList.add('hidden');
  returnDiv.classList.add('market-view');


  const sportsbookRow = document.createElement("div");
  sportsbookRow.classList.add("all-books-view");
  // sportsbookRow.classList.add("mobile-no-display");

  const blank = document.createElement("div");
  blank.classList.add("blank");
  // blank.style.width = "10%";
  sportsbookRow.appendChild(blank);

  const bestOddsTitle = document.createElement("div");
  const bestOddsTitleValue = document.createElement("p");
  bestOddsTitle.appendChild(bestOddsTitleValue);
  bestOddsTitleValue.innerText = "Best Odds";
  bestOddsTitle.classList.add("market-view-best-odds-title");
  bestOddsTitle.classList.add("all-books-ind-logo");
  bestOddsTitle.classList.add("all-books-ind-value");


  // bestOddsTitle.style.width = "10%";

  const avgOddsTitle = document.createElement("div");
  const avgOddsTitleValue = document.createElement("p");
  avgOddsTitle.appendChild(avgOddsTitleValue);
  avgOddsTitleValue.innerText = "Avg Odds";
  avgOddsTitle.classList.add("market-view-best-odds-title");
  avgOddsTitle.classList.add("all-books-ind-logo");
  avgOddsTitle.classList.add("all-books-ind-value");


  // avgOddsTitle.style.width = "10%";

  sportsbookRow.appendChild(avgOddsTitle);
  sportsbookRow.appendChild(bestOddsTitle);


  const firstValuesRow = document.createElement("div");
  firstValuesRow.classList.add("all-books-view");
  // firstValuesRow.classList.add("mobile-no-display");
  const info_1 = blank.cloneNode(true);
  const info_1Value = document.createElement("p");
  info_1Value.textContent = data['wager_display']

  info_1.appendChild(info_1Value);
  firstValuesRow.appendChild(info_1);

  const secondValuesRow = document.createElement("div");
  secondValuesRow.classList.add("all-books-view");
  // secondValuesRow.classList.add("mobile-no-display");
  const info_2 = blank.cloneNode(true);
  const info_2Value = document.createElement("p");

  info_2Value.textContent = data['wager_display_other']
  info_2.appendChild(info_2Value);
  secondValuesRow.appendChild(info_2);

  const averageOddsDiv = document.createElement("div");
  averageOddsDiv.classList.add("all-books-ind-value");
  const averageOddsValue = document.createElement("div");
  var averageOddsDisplay = parseInt(decimalToAmerican(data['average_market_odds']));
  if (averageOddsDisplay < 0) {
    averageOddsValue.innerText = averageOddsDisplay;
  } else {
    averageOddsValue.innerText = "+" + averageOddsDisplay;
  }
  averageOddsDiv.appendChild(averageOddsValue);

  const bestOddsDiv = document.createElement("div");
  bestOddsDiv.classList.add("all-books-ind-value");

  const bestOddsValue = document.createElement("div");
  var bestOddsDisplay = parseInt(data['highest_bettable_odds']);
  if (bestOddsDisplay < 0) {
    bestOddsValue.innerText = bestOddsDisplay;
  } else {
    bestOddsValue.innerText = "+" + bestOddsDisplay;
  }

  bestOddsDiv.appendChild(bestOddsValue);

  firstValuesRow.appendChild(averageOddsDiv);
  firstValuesRow.appendChild(bestOddsDiv);


  const averageOddsDivOther = document.createElement("div");
  averageOddsDivOther.classList.add("all-books-ind-value");
  const averageOddsValueOther = document.createElement("div");
  if (parseInt(decimalToAmerican(data['other_average_market_odds'])) > 0) {
    averageOddsValueOther.innerText = "+" + parseInt(decimalToAmerican(data['other_average_market_odds']));
  } else {
    averageOddsValueOther.innerText = parseInt(decimalToAmerican(data['other_average_market_odds']));
  }

  averageOddsDivOther.appendChild(averageOddsValueOther);

  const bestOddsDivOther = document.createElement("div");
  bestOddsDivOther.classList.add("all-books-ind-value");

  const bestOddsValueOther = document.createElement("div");
  bestOddsValueOther.innerText = decimalToAmerican(data['highest_bettable_odds_other_X']);
  bestOddsDivOther.appendChild(bestOddsValueOther);

  secondValuesRow.appendChild(averageOddsDivOther);
  secondValuesRow.appendChild(bestOddsDivOther);


  for (const key in data) {

    if (data.hasOwnProperty(key) && (sportsbooksForDisplay.includes(key) | sportsbooksForDisplay.includes(key.split("_other_X")[0])) && data[key] > 1.01) {

      if (!sportsbooksAlreadyDisplayed.includes(key.split("_other_X")[0])) {


        sportsbooksAlreadyDisplayed.push(key.split("_other_X")[0]);

        sportsbookRow.appendChild(getImageSportsbookRow(key.split("_other_X")[0]));

        var valueDiv = document.createElement("div");
        var valueDivP = document.createElement("p");
        valueDiv.appendChild(valueDivP);

        var valueDiv2 = document.createElement("div");
        var valueDiv2P = document.createElement("p");
        valueDiv2.appendChild(valueDiv2P);

        valueDiv.classList.add(`${key}`);
        valueDiv2.classList.add(`${key}`);
        valueDiv.classList.add("all-books-ind-value");
        valueDiv2.classList.add("all-books-ind-value");


        valueDivP.innerText = '-'
        valueDiv2P.innerText = '-'

        firstValuesRow.appendChild(valueDiv);
        secondValuesRow.appendChild(valueDiv2);

      }

      if (key.includes("_other_X")) {
        valueDiv2P.textContent = decimalToAmerican(data[key]);
        secondValuesRow.appendChild(valueDiv2);
      } else {
        valueDivP.textContent = decimalToAmerican(data[key]);
        firstValuesRow.appendChild(valueDiv);
      }


    }


  }

  returnDiv.appendChild(sportsbookRow);
  returnDiv.appendChild(firstValuesRow);
  returnDiv.appendChild(secondValuesRow);



  return returnDiv

}

function decimalToAmerican(decimalOddsString) {

  var decimalOdds = parseFloat(decimalOddsString);

  if (decimalOdds < 2) {
    return Math.round((-100 / (decimalOdds - 1))).toString()
  } else {
    return "+" + Math.round((decimalOdds - 1) * 100).toString();
  }
}

function americanToDecimal(americanOddsString) {

  var americanOdds = parseInt(americanOddsString);

  if (americanOdds < 0) {
    return (100 / Math.abs(americanOdds)) + 1;
  } else {
    return ((americanOdds / 100) + 1);
  }
}


function returnSportsbookLogoDiv(data) {

  const sportsbooksForDisplay = ['betclic', 'betfair_ex_au', 'betfair_ex_eu', 'betfair_ex_uk', 'betfair_sb_uk', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betsson', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'livescorebet', 'livescorebet_eu', 'lowvig', 'marathonbet', 'matchbook', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'onexbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

  const rowDiv = document.createElement('div');

  rowDiv.classList.add("all-books-view");

  rowDiv.classList.add("hidden");

  rowDiv.classList.add("mobile-no-display");

  const sportsbooksAlreadyDisplayed = []

  for (const key in data) {

    if (data.hasOwnProperty(key) && (sportsbooksForDisplay.includes(key) | sportsbooksForDisplay.includes(key.split("_other_X"))) && data[key] > 1.01 && (!sportsbooksAlreadyDisplayed.includes(key.split("_other_X")[0]))) {

      sportsbooksAlreadyDisplayed.push(key.split("_other_X")[0]);

      const columnDiv_1 = document.createElement('div');

      const columnDiv = document.createElement('div');

      columnDiv_1.appendChild(columnDiv)

      columnDiv.appendChild(getImageSportsbookRow(key.split("_other_X")[0]))

      rowDiv.appendChild(columnDiv);

    }
  }





  return rowDiv;

}


function toggleAllBooksView() {

  const nextSibling = this.nextElementSibling;

  nextSibling.classList.toggle('hidden');

  this.classList.toggle("open");


  // Function that preloads all of the sportsbook logos

  // 

}


function createSportsBooksView(data) {
  const sportsbooksForDisplay = ['betclic', 'betfair_ex_au', 'betfair_ex_eu', 'betfair_ex_uk', 'betfair_sb_uk', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betsson', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'livescorebet', 'livescorebet_eu', 'lowvig', 'marathonbet', 'matchbook', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'onexbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

  const rowDiv = document.createElement('div');

  rowDiv.classList.add("all-books-view");

  rowDiv.classList.add("hidden");

  rowDiv.classList.add("mobile-no-display");

  const infoDiv = document.createElement('div');

  infoDiv.classList.add("sportsbook-view-info");

  const info1 = document.createElement('div');

  info1.classList.add("sportsbook-view-info-1");

  info1.textContent = `${data['market']}`

  const info2 = document.createElement('div');

  info2.classList.add("sportsbook-view-info-1");


  info2.textContent = `${data['wager_display']}`

  infoDiv.appendChild(info1);
  infoDiv.appendChild(info2);

  rowDiv.appendChild(infoDiv);

  for (const key in data) {
    if (data.hasOwnProperty(key) && sportsbooksForDisplay.includes(key) && data[key] > 1.01) {

      const columnDiv = document.createElement('div');
      columnDiv.classList.add("sportsbook-view-column");

      const Sportsbookdiv = document.createElement('div');
      const valueDiv = document.createElement('div');

      Sportsbookdiv.textContent = `${key}`;

      valueDiv.textContent = `${data[key]}`

      columnDiv.appendChild(Sportsbookdiv);
      columnDiv.appendChild(valueDiv);

      rowDiv.appendChild(columnDiv);
    }
  }
  return rowDiv;
}

function createSportsBooksViewOther(data) {
  const sportsbooksForDisplay = ['betclic', 'betfair_ex_au', 'betfair_ex_eu', 'betfair_ex_uk', 'betfair_sb_uk', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betsson', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'livescorebet', 'livescorebet_eu', 'lowvig', 'marathonbet', 'matchbook', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'onexbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

  const rowDiv = document.createElement('div');

  rowDiv.classList.add("all-books-view");

  rowDiv.classList.add("hidden");

  rowDiv.classList.add("mobile-no-display");

  const infoDiv = document.createElement('div');

  infoDiv.classList.add("sportsbook-view-info");

  const info1 = document.createElement('div');

  info1.classList.add("sportsbook-view-info-1");

  info1.textContent = `${data['market']}`

  const info2 = document.createElement('div');

  info2.classList.add("sportsbook-view-info-1");

  info2.textContent = `${data['wager_display_other']}`

  infoDiv.appendChild(info1);
  infoDiv.appendChild(info2);

  rowDiv.appendChild(infoDiv);

  for (const key in data) {
    if (
      data.hasOwnProperty(key) &&
      sportsbooksForDisplay.includes(key.split("_other_X")[0]) &&
      data[key] > 1.01 &&
      key.includes("_other_X")
    ) {
      const columnDiv = document.createElement('div');
      columnDiv.classList.add("sportsbook-view-column");

      const Sportsbookdiv = document.createElement('div');
      const valueDiv = document.createElement('div');

      Sportsbookdiv.textContent = `${key}`;

      valueDiv.textContent = `${data[key]}`

      columnDiv.appendChild(Sportsbookdiv);
      columnDiv.appendChild(valueDiv);

      rowDiv.appendChild(columnDiv);


    }
  }
  return rowDiv;
}

function updatebankroll(data) {
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
  const options = { timeZone: userTimezone, hour12: true, hour: 'numeric', minute: 'numeric', second: 'numeric' };
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
    success: function (response) {
      console.log(response.message); // Log the response from Flask
    },
    error: function (error) {
      console.error('Error adding bet to betslip:', error);
    }
  });
}

function resetRowView() {
  location.reload();
}

function saveRow(row) {
  var toggleButton = row.querySelector('.toggle-button');
  var modifiedNumber = toggleButton.innerText === "-" ? - + row.querySelector("#odds-taken-input").value : row.querySelector("#odds-taken-input").value;
  // make a dict with thte values of each cell in the right spot

  var rowDataDict = {
    'game_id': row.querySelector("#game-id").innerHTML,

    'average_market_odds': row.querySelector("#avg-market-odds").innerHTML,

    'team': row.querySelector("#team-bet-on").innerText.replace(/\n/g, ''),

    'sportsbooks_used': row.querySelector("#selected-option img").getAttribute('alt'),

    'bet_amount': row.querySelector("#bet-size-input").value,

    'highest_bettable_odds': modifiedNumber,

    'minimum_acceptable_odds': row.querySelector("#min-odds").innerHTML,

    'ev': row.querySelector("#ev").innerHTML.replace(/%/g, ''),

    'date': row.querySelector("#game-date").innerHTML,

    'time_difference_formatted': row.querySelector("#time-dif").innerHTML,
  }

  $.ajax({
    url: '/add_saved_bet',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(rowDataDict),
    success: function (response) {
      if (response.status_code === 'error') {
        console.log('Error saving bet:', response.message);
      } else {
        console.log('Bet saved successfully:', response.message);
        currentlyEditingRow = false;
        resetRowView();
      }
    },
    error: function (error) {
      console.error('Error saving bet:', error);
    }
  });
}

function displaySportsbookDropdown(row) {

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

function changeRowDisplay(row) {
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


function changePlusSignDisplay(row) {
  buttonLi = row.querySelector("#add-to-betslip-button");
  buttonLi.innerHTML = '';
  buttonEl = document.createElement('button');
  buttonEl.id = ("save-button");
  buttonEl.innerHTML = "Save"
  buttonEl.classList.add("adding-to-bet-tracker");
  buttonLi.appendChild(buttonEl);
  buttonLi.onclick = function () {
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


function getImage(sportsbook_string, row) {

  var imageContainer = row.querySelector('#sportsbook');

  imageContainer.classList.add("tooltip");

  var sportsbookP = document.createElement('p');

  sportsbookP.innerText = sportsbook_string;
  sportsbookP.classList.add("tooltiptext_img");
  imageContainer.appendChild(sportsbookP);

  // Check if the image container exists before setting its style
  if (imageContainer) {

    var imageDictionary = {
      'Unibet_Us': '/static/images/sportsbook_logos/unibet.png', 'Bovada': '/static/images/sportsbook_logos/bovada.png', 'Tipico_Us': '/static/images/sportsbook_logos/tipico.png', 'Livescore': '/static/images/sportsbook_logos/livescore.png', 'Matchbook': '/static/images/sportsbook_logos/matchbook.png', 'Betsson': '/static/images/sportsbook_logos/betsson.png', 'Sportsbet': '/static/images/sportsbook_logos/sportsbet.png', 'Fliff': '/static/images/sportsbook_logos/fliff.png', 'Fanduel': '/static/images/sportsbook_logos/fanduel.png', 'Playup': '/static/images/sportsbook_logos/playup.png', 'Windcreek': '/static/images/sportsbook_logos/windcreek.png', 'Twinspires': '/static/images/sportsbook_logos/twinspires.png', 'Pointsbet': '/static/images/sportsbook_logos/pointsbet.png', 'Coolbet': '/static/images/sportsbook_logos/coolbet.png', 'Suprabets': '/static/images/sportsbook_logos/suprabets.png', 'Neds': '/static/images/sportsbook_logos/neds.png', 'Virginbet': '/static/images/sportsbook_logos/virginbet.png', 'Betus': '/static/images/sportsbook_logos/betus.png', 'Betonlineag': '/static/images/sportsbook_logos/betonlineag.png', 'Mybookieag': '/static/images/sportsbook_logos/mybookie.png', 'Draftkings': '/static/images/sportsbook_logos/draftkings.png', 'Nordicbet': '/static/images/sportsbook_logos/nordicbet.png', 'Pinnacle': '/static/images/sportsbook_logos/pinnacle.png', 'Grosvenor': '/static/images/sportsbook_logos/grosvenor.png', 'Topsport': '/static/images/sportsbook_logos/topsport.png', 'Betmgm': '/static/images/sportsbook_logos/betmgm.png', 'Boyle': '/static/images/sportsbook_logos/boyle.png', 'Superbook': '/static/images/sportsbook_logos/superbook.png', 'Espnbet': '/static/images/sportsbook_logos/espnbet.png', 'Betvictor': '/static/images/sportsbook_logos/betvictor.png', '888Sport': '/static/images/sportsbook_logos/888sport.png', 'Wynnbet': '/static/images/sportsbook_logos/wynnbet.png', 'Betway': '/static/images/sportsbook_logos/betway.png', 'Casumo': '/static/images/sportsbook_logos/casumo.png', 'Betrivers': '/static/images/sportsbook_logos/betrivers.png', 'Betparx': '/static/images/sportsbook_logos/betparx.png', 'Betfair': '/static/images/sportsbook_logos/betfair.png', 'Everygame': '/static/images/sportsbook_logos/everygame.png', 'Marathonbet': '/static/images/sportsbook_logos/marathonbet.png', 'Williamhill_Us': '/static/images/sportsbook_logos/williamhill.png', 'Ladbrokes': '/static/images/sportsbook_logos/ladbrokes.png', 'Paddypower': '/static/images/sportsbook_logos/paddypower.png', 'Si_Sportbsook': '/static/images/sportsbook_logos/si_sportbsook.png', 'Leovegas': '/static/images/sportsbook_logos/leovegas.png', 'Coral': '/static/images/sportsbook_logos/coral.png', 'Betclic': '/static/images/sportsbook_logos/betclic.png', 'Bluebet': '/static/images/sportsbook_logos/bluebet.png', '1Xbet': '/static/images/sportsbook_logos/1xbet.png', 'Mrgreen': '/static/images/sportsbook_logos/mrgreen.png', 'Betr': '/static/images/sportsbook_logos/betr.png', 'Skybet': '/static/images/sportsbook_logos/skybet.png', 'Unibet_Eu': '/static/images/sportsbook_logos/unibet.png'
    }

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
        console.error('Image URL not found for: ', sportsbook, " in getImage");
      }
    });
  } else {
    console.error('Image container not found.');
  }
}

function getImageSportsbookRow(sportsbook_string) {

  var imageDictionary = {'unibet_us': '/static/images/sportsbook_logos/unibet.png', 'bovada': '/static/images/sportsbook_logos/bovada.png', 'tipico_us': '/static/images/sportsbook_logos/tipico.png', 'livescore': '/static/images/sportsbook_logos/livescore.png', 'matchbook': '/static/images/sportsbook_logos/matchbook.png', 'betsson': '/static/images/sportsbook_logos/betsson.png', 'sportsbet': '/static/images/sportsbook_logos/sportsbet.png', 'fliff': '/static/images/sportsbook_logos/fliff.png', 'fanduel': '/static/images/sportsbook_logos/fanduel.png', 'playup': '/static/images/sportsbook_logos/playup.png', 'windcreek': '/static/images/sportsbook_logos/windcreek.png', 'twinspires': '/static/images/sportsbook_logos/twinspires.png', 'pointsbetus': '/static/images/sportsbook_logos/pointsbet.png', 'coolbet': '/static/images/sportsbook_logos/coolbet.png', 'suprabets': '/static/images/sportsbook_logos/suprabets.png', 'neds': '/static/images/sportsbook_logos/neds.png', 'virginbet': '/static/images/sportsbook_logos/virginbet.png', 'betus': '/static/images/sportsbook_logos/betus.png', 'betonlineag': '/static/images/sportsbook_logos/betonlineag.png', 'mybookieag': '/static/images/sportsbook_logos/mybookie.png', 'draftkings': '/static/images/sportsbook_logos/draftkings.png', 'nordicbet': '/static/images/sportsbook_logos/nordicbet.png', 'pinnacle': '/static/images/sportsbook_logos/pinnacle.png', 'grosvenor': '/static/images/sportsbook_logos/grosvenor.png', 'topsport': '/static/images/sportsbook_logos/topsport.png', 'betmgm': '/static/images/sportsbook_logos/betmgm.png', 'boyle': '/static/images/sportsbook_logos/boyle.png', 'superbook': '/static/images/sportsbook_logos/superbook.png', 'espnbet': '/static/images/sportsbook_logos/espnbet.png', 'betvictor': '/static/images/sportsbook_logos/betvictor.png', '888sport': '/static/images/sportsbook_logos/888sport.png', 'wynnbet': '/static/images/sportsbook_logos/wynnbet.png', 'betway': '/static/images/sportsbook_logos/betway.png', 'casumo': '/static/images/sportsbook_logos/casumo.png', 'betrivers': '/static/images/sportsbook_logos/betrivers.png', 'betparx': '/static/images/sportsbook_logos/betparx.png', 'betfair': '/static/images/sportsbook_logos/betfair.png', 'everygame': '/static/images/sportsbook_logos/everygame.png', 'marathonbet': '/static/images/sportsbook_logos/marathonbet.png', 'williamhill_us': '/static/images/sportsbook_logos/williamhill.png', 'ladbrokes': '/static/images/sportsbook_logos/ladbrokes.png', 'paddypower': '/static/images/sportsbook_logos/paddypower.png', 'si_sportbsook': '/static/images/sportsbook_logos/si_sportbsook.png', 'leovegas': '/static/images/sportsbook_logos/leovegas.png', 'coral': '/static/images/sportsbook_logos/coral.png', 'betclic': '/static/images/sportsbook_logos/betclic.png', 'bluebet': '/static/images/sportsbook_logos/bluebet.png', '1xbet': '/static/images/sportsbook_logos/1xbet.png', 'mrgreen': '/static/images/sportsbook_logos/mrgreen.png', 'betr': '/static/images/sportsbook_logos/betr.png', 'skybet': '/static/images/sportsbook_logos/skybet.png', 'unibet_eu': '/static/images/sportsbook_logos/unibet.png'
};

  const div = document.createElement("div");
  div.classList.add("all-books-ind-logo")


  var imageUrl = imageDictionary[sportsbook_string];
  if (imageUrl) {
    var imgElement = document.createElement('img');
    imgElement.src = imageUrl;
    imgElement.alt = sportsbook_string;
    imgElement.height = 64;
    imgElement.width = 64;

    div.appendChild(imgElement);

    return div
  } else {
    console.error('Image URL not found for:', sportsbook_string, ' in getImageSportsbookRow');
    var imgElement = document.createElement('img');
    imgElement.height = 32;
    imgElement.width = 32;

    div.appendChild(imgElement);

    return div

  }
}


function fetchDataAndUpdateTable() {
  var activeElements = document.querySelectorAll('.filter-dropdown-item.active');
  var innerTextDictionary = {};

  activeElements.forEach(function (element) {
    var parentId = element.parentNode.id;
    var value = element.querySelector('.filter-value-content-a').innerText.trim();

    if (innerTextDictionary.hasOwnProperty(parentId)) {

      if (Array.isArray(innerTextDictionary[parentId])) {
        innerTextDictionary[parentId].push(value);
      } else {
        innerTextDictionary[parentId] = [innerTextDictionary[parentId], value];
      }
    } else {
      innerTextDictionary[parentId] = [value];
    }
  });


  var ascendingBool = null;

  try {

    var ascendingBool = document.querySelector('svg.active').parentNode.getAttribute("ascending");

    if (ascendingBool == null) {
      try {
        var ascendingBool = document.querySelector('svg.active').getAttribute("ascending");
        console.log(ascendingBool);
      } catch (error) {
        console.log(error);
      }
    }
  } catch (error) {
    console.log(error);
  }

  if (ascendingBool == null) {
    ascendingBool = false;
  } else if (ascendingBool == "true") {
    ascendingBool = true
  } else {
    ascendingBool = false
  }

  //Getting min and max values:
  //TODO: Add an active thing so you can tell which is selected
  try {
    var minOddsInput = document.getElementById('min-odds-input').value.trim();
    var maxOddsInput = document.getElementById('max-odds-input').value.trim();
    innerTextDictionary['best-odds-filter'] = { 'minodds': minOddsInput, 'maxodds': maxOddsInput };

  } catch (error) {
    console.log(error);
  }

  try {
    innerTextDictionary['sort-by'] = [document.querySelector('svg.sort-icon.active').getAttribute("id"), ascendingBool];
  } catch (error) {
    innerTextDictionary['sort-by'] = ['ev', ascendingBool];
  }

  //finding the things that are active:
  // Get the last segment (element) of the URL
  const url = '/get_positive_ev_dash_data?';

  const table_row_to_append_to = document.querySelector('.table-custom__content__rows')
  table_row_to_append_to.innerHTML = '';
  const tr = document.createElement('ul');

  tr.classList.add('table-custom__content__rows__row');

  var objectElement = document.createElement('img');

  objectElement.src = '/static/images/ring-resize.svg';

  tr.innerHTML = '<li class="centered"><img src="/static/images/ring-resize.svg"></li>';

  table_row_to_append_to.appendChild(tr);

  fetchDataWithRetry(url, innerTextDictionary)
    .then(data => {
      if (userPermissionVar == 'standard' || userPermissionVar == 'premium' || userPermissionVar == 'ev') {
        updateTable(data);
      } else {
        updateTableFree(data);
      }
    })
    .catch(error => console.error('Error fetching data with retry:', error));

}

function fetchDataWithRetry(url, innerTextDictionary, retryLimit = 3) {
  return new Promise((resolve, reject) => {
    const fetchData = (retryCount) => {
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: innerTextDictionary }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          resolve(data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          if (retryCount > 0) {
            console.log(`Retrying... ${retryCount} retries left.`);
            fetchData(retryCount - 1);
          } else {
            reject(new Error('Retry limit exceeded'));
          }
        });
    };

    fetchData(retryLimit);
  });
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

  saveButton.addEventListener("click", function () {
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

function toggleSport() {
  var currentURL = window.location.href;

  var urlSegments = currentURL.split('/');

  var targetSport = urlSegments[urlSegments.length - 1];

  var elements = document.querySelectorAll('[data-sport="' + targetSport + '"]');

  if (elements.length > 0) {
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

function greenIfFiltered(event) {
  var filterSVG = findCousinWithClass(event.target, 'dropbtn');

  if (filterSVG && event.target.innerText !== 'ALL') {
    var paths = filterSVG.querySelectorAll('path');
    paths.forEach(function (path) {
      path.style.fill = '#21ce99';
    })
  }
  else if (filterSVG && event.target.innerText == 'ALL') {
    var paths = filterSVG.querySelectorAll('path');
    paths.forEach(function (path) {
      path.style.fill = 'var(--table-thead-color)';
    });

  }
}

function makeSingleFilterValue(value) {
  return `
  <label class="custom-checkbox">
    <input type="checkbox">
      <span class="checkmark"></span>
      <a class = "filter-value-content-a">
        ${value.toUpperCase()}
      </a>
  </label>`
}

function fillFilterValues(callback1, callback2) {

  // for the ones where you can select 
  fetch('/get_filter_dropdown_values', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(response => response.json())
    .then(data => {
      var sportLeagueFilterDiv = document.getElementById("sport-league-filter");
      data['sport_league_display'].forEach(function (league) {
        var filterValue = document.createElement('div');
        filterValue.classList.add("filter-dropdown-item");
        filterValue.innerHTML = makeSingleFilterValue(league);
        sportLeagueFilterDiv.appendChild(filterValue);
      })

      var sportLeagueFilterDiv = document.getElementById("market-filter");
      data['market_display'].forEach(function (league) {
        var filterValue = document.createElement('div');
        filterValue.classList.add("filter-dropdown-item");
        filterValue.innerHTML = makeSingleFilterValue(league);
        sportLeagueFilterDiv.appendChild(filterValue);
      })

      var sportLeagueFilterDiv = document.getElementById("sportsbook-filter");

      data['sportsbooks_used'].forEach(function (league) {
        console.log(league);
        var filterValue = document.createElement('div');
        filterValue.classList.add("filter-dropdown-item");
        filterValue.innerHTML = makeSingleFilterValue(league);

        sportLeagueFilterDiv.appendChild(filterValue);
      })

      callback1()
      callback2()

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
      console.log(response)
      return response.json();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      throw error; // Re-throw the error to handle it outside this function if needed
    });
}

function makeSlideResponsive() {
  const leftBox = document.getElementById("full-filter");
  const rightBox = document.querySelectorAll(".table-custom")[0];
  function handleTouchStart(event) {
    startX = event.touches[0].clientX;
  }
  function handleTouchMove(event) {
    const currentX = event.touches[0].clientX;
    const diffX = currentX - startX;
    if (diffX < -50) {
      rightBox.classList.remove('table-hidden');
      leftBox.style.transition = 'transform 0.3s ease';
      leftBox.style.transform = 'translateX(-100%)';
      rightBox.style.transition = 'flex-grow 0.3s ease';
      rightBox.style.flexGrow = '100';
    }
  }

  function handleTouchEnd() {
    leftBox.addEventListener('transitionend', function () {
      leftBox.style.transition = '';
      leftBox.style.transform = '';
      leftBox.classList.add('hidden');

      rightBox.style.transition = 'flex-grow 1.3s ease';
    }, { once: true });
    rightBox.addEventListener('transitionend', function () {

      rightBox.style.transition = '';
      rightBox.style.flexGrow = '';
    }, { once: true });
  }
  leftBox.addEventListener('touchstart', handleTouchStart);
  leftBox.addEventListener('touchmove', handleTouchMove);
  leftBox.addEventListener('touchend', handleTouchEnd);

}

function showFilter() {
  if (!document.querySelector('.sort-by-content').classList.contains("mobile-hidden")) {
    document.querySelector('.sort-by-content').classList.add("mobile-hidden");
  }

  document.getElementById('footer').classList.toggle('mobile-hidden');

  document.querySelector('.navbar-custom').classList.toggle("mobile-hidden");

  var allFiltersDiv = document.getElementById('full-filter');
  var tableCustom = document.querySelector('.table-custom__wrapper');
  allFiltersDiv.classList.toggle('mobile-hidden');
  tableCustom.classList.toggle('table-hidden');

  var sortByButtonMobile = document.querySelector('.sort-by-button-mobile');
  var filterButtonMobile = document.querySelector('.filter-button-mobile');
  sortByButtonMobile.classList.toggle("mobile-hidden");
  filterButtonMobile.classList.toggle("mobile-hidden");

  var filterValues = document.querySelectorAll('.full-filter-ind-content-values');

  filterValues.forEach(function (filter) {
    filter.classList.remove('hidden');
  })

  var evDashHeader = document.getElementById("ev-dash-header");

  var tableheader = document.querySelector(".table-custom__header");
  document.querySelector(".table-custom__wrapper").classList.toggle("hidden");

  tableheader.classList.add("fixed");

  evDashHeader.classList.add("fixed");

  evDashHeader.querySelector('.ev-dash-title').classList.toggle('hidden');

  var newH2 = document.querySelector('.ev-dash-filters-title');

  newH2.classList.toggle("mobile-hidden");

  evDashHeader.classList.toggle("centered-2");

  document.getElementById('min-odds-input').placeholder = "Min, i.e. -300";

  document.getElementById('max-odds-input').placeholder = "Max, i.e. +200";
}

function adjustLayout() {

  const screenWidth = window.innerWidth;

  if (screenWidth < 768) {
    var desktopFilterButton = document.getElementById('all-filters-button-div-li');

    var evDashHeader = document.getElementById("ev-dash-header");

    evDashHeader.appendChild(desktopFilterButton);

    filterSVG = desktopFilterButton.querySelector("svg");

    filterSVG.querySelector("path").style.fill = "var(--table-btn-bg)"

    filterSVG.setAttribute('transform', 'scale(2)');

  }
}

function deselectAllAndKeepSelected(checkbox) {

  var elements = checkbox.parentNode.parentNode.parentNode.querySelectorAll('.filter-dropdown-item.active');

  var searchString = 'ALL';

  if (checkbox.parentNode.querySelector('a').innerText.trim().toUpperCase() == "ALL") {
    elements.forEach(function (element) {

      element.querySelector('input[type="checkbox"]').click();

    });
  }

  elements.forEach(function (element) {
    if (element.innerText.trim().toUpperCase() === searchString) {
      element.querySelector('input[type="checkbox"]').click();
    }
  });

}

function clearFilter() {

  this.parentNode.querySelector('.filter-dropdown-button').innerText = ">";

  var lookingForContentDivToClose = this.parentNode.parentNode.querySelector('.full-filter-ind-content-values');

  if (!lookingForContentDivToClose.classList.contains('hidden')) {
    lookingForContentDivToClose.classList.add('hidden');
  }

  var values = this.parentNode.parentNode.querySelectorAll('.filter-dropdown-item');

  values.forEach(function (value) {
    if (value.classList.contains('active')) {
      value.querySelector('input[type="checkbox"]').click();
    }
  });

  var inputs = this.parentNode.parentNode.querySelectorAll('input[type="text"]');
  if (inputs.length > 0) {
    inputs.forEach(function (input) {
      input.value = '';
      fetchDataAndUpdateTable();
    });
  }

}

function addDropdownListeners() {
  var dropdownButtons = document.querySelectorAll('.full-filter-ind-content-title');

  dropdownButtons.forEach(btn => {
    btn.addEventListener('click', showDropdown)
  });

  var checkboxes = document.querySelectorAll('input[type="checkbox"]');

  checkboxes.forEach(function (checkbox) {
    if (!checkbox.hasEventListener) {
      checkbox.addEventListener('click', function () {
        checkbox.parentNode.parentNode.classList.toggle("active");
        var selectedCount = checkbox.parentNode.parentNode.parentNode.querySelectorAll('.active').length;
        checkbox.parentNode.parentNode.parentNode.parentNode.querySelector('.amount-selected a').innerText = selectedCount;
        deselectAllAndKeepSelected(checkbox);
        fetchDataAndUpdateTable();
      });
      checkbox.hasEventListener = true;
    }
  });


  var oddsInput = document.querySelectorAll('input[type="text"]');

  oddsInput.forEach(function (input) {
    if (!input.hasEventListener) {
      input.addEventListener('click', function () {
        input.parentNode.parentNode.classList.toggle("active");
      });
      input.hasEventListener = true;
    }

  });

  var clearFilterButtons = document.querySelectorAll('.filter-dropdown-button-close');

  clearFilterButtons.forEach(function (button) {
    button.addEventListener('click', clearFilter);
  });

  document.querySelector('.filter-button-mobile').addEventListener('click', showFilter);

}

function showDropdown(event) {

  var oddsCloseButton = event.target.closest('.full-filter-ind-content').querySelector('.filter-dropdown-button-close');

  if (oddsCloseButton.classList.contains('hidden')) {
    oddsCloseButton.classList.toggle('hidden');
  }

  if (!event.target.classList.contains('filter-dropdown-button-close')) {
    var parentNode = this.parentNode;

    var dropdownOptionsDiv = parentNode.querySelector('.full-filter-ind-content-values');

    dropdownOptionsDiv.classList.toggle('hidden');

    if (this.parentNode.querySelector('.filter-dropdown-button').innerText == ">") {

      this.parentNode.querySelector('.filter-dropdown-button').innerText = "<"

    } else {
      this.parentNode.querySelector('.filter-dropdown-button').innerText = ">"
    }

  } else {
    event.target.classList.toggle('hidden');
  }




}

function addDynamicOddsInputDisplayFunction() {
  var minOddsInput = document.getElementById('min-odds-input');
  var minOddsSelected = document.getElementById('min-odds-selected');
  minOddsInput.addEventListener('input', function () {
    if (minOddsInput.value.trim() !== '') {
      minOddsSelected.innerText = minOddsInput.value.trim();
    } else {
      minOddsSelected.innerText = minOddsInput.value.trim();
    }
    if (minOddsInput.value[0] == '-') {
      var lengthRequired = 4;
    } else {
      var lengthRequired = 3;
    }

    if (minOddsInput.value.length >= lengthRequired) {
      fetchDataAndUpdateTable();
    }
  });

  var maxOddsInput = document.getElementById('max-odds-input');
  var maxOddsSelected = document.getElementById('max-odds-selected');

  maxOddsInput.addEventListener('input', function () {
    if (maxOddsInput.value.trim() !== '') {
      maxOddsSelected.innerText = maxOddsInput.value.trim();
    }
    if (maxOddsInput.value[0] == '-') {
      var lengthRequired = 4;
    } else {
      var lengthRequired = 3;
    }
    if (maxOddsInput.value.length >= lengthRequired) {
      fetchDataAndUpdateTable();
    }
  });
}

function returnAscendingSvg() {
  return `<svg
  width="14"
  height="11"
  viewBox="0 0 0.42 0.33"
  fill="none"
  version="1.1"
  id="svg6"
  sodipodi:docname="ascending.svg"
  inkscape:version="1.3 (0e150ed, 2023-07-21)"
  xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
  xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
  xmlns="http://www.w3.org/2000/svg"
  xmlns:svg="http://www.w3.org/2000/svg">
 <defs
    id="defs6" />
 <sodipodi:namedview
    id="namedview6"
    pagecolor="#ffffff"
    bordercolor="#000000"
    borderopacity="0.25"
    inkscape:showpageshadow="2"
    inkscape:pageopacity="0.0"
    inkscape:pagecheckerboard="0"
    inkscape:deskcolor="#d1d1d1"
    showguides="false"
    inkscape:zoom="16.257958"
    inkscape:cx="6.4583757"
    inkscape:cy="3.6289921"
    inkscape:window-width="1312"
    inkscape:window-height="449"
    inkscape:window-x="0"
    inkscape:window-y="25"
    inkscape:window-maximized="0"
    inkscape:current-layer="svg6" />
 <path
    d="m 0.14208306,0.08560364 c -0.004537,0 -0.009075,-0.0014616 -0.0126565,-0.0045939 L 0.08238282,0.03987839 0.03533906,0.08100976 c -0.0069247,0.0060544 -0.01838768,0.0060544 -0.02531285,0 -0.00692467,-0.0060544 -0.00692467,-0.01607674 0,-0.02213156 L 0.06972634,0.0066811 c 0.0069247,-0.006054386 0.01838767,-0.006054386 0.02531284,0 L 0.1547393,0.0588782 c 0.006925,0.0060544 0.006925,0.01607674 0,0.02213156 -0.003583,0.0031323 -0.008119,0.0045939 -0.0126562,0.0045939 z"
    fill="#000000"
    id="path1"
    style="stroke-width:0.0223291" />
 <path
    d="m 0.08238288,0.32571177 c -0.009791,0 -0.01791009,-0.007099 -0.01791009,-0.0156592 V 0.01774859 c 0,-0.00856043 0.0081193,-0.01565917 0.01791009,-0.01565917 0.0097909,0 0.01791009,0.00709885 0.01791009,0.01565917 v 0.29230404 c 0,0.00856 -0.0081193,0.0156592 -0.01791009,0.0156591 z"
    fill="#000000"
    id="path2"
    style="stroke-width:0.0223291" />
 <path
    d="M 0.40476383,0.08560489 H 0.21372327 c -0.009791,0 -0.0179101,-0.0070989 -0.0179101,-0.01565917 0,-0.0085604 0.008119,-0.01565918 0.0179101,-0.01565918 h 0.19104056 c 0.009791,0 0.0179101,0.0070988 0.0179101,0.01565918 0,0.0085604 -0.008119,0.01565917 -0.0179101,0.01565917 z"
    fill="#000000"
    id="path3"
    style="stroke-width:0.0223291" />
 <path
    d="m 0.30924355,0.21087805 h -0.0955203 c -0.009791,0 -0.0179101,-0.007099 -0.0179101,-0.0156592 0,-0.00856 0.008119,-0.0156592 0.0179101,-0.0156592 h 0.0955203 c 0.009791,0 0.0179101,0.007099 0.0179101,0.0156592 0,0.00856 -0.008119,0.0156592 -0.0179101,0.0156592 z"
    fill="#000000"
    id="path4"
    style="stroke-width:0.0223291" />
 <path
    d="M 0.2614834,0.27351463 H 0.2137233 c -0.009791,0 -0.0179101,-0.007099 -0.0179101,-0.0156592 0,-0.00856 0.008119,-0.0156592 0.0179101,-0.0156592 h 0.0477601 c 0.009791,0 0.0179101,0.007099 0.0179101,0.0156592 0,0.00856 -0.008119,0.0156592 -0.0179101,0.0156592 z"
    fill="#000000"
    id="path5"
    style="stroke-width:0.0223291" />
 <path
    d="M 0.35700368,0.14824147 H 0.21372327 c -0.009791,0 -0.0179101,-0.007099 -0.0179101,-0.0156592 0,-0.00856 0.008119,-0.0156592 0.0179101,-0.0156592 h 0.14328041 c 0.009791,0 0.0179101,0.007099 0.0179101,0.0156592 0,0.00856 -0.008119,0.0156592 -0.0179101,0.0156592 z"
    fill="#000000"
    id="path6"
    style="stroke-width:0.0223291" />
</svg>
`
}


function addSortListenersDesktop() {

  var svgs = document.querySelectorAll('.sort-icon');

  svgs.forEach(function (svg) {

    svg.setAttribute('ascending', false);

    svg.addEventListener('click', function () {

      // See if this one is ascending and active
      var isAscending = this.getAttribute('ascending');
      var isActive = this.classList.contains('active');

      // Turn all others to inactive
      svgs.forEach(function (s) {
        s.classList.remove('active');
        s.setAttribute('ascending', 'false');
        s.querySelector('#path6').setAttribute('d', "M 5.8192143,4.1580783 5.6812692,4.0201331 c -0.036579,-0.036579 -0.086208,-0.057141 -0.1379452,-0.057141 -0.051737,0 -0.1013666,0.020562 -0.1379647,0.057141 L 4.7344007,4.6910917 v -4.398463 c 0,-0.10774588 -0.08734,-0.1950858 -0.1950858,-0.1950858 H 4.3442291 c -0.1077459,0 -0.1950858,0.08733992 -0.1950858,0.1950858 V 4.6910722 L 3.4781847,4.0201136 c -0.036598,-0.036579 -0.086208,-0.057141 -0.1379451,-0.057141 -0.051737,0 -0.1013666,0.020562 -0.1379452,0.057141 L 3.0643297,4.1580587 c -0.076161,0.076181 -0.076161,0.1997094 0,0.2758904 l 1.2394972,1.2394971 c 0.0381,0.0381 0.088023,0.057141 0.1379451,0.057141 0.049923,0 0.099864,-0.01904 0.1379452,-0.057141 L 5.8192143,4.4339491 c 0.076181,-0.076181 0.076181,-0.1997093 0,-0.2758708 z");
      })

      // Turn this one active 
      this.classList.add('active');

      if (isActive && isAscending === 'true') {
        this.setAttribute('ascending', 'false');
        this.querySelector('#path6').setAttribute('d', "M 5.8192143,4.1580783 5.6812692,4.0201331 c -0.036579,-0.036579 -0.086208,-0.057141 -0.1379452,-0.057141 -0.051737,0 -0.1013666,0.020562 -0.1379647,0.057141 L 4.7344007,4.6910917 v -4.398463 c 0,-0.10774588 -0.08734,-0.1950858 -0.1950858,-0.1950858 H 4.3442291 c -0.1077459,0 -0.1950858,0.08733992 -0.1950858,0.1950858 V 4.6910722 L 3.4781847,4.0201136 c -0.036598,-0.036579 -0.086208,-0.057141 -0.1379451,-0.057141 -0.051737,0 -0.1013666,0.020562 -0.1379452,0.057141 L 3.0643297,4.1580587 c -0.076161,0.076181 -0.076161,0.1997094 0,0.2758904 l 1.2394972,1.2394971 c 0.0381,0.0381 0.088023,0.057141 0.1379451,0.057141 0.049923,0 0.099864,-0.01904 0.1379452,-0.057141 L 5.8192143,4.4339491 c 0.076181,-0.076181 0.076181,-0.1997093 0,-0.2758708 z");
      }

      else if (isActive && isAscending === 'false') {
        this.setAttribute('ascending', 'true');
        this.querySelector('#path6').setAttribute('d', "M 5.8192143,1.6700518 5.6812692,1.807997 C 5.6446902,1.844576 5.5950612,1.865138 5.543324,1.865138 5.491587,1.865138 5.4419574,1.844576 5.4053593,1.807997 L 4.7344007,1.1370384 v 4.398463 c 0,0.1077459 -0.08734,0.1950858 -0.1950858,0.1950858 H 4.3442291 c -0.1077459,0 -0.1950858,-0.08734 -0.1950858,-0.1950858 V 1.1370579 L 3.4781847,1.8080165 c -0.036598,0.036579 -0.086208,0.057141 -0.1379451,0.057141 -0.051737,0 -0.1013666,-0.020562 -0.1379452,-0.057141 L 3.0643297,1.6700714 c -0.076161,-0.076181 -0.076161,-0.1997094 0,-0.2758904 L 4.3038269,0.1546839 c 0.0381,-0.0381 0.088023,-0.057141 0.1379451,-0.057141 0.049923,0 0.099864,0.01904 0.1379452,0.057141 L 5.8192143,1.394181 c 0.076181,0.076181 0.076181,0.1997093 0,0.2758708 z");
      }
      fetchDataAndUpdateTable()
    });

  });


}

function clearAllFilters() {
  var filterDropdownItems = document.querySelectorAll('.filter-dropdown-item');

  filterDropdownItems.forEach(function (filterItem) {
    if (filterItem.classList.contains("active")) {
      filterItem.querySelector('label').click();
    }
  })

  document.getElementById('min-odds-input').value = "";
  document.getElementById('max-odds-input').value = "";

  fetchDataAndUpdateTable();

}

function hideFilter() {

  document.getElementById("full-filter").classList.toggle("mobile-hidden");

  document.querySelector('.navbar-custom').classList.toggle('mobile-hidden');

  document.getElementById('footer').classList.toggle('mobile-hidden');


  document.querySelector('.table-custom__wrapper').classList.toggle("table-hidden");

  var sortByButtonMobile = document.querySelector('.sort-by-button-mobile');
  var filterButtonMobile = document.querySelector('.filter-button-mobile');
  sortByButtonMobile.classList.toggle("mobile-hidden");
  filterButtonMobile.classList.toggle("mobile-hidden");

  var evDashHeader = document.getElementById("ev-dash-header");

  var tableheader = document.querySelector(".table-custom__header");
  document.querySelector(".table-custom__wrapper").classList.toggle("hidden");

  tableheader.classList.remove("fixed");

  evDashHeader.classList.remove("fixed");

  evDashHeader.querySelector('.ev-dash-title').classList.toggle('hidden');

  var newH2 = document.querySelector('.ev-dash-filters-title');

  newH2.classList.toggle("mobile-hidden");

  evDashHeader.classList.toggle("centered-2");


}

function addMobileCloseListeners() {
  document.querySelector('.done-div-clear-all-button').addEventListener('click', clearAllFilters);

  document.querySelector('.done-div-done-button').addEventListener('click', hideFilter);

}

function addSortByDiv() {

  var sortIcons = document.querySelectorAll('.sort-icon');

  sortIcons.forEach(function (icon) {

    var newValAscending = icon.parentNode.cloneNode(true);

    var newValDescending = icon.parentNode.cloneNode(true);

    if (!newValAscending.innerText.toUpperCase().includes("MIN.")) {

      newValAscending.setAttribute('ascending', true);
      newValDescending.setAttribute('ascending', false);

      if (!newValAscending.querySelector('svg').classList.contains('mobile-hidden')) {
        newValAscending.querySelector('svg').classList.add('mobile-hidden');
        newValDescending.querySelector('svg').classList.add('mobile-hidden');
      }

      if (!newValAscending.classList.contains('sort-by-filter-container-2')) {
        newValAscending.classList.add('sort-by-filter-container-2');
        newValDescending.classList.add('sort-by-filter-container-2');
        newValDescending.classList.add('filter-value-content-b');
        newValAscending.classList.add('filter-value-content-b');
      }


      var text = newValAscending.innerText;

      var formattedText = text.toLowerCase().replace(/(?:^|\s)\w/g, function (match) {
        return match.toUpperCase();
      });

      newValAscending.innerText = formattedText;

      newValDescending.innerText = formattedText;

      newValAscending.innerText += "(Low to High)";

      newValDescending.innerText += "(High to Low)";

      var clonedIcon = icon.cloneNode(true);
      clonedIcon.classList.add("mobile-hidden");
      newValAscending.appendChild(clonedIcon);

      clonedIcon = icon.cloneNode(true);
      clonedIcon.classList.add("mobile-hidden");
      newValDescending.appendChild(clonedIcon);

      if (!(newValAscending.querySelector('svg').id === "bet_amount" && newValAscending.getAttribute("ascending") === "true") &&
        !(newValAscending.querySelector('svg').id === "ev" && newValAscending.getAttribute("ascending") === "true")) {
        document.querySelector('.sort-by-content').appendChild(newValAscending);
        newValAscending.appendChild(clonedIcon);
      }

      if ((newValAscending.querySelector('svg').id === "highest_bettable_odds" && newValAscending.getAttribute("ascending") === "true")) {
        newValAscending.innerText = "Odds: Low to High";
        newValDescending.innerText = "Odds: High to Low";
        newValAscending.appendChild(clonedIcon);
        newValDescending.appendChild(clonedIcon);
      }

      if ((newValDescending.querySelector('svg').id === "bet_amount" && newValDescending.getAttribute("ascending") === "false")) {
        newValDescending.innerText = "Best Bets";
        newValDescending.appendChild(clonedIcon);
      }

      try {
        if (newValDescending.querySelector('svg').id === "ev") {
          newValDescending.innerText = "%+EV";
          newValDescending.appendChild(clonedIcon);

        }
      } catch (error) { }

      clonedIcon = icon.cloneNode(true);
      clonedIcon.classList.add("mobile-hidden");
      newValAscending.appendChild(clonedIcon);

      clonedIcon = icon.cloneNode(true);
      clonedIcon.classList.add("mobile-hidden");
      newValDescending.appendChild(clonedIcon);

      document.querySelector('.sort-by-content').appendChild(newValDescending);

      var brElements = newValDescending.querySelectorAll('br');

      brElements.forEach(function (brElement) {
        brElement.parentNode.removeChild(brElement);
      });

      brElements = newValAscending.querySelectorAll('br');
      brElements.forEach(function (brElement) {
        brElement.parentNode.removeChild(brElement);
      });

      newValAscending.addEventListener('click', function () {
        var activeElements = document.querySelectorAll("svg.active");
        activeElements.forEach(function (icon) {
          icon.classList.remove('active');
          icon.parentNode.classList.remove("green");
        });
        this.querySelector('svg').classList.add('active');
        this.classList.add("green");
        showSortBy();
        fetchDataAndUpdateTable();
      });

      newValDescending.addEventListener('click', function () {
        var activeElements = document.querySelectorAll("svg.active");
        activeElements.forEach(function (icon) {
          icon.classList.remove('active');
          icon.parentNode.classList.remove("green");

        });
        this.querySelector('svg').classList.add('active');
        this.classList.add("green");
        showSortBy();
        fetchDataAndUpdateTable();
      });

    }

  });

  document.querySelectorAll("svg.active").forEach(function (svg) {
    svg.classList.remove('active');
  })

  var elementsWithSameId = document.querySelectorAll('#bet_amount');

  elementsWithSameId.forEach(function (element) {
    try {
      if (element.parentNode.getAttribute('ascending') === 'false') {
        element.classList.add('active');
      }
      else {
        element.remove();
      }
    }
    catch (error) {
      element.remove();
    }

  });


}

function showSortBy() {
  document.querySelector('.sort-by-content').classList.toggle('mobile-hidden');
  document.querySelector('.table-custom__wrapper').classList.toggle('mobile-hidden');
  if (document.querySelector('.sort-by-button-mobile a').innerText == ">") {
    document.querySelector('.sort-by-button-mobile a').innerText = "<";
  } else {
    document.querySelector('.sort-by-button-mobile a').innerText = ">";
  }
}

function addSortListenersMobile() {
  addSortByDiv();
  document.querySelector('.sort-by-button-mobile').addEventListener("click", showSortBy)
}

function addWholePageClickListenerToCloseActiveDropdowns() {

  function getLengthOfClassWithoutAnotherClass(className) {

    const elements = document.querySelectorAll('.' + className);

    let count = 0;

    elements.forEach(function (element) {
      if (!element.classList.contains('hidden')) {
        count++;
      }
    });
    return count;
  }


  function handleClick(event) {
    // Checks to see if we have an open filter div 
    if (getLengthOfClassWithoutAnotherClass('full-filter-ind-content-values') > 0) {
      // if we do, check if we're clicking in that filter div
      const clickedElement = event.target;

      if (clickedElement.closest('.full-filter-ind-content-values') || clickedElement.closest('.full-filter-ind-content-title')) {
        return;
      }


      document.querySelectorAll('.full-filter-ind-content-values').forEach(function (element) {
        if (!element.classList.contains('hidden')) {
          element.parentNode.querySelector('.filter-dropdown-button').click();
        }
      });
    }
    return
  }

  document.addEventListener('click', handleClick);
}


$(document).ready(function () {

  const menuIcon = document.querySelector(".navbar-custom__left i");
  const closeIcon = document.querySelector(".sidebar-custom .close-icon");
  const logo = document.querySelector(".sidebar-custom__logo img");
  menuIcon.addEventListener("click", (e) => {
    document.querySelector(".sidebar-custom").classList.toggle("active");
  });

  closeIcon.addEventListener("click", (e) => {
    document.querySelector(".sidebar-custom").classList.remove("active");
  });

  const systemSettingDark = window.matchMedia("(prefers-color-scheme: dark)");

  toggleSport();

  if (window.innerWidth <= 768) {
    addSortListenersMobile();
  } else {
    addSortListenersDesktop();
    addWholePageClickListenerToCloseActiveDropdowns();

  }

  fillFilterValues(addDropdownListeners, addMobileCloseListeners);

  addDynamicOddsInputDisplayFunction();



  // addDesktopSortListeners();

  // addMobileCloseListeners();

  // makeSlideResponsive();

  // window.addEventListener('resize', adjustLayout);

  // adjustLayout();

  //


  /** 
 * 5. Add an event listener to update table and bankroll
 */
  document.getElementById('fetch-button').addEventListener('click', fetchDataAndUpdateTable);

  getUserPermission()
    .then(userPermission => {
      userPermissionVar = userPermission.permission;
      console.log(userPermissionVar);
      fetchDataAndUpdateTable();
    })
    .catch(error => {
      console.log(error);
    });

});

