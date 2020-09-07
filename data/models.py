import time

class RevenueDataException(Exception):
    pass

class FinanceEventType:
    REVENUE = 0
    COST = 1
    
class FinanceData:
    def __init__(self, amount, timestamp, description = '', evidence_url = '', event_type = FinanceEventType.REVENUE):
        """
        timestamp is the number obtained by `time.time()`
        amount is the amount identified with revenue (+) and cost (-)
        """
        self.amount = amount
        self.timestamp = timestamp
        self.formatted_time = time.asctime(time.localtime(timestamp))
        self.description = description
        self.evidence_url = evidence_url
        self.event_type = event_type
        
    def to_object(self):
        return {
            'amount': self.amount,
            'timestamp': self.formatted_time,
            'description': self.description,
            'evidence_url': self. evidence_url,
            'event_type': self. event_type
        }
    


