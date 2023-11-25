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


function initiateCheckout(event, price_id) {
  event.preventDefault(); // Prevent the default link behavior (i.e., navigating to href)

  fetch('/create_checkout_session/' + price_id)
    .then(response => response.json())
    .then(data => {
      // Redirect the user to the Stripe Checkout Session URL
      window.location.href = data.checkout_session_url;
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle errors or show a message to the user
    });
}