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


function trackClickButtonEvent() {
  ttq.track('ClickButton', {
    "contents": [
      {
        "content_type": "get started",
        "content_name": "99 version" 
      }
    ]
  });
}
const trackButton = document.getElementById('get-started-id');

trackButton.addEventListener('click', function(event) {
  trackClickButtonEvent();
});