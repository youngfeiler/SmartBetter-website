$(document).ready(function() {
  function formatNumber(number) {
    const absNumber = Math.abs(number);
    const formattedNumber = absNumber.toLocaleString();
    return (number >= 0) ? `+$${formattedNumber}` : `-$${formattedNumber}`;
  }


    $.ajax({
      url: "/get_user_performance_data",
      type: "GET",
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(graphData) {
        if (graphData.status === 'error') {
          $('#graph').text(graphData.message).css('color', 'white');;
        } else {
        $('#graph').empty();
        
        var xData = [];
        var yData = [];
        var infoData = [];
        var dayResultInfo = [];
        var runningPL =[];
        var totalPL;
        var totalPrecision;
        var bestDay;
        var worstDay;
        var totalBetsPlaced;
        var returnOnMoney;

        console.log(graphData)
        graphData.forEach(function(item) {
          xData.push(item.date);
          yData.push(item.running_p_l);
          runningPL.push(item.running_p_l);
          dailyPL = item.daily_result;
          totalPrecision = item.total_precision;
          bestDay = item.best_day;
          worstDay = item.worst_day;
          totalBetsPlaced = item.total_bets_placed;
          returnOnMoney = item.return_on_money;
          totalPL = item.total_p_l;
          var dayInfo = "";
            dayInfo += "<b>Cumulative: $" + item.running_p_l + "<br> <b>Day: $"+ item.daily_result;
          dayResultInfo.push(dayInfo);
        });

        const FormattedTotalPl = formatNumber(parseInt(totalPL));
        var titleColor = (totalPL >= 0) ? '#00c805' : 'red';


        console.log(yData)

        var trace = {
          x: xData,
          y: yData,
          mode: 'lines+markers',
          hovertext: dayResultInfo,
          hoverinfo: 'text',
          marker: {
            size: 2,
            color : titleColor,
          },
          hoverlabel: {
            bgcolor: '#ffffff', // Customize background color of the hover template
            bordercolor: '#ffffff', // Set the border color of the hover template
            font: {
              color: '#000000', // Customize text color of the hover template
              size: 12, // Customize font size of the hover template
            },
          },
        };

        var layout = {
          title: {
            text: FormattedTotalPl,
            font: {
              family: 'Arial, sans-serif',
              size: 24,
              color: titleColor,
              weight: 'bold'
            }
          },
          showline: false,
          titlefont: {
            family: 'Arial, sans-serif',
            size: 18,
            color: 'black',
            weight: 'bold' // Set the font weight to bold for axis title
          },
          xaxis: {
            showgrid: false,
            showline: false,
            zeroline: false,
            linecolor: '#000000',
            tickfont: {
              color: '#000000',
                weight: 'bold'
            },
            automargin: true,
          },
          yaxis: {
            showgrid: false,
            showline: false, 
            zeroline: false,
            titlefont:{
              weight: 'bold'
            }
          },
          font: {
            color: '#000000',
            weight: 'bold',
          },
          plot_bgcolor: '#ffffff',
          paper_bgcolor: '#ffffff',
        };


        var graph = document.getElementById('graph');
        Plotly.newPlot(graph, [trace], layout);


        var overallStats = document.getElementById('overall-info-box');

        var worstDayEl = overallStats.querySelector('#worst-day');
        var bestDayEl = overallStats.querySelector('#best-day');
        var totalPlEl = overallStats.querySelector('#total-pl');
        var precEl = overallStats.querySelector('#precision');
        var totalBetsPlacedEl = overallStats.querySelector('#total-bets-placed');
        var returnOnMoneyEl = overallStats.querySelector('#return-on-money');

        worstDayEl.innerHTML = worstDay ;
        bestDayEl.innerHTML = "+"+bestDay;
        // totalPlEl.innerHTML = "+"+TotalPL ;
        precEl.innerHTML = totalPrecision + "%";
        totalBetsPlacedEl.innerHTML =totalBetsPlaced;
        returnOnMoneyEl.innerHTML = returnOnMoney + "%";

        $('#graph-info-tab').addClass('active');

        // Rest of your success function code...

        // Event handler for clicking on a data point
        graph.on('plotly_click', function(data) {
          var pointIndex = data.points[0].pointIndex;
          var selectedInfo = infoData[pointIndex];
          var selectedDate = data.points[0].x; // Get the date associated with the clicked point


          // Show the day-info-list when a data point is clicked
          $('#info-list').hide();
          var infoBox = document.getElementById('day-info-list');
          infoBox.innerHTML = "<b>Date: " + selectedDate + "</b><br>" + selectedInfo;
          $('#day-info-list').show()
          $('#day-info-tab').addClass('active');
          $('#graph-info-tab').removeClass('active');
        });

      }}
    });
  }
)
