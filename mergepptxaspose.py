import asposeslidescloud
import shutil
from asposeslidescloud.apis.slides_api import SlidesApi
from asposeslidescloud.models import *
import platform
import os


def getfile_insensitive(paths):
    for path, subdirs, files in os.walk("/root/Dropbox/PowerPoints/"):
        for name in files:
            #print(os.path.join(path, name).lower())
            if (os.path.join(path, name).lower() == paths.lower()):
                return (os.path.join(path, name))

import changeWord
def makeIntoList(y):
    
    y["anaphora"] = changeWord.insertChange(y["anaphora"], y["verb"])
    if("Annual" in y["matinsVerseofTheCymbals"]):
        y["matinsVerseofTheCymbals"] = changeWord.insertChange(y["matinsVerseofTheCymbals"], y["verb"])
          
    if("Annual" in y["vespersVerseofTheCymbals"]):
        y["vespersVerseofTheCymbals"] = changeWord.insertChange(y["vespersVerseofTheCymbals"], y["verb"])
    
    if("Annual" in y["praxis"]):
        y["praxis"] = changeWord.insertChange(y["praxis"], y["verb"])
    
    if("Annual" in y["hymnofIntercessions"]):
        y["hymnofIntercessions"] = changeWord.insertChange(y["hymnofIntercessions"], y["verb"])

    y["gospels"] = changeWord.insertChange(y["gospels"], y["verb"])

    answer = []
    for i in y:
        if (i != "Ocassion" and i != "Season" and i != "Sunday" and i != 'verb'):
            if (type(y[i]) is list):
                for l in y[i]:
                    # print(l)
                    #print(getfile_insensitive(path + l))
                    l = l.replace('powerpoints', 'PowerPoints')
                    answer.append(l)
                    pass
            else:
                # print(y[1][i])
                if (y[i] != ""):
                    answer.append(y[i])
    
    return (answer)


def merge(finishedList):

    platform.platform()
    if ("Windows" in platform.platform()):
        path = "C:/Users/minah/DropBox/"
    if (("Linux" in platform.platform())):
        path = "/root/Dropbox/"

    presentaionsArray = []

    count = 0
    for i in range(0, len(finishedList), 10):
        files = []
        for k in finishedList[i:i+10]:
            print(path + k)
            try:
                with open(path + k, "rb") as file_stream:
                    files.append(file_stream.read())
            except:
                #print("here", getfile_insensitive(path+i))
                with open(getfile_insensitive(path + k), "rb") as file_stream:
                    files.append(file_stream.read())

        print("uploading....")

        slides_api = SlidesApi(
            None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")
        slides_api.merge_and_save_online(
            str(count) + ".pptx", files, None, "internal")

        presentation = PresentationToMerge()
        presentation.path = str(count) + ".pptx"
        presentation.source = "Storage"

        presentaionsArray.append(presentation)

        count += 1

    request = OrderedMergeRequest()
    request.presentations = presentaionsArray
    response = slides_api.merge_and_save_online("MyPresentation.pptx",None,  request, "internal")
    
    result_path = path + "PowerPoints/result1.pptx"
    temp_path = slides_api.download_file("MyPresentation.pptx", "internal")
    shutil.copyfile(temp_path, result_path)
    
    print('complete')


'''
import springApiTest

request = OrderedMergeRequest()
lists = []
for i in springApiTest.getlist():
    presentation = PresentationToMerge()
    presentation.path = i
    presentation.source = "Storage"
    lists.append(presentation)

request.presentations = lists

slides_api.merge_and_save_online("Powerpoints/blank.pptx", None,request,"Dropbox1")


# Merge the presentations.
result_file_path = slides_api.merge_online(files)

print("The output presentation was saved to ", result_file_path)
'''
