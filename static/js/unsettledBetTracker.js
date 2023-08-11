// Assuming you fetch data and format it correctly
fetch('/get_unsettled_bet_data')
  .then(response => response.json())
  .then(data => {
    console.log(data)
    const tableBody = document.querySelector('#table-body');
    let previousGameId = null;

    for (const game_id in data) {
      const rows = data[game_id];

      for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const tableRow = document.createElement('tr');

        const teamCell = document.createElement('td');
        teamCell.textContent = row.team;
        tableRow.appendChild(teamCell);

        const ifWinCell = document.createElement('td');
        ifWinCell.textContent = row.if_win;
        tableRow.appendChild(ifWinCell);

        const avgOddsCell = document.createElement('td');
        avgOddsCell.textContent = row.average_odds;
        tableRow.appendChild(avgOddsCell);

        const highestOddsCell = document.createElement('td');
        highestOddsCell.textContent = row.highest_odds;
        tableRow.appendChild(highestOddsCell);

        // Add a border class to the first row of each game_id pair
        if (game_id !== previousGameId) {
          tableRow.classList.add('border-top');
          previousGameId = game_id;
        }

        tableRow.classList.add('border-r-l');

        // Add padding to create spacing between pairs of rows
        if (i === 0) {
          tableRow.classList.add('pair-start');
        }

        


        tableBody.appendChild(tableRow);
      }
    }
  });
