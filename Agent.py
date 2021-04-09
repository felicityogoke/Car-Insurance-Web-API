import uuid


# Represents the insurance agent
class Agent:
    def __init__(self, name, address):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.address = address
        self.Assigned_customers = []
        self.revenue = 0

    # convert object to JSON

    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'address': self.address,
            'Assigned_customers': self.Assigned_customers,
            'revenue': self.revenue
        }

    def Assign(self, cust):
        self.Assigned_customers.append(cust)
