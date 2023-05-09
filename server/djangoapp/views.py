from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import  CarModel
from .restapis import get_dealers_from_cf,get_dealer_by_id_from_cf,post_request,get_dealers_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request,'djangoapp/user_login.html',context)
    else:
        return render(request,'djangoapp/user_login.html',context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request,'djangoapp/registration.html',context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New User")
        if not user_exist:
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name,
                                            password=password)
            login(request,user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/06486887-3874-4c1e-81b5-519645529326/dealership-package/get-dealership-sequence.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
       
        context["dealership_list"] = dealerships
        # Return a list of dealer short name
        return render(request,'djangoapp/index.html',context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request,dealer_id):
    context = {'dealer_id':dealer_id}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/06486887-3874-4c1e-81b5-519645529326/dealership-package/get-review-sequence.json"
        
        url2 = "https://us-south.functions.appdomain.cloud/api/v1/web/06486887-3874-4c1e-81b5-519645529326/dealership-package/get-dealership-sequence.json"
        # Get reviews from the URL
        dealers = get_dealers_by_id(url2,dealer_id)
        reviews = get_dealer_by_id_from_cf(url,dealer_id)
        context["dealer_id"] = dealer_id
        context["dealers"] = dealers
        context['reviews_list'] = reviews
        # Return a list of review short name
        return render(request,'djangoapp/dealer_details.html',context)
    
    
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/06486887-3874-4c1e-81b5-519645529326/dealership-package/post-review-sequence.json"
    url2 = "https://us-south.functions.appdomain.cloud/api/v1/web/06486887-3874-4c1e-81b5-519645529326/dealership-package/get-dealership-sequence.json"
    context = {}
    review = {}
    json_payload = {}
    
    context['dealer_id'] = dealer_id
    dealer = get_dealers_by_id(url2,dealer_id)[0]
    cars = CarModel.objects.filter(dealer_id=dealer_id)
    
    context["dealer"] = dealer
    context["cars"] = cars

    if request.method == "GET":
        return render(request,'djangoapp/add_review.html',context)
    elif request.method == "POST":
        selected = int(request.POST["car"])
        
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = str(request.POST['fname']) + " " +str(request.POST['lname'])
        review["dealership"] = dealer_id
        review["review"] = request.POST['review']
        review["purchase"] = request.POST['purchase'] =='1' if True else False
        review["purchase_date"] = request.POST["date-own"]
        
        car = cars.filter(id=selected)[0]
    
        review["car_model"] = car.get_name()
        review["car_make"] = car.get_maker_name()
        review["car_year"] = car.get_prd_date()
        json_payload['review'] = review         
        post_request(url, json_payload, dealerId=dealer_id)
        
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    


