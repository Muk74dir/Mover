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
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2023)))
    class Meta:
        model = PersonModel
        fields = ('image', 'phone', 'dob', 'account_type')

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ('address_line', 'city', 'state', 'zipcode', 'country')

AddressInfoFormSet = forms.inlineformset_factory(PersonModel, AddressModel, form=AddressForm, extra=1)


