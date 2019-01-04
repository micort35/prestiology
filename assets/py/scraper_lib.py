#!usr/bin/env/python
from datetime import date, timedelta

def daterange(start, end):
    for n in range(int((end-start).days)):
        yield start + timedelta(n)