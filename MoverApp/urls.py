from django.urls import path
from .views import HomeView, GeolocationView, DirectionView


urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('geolocation/', GeolocationView.as_view(), name='geolocation'),
    path('direction/', DirectionView.as_view(), name='direction'),
]   
