import asposeslidescloud
import shutil
from asposeslidescloud.apis.slides_api import SlidesApi
from asposeslidescloud.models import *
import platform
import springApiTest
import os


def getfile_insensitive(paths):
    for path, subdirs, files in os.walk("/root/Dropbox/PowerPoints/"):
        for name in files:
            #print(os.path.join(path, name).lower())
            if (os.path.join(path, name).lower() == paths.lower()):
                return (os.path.join(path, name))


platform.platform()
if ("Windows" in platform.platform()):
    path = "C:/Users/Mina Hanna/OneDrive/"
if (("Linux" in platform.platform())):
    path = "/root/Dropbox/"

slides_api = SlidesApi(
    None, "2d3b1ec8-738b-4467-915f-af02913aa7fa", "1047551018f0feaacf4296fa054d7d97")
files = []

for i in springApiTest.getlist():
    print(path + i)
    try:
        with open(path + i, "rb") as file_stream:
            files.append(file_stream.read())
    except:
        #print("here", getfile_insensitive(path+i))
        with open(getfile_insensitive(path+i), "rb") as file_stream:
            files.append(file_stream.read())


print("uploading....")

slides_api.merge_and_save_online(
    "MyPresentation.pptx", files, None, "internal")

storage_name = "internal"
file_path = "MyPresentation.pptx"
result_path = path + "PowerPoints/result1.pptx"
print("downloading....")

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
