import uuid
from Claims import *
from Payment import *
# Represents the customer of the car insurance company
class Customer:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.cars = [] # List of cars
        self.agent = []
        #Claims
        self.claims = []
        #Payouts
        self.payments = []
        
    #Adds a car to the customers car list   
    def addCar (self, car):
        self.cars.append(car)

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'address': self.address,
            'cars': self.cars
        }
    
    #Appends the claim to their claim list and their agents claims list
    def makeClaim(self, claim):
        self.claims.append(claim)
        self.agent[0].claims.append(claim)
    #Returns a claim if the entered ID matches the ID of a claim that they've made
    def getClaimbyID(self, id_):
        for i in self.claims:
            if i.ID == id_:
                return i
        return None
    
    #Uses the payment class to make a payment. Appends to their payment list and their agents customer payments list
    def makePayment(self, payment):
        self.payments.append(payment)
        self.agent[0].c_payments.append(payment)
        
#Represents the car owned by a customer
class Car :
    def __init__(self, model_name, number_plate, motor_power, year):
        self.name = model_name
        self.number_plate = number_plate
        self.motor_power = motor_power
        self.year = year
    
    #converts to JSON
    def serialize(self):
        return {
            'number plate': self.number_plate, 
            'name': self.name, 
            'motor power': self.motor_power,
            'year': self.year
        }