from data.models import FinanceData
from typing import List
data_array: List[FinanceData] = []
import datetime
import random, time

for _ in range(128):
    data_array.append(FinanceData(
        random.randint(1,10000),
        datetime.datetime.now(),
        )
    )

for _ in range(128):
    data_array.append(FinanceData(
        random.randint(-100000,-1),
        datetime.datetime.now(),
        )
    )
    
sorted_data_array = sorted(data_array, key = lambda x: -x.timestamp.timestamp())

def obtain_range(start, end):
    global sorted_data_array
    return [el.to_object() for el in sorted_data_array[start: end]]

def obtain_total_number():
    global sorted_data_array
    return len(sorted_data_array)

