from Customer import *
from Agent import *
from Claim import *
from Payment import *


class InsuranceCompany:
    def __init__(self, name):
        self.name = name  # Name of the Insurance company
        self.customers = []  # list of customers
        self.agents = []  # list of dealers
        self.Assigned_customers = []
        self.claims = []
        self.Payments = []

    def getCustomers(self):
        return list(self.customers)

    def addCustomer(self, name, address):
        c = Customer(name, address)
        self.customers.append(c)
        return c.ID

    def getCustomerById(self, id_):
        for d in self.customers:
            if d.ID == id_:
                return d
        return None

    def deleteCustomer(self, customer_id):
        c = self.getCustomerById(customer_id)
        self.customers.remove(c)

        # AGENTS

    def getAgents(self):
        return list(self.agents)

    def addAgents(self, name, address):
        a = Agent(name, address)
        self.agents.append(a)
        return a.ID

    def getAgentById(self, id_):
        for a in self.agents:
            if a.ID == id_:
                return a
        return None

    def deleteAgent(self, Agent_id):
        a = self.getAgentById(Agent_id)
        self.agents.remove(a)

    # CLAIMS
    def addClaim(self, date, incident_description, claim_amount):
        c = Claim(date, incident_description, claim_amount)
        self.claims.append(c)
        return c.ID

    def getClaims(self):
        return list(self.claims)

    def getClaimById(self, id_):
        for a in self.claims:
            if a.ID == id_:
                return a
        return None

    # PAYMENTS

    def getPayments(self):
        return list(self.Payments)
