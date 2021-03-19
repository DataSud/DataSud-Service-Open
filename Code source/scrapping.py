#! /bin/python3

import re, json

import requests
from bs4 import BeautifulSoup

SITE = "<URL SITE WEB>"

homepage = requests.get(SITE)

print(homepage)
