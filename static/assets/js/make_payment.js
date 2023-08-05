


function payWithPaystack(e) {
    e.preventDefault();
    fetch("{% url 'initiate-payment' %}")
    .then((res) => {
        return res.json();
    }).then((data) => {
        console.log(data)
        //payWithPaystack(data)
    }).catch((err) => {
        console.log(err)
    })
}

    let handler = PaystackPop.setup({
        key: {{ paystack_public_key }}, // Replace with your public key
        email: {{ user.email }},
        amount: document.getElementById("amount").value * 100,
        ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
        // label: "Optional string that replaces customer email"
        onClose: function(){
        alert('Window closed.');
        },
        callback: function(response){
        let message = 'Payment complete! Reference: ' + response.reference;
        alert(message);
        }
});

   // handler.openIframe();
    


