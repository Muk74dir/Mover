from decouple import config
import googlemaps
import requests

API_KEY = config('API_KEY')


gmaps = googlemaps.Client(key=API_KEY)

lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
direction_matrix = gmaps.distance_matrix(origins='Dhaka', destinations='Rajshahi Ruet', mode='driving')

print(direction_matrix)

re = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+API_KEY)
