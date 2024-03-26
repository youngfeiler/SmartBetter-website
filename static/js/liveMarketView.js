var allData;

var leagueDisplayDict = {
    basketball_nba: 'NBA',
    basketball_ncaab: 'NCAAB',
};

function decimalToAmerican(decimalOddsString) {


    var decimalOdds = parseFloat(decimalOddsString);

    if (decimalOdds == 0) {
        return "-"
    }
    else if (decimalOdds < 2) {
      return Math.round((-100 / (decimalOdds - 1))).toString()
    } 
    else{
      return "+" + Math.round((decimalOdds - 1) * 100).toString();
    }
}

function doesElementExistWithId(id) {
    return document.getElementById(id) !== null;
}

function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}

function initialLoadData() {
    fetch('/load_initial_market_view_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            allData = data;
            document.getElementById('data-list').innerHTML = '';

            fillFilterValues(data);
            fillHeader(data);
            addData(data);

        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function addData(data) {

    var activeSportValue = document.getElementById('sport-league-filter').querySelector('.active').querySelector('a').innerText

    let activeSport = getKeyByValue(leagueDisplayDict, activeSportValue);

    let activeMarket = document.getElementById('market-filter').querySelector('.active').querySelector('a').innerText;

    var filteredData = data.filter(function (item) {
        return item.sport_title === activeSport && item.market_reduced === activeMarket;
    });


    let rowCounter = 0;
    var isFirst = false;

    if (filteredData.length != 0) {
    console.log("adding data");


    console.log(filteredData);


        filteredData.forEach(function (row) {

            rowCounter += 1;

            // Make a new div that will contain all of the odds
            const oddsContainer = document.createElement('div');
            const oddsDiv1 = document.createElement('div');
            const oddsDiv2 = document.createElement('div');

            oddsContainer.classList.add("odds-container");
            oddsDiv1.classList.add("odds-row");
            oddsDiv2.classList.add("odds-row");

            var counter = 0;

            for (var columnName in row) {

                counter++;

                if (counter >= 26 && counter <= 88) {
                    var oddsValueContainer = document.createElement('div');
                    oddsValueContainer.classList.add(columnName);
                    var oddsValue = decimalToAmerican(row[columnName]);
                    var oddsValueP = document.createElement('p');
                    oddsValueP.innerText = oddsValue;

                    oddsValueContainer.appendChild(oddsValueP);
                    oddsDiv1.appendChild(oddsValueContainer);
                } else if (counter >= 89 && counter <= 151) {
                    var oddsValueContainer = document.createElement('div');
                    oddsValueContainer.classList.add(columnName);
                    var oddsValue = decimalToAmerican(row[columnName]);
                    var oddsValueP = document.createElement('p');

                    oddsValueP.innerText = oddsValue;
                    oddsValueContainer.appendChild(oddsValueP);
                    oddsDiv2.appendChild(oddsValueContainer);
                }
            }

            oddsContainer.appendChild(oddsDiv1);
            oddsContainer.appendChild(oddsDiv2);

            if (!doesElementExistWithId(row.game_id)) {
                const gameIdDiv = document.createElement('div');
                gameIdDiv.classList.add("single-game");
                gameIdDiv.addEventListener('click', function () {
                    showSubLines(gameIdDiv)
                });
                gameIdDiv.id = row.game_id;
                document.getElementById('data-list').appendChild(gameIdDiv);
                isFirst = "first";
            } else {
                isFirst = "hidden";
            }

            const gameIdDiv = document.getElementById(row.game_id);
            const newRow = document.createElement('tr');
            newRow.id = row.hashable_id;

            newRow.innerHTML = `
        <div class = "game-div-row">
            <div class = "game-div-row away-team"><p>${row.wager_display}</p></div>
            <div class = "game-div-row home-team"><p>${row.wager_display_other}</p></div>
        </div>
        `;

            newRow.appendChild(oddsContainer);

            newRow.classList.add(isFirst);

            gameIdDiv.appendChild(newRow);

        });
    }

};

function showSubLines(clickedElement) {
    clickedElement.querySelectorAll('tr').forEach(function (el) {
        if (el !== clickedElement.firstElementChild) {
            el.classList.toggle('hidden');
        }
    });
}

function modifyRows(data) {

    console.log("Changing:");
    console.log(data);

    var activeSportValue = document.getElementById('sport-league-filter').querySelector('.active').querySelector('a').innerText

    let activeSport = getKeyByValue(leagueDisplayDict, activeSportValue);

    console.log(activeSport)

    let activeMarket = document.getElementById('market-filter').querySelector('.active').querySelector('a').innerText;

    var filteredData = data.filter(function (item) {
        return item.sport_title === activeSport && item.market_reduced === activeMarket;
    });

    console.log("filtered data: ", filteredData)

    filteredData.forEach(function(row) {
        var rowToEdit = document.getElementById(row.hashable_id);
    
        if (rowToEdit) {
            for (var key in row) {
                var childElement = rowToEdit.querySelector(`.${key} p:first-child`);
                if (childElement) {

                    var value = String(decimalToAmerican(String(row[key])));

                    // Compare values, higher = green fade, lower = red fade 
                    // Maybe make these numbers from the get-go and then convert to string once? 
    
                    if (childElement.innerText != value) {
                        if (!childElement.classList.contains("fade-to-red")) {
                            childElement.classList.add("fade-to-red");
                        }

                        childElement.innerText = value;
                    }
                }
            }
        } else {
            console.error("rowToEdit is not a valid DOM element");
        }
    });
    
    // Add animationend event listener to elements with fade-to-red class
    document.querySelectorAll('.fade-to-red').forEach(function(element) {
        element.addEventListener('animationend', animationEndHandler);
    });

}


function animationEndHandler() {
    this.classList.remove('fade-to-red');
    this.removeEventListener('animationend', animationEndHandler);
}


function fillFilterValues(data) {

    document.querySelectorAll(".full-filter-ind-content-title").forEach(function (el) {
        el.addEventListener('click', function () {
            el.parentNode.querySelector('.full-filter-ind-content-values').classList.toggle("hidden");
        })
    });

    var uniqueSportLeagues = new Set(data.map(item => item.sport_title));

    var uniqueSportLeaguesArray = Array.from(uniqueSportLeagues);

    var leagueFilterDiv = document.getElementById("sport-league-filter");

    var isFirst = true;

    uniqueSportLeaguesArray.forEach(function (value) {
        var filterDropdownItem = document.createElement("div");

        var filterContentLabel = document.createElement("label");
        filterContentLabel.classList.add("custom-checkbox");

        var filterContentLabelInput = document.createElement("input");
        var filterContentLabelSpan = document.createElement("span");
        var filterValueContent = document.createElement("a");

        filterContentLabel.appendChild(filterContentLabelInput);
        filterContentLabel.appendChild(filterContentLabelSpan);
        filterContentLabel.appendChild(filterValueContent);

        filterContentLabelInput.type = "checkbox"
        filterContentLabelSpan.classList.add("checkmark")
        filterDropdownItem.classList.add("filter-dropdown-item");
        filterValueContent.classList.add("filter-value-content-a");

        filterDropdownItem.appendChild(filterContentLabel);
        filterValueContent.innerText = leagueDisplayDict[value];

        leagueFilterDiv.appendChild(filterDropdownItem);

        filterDropdownItem.addEventListener('click', function (event) {
            // document.getElementById('data-list').innerHTML = '';

            leagueFilterDiv.querySelectorAll(".filter-dropdown-item").forEach(function (item) {
                item.classList.remove("active");
                item.querySelector("checkbox")
                var checkboxElement = item.querySelector('.custom-checkbox input[type="checkbox"]');
                checkboxElement.checked = false;
            });
            if (!filterDropdownItem.classList.contains("active")) {
                filterDropdownItem.classList.add("active");
                var checkboxElement = filterDropdownItem.querySelector('.custom-checkbox input[type="checkbox"]');
                checkboxElement.checked = true;
            }
            if (!leagueFilterDiv.classList.contains("hidden")) {
                leagueFilterDiv.classList.add("hidden")
                leagueFilterDiv.parentNode.querySelector('.amount-selected a').innerText = filterDropdownItem.querySelector('.filter-value-content-a').innerText;
            document.getElementById('data-list').innerHTML = '';

                addData(data);
            };
        });

        if (isFirst) {
            filterDropdownItem.classList.add("active");
        }

        isFirst = false;


    })

    var uniqueMarkets = new Set(data.map(item => item.market_reduced));

    var uniqueMarketsArray = Array.from(uniqueMarkets);

    var marketFilterDiv = document.getElementById("market-filter");

    isFirst = true;



    uniqueMarketsArray.forEach(function (value) {

        var filterDropdownItem = document.createElement("div");

        var filterContentLabel = document.createElement("label");
        filterContentLabel.classList.add("custom-checkbox");

        var filterContentLabelInput = document.createElement("input");
        var filterContentLabelSpan = document.createElement("span");
        var filterValueContent = document.createElement("a");

        filterContentLabel.appendChild(filterContentLabelInput);
        filterContentLabel.appendChild(filterContentLabelSpan);
        filterContentLabel.appendChild(filterValueContent);

        filterContentLabelInput.type = "checkbox"
        filterContentLabelSpan.classList.add("checkmark")
        filterDropdownItem.classList.add("filter-dropdown-item");
        filterValueContent.classList.add("filter-value-content-a");

        filterDropdownItem.appendChild(filterContentLabel);
        filterValueContent.innerText = value;

        marketFilterDiv.appendChild(filterDropdownItem);

        filterDropdownItem.addEventListener('click', function (event) {

            marketFilterDiv.querySelectorAll(".filter-dropdown-item").forEach(function (item) {
                item.classList.remove("active");
                item.querySelector("checkbox")
                var checkboxElement = item.querySelector('.custom-checkbox input[type="checkbox"]');
                checkboxElement.checked = false;
            });
            if (!filterDropdownItem.classList.contains("active")) {
                filterDropdownItem.classList.add("active");
                var checkboxElement = filterDropdownItem.querySelector('.custom-checkbox input[type="checkbox"]');
                checkboxElement.checked = true;
            }
            if (!marketFilterDiv.classList.contains("hidden")) {
                marketFilterDiv.classList.add("hidden")
                marketFilterDiv.parentNode.querySelector('.amount-selected a').innerText = filterDropdownItem.querySelector('.filter-value-content-a').innerText;
            document.getElementById('data-list').innerHTML = '';

                addData(data);
            };
        });

        if (isFirst) {
            filterDropdownItem.classList.add("active");
        }

        isFirst = false;

    })
    leagueFilterDiv.parentNode.querySelector('.amount-selected a').innerText = leagueFilterDiv.querySelector('.active').querySelector('a').innerText;

    marketFilterDiv.parentNode.querySelector('.amount-selected a').innerText = marketFilterDiv.querySelector('.active').querySelector('a').innerText;

}

function getImageSportsbookRow(sportsbook_string) {

    var imageDictionary = {
        'unibet_us': '/static/images/sportsbook_logos/unibet.png', 
        'bovada': '/static/images/sportsbook_logos/bovada.png', 
        'tipico_us': '/static/images/sportsbook_logos/tipico.png', 
        'livescore': '/static/images/sportsbook_logos/livescore.png', 
        'matchbook': '/static/images/sportsbook_logos/matchbook.png', 
        'betsson': '/static/images/sportsbook_logos/betsson.png', 
        'sportsbet': '/static/images/sportsbook_logos/sportsbet.png', 
        'fliff': '/static/images/sportsbook_logos/fliff.png', 
        'fanduel': '/static/images/sportsbook_logos/fanduel.png', 
        'playup': '/static/images/sportsbook_logos/playup.png', 
        'windcreek': '/static/images/sportsbook_logos/windcreek.png', 
        'twinspires': '/static/images/sportsbook_logos/twinspires.png', 
        'pointsbetus': '/static/images/sportsbook_logos/pointsbet.png', 
        'pointsbetau': '/static/images/sportsbook_logos/pointsbet.png', 
    
        'coolbet': '/static/images/sportsbook_logos/coolbet.png', 
        'suprabets': '/static/images/sportsbook_logos/suprabets.png', 
        'neds': '/static/images/sportsbook_logos/neds.png', 
        'virginbet': '/static/images/sportsbook_logos/virginbet.png', 
        'betus': '/static/images/sportsbook_logos/betus.png', 
        'betonlineag': '/static/images/sportsbook_logos/betonlineag.png', 
        'mybookieag': '/static/images/sportsbook_logos/mybookie.png', 
        'draftkings': '/static/images/sportsbook_logos/draftkings.png', 
        'nordicbet': '/static/images/sportsbook_logos/nordicbet.png', 
        'pinnacle': '/static/images/sportsbook_logos/pinnacle.png', 
        'grosvenor': '/static/images/sportsbook_logos/grosvenor.png', 
        'topsport': '/static/images/sportsbook_logos/topsport.png', 
        'betmgm': '/static/images/sportsbook_logos/betmgm.png', 
        'boyle': '/static/images/sportsbook_logos/boyle.png', 
        'superbook': '/static/images/sportsbook_logos/superbook.png', 
        'espnbet': '/static/images/sportsbook_logos/espnbet.png', 
        'betvictor': '/static/images/sportsbook_logos/betvictor.png', 
        'sport888': '/static/images/sportsbook_logos/888sport.png', 
        'wynnbet': '/static/images/sportsbook_logos/wynnbet.png', 
        'betway': '/static/images/sportsbook_logos/betway.png', 
        'casumo': '/static/images/sportsbook_logos/casumo.png', 
        'betrivers': '/static/images/sportsbook_logos/betrivers.png', 
        'betparx': '/static/images/sportsbook_logos/betparx.png', 
        'betfair': '/static/images/sportsbook_logos/betfair.png', 
        'betfair_ex_eu': '/static/images/sportsbook_logos/betfair.png', 
        'everygame': '/static/images/sportsbook_logos/everygame.png', 
        'marathonbet': '/static/images/sportsbook_logos/marathonbet.png', 
        'williamhill_us': '/static/images/sportsbook_logos/williamhill.png', 
        'ladbrokes': '/static/images/sportsbook_logos/ladbrokes.png', 
        'paddypower': '/static/images/sportsbook_logos/paddypower.png', 
        'si_sportbsook': '/static/images/sportsbook_logos/si_sportbsook.png', 
        'leovegas': '/static/images/sportsbook_logos/leovegas.png', 
        'coral': '/static/images/sportsbook_logos/coral.png', 
        'betclic': '/static/images/sportsbook_logos/betclic.png', 
        'bluebet': '/static/images/sportsbook_logos/bluebet.png', 
        '1xbet': '/static/images/sportsbook_logos/1xbet.png', 
        'mrgreen': '/static/images/sportsbook_logos/mrgreen.png', 
        'betr': '/static/images/sportsbook_logos/betr.png', 
        'skybet': '/static/images/sportsbook_logos/skybet.png', 
        'unibet_eu': '/static/images/sportsbook_logos/unibet.png', 
        'livescorebet_eu': '/static/images/sportsbook_logos/livescore.png', 
        'onexbet': '/static/images/sportsbook_logos/1xbet.png',
        'williamhill': '/static/images/sportsbook_logos/williamhill.png',
        'sisportsbook': '/static/images/sportsbook_logos/si_sportsbook.png',
        'betfair_ex_uk': '/static/images/sportsbook_logos/betfair.png',
        'betfair_sb_uk': '/static/images/sportsbook_logos/betfair.png',
        'betfair_ex_au': '/static/images/sportsbook_logos/betfair.png',
        'betr_au': '/static/images/sportsbook_logos/betr.png',
        'boylesports': '/static/images/sportsbook_logos/boyle.png',
        'ladbrokes_uk': '/static/images/sportsbook_logos/ladbrokes.png',
        'ladbrokes_au': '/static/images/sportsbook_logos/ladbrokes.png',
        'livescorebet': '/static/images/sportsbook_logos/livescore.png',
        'unibet_uk': '/static/images/sportsbook_logos/unibet.png',
        'unibet_uk': '/static/images/sportsbook_logos/unibet.png',
        'unibet': '/static/images/sportsbook_logos/unibet.png',
    };
  
    const div = document.createElement("div");
    div.classList.add("all-books-ind-logo")
  
    var imageUrl = imageDictionary[sportsbook_string];
    if (imageUrl) {
      var imgElement = document.createElement('img');
      imgElement.src = imageUrl;
      imgElement.alt = sportsbook_string;
      imgElement.height = 80;
      imgElement.width = 80;
  
      div.appendChild(imgElement);
  
      return div
    } else {
      console.error('Image URL not found for:', sportsbook_string, ' in getImageSportsbookRow');
      var imgElement = document.createElement('img');
      imgElement.height = 80;
      imgElement.width = 80;
      div.appendChild(imgElement);
      return div
  
    }
}

  function fillHeader(data){

    const header = document.getElementById("data-list-header");

    if (data.length > 0) {
        const firstRow = data[0];

        var counter = 0;

        for (var columnName in firstRow) {

            counter++;

            if (counter >= 26 && counter <= 88) {
                var imgDiv = getImageSportsbookRow(columnName);
                header.appendChild(imgDiv);
            } 
        }
    } else {
        console.error("Data array is empty.");
    }

}


document.addEventListener('DOMContentLoaded', function () {

    initialLoadData();

    const socket = io.connect();

    socket.on('connect', function () {
        console.log('Connected to server');
    });

    socket.on('update_data', function (data) {

        var addedRows = JSON.parse(data['added_rows']);

        var modifiedRows = JSON.parse(data['changed_rows']);

        addData(addedRows);

        modifyRows(modifiedRows);

    });


});


// Need an initial fill method