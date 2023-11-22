from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm
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