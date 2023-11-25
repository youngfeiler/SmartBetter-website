document.querySelectorAll('.scroll-link').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href').substring(1);
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop,
        behavior: 'smooth'
      });
    }
  });
});


function trackClickButtonEvent99() {
  ttq.track('ClickButton', {
    "contents": [
      {
        "content_type": "Get Started Button",
        "content_name": "$99 Box" 
      }
    ]
  });
}

function trackClickButtonEvent199() {
  ttq.track('ClickButton', {
    "contents": [
      {
        "content_type": "Get Started Button",
        "content_name": "$199 Box" 
      }
    ]
  });
}

function trackClickButtonEventFree() {
  ttq.track('ClickButton', {
    "contents": [
      {
        "content_type": "Get Started Button",
        "content_name": "Trial Link" 
      }
    ]
  });
}

const trackButton99 = document.getElementById('get-started-99');
const trackButton199 = document.getElementById('get-started-199');
const trackButtonFree = document.getElementById('get-started-free');


trackButton99.addEventListener('click', function(event) {
  trackClickButtonEvent99();
});

trackButton199.addEventListener('click', function(event) {
  trackClickButtonEvent199();
});

trackButtonFree.addEventListener('click', function(event) {
  trackClickButtonEventFree();
});