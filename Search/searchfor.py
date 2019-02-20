import os
import time
import requests
from bs4 import BeautifulSoup
import re

def searchfor(self, subject, unit, topic):
    page = requests.get("https://www.google.co.in/search?q={}+{}".format(topic, subject))
    soup = BeautifulSoup(page.content, "lxml")
    page.connection.close()
    links = soup.findAll("a")
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        yield re.split(":(?=http)",link["href"].replace("/url?q=",""))
