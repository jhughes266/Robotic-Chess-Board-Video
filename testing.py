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
sampleFrame= np.zeros((videoHeight, videoWidth, 3), np.uint8)

testLine = Line(pt1=[0.1,0.7], pt2=[0.3,0.7], colour=(0,255,0),thickness=5, drawProportion=0, sampleFrame=sampleFrame)
testArrowedLine = ArrowedLine(pt1=[0.3,0.7], pt2=[0.1,0.5], colour=(0,255,0),thickness=5, drawProportion=0, sampleFrame=sampleFrame)
testRectangle = Rectangle(pt1=[0.0,0.2], pt2=[0.3,0.3], colour=(0,255,0),thickness=5, drawProportion=0.90, sampleFrame=sampleFrame)
testEllipse = Ellipse(center=[0.5,0.6], axes=(75,75), angle=0, startAngle=30, endAngle=390, colour=(0,0,255), thickness=5, drawProportion=0.30, sampleFrame=sampleFrame)
testText = Text(text="Hello World", org=[0.5,0.5], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, colour=(255,255,255), drawProportion=1, progressiveDrawMode='letterByLetter', insertCursorThickness=5, sampleFrame=sampleFrame)

testImage = Image(topLeft=[0.1,0.0], imgPath='testImage.jpg', imageWidth=.2, colour=None, drawProportion=1, maxNumBlurs = 100, sampleFrame=sampleFrame)

for i in range(numberOfFrames):
    frame = np.zeros((videoHeight, videoWidth, 3), np.uint8)

    testImage.updateDrawProportion ((2 * i + 1) / numberOfFrames)
    testImage.updatePosition((10, 0))
    testImage.draw(frame)

    testText.updateDrawProportion ((2 * i + 1) / numberOfFrames)
    testText.updatePosition((1, -1))
    testText.draw(frame)


    testLine.updateDrawProportion ((2 * i + 1) / numberOfFrames)
    testLine.updatePosition((1,-1))
    testLine.draw(frame)

    testArrowedLine.updateDrawProportion ((2 * i + 1) / numberOfFrames)
    testArrowedLine.updatePosition((1, 0))
    testArrowedLine.draw(frame)

    testRectangle.updateDrawProportion ((2 * i + 1) / numberOfFrames)
    testRectangle.updatePosition((1, 0))
    testRectangle.draw(frame)

    testEllipse.updateDrawProportion ((2 * i + 1) / numberOfFrames)
    testEllipse.updatePosition((1, 0))
    testEllipse.draw(frame)



    outputVideo.write(frame)

outputVideo.release()
print("Finished")