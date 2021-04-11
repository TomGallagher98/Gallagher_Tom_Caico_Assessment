from Customer import *
from Agent import *
from Claims import *
from Payment import *

class InsuranceCompany:
    def __init__(self, name):
        self.name = name # Name of the Insurance company
        self.customers = [] # list of customers
        self.agents = []  # list of dealers
        self.claims = [] #list of all insurance claims
        self.payment_in = [] #list of all payments made by customers
        self.payment_out = [] #list of all payments made to agents
        

# Customer Codes
    #returns a list of all customers
    def getCustomers (self):
        return list(self.customers)
    #adds a customer to the company databse
    def addCustomer (self, name, address):
        c = Customer (name, address)
        self.customers.append(c)
        return c.ID
    #returns a customer specified by their ID if they exist
    def getCustomerById(self, id_):
        for d in self.customers:
            if(d.ID==id_):
                return d
        return None
    #removes a customer from the system 
    def deleteCustomer (self, customer_id):
        c = self.getCustomerById(customer_id)
        c.agent.customers.remove(c)
        self.customers.remove(c)

#Agent Code
    #returns a list of all agents
    def getAgents(self):
        return list(self.agents)
    #adds an agent to the system
    def addAgent(self, name, address):
        a = Agent (name, address)
        self.agents.append(a)
        return a.ID
    #returns a specific agent by their ID if they exist
    def getAgentbyId(self, id_):
        for i in self.agents:
            if i.ID==id_:
                return i
        return None
    #Appends all of the customers from an old agents customer list  into a new agents customer list
    def moveAgentCustomers(self,old_agent_id,new_agent_id):
        if len(self.getAgentbyId(old_agent).customers) > 0:
            for i in self.getAgentbyId(old_agent_id).customers:
                self.getAgentbyId(new_agent_id).addCustomer(i)
    #First removes the agent from all of their old customers agent list then removes them from the company system        
    def deleteAgent(self, agent_id):
        a = self.getAgentbyId(agent_id)
        for c in a.customers:
            c.agent.remove(c.agent[0])
        self.agents.remove(a)
        
#Claims Code
    #adds a claim into the company system
    def addClaim(self,claim):
        self.claims.append(claim)

    #Returns a list of all claims
    def getClaims(self):
        return list(self.claims)
    #Returns a specific claim
    def getClaimbyID(self, id_):
        for i in self.claims:
            if i.ID == id_:
                return i
        return None

#Payment Code
    #Appends a payment into the customer payments list
    def add_customer_payment(self,payment):
        self.payment_in.append(payment)
    #Adds a payment into a specified agents payment list, also appends the payment to the companies outgoing payment list
    def Pay_Agent(self, payment):    
        for A in self.agents:
            if A.ID == payment.agent:
                A.payment.append(payment)
                self.payment_out.append(payment)
    #Returns a list of all incoming payments from customers
    def get_In_Payments(self):
        return list(self.payment_in)
    #Returns a list of all outgoing payments to agents
    def get_Out_Payments(self):
        return list(self.payment_out)
            
            
            
#Stats Code
    #Ranking system for agents
    #Takes an agents total incoming payments from customers and subtracts the companies payments to the agent
    #Then divides the total by how many payments(months) that the agent has recieved
    #Shows how much the profit agent is generating per month over their entire time at the company
    def Count_Agent_Revenue(self,agent):
        for i in range(0,len(self.agents)):
            if agent == self.agents[i]:
                return (sum(self.agents[i].Customer_Payments)-sum(self.agents[i].payment))/len((self.agents[i].payment))
    
    #Uses the data from the Count_Agent_Revenue function to perform an insertion sort on all of the agents
    #Returns the list of sorted agents with highest Profit in the first (left) index through to lowest in the last (right) index
    def Sort_Agents(self):
        sortedagents = [i for i in self.agents]
        for j in range (0,len(sortedagents)-1):
            store = sortedagents[j+1]
            while j >= 0:
                if self.Count_Agent_Revenue(store) > self.Count_Agent_Revenue(sortedagents[j]):
                    sortedagents[j+1] = sortedagents[j]
                    sortedagents[j] = store
                    
                    j -= 1
                    
                else:
                    break
                
        return(sortedagents)
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            