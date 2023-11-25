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
    
    Promise.all([hashString(email), hashString(phoneNumber)])
      .then(([hashedEmail, hashedPhoneNumber]) => {
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
      })
      .catch(error => {
        console.error('Error while hashing:', error);
      });
  }
}


async function hashString(str) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  const hash = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hash));
  const hashedString = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashedString;
}

document.addEventListener('DOMContentLoaded', function() {
  const myButton = document.getElementById('TEST-BUTTON');
  myButton.addEventListener('click', extractAndTrackPaymentInfo);

})