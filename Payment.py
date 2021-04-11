import uuid

#Represents the overall basic payment system
class Payment:
    def __init__(self,P_date,P_amount):
        self.ID= str(uuid.uuid1())
        self.P_date = P_date
        self.P_amount = P_amount

#Represents the incoming payments, includes the ID of the paying customer
class Payment_In(Payment):
    def __init__ (self,P_date,P_amount,C_Id):
        Payment.__init__(self, P_date, P_amount)
        self.customer = str(C_Id)

    def serialize(self):
        return {
            'id': self.ID, 
            'date': self.P_Date, 
            'amount': self.P_amount,
            'agent': self.customer
        }

#Represents outgoing payments, includes the ID of the agent being paid    
class Payment_Out(Payment):
    def __init__(self, P_date, P_amount, A_Id):
        Payment.__init__(self,P_date,P_amount)
        self.agent = str(A_Id)
    
    def serialize(self):
        return {
            'id': self.ID, 
            'date': self.P_Date, 
            'amount': self.P_amount,
            'agent': self.agent
        }
        