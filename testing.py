import os

paths = "/root/Dropbox/PowerPoints/doxologies/stmarkdoxologies.pptx"
#newPath = paths.split("/")
#tempPath = ('/').join(newPath[:(len(newPath)-1)])

# print(tempPath)
dictionary = {'standardPsalm150': 6, 'Psalm150': 7, 'Fraction to the Father for Advent and the Nativity': 3}


test = ["1","2","1","4","5"]
i = 0
print((test.index("1",1)))

'''
for path, subdirs, files in os.walk("/root/Dropbox/PowerPoints/"):
    for name in files:
        #print(os.path.join(path, name).lower())
        if (os.path.join(path, name).lower() == paths.lower()):
            print(os.path.join(path, name))
            break
'''
