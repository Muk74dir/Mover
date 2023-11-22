from django.urls import path
from .views import HomeView, GeolocationView, DirectionView, DistanceView, DemoView, SignUpView, LogInView, LogOutView


urlpatterns = [
    
    path('', HomeView.as_view(), name='homepage'),
    path('geolocation/', GeolocationView.as_view(), name='geolocation'),
    path('direction/', DirectionView.as_view(), name='direction'),
    path('distance/', DistanceView.as_view(), name='distance'),
    path('demo/', DemoView.as_view(), name='demo'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    
]      
