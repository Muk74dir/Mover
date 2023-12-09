from typing import Any, Dict, Optional
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, InfoForm, AddressInfoFormSet, PersonModelForm, AddressModelForm, DirectionForm
from .forms import VehicleRegistrationForm, VehicleSearchFrom
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import PersonModel, AddressModel, VehicleModel, TripModel
from django.contrib.auth.models import User
import googlemaps, stripe, requests
from django.db import transaction
from .constants import API_KEY, STRIPE_API_KEY
import datetime as dt
from .ssl import sslcommerz_payment_gateway

gmaps = googlemaps.Client(key=API_KEY)

lant = gmaps.geolocate(home_mobile_country_code=+880)['location']['lat']
long = gmaps.geolocate(home_mobile_country_code=+880)['location']['lng']
direction_matrix = gmaps.distance_matrix(origins='Dhaka', destinations='Chittagong', mode='driving')

re = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+API_KEY)




class BaseLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = '/login/'


class HomeView(BaseLoginRequiredMixin, View):
    def get(self, request):
        if AddressModel.objects.filter(person__user=request.user).exists() == False:
            return redirect('additional_info')
        context = {}
        context['API_KEY'] = API_KEY
        person = PersonModel.objects.get(user=request.user)
        context['person'] = person
        context['type'] = person.account_type
        return render(request, 'base.html', context)

class DistanceView(BaseLoginRequiredMixin, View):
    context = {}
    def get(self, request):
        if AddressModel.objects.filter(person__user=request.user).exists() == False:
            return redirect('additional_info')
        self.context = {}
        self.context['form'] = DirectionForm()
        self.context['search_form'] = VehicleSearchFrom()
        self.context['title'] = 'Set Direction'
        self.context['button'] = 'Set'
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        return render(request, 'distance.html', self.context)

    def post(self, request):
        form = DirectionForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            mode = form.cleaned_data['travel_mode']
            if mode == 'CAR':
                direction_matrix = gmaps.distance_matrix(origins=origin, destinations=destination, mode='transit')
            else:
                direction_matrix = gmaps.distance_matrix(origins=origin, destinations=destination, mode='driving')
            
            distance = direction_matrix['rows'][0]['elements'][0]['distance']['text']
            duration = direction_matrix['rows'][0]['elements'][0]['duration']['text']
            
            request.session['redirected_from_direction'] = True
            request.session['distance'] = distance
            request.session['duration'] = duration
            request.session['origin'] = origin
            request.session['destination'] = destination
            request.session.save()
            
            return redirect('driver_list')
        

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/login/'
    
class AdditionalInfoView(BaseLoginRequiredMixin, CreateView):
    template_name = 'additional_info.html'
    model = PersonModel
    form_class = InfoForm
    success_url = '/home/'
    
    def get(self, request):
        if PersonModel.objects.filter(user=request.user).exists():
            return redirect('homepage')
        else:
            return super().get(request)
    

    def form_valid(self, form):
        user_instance = get_user_model().objects.get(pk=self.request.user.pk)
        
        form.instance.user = user_instance
        form.instance.username = user_instance.username
        form.instance.first_name = user_instance.first_name
        form.instance.last_name = user_instance.last_name
        form.instance.email = user_instance.email
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
        context = {}
        if user:
            login(request, user)
            return redirect('additional_info')
        else:
            context['form'] = self.form_class(self.request.POST)
            context['Error'] = 'Invalid Username or Password'
            return render(request, self.template_name, context)
        

class LogOutView(BaseLoginRequiredMixin, LogoutView):
    def get(self, request):
        logout(request)
        return redirect('homepage')
    

class ProfileView(BaseLoginRequiredMixin, View):
    def get(self, request):
        if AddressModel.objects.filter(person__user=request.user).exists() == False:
            return redirect('additional_info')
        get_person = PersonModel.objects.get(user=request.user)
        get_person_address = AddressModel.objects.get(person=get_person)
        context = {}
        context['person'] = get_person
        context['address'] = get_person_address
        context['type'] = get_person.account_type
        context['vehicles'] = VehicleModel.objects.filter(driver=get_person)
        return render(request, 'profile.html', context)
    
class EditPersonView(BaseLoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = PersonModel
    form_class = PersonModelForm
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(PersonModel, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Edit Profile'
        context['button'] = 'Update'
        context['form'] = self.form_class(instance=self.get_object())
        return context

class EditAddressView(BaseLoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = AddressModel
    form_class = AddressModelForm
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(AddressModel, person__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Edit Address'
        context['button'] = 'Update'
        context['form'] = self.form_class(instance=self.get_object())
        return context
    
 
class ChangePasswordView(BaseLoginRequiredMixin, PasswordChangeView):
    template_name = 'edit_profile.html'
    Model = PersonModel
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(PersonModel, user=self.request.user)
    
    def get_context_data(self, **kwargs: Any) -> Any:
        context = {}
        context['title'] = 'Change Password'
        context['button'] = 'Change'
        context['form'] = self.form_class(self.request.user)
        return context
    
class DeleteProfileView(BaseLoginRequiredMixin, DeleteView):
    template_name = 'edit_profile.html'
    model = PersonModel
    success_url = '/logout/'
    
    def get_object(self, queryset=None):
        return get_object_or_404(PersonModel, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Are you sure you want to delete your Account?'
        context['button'] = 'Delete'
        return context
    
    def post(self, request):
        PersonModel.objects.get(user=self.request.user).delete()
        User.objects.get(pk=self.request.user.pk).delete()
        return redirect('logout')
        
        
class RegisterVehicle(BaseLoginRequiredMixin, CreateView):
    context={}
    def get(self, request):
        self.context['form'] = VehicleRegistrationForm()
        self.context['title'] = 'Register Vehicle'
        self.context['button'] = 'Register'
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        return render(request, 'edit_profile.html', self.context)
    
    def post(self, request):
        form = VehicleRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.driver = PersonModel.objects.get(user=request.user)
            vehicle.save()
            return redirect('profile')
        else:
            self.get(request)
            return render(request, 'edit_profile.html', self.context)

class AnotherProfileView(BaseLoginRequiredMixin, View):
    context={}
    def get(self, request, pk):
        vehicle = VehicleModel.objects.get(pk=pk)
        self.context['person'] = PersonModel.objects.get(pk=vehicle.driver.pk)
        self.context['vehicles'] = VehicleModel.objects.filter(driver=self.context['person'])
        self.context['address'] = AddressModel.objects.get(person=self.context['person'])
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        return render(request, 'another_profile.html', self.context)


class RequestsView(BaseLoginRequiredMixin, View):
    context={}
    def get(self, request):
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        return render(request, 'requests.html', self.context)
    
    
class DriverListView(BaseLoginRequiredMixin, View):
    context={}
    def get(self, request):
        if AddressModel.objects.filter(person__user=request.user).exists() == False:
            return redirect('additional_info')
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        self.context['vehicles'] = VehicleModel.objects.all()
        self.context['distance'] = None
        self.context['duration'] = None
        self.context['origin'] = None
        self.context['destination'] = None
        
        redirected = request.session.get('redirected_from_direction')
        if redirected==True:
            self.context['distance'] = request.session.get('distance')
            self.context['duration'] = request.session.get('duration')
            self.context['origin'] = request.session.get('origin')
            self.context['destination'] = request.session.get('destination')
            request.session['redirected_from_direction'] = False
            request.session.save()
        
        return render(request, 'driver_list.html', self.context)
    
    def post(self, request):
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        self.context['vehicles'] = VehicleModel.objects.all()
        form = VehicleSearchFrom(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            self.context['vehicles'] = VehicleModel.objects.filter(model__icontains=search)
        return render(request, 'driver_list.html', self.context)
    

class VehicleDetailsView(BaseLoginRequiredMixin, View):
    context={}
    def get(self, request, pk):
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        vehicle = VehicleModel.objects.get(pk=pk)
        self.context['vehicle'] = vehicle
        self.context['owner'] = PersonModel.objects.get(pk=vehicle.driver.pk)
        return render(request, 'vehicle_details.html', self.context)
        

class TripDetailsView(BaseLoginRequiredMixin, View):
    context={}
    
    def get(self, request, pk):
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        self.context['vehicle'] = VehicleModel.objects.get(pk=pk)
        self.context['owner'] = PersonModel.objects.get(pk=self.context['vehicle'].driver.pk)
        self.context['passenger'] = PersonModel.objects.get(user=request.user)
        
        self.context['distance'] = request.session.get('distance')
        self.context['duration'] = request.session.get('duration')
        self.context['origin'] = request.session.get('origin')
        self.context['destination'] = request.session.get('destination')
        
        self.context['start_time'] = dt.datetime.now()
        
        if self.context['duration'].split()[1] == 'mins':
            self.context['end_time'] = self.context['start_time'] + dt.timedelta(
                minutes=int(self.context['duration'].split()[0])
            )
        else:
            self.context['end_time'] = dt.datetime.now() + dt.timedelta(
                hours=int(self.context['duration'].split()[0]),
                minutes=int(self.context['duration'].split()[2])
            )
        
        remaining_time = self.context['end_time'] - self.context['start_time']
        remaining_distance = self.context['distance'].split()[0]
        
        self.context['remaining_time'] = remaining_time
        self.context['remaining_distance'] = remaining_distance
        
        TripModel.objects.create(
            pk=pk,
            passenger=self.context['passenger'],
            driver=self.context['owner'],
            vehicle=self.context['vehicle'],
            start_from=self.context['origin'],
            end_to=self.context['destination'],
            distance=self.context['distance'],
            duration=self.context['duration'],
            fare=(int(self.context['distance'].split()[0]) * 5 ) + 110,
            status=True,
            rating=None,
        )
        return render(request, 'trip_details.html', self.context)
    
    
class BillingView(BaseLoginRequiredMixin, View):
    context={}
    def get(self, request, pk):
        self.context['type'] = PersonModel.objects.get(user=request.user).account_type
        self.context['person'] = PersonModel.objects.get(user=request.user)
        self.context['invoice_no'] = f"000{pk}"
        self.context['date'] = dt.datetime.today().strftime('%B %d, %Y')
        user = PersonModel.objects.get(user=request.user)
        vehicle = VehicleModel.objects.get(pk=pk)
        driver = PersonModel.objects.get(pk=vehicle.driver.pk)
        self.context['fare'] = TripModel.objects.get(pk=pk).fare
        self.context['vehicle'] = vehicle
        return render(request, 'billing.html', self.context)
    
    def post(self, request, pk):
        trip_instance = TripModel.objects.get(pk=pk)
        grand_total = trip_instance.fare
        user = PersonModel.objects.get(user=request.user)
        
        return redirect(sslcommerz_payment_gateway(request, pk, user.pk, grand_total))

@csrf_exempt
def success(request):
    context = {}
    context['type'] = 'passenger'
    return render(request, 'success.html', context)

@csrf_exempt
def faild(request):
    context = {}
    context['type'] = 'passenger'
    return render(request, 'failed.html', context)

@csrf_exempt
def cancelled(request):
    context = {}
    context['type'] = 'passenger'
    return render(request, 'cancelled.html', context)