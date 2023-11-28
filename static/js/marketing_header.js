document.addEventListener('DOMContentLoaded', function() {
  const downArrow = document.querySelector('.down-arrow');
  const displayElement = document.querySelector('.column-mh');
  const chev = document.querySelector('.down-arrow');
  var clicked = false;

  downArrow.addEventListener('click', function() {
      if(clicked == false){
        displayElement.style.display = 'flex';
        clicked =  true;
        chev.src = ('static/images/chevron-up.svg');

      }else{
        displayElement.style.display = "none";
        clicked = false;
        chev.src = ('static/images/chevron-down.svg');

      }
  });
});
