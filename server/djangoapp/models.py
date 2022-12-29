from unicodedata import name
from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
            return f'CarMake: {self.name}'


class CarModel(models.Model):
    Sedan = "Sedan"
    SUV = "SUV"
    WAGON = "WAGON"
    MPV = "MPV"
    PICKUP = "Pick-Up"
    CONVERTIBLE = "convertible"

    TYPE_CHOICES = (
        (Sedan, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "WAGON"),
        (MPV ,"MPV"),
        (PICKUP , "Pick-Up"),
        (CONVERTIBLE , "convertible")
    )
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    dealer_id = models.IntegerField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    year = models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
            return f'CarModel name : {self.name}, {str(self.car_make)}, dealer_id: {self.dealer_id}, type: {self.type}, year: {str(self.year)}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = None
        self.id = id
    
    #
    @property            # first decorate the getter method
    def sentiment(self): # This getter method name is *the* name
        return self._sentiment
    #
    @sentiment.setter    # the property decorates with `.setter` now
    def sentiment(self, value):   # name, e.g. "attribute", is the same
        self._sentiment = value   # the "value" name isn't special
    #
    @sentiment.deleter     # decorate with `.deleter`
    def sentiment(self):   # again, the method name is the same
        del self._sentiment