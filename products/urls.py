from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('popup/', views.loginuser, name='loginpopup'),
    path('stock/<int:id>/', views.checkStock, name='check_stock'),
    path('subcategories/', views.getSubcategories, name='get_subcategories'),
    path('getspecialdeals/',views.getspecialdeals,name="getspecialdeals"),
    path('specificcategories/', views.getSpecificcategories, name='get_specificcategories'),
    
    path('detail/<slug:slug>/', views.productDetail, name='product-detail'),
    path('all_products/', views.allProducts, name='all'),
    path('specific_categories/<slug:mainslug>/<slug:subslug>/<slug:slug>/', views.specificCategoryDetail, name='specific_category_detail'),
    path('sub_categories/<slug:mainslug>/<slug:slug>/', views.subCategoryDetail, name='sub_category_detail'),
    
    path('categories/<slug:slug>/', views.categoryDetail, name='category_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('orderprocessing/', views.orderprocessing, name='orderprocessing'),
    path('orderpayment/<int:pk>/', views.orderpayment, name='orderpayment'),
	
    path('search/', views.search, name='search'),
    path('special_deals/', views.specialDeal, name='special'),
    path('trending/', views.trendingItems, name='trending'),
    path('custom/', views.customItems, name='custom'),
    path('new-arrivals/', views.newItems, name='new'),

    path('add_products/', views.addProduct, name='add_product'),
    path('all_items/', views.everyProduct, name='all_items'),
    path('delete_item/<int:pk>/', views.deleteProduct, name='delete_product'),
    path('update_item/<int:pk>/', views.updateProduct, name='update_product'),
    path('specialdeal/',views.specaildeal,name="specaildeal"),
    path('addspecialdeal/<int:id>/',views.addspecaildeal,name='deal'),
    path('updatespecialdeal/<int:id>/',views.editspecaildeal,name='updatedeal'),
    path('deletespecaildeal/<int:id>/',views.deletespecaildeal, name="deletedeal"),

    path('orders/', views.orders, name='orders'),
    path('order_detail/<int:pk>/', views.orderDetail, name='order-detail'),
    path('delete_order/<int:pk>/', views.deleteOrder, name='delete_order'),
    path('update_order/<int:pk>/', views.editOrder, name='update_order'),
    path('update_orderstatus/', views.update_orderstatus, name='update_orderstatus'),

    path('high/', views.highToLow, name='high'),
    path('itemdelete/', views.itemdelete, name='itemdelete'),
    path('pricerange/', views.pricerange, name='pricerange'),
    path('onsalefilter/', views.onsalefilter,name="onsalefilter")
    
]