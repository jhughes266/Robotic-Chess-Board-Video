from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math


class Message:
    def __init__(self, sceneAnimator, x, y, message, colour, videoWidth, videoHeight, fps, scale):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__text = Text(text=message, org=[x, y], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=scale,
                      colour=colour, drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=20,
                      frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

    def drawInText(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__text)
        holdAnimation.addPrimitive(self.__text)
        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawOutText(self, startTime, vanishDuration):
        vanishAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=0,
                                           startTime=startTime,
                                           endTime=startTime + vanishDuration,
                                           fps=self.__fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)


        vanishAnimation.addPrimitive(self.__text)
        self.__sceneAnimator.addPrimitiveAnimation(vanishAnimation)


    def move(self, startTime, duration, xDelta, yDelta):

        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        moveAnimation.addPrimitive(self.__text)

        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)


videoWidth = int(3840)
videoHeight = int(2160)
fps = 30
videoDuration = 5
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='1.mp4')

message = Message(sceneAnimator, 0.5, 0.4, 'Bringing Everything Together', (255,255,255), videoWidth, videoHeight, fps, scale=7)

message.drawInText(startTime=1, drawDuration=2, holdDuration=videoDuration)


sceneAnimator.renderAnimation()

