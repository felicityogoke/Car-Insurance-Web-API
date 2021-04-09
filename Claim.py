import uuid


class Claim:
    def __init__(self, date, incident_description, claim_amount):
        self.ID = str(uuid.uuid1())
        self.date = date
        self.incident_description = incident_description
        self.claim_amount = claim_amount
        self.status = None
        self.approved_amount = None

    # convert object to JSON
    def serialize(self):
        return {
            'id': self.ID,
            'date': self.date,
            'incident': self.incident_description,
            'claim amount': self.claim_amount,
            'status': self.status,
            'approved_amount': self.approved_amount
        }

    def Approved(self, Amnt):
        self.approved_amount = Amnt
        return Amnt
