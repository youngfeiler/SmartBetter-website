function formatCurrency(number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(number);
}

// Assuming you fetch data and format it correctly
fetch('/get_unsettled_bet_data')
  .then(response => response.json())
  .then(data => {
    console.log(data)
    const tableBody = document.querySelector('#bets-container');
    let previousGameId = null;

    for (const game_id in data) {

      const betBox = document.createElement('div');
      betBox.classList.add("bet");
      

      const rows = data[game_id];

      const headerBox = document.createElement('div');
      headerBox.classList.add("header-box");
      teamHeader = document.createElement('h3');
      teamHeader.textContent = "Team";

      result = document.createElement('h3');
      result.textContent = "Payout";

      avgOdds = document.createElement('h3');
      avgOdds.textContent = "Avg Odds";

      headerBox.appendChild(teamHeader);
      headerBox.appendChild(result);
      headerBox.appendChild(avgOdds);

      betBox.appendChild(headerBox);

      for (let i = 0; i < rows.length; i++) {
        const row = rows[i];

        const rowBox = document.createElement('div');
        rowBox.classList.add('row-box');
        
        var teamCellDiv = document.createElement('div');
        teamCellDiv.classList.add("cell-div");
        teamCellDiv.classList.add("team-div");


        const teamCell = document.createElement('h3');
        teamCell.textContent = row.team;
        teamCellDiv.appendChild(teamCell);
        rowBox.appendChild(teamCellDiv);

        teamCellDiv = document.createElement('div');
        teamCellDiv.classList.add("cell-div");
        const ifWinCell = document.createElement('h3');
        ifWinCell.textContent = formatCurrency(row.if_win);

        teamCellDiv.appendChild(ifWinCell);
        rowBox.appendChild(teamCellDiv)
        
        teamCellDiv = document.createElement('div');
        teamCellDiv.classList.add("cell-div");

        const avgOddsCell = document.createElement('h3');
        avgOddsCell.textContent = "-";

        if(row.average_odds.toString().length > 1){
          avgOddsCell.textContent = addSign(row.average_odds.toString());
        }
        teamCellDiv.appendChild(avgOddsCell);
        rowBox.appendChild(teamCellDiv);

        betBox.appendChild(rowBox);
      }
      imgContainer = document.createElement('div');
      imgContainer.classList.add("row-box");
      imgContainer.classList.add("img-container");

      img = document.createElement('img');
      img.classList.add("logo-img");
      img.src = "static/images/sidebar_logo.png";
      imgContainer.appendChild(img);
      betBox.appendChild(imgContainer);
    tableBody.append(betBox);
    }

  });
