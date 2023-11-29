from typing import Any, Dict, Optional
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, InfoForm, AddressInfoFormSet, PersonModelForm, AddressModelForm, DirectionForm
from django.contrib.auth import get_user_model
from .models import PersonModel, AddressModel, TripModel
from django.contrib.auth.models import User
from django.db import transaction
from django.core.files import File
from .constants import API_KEY
import googlemaps
import requests

gmaps = googlemaps.Client(key=API_KEY)

lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
direction_matrix = gmaps.distance_matrix(origins='Dhaka', destinations='Chittagong', mode='driving')

re = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+API_KEY)




class BaseLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = '/login/'


class HomeView(BaseLoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context['API_KEY'] = API_KEY
        return render(request, 'base.html', context)

class DistanceView(BaseLoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context['form'] = DirectionForm()
        context['title'] = 'Set Direction and Vehicle'
        context['button'] = 'Set'
        return render(request, 'distance.html', context)

    def post(self, request):
        pass

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/login/'
    
class AdditionalInfoView(BaseLoginRequiredMixin, CreateView):
    template_name = 'additional_info.html'
    model = PersonModel
    form_class = InfoForm
    success_url = '/home/'
    
    def get(self, request):
        if PersonModel.objects.filter(user=request.user).exists():
            return redirect('homepage')
        else:
            return super().get(request)
    

    def form_valid(self, form):
        user_instance = get_user_model().objects.get(pk=self.request.user.pk)
        
        form.instance.user = user_instance
        form.instance.username = user_instance.username
        form.instance.first_name = user_instance.first_name
        form.instance.last_name = user_instance.last_name
        form.instance.email = user_instance.email
        form.instance.status = 'Available'
        form.instance.rating = None

        with transaction.atomic():
            response = super().form_valid(form)
            
            address_formset = AddressInfoFormSet(self.request.POST, instance=self.object)
            if address_formset.is_valid():
                address_formset.save()

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['address_formset'] = AddressInfoFormSet(self.request.POST, instance=self.object)
        else:
            context['address_formset'] = AddressInfoFormSet(instance=self.object) if self.object else AddressInfoFormSet()
        return context
        
    
    
    
    
class LogInView(LoginView):
    template_name = 'login.html'
    
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        context = {}
        if user:
            login(request, user)
            return redirect('additional_info')
        else:
            context['form'] = self.form_class(self.request.POST)
            context['Error'] = 'Invalid Username or Password'
            return render(request, self.template_name, context)
        

class LogOutView(BaseLoginRequiredMixin, LogoutView):
    def get(self, request):
        logout(request)
        return redirect('homepage')
    

class ProfileView(BaseLoginRequiredMixin, View):
    def get(self, request):
        get_person = PersonModel.objects.get(user=request.user)
        get_person_address = AddressModel.objects.get(person=get_person)
        context = {}
        context['person'] = get_person
        context['address'] = get_person_address
        return render(request, 'profile.html', context)
    
class EditPersonView(BaseLoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = PersonModel
    form_class = PersonModelForm
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(PersonModel, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Edit Profile'
        context['button'] = 'Update'
        context['form'] = self.form_class(instance=self.get_object())
        return context

class EditAddressView(BaseLoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = AddressModel
    form_class = AddressModelForm
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(AddressModel, person__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Edit Address'
        context['button'] = 'Update'
        context['form'] = self.form_class(instance=self.get_object())
        return context
    
 
class ChangePasswordView(BaseLoginRequiredMixin, PasswordChangeView):
    template_name = 'edit_profile.html'
    Model = PersonModel
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(PersonModel, user=self.request.user)
    
    def get_context_data(self, **kwargs: Any) -> Any:
        context = {}
        context['title'] = 'Change Password'
        context['button'] = 'Change'
        context['form'] = self.form_class(self.request.user)
        return context
    
class DeleteProfileView(BaseLoginRequiredMixin, DeleteView):
    template_name = 'edit_profile.html'
    model = PersonModel
    success_url = '/logout/'
    
    def get_object(self, queryset=None):
        return get_object_or_404(PersonModel, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Are you sure you want to delete your profile?'
        context['button'] = 'Delete'
        person = self.get_object()
        PersonModel.objects.get(user=self.request.user).delete()
        User.objects.get(pk=self.request.user.pk).delete()
        return context
        
        
