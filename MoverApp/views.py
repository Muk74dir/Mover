from django.shortcuts import render
from django.views.generic import View, CreateView
from constants import API_KEY
import googlemaps
import requests

gmaps = googlemaps.Client(key=API_KEY)

lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
help(gmaps)
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
        direction = gmaps.distance_matrix(origins='Dhaka', destinations='Rajshahi', mode='driving')
        context['direction'] = direction
        context['API_KEY'] = API_KEY 
        return render(request, 'direction.html', context)