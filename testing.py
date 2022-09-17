import os

paths = "/root/Dropbox/PowerPoints/doxologies/stmarkdoxologies.pptx"
#newPath = paths.split("/")
#tempPath = ('/').join(newPath[:(len(newPath)-1)])

# print(tempPath)


for path, subdirs, files in os.walk("/root/Dropbox/PowerPoints/"):
    for name in files:
        #print(os.path.join(path, name).lower())
        if (os.path.join(path, name).lower() == paths.lower()):
            print(os.path.join(path, name))
            break
