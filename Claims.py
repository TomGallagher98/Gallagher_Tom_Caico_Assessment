import uuid
# Represents the customer of the car insurance company
class Claim:
    def __init__(self, C_Date, C_Description, C_Amount):
        self.ID= str(uuid.uuid1())
        self.C_Date = C_Date
        self.description = C_Description
        self.amount = C_Amount
        self.status = "PENDING"
        #Initital status is set to pending

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.ID, 
            'date': self.C_Date, 
            'description': self.description,
            'amount': self.amount,
            'status': self.status
        }
    

    
        