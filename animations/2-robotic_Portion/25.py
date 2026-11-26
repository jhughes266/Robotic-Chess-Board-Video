from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math

class HolderVisuals:
    def __init__(self, sceneAnimator, imagePath, imageWidth, topLeftX, topLeftY, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__holderImage = Image(topLeft=[topLeftX, topLeftY],
                                   imgPath=imagePath,
                                   imageWidth=imageWidth,
                                   colour=None, drawProportion=0, maxNumBlurs=0,
                                   frameWidth=videoWidth, frameHeight=videoHeight,
                                   onlyKeepMonoChrome=False)

        self.__ledText = Text(text='Infrared LED Holder', org=[0.15, 0.25], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2,
                      colour=(0,0,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=20,
                      frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        self.__ledLine = Line(
                pt1=[0.23, 0.25],
                pt2=[0.49, 0.3],
                colour=(0,0,255), thickness=10, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight)

        self.__phototransistorText = Text(text='Phototransistor Holder', org=[0.85, 0.25], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2,
                              colour=(0, 0, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                              insertCursorThickness=20,
                              frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        self.__phototransistorLine = Line(
                pt1=[0.76, 0.25],
                pt2=[0.54, 0.3],
                colour=(0,0,255), thickness=10, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight)

    def drawInHolderImage(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__holderImage)
        holdAnimation.addPrimitive(self.__holderImage)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInHolderText(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__ledText)

        drawAnimation.addPrimitive(self.__phototransistorText)

        holdAnimation.addPrimitive(self.__ledText)

        holdAnimation.addPrimitive(self.__phototransistorText)



        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInHolderLine(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__ledLine)

        drawAnimation.addPrimitive(self.__phototransistorLine)

        holdAnimation.addPrimitive(self.__ledLine)

        holdAnimation.addPrimitive(self.__phototransistorLine)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)








videoWidth = int(3840)
videoHeight = int(2160)
fps = 30
videoDuration = 8
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='25.mp4')

holderVisuals = HolderVisuals(sceneAnimator=sceneAnimator, imagePath='../resources/LED_Phototransistor_Holders.jpg', imageWidth=0.5, topLeftX=0.25, topLeftY=0.1, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)

holderVisuals.drawInHolderImage(startTime=0, drawDuration=2, holdDuration=videoDuration)
holderVisuals.drawInHolderText(startTime=2, drawDuration=2, holdDuration=videoDuration)
holderVisuals.drawInHolderLine(startTime=4, drawDuration=2, holdDuration=videoDuration)




sceneAnimator.renderAnimation()