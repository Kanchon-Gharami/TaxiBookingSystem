from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.db import IntegrityError, transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

import datetime

from app.models import *
# Create your views here.

#index view
def index(request):
    return render(request, 'index.html')


#logout view
def logoutView(request):
    logout(request)
    return redirect('app:index')


# login, Logout, Register & Profile Redirect Views
def signInView(request):
    if request.method == "POST":
        this_username = request.POST['username']
        plain_password = request.POST['password']
        user = authenticate(username=this_username, password=plain_password)
        if user is not None:
            login(request, user)
            '''if user.isStudent == True:
                return redirect('app:examevent')
            elif user.isQuestionSetter == True:
                return redirect('app:questionSetterProfile')
            elif user.isAdmin == True:
                return redirect('app:adminProfile')'''
    return redirect('app:index')


#signup customer view
def signUpCustomer(request):
    if request.method == "POST":
        this_username = request.POST['username']
        plain_password = request.POST['password']
        password2 = request.POST['password2']
        this_name = request.POST['name']
        this_email = request.POST['email']
        this_phone = request.POST['phone']
        this_address = request.POST['address']
        this_paymentMethod = request.POST['paymentMethod']

        try:
            with transaction.atomic():
                if this_username != '' and plain_password != '' and this_name != '' and this_email != '' and this_phone != '' and this_address != '' and this_paymentMethod != '':
                    if myCustomeUser.objects.filter(username=this_username).exists():
                        return render(request, 'signUpCustomer.html', {'error': 'Username already exists'})
                    elif plain_password != password2:
                        return render(request, 'signUpCustomer.html', {'error': 'Passwords do not match'})
                    else:
                        new_user = myCustomeUser(username=this_username, password=make_password(plain_password), name=this_name, email=this_email, phone=this_phone, isCustomer=True, isDriver=False, isAdmin=False)
                        new_user.save()
                        new_customer = Customer(user=new_user, paymentMethod=this_paymentMethod, address=this_address)
                        new_customer.save()
                        login(request, new_user)
                        return redirect('app:signIn')
                else:
                    return render(request, 'signUpCustomer.html', {'error': 'All fields are required'})
        except Exception as e:
            return render(request, 'signUpCustomer.html', {'error': e})
    return render(request, 'signUpCustomer.html')



#signup driver view
def signUpDriver(request):
    if request.method == "POST":
        this_username = request.POST['username']
        plain_password = request.POST['password']
        password2 = request.POST['password2']
        this_name = request.POST['name']
        this_email = request.POST['email']
        this_phone = request.POST['phone']
        this_licenseNo = request.POST['licenseNo']
        try:
            with transaction.atomic():
                if this_username != '' and plain_password != '' and this_name != '' and this_email != '' and this_phone != '' and this_licenseNo != '':
                    if myCustomeUser.objects.filter(username=this_username).exists():
                        return render(request, 'signUpDriver.html', {'error': 'Username already exists'})
                    elif plain_password != password2:
                        return render(request, 'signUpDriver.html', {'error': 'Passwords do not match'})
                    else:
                        new_user = myCustomeUser(username=this_username, password=make_password(plain_password), name=this_name, email=this_email, phone=this_phone, isCustomer=False, isDriver=True, isAdmin=False)
                        new_user.save()
                        new_driver = Driver(user=new_user, licenseNo=this_licenseNo)
                        new_driver.save()
                        login(request, new_user)
                        return redirect('app:index')
                else:
                    return render(request, 'signUpDriver.html', {'error': 'All fields are required'})
        except Exception as e:
            return render(request, 'signUpDriver.html', {'error': e})
    return render(request, 'signUpDriver.html')


#signup admin view
def signUpAdmin(request):
    if request.method == "POST":
        this_username = request.POST['username']
        plain_password = request.POST['password']
        password2 = request.POST['password2']
        this_name = request.POST['name']
        this_email = request.POST['email']
        this_phone = request.POST['phone']
        try:
            with transaction.atomic():
                if this_username != '' and plain_password != '' and this_name != '' and this_email != '' and this_phone != '':
                    if myCustomeUser.objects.filter(username=this_username).exists():
                        return render(request, 'signUpAdmin.html', {'error': 'Username already exists'})
                    elif plain_password != password2:
                        return render(request, 'signUpAdmin.html', {'error': 'Passwords do not match'})
                    else:
                        new_user = myCustomeUser(username=this_username, password=make_password(plain_password), name=this_name, email=this_email, phone=this_phone, isCustomer=False, isDriver=False, isAdmin=False)
                        new_user.save()
                        login(request, new_user)
                        return redirect('app:index')
                else:
                    return render(request, 'signUpAdmin.html', {'error': 'All fields are required'})
        except Exception as e:
            return render(request, 'signUpAdmin.html', {'error': e})
    return render(request, 'signUpAdmin.html')


#Customer list view
def customerList(request):
    return render(request, 'customerList.html', {'customerList': Customer.objects.all()})


#Driver list view
def driverList(request):
    return render(request, 'driverList.html', {'driverList': Driver.objects.all()})


#admin list view
def adminList(request):
    return render(request, 'adminList.html', {'adminList': myCustomeUser.objects.filter(isAdmin=True)})



#all My trips
def allMyTrips(request):
    customerObj = Customer.objects.get(user=request.user)
    try:
        if request.method == "POST":
            tripObj = Trip(
                customer=Customer.objects.get(user=request.user), 
                pickup=request.POST['pickup'], 
                pickupDate=request.POST['pickupDate'], 
                drop=request.POST['drop']
            )
            tripObj.save()
            return redirect('app:allMyTrips')
    except Exception as e:
        return render(request, 'allMyTrips.html', {'error': e})
    return render(request, 'allMyTrips.html', {'allMyTrips': Trip.objects.filter(customer=customerObj)})


#cancle trip
def cancleTrip(request, trip_id):
    try:
        Trip.objects.get(id=trip_id).delete()
        return redirect('app:allMyTrips')
    except Exception as e:
        return render(request, 'allMyTrips.html', {'error': e})


#all orderd trips
def allOrderedTrips(request):
    driverObj = Driver.objects.get(user=request.user)
    return render(request, 'allOrderedTrips.html', {'allOrderedTrips': Trip.objects.filter(driver=driverObj)})


#Trip Completed
def tripCompleted(request, trip_id):
    try:
        tripObj = Trip.objects.get(id=trip_id)
        tripObj.status = "Completed"
        tripObj.dropDate = datetime.now()
        tripObj.save()
        return redirect('app:allOrderedTrips')
    except Exception as e:
        return render(request, 'allOrderedTrips.html', {'error': e})

#Trip Picked Up
def tripPickedUp(request, trip_id):
    try:
        tripObj = Trip.objects.get(id=trip_id)
        tripObj.status = "PickedUp"
        tripObj.save()
        return redirect('app:allOrderedTrips')
    except Exception as e:
        return render(request, 'allOrderedTrips.html', {'error': e})



#adminPannel view
def adminPannel(request):
    try:
        if request.method == "POST":
            driverpk = request.POST['driver']
            tripObj = Trip.objects.get(id=request.POST['tripId'])
            tripObj.driver=Driver.objects.get(pk=driverpk)
            tripObj.fare=request.POST['fare']
            tripObj.status = "Confirmed Booking"
            tripObj.save()
            return redirect('app:adminPannel')
    except Exception as e:
        return render(request, 'adminPannel.html', {'error': e, 'Trip': Trip.objects.all(), 'driver': Driver.objects.all()})
    return render(request, 'adminPannel.html', {'Trip': Trip.objects.all(), 'driver': Driver.objects.all()})


