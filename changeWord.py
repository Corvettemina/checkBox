import collections 
import collections.abc
from pptx import Presentation
from pptx.dml.color import RGBColor
import platform

def insertChange(input_pptx, replaceString):

    if ("Windows" in platform.platform()):
        path = "C:/Users/minah/DropBox/"
    if (("Linux" in platform.platform())):
        path = "/root/Dropbox/"

    prs = Presentation(path + input_pptx)
    #slide = prs.slides[242]

    testString = "#SEASON#"
 
    '''
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
                                    'italic':r.font.italic,
                                    'color':r.font.color})
        
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
                    run.font.color = formats[i]['color']

    tempArray = input_pptx.split(".pptx")
    newPath = tempArray[0] + "today.pptx" 

    prs.save(path + newPath)
    #newPath = newPath.replace(path,"")
    '''
    
    # To get shapes in your slides
    slides = [slide for slide in prs.slides]
    shapes = []
    for slide in slides:
        for shape in slide.shapes:
            shapes.append(shape)

    replaces = {
                        testString: replaceString
                }
    
    for shape in shapes:
        for match, replacement in replaces.items():
            if shape.has_text_frame:
                if (shape.text.find(match)) != -1:
                    text_frame = shape.text_frame
                    for paragraph in text_frame.paragraphs:
                        whole_text = "".join(run.text for run in paragraph.runs)
                        whole_text = whole_text.replace(str(match), str(replacement))
                        for idx, run in enumerate(paragraph.runs):
                            if idx != 0:
                                p = paragraph._p
                                p.remove(run._r)
                        if bool(paragraph.runs):
                            paragraph.runs[0].text = whole_text
    
    tempArray = input_pptx.split(".pptx")
    newPath = tempArray[0] + "today.pptx" 

    prs.save(path + newPath)
    return newPath

insertChange("PowerPoints/Agpeya/gospels.pptx","have come")