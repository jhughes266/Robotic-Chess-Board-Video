from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math



class PanelVisuals:
    def __init__(self, sceneAnimator, imagePath, imageWidth, topLeftX, topLeftY, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__panelImage = Image(topLeft=[topLeftX, topLeftY],
                                  imgPath=imagePath,
                                  imageWidth=imageWidth,
                                  colour=None, drawProportion=0, maxNumBlurs=0,
                                  frameWidth=videoWidth, frameHeight=videoHeight,
                                   onlyKeepMonoChrome=False)

    def drawInPanelImage(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__panelImage)
        holdAnimation.addPrimitive(self.__panelImage)
        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

videoWidth = int(3840)
videoHeight = int(2160)
fps = 30
videoDuration = 5
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='21.mp4')

panelVisuals = PanelVisuals(sceneAnimator=sceneAnimator, imagePath='../resources/side_on_panel.jpg', imageWidth=0.8, topLeftX=0.1, topLeftY=0.1, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)

panelVisuals.drawInPanelImage(startTime=0, drawDuration=2, holdDuration=videoDuration)



sceneAnimator.renderAnimation()