import collections
import collections.abc

from pptx.dml.color import RGBColor
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN


def makePPT(result_path, indexes):
    #readings = getReadingsDictionary(year, month, day)

    prs = Presentation(result_path)
    slide = prs.slides[0]
    currentIndex = 0

    
    text = "HI"
    verticalPostion = .48 

    blessed = slide.shapes.add_textbox(
        Inches(.48), Inches(verticalPostion), Inches(2.57), Inches(.54))
    tf = blessed.text_frame

    p = tf.paragraphs[0]
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.word_wrap = True
    blessed.fill.solid()
    blessed.fill.fore_color.rgb = RGBColor(255, 255, 255)
    click_action = blessed.click_action
    click_action.target_slide = prs.slides[1]
    click_action.action
    line = blessed.line
    line.color.rgb = RGBColor(79, 129, 189)
    line.width = Pt(2)

    run = p.add_run()

    run.text = text
    font = run.font
    font.name = 'Calibri'
    font.size = Pt(24)
    prs.save(result_path)

    #import os
    #os.startfile("communion2.pptx")

makePPT()