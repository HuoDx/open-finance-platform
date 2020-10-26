import time, datetime, random
from typing import List
from data.models import FinanceData
from utils.sql_connection import connection

import psycopg2
from psycopg2 import pool
from config import Database
postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 2048,
                                              user = Database.user,
                                              password = Database.password,
                                              host = Database.host,
                                              port = Database.port,
                                              database = Database.database)

scale = lambda x: x*10

scales = []
data_gen_time = []
filter_time = []
filter_b_time = []
case = 0
size = 64

while case < size:
    case += 1
    if case % (size/100) == 0:
        print('■', end='')

    data_array: List[FinanceData] = []
    scales.append(scale(case))
    
    st = time.perf_counter_ns()
    for _ in range(scale(case)//2):
        data_array.append(FinanceData(
            random.randint(1,2000),
            datetime.datetime.now(),
            tags = ['Revenue'],
            description='Auto generated'
            )
        )

    for _ in range(int(scale(case)/2.25)):
        data_array.append(FinanceData(
            random.randint(-5000,-1),
            datetime.datetime.now(),
            tags = ['Cost'],
            description="Buying paper."
            )
        )
    span = time.perf_counter_ns() - st
    data_gen_time.append(span*1e-6)
    
    st = time.perf_counter_ns()
    for _ in data_array:
        conn = postgreSQL_pool.getconn()
        csr = conn.cursor()
        _.to_sql(csr)
        conn.commit()
        csr.close()
        postgreSQL_pool.putconn(conn)
    span = time.perf_counter_ns() - st
    filter_time.append(span*1e-6)
    
    st = time.perf_counter_ns()
    for _ in data_array:
        with connection() as csr:
            _.to_sql(csr)
            
    span = time.perf_counter_ns() - st
    filter_b_time.append(span*1e-6)
from matplotlib import pyplot as plt

plt.plasma()
gen_time, =plt.plot(scales, data_gen_time, color='red', label='data generation time')

filt_a_time, =plt.plot(scales, filter_time, color='green', label='SQL Execution time (raw)')
filt_b_time, =plt.plot(scales, filter_b_time, color='blue', label='SQL Execution time (with context manager)')
plt.legend(handles=[gen_time, filt_a_time, filt_b_time])
plt.xlabel('Number of SQL Operations')
plt.ylabel('Processing Time (ms)')
plt.show()