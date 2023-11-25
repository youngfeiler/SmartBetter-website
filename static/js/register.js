function trackPurchaseEventToTikTok(value, currency) {
  ttq.track('CompletePayment', {
    "contents": [
      {
        "content_type": "Subscription",
        "content_name": "Subscription" 
      }
    ],
    "value": value,
    "currency":currency
  });
}

function extractAndTrackPaymentInfo() {
  const urlParams = new URLSearchParams(window.location.search);
  console.log("console logging:");
  console.log(urlParams);
  // const sessionID = urlParams.get('session_id');
  // const amount = urlParams.get('amount');
  // const currency = urlParams.get('currency');
  // const userEmail = urlParams.get('email'); 
  // const userPhoneNumber = urlParams.get('phone_number'); 
  // const externalID = urlParams.get('external_id'); 
  // if (sessionID && amount && currency) {
  //   trackPurchaseEventToTikTok(amount, currency);
  // }

  // // Identify hashed user information
  // ttq.identify({
  //   "email": userEmail ? userEmail : "<hashed_email_address>",
  //   "phone_number": userPhoneNumber ? userPhoneNumber : "<hashed_phone_number>",
  //   "external_id": externalID ? externalID : "<hashed_external_id>"
  // });

  // // Track 'CompletePayment' event
  // ttq.track('CompletePayment', {
  //   "contents": [
  //     {
  //       "content_type": "<content_type>", // Replace with actual content type (e.g., product or product_group)
  //       "content_name": "<content_name>" // Replace with actual content name (e.g., shirt)
  //     }
  //   ],
  //   "value": amount ? amount : "<content_value>", // Use extracted amount or fallback to default
  //   "currency": currency ? currency : "<content_currency>" // Use extracted currency or fallback to default
  // });
}

// Call the function to extract and track payment information when the page loads
window.onload = function() {
  extractAndTrackPaymentInfo();
};