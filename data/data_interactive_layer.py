from data.models import FinanceData
from utils.sql_connection import connection
import time
from utils.asizeof import asizeof
from typing import List

financial_records: List[FinanceData] = []

total_revenue = 0
total_cost = 0


print('loading data...')
with connection() as cursor:
    st = time.perf_counter_ns()
    cursor.execute('SELECT * FROM %s;'%FinanceData.SQL_TABLE_NAME)
    print('    · loading data from database...')
    results = cursor.fetchall()
    print('    · building object cache layer and statistics...')
    
    for result in results:
        record: FinanceData = FinanceData.from_sql(result)
        if record.amount > 0:
            total_revenue += record.amount 
        else:
            total_cost -= record.amount # because the absolue amount is negative.
        financial_records.append(record)
    print('    · sorting...')
    financial_records = sorted(financial_records, key = lambda x: x.timestamp.timestamp())
    span = time.perf_counter_ns() - st

    print('Loaded',len(financial_records), 'rows;','with time', span/1e6, 'ms.')
    print('calculating memory consumption...')
    print('Cache size:', round(asizeof(financial_records)/1024/1024, 4), 'MB.')
    
def obtain_all_data() -> List[FinanceData]:
    global financial_records
    return financial_records

def obtain_total_number():
    global financial_records
    return financial_records

def obtain_stats():
    global total_cost, total_revenue
    return total_cost, total_revenue
def new_record(self, finance_data: FinanceData):
    with connection() as cursor:
        finance_data.to_sql(cursor)
    global financial_records
    financial_records.append(finance_data)
    
    if finance_data.amount > 0:
        total_revenue += finance_data.amount 
    else:
        total_cost -= finance_data.amount # because the absolue amount is negative.


    