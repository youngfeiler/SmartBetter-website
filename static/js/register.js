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
  for (const [key, value] of urlParams) {
    console.log(`${key}: ${value}`);
  }

  const price = urlParams.get('price');
  const currency = "USD"
  if (urlParams && price && currency) {
    trackPurchaseEventToTikTok(price, currency);
  }
}

window.onload = function() {
  extractAndTrackPaymentInfo();
};