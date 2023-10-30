document.addEventListener('DOMContentLoaded', function() {
  makeTeamElements();
  const toggleUpButtons = document.querySelectorAll('.toggle_up');
  const submitCustom = document.querySelectorAll('#submitCustom');


  customButton = document.getElementById('customButton');
  customText = document.getElementById('customText');
  let parentButtonToUpdate; // Store a reference to the parent button
  
  // Function that handles the selecting and deslecting of proper sport shit 
  const leagueLabels = document.querySelectorAll('[data-label="sport"]');
  leagueLabels.forEach(sportLabel => {
    sportLabel.addEventListener('click', function(e) {

      // Deselect all confs, divs, teams 
      handleLeagueClick(this);
      var thisSport = "";
      var otherSport = "";
      if(sportLabel.innerHTML == 'NFL'){
        
        var thisSport = "NFL";
        var otherSport = "NBA";
      }else if(sportLabel.innerHTML == "NBA"){
        var thisSport = "NBA";
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

  const conferenceLabels = document.querySelectorAll('[data-label="this_team_conference"]');
  conferenceLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      handleConferenceClick(this);
    })
  });

  const conferenceLabelsOpponent = document.querySelectorAll('[data-label="opponent_team_conference"]');
  conferenceLabelsOpponent.forEach(label => {
    label.addEventListener('click', function(e) {
      handleConferenceClickOpponent(this);
    })
  });

  const divisionLabels = document.querySelectorAll('[data-label="this_team_division"]');
  divisionLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      handleDivisionClick(this);
    })
  });

  const divisionLabelsOpponent = document.querySelectorAll('[data-label="opponent_team_division"]');
  divisionLabelsOpponent.forEach(label => {
    label.addEventListener('click', function(e) {
      handleDivisionClickOpponent(this);
    })
  });



  const homeAwayLabels = document.querySelectorAll('[data-label="home_away"]');
  homeAwayLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      this.classList.toggle('active');
  });
});

  const dayNightLabels = document.querySelectorAll('[data-label="day_night"]');
  dayNightLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      this.classList.toggle('active');
  });
});

  const dayOfWeekLabels = document.querySelectorAll('[data-label="day_of_week"]');
  dayOfWeekLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      this.classList.toggle('active');
  });
});

  const pregameFavorites = document.querySelectorAll('[data-label="pregame_favorites"]');
  pregameFavorites.forEach(label => {
    label.addEventListener('click', function(e) {
      this.classList.toggle('active');
  });
});

  const winStreak = document.querySelectorAll('[data-label="team_1_win_streak"]');
  winStreak.forEach(label => {
    label.addEventListener('click', function(e) {
      winStreak.forEach(label => {
        label.classList.remove('active');
      });
      this.classList.add('active');
    })
  });

  toggleUpButtons.forEach(toggleUpButton => {
    toggleUpButton.addEventListener('click', function(e) {
      const text = e.target.innerText;
      if (text === 'Custom') {
        parentButtonToUpdate = $(this).closest('.dropdown');
        customButton = parentButtonToUpdate.find('#customButton'); // Replace 'this' with the clicked element
        customText = parentButtonToUpdate.find('#customText')[0]; // Replace 'this' with the clicked element
        customButton[0].style.display = 'block';
      } else {
        const parentButton = $(this).closest('.dropdown');
        const btn = parentButton.find('.btn');
        btn.text(text);
        console.log(text);
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
    console.log('clicked');
    filterAndDisplayData();
});

function handleLeagueClick(clickedElement){
  var elements = document.querySelectorAll('.active');
  elements.forEach(function(element) {
      element.classList.remove('active');
  });

  clickedElement.classList.toggle('active');
}

function handleConferenceClick(clickedElement){
  var params = {
    conference: clickedElement.innerHTML
  }

  clickedElement.classList.toggle('active');
  console.log(clickedElement);

  fetch('/get_divisions_teams_from_conference', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
})
.then(response => response.json())
.then(data => {
  data.forEach(function(row) {
    var element = document.querySelector(`[data-label="team_1"][data-value="${row.team}"]`);
    element.classList.toggle('active');
  });
  
})
}

function handleConferenceClickOpponent(clickedElement){
  var params = {
    conference: clickedElement.innerHTML
  }

  clickedElement.classList.toggle('active');

  fetch('/get_divisions_teams_from_conference', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
})
.then(response => response.json())
.then(data => {
  data.forEach(function(row) {
    var element = document.querySelector(`[data-label="opponent"][data-value="${row.team}"]`);
    element.classList.toggle('active');
  });
  
})
}


function handleDivisionClick(clickedElement){
  var element = document.querySelector(`[data-label="this_team_conference"].active`);
  var params = {
    division: clickedElement.innerHTML,
    conference:element.innerHTML
  }

  clickedElement.classList.toggle('active');

  fetch('/get_teams_from_division', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
})
.then(response => response.json())
.then(data => {
  var teams = document.querySelectorAll(`[data-label="team_1"].active`);
  teams.forEach(function(each){
    each.classList.toggle('active');
  })
  data.forEach(function(row) {
    var element = document.querySelector(`[data-label="team_1"][data-value="${row.team}"]`);
    element.classList.toggle('active');
  });
  
})
}

function handleDivisionClickOpponent(clickedElement){
  var element = document.querySelector(`[data-label="opponent_team_conference"].active`);
  console.log(element);
  var params = {
    division: clickedElement.innerHTML,
    conference:element.innerHTML
  }

  clickedElement.classList.toggle('active');
  console.log(clickedElement);

  fetch('/get_teams_from_division', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
})
.then(response => response.json())
.then(data => {
  var teams = document.querySelectorAll(`[data-label="opponent"].active`);
  teams.forEach(function(each){
    each.classList.toggle('active');
  })
  data.forEach(function(row) {
    var element = document.querySelector(`[data-label="opponent"][data-value="${row.team}"]`);
    element.classList.toggle('active');
  });
  
})
}


function filterAndDisplayData() {
  const dictionary = {};
  dictionary['team_1'] = []
  dictionary['this_team_conference'] = []
  dictionary['this_team_division'] = []
  dictionary['day_of_week'] = []

  dictionary['opponent'] = []
  dictionary['opponent_team_conference'] = []
  dictionary['opponent_team_division'] = []
  

  const actives = document.querySelectorAll('a.active');
  actives.forEach(label => {
    console.log(label.getAttribute('data-label'));
    console.log(label.getAttribute('data-value'));
    console.log("------------------");


    if(
      label.getAttribute('data-label') == 'team_1' || 
      label.getAttribute('data-label') == 'conference' || 
      label.getAttribute('data-label') == 'division' || 
      label.getAttribute('data-label') == 'day_of_week'||
      label.getAttribute('data-label') == 'opponent'||
      label.getAttribute('data-label') == 'this_team_conference'||
      label.getAttribute('data-label') == 'opponent_team_conference'||
      label.getAttribute('data-label') == 'this_team_division'||
      label.getAttribute('data-label') == 'opponent_team_division'
      ){
      dictionary[label.dataset.label].push(label.dataset.value)
    }
    else{
      dictionary[label.dataset.label] = label.dataset.value;
    }
  });
  console.log(dictionary)

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
  const xData = parsedData.map(entry => entry.date);
  const yData = parsedData.map(entry => entry.running_sum);
  const dailyPl = parsedData.map(entry => entry.result);

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
      title: 'Running P/L (u)',
      xaxis: {
          title: 'Date'
      },
      yaxis: {
          title: 'Running P/L (u)'
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

function makeTeamElements() {
  $.ajax({
    url: "/get_team_vals_for_scenarios",
    type: "GET",
    dataType: "json",
    success: function(data) {
      const teamsUl = document.getElementById('teams');
      const opponentsUl = document.getElementById('opponents');

      data.forEach(function(row) {
        var customLi = document.createElement('li');
        var customAnchor = document.createElement('a');
        customAnchor.className = 'toggle_up';
        customAnchor.setAttribute('data-label', 'team_1');
        customAnchor.setAttribute('data-value', row.team);
        customAnchor.setAttribute('data-sport', row.sport);
        customAnchor.textContent = row.team; 
        customLi.appendChild(customAnchor);
        teamsUl.appendChild(customLi);

        var customLi2 = document.createElement('li');
        var customAnchor2 = document.createElement('a');
        customAnchor2.className = 'toggle_up';
        customAnchor2.setAttribute('data-label', 'opponent');
        customAnchor2.setAttribute('data-value', row.team);
        customAnchor2.setAttribute('data-sport', row.sport);
        customAnchor2.textContent = row.team; 
        customLi2.appendChild(customAnchor2);
        opponentsUl.appendChild(customLi2);
        
      });

      attachEventListeners();
    }
  });
}

function attachEventListeners() {
  const toggleUpButtons = document.querySelectorAll('.toggle_up');
  const teamLabels = document.querySelectorAll('[data-label="team_1"]');
  teamLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      label.classList.toggle('active');
    });
  });

  const opponentLabels = document.querySelectorAll('[data-label="opponent"]');
  opponentLabels.forEach(label => {
    label.addEventListener('click', function(e) {
      label.classList.toggle('active');
    });
  });

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
}


