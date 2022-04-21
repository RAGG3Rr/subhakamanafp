var updateBtns = document.getElementsByClassName('update-cart')

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        var itemQuantity = this.dataset.quantity
        var newprice = this.dataset.price
        var color = this.dataset.color
        itemQuantity = parseInt(itemQuantity)
        newprice = parseFloat(newprice)
		console.log(itemQuantity);
        var remStocks;
		updateUserOrder(productId, action, itemQuantity,newprice,color)
		
        // var url = './stock/' + productId;
        //console.log('productId:', productId, 'action:', action, 'itemQuantity:', itemQuantity)

        /* $.ajax({
            type: 'GET',
            url: '/stock/' + productId,
            data: {},
            dataType: 'json',
            success: function (data) {
                remStocks = data.data
                if (user == 'AnonymousUser') {
                    addCookieItem(productId, action, remStocks, itemQuantity)
                } else {
                    updateUserOrder(productId, action, itemQuantity)
                }
            },
        }); */
    })
}

function addCookieItem(productId, action, remStocks, itemQuantity) {
    console.log(cart);
    cart[productId] = { 'quantity': itemQuantity }
    if (action == 'add') {
        if (remStocks > 0) {
            if (cart[productId] == undefined) {
                cart[productId] = { 'quantity': itemQuantity }
            } else {
                if (cart[productId]['quantity'] + itemQuantity <= remStocks) {
                    cart[productId]['quantity'] += itemQuantity
                }
                else {
                    alert('Sorry, only ' + remStocks + ' items in stock!')
                }
            }
        }
        else {
            alert('Sorry, no more items in stock!')
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
		//console.log(cart);
        if (cart[productId]['quantity'] <= 0) {
            //console.log('Remove Item')
            delete cart[productId]
        }
    }

    //console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action, itemQuantity,newprice,usrcolor) {
    console.log(newprice)

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action, 'quantity': itemQuantity,'price':newprice,'usrcolor':usrcolor })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            //console.log('data:', data);
            location.reload()
        })
}