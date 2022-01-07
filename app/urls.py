from django.urls import path, include
from app.views import *

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),


    # signup & signin views
    path('signIn/', signInView, name='signIn'),
    path('signUpCustomer/', signUpCustomer, name='signUpCustomer'),
    path('signUpDriver/', signUpDriver, name='signUpDriver'),
    path('signUpAdmin/', signUpAdmin, name='signUpAdmin'),
    path('logout/', logoutView, name='logout'),

    path('customerList/', customerList, name='customerList'),
    path('driverList/', driverList, name='driverList'),
    path('adminList/', adminList, name='adminList'),

    path('allMyTrips/', allMyTrips, name='allMyTrips'),
    path('cancleTrip/<int:trip_id>', cancleTrip, name='cancleTrip'),

    path('allOrderedTrips/', allOrderedTrips, name='allOrderedTrips'),
    path('tripPickedUp/<int:trip_id>', tripPickedUp, name='tripPickedUp'),
    path('tripCompleted/<int:trip_id>', tripCompleted, name='tripCompleted'),

    path('adminPannel/', adminPannel, name='adminPannel'),

]



