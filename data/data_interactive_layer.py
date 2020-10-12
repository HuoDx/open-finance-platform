from data.models import FinanceData
from utils.sql_connection import connection
import time
from utils.asizeof import asizeof
from typing import List

financial_records: List[FinanceData] = []
tags: List[str] = []

total_revenue = 0
total_cost = 0


print('loading data...')

def _update_tags(_tags: List[str]):
    global tags;
    for tag in _tags:
        if tag not in tags:
            tags.append(tag)
            
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
    print('    · building tags...')
    for financial_record in financial_records:
        _update_tags(financial_record.tags)
    span = time.perf_counter_ns() - st

    print('Loaded',len(financial_records), 'rows;','with time', span/1e6, 'ms.', len(tags), 'tag(s) discovered.')
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

def new_record(finance_data: FinanceData):
    with connection() as cursor:
        finance_data.to_sql(cursor)
    global financial_records, tags
    financial_records.append(finance_data)
    _update_tags(finance_data.tags)
    
    if finance_data.amount > 0:
        total_revenue += finance_data.amount 
    else:
        total_cost -= finance_data.amount # because the absolue amount is negative.

def obtain_tags():
    global tags
    return tags

    