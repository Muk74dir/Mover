from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PersonModel, AddressModel
from django import forms

class SignUpForm(UserCreationForm):
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


