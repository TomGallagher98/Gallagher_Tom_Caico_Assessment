  
from flask import Flask, request, jsonify
from InsuranceCompany import *
from Customer import *
from Agent import *
from Payment import *
from Claims import *

app = Flask(__name__)

# Root object for the insurance company
company = InsuranceCompany ("Be-Safe Insurance Company")

#Add a new customer (parameters: name, address).
@app.route("/customer", methods=["POST"])
def addCustomer():
    # parameters are passed in the body of the request
    cid = company.addCustomer(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new customer with ID {cid}")

#Return the details of a customer of the given customer_id.
@app.route("/customer/<customer_id>", methods=["GET"])
def customerInfo(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        return jsonify(c.serialize())
    return jsonify(
            success = False, 
            message = "Customer not found")

#Add a new car (parameters: model, numberplate).
@app.route("/customer/<customer_id>/car", methods=["POST"])
def addCar(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        car = Car(request.args.get(',model'), request.args.get('number_plate'), request.args.get('motor_power'))
        c.addCar (car)
    return jsonify(
            success = c!=None,
            message = "Customer not found")

    
@app.route("/customer/<customer_id>", methods=["DELETE"])
def deleteCustomer(customer_id):
    result = company.deleteCustomer(customer_id)
    if(result): 
        message = f"Customer with id{customer_id} was deleted"
    else: 
        message = "Customer not found"
    return jsonify(
            success = result, 
            message = message)


@app.route("/customers", methods=["GET"])
def allCustomers():
    return jsonify(customers=[h.serialize() for h in company.getCustomers()])

################Agents####################

#Add a new agent (parameters: name, address).
@app.route("/agent", methods=["POST"])
def addAgent():
    # parameters are passed in the body of the request
    aid = company.addAgent(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new agent with ID {aid}")


#Return the details of an agent of the given agent_id.
@app.route("/agent/<agent_id>", methods=["GET"])
def agentInfo(agent_id):
    a = company.getAgentById(agent_id)
    if(a!=None):
        return jsonify(a.serialize())
    return jsonify(
            success = False, 
            message = "Agent not found")


#Assign a new customer to the agent
@app.route("/agent/<agent_id>/<customer_id>", methods=["POST"])
def addCustomer(agent_id):
    a = company.getAgentById(agent_id)
    if(a!=None): #checks if the agent and customer exists before assigning
        customer = Customer(request.args.get('id'))
        if (customer != None):     
            a.addCustomer (customer)
            return jsonify(success = True,
                           message = f'Added a new customer {customer} to agent {a}')
        return jsonify(
            message = "Error Customer not found")
    return jsonify(message = "Error Agent not found")


@app.route("/agent/<agent_id>", methods=["DELETE"])
#Transfers all of the agents customers to a new agent, deletes the old agent
def deleteAgent(agent_id): #Requests the old and new agent id's for the moveAgentCustomers code
    company.moveAgentCustomers(request.args.get('old_agent_id'),request.args.get('new_agent_id'))
    result = company.deleteAgent(agent_id)
    if(result): 
        message = f"Agent with id{agent_id} was deleted"
    else: 
        message = "Agent not found"
    return jsonify(
            success = result, 
            message = message)

#Returns all of the agents in the company
@app.route("/agents", methods=["GET"])
def allAgents():
    return jsonify(agents=[h.serialize() for h in company.getAgents()])

#############Claims#################

#Add a new claim (parameters: date, description, amount).
@app.route("/claims/<customer_id>/file", methods=["POST"])
def makeClaim(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None): #Checks that the customer exists before allowing the claim
        claim = Claim(request.args.get('date'), request.args.get('description'), request.args.get('amount'))
        c.makeClaim (claim)
        company.addClaim(claim)
        return jsonify(success = True,
                       message = "Claim has been submitted")
    return jsonify(
            success = c!=None,
            message = "Customer not found")


#Selects a claim by its ID returns its details
@app.route("/claims/<claim_id>", methods=["GET"])
def claimInfo(claim_id):
    cl = company.getClaimById(claim_id)
    if(cl!=None):
        return jsonify(cl.serialize())
    return jsonify(
            success = False, 
            message = "Claim not found")

#Returns all the claims in the company database
@app.route("/claims", methods=["GET"]) #return all claims in the company
def allClaims():
    return jsonify(claims=[h.serialize() for h in company.getClaims()])

#Allows an agent to update a claim
@app.route("/claims/<claim_id>/status", methods=["PUT"])
def updateStatus(claim_id):
    agent = company.getAgentById(request.args.get('agent_id'))
    if (agent != None):#Agent must enter their valid id
        newstatus =  request.args.get('newstatus') #Updates the statues to one of the three options
        cl = company.getClaimById(claim_id)
        if newstatus == "Rejected" or newstatus == "Partly Covered" or newstatus == "Fully Covered":
            if (cl!=None):
                cl.status = newstatus.upper()
                return jsonify(f"Status has been updated to {newstatus}")
            return jsonify(success = False, 
                           message = "Error claim not found")
        return jsonify(success = False,
                       message = "Error: status must be updated to 'Rejected', 'Partly Covered' or 'Fully Covered'")
    return jsonify(success = False,
                   message = 'Error only agents can update claim status')


###########Payments##############
@app.route("/payment/in ", methods=["POST"])
#Customer payments into the company
def makePayment(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):#Checks the customer is registered asks for parameters for the payment
        Payment = Payment_In(request.args.get('date'), request.args.get('amount'), customer_id)
        c.makePayment (Payment)
        company.add_customer_payment(Payment)
        return jsonify(success = True,
                       message = "Your payment was successful")
    return jsonify (success = False,
                    message = "Customer not found")
        

@app.route("/payment/out ", methods=["POST"])
#Payments made to Agents
def PayAgent(agent_id):
    c = company.getAgentById(agent_id)
    if(c!=None): #checks the agent is in the system, pays them the required amount
        Payment = Payment_Out(request.args.get('date'), request.args.get('amount'), agent_id)
        company.Pay_Agent (Payment)
        return jsonify(success = True,
                       message = 'Payment successful')
    return jsonify(success = False,
                   message = "Agent not found")

@app.route("/payments/ ", methods=["GET"])
#Shows all payements, first the payments made by customers then the payments to agents
def ViewPayments(): 
    return jsonify(payment=[h.serialize() for h in company.get_In_Payments()]), jsonify(payment=[h.serialize() for h in company.get_Out_Payments()])


#########Stats##############
@app.route("/stats/claims ", methods=["GET"])
#For every agent in the companies agent list, returns a list of the claims managed by them
def ViewClaims():
    for a in company.Agents:
        return jsonify(claims=[h.serialize() for h in a.Agent_Claims()])

@app.route("/stats/revenues ", methods=["GET"])
#For every agent in the companies agent list, returns the payments made to them
def ViewRevenues():
    for a in company.Agents:
        return jsonify(revenue=[h.serialize() for h in a.Agent_Revenues()])

@app.route("/stats/agents ", methods=["GET"])
#Calls on a function that ranks agents and returns the ordered list
def Rank_Agents():
    return jsonify(agents=[h.serialize() for h in a.Sort_Agents()])


###DO NOT CHANGE CODE BELOW THIS LINE ##############################
@app.route("/")
def index():
    return jsonify(
            success = True, 
            message = "Your server is running! Welcome to the Insurance Company API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)