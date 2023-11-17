
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
      ],
  },
  options: {
      responsive: true,
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

                  // Draw red background
                  ctx.save();
                  ctx.fillStyle = 'rgba(0, 0, 0, 0)';
                  ctx.fillRect(x, 0, 2, lineChartInstance.height);
                  ctx.restore();

                  // Draw black dashed hover line
                  ctx.save();
                  ctx.beginPath();
                  ctx.setLineDash([5, 5]); // Set the dash pattern
                  ctx.moveTo(x, 0);
                  ctx.lineTo(x, lineChartInstance.height);
                  ctx.lineWidth = 2;
                  ctx.strokeStyle = 'rgb(208, 208, 208)';
                  ctx.stroke();
                  ctx.restore();
              }
          },
      },
  },
};

const chart = document.getElementById('lineChart');
lineChart = new Chart(chart, lineConfig);

function makeChart(data){
  console.log(data);
  if ($(window).width() <= 800) {
    chart.style.height="200px";
    $("#lineChart").attr("height", "200");
    // $("#lineChart").style.height = "200 !important";

  }
  lineConfig.data.labels = data.game_date;
  lineConfig.data.datasets[0].data = data.running_sum;
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

document.addEventListener('DOMContentLoaded', function() {
  addEventListeners();
  updateGraph();
});