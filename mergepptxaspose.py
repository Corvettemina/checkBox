import changeWord
import asposeslidescloud
import shutil
from asposeslidescloud.apis.slides_api import SlidesApi
from asposeslidescloud.models import *
import platform
import os
import collections
import collections.abc
from pptx import Presentation


def getfile_insensitive(paths):
    for path, subdirs, files in os.walk("/root/Dropbox/PowerPoints/"):
        for name in files:
            #print(os.path.join(path, name).lower())
            if (os.path.join(path, name).lower() == paths.lower()):
                return (os.path.join(path, name))


def makeIntoList(y):

    y["anaphora"] = changeWord.insertChange(y["anaphora"], y["verb"])
    if ("Annual" in y["matinsVerseofTheCymbals"]):
        y["matinsVerseofTheCymbals"] = changeWord.insertChange(
            y["matinsVerseofTheCymbals"], y["verb"])

    if ("Annual" in y["vespersVerseofTheCymbals"]):
        y["vespersVerseofTheCymbals"] = changeWord.insertChange(
            y["vespersVerseofTheCymbals"], y["verb"])

    if ("Annual" in y["praxis"]):
        y["praxis"] = changeWord.insertChange(y["praxis"], y["verb"])

    if ("Annual" in y["hymnofIntercessions"]):
        y["hymnofIntercessions"] = changeWord.insertChange(
            y["hymnofIntercessions"], y["verb"])

    y["gospels"] = changeWord.insertChange(y["gospels"], y["verb"])

    answer = []
    for i in y:
        if (i != "Ocassion" and i != "Season" and i != "Sunday" and i != "verb"):
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
        path = "C:/Users/Mina Hanna/DropBox/"
    if (("Linux" in platform.platform())):
        path = "/root/Dropbox/"

    presentaionsArray = []
    #finishedList.append("PowerPoints/communion.pptx")
    pptxLengths = {}
    totalBeforeCommunion = 0
    count = 0
    atMenu = False
    index = 0
    for i in range(0, len(finishedList), 10):
        files = []
        filesToremove = []
        x = 10
        if(len(finishedList[i+10:i+20]) < 2):
            x = 11
            
        for k in finishedList[i:i+x]:
            print(path + k)
            if ("today.pptx" in path + k):
                filesToremove.append(path+k)
            try:
                with open(path + k, "rb") as file_stream:
                    files.append(file_stream.read())
                    if(finishedList.index(k,index) > finishedList.index("PowerPoints/BackBone/communionMenuTemplate.pptx") and finishedList.index(k,index) < finishedList.index("PowerPoints/BackBone/finalConclusion1.pptx")):
                        pptxLengths[str(k.split("/")[-1].split(".")[0])] = (len(Presentation(path + k).slides))

                    if(finishedList.index(k,index) < finishedList.index("PowerPoints/BackBone/communionMenuTemplate.pptx") and atMenu == False):
                        totalBeforeCommunion = totalBeforeCommunion + (len(Presentation(path + k).slides))
                    if(k == "PowerPoints/BackBone/communionMenuTemplate.pptx"):
                        atMenu = True
                        #totalBeforeCommunion = totalBeforeCommunion - 1

                    
            except:
                try:
                    with open(getfile_insensitive(path + k), "rb") as file_stream:
                        files.append(file_stream.read())
                        if(finishedList.index(k,index) > finishedList.index("PowerPoints/BackBone/communionMenuTemplate.pptx") and finishedList.index(k,index) < finishedList.index("PowerPoints/BackBone/finalConclusion1.pptx")):
                            pptxLengths[str(k.split("/")[-1].split(".")[0])] = (len(Presentation(getfile_insensitive(path + k)).slides))
                   
                        if(finishedList.index(k,index) < finishedList.index("PowerPoints/BackBone/communionMenuTemplate.pptx") and atMenu == False):
                            totalBeforeCommunion = totalBeforeCommunion + (len(Presentation(getfile_insensitive(path + k)).slides))
                        if(k == "PowerPoints/BackBone/communionMenuTemplate.pptx"):
                            atMenu = True
                except:
                    pass
            #print("Before Communion" ,  totalBeforeCommunion)
            index+=1
        print("uploading....")

        slides_api = SlidesApi(
            None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")
        slides_api.merge_and_save_online(
            str(count) + ".pptx", files, None, "internal")

        presentation = PresentationToMerge()
        presentation.path = str(count) + ".pptx"
        presentation.source = "Storage"

        presentaionsArray.append(presentation)

        for i in filesToremove: 
            os.remove(i)

        count += 1
        if x == 11:
            break
    '''
    presentation = PresentationToMerge()
    presentation.path = "communion.pptx"
    presentation.source = "Storage"

    presentaionsArray.append(presentation)
    '''
    request = OrderedMergeRequest()
    request.presentations = presentaionsArray
    response = slides_api.merge_and_save_online(
        "MyPresentation.pptx", None,  request, "internal")

    result_path = path + "PowerPoints/result1.pptx"
    temp_path = slides_api.download_file("MyPresentation.pptx", "internal")
    shutil.copyfile(temp_path, result_path)

    print(pptxLengths)

    if(len(pptxLengths.keys()) > 0):
        print("HEREEEEE")
        from makeCommunionpptx import makePPT
        makePPT(result_path, pptxLengths, totalBeforeCommunion)

    print('complete')


def mergeCommunion(finishedList):
    
    platform.platform()
    if ("Windows" in platform.platform()):
        path = "C:/Users/Mina Hanna/DropBox/"
    if (("Linux" in platform.platform())):
        path = "/root/Dropbox/"

    presentaionsArray = []

    count = 0
    for i in range(0, len(finishedList), 10):
        files = []
        filesToremove = []
        pptxLengths = {}
        for k in finishedList[i:i+10]:
            print(path + k)
            if ("today.pptx" in path + k):
                filesToremove.append(path+k)
            try:
                with open(path + k, "rb") as file_stream:
                    files.append(file_stream.read())
                    #print(str(k.split("/")[-1].split(".")[0]))
                    if(finishedList.index(k) > finishedList.index("PowerPoints/BackBone/communionMenuTemplate.pptx") and finishedList.index(k) < finishedList.index("PowerPoints/BackBone/finalConclusion1.pptx")):
                        pptxLengths[str(k.split("/")[-1].split(".")[0])] = (len(Presentation(path + k).slides))
            except:
                #print("here", getfile_insensitive(path+i))
                try:
                    with open(getfile_insensitive(path + k), "rb") as file_stream:
                        files.append(file_stream.read())
                        #print(str(k.split("/")[-1].split(".")[0]))
                        if(k!= finishedList[0] and k != finishedList[-1] and k != finishedList[-2] and k != finishedList[-3] and k != finishedList[-4]):
                            pptxLengths[str(k.split("/")[-1].split(".")[0])] = (len(Presentation(getfile_insensitive(path + k)).slides))
                except:
                    pass

        print("uploading....")
        print(pptxLengths)
        slides_api = SlidesApi(
            None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")
        slides_api.merge_and_save_online("communion.pptx", files, None, "internal")

    result_path = path + "PowerPoints/communion.pptx"
    temp_path = slides_api.download_file("communion.pptx", "internal")
    shutil.copyfile(temp_path, result_path)

    print('creating menu slide')
    
    if(len(pptxLengths.keys()) > 0):
        from makeCommunionpptx import makePPT
        makePPT(result_path, pptxLengths)

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
