import json
from .models import Category, Mobilememory, Product, Order, OrderItem, ShippingAddress, SpecialDeals, Specialdealattr
from random import randint, randrange

# def cookieCart(request):
#     try:
#         cart = json.loads(request.COOKIES['cart'])
#     except:
#         cart = {}

#     items=[]
#     special_products = []
#     order = {'get_cart_total':0, 'get_cart_items':0}
#     cartItems = order['get_cart_items']
#     special_deals = SpecialDeals.objects.all()
#     for i in cart:
#         # try:
#         for special_deal in special_deals:
#             special_products.append(special_deal.product_id)
#         quantity_item = cart[i]['quantity']
#         cartItems += quantity_item
#         product  = Product.objects.get(id=i)
#         if i in special_products:
#             special_deal_item = SpecialDeals.objects.get(product = i)
#             total = (special_deal_item.discounted_price * quantity_item)
        
#             order['get_cart_total'] += total
#             order['get_cart_items'] += quantity_item

#             item = {
#                 'product':{
#                     'id': product.id,
#                     'product_title': product.product_title,
#                     'price': special_deal_item.discounted_price,
#                     'image': product.image,
#                 },
#                 'quantity': quantity_item,
#                 'get_total': total,
#             }
#         else:
#             total = (product.price * quantity_item)
            
#             order['get_cart_total'] += total
#             order['get_cart_items'] += quantity_item
#             item = {
#                 'product':{
#                     'id': product.id,
#                     'product_title': product.product_title,
#                     'price': product.price,
#                     'image': product.image,
#                 },
#                 'quantity': quantity_item,
#                 'get_total': total,
#             }

#         items.append(item)
#         # except:
#         #     pass
#     return {'cartItems': cartItems, 'order':order, 'items':items}

def orderItemsCart(request,querySet):
    items=[]
    # special_products = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']
    # special_deals = SpecialDeals.objects.all()
    
    for i in range(0,len(querySet)):
        try:
            # for special_deal in special_deals:
            #     special_products.append(special_deal.product_id)
            cartItems += querySet[i].quantity
            product  = querySet[i].product
            pp  = querySet[i].price

            # if querySet[i].product.id in special_products:
            #     special_deal_item = SpecialDeals.objects.get(product = querySet[i].product)
            #     # for attr in attr:
            #     #      if attr.productsize.description == querySet[i].features:
            #     #         if request.user.profile.user_type == "Retailer":
            #     #             total = (attr.retail_discount_price * querySet[i].quantity)
            #     #         else:
            #     #             total = (attr.discounted_price * querySet[i].quantity)
            #     total = (pp * querySet[i].quantity)
            #     order['get_cart_total'] += total
            #     order['get_cart_items'] += querySet[i].quantity

            #     item = {
            #         'product':{
            #             'id': product.id,
            #             'product_title': product.product_title,
            #             'price': querySet[i].price,
            #             'image': product.image,
            #         },
            #         'quantity': querySet[i].quantity,
            #         'get_total': total,
            #         'features': querySet[i].features,
            #         'colors': querySet[i].colors,
            #         'orderitemid': querySet[i].id

            #     }
            #     # for attr in special_deal_item.specialdealattr_set.all():
            #     #      if attr.productsize.description == querySet[i].features:
            #     #         if request.user.profile.user_type == "Retailer":
            #     #             item['product']['price'] = attr.retail_discount_price
            #     #         else:
            #     #             item['product']['price'] = attr.discounted_price
            # else:
                #total = (product.price * querySet[i].quantity)
            total = (pp * querySet[i].quantity)
            order['get_cart_total'] += total
            order['get_cart_items'] += querySet[i].quantity
            item = {
                'product':{
                    'id': product.id,
                    'product_title': product.product_title,
                    'price': pp,
                    'image': product.image,
                },
                'quantity': querySet[i].quantity,
                'get_total': total,
                'features': querySet[i].features,
                'colors': querySet[i].colors,
                'orderitemid':querySet[i].id
            }
            items.append(item)
        except Exception as e:
            #print(e)
            break
    return {'cartItems': cartItems, 'order':order, 'items':items}

def cartData(request):
    #randint(100, 999)     
    sessionid=randrange(1, 10000)
    if request.session.get('session_id') is not None:
        sessionid=request.session.get('session_id')
    else:
        request.session['session_id'] = sessionid
        sessionid=sessionid
    
    
    if request.user.is_authenticated:
        customer = request.user
        #cookieData = cookieCart(request)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        #cookieData = cookieCart(request)
        order, created = Order.objects.get_or_create(complete=False,sessionid=sessionid)
    
    # if len(cookieData["items"]) > 0:
        # for item in cookieData["items"]:
            # product = Product.objects.get(id=item['product']['id'])
    
            # orderItem, created = OrderItem.objects.get_or_create(
                # product=product,
                # order=order,
                # sessionid=sessionid
            # )
    
            # available_quantity = product.items_in_stock
    
            # if created:
                # orderItem.quantity = item['quantity']
                # orderItem.save()
            # else:
                # orderItem.quantity += item['quantity']
                # if orderItem.quantity >= available_quantity:
                    # orderItem.quantity = available_quantity
                    
                # orderItem.save()
    
    # Fetching data from DB 
    order_items = OrderItem.objects.filter(order=order)
    # Formatted in a way in which the cart is expecting
    cartData = orderItemsCart(request,order_items)
    return {'cartItems': cartData['cartItems'], 'order':cartData['order'], 'items':cartData['items']}        
    # else:
        # # if user is not logged in
        # cookieData = cookieCart(request) 
        # order = cookieData['order']
        # cartItems = cookieData['cartItems']
        # items = cookieData['items']
        # return {'cartItems': cartItems, 'order':order, 'items':items}

        
        
# def guestOrder(request, order):

#     cookieData = cookieCart(request)
#     items = cookieData['items']

#     for item in items:
#         product = Product.objects.get(id=item['product']['id'])

#         orderItem = OrderItem.objects.create(
#             product = product,
#             order = order,
#             quantity = item['quantity']
#         )

def clearCookie(request,response):
    if request.user.is_authenticated:
        response.delete_cookie("cart")
        # del request.session['session_id']
    # else:
        # del request.session['session_id']
    return response