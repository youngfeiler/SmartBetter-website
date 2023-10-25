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

document.addEventListener('DOMContentLoaded', function() {
  const toggleUpButtons = document.querySelectorAll('.toggle_up');
  const customButton = document.getElementById('customButton');
  const customText = document.getElementById('customText');
  const submitCustom = document.getElementById('submitCustom');
  let parentButtonToUpdate; // Store a reference to the parent button

  toggleUpButtons.forEach(toggleUpButton => {
    toggleUpButton.addEventListener('click', function(e) {
      const text = e.target.innerText;
      if (text === 'Custom') {
        parentButtonToUpdate = $(this).closest('.dropdown');
        customButton.style.display = 'block';
      } else {
        const parentButton = $(this).closest('.dropdown');
        const btn = parentButton.find('.btn');
        btn.text(text);
        customButton.style.display = 'none';
      }
    });
  });

  submitCustom.addEventListener('click', function() {
    const customButtonText = customText.value;
    if (parentButtonToUpdate) {
      const btn = parentButtonToUpdate.find('.btn');
      btn.text(btn.text()+ " greater than " + customButtonText);
      customButton.style.display = 'none';
    }
  });
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


