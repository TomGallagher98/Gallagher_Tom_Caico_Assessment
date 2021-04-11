import uuid
# Represents the insurance agent
class Agent:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.customers = [] #list of agents customers (customer ID)
        self.claims = [] #List of claims made by their customers
        self.payment = [] #List of payments from the company to the agent
        self.Customer_Payments = [] #List of Payments made from the agents customers
    
    #Adds a customer to the customer list, also adds themself to the respective customers agent list
    def addCustomer(self, customer_id): 
        self.customers.append(customer_id)
        customer_id.agents.append(self)

    # convert object to JSON
    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name, 
            'address': self.address,
            'customers': self.customers
        }
    # agent claim management
    #Searches through the claims in their claim list, and returns a claim if the entered ID matches the ID of a claim
    def getClaimbyID(self, id_):
        for i in self.claims:
            if i.ID == id_:
                return i
        return None
    
    # agent statistics
    #Returns a list of all the agents handled claims or revenues for statistics purposes
    def Agent_Claims(self):
        return list(self.claims)
    def Agent_Revenues(self):
        return list(self.Customer_Payments)