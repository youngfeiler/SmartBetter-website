
document.addEventListener("DOMContentLoaded", function () {
const toggleButton = document.getElementById("cancel-subscription-button");

toggleButton.addEventListener("click", function () {
    // print something to console
    console.log("Cancel subscription button clicked!");
    // Send an AJAX request to Flask to cancel the subscription
    fetch("/cancel_subscription", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ action: "cancel" }), // You can send any data you need
    })
    .then((response) => response.json())
    .then((data) => {
        // Handle the response from Flask, e.g., display a success message
        if (data.success) {
        alert("Subscription canceled successfully.");
        } else {
        alert("Failed to cancel subscription. Please try again.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});
});