function submitQuestion(){

  const inputValue = $('#input-box').val();

  addQuestionToDisplay(inputValue);

  clearInput();

  addResponseToDisplay();

  $.ajax({
      url: '/handle_chat',
      method: 'POST',
      data: { text: inputValue },
      success: function(response) {
        fillResponse(response);
      },
      error: function(error) {
          console.error('Error:', error);
      }
  });
}

function addQuestionToDisplay(question){
  const conversation = document.getElementsByClassName("conversation")[0];

  const userMessageBox = document.createElement('div');

  const icon = document.createElement('div');
  icon.classList.add("user-circle-container")
  icon.innerHTML = `<svg class = "user-circle">
                      <circle cx="10" cy="10" r="10"/>
                    </svg> `

  const message = document.createElement('div');
  message.classList.add("message");

  const you = document.createElement('div');
  you.classList.add("you");

  you.innerText = "You";

  const messageText = document.createElement('div');
  messageText.classList.add("question");



  messageText.innerText = question;
  
  userMessageBox.classList.add("user-message-box");
  userMessageBox.classList.add('user-message');

  userMessageBox.append(icon);
  userMessageBox.append(message);

  message.append(you);
  message.append(messageText);

  conversation.prepend(userMessageBox);


  conversation.scrollTop = conversation.scrollHeight;


}

function addResponseToDisplay(){
  const conversation = document.getElementsByClassName("conversation")[0];

  const userMessageBox = document.createElement('div');

  const icon = document.createElement('div');
  icon.classList.add("user-circle-container")
  icon.innerHTML = `<svg class = "gpt-circle">
                      <circle cx="10" cy="10" r="10"/>
                    </svg> `

  const message = document.createElement('div');
  message.classList.add("message");

  const you = document.createElement('div');
  you.classList.add("you");
  you.innerText = "SportGPT";

  const messageText = document.createElement('div');
  messageText.classList.add("question");

  messageText.id = "chat-response";
  const img = document.createElement("img");
  img.id = "chat-img"
  img.src = "/static/images/loading-dots-2.gif";
  messageText.appendChild(img)
  
  userMessageBox.classList.add("user-message-box");
  userMessageBox.classList.add('user-message');

  userMessageBox.append(icon);
  userMessageBox.append(message);

  message.append(you);
  message.append(messageText);

  conversation.prepend(userMessageBox);

  conversation.scrollTop = conversation.scrollHeight;

}

function fillResponse(response){

  const img = document.getElementById("chat-img");

  const messageText = document.getElementById("chat-response");

  messageText.removeChild(img);

  messageText.innerText = response;

}

function handleEnterKeyPress(event) {
  if (event.key === 'Enter') {
    submitQuestion();
  }
}

function clearInput(){
  var inputElement = document.getElementById("input-box");
  
  inputElement.value = "";

  return;
}



$(document).ready(function(){

  const submit = document.querySelector(".submit-button");
  submit.addEventListener('click', submitQuestion);
  document.addEventListener('keypress', handleEnterKeyPress);


});