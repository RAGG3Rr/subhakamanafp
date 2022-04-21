from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.validators import MaxValueValidator

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    # contact_number = forms.IntegerField(validators=[MaxValueValidator(9999999999)])
    class Meta:
        model = Profile
        fields = ['image','phone_no','address','city','zipcode']

class CompanyProfileForm(forms.ModelForm):
    phone_no = forms.CharField(required=True)
    city = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ['phone_no','address','city','zipcode','company_name','company_website','purpose']


