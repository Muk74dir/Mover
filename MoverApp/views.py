from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, InfoForm, AddressForm, AddressInfoFormSet
from .models import PersonModel
from django.db import transaction
from .constants import API_KEY
import googlemaps
import requests

# gmaps = googlemaps.Client(key=API_KEY)

# lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
# long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
# direction_matrix = gmaps.distance_matrix(origins='Dhaka', destinations='Chittagong', mode='driving')

# re = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+API_KEY)

class BaseLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = '/login/'


class HomeView(View):
    def get(self, request):
        context = {}
        context['API_KEY'] = API_KEY
        return render(request, 'base.html', context)

class DistanceView(View):
    def get(self, request):
        context = {}
        context['API_KEY'] = API_KEY
        return render(request, 'distance.html', context)
    
    def post(self, request):
        values = request.POST
        print(values)
        destination_address = request.POST.get('destination-address')
        travel_mode = request.POST.get('travel-mode')
        print(destination_address, travel_mode)
        context = {}
        context['API_KEY'] = API_KEY
        return render(request, 'distance.html', context)

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/login/'
    
class AdditionalInfoView(CreateView):
    template_name = 'additional_info.html'
    model = PersonModel
    form_class = InfoForm
    success_url = '/distance/'
    

    def form_valid(self, form):
        user_instance = self.request.user
        
        form.instance.user = user_instance
        form.instance.username = self.request.user.username
        form.instance.first_name = self.request.user.first_name
        form.instance.last_name = self.request.user.last_name
        form.instance.email = self.request.user.email
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
        
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, self.template_name, {'Error': 'Invalid Username or Password'})
        

class LogOutView(BaseLoginRequiredMixin, LogoutView):
    def get(self, request):
        logout(request)
        return redirect('homepage')