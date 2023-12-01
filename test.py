from decouple import config
import googlemaps
import requests

API_KEY = config('API_KEY')


gmaps = googlemaps.Client(key=API_KEY)

lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
direction_matrix = gmaps.distance_matrix(origins='Dhaka, Bangladesh', destinations='Rajshahi, Bangladesh', mode='driving')

re = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+API_KEY)

x = {
    'destination_addresses': ['Dhaka, Bangladesh'], 
    'origin_addresses': ['Rajshahi, Bangladesh'], 
    'rows':[
            {'elements': 
                [
                {'distance': 
                    {'text': '278 km', 'value': 277855}, 
                'duration': {'text': '6 hours 31 mins', 'value': 23474}, 
                'status': 'OK'}]}
        ], 
    'status': 'OK'}

print(x['rows'][0]['elements'][0]['distance']['text'])