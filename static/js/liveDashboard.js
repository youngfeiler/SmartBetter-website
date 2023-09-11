let isPageVisible = true;
let updateInterval;
let currentlyEditingRow = false;


function updateTable(data) {
  const tableBody = document.querySelector('#data-table tbody');
  tableBody.innerHTML = '';
  const tr = document.createElement('tr');
  tr.classList.add('center-text');
  tr.innerHTML = `
  <td colspan="8">No approved bets available right now.</td>`;
  tableBody.appendChild(tr);
  boolin = true;
  if (!(data.length === 1 && data[0].update === false) && boolin) {
    const tableBody = document.querySelector('#data-table tbody');    tableBody.innerHTML = '';

    data.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
      <td style="display:none;">${row.game_id}</td>
      <td style="display:none;">${row.average_market_odds}</td>
      <td before-data="Team: " class="centered"><b>${row.team}</b></td>
      <td before-data="Sportsbook with Odds">${row.sportsbooks_used}</td>
      <td before-data="Recommended Bet Size ($): ">${row.bet_amount}</td>
      <td before-data="Odds to Take: ">${row.highest_bettable_odds}</td>
      <td before-data="+EV%: ">${row.ev}</td>
      <td class="mobile-no-display">${row.date}</td>
      <td before-data="Time Since Odds Update: ">${row.time_difference_formatted}</td>
      <td data-title="button"><button onclick="editRow(this)" class="add-to-betslip-button" id="add-to-betslip-button" data-ev="${row.ev}" data-team="${row.team}" data-odds="${row.highest_bettable_odds}">Add to My Bets</button></td>
      `;
      console.log(row)
      tableBody.appendChild(tr);
    });
  }
  else
  {
    console.log('No update');
  }
}

function updatebankroll(data){
  const bankroll = document.querySelector('#bankroll');
  bankroll.innerHTML = 'Bankroll: $';
  bankroll.innerHTML  += `${data[0].bankroll}`;
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

function saveRow(button) {
  console.log('Saving row:');
  const row = button.parentNode.parentNode;
  const cells = row.querySelectorAll('td:not(:last-child)');
    
  let rowData = {};
  cells.forEach((cell, index) => {
    const input = cell.querySelector('input');
    const columnName = ['game_id', 'average_market_odds', 'ev', 'team', 'odds', 'sportsbook', 'game_date', 'time_updated', 'bet_amount']; // Replace with your column names
    rowData[columnName[index]] = input.value;
    console.log(input.value);

    cell.innerHTML = input.value;
  });
  console.log(rowData);
  button.innerText = 'Edit';
  button.onclick = () => editRow(button);
  row.classList.remove('editing-row');

  $.ajax({
    url: '/add_saved_bet',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(rowData), // Convert rowData to JSON
    success: function(response) {
      if (response.status_code === 'error') {
        console.log('Error saving bet:', response.message);
      } else {
        console.log('Bet saved successfully:', response.message);
        currentlyEditingRow = false;
      }
    },
    error: function(error) {
      console.error('Error saving bet:', error);
    }
  });
}

function editRow(button) {
  console.log('Editing row:');
  currentlyEditingRow = true;
  const row = button.parentNode.parentNode;
  const cells = row.querySelectorAll('td:not(:last-child)');
  row.classList.add('editing-row');
  cells.forEach(cell => {
      const oldValue = cell.textContent.trim();
      const input = document.createElement('input');
      input.type = 'text';
      input.value = oldValue;
      cell.innerHTML = '';
      cell.appendChild(input);
  });
  const ev = cells[0]['childNodes'][0]['value'];

  button.innerText = 'Save';
  button.onclick = function() {
      saveRow(button);
  };
}
// Attach event listener to dynamically loaded element



function fetchDataAndUpdateTable() {
  console.log('Fetching data and updating table...');
  //remove if for refresh button
  //if (!currentlyEditingRow){
    const url = '/get_live_mlb_dash_data?' + new Date().getTime();
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (isPageVisible) {
          updateTable(data);
          updatebankroll(data);
        }
      })
      .catch(error => console.error('Error fetching data:', error));
  //}
}


function handleVisibilityChange() {
  isPageVisible = !document.hidden;

  if (isPageVisible) {
    // If the page becomes visible again, start the interval
    startUpdateInterval();
  } else {
    // If the page becomes hidden, stop the interval
    stopUpdateInterval();
  }
}



function sendDataToFlask(name, email) {
  $.post("/add_to_bet_tracker", { name: name, email: email }, function (data) {
    console.log("Data submitted:", data);
  });
}


function startUpdateInterval() {
  if (!updateInterval) {
    fetchDataAndUpdateTable();
    updateInterval = setInterval(fetchDataAndUpdateTable, 5000);
  }
}

function stopUpdateInterval() {
  clearInterval(updateInterval);
  updateInterval = null;
}

const bankrollP = document.getElementById("bankroll");
const addButton = document.getElementById("add-to-bankroll");

addButton.addEventListener("click", addToBankroll);

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

$(document).ready(
  fetchDataAndUpdateTable
);

document.getElementById('fetch-button').addEventListener('click', fetchDataAndUpdateTable);
