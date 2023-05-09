from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='name')
    description = models.CharField(null=False,max_length=300,default='description')
    
    def __str__(self):
        return "Name: "+self.name +", Description: "+ self.description




# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    makers = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='name')
    maker_name = models.CharField(null=False, max_length=30, default='maker_name')
    prd_date = models.DateField()
    dealer_id = models.CharField(null=False, max_length=30, default='dealer_id')
    TYPE_SIZES = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "WAGON"),
    ]
    
    types = models.CharField(null=False,choices=TYPE_SIZES)
    
    def get_name(self):
        return self.name
    
    def get_maker_name(self):
        return self.maker_name
    
    def get_prd_date(self):
        return self.prd_date
    
    def __str__(self):
        return "Name: "+self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, 
                dealership, 
                name, 
                purchase, 
                review, 
                car_make, 
                car_model, 
                car_year,
                purchase_date, 
                sentiment='unknown', 

                ):
        # Dealer dealership
        self.dealership = dealership
        # Dealer name
        self.name = name
        # purchase
        self.purchase = purchase
        # Dealer review
        self.review = review
        # Location purchase date
        self.purchase_date = purchase_date
        # car make
        self.car_make = car_make
        # car model
        self.car_model = car_model
        # car_year
        self.car_year = car_year
        # sentiment
        self.sentiment = sentiment
        # review id
        self.id = id

    def __str__(self):
        return "Reviewer name: " + self.name