import platform
from unittest import mock
import requests
import json
import os
import datetime
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

today = ""
d1 = ""

copticDay = ""


class Springapi:
    today = datetime.date.today()
    d1 = today.strftime("%Y-%m-%d")
    copticDay = ""
    season = ""
    occasion = ""
    sunday = ""
    dictionary = {}

    def __init__(self, path):
        
        today = datetime.date.today()
        d1 = today.strftime("%Y-%m-%d")
        self.date = path
        try:
            datearr = self.date.split(" ")

            datetime_object = datetime.datetime.strptime(datearr[2], "%b")
            month_number = datetime_object.month
            if (month_number < 10):
                month_number = "0" + str(month_number)

            newDate = str(datearr[3]) + '-' + \
                str(month_number) + '-' + str(datearr[1])
        except:
            newDate = d1
        
        print(path)
        response = requests.get(
                'https://stmarkapi.com:8080/greeting/?date=' + newDate , verify=False)
  
        
        y = json.loads(response.text)

        self.dictionary = y[1]
        
    def getfile_insensitive(self):
        if ("Windows" in platform.platform()):
            path = "C:/Users/Mina Hanna/DropBox/"
        if (("Linux" in platform.platform())):
            path = "/root/Dropbox/"
        directory, filename = os.path.split(path)
        directory, filename = (directory or '.'), filename.lower()
        for f in os.listdir(directory):
            newpath = os.path.join(directory, f)
            if os.path.isfile(newpath) and f.lower() == filename:
                return newpath


