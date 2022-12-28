from unicodedata import name
from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
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


# <HINT> Create a plain Python class `DealerReview` to hold review data
