from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 5


sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2a-board_layout.mp4')

line = Line(pt1=[0.1, 0.8], pt2=[0.8, 0.8], colour=(0, 255, 0), thickness=5000, drawProportion=1, frameWidth=videoWidth, frameHeight=videoHeight)
image = Image(topLeft=[0.5, 0.5], imgPath='../resources/piece_images/black_king.jpg', imageWidth=.1, colour=None, drawProportion=0, maxNumBlurs = 100, frameWidth=videoWidth, frameHeight=videoHeight, onlyKeepMonoChrome=True)

imageDraw = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.1, .2], startDrawProportion=0, endDrawProportion=1, startTime=0, endTime=2, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDraw = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, .0], startDrawProportion=1, endDrawProportion=1, startTime=0, endTime=2, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)


lineDraw.addPrimitive(line)
imageDraw.addPrimitive(image)



imageHold = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=2, endTime=10, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHold = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=2, endTime=10, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)


lineHold.addPrimitive(line)
sceneAnimator.addPrimitiveAnimation(lineDraw)
sceneAnimator.addPrimitiveAnimation(lineHold)
imageHold.addPrimitive(image)
sceneAnimator.addPrimitiveAnimation(imageDraw)
sceneAnimator.addPrimitiveAnimation(imageHold)

# render the animation
sceneAnimator.renderAnimation()

