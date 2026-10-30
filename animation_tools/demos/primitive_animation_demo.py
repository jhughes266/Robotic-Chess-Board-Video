from animation_tools.elements import *
from animation_tools.primative_animation import *
videoWidth = 1280
videoHeight = 720
fps = 30
numberOfFrames = 500
outputFile = 'test.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
outputVideo = cv2.VideoWriter(outputFile, fourcc, fps, (videoWidth, videoHeight))
sampleFrame= np.zeros((videoHeight, videoWidth, 3), np.uint8)

testLine = Line(pt1=[0.1,0.7], pt2=[0.3,0.7], colour=(0,255,0),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
testArrowedLine = ArrowedLine(pt1=[0.3,0.7], pt2=[0.1,0.5], colour=(0,255,0),thickness=5, drawProportion=0,  frameWidth=videoWidth, frameHeight=videoHeight)
testRectangle = Rectangle(pt1=[0.0,0.0], pt2=[0.3,0.3], colour=(0,255,0),thickness=5, drawProportion=0,  frameWidth=videoWidth, frameHeight=videoHeight)
testEllipse = Ellipse(center=[0.2,0.3], axes=(75,75), angle=0, startAngle=30, endAngle=390, colour=(0,0,255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
testText = Text(text="Hello World", org=[0.5,0.5], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5, frameWidth=videoWidth, frameHeight=videoHeight)
testImage = Image(topLeft=[0.5,0.5], imgPath='testImage.jpg', imageWidth=.1, colour=None, drawProportion=0, maxNumBlurs = 100, frameWidth=videoWidth, frameHeight=videoHeight)

testPrimitiveAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.3,.3], startDrawProportion=0, endDrawProportion=1, startTime=3, duration=1, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

testPrimitiveAnimation.addPrimitive(testImage)
testPrimitiveAnimation.addPrimitive(testLine)
testPrimitiveAnimation.addPrimitive(testArrowedLine)
testPrimitiveAnimation.addPrimitive(testRectangle)
testPrimitiveAnimation.addPrimitive(testEllipse)
testPrimitiveAnimation.addPrimitive(testText)

testPrimitiveAnimation2 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.05,-.3], startDrawProportion=1, endDrawProportion=0, startTime=4, duration=1, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
testPrimitiveAnimation2.addPrimitive(testEllipse)

testPrimitiveAnimation3 = PrimitiveAnimation(startLocation=[0.3,.3], endLocation=[0.3,0.3], startDrawProportion=1, endDrawProportion=0, startTime=4, duration=1, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
testPrimitiveAnimation3.addPrimitive(testImage)
testPrimitiveAnimation3.addPrimitive(testLine)
testPrimitiveAnimation3.addPrimitive(testArrowedLine)
testPrimitiveAnimation3.addPrimitive(testRectangle)
testPrimitiveAnimation3.addPrimitive(testText)




for i in range(numberOfFrames):
    frame = np.zeros((videoHeight, videoWidth, 3), np.uint8)
    testPrimitiveAnimation.draw(frame)
    testPrimitiveAnimation2.draw(frame)
    testPrimitiveAnimation3.draw(frame)




    outputVideo.write(frame)

outputVideo.release()
print("Finished")