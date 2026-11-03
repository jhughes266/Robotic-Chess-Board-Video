from multiprocessing import connection

from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *


class TwoAxisRobotAndGripper:
    def __init__(self, sceneAnimator, videoWidth, videoHeight, videoDuration):
        self.__sceneAnimator = sceneAnimator
        railTopLegnth = 0.35
        railSideLength = videoWidth / videoHeight * railTopLegnth
        railX = (1 - railTopLegnth)/2
        railY = 0.2
        self.__videoDuration = videoDuration

        # Rails
        self.__topRail = Line(pt1=[railX, railY], pt2=[railX + railTopLegnth, railY], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)
        self.__bottomRail = Line(pt1=[railX, railY + railSideLength], pt2=[railX + railTopLegnth, railY + railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightRail = Line([railX + railTopLegnth , railY], pt2=[railX + railTopLegnth , railY + railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)
        self.__leftRail = Line(pt1=[railX, railY], pt2=[railX, railY + railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)

        # Carriage
        carriageTopLegnth = 0.05
        carriageSideLength = videoWidth / videoHeight * carriageTopLegnth
        carriageX = ((railX + railX + railTopLegnth) / 2) - (carriageTopLegnth / 2)
        carriageY = ((railY + railY + railSideLength) / 2) - (carriageSideLength / 2)
        self.__carriage = Rectangle(pt1=[carriageX, carriageY], pt2=[carriageX + carriageTopLegnth, carriageY + carriageSideLength], colour=(255, 255, 255), thickness=10, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

        # Carriage Connections
        connectionVerticalLength = railSideLength
        connectionHorizontalLength = railTopLegnth
        connectionX = railX
        connectionY = railY
        xAxisColour = (210, 210, 210)
        yAxisColour = (70, 70, 70)
        self.__verticalConnection = Line(pt1=[connectionX + connectionHorizontalLength/2, connectionY], pt2=[connectionX + connectionHorizontalLength/2, connectionY + connectionVerticalLength], colour=yAxisColour,
                              thickness=20, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)
        self.__horizontalConnection = Line(pt1=[connectionX, connectionY + connectionVerticalLength/2],
                                 pt2=[connectionX + connectionHorizontalLength, connectionY + connectionVerticalLength/2], colour=xAxisColour,
                                 thickness=20, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

        # Bearings
        horizontalBearingLength = 0.05
        horizontalBearingWidth = 0.025
        verticalBearingLength = horizontalBearingLength * (videoWidth / videoHeight)
        verticalBearingWidth = horizontalBearingWidth * (videoHeight / videoWidth)
        carriageCentreX = ((railX + railX + railTopLegnth) / 2)
        carriageCentreY = ((railY + railY + railSideLength) / 2)
        self.__topBearing = Rectangle(pt1=[carriageCentreX - horizontalBearingLength / 2, carriageCentreY - connectionVerticalLength/2 - horizontalBearingWidth/2],
                                      pt2=[carriageCentreX - horizontalBearingLength / 2 + horizontalBearingLength, carriageCentreY - connectionVerticalLength/2 - horizontalBearingWidth/2 + horizontalBearingWidth],
                                      colour=yAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)

        self.__bottomBearing = Rectangle(pt1=[carriageCentreX - horizontalBearingLength / 2, carriageCentreY + connectionVerticalLength/2 - horizontalBearingWidth/2],
                                      pt2=[carriageCentreX - horizontalBearingLength / 2 + horizontalBearingLength, carriageCentreY + connectionVerticalLength/2 - horizontalBearingWidth/2 + horizontalBearingWidth],
                                      colour=yAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)

        self.__rightBearing = Rectangle(pt1=[carriageCentreX - connectionHorizontalLength/2 - verticalBearingWidth/2, carriageCentreY - verticalBearingLength/2],
                                      pt2=[carriageCentreX - connectionHorizontalLength/2 - verticalBearingWidth/2 + verticalBearingWidth, carriageCentreY - verticalBearingLength/2 + verticalBearingLength],
                                      colour=xAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)

        self.__leftBearing = Rectangle(pt1=[carriageCentreX + connectionHorizontalLength/2 - verticalBearingWidth/2, carriageCentreY - verticalBearingLength/2],
                                      pt2=[carriageCentreX + connectionHorizontalLength/2 - verticalBearingWidth/2 + verticalBearingWidth, carriageCentreY - verticalBearingLength/2 + verticalBearingLength],
                                      colour=xAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)


    def drawInAnimation(self):
        drawTime = 2
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                             startDrawProportion=0, endDrawProportion=1, startTime=0, endTime=drawTime,
                                             fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        drawAnimation.addPrimitive(self.__topRail)
        drawAnimation.addPrimitive(self.__bottomRail)
        drawAnimation.addPrimitive(self.__rightRail)
        drawAnimation.addPrimitive(self.__leftRail)
        drawAnimation.addPrimitive(self.__verticalConnection)
        drawAnimation.addPrimitive(self.__horizontalConnection)
        drawAnimation.addPrimitive(self.__carriage)
        drawAnimation.addPrimitive(self.__topBearing)
        drawAnimation.addPrimitive(self.__bottomBearing)
        drawAnimation.addPrimitive(self.__rightBearing)
        drawAnimation.addPrimitive(self.__leftBearing)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1, startTime=drawTime, endTime=self.__videoDuration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        holdAnimation.addPrimitive(self.__topRail)
        holdAnimation.addPrimitive(self.__bottomRail)
        holdAnimation.addPrimitive(self.__rightRail)
        holdAnimation.addPrimitive(self.__leftRail)
        holdAnimation.addPrimitive(self.__verticalConnection)
        holdAnimation.addPrimitive(self.__horizontalConnection)
        holdAnimation.addPrimitive(self.__carriage)
        holdAnimation.addPrimitive(self.__topBearing)
        holdAnimation.addPrimitive(self.__bottomBearing)
        holdAnimation.addPrimitive(self.__rightBearing)
        holdAnimation.addPrimitive(self.__leftBearing)

        sceneAnimator.addPrimitiveAnimation(drawAnimation)
        sceneAnimator.addPrimitiveAnimation(holdAnimation)





videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 3
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2b-2_axis_robot_and_gripper.mp4')
twoAxisRobot = TwoAxisRobotAndGripper(sceneAnimator, videoWidth, videoHeight, videoDuration)
twoAxisRobot.drawInAnimation()
sceneAnimator.renderAnimation()



