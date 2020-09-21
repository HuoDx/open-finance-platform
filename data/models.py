import time
from datetime import datetime
class FinanceData:
    SQL_TABLE_NAME = 'financial_data'
    def __init__(self, amount: int, timestamp: datetime, tags = [], description = ''):
        """
        timestamp is the datetime object obtained by `datetime.datetime.now()`
        amount is the amount identified with revenue (+) and cost (-)
        """
        self.amount = amount
        self.timestamp = timestamp
        self.formatted_time = self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        self.tags = tags
        self.description = description
        
    def to_object(self):
        return {
            'amount': self.amount,
            'timestamp': self.formatted_time,
            'description': self.description,
            'tags': self.tags
        }
        
    def __repr__(self):
        return '| %s | %s | %s | %s | \n'%(
            self.amount,
            self.formatted_time,
            self.description,
           ', '.join(self.tags)
        )
    def to_sql(self, cursor):
        cursor.execute('INSERT INTO financial_data VALUES(%s, %s, %s, %s);', 
                       (self.amount,
                       self.timestamp,
                       self.tags,
                       self.description)
        )
    @classmethod
    def from_sql(cls, sql_result):
        return FinanceData(
            sql_result[0],
            sql_result[1],
            sql_result[2],
            sql_result[3]
            )
    


