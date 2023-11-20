from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from .constants import API_KEY
import googlemaps
import requests

gmaps = googlemaps.Client(key=API_KEY)

lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
direction_matrix = gmaps.distance_matrix(origins='Dhaka', destinations='Chittagong', mode='driving')

re = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+API_KEY)


class HomeView(View):
    def get(self, request):
        context = {}
        print(gmaps.geolocate())
        lant = gmaps.geolocate()['location']['lat']
        long = gmaps.geolocate()['location']['lng']
        context['lant'] = lant
        context['long'] = long
        context['API_KEY'] = API_KEY
        return render(request, 'base.html', context)
    
class GeolocationView(View):
    def get(self, request):
        context = {}
        lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
        long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
        context['lant'] = lant
        context['long'] = long
        context['API_KEY'] = API_KEY
        return render(request, 'geolocation.html', context)
    
    def post(self, request):
        pass

class DirectionView(View):
    def get(self, request):
        context = {}  
        context['API_KEY'] = API_KEY 
        return render(request, 'direction.html', context)
    
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
    
class DemoView(View):
    def get(self, request):
        context = {}
        context['API_KEY'] = API_KEY
        return render(request, 'demo.html', context)