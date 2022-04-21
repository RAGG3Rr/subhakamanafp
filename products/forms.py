from django import forms
from django.forms import ModelForm
from .models import Product, ProductImage, OrderStatus, PaymentMedium, SpecialDeals

class ReviewForm(forms.Form):
    comment = forms.CharField(max_length=100)
    rate = forms.IntegerField()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password =  forms.CharField(max_length=32, widget=forms.PasswordInput)

class ProductForm(ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "multiple":True
    }))
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('slug','colors','on_sale') 
        labels = {
            'image':'Thumbnail Image',
        }

class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('slug','colors','on_sale') 
        labels = {
            'image':'Thumbnail Image',
        }

class EditOrderForm(ModelForm):
    class Meta:
        model = OrderStatus
        fields = ['order_status']

class EditPaymentMode(ModelForm):
    class Meta:
        model = PaymentMedium
        fields = ['payment_mode']
    def __init__(self, *args, **kwargs):
        super(EditPaymentMode, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['payment_mode'].widget.attrs['readonly'] = True

class AddSpecialdeal(ModelForm):
    class Meta:
        model = SpecialDeals
        fields = ('product',)

class EditSpecialdeal(ModelForm):
    class Meta:
        model = SpecialDeals
        fields = ('product',)
