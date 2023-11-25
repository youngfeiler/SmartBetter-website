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
              "content_name": "Subscription",
              "content_id":"non_id"
            }
          ],
          "value": price,
          "currency": currency
        });
  }
}


function hashString(str) {
  const hashedString = CryptoJS.SHA256(str).toString(CryptoJS.enc.Hex);
  return hashedString;
}



document.addEventListener('DOMContentLoaded', function() {
  const myButton = document.getElementById('TEST-BUTTON');
  myButton.addEventListener('click', extractAndTrackPaymentInfo);

})