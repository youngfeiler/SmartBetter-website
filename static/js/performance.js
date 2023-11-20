
let lineChart;
const lineConfig = {
  type: 'line',
  data: {
      labels: [],
      datasets: [
          {
              backgroundColor: createGradient('rgba(165, 255, 227, 1)', 'rgba(201, 255, 238, 0.1)'),
              borderColor: '#21CE99',
              pointHoverBackgroundColor: '#21CE99', // Customize hover background color
              pointHoverBorderColor: '#ffffff', // Customize hover border color
              data: [],
              fill: 'start',
              tension: 0.6,
              pointRadius: 1, // Initial point radius set to 0
              pointHoverRadius: 8, // Increase the hover radius for a shadow effect
          },
          {
            backgroundColor: createGradient('rgba(165, 255, 227, 1)', 'rgba(201, 255, 238, 0.1)'),
            borderColor: '#21CE99',
            pointHoverBackgroundColor: '#21CE99', // Customize hover background color
            pointHoverBorderColor: '#ffffff', // Customize hover border color
            data: [],
            fill: 'start',
            tension: 0.6,
            pointRadius: 1, // Initial point radius set to 0
            pointHoverRadius: 8, // Increase the hover radius for a shadow effect
        },
      ],
  },
  options: {
      responsive: true,
      maintainAspectRatio: false,
      elements: {
          point: {
              radius: 5,
              hoverRadius: 8,
              borderWidth: 5,
              hoverBorderWidth: 8, // Set the border width on hover
          }
      },
      legend: {
          display: false, // Set display to false to hide the legend
      },
      scales: {
          yAxes: [{
              min: 1800,
              max: 12200,
              stepSize: 100,
              position: 'right',
              gridLines: {
                  display: true,
              },
          }],
          xAxes: [{
              display: true,
              gridLines: {
                  display: false,
              },
          }],
      },
      layout: {
          padding: {
              right: 0,
          },
      },
      hover: {
          onHover: function (e) {
              const lineChartInstance = this.chart;
              const hoverPoint = lineChartInstance.getElementsAtEventForMode(e, 'nearest', { intersect: true }, false);

              if (hoverPoint.length > 0) {
                  const activePoint = hoverPoint[0];
                  const ctx = lineChartInstance.ctx;
                  const x = activePoint.tooltipPosition().x;
              }
          },
      },
      tooltips: {
        callbacks: {
          label: function (tooltipItem, data) {
            const value = data.datasets[1].data[tooltipItem.index];
            return value;
          },
        },
        // filter: function (tooltipItem) {
        //   return tooltipItem.datasetIndex === 1; // Filter to apply word wrap only for the second dataset tooltip
        // },
        bodyFont: {
          wordWrap: 'break-word', // Set word wrap for tooltip body
        },

        
      },
  },
};

const chart = document.getElementById('lineChart');
lineChart = new Chart(chart, lineConfig);

function makeChart(data){
  if ($(window).width() <= 800) {
    chart.style.width = "100%";
    chart.style.height = "250px !important"; 
    console.log(lineConfig);
    lineConfig.options.elements.point.radius = 2; 
    lineConfig.options.elements.point.borderWidth = 2;
  } 
  else {
    // chart.style.width = "600px";
    // chart.style.height = "100%";
  }
  lineConfig.data.labels = data.game_date;
  lineConfig.data.datasets[0].data = data.running_sum;
  lineConfig.data.datasets[1].data = data.hover_info;

  removeLoadingAnimation();

  lineChart.update();
};

function addEventListeners() {
  var selectElements = document.querySelectorAll('.form-select');
  selectElements.forEach(function(selectElement) {
    selectElement.addEventListener('change', updateGraph);
  });
}

function createGradient(startColor, endColor) {
    const ctx = document.createElement('canvas').getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, startColor);
    gradient.addColorStop(1, endColor);
    return gradient;
}

function makeInfo(data){
  totalPl = document.getElementById('total-pl');
  totalPl.innerHTML = formatCurrency(data.total_pl[0]);

  worstDay = document.getElementById('worst-day');
  worstDay.innerHTML = formatCurrency(data.worst_day[0]);

  bestDay = document.getElementById('best-day');
  bestDay.innerHTML = formatCurrency(data.best_day[0]);
  
  winRate = document.getElementById('win-rate');
  winRate.innerHTML = formatPercentage(data.win_rate[0]);

  totalBets = document.getElementById('total-bets');
  totalBets.innerHTML = data.amount_of_bets[0];

  returnOnMoney = document.getElementById('return');
  returnOnMoney.innerHTML = formatPercentage(data.return_on_money[0]);

  total = document.getElementById('total');
  total.innerHTML = formatCurrency(data.total_pl[0] + 1000);

}

function formatCurrency(number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(number);
}

function formatPercentage(percentage) {
  return (percentage).toLocaleString('en-US', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  });
}

function updateGraph() {
  var actives = document.querySelectorAll('option:checked');
  var paramsDict = {
    'sport_title':actives[0].value,
    'timing':actives[1].value,
    'bet_size':actives[2].value
  }
  const url = '/get_performance_data?';
  clearInfoBoxes();
  showLoadingAnimation();

  fetch(url,{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ params: paramsDict }),
  })
    .then(response => response.json())
    .then(data => {
      makeChart(data);
      makeInfo(data);
    })
    .catch(error => console.error('Error fetching data:', error));
}

function clearInfoBoxes(){
  totalPl = document.getElementById('total-pl');
  totalPl.innerHTML = "";

  worstDay = document.getElementById('worst-day');
  worstDay.innerHTML = "";

  bestDay = document.getElementById('best-day');
  bestDay.innerHTML = "";
  
  winRate = document.getElementById('win-rate');
  winRate.innerHTML = "";

  totalBets = document.getElementById('total-bets');
  totalBets.innerHTML = "";

  returnOnMoney = document.getElementById('return');
  returnOnMoney.innerHTML = "";

  total = document.getElementById('total');
  total.innerHTML = "";
}

function showLoadingAnimation(){
  const animation = document.querySelector("#loading-animation");
  const canvas = document.querySelector("#lineChart");

  canvas.style.display = "none";
  animation.style.display = "flex";
}

function removeLoadingAnimation(){
  const animation = document.querySelector("#loading-animation");
  const canvas = document.querySelector("#lineChart");
  canvas.style.display = "block";
  animation.style.display = "none";
}


document.addEventListener('DOMContentLoaded', function() {
  addEventListeners();
  updateGraph();
});