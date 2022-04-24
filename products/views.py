from multiprocessing import context
from re import template
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.db.models import Avg
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .utils import  cartData, clearCookie
from django.contrib.auth import authenticate, login
from .forms import *
from .decorators import allowed_users
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from nationalmobile.settings import BASE_DIR
import os
from pathlib import Path
from django.template import loader, Context
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import timedelta
from django.db.models import F, Q, Count
from users.models import Profile
from decimal import Decimal
from random import randint, randrange
from django.core.mail import send_mail
from nationalmobile.settings import EMAIL_HOST_USER
# from django.core import mail
# from django.contrib.sites.shortcuts import get_current_site
# from users.models import Subscription
# from django.utils.html import strip_tags


# Create your views here.

    
def home(request):
    template = "products/index.html"
    
    special_deals=SpecialDeals.objects.all()
    for i in special_deals:
        if i.no_of_days !=None:
            limited_days=timezone.now() - timedelta(i.no_of_days)
            if i.added_date<limited_days:
                special_deals=special_deals.exclude(id=i.id)
                # SpecialDeals.objects.filter(id=i).delete()
    trending_items = Trending.objects.filter(product__on_sale=False)
    slideshow_images = Slideshow.objects.all()
    poster = Poster.objects.all().order_by('-id')
    custom_items = CustomTable.objects.filter(product__on_sale=False)
    custom_name = CustomTableName.objects.last()
    new_arrivals = Product.nosale.all()[:20]
    features = Mobilememory.objects.all()

    context={
        'special_deals': special_deals, 
        'trending_items':trending_items,
        'slideshow_images' : slideshow_images,
        'poster': poster,
        'custom_items': custom_items,
        'custom_name': custom_name,
        'new_arrivals': new_arrivals,
        'features':features
    }

    if request.session.get('order_success') is not None:
        messages.success(request, f'Your Order has been placed successfully!!!')
        del request.session['order_success']
    response = render(request, template, context)
    return clearCookie(request,response)

def pricerange(request):
    title = request.GET.get('title')
    main_category_id = request.GET.get('main_category_id')
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    sub_category_item = request.GET.get('sub_category_item')
    specific_category_item = request.GET.get('specific_category_item')
    #print(main_category_id,min,max,sub_category_item,specific_category_item)
    
    if sub_category_item:
        pro=Product.objects.filter(sub_category_id = sub_category_item)
    elif specific_category_item:
        pro = Product.objects.filter(specific_category_id = specific_category_item)
    else: 
      if main_category_id == '0':
          pro = Product.objects.all()  
      else:
          pro= Product.objects.filter(main_category_id= main_category_id)
    
    if min == '' and max =='':
        #print('here')
        high_to_low=pro 
    elif min == '':
        high_to_low=pro.filter(price__lte=max)
    elif max == '':
        high_to_low=pro.filter(price__gte=min)
    
    else:
        high_to_low=pro.filter(price__gte=min,price__lte=max)
    #print(high_to_low)
    template = "products/all.html"
    
    id=main_category_id
    data = 'All'

    context={
        'id': id,
        'items':high_to_low,
        'title': title,
        'data': data,
    }
    return render(request, template, context)

def onsalefilter(request):
    orderedproduct= []
    if request.is_ajax():
        main_category_id = request.GET.get('main_category_id')
        check = request.GET.get('check')
        sub_category_item = request.GET.get('sub_category_item')
        specific_category_item = request.GET.get('specific_category_item')
        
        if sub_category_item:
            pro=Product.objects.filter(sub_category_id = sub_category_item)
        elif specific_category_item:
            pro = Product.objects.filter(specific_category_id = specific_category_item)
        else: 
            if main_category_id == '0':
                pro = Product.objects.all()  
            else:
                pro= Product.objects.filter(main_category_id= main_category_id)
        if check == 'true' :
            high_to_low = pro.filter(on_sale = True)
            sale = 'sale'
        else:
            high_to_low = pro.filter(on_sale = False)
            sale = None

        template = loader.get_template('products/all.html')
        context = {'items':  high_to_low,'onsale': sale}
        html = template.render(request=request, context=context)
        return HttpResponse(html)

    return JsonResponse(list(high_to_low.values('id', 'product_title')), safe=False) 
    
def highToLow(request):
    orderedproduct= []
    if request.is_ajax():
        main_category_id = request.GET.get('main_category_id')
        check = request.GET.get('check')
        sub_category_item = request.GET.get('sub_category_item')
        specific_category_item = request.GET.get('specific_category_item')
        
        if sub_category_item:
            pro=Product.objects.filter(sub_category_id = sub_category_item)
        elif specific_category_item:
            pro = Product.objects.filter(specific_category_id = specific_category_item)
        else: 
            if main_category_id == '0':
                pro = Product.objects.all()  
            else:
                pro= Product.objects.filter(main_category_id= main_category_id)
        
        
        if check == 'Random':
            high_to_low = pro
        elif check == 'Price: Low to High':
            high_to_low = pro.filter().order_by('price')
        elif check == 'Price: High to Low':
            high_to_low = pro.filter().order_by('-price')
        elif check == 'Recent Products':
            high_to_low = pro.filter().order_by('-id')
        elif check == 'Popular Products':
            ordercount = OrderItem.objects.values("product").annotate(Count("product"))
            ordercount = sorted(ordercount, key = lambda i: i['product__count'],reverse=True)
            for i in ordercount:
                orderedproduct.append(i['product'])
            #print(orderedproduct)
            high_to_low = pro.filter(id__in=orderedproduct)
        #print(aa)  
        template = loader.get_template('products/all.html')
        context = {'items':  high_to_low}
        html = template.render(request=request, context=context)
        return HttpResponse(html)

    return JsonResponse(list(high_to_low.values('id', 'product_title')), safe=False)    
 
@csrf_exempt 
def loginuser(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'The user does not exist.')
            return redirect('register')
    else:
        form = LoginForm()

def productDetail(request, slug):
    template="products/detail.html"
    
    product = Product.objects.get(slug=slug)
    related_id = product.sub_category_id
    if product.on_sale == True:
        related_items = Product.objects.filter(sub_category_id = related_id , on_sale = True)
    else:
        related_items = Product.objects.filter(sub_category_id = related_id , on_sale = False)
    id=product.id
    features = Mobilememory.objects.filter(product=id)
    c=product.colors
    color=[]
    if c:
        col = ''.join(str(c).split(','))
        color = Colors.objects.filter(id__in=col)
    
    try:
        special_deal = SpecialDeals.objects.get(product_id  = id)
    except SpecialDeals.DoesNotExist:
        special_deal = None

    # sizes = Size.objects.get(products_id = id)
    # available_sizes = sizes.objects.filter()

    related_products = []
    for i in related_items:
        if product.id == i.id:
            continue
        else:
            related_products.append(i)
    
    form = ReviewForm(request.POST or None)

    reviews = Review.objects.filter(products=id)
    avg_rating = reviews.aggregate(Avg('rating')).get('rating__avg')
    if avg_rating == None:
        avg_rating = 0

    if request.method == "POST":
        if form.is_valid():
            data = Review()
            data.products = Product.objects.get(pk=id)
            data.review = form.cleaned_data['comment']
            data.rating = form.cleaned_data['rate']
            current_user= request.user
            data.user_id = current_user.id
            data.save()
        else:
            messages.error(request, f'Do not leave any fields unattended.')

    context={
        'product': product,
        'form': form,
        'reviews':reviews,
        'avg_rating':avg_rating,
        'related_items': related_products,
        'special_deal': special_deal,
        'features': features,
        'color': color,
    }

    return render(request, template, context)

def specialDeal(request):
    template = "products/special_deals.html"
    special_deals = SpecialDeals.objects.filter(product__on_sale = True)

    context={
        'special_deals': special_deals,
        'title': "Special Deals",
        'check': 'sale'
    }

    return render(request, template, context)

def customItems(request):
    template = "products/special_deals.html"

    custom_items = CustomTable.objects.filter(product__on_sale = False)
    custom_name = CustomTableName.objects.last()

    context={
        'special_deals': custom_items,
        'title': custom_name,
        'check': 'productrel'
    }

    return render(request, template, context)
    
def newItems(request):
    template = "products/special_deals.html"

    new_items = Product.nosale.all()[:20]

    context={
        'special_deals': new_items,
        'title': "New Arrivals",
        'check': 'nosale'
    }

    return render(request, template, context)

def trendingItems(request):
    template = "products/special_deals.html"
    special_deals = Trending.objects.filter(product__on_sale = False)

    context={
        'special_deals': special_deals,
        'title': "Trending Now",
        'check': 'productrel'
    }

    return render(request, template, context)

def categories(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    #print(items)
    items_stock = Product.objects.filter(items_in_stock = 0)

    return {
        'categories': Category.objects.all(),
        'main_categories':  Category.objects.filter(display = True)[:5],
        'sub_categories': SubCategory.objects.all(),
        'specific_category': SpecificCategory.objects.all(),
        'all_products': Product.objects.all(),
        'cartItems':cartItems,
        "order":order,
        "items":items,
        'items_stock': items_stock
    }

def subCategoryDetail(request, mainslug ,slug):
    obj = SubCategory.objects.get(slug=slug)
    maincat = Category.objects.get(slug= mainslug)
    sub_item = Product.objects.filter(main_category=maincat, sub_category=obj.id,on_sale = False)
    template = "products/all.html"

    sub_category_item = obj.id
    id=obj.id
    #id = obj.main_category_id
    #maincategory = obj.main_category #Category.objects.get(id=id)
    title = obj.main_category

    context={
        'id': id,
        'items': sub_item,
        'title':title,
        'data': obj,
        'sub_category_item': sub_category_item,
    }
    return render(request, template, context)

def allProducts(request):
    all_products = Product.objects.all()
    template = "products/all.html"
    title = "Products"
    data = "All"
    product_id = 0

    context={
        'items': all_products,
        'title': title,
        'data': data,
        'id': product_id,
    }
    return render(request, template, context)

def specificCategoryDetail(request,mainslug,subslug, slug):
    obj = SpecificCategory.objects.get(slug=slug)
    subslug= SubCategory.objects.get(slug=subslug)
    mainslug= Category.objects.get(slug= mainslug)
    specific_item = Product.objects.filter(main_category=mainslug,sub_category=subslug,specific_category=obj, on_sale=False)
    template = "products/all.html"
    #obj = SpecificCategory.objects.get(id=obj.id)

    specific_category_item = obj.id
    
    id = obj.main_category.id
    category = Category.objects.get(id = id)
    category_name = category.main_category

    data = SubCategory.objects.get(id=obj.sub_category.id)

    context={
        'title': category_name,
        'items':specific_item,
        'id':id,
        'data': data,
        'specific_category_item': specific_category_item,
    }
    return render(request, template, context)

def categoryDetail(request, slug):
    #id = Category.objects.get(slug=slug)
    title = Category.objects.get(slug=slug)
    category_item = Product.objects.filter(main_category=title.id, on_sale = False)
    template = "products/all.html"
    id=title.id
    data = 'All'

    context={
        'id': id,
        'items':category_item,
        'title': title,
        'data': data,
    }
    return render(request, template, context)

def cart(request):
    template= "products/cart.html"
    
    
    return render(request, template)

def getSubcategories(request):
    main_category_id = request.GET.get('main_category_id')
    sub_dropdown = SubCategory.objects.filter(main_category = main_category_id)

    return JsonResponse(list(sub_dropdown.values('id', 'sub_category','Add_features')), safe=False)

def getSpecificcategories(request):
    sub_category_id = request.GET.get('sub_category_id')
    specific_dropdown = SpecificCategory.objects.filter(sub_category = sub_category_id)

    return JsonResponse(list(specific_dropdown.values('id', 'specific_category')), safe=False)

def getspecialdeals(request):
    getid = request.GET.get('getid')
    size = Mobilememory.objects.filter(product = getid)

    return JsonResponse(list(size.values('id','description')), safe=False)

@csrf_exempt
def checkout(request):
    data = cartData(request)
    items = data['items']

    if request.user.is_authenticated:
        form = Profile.objects.get(id= request.user.profile.id)
    else:
        form = {}
    
    if items:
        template= "products/checkout.html"
  
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        shipping = ShippingCharges.objects.first()
        shipping_charge = shipping.charges
        total = list(order.values())[0]
        
        grand_total = total + shipping_charge

        context={
            'items':items,
            'order':order,
            'cartItems':cartItems,
            'shipping': shipping_charge,
            'grand_total': grand_total,
        }
    else:
        messages.error(request, f'You have no items in your cart.')
        return redirect('cart')

    context={
        'shipping': shipping_charge,
        'grand_total': grand_total,
        'p_form':form,
    }

    response = render(request, template, context)
    return clearCookie(request,response)

def checkStock(request, id):
    stock = Product.objects.get(id = id)
    remaining_stocks = stock.items_in_stock

    return JsonResponse({
        'data': remaining_stocks
    })

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    price = data['price']
    feature = data['feature']
    color = data['usrcolor']
    usertype = data['usertype']
    specattr = data['specattr']

    try:
        itemQuantity = data['quantity']
    except:
        itemQuantity = 1

    sessionid=request.session.get('session_id')
    customer = request.user
    product = Product.objects.get(id=productId)
        
    try:
        f=Mobilememory.objects.get(id=feature)
        feature=f.description

    except:
        feature=[]

    try:
        specialdeal=SpecialDeals.objects.get(product=product)
    except:
        specialdeal = None

    try:
        specialdealattr = Specialdealattr.objects.get(id=specattr)
    except :
        specialdealattr = None

    if (specialdeal):
        if usertype == 'Retailer':
            price = specialdealattr.retail_discount_price
        elif usertype == 'Normal':
            price = specialdealattr.discounted_price
        else:
            price=product.discounted_price            
    else:
        if usertype == 'Retailer':
            price = f.retailprice
        elif usertype == 'Normal':
            price = f.price
        else:
            price=f.price

    try:
        col = Colors.objects.get(id= color)
        color = col.name
    except:
        color= []

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product,features=feature,colors=color) 
    else:
        order, created = Order.objects.get_or_create(sessionid=sessionid, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product,features=feature,colors=color,sessionid=sessionid)   
    available_stock = product.items_in_stock 
    
    if orderItem.price == 0 or orderItem.price == '':
        orderItem.price = price
    # elif orderItem.price != price:
        # if price is not None:
            # orderItem.price = price
        # else:
            # pass
    if action == 'add':
        # if orderItem.quantity >= available_stock or available_stock == 0:
            # messages.error(request, f'Sorry, no more items in stock!')
        # elif orderItem.quantity + itemQuantity > available_stock:
            # messages.error(request, 'Sorry, only {} items in stock.'.format(available_stock))
        # else:
        orderItem.quantity = (orderItem.quantity + itemQuantity)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    # if usercolor:
    #     orderItem.colors= usercolor or None
    orderItem.name=product.product_title or None
    if orderItem.features == None:
        orderItem.features=feature or None
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    data = cartData(request)
    order = data['order']
    totalitem = order["get_cart_items"]

    return JsonResponse(totalitem, safe=False)

def itemdelete(request):
    product_id = request.GET.get('product_id')
    orderitem_id = request.GET.get('oitemid')
    user_id = request.user.id
    sessionid=request.session.get('session_id')

    if user_id is None:
        order_id = Order.objects.get(sessionid = sessionid, complete=False)
    else:
        order_id = Order.objects.get(customer_id = user_id, complete=False)
    remove = OrderItem.objects.filter(id= orderitem_id,order_id = order_id, product_id = product_id)
    for obj in remove:
        obj.delete()

    return JsonResponse('Item was removed', safe=False)

# def processOrder(request):
    # transaction_id = datetime.datetime.now().timestamp()
    # data = json.loads(request.body)
    # items_total = 0
    # sessionid=request.session.get('session_id')
    
    # if request.user.is_authenticated:
        # customer = request.user
        # #order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # order = Order.objects.get(customer=customer, complete=False)
    # else:
        # User.objects.create(
        # first_name = data['form']['firstname'],
        # last_name = data['form']['lastname'],
        # email = data['form']['email'],
        # is_active=False,
        # is_staff=False,
                    # #phone_no=data['form']['phone_no']
        # username=data['form']['firstname'],
        # password='',
        # )
        
        # obj=Profile.objects.last()
        # obj.refresh_from_db()
        # obj=Profile.objects.last()
        # obj.phone_no= data['form']['phone_no']
        # obj.save()
        
        # customer=User.objects.last()
        # Order.objects.filter(sessionid=sessionid, complete=False).update(customer=customer)
        # order = Order.objects.get(customer=customer, complete=False,sessionid=sessionid)
    # #Ordtatus.objects.create(
    # OrderStatus.objects.create(
        # order = order,
        # order_status = 'Pending',
    # )

    # obj = OrderItem.objects.filter(order_id = order.id)    

    # special_deals = SpecialDeals.objects.all()
    # special_products = []
    # for special_deal in special_deals:
        # special_products.append(special_deal.product_id)
    # for i in obj:
        # product_obj = Product.objects.get(id=i.product_id)
        # try:
            # special_deal_item = SpecialDeals.objects.get(product = i.product_id)
        # except:
            # pass
        # if i.product_id in special_products:
            # OrderItem.objects.filter(pk = i.id).update(name = product_obj.product_title, price = special_deal_item.discounted_price)
        # else:
            # OrderItem.objects.filter(pk = i.id).update(name = product_obj.product_title, price = product_obj.price)

    

    # ####################### update stock of products after order processing ################
    # # obj2 = OrderItem.objects.filter(order_id = order.id)
    # # for i in obj2:
        # # product_obj = Product.objects.get(id=i.product_id)
        # # items_price = i.price
        # # items_total =+ items_price
        # # items_available = product_obj.items_in_stock
        # # quantity_ordered = i.quantity
        # # updated_stock = items_available - quantity_ordered
        # # Product.objects.filter(pk=i.product_id).update(items_in_stock = updated_stock)

    # #Confirm total regardless of who is checking out  
    # order.transaction_id = transaction_id
    
    # # if total == float(items_total):
    # order.complete = True
    # order.save()

    # ShippingAddress.objects.create(
            # customer =customer,
            # order = order,
            # address = data['shipping']['address'],
            # city = data['shipping']['city'],
            # state = data['shipping']['state'],
            # zipcode = data['shipping']['zipcode'],
            # phone = data['shipping']['phone'],
    # )
    # try:
        # confirmationEmail(request, order,customer.first_name, customer.email)
    # except:
        # pass
    # if data['mode'] == 'cod':
        # PaymentMedium.objects.create(
            # order = order,
            # payment_mode = 'Cash On Delivery',
        # )

    # return JsonResponse('Payment Complete', safe=False)

def processOrder(request):
    randomid=randrange(1, 10000)
    data = json.loads(request.body)
    items_total = 0
    sessionid=request.session.get('session_id')
    
    if request.user.is_authenticated:
        customer = request.user
        #order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order = Order.objects.get(customer=customer, complete=False)
    else:
        name=data['form']['firstname']
        if User.objects.filter(username=name).exists():
            name+=str(randomid)
        User.objects.create(
        first_name = data['form']['firstname'],
        last_name = data['form']['lastname'],
        email = data['form']['email'],
        is_active=False,
        is_staff=False,
                    #phone_no=data['form']['phone_no']
        username=name,
        password='',
        )
        
        obj=Profile.objects.last()
        obj.refresh_from_db()
        obj=Profile.objects.last()
        obj.phone_no= data['form']['phone_no']
        obj.save()
        
        customer=User.objects.last()
        Order.objects.filter(sessionid=sessionid, complete=False).update(customer=customer)
        order = Order.objects.get(customer=customer, complete=False,sessionid=sessionid)
    
    if OrderStatus.objects.filter(order = order).exists():
        pass
    else:   
        OrderStatus.objects.get_or_create(order = order, order_status = 'Pending',)

    obj = OrderItem.objects.filter(order_id = order.id)    

    special_deals = SpecialDeals.objects.all()
    special_products = []
    for special_deal in special_deals:
        special_products.append(special_deal.product_id)
    for i in obj:
        product_obj = Product.objects.get(id=i.product_id)
        try:
            special_deal_item = SpecialDeals.objects.get(product = i.product_id)
        except:
            pass
        # if i.product_id in special_products:
        #     OrderItem.objects.filter(pk = i.id).update(name = product_obj.product_title, price = special_deal_item.discounted_price)
        # else:
        OrderItem.objects.filter(pk = i.id).update(name = product_obj.product_title)

    #order.complete = True
    order.save()
    if ShippingAddress.objects.filter(order = order).exists():
        ShippingAddress.objects.filter(order = order).update(
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
                phone = data['shipping']['phone'],
        )
    else:
        ShippingAddress.objects.create(
                customer =customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
                phone = data['shipping']['phone'],
        )
    if PaymentMedium.objects.filter(order = order).exists():
        pass
    else:
        if data['mode'] == 'cod':
            PaymentMedium.objects.get_or_create(
                order=order,
            )
        
    context={
        'items':obj,
        'order':order,
    }
    
    return JsonResponse('Order successful proceed for payment', safe=False)

def orderprocessing(request):
    template = "products/final_checkout.html"
    sessionid=request.session.get('session_id')
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get(customer=customer, complete=False)
    else:
        order = Order.objects.get(sessionid=sessionid, complete=False)
    item=OrderItem.objects.filter(order_id=order.id)
    shipping = ShippingCharges.objects.first()
    shipping_charge = shipping.charges
    total = sum([(i.price * i.quantity) for i in item])
    grand_total = total + shipping_charge
    payments=Add_payment_types.objects.all()
    context={
        'items':item,
        'ourorder':order,
        'shipping': shipping_charge,
        'grand_total': grand_total,   
        'payments': payments,
    }
    
    return render(request, "products/final_checkout.html", context)

def orderpayment(request,pk):
    transaction_id = datetime.datetime.now().timestamp()
    paymentmode=request.POST.get('paymenttype')
    #paymode=Add_payment_types.objects.get(id=paymentmode)
    getorder = Order.objects.get(id=pk)

    Order.objects.filter(id=pk).update(complete=True,transaction_id=transaction_id)
    PaymentMedium.objects.filter(order_id=pk).update(payment_mode=paymentmode)
    for o in getorder.orderitem_set.all():
        product = Product.objects.get(id = o.product.id)
        product.items_in_stock = product.items_in_stock - o.quantity
        product.save()
    try:
        logged_in_user=request.user
        confirmationEmail(request, pk,logged_in_user.first_name, logged_in_user.email)
    except:
        pass
    request.session['order_success'] = "Your Order has been placed successfully!!!"
    return redirect('home')
    
def confirmationEmail(request, order, name, mailaddress):
    from django.contrib.sites.shortcuts import get_current_site
    
    current_site = get_current_site(request)
    template = render_to_string('products/confirm_order_email.html', {'name': name, 'pk': order,'current_site':current_site})
    email = EmailMessage(
        'Order Confirmation',
        template,
        settings.EMAIL_HOST_USER,
        [mailaddress],
        #[request.user.email],
    )
    email.fail_silently = False
    email.send()

def search(request):
    template = "products/search_results.html"
    if request.method == "POST":
        search = request.POST['search']
        results = Product.objects.filter(product_title__icontains=search)
     
        context={
            'search': search,
            'results': results,
        }
    else:
        results = Product.objects.all()
        context={
            'results' : results,
        }

    return render(request, template, context)

@allowed_users
def addProduct(request):
    template = "products/add_products.html"
    
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES)
        color = request.POST.get('colorfeature')
        feature = request.POST.get('allfeature')
        feature = json.loads(feature)
        if form.is_valid():
            p = form.save(commit=False)
            if color:
                p.colors=color
            p.save()
            images = request.FILES.getlist("more_images")
            for i in images:
                ProductImage.objects.create(product=p, image=i)
            tot_data = len(feature) / 3
            chunk_final = 3
            chunk_initial = 0
            counter = 1
            while counter <= tot_data:
                aa = feature[chunk_initial:chunk_final]
                memory=aa[0]
                price=Decimal(aa[1])
                retailprice = Decimal(aa[2])
                
                Mobilememory.objects.create(
                product=p,
                description=memory,
                price=price,
                retailprice=retailprice
                )
                counter += 1
                chunk_final += 3
                chunk_initial += 3
            
            messages.success(request, f'Product successfully added.')
            return redirect('all_items')
        else:
            messages.error(request, f'Please fill the required fields.')
    else:
        form = ProductForm()
        color=Colors.objects.all()
    context={
        'form': form,
        'color': color,
        #'sub': sub,
    }
    return render(request, template, context)

@allowed_users
def everyProduct(request):
    template = "products/all_items.html"
    all_items = Product.nosale.all().order_by('-id')
    delorder = Order.objects.filter(complete=0).filter(date_ordered__lte= timezone.now()-datetime.timedelta(days=2))
    if delorder:
        for i in delorder:
            OrderItem.objects.filter(order_id=i.id).delete()
            ShippingAddress.objects.filter(order_id=i.id).delete()
            OrderStatus.objects.filter(order_id=i.id).delete()
            PaymentMedium.objects.filter(order_id=i.id).delete()
            Order.objects.filter(id=i.id).delete()
    
    context={
        'all_items': all_items,
        'check' : 'nosale'
    }

    return render(request, template, context)

@allowed_users
def deleteProduct(request, pk):
    pk=request.POST.get('deleteId')
    try:
        post_to_delete = Product.objects.get(id=pk)
        image_delete = ProductImage.objects.filter(product=post_to_delete.id)
    except Product.DoesNotExist:
        messages.error(request, f'This product does not exist.')
        return redirect('all_items')

    if post_to_delete:
        #post_to_delete.delete()
        if os.path.isfile(post_to_delete.image.path):
            os.remove(post_to_delete.image.path)
        if image_delete:
            for i in image_delete:
                if os.path.isfile(i.image.path):
                    os.remove(i.image.path)
        post_to_delete.delete()
        messages.success(request, f'The product has been deleted.')
        return redirect('all_items')        

    # return render(request, "products/all_products.html")

@allowed_users
def updateProduct(request, pk):
    product_id = pk
    try:
        UpdateFormSet = modelformset_factory(ProductImage, fields=('image',), extra=1)
        img_form = UpdateFormSet(queryset=ProductImage.objects.filter(product_id=pk))
        obj2 = ProductImage.objects.filter(product_id=pk)

        obj = Product.objects.get(id=pk)
        obj_img = obj.image.url

        u_form = ProductUpdateForm(instance = obj)
    except:
        messages.error(request, f'This product does not exist.')
        return redirect('all_items')
    
    if request.method == "POST":
        u_form = ProductUpdateForm(request.POST or None, request.FILES, instance = obj)
        img_form = UpdateFormSet(request.POST or None, request.FILES, queryset=ProductImage.objects.filter(product_id=pk))
        feature = request.POST.get('allfeature')
        feature = json.loads(feature)
        color = request.POST.get('colorfeature')
        #print(color)
        if u_form.is_valid() and img_form.is_valid():
            #print(request.FILES.getlist('image'))
            if request.FILES.getlist('image'):
            # print(os.path.exists(os.path.join(Path(BASE_DIR), Path(obj.image.url[1:]))))
                if os.path.exists(os.path.join(BASE_DIR, Path(obj_img[1:]))):
                    os.remove(os.path.join(BASE_DIR, Path(obj_img[1:])))

            # obj_img.delete()
            p = u_form.save(commit=False)
            #if color:
            p.colors=color
            p.save()
            for x, i in enumerate(obj2):
                more_images = f'form-{x}-image'
                if request.FILES.getlist(more_images):
                    old_image = i.image.url
                # print(old_image)
                # print(os.path.join(Path(BASE_DIR), Path(old_image[1:])))
                # print(os.path.exists(os.path.join(Path(BASE_DIR), Path(old_image[1:]))))
                
                    if os.path.exists(os.path.join(Path(BASE_DIR), Path(old_image[1:]))):
                        os.remove(os.path.join(Path(BASE_DIR), Path(old_image[1:])))
            
            obj2.delete()

            for form in img_form.cleaned_data:
                #print(form)
                if form:
                    image = form['image']
                    photo = ProductImage(product=p, image=image)
                    photo.save()   
            
            tot_data = len(feature) / 4
            chunk_final = 4
            chunk_initial = 0
            counter = 1
            while counter <= tot_data:
                aa = feature[chunk_initial:chunk_final]
                featureid=aa[0]
                memory=aa[1]
                price=Decimal(aa[2])
                retailprice = Decimal(aa[3])
                
                if featureid == '':
                    newupdate=Mobilememory.objects.create(price=price,retailprice=retailprice)
                else:
                    newupdate=Mobilememory.objects.get(id=featureid)
                
                newupdate.product=Product.objects.get(id=obj.id)
                newupdate.description=memory
                newupdate.price=price
                newupdate.retailprice = retailprice
                newupdate.save()
                
                counter += 1
                chunk_final += 4
                chunk_initial += 4
            messages.success(request, f'Product successfully updated.')
            
            return redirect('all_items')
        else:
            messages.error(request, f'Please fill the required fields.') 
    
    features = Mobilememory.objects.filter(product_id=obj.id)
    subcategory = SubCategory.objects.all()
    c=obj.colors
    color=Colors.objects.all()
    product_colors=[]
    if c:
        col = ''.join(str(c).split(','))
        product_colors = Colors.objects.filter(id__in=col)

    context={
        'u_form': u_form,
        'img_form':img_form,
        'product_id':product_id,
        'features':features,
        'sub':subcategory,
        'colors':color,
        'specific_col':product_colors,
    }       

    return render(request, "products/update_product.html", context)

@allowed_users
def orders(request):
    template = "products/orders.html"

    orders = Order.objects.filter(complete=True).order_by('-id')
    status = OrderStatus.objects.all()
    payment_mode = PaymentMedium.objects.all()
   
    context={
        'orders':orders,
        'status': status,
        'payment_mode': payment_mode,
    }

    return render(request, template, context)

@login_required
def orderDetail(request, pk):
    template = "products/order_detail.html"
    
    orders = Order.objects.get(pk=pk)
    if request.user.id == orders.customer_id or request.user.is_superuser:
        address = ShippingAddress.objects.get(order_id=pk)
        order_items = OrderItem.objects.filter(order_id=pk)
        payment_mode = PaymentMedium.objects.get(order_id=pk)
        status = OrderStatus.objects.get(order=pk)
        form = EditOrderForm(instance = status)
        total=0
        price = 0
        grand_total = 0
        shipping = ShippingCharges.objects.first()
        for i in order_items:
            price = i.price * i.quantity
            total = total + price 
        grand_total = total + shipping.charges
            
        context={
            'form': form,
            'orders': orders,
            'order_items':order_items,
            'total': total,
            'address':address,
            'payment_mode': payment_mode,
            'status': status,
            'shipping': shipping,
            'grand_total': grand_total,
        }
    else:
        messages.error(request, f'You are not authorized to view that page.')
        return redirect('home')

    return render(request, template, context)


@allowed_users
def deleteOrder(request, pk):
    
    try:
        delid = request.POST.get('deleteorder')
        order_to_delete = Order.objects.filter(id=delid)
    except Order.DoesNotExist:
        messages.error(request, f'This order does not exist.')
        return redirect('orders')
    
    
    if order_to_delete:
        for i in order_to_delete:
            OrderItem.objects.filter(order_id=i.id).delete()
            ShippingAddress.objects.filter(order_id=i.id).delete()
            OrderStatus.objects.filter(order_id=i.id).delete()
            PaymentMedium.objects.filter(order_id=i.id).delete()
        order_to_delete.delete()
        messages.success(request, f'The order has been deleted.')
        return redirect('orders') 

@allowed_users
def editOrder(request, pk):
    order_id = pk
    template = "products/update_order.html"
    
    try: 
        orders = Order.objects.get(pk=pk)
        address = ShippingAddress.objects.get(order_id=pk)
        order_items = OrderItem.objects.filter(order_id=pk)
        total=0
        price = 0
        grand_total = 0
        ship = 0
        shipping = ShippingCharges.objects.first()
        #paymedium=PaymentMedium.objects.get(order_id=pk)
        for i in order_items:
            price = (i.price * i.quantity)
            total = total + price 
            ship = shipping.charges
            grand_total = total + ship
            
        order_to_edit = OrderStatus.objects.get(order=pk)
        payment_to_edit = PaymentMedium.objects.get(order=pk)

        form = EditOrderForm(instance = order_to_edit)
        pform = EditPaymentMode(instance = payment_to_edit)

    except Order.DoesNotExist:
        messages.error(request, f'This order does not exist.')
        return redirect('orders')

    if request.method == "POST":
        form = EditOrderForm(request.POST, instance = order_to_edit)
        pform = EditPaymentMode(request.POST, instance = payment_to_edit)
        if form.is_valid() and pform.is_valid():
            form.save()
            pform.save()
            messages.success(request, f'Order successfully updated.')
            return redirect('orders')
        else:
            messages.error(request, f'Please do not leave the fields unattended.')
    
    context={
        'form': form,
        'pform': pform,
        'order_id': order_id,
        'orders': orders,
        'order_items':order_items,
        'total': total,
        'address':address,
        'grand_total': grand_total,
        'shipping': shipping,
        'total': total,
    }
    return render(request, template, context)
        
def update_orderstatus(request):
    status = request.GET['status']  
    order_id = request.GET['orderid']
    order_id = int(order_id)
    OrderStatus.objects.filter(order_id=order_id).update(order_status=status)
    
    return JsonResponse('Status successfully updated', safe=False)

@allowed_users
def specaildeal(request):
    template = "products/all_items.html"
    all_items = Product.objects.filter(on_sale = True)
    
    context={
        'all_items': all_items,
        'check' : 'sale'
    }

    return render(request, template, context)
    
@allowed_users
def addspecaildeal(request,id):
    template = 'products/addspecialdeal.html'
    prod = Product.objects.get(id=id)
    prodattr = prod.mobilememory_set.all()
    countattr = prodattr.count()
    productformset = modelformset_factory(Specialdealattr,exclude=("specialdeal",),extra=countattr)
    attr_form = productformset(queryset=Specialdealattr.objects.none())

    if request.method == "POST":
        totalform = request.POST.get(f'form-TOTAL_FORMS')
        totalform = int(totalform)
        specdeal = AddSpecialdeal(request.POST)
        if specdeal.is_valid():            
            deal=specdeal.save()

            arrsize = []
            for i in range(0,totalform):
                size = request.POST.get(f'form-{i}-productsize')
                discprice = request.POST.get(f'form-{i}-discounted_price') or None
                retaildiscprice = request.POST.get(f'form-{i}-retail_discount_price') or None
                if size:
                    if size in arrsize:
                        pass
                    else:
                        Specialdealattr.objects.create(specialdeal=deal,productsize_id= size,discounted_price= discprice,retail_discount_price=retaildiscprice )
                        arrsize.append(size)
            Product.objects.filter(id = prod.id ).update(on_sale=True)
        else:
            messages.error(request, f'This Product is already on deal.')
            return redirect('deal',id=prod.id)

        messages.success(request, f'Added product on Specail Deal Successfully.')
        return redirect('specaildeal')
    else:
        productformset = productformset()

    context = {
        'form': AddSpecialdeal(),
        'attr_form':attr_form,
        'pk': id
    }
    return render(request,template,context)

@allowed_users
def editspecaildeal(request,id):
    template = 'products/editspecialdeal.html'
    prod = Product.objects.get(id=id)
    specialdeal = SpecialDeals.objects.get(product=prod)
    prodattr = prod.mobilememory_set.all()
    countattr = prodattr.count()
    extraform = countattr - specialdeal.specialdealattr_set.count()
    if extraform != 0:
        extraform = 1
    UpdateFormSet = modelformset_factory(Specialdealattr, exclude=('specialdeal',), extra=extraform,can_delete=True)
    attr_form = UpdateFormSet(queryset=Specialdealattr.objects.filter(specialdeal=SpecialDeals.objects.get(product=prod)))

    if request.method == "POST":
        product_form = EditSpecialdeal(request.POST, instance= specialdeal)
        attrformset = UpdateFormSet(request.POST)

        if product_form.is_valid():
            p = product_form.save(commit=False)
            p.product = prod
            p.save()

            if attrformset.is_valid():
                s = attrformset.save(commit=False)
                for s in s:
                    s.specialdeal = specialdeal
                    s.save()
                for object in attrformset.deleted_objects:
                    object.delete()
            else:
                messages.error(request, f'Fields cannot be empty.')
                return redirect('updatedeal',id=prod.id)
        else:
            messages.error(request, f'Something went wrong')
            return redirect('updatedeal',id=prod.id)
        
        return redirect('specaildeal')

    context = {
        'form': EditSpecialdeal(instance=specialdeal),
        'attr_form':attr_form,
        'pk': id
    }
    return render(request,template,context)


@allowed_users
def deletespecaildeal(request,id):
    prod = Product.objects.get(id=id)
    try:
        specialdeal = SpecialDeals.objects.get(product=prod)
        specialdeal.delete()
        prod.on_sale =  False
        prod.save()

        messages.success(request, f'Successfully removed product from sale')
    except:
        messages.error(request, f'Cannot delete this Sale item.')

    return redirect('specaildeal')
