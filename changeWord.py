import collections 
import collections.abc
from pptx import Presentation
import platform

def insertChange(input_pptx, replaceString):

    if ("Windows" in platform.platform()):
        path = "C:/Users/minah/DropBox/"
    if (("Linux" in platform.platform())):
        path = "/root/Dropbox/"

    prs = Presentation(path + input_pptx)
    #slide = prs.slides[242]

    testString = '#SEASON#'
 

    # iterate through all shapes on slide
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
                
            # iterate through paragarphs in shape
            for p in shape.text_frame.paragraphs:
                # store formats and their runs by index (not dict because of duplicate runs)
                formats, newRuns = [], []
        
                # iterate through runs
                for r in p.runs:
                    # get text
                    text = r.text
                    
                    # replace text
                    text = text.replace(testString,replaceString)
        
                    # store run
                    newRuns.append(text)
        
                    # store format
                    formats.append({'size':r.font.size,
                                    'bold':r.font.bold,
                                    'underline':r.font.underline,
                                    'italic':r.font.italic})
        
                # clear paragraph
                p.clear()
        
                # iterate through new runs and formats and write to paragraph
                for i in range(len(newRuns)):
                    # add run with text
                    run = p.add_run()
                    run.text = newRuns[i]
        
                    # format run
                    run.font.bold = formats[i]['bold']
                    run.font.italic = formats[i]['italic']
                    run.font.size = formats[i]['size']
                    run.font.underline = formats[i]['underline']
    tempArray = input_pptx.split(".pptx")
    newPath = tempArray[0] + "today.pptx" 

    prs.save(path + newPath)
    #newPath = newPath.replace(path,"")

    return newPath

#insertChange("C:/Users/minah/Documents/checkBox/Anaphora - Basil.pptx","have come")