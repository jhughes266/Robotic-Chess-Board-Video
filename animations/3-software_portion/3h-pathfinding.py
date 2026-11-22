from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *


class ImageTest:
    def __init__(self, sceneAnimator, topLeftX, topLeftY, imageWidth, path, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__image = NewImage(topLeft=[topLeftX, topLeftY],
                             imgPath=path,
                             imageWidth=imageWidth,
                             colour=None, drawProportion=0, maxNumBlurs=100,
                             frameWidth=videoWidth, frameHeight=videoHeight,
                             onlyKeepMonoChrome=True)

    def drawInImage(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                startDrawProportion=0, endDrawProportion=1,
                                                startTime=startTime,
                                                endTime=startTime + drawDuration,
                                                fps=self.__fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                startDrawProportion=1, endDrawProportion=1,
                                                startTime=startTime + drawDuration,
                                                endTime=startTime + drawDuration + holdDuration,
                                                fps=self.__fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        drawAnimation.addPrimitive(self.__image)
        holdAnimation.addPrimitive(self.__image)
        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)



videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 5


sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='3h-pathfinding.mp4')
image = ImageTest(sceneAnimator=sceneAnimator, topLeftX=-0.05, topLeftY=0.5,imageWidth=0.1, path='../resources/piece_images/black_king.jpg', videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)
image.drawInImage(startTime=0, drawDuration=1, holdDuration=1)



sceneAnimator.renderAnimation()
