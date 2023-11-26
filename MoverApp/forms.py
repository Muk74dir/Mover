from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PersonModel, AddressModel, TripModel
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
        label='Username'
    )
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
        label='First Name'
    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
        label='Last Name'
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        label='Email'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label='Password'
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
class InfoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'
    }))
    dob = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2023), 
        attrs={'style': 'width: 33%; display: inline-block;', 'class': 'form-control'}),
        label='Date of Birth',
    )
    class Meta:
        model = PersonModel
        fields = ('image', 'phone', 'dob', 'account_type')


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ('address_line', 'city', 'state', 'zipcode', 'country')

AddressInfoFormSet = forms.inlineformset_factory(PersonModel, AddressModel, form=AddressForm, extra=1, can_delete=False)

class PersonModelForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2023), 
        attrs={'style': 'width: 33%; display: inline-block;', 'class': 'form-control'}),
        label='Date of Birth',
    )
    class Meta:
        model = PersonModel
        fields = ['image', 'first_name', 'last_name', 'email', 'phone', 'dob']
        
class AddressModelForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ['address_line', 'city', 'state', 'zipcode', 'country']
        
        
class DirectionForm(forms.ModelForm):
    origin = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'From',
               'id': 'origin',
               'type': 'text',}),
        label='Origin'
    )
    destination = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'To',
               'id': 'destination',
               'type': 'text',}),
        label='Destination'
    )
    class Meta:
        model = TripModel
        fields = ['origin', 'destination']