let isPageVisible = true;
let updateInterval;
let currentlyEditingRow = false;

function updateTable(data) {
  const tableBody = document.querySelector('#data-table tbody');
  tableBody.innerHTML = '';

  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
    <td style = "display:none;">${row.game_id}</td>
    <td>${row.ev}</td>
    <td><b>${row.team}</b><br> v. ${row.opponent}</td>
    <td>${row.highest_bettable_odds}</td>
    <td>${row.sportsbooks_used}</td>
    <td>${convertToUserTimezone(row.date)}</td>
    <td>${convertToUserTimezoneUpdate(row.snapshot_time)}</td>
    <td><button onclick = "editRow(this)" class="add-to-betslip-button" id="add-to-betslip-button" data-ev="${row.ev}" data-team="${row.team}" data-odds="${row.highest_bettable_odds}">Add to Betslip</button></td>`;
    tableBody.appendChild(tr);
  });
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

function saveRow(button) {
  console.log('Saving row:');
  const row = button.parentNode.parentNode;
  const cells = row.querySelectorAll('td:not(:last-child)');
    
  let rowData = {};
  cells.forEach((cell, index) => {
    const input = cell.querySelector('input');
    const columnName = ['game_id', 'ev', 'team', 'odds', 'sportsbook', 'game_date', 'time_updated']; // Replace with your column names
    rowData[columnName[index]] = input.value;
    console.log(input.value);

    cell.innerHTML = input.value;
  });
  console.log(rowData);
  button.innerText = 'Edit';
  button.onclick = () => editRow(button);

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
  console.log('this has been called');
  console.log(currentlyEditingRow);
  if (!currentlyEditingRow){
    const url = '/get_live_dash_data?' + new Date().getTime();
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (isPageVisible) {
          updateTable(data);
        }
      })
      .catch(error => console.error('Error fetching data:', error));
    }
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


document.addEventListener('visibilitychange', handleVisibilityChange);


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


$(document).ready(
  startUpdateInterval
);