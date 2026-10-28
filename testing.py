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

for i in range(numberOfFrames):
    frame = np.zeros((videoHeight, videoWidth, 3), np.uint8)
    testLine.draw(frame)
    testLine.drawProportion = i / numberOfFrames
    testLine.updatePosition((.00,.00))
    outputVideo.write(frame)

outputVideo.release()
print("Finished")