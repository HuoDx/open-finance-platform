from data.models import FinanceData, FinanceEventType
data_array = []
import random, time

for _ in range(128):
    data_array.append(FinanceData(
        random.randint(1,10000),
        time.time() + random.randint(-399339354, 99339354)
        )
    )

for _ in range(128):
    data_array.append(FinanceData(
        random.randint(-100000,-1),
        time.time() + random.randint(-399339354, 99339354),
        event_type=FinanceEventType.COST
        )
    )
    
sorted_data_array = sorted(data_array, key = lambda x: -x.timestamp)

def obtain_range(start, end):
    global sorted_data_array
    return [el.to_object() for el in sorted_data_array[start: end]]


