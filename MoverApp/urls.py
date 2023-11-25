from django.urls import path
from .views import HomeView, DistanceView, SignUpView, LogInView, LogOutView, AdditionalInfoView, ProfileView
from .views import ChangePasswordView, EditPersonView, EditAddressView


urlpatterns = [
    
    path('home/', HomeView.as_view(), name='homepage'),
    path('distance/', DistanceView.as_view(), name='distance'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('additional_info/', AdditionalInfoView.as_view(), name='additional_info'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('edit_profile/', EditPersonView.as_view(), name='edit_profile'),
    path('edit_address/', EditAddressView.as_view(), name='edit_address'),
]      
