from itertools import product
from django.contrib import admin
from .models import *

# Register your models here. 
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
    # list_display = ['product_title', 'price']
    # list_editable = ['price']
    # search_fields = ['product_title']
    # exclude = ('slug',)
    # class Media:
        # js = ("js/admin.js",)

@admin.register(SpecificCategory)
class SpecificCategory(admin.ModelAdmin):
    exclude = ('slug',)
    class Media:
        js = ("js/admin.js",)

		
# @admin.register(SpecialDeals)		
# class SpecialDeals(admin.ModelAdmin):
#     exclude = ('',)
#     class Media:
#         js = ("js/special_deal.js",)


@admin.register(Category)
class Category(admin.ModelAdmin):
    exclude = ('slug',)
    class Media:
        js = ("js/admin.js",)

@admin.register(SubCategory)
class SubCategory(admin.ModelAdmin):
    exclude = ('slug',)
    class Media:
        js = ("js/admin.js",)
		
admin.site.register(Order)
admin.site.register(Colors)
# admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
# admin.site.register(OrderStatus)

# admin.site.register(ProductImage)

@admin.register(Trending)
class TrendingAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # request.resolver_match.kwargs['object_id']
        kwargs['queryset'] = Product.objects.filter(on_sale= False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# admin.site.register(Size)

# admin.site.register(Mobilememory)
# admin.site.register(Specialdealattr)

admin.site.register(Slideshow)
admin.site.register(Poster)

@admin.register(CustomTable)
class CustomTableAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # request.resolver_match.kwargs['object_id']
        kwargs['queryset'] = Product.objects.filter(on_sale= False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(CustomTableName)

admin.site.register(PaymentMedium)
admin.site.register(Add_payment_types)
admin.site.register(ShippingCharges)