#!usr/bin/env/python
from datetime import date, timedelta
import time

def daterange(start, end):
    for n in range(int((end-start).days)):
        yield start + timedelta(n)

def benchmark(func):
    def wrapper(*args, **kwargs):       
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end-start)
    return wrapper


