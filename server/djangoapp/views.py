from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
#from .models import related models
from .models import CarMake, CarModel
from .restapis import get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, get_dealers_from_cf
#from .restapis import related methods
from .restapis import get_request, get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        password = request.POST["psw"]
        user = User.objects.create_user(username=username,password=password)
        user.firstname=firstname
        user.lastname=lastname
        user.save()
        auth = authenticate(username=username, password=password)
        login(request, auth)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f446558e-994f-4be2-829f-08ca67ac4254/dealership/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {"reviews_list":[]}
        baseUrl = "https://us-south.functions.appdomain.cloud/api/v1/web/f446558e-994f-4be2-829f-08ca67ac4254/dealership/get-dealership"
        url = f'{baseUrl}/review'
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        if len(reviews)>0:
            i=0
            for review in reviews:
                purchase_year = datetime.strptime(review.purchase_date, "%m/%d/%Y").date()
                review.purchase_year = purchase_year
                reviews[i] = review
                i+=1
            context["reviews_list"] = reviews
        context["dealer_name"] = get_dealer_by_id_from_cf(f'{baseUrl}/dealership',dealer_id)
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/f446558e-994f-4be2-829f-08ca67ac4254/actions/dealership/post-review"
            car_model = CarModel.objects.get(id=request.POST["car"])
            car_make = car_model.car_make
            review = {"name":request.user.get_full_name(),
                      "dealership":dealer_id,
                      "review":request.POST["content"],
                      "purchase":request.POST["purchasecheck"]=='on',
                      "purchase_date":request.POST["purchasedate"],
                      "car_make":car_make.name,
                      "car_model":car_model.name,
                      "car_year": car_model.year.strftime("%Y")
                      }
            print(review)
            json_payload = {}
            json_payload["review"] = review
            response = post_request(url,json_payload)
            print(response)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            # return HttpResponse(str(response))
        return HttpResponse("not authenticated")

    if request.method == "GET":
        print(request)
        baseUrl = "https://us-south.functions.appdomain.cloud/api/v1/web/f446558e-994f-4be2-829f-08ca67ac4254/dealership/get-dealership"
        context = {}
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars
        context["dealer_id"] = dealer_id
        context["dealer_name"] = get_dealer_by_id_from_cf(f'{baseUrl}/dealership',dealer_id)
        return render(request, 'djangoapp/add_review.html', context)

