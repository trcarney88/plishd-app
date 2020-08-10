// Set up Stripe.js and Elements to use in checkout form
var style = {
base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
    color: "#aab7c4"
    }
},
invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
}
};

var cardElement = elements.create("card", { style: style });
cardElement.mount("#card-element");

cardElement.addEventListener('change', ({error}) => {
const displayError = document.getElementById('card-errors');
if (error) {
    displayError.textContent = error.message;
} else {
    displayError.textContent = '';
}
});

function showCardError(error) {
    changeLoadingState(false);
    // The card was declined (i.e. insufficient funds, card has expired, etc)
    var errorMsg = document.querySelector('.sr-field-error');
    errorMsg.textContent = error.message;
    setTimeout(function() {
        errorMsg.textContent = '';
    }, 8000);
};
// Show a spinner on payment submission
var changeLoadingState = function(isLoading) {
    if (isLoading) {
        document.querySelector("#pay_btn").disabled = true;
        document.querySelector("#pay_btn").classList.remove("btn-outline-info");
        document.querySelector("#pay_btn").classList.add("btn-info")
      
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("#pay_btn").disabled = false;
        document.querySelector("#pay_btn").classList.add("btn-outline-info");
        document.querySelector("#pay_btn").classList.remove("btn-info")

        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
};

var form = document.getElementById('subscription-form');

form.addEventListener('submit', function(event) {
    // We don't want to let default form submission happen here,
    // which would refresh the page.
    event.preventDefault();
    // Show a spinner on the pay/subscribe button
    changeLoadingState(true)
    stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
        billing_details: {
        email: email,
        },
    }).then(stripePaymentMethodHandler);
    });
function stripePaymentMethodHandler(result, email) {
    if (result.error) {
        // Show error in payment form 
        console.log(result.error)
        showCardError(result.error)
    } else {
        // Otherwise send paymentMethod.id to your server
        document.getElementById("payment-method").setAttribute("value", result.paymentMethod.id)
    }

    form.submit();
}