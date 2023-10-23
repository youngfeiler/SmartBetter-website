document.addEventListener('DOMContentLoaded', function() {
  const dropdownButton = document.querySelector('.dropdown-button');
  const mainMenu = document.querySelector('.main-menu');

  dropdownButton.addEventListener('click', function() {
      mainMenu.classList.toggle('active');
  });

  const submenuButtons = document.querySelectorAll('.submenu .dropdown-button');

  submenuButtons.forEach(submenuButton => {
      submenuButton.addEventListener('click', function() {
          this.parentElement.classList.toggle('active');
  
          // Get the unique identifier for the submenu
          const submenuIdentifier = this.parentElement.getAttribute('data-submenu');
  
          if (submenuIdentifier) {
              // Toggle the "selected" class on li elements within the submenu with the matching identifier
              const finalSubmenu = document.querySelector(`.final.${submenuIdentifier}`);
              if (finalSubmenu) {
                  const liElements = finalSubmenu.querySelectorAll('li');
                  liElements.forEach(li => {
                      li.classList.toggle('selected');
                  });
              }
          }
      });
  });


  const backButtons = document.querySelectorAll('.back');

  backButtons.forEach(backButton => {
      backButton.addEventListener('click', function(e) {
          e.preventDefault();
          const submenu = this.closest('.submenu');
          submenu.classList.remove('active');
      });
  });
});