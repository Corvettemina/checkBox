import collections
import collections.abc
from pptx import Presentation
from pptx.dml.color import RGBColor
import platform


def insertChange(input_pptx, replaceString):

    if ("Windows" in platform.platform()):
        path = "C:/Users/Mina Hanna/DropBox/"
    if (("Linux" in platform.platform())):
        path = "/root/Dropbox/"

    prs = Presentation(input_pptx)
    #slide = prs.slides[242]

    testString = "#SEASON#"

 
    # To get shapes in your slides
    slides = [slide for slide in prs.slides]
    shapes = []
    for slide in slides:
        try:
            for shape in slide.shapes:
                shapes.append(shape)
        except:
            print("EXCEPTION")

    replaces = {
        testString: replaceString
    }
    
    for shape in shapes:
        for match, replacement in replaces.items():
            if shape.has_text_frame:
                if (shape.text.find(match)) != -1:
                    text_frame = shape.text_frame
                    for paragraph in text_frame.paragraphs:
                        whole_text = "".join(
                            run.text for run in paragraph.runs)
                        whole_text = whole_text.replace(
                            str(match), str(replacement))
                        for idx, run in enumerate(paragraph.runs):
                            if idx != 0:
                                p = paragraph._p
                                p.remove(run._r)
                        if bool(paragraph.runs):
                            paragraph.runs[0].text = whole_text

    tempArray = input_pptx.split(".pptx")
    #newPath = tempArray[0] + "today.pptx"

    prs.save(input_pptx)
    return input_pptx
def main():
    insertChange("PowerPoints/result1.pptx","have come")

if __name__ == "__main__":
    main()