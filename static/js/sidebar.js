function redirectFromSideBar(){
  var route = this.querySelector('a').getAttribute('href');
  window.location.href = `/.${route}`;
}

function addSidebarButtons(){
  var liElements = document.querySelectorAll('.sidebar-custom__navigations-links li')
  liElements.forEach(function(liEl){
    liEl.addEventListener('click', redirectFromSideBar)
  })
}

$(document).ready(function(){

  addSidebarButtons();

});
