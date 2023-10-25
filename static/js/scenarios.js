document.addEventListener('DOMContentLoaded', function() {
  const sportTitleButtons = document.querySelectorAll('.sport-title');
  const sportToggle = document.querySelector('.dropdown .sport');

  sportTitleButtons.forEach(sportTitleButton => {
    sportTitleButton.addEventListener('click', function(e) {
      e.preventDefault();
      sportToggle.innerText = sportTitleButton.innerText;
      getSportAndReturnData(sportTitleButton.innerText);
  });
  })
});

function getSportAndReturnData(sportTitle){
  const dataToSend = { sport: sportTitle };
  fetch('/get_scenario_data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(dataToSend),
})
.then(response => response.json())
.then(data => {
  // Parse the JSON data
  const parsedData = JSON.parse(data.data);

  // Extract x and y data
  const xData = parsedData.map(entry => entry.time_pulled);
  const yData = parsedData.map(entry => entry.running_win_sum);

  // Create the Plotly trace
  const trace = {
      x: xData,
      y: yData,
      mode: 'lines',
      type: 'scatter',
      name: 'Line Chart'
  };

  // Define the layout for the chart
  const layout = {
      title: 'Line Chart Example',
      xaxis: {
          title: 'Test'
      },
      yaxis: {
          title: 'Running Wins'
      }
  };

  // Create the Plotly chart
  Plotly.newPlot('chart', [trace], layout);
})
.catch(error => {
    console.error('Error:', error);
});
};


