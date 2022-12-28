from cgitb import text
from distutils.log import error
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = None
        if "api_key" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                                auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = None
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    # print('json_result from line 31', json_result)    

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
    print(json_result)
    if "reviews" in json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            if not("car_model" in review):
                review["car_make"] = ""
                review["car_model"] = ""
                review["car_year"] = ""
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                   review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                   car_model=review["car_model"],
                                   car_year=review["car_year"], id=review["_id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/29ce2814-a254-48b7-9fec-306f1302b775"
    apiKey = "jnU4RR2ZuQ2WG_X9S4SWeH2BP_9zY2FWs3-I8y-rVrFG"
    json_result = get_request(url, api_key=apiKey, text=dealerreview, version="2022-04-07", features="sentiment", return_analyzed_text=False)
    if "error" in json_result:
        print(json_result)
        return "neutral"
    return json_result["sentiment"]["document"]["label"]



