function extractAndTrackPaymentInfo() {
  const urlParams = new URLSearchParams(window.location.search);
  const price = urlParams.get('price');
  const currency = "USD";
  const phoneNumberInput = document.getElementById('phone_number');
  const emailInput = document.getElementById('email');
  console.log("clicked")
  
  if (price && currency && phoneNumberInput && emailInput) {
    const phoneNumber = phoneNumberInput.value;
    const email = emailInput.value;
    
    hashedEmail = hashString(email);
    hashedPhoneNumber = hashString(phoneNumber);
    ttq.identify({
          "email": hashedEmail,
          "phone_number": hashedPhoneNumber,
          "external_id": "none"
    });

    console.log(hashedEmail);
    console.log(hashedPhoneNumber);

    ttq.track('CompletePayment', {
          "contents": [
            {
              "content_type": "Subscription",
              "content_name": "Subscription" 
            }
          ],
          "value": price,
          "currency": currency
        });
  }
}


function hashString(str) {
  const shaObj = new jsSHA('SHA-256', 'TEXT');
  shaObj.update(str);
  return shaObj.getHash('HEX');
}


document.addEventListener('DOMContentLoaded', function() {
  const myButton = document.getElementById('TEST-BUTTON');
  myButton.addEventListener('click', extractAndTrackPaymentInfo);

})