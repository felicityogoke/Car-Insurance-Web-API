from flask import Flask, request, jsonify
from InsuranceCompany import *
from Customer import *
from Payment import *

app = Flask(__name__)

# Root object for the insurance company
# Root object for the insurance company
company = InsuranceCompany("Be-Safe Insurance Company")


# Add a new customer (parameters: name, address).
@app.route("/customer", methods=["POST"])
def addCustomer():
    # parameters are passed in the body of the request
    cid = company.addCustomer(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new customer with ID {cid}")


# Return the details of a customer of the given customer_id.
@app.route("/customer/<customer_id>", methods=["GET"])
def customerInfo(customer_id):
    c = company.getCustomerById(customer_id)
    if c != None:
        return jsonify(c.serialize())
    return jsonify(
        success=False,
        message="Customer not found")


# Add a new car (parameters: model, numberplate).
@app.route("/customer/<customer_id>/car", methods=["POST"])
def addCar(customer_id):
    c = company.getCustomerById(customer_id)
    if (c != None):
        car = Car(request.args.get(',model'), request.args.get('number_plate'), request.args.get('motor_power'),
                  request.args.get('year'))
        c.addCar(car.serialize())
    return jsonify(
        success=c != None,
        message="Customer not found")


@app.route("/customer/<customer_id>", methods=["DELETE"])
def deleteCustomer(customer_id):
    result = company.deleteCustomer(customer_id)
    if result:
        message = f"Customer with id{customer_id} was deleted"
    else:
        message = "Customer not found"
    return jsonify(
        success=result,
        message=message)


@app.route("/customers", methods=["GET"])
def allCustomers():
    return jsonify(customers=[h.serialize() for h in company.getCustomers()])


# Add a new Insurance Agent (parameters: name, address).
@app.route("/agent", methods=["POST"])
def addAgent():
    # parameters are passed in the body of the request
    cid = company.addAgents(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new Agent with ID {cid}")


# Return the details of an agent with the given agent_id.
@app.route("/agent/<agent_id>", methods=["GET"])
def AgentInfo(agent_id):
    a = company.getAgentById(agent_id)
    if a != None:
        return jsonify(a.serialize())
    return jsonify(
        success=False,
        message="Agent not found")


# assign customers to agents
@app.route("/agent/<agent_id>/<customer_id>", methods=["POST"])
def AssignCustomer(agent_id, customer_id):
    agent_ = company.getAgentById(agent_id)
    customer_ = company.getCustomerById(customer_id)
    agent_.Assign(customer_.serialize())
    return jsonify(f"Assigned new client: {customer_.serialize()} to {agent_.name}")


# Delete Agent with given agent ID
@app.route("/agent/<agent_id>", methods=["DELETE"])
# get agent by id:
def DeleteAgent(agent_id):
    for a in company.getAgents():
        if company.getAgentById(agent_id) == a:
            if a.Assigned_customers:  # check if agent has customers.......if no? go to line78
                n_a = company.getAgents().index(a)
                n_a += 1
                next_a = company.getAgents()[n_a]
                next_a.Assign(a.Assigned_customers)  # if yes? then assign customers to next agent in list
                company.deleteAgent(a.ID)
                return jsonify(f"Deleted agent {a.name} from list, customers are reassigned to {next_a.name}")
            company.deleteAgent(a.ID)  # delete agent
            return jsonify(f"Deleted agent {a.name} from list!")


# get a list of all agents
@app.route("/agents", methods=["GET"])
def allAgents():
    return jsonify(agents=[h.serialize() for h in company.getAgents()])


# add claims
@app.route("/claims/<customer_id>/file", methods=["POST"])
def addClaim(customer_id):
    customer_ = company.getCustomerById(customer_id)
    claim_id = company.addClaim(request.args.get('date'), request.args.get('incident_description'),
                                request.args.get('claim_amount'))
    customer_.File_claim(company.getClaimById(claim_id).serialize())
    return jsonify(f"{customer_.name} has filed up an Insurance claim of ID: {claim_id}")


# Return the details of claim
@app.route("/claims/<claim_id>", methods=["GET"])
def ClaimInfo(claim_id):
    a = company.getClaimById(claim_id)
    if a != None:
        return jsonify(a.serialize())
    return jsonify(
        success=False,
        message="Claim not found")


# change status
@app.route("/claims/<claim_id>/status", methods=["PUT"])
def setStaus(claim_id):
    c = company.getClaimById(claim_id)
    Amount = c.Approved(request.args.get('approved_amount'))  # not sure about thus one
    # n = int(c.claim_amount)
    if int(Amount) > int(c.claim_amount):
        c.status = "PARTLY COVERED"
    if int(Amount) == int(c.claim_amount):
        c.status = "FULLY COVERED"
    if int(Amount) < int(c.claim_amount):
        c.status = "REJECTED"

    return jsonify(f"Approved Amount: {Amount}, Claim Amount: {c.claim_amount}, Status: {c.status}")


# return list of all claims
@app.route("/claims", methods=["GET"])
def allClaims():
    return jsonify(claims=[h.serialize() for h in company.getClaims()])


# Financials

# Add a new payment received from a customer parameters: date, customer_id, amount_received.
@app.route("/payment/in/", methods=["POST"])
def PaymentIn():
    try:
        payment_ = Payment(request.args.get('date'), request.args.get('customer_id'), request.args.get('amount_recieved'))
        company.Payments.append(payment_.serialize())
        customer = company.getCustomerById(payment_.id_)
        customer.payments += int(payment_.Amount)
        return jsonify(f"Client {customer.name} paid a sum of {payment_.Amount} on {payment_.date}")
    except ValueError:
        return jsonify("  ")

# Add a new payment to agent parameters: date, agent_id, amount_sent.
@app.route("/payment/out/", methods=["POST"])
def PaymentOut():
    try:
        payment_ = Payment(request.args.get('date'), request.args.get('agent_id'), request.args.get('amount_sent'))
        company.Payments.append(payment_.serialize())
        agent = company.getAgentById(payment_.id_)
        agent.revenue += int(payment_.Amount)
        return jsonify(f"Agent {agent.name} recieved a monthly salary of {payment_.Amount} on {payment_.date}")
    except ValueError:
        return jsonify("  ")


# return list of all Incoming and Outgoing Payments
@app.route("/payments/", methods=["GET"])
def allPayments():
    return jsonify(payments=[p for p in company.getPayments()])



# return list of all Incoming and Outgoing Payments
@app.route("/stats/claims", methods=["GET"])
def Stats_Claim():
    claims = []
    for a in company.getAgents():
        for c in a.Assigned_customers:
            claims.append(f"{a.name} :{c['claims']}")
    return jsonify(claims)

# return all revenue by responsible agents
@app.route("/stats/revenues", methods=["GET"])
def Stats_Revenue():
    all_revenue = []
    for a in company.getAgents():
        all_revenue.append(f"{a.name} :{a.revenue}")
    return jsonify(all_revenue)



# sorted list of agents
# agents sorted from most to least assigned customers
@app.route("/stats/agents", methods=["GET"])
def Stats_agents():
    def SortByCust(elem):
        return len(elem.Assigned_customers)

    agent_list = [a for a in company.getAgents()]
    agent_list.sort(key=SortByCust, reverse=True)

    return jsonify([a.serialize() for a in agent_list])










# #DO NOT CHANGE CODE BELOW THIS LINE ##############################
@app.route("/")
def index():
    return jsonify(
        success=True,
        message="Your server is running! Welcome to the Insurance Company API.")


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE"
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8888)
