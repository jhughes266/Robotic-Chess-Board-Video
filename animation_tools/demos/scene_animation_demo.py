from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
videoWidth = 1280
videoHeight = 720
fps = 60
videoDuration = 10
testSceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='demo.mp4')

testLine = Line(pt1=[0.1,0.7], pt2=[0.3,0.7], colour=(0,255,0),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
testArrowedLine = ArrowedLine(pt1=[0.3,0.7], pt2=[0.1,0.5], colour=(0,255,0),thickness=5, drawProportion=0,  frameWidth=videoWidth, frameHeight=videoHeight)
testRectangle = Rectangle(pt1=[0.0,0.0], pt2=[0.3,0.3], colour=(0,255,0),thickness=5, drawProportion=0,  frameWidth=videoWidth, frameHeight=videoHeight)
testEllipse = Ellipse(center=[0.2,0.3], axes=(75,75), angle=0, startAngle=30, endAngle=390, colour=(0,0,255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
testText = Text(text="Hello World", org=[0.5,0.5], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5, frameWidth=videoWidth, frameHeight=videoHeight)
testImage = Image(topLeft=[0.5,0.5], imgPath='testImage.jpg', imageWidth=.1, colour=None, drawProportion=0, maxNumBlurs = 100, frameWidth=videoWidth, frameHeight=videoHeight)

# 1st animation: 0 - 2 seconds
testPrimitiveAnimation1 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.1,.2], startDrawProportion=0, endDrawProportion=1, startTime=0, endTime=2, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

testPrimitiveAnimation1.addPrimitive(testImage)
testPrimitiveAnimation1.addPrimitive(testLine)
testPrimitiveAnimation1.addPrimitive(testArrowedLine)
testPrimitiveAnimation1.addPrimitive(testRectangle)
testPrimitiveAnimation1.addPrimitive(testEllipse)
testPrimitiveAnimation1.addPrimitive(testText)

# 2nd animation: 2 - 3 seconds
testPrimitiveAnimation2 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.05,-.3], startDrawProportion=1, endDrawProportion=0, startTime=2, endTime=10, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
testPrimitiveAnimation2.addPrimitive(testEllipse)

# 3rd animation: 2 - 3 seconds
testPrimitiveAnimation3 = PrimitiveAnimation(startLocation=[0.3,.3], endLocation=[0.3,0.3], startDrawProportion=1, endDrawProportion=1, startTime=2, endTime=10, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
testPrimitiveAnimation3.addPrimitive(testImage)
testPrimitiveAnimation3.addPrimitive(testLine)
testPrimitiveAnimation3.addPrimitive(testArrowedLine)
testPrimitiveAnimation3.addPrimitive(testRectangle)
testPrimitiveAnimation3.addPrimitive(testText)

# add animations to scene
testSceneAnimator.addPrimitiveAnimation(testPrimitiveAnimation1)
testSceneAnimator.addPrimitiveAnimation(testPrimitiveAnimation2)
testSceneAnimator.addPrimitiveAnimation(testPrimitiveAnimation3)

# render the animation
testSceneAnimator.renderAnimation()
