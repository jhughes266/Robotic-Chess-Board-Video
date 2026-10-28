import cv2
import numpy as np
from animation_tools.elements import *
videoWidth = 1280
videoHeight = 720
fps = 30
numberOfFrames = 100
outputFile = 'test.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
outputVideo = cv2.VideoWriter(outputFile, fourcc, fps, (videoWidth, videoHeight))


testLine = Line(pt1=[0.1,0.7], pt2=[0.3,0.7], colour=(0,255,0),thickness=5, drawProportion=0)
testArrowedLine = ArrowedLine(pt1=[0.3,0.7], pt2=[0.1,0.5], colour=(0,255,0),thickness=5, drawProportion=0)
testRectangle = Rectangle(pt1=[0.0,0.2], pt2=[0.3,0.3], colour=(0,255,0),thickness=5, drawProportion=0.90)
testEllipse = Ellipse(center=[0.5,0.6], axes=(75,75), angle=0, startAngle=30, endAngle=390, colour=(0,0,255), thickness=5, drawProportion=0.30)
testText = Text(text="Hello World", org=[0.5,0.5], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, colour=(0,0,255), drawProportion=1)

for i in range(numberOfFrames):
    frame = np.zeros((videoHeight, videoWidth, 3), np.uint8)


    testLine.drawProportion = (i + 1) / numberOfFrames
    testLine.updatePosition((.00,.00))
    testLine.draw(frame)

    testArrowedLine.drawProportion = (i + 1) / numberOfFrames
    testArrowedLine.updatePosition((.001, .00))
    testArrowedLine.draw(frame)

    testRectangle.drawProportion = (i + 1) / numberOfFrames
    testRectangle.updatePosition((.01, .00))
    testRectangle.draw(frame)

    testEllipse.drawProportion = (i + 1) / numberOfFrames
    testEllipse.updatePosition((.001, .00))
    testEllipse.draw(frame)

    testText.drawProportion = (i + 1) / numberOfFrames
    testText.updatePosition((.00, .00))
    testText.draw(frame)

    outputVideo.write(frame)

outputVideo.release()
print("Finished")