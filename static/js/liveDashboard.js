let isPageVisible = true;
let updateInterval;

function updateTable(data) {
  const tableBody = document.querySelector('#data-table tbody');
  tableBody.innerHTML = '';

  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
    <td>${row.ev}</td>
    <td><b>${row.team}</b> against ${row.opponent}</td>
    <td>${row.highest_bettable_odds}</td>
    <td>${row.sportsbooks_used}</td>
    <td>${convertToUserTimezone(row.date)}</td>
    <td>${convertToUserTimezoneUpdate(row.snapshot_time)}</td>`;
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


function fetchDataAndUpdateTable() {
  console.log('this has been called');
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

fetchDataAndUpdateTable();

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

fetchDataAndUpdateTable();


startUpdateInterval();