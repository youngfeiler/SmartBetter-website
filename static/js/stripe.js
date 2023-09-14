var stripe = Stripe(checkout_public_key);
const button = document.querySelector('a[str="button"]');
button.addEventListener("click", () => {
    print('clicked');
    stripe.redirectToCheckout({
        sessionId: checkout_session_id
    }).then(function (result) {
        console.log(result);
    });

});