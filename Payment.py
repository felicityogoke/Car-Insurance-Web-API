class Payment:
    def __init__(self, date, id_, Amount):
        self.date = date
        self.id_ = id_
        self.Amount = Amount

    def serialize(self):
        return {
            'date': self.date,
            'id_': self.id_,
            'Amount': self.Amount
        }
