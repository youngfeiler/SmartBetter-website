document.addEventListener('DOMContentLoaded', function() {
  const toggleUpButtons = document.querySelectorAll('.toggle_up');
  const submitCustom = document.querySelectorAll('#submitCustom');


  customButton = document.getElementById('customButton');
  customText = document.getElementById('customText');
  let parentButtonToUpdate; // Store a reference to the parent button
  
  // Function that handles the selecting and deslecting of proper sport shit 
  const sportLabels = document.querySelectorAll('[data-label="sport"]');
  sportLabels.forEach(sportLabel => {
    sportLabel.addEventListener('click', function(e) {

      sportLabels.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');

      var thisSport = "";
      var otherSport = "";
      if(sportLabel.innerHTML == 'NFL'){
        
        var thisSport = "NFL";
        var otherSport = "MLB";
      }else if(sportLabel.innerHTML == "MLB"){
        var thisSport = "MLB";
        var otherSport = "NFL";
      }
      const thisSportDropdowns = document.querySelectorAll(`[data-sport="${thisSport}"]`);
      const otherSportDropdowns = document.querySelectorAll(`[data-sport="${otherSport}"]`);
      thisSportDropdowns.forEach(item => {
        item.style.display = 'block';
      });
      otherSportDropdowns.forEach(item => {
        item.style.display = 'none';
      });
    })
  });

  const conferenceLabels = document.querySelectorAll('[data-label="team_1_conference"]');
  conferenceLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      conferenceLabels.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');
    })
  });

  const divisionLabels = document.querySelectorAll('[data-label="team_1_division"]');
  divisionLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      divisionLabels.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');
    })
  });

  const homeAwayLabels = document.querySelectorAll('[data-label="home_away"]');
  homeAwayLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      homeAwayLabels.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');
    })
  });

  const dayNightLabels = document.querySelectorAll('[data-label="day_night"]');
  dayNightLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      dayNightLabels.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');
    })
  });

  const dayOfWeekLabels = document.querySelectorAll('[data-label="day_of_week"]');
  dayOfWeekLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      dayOfWeekLabels.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');
    })
  });



    //   const text = e.target.innerText;
    //   if (text === 'Custom') {
    //     parentButtonToUpdate = $(this).closest('.dropdown');
    //     customButton.style.display = 'block';
    //   } else {
    //     const parentButton = $(this).closest('.dropdown');
    //     const btn = parentButton.find('.btn');
    //     btn.text(text);
    //     customButton.style.display = 'none';
    //   }
    // });

  toggleUpButtons.forEach(toggleUpButton => {
    toggleUpButton.addEventListener('click', function(e) {
      const text = e.target.innerText;
      if (text === 'Custom') {
        parentButtonToUpdate = $(this).closest('.dropdown');
        customButton = parentButtonToUpdate.find('#customButton'); // Replace 'this' with the clicked element
        customText = parentButtonToUpdate.find('#customText')[0]; // Replace 'this' with the clicked element
        console.log(customText);
        customButton[0].style.display = 'block';
      } else {
        const parentButton = $(this).closest('.dropdown');
        const btn = parentButton.find('.btn');
        btn.text(text);
      }
    });
  });

submitCustom.forEach(submitCustomCurrent => {
  submitCustomCurrent.addEventListener('click', function() {
    const customButtonText = customText.value;
    if (parentButtonToUpdate) {
      const btn = parentButtonToUpdate.find('.btn');
      btn.text(parentButtonToUpdate.find('h5').text()+ " greater than " + customButtonText);
      customButton[0].style.display = 'none';
    }
  });
  });
});


const goButton = document.getElementById('goButton');
goButton.addEventListener('click', function() {
    filterAndDisplayData();
});


function filterAndDisplayData() {
  const dictionary = {};
  const actives = document.querySelectorAll('.active');
  actives.forEach(label => {
    dictionary[label.dataset.label] = label.dataset.value;
    console.log(dictionary);
  });
  fetch('/get_scenario_data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(dictionary),
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
}





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




// document.addEventListener('DOMContentLoaded', function() {
//   const toggleUpButtons = document.querySelectorAll('.toggle_up');

//   toggleUpButtons.forEach(toggleUpButtons => {
//     toggleUpButtons.addEventListener('click', function(e) {
//         console.log('clicked');
//         e.preventDefault();
//         //get the parent of the button
//         parentButton = $(this).closest('.dropdown')
//         //get the text of the button
//         console.log(parentButton)
//         // get the first button in the parent
//         btn = parentButton.find('.btn')
//         //change the text of the button
//         //console log the text of btn
//         console.log(btn)
//         console.log(btn.textContent)
//         btn.text(e.target.innerText);
//         // getSportAndReturnData(toggleUpButtons.innerText);
//   });
//   })
// });

// document.addEventListener('DOMContentLoaded', function() {
//   const toggleUpButtons = document.querySelectorAll('.toggle_up');
//   const customButton = document.getElementById('customButton');
//   const customText = document.getElementById('customText');
//   const submitCustom = document.getElementById('submitCustom');

//   toggleUpButtons.forEach(toggleUpButton => {
//     toggleUpButton.addEventListener('click', function(e) {
//       const text = e.target.innerText;
//       if (text === 'Custom') {
//         customButton.style.display = 'block';
//       } else {
//         const parentButton = $(this).closest('.dropdown');
//         const btn = parentButton.find('.btn');
//         btn.text(text);
//         customButton.style.display = 'none';
//       }
//     });
//   });

//   submitCustom.addEventListener('click', function() {
//     const customButtonText = customText.value;
//     const parentButton = $('.dropdown');
//     const btn = parentButton.find('.btn');
//     btn.text(customButtonText);
//     customButton.style.display = 'none';
//   });
// });