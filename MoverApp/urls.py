from django.urls import path
from .views import HomeView, DistanceView, SignUpView, LogInView, LogOutView, AdditionalInfoView


urlpatterns = [
    
    path('', HomeView.as_view(), name='homepage'),
    path('distance/', DistanceView.as_view(), name='distance'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('additional_info/', AdditionalInfoView.as_view(), name='additional_info'),
    
]      
