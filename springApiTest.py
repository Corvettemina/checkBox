import platform
from unittest import mock
import requests
import json
import os
import datetime

today = datetime.date.today()
d1 = today.strftime("%Y-%m-%d")

copticDay = ""


class Springapi:
    copticDay = ""
    season = ""
    occasion = ""
    sunday = ""
    dictionary = {}

    def __init__(self, date=d1):
        self.date = date
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

        response = requests.get(
            'http://192.81.219.24:8080/greeting?date=' + str(newDate))

        answer = []
        y = json.loads(response.text)

        # print(y[0]['standardDoxologies'])
        self.copticDay = (y[0]['date'])
        self.sunday = (y[1]['Sunday'])
        self.season = (y[1]['Season'])
        self.occasion = (y[1]['Ocassion'])
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

    def getlist(self):
        pass

        '''        for i in y[1]:
            if (i != "Ocassion" and i != "Season" and i != "Sunday"):
                if (type(y[1][i]) is list):
                    for l in y[1][i]:
                        # print(l)
                        #print(getfile_insensitive(path + l))
                        l = l.replace('powerpoints', 'PowerPoints')
                        answer.append(l)
                        pass
                else:
                    # print(y[1][i])
                    if (y[1][i] != ""):
                        answer.append(y[1][i])
        print(answer)'''


# print(Springapi().getlist()["seasonVespersDoxologies"])
'''
spring = Springapi()
print(spring.getlist())

print(platform.platform())
for i in getlist():
    print(i)
'''
