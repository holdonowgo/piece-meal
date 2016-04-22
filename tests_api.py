#!flask/bin/python
import os
import unittest
import datetime
from datetime import date, timedelta
from config import basedir
from app import app, db
from coverage import coverage
from Flask import Response, Request

cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()