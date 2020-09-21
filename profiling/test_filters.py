from data.models import FinanceData
from search_engine.filters import ComposedFilter, DateRangeFilter, KeyWordFilter, TagFilter
import random, time

composed_filter = ComposedFilter(filters = [
    KeyWordFilter(['gen', 'Aut']),
    DateRangeFilter('1-12-2019', '31-12-2020'),
    TagFilter('Revenue'),
    KeyWordFilter(['gen', 'Aut']),  
    KeyWordFilter(['gen', 'Aut']),
    DateRangeFilter('1-12-2019', '31-12-2020'),
    TagFilter('Revenue'),
    KeyWordFilter(['gen', 'Aut']), 
    KeyWordFilter(['gen', 'Aut']),
    DateRangeFilter('1-12-2019', '31-12-2020'),
    TagFilter('Revenue'),
    KeyWordFilter(['gen', 'Aut']),  
    KeyWordFilter(['gen', 'Aut']),
    DateRangeFilter('1-12-2019', '31-12-2020'),
    TagFilter('Revenue'),
    KeyWordFilter(['gen', 'Aut']), 
])
composed_b_filter = ComposedFilter(filters = [
    KeyWordFilter(['gen', 'Aut']),
    DateRangeFilter('1-12-2019', '31-12-2020'),
    TagFilter('Revenue'), 
])

scale = lambda x: x*10

scales = []
data_gen_time = []
filter_time = []
filter_b_time = []
case = 0
size = 1000

while case < size:
    case += 1
    if case % (size/100) == 0:
        print('■', end='')

    data_array = []
    scales.append(scale(case))
    
    st = time.perf_counter_ns()
    for _ in range(scale(case)):
        data_array.append(FinanceData(
            random.randint(1,10000),
            time.time() + random.randint(-399339354, 99339354),
            tags = ['Revenue'],
            description='Auto generated'
            )
        )

    for _ in range(scale(case)):
        data_array.append(FinanceData(
            random.randint(-100000,-1),
            time.time() + random.randint(-399339354, 99339354),
            )
        )
    span = time.perf_counter_ns() - st
    data_gen_time.append(span*1e-6)
    
    st = time.perf_counter_ns()
    ta = composed_filter.filter(data_array)
    span = time.perf_counter_ns() - st
    filter_time.append(span*1e-6)
    
    st = time.perf_counter_ns()
    ta = composed_b_filter.filter(data_array)
    span = time.perf_counter_ns() - st
    filter_b_time.append(span*1e-6)
from matplotlib import pyplot as plt

plt.plasma()
gen_time, =plt.plot(scales, data_gen_time, color='red', label='data generation time')

filt_a_time, =plt.plot(scales, filter_time, color='green', label='filtering time (16 filters loaded)')
filt_b_time, =plt.plot(scales, filter_b_time, color='blue', label='filtering time (3 filters loaded)')
plt.legend(handles=[gen_time, filt_a_time, filt_b_time])
plt.xlabel('Number of Unfiltered Rows')
plt.ylabel('Processing Time (ms)')
plt.show()