from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm





from .models import Customer,Route


class CreateUserForm(UserCreationForm):
    
    firstname = forms.CharField()
    lastname = forms.CharField()
    phone_number = forms.CharField()
    email_address = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', 'phone_number', 'email_address', 'password1','password2']
        

class CreateRouteForm(ModelForm):
    class Meta:
        model = Route
        fields = ['departure','routFrom','routTo','seatsReserved','price','rout_category','user_id']
        widgets = {'user_id': forms.HiddenInput()}
        
        
        
class FindRouteForm(ModelForm):
    
    class Meta:
        model = Route
        fields = ['routFrom','routTo','rout_category']
        


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
