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
        var feature = this.dataset.feature
        var usertype = this.dataset.user
        var specattr = this.dataset.discount
        itemQuantity = parseInt(itemQuantity)
        newprice = parseFloat(newprice)
        feature = parseInt(feature)
        color = parseInt(color)
        specattr = parseInt(specattr)
        
        var remStocks;
		updateUserOrder(productId, action, itemQuantity,newprice,color,feature,usertype,specattr)
    })
}

function addCookieItem(productId, action, remStocks, itemQuantity) {
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
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }

    //console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action, itemQuantity,newprice,usrcolor,feature,usertype,specattr) {
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action, 'quantity': itemQuantity,'price':newprice,'usrcolor':usrcolor,'feature':feature,'usertype':usertype,'specattr':specattr })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            $('#cart-total').text(data)
            $("#cartmodal").modal("show")
        })
}