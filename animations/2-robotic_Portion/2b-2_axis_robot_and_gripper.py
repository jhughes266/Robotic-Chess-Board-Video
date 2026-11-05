from multiprocessing import connection

from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *


class TwoAxisRobotAndGripper:
    def __init__(self, sceneAnimator, videoWidth, videoHeight, videoDuration):
        self.__sceneAnimator = sceneAnimator
        self.__railTopLength = 0.35
        self.__railSideLength = videoWidth / videoHeight * self.__railTopLength
        self.__railX = (1 - self.__railTopLength) / 2
        self.__railY = 0.2
        self.__videoDuration = videoDuration
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__gripperEngaged = False
        # Rails
        self.__topRail = Line(pt1=[self.__railX, self.__railY], pt2=[self.__railX + self.__railTopLength, self.__railY], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)
        self.__bottomRail = Line(pt1=[self.__railX, self.__railY + self.__railSideLength], pt2=[self.__railX + self.__railTopLength, self.__railY + self.__railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightRail = Line([self.__railX + self.__railTopLength , self.__railY], pt2=[self.__railX + self.__railTopLength , self.__railY + self.__railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                                frameWidth=videoWidth, frameHeight=videoHeight)
        self.__leftRail = Line(pt1=[self.__railX, self.__railY], pt2=[self.__railX, self.__railY + self.__railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)

        # Carriage
        carriageTopLegnth = 0.05
        carriageSideLength = videoWidth / videoHeight * carriageTopLegnth
        carriageX = ((self.__railX + self.__railX + self.__railTopLength) / 2) - (carriageTopLegnth / 2)
        carriageY = ((self.__railY + self.__railY + self.__railSideLength) / 2) - (carriageSideLength / 2)
        self.__carriage = Rectangle(pt1=[carriageX, carriageY], pt2=[carriageX + carriageTopLegnth, carriageY + carriageSideLength], colour=(255, 255, 255), thickness=10, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

        # Carriage Connections
        connectionVerticalLength = self.__railSideLength
        connectionHorizontalLength = self.__railTopLength
        connectionX = self.__railX
        connectionY = self.__railY
        xAxisColour = (190, 190, 190)
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
        self.__carriageCentreX = ((self.__railX + self.__railX + self.__railTopLength) / 2)
        self.__carriageCentreY = ((self.__railY + self.__railY + self.__railSideLength) / 2)
        self.__topBearing = Rectangle(pt1=[self.__carriageCentreX - horizontalBearingLength / 2, self.__carriageCentreY - connectionVerticalLength/2 - horizontalBearingWidth/2],
                                      pt2=[self.__carriageCentreX - horizontalBearingLength / 2 + horizontalBearingLength, self.__carriageCentreY - connectionVerticalLength/2 - horizontalBearingWidth/2 + horizontalBearingWidth],
                                      colour=yAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)

        self.__bottomBearing = Rectangle(pt1=[self.__carriageCentreX - horizontalBearingLength / 2, self.__carriageCentreY + connectionVerticalLength/2 - horizontalBearingWidth/2],
                                      pt2=[self.__carriageCentreX - horizontalBearingLength / 2 + horizontalBearingLength, self.__carriageCentreY + connectionVerticalLength/2 - horizontalBearingWidth/2 + horizontalBearingWidth],
                                      colour=yAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)

        self.__rightBearing = Rectangle(pt1=[self.__carriageCentreX - connectionHorizontalLength/2 - verticalBearingWidth/2, self.__carriageCentreY - verticalBearingLength/2],
                                      pt2=[self.__carriageCentreX - connectionHorizontalLength/2 - verticalBearingWidth/2 + verticalBearingWidth, self.__carriageCentreY - verticalBearingLength/2 + verticalBearingLength],
                                      colour=xAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)

        self.__leftBearing = Rectangle(pt1=[self.__carriageCentreX + connectionHorizontalLength/2 - verticalBearingWidth/2, self.__carriageCentreY - verticalBearingLength/2],
                                      pt2=[self.__carriageCentreX + connectionHorizontalLength/2 - verticalBearingWidth/2 + verticalBearingWidth, self.__carriageCentreY - verticalBearingLength/2 + verticalBearingLength],
                                      colour=xAxisColour, thickness=60, drawProportion=0, frameWidth=videoWidth,frameHeight=videoHeight)
        # Gripper
        self.__carriageCentreX = ((self.__railX + self.__railX + self.__railTopLength) / 2)
        self.__carriageCentreY = ((self.__railY + self.__railY + self.__railSideLength) / 2)

        xDistanceToGripperTopLeft = 0.0125
        yDistanceToGripperTopLeft = xDistanceToGripperTopLeft * (videoWidth / videoHeight)

        gripperXPaddelLength = 0.01
        gripperYPaddelLength = gripperXPaddelLength * (videoWidth / videoHeight)

        gripperTopLeftX = self.__carriageCentreX - xDistanceToGripperTopLeft
        gripperTopLeftY = self.__carriageCentreY - yDistanceToGripperTopLeft

        topRightGripperColour = (0,0,255)
        bottomLeftGripperColour = (0,255,0)

        self.__topRightHorizontalGripperPadel = Line(pt1=[gripperTopLeftX + 2 * xDistanceToGripperTopLeft, gripperTopLeftY],
                                                    pt2=[gripperTopLeftX + 2 * xDistanceToGripperTopLeft - gripperXPaddelLength, gripperTopLeftY],
                                                    colour=topRightGripperColour,
                                                    thickness=20, drawProportion=0, frameWidth=videoWidth,
                                                    frameHeight=videoHeight)

        self.__topRightVerticalGripperPadel = Line(pt1=[gripperTopLeftX + 2 * xDistanceToGripperTopLeft, gripperTopLeftY],
                                                    pt2=[gripperTopLeftX + 2 * xDistanceToGripperTopLeft, gripperTopLeftY + gripperYPaddelLength],
                                                    colour=topRightGripperColour,
                                                    thickness=20, drawProportion=0, frameWidth=videoWidth,
                                                    frameHeight=videoHeight)

        self.__bottomLeftHorizontalGripperPadel = Line(pt1=[gripperTopLeftX, gripperTopLeftY + 2 * yDistanceToGripperTopLeft],
                                                    pt2=[gripperTopLeftX + gripperXPaddelLength, gripperTopLeftY + 2 * yDistanceToGripperTopLeft],
                                                    colour=bottomLeftGripperColour,
                                                    thickness=20, drawProportion=0, frameWidth=videoWidth,
                                                    frameHeight=videoHeight)

        self.__bottomLeftVerticalGripperPadel = Line(pt1=[gripperTopLeftX, gripperTopLeftY + 2 * yDistanceToGripperTopLeft],
                                                    pt2=[gripperTopLeftX, gripperTopLeftY + 2 * yDistanceToGripperTopLeft - gripperYPaddelLength],
                                                    colour=bottomLeftGripperColour,
                                                    thickness=20, drawProportion=0, frameWidth=videoWidth,
                                                    frameHeight=videoHeight)

        #Establishing groupings for movement of the robot
        self.__xMovementGroup = []
        self.__xMovementGroup.append(self.__verticalConnection)
        self.__xMovementGroup.append(self.__bottomBearing)
        self.__xMovementGroup.append(self.__topBearing)
        self.__yMovementGroup = []
        self.__yMovementGroup.append(self.__horizontalConnection)
        self.__yMovementGroup.append(self.__rightBearing)
        self.__yMovementGroup.append(self.__leftBearing)
        self.__xyMovementGroup = []
        self.__xyMovementGroup.append(self.__carriage)
        self.__xyMovementGroup.append(self.__topRightVerticalGripperPadel)
        self.__xyMovementGroup.append(self.__topRightHorizontalGripperPadel)
        self.__xyMovementGroup.append(self.__bottomLeftVerticalGripperPadel)
        self.__xyMovementGroup.append(self.__bottomLeftHorizontalGripperPadel)
        # Grouping for all elements to allow animations to be performed on all elements
        self.__allGroup = []
        self.__allGroup.append(self.__topRail)
        self.__allGroup.append(self.__bottomRail)
        self.__allGroup.append(self.__rightRail)
        self.__allGroup.append(self.__leftRail)
        self.__allGroup.append(self.__carriage)
        self.__allGroup.append(self.__verticalConnection)
        self.__allGroup.append(self.__horizontalConnection)
        self.__allGroup.append(self.__topBearing)
        self.__allGroup.append(self.__bottomBearing)
        self.__allGroup.append(self.__rightBearing)
        self.__allGroup.append(self.__leftBearing)
        self.__allGroup.append(self.__topRightVerticalGripperPadel)
        self.__allGroup.append(self.__topRightHorizontalGripperPadel)
        self.__allGroup.append(self.__bottomLeftVerticalGripperPadel)
        self.__allGroup.append(self.__bottomLeftHorizontalGripperPadel)

        # Chess board
        proportionOfRail = 0.8
        chessBoardTopLeftX = self.__railX + (1 - proportionOfRail)/2 * self.__railTopLength
        chessBoardTopLeftY = self.__railY + (1 - proportionOfRail)/2 * self.__railSideLength
        sqaureWidth = (proportionOfRail * self.__railTopLength)/12
        squareHeight = (proportionOfRail * self.__railSideLength)/12
        squareWidthOffset = sqaureWidth * 0.03
        squareHeightOffset = squareHeight * 0.03
        self.__chessFadeRectangles = []

        graveYardDarkColour = (0, 0, 255)
        graveYardLightColour = (0, 0, 125)
        graveYardColourFlag = False
        bufferDarkColour = (125, 125, 125)
        bufferLightColour = (192, 192, 192)
        bufferColourFlag = False
        chessBoardDarkColour = (21,67,120)
        chessBoardLightColour = (89,155,240)
        chessBoardColourFlag = False
        colour = None
        for i in range(12):
            for j in range(12):
                # colour selection
                squareNumber = i * 12 + j
                if (i == 0) or (i == 11) or (j == 0) or (j == 11):
                    if graveYardColourFlag:
                        colour = graveYardDarkColour
                    else:
                        colour = graveYardLightColour
                elif (i > 1) and (i < 10) and (j > 1) and (j < 10):
                    if chessBoardColourFlag:
                        colour = chessBoardDarkColour
                    else:
                        colour = chessBoardLightColour
                else:
                    if bufferColourFlag:
                        colour = bufferDarkColour
                    else:
                        colour = bufferLightColour

                self.__chessFadeRectangles.append(FadeRectangle(
                    pt1=[chessBoardTopLeftX + i * sqaureWidth + squareWidthOffset, chessBoardTopLeftY + j * squareHeight + squareHeightOffset],
                    pt2=[chessBoardTopLeftX + (i + 1) * sqaureWidth - squareWidthOffset, chessBoardTopLeftY + (j + 1) * squareHeight - squareHeightOffset],
                    colour=colour, frameWidth=videoWidth,
                                          frameHeight=videoHeight, thickness=5, lineType=cv2.LINE_8, drawProportion=1))

                graveYardColourFlag = not graveYardColourFlag
                bufferColourFlag = not bufferColourFlag
                chessBoardColourFlag = not chessBoardColourFlag

            graveYardColourFlag = not graveYardColourFlag
            bufferColourFlag = not bufferColourFlag
            chessBoardColourFlag = not chessBoardColourFlag

        for fadeRectangle in self.__chessFadeRectangles:
            self.__allGroup.append(fadeRectangle)


    def drawInAnimation(self, startTime, drawInDuration):

        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                             startDrawProportion=0, endDrawProportion=1, startTime=0, endTime=startTime + drawInDuration,
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
        drawAnimation.addPrimitive(self.__bottomLeftHorizontalGripperPadel)
        drawAnimation.addPrimitive(self.__bottomLeftVerticalGripperPadel)
        drawAnimation.addPrimitive(self.__topRightHorizontalGripperPadel)
        drawAnimation.addPrimitive(self.__topRightVerticalGripperPadel)


        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1, startTime=startTime + drawInDuration, endTime=self.__videoDuration,
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
        holdAnimation.addPrimitive(self.__bottomLeftHorizontalGripperPadel)
        holdAnimation.addPrimitive(self.__bottomLeftVerticalGripperPadel)
        holdAnimation.addPrimitive(self.__topRightHorizontalGripperPadel)
        holdAnimation.addPrimitive(self.__topRightVerticalGripperPadel)


        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInChessBoard(self, startTime, boardDrawDuration, boardHoldDuration, boardSeeThroughDuration, boardSeeThroughHoldDuration):

        rectangleDrawTime = boardDrawDuration / (len(self.__chessFadeRectangles) + 1)
        rectangleVanishTime = boardSeeThroughDuration / (len(self.__chessFadeRectangles) + 1)
        for i, fadeRectangle in enumerate(self.__chessFadeRectangles):

            boardConstruction = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                           startDrawProportion=1,
                                           endDrawProportion=1,
                                           startTime=startTime + i * rectangleDrawTime,
                                           endTime=startTime + (i + 1) * rectangleDrawTime,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)
            boardConstruction.addPrimitive(fadeRectangle)
            self.__sceneAnimator.addPrimitiveAnimation(boardConstruction)

            boardHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                                 startDrawProportion=1, endDrawProportion=1,
                                                 startTime=startTime + (i + 1) * rectangleDrawTime,
                                                 endTime=startTime + boardDrawDuration + boardHoldDuration,
                                                 fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)
            boardHold.addPrimitive(fadeRectangle)
            self.__sceneAnimator.addPrimitiveAnimation(boardHold)

            boardSeeThroughStartTime = startTime + boardDrawDuration + boardHoldDuration
            boardSeeThroughEndTime = max(boardSeeThroughStartTime + .2, boardSeeThroughStartTime + (i + 1) * rectangleVanishTime)

            seeThroughBoard = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                           startDrawProportion=1, endDrawProportion=0.5,
                                           startTime=boardSeeThroughStartTime,
                                           endTime=boardSeeThroughEndTime,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)
            seeThroughBoard.addPrimitive(fadeRectangle)
            self.__sceneAnimator.addPrimitiveAnimation(seeThroughBoard)

            seeThroughBoardHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                                 startDrawProportion=0.5, endDrawProportion=0.5,
                                                 startTime=boardSeeThroughEndTime,
                                                 endTime=boardSeeThroughStartTime + boardHoldDuration + boardSeeThroughHoldDuration,
                                                 fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)
            seeThroughBoardHold.addPrimitive(fadeRectangle)
            self.__sceneAnimator.addPrimitiveAnimation(seeThroughBoardHold)





    def moveGantry(self, startTime, duration, xGantry, yGantry):
        x = (xGantry / 120) * self.__railTopLength + self.__railX
        y = (yGantry / 120) * self.__railSideLength + self.__railY

        xDelta = x - self.__carriageCentreX
        yDelta = y - self.__carriageCentreY
        self.__carriageCentreX += xDelta
        self.__carriageCentreY += yDelta

        # x movement
        xAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, 0.0],
                           startDrawProportion=1, endDrawProportion=1, startTime=startTime, endTime=startTime + duration,
                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        for primitive in self.__xMovementGroup:
            xAnimation.addPrimitive(primitive)
        self.__sceneAnimator.addPrimitiveAnimation(xAnimation)

        # y movement
        yAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, yDelta],
                           startDrawProportion=1, endDrawProportion=1, startTime=startTime,
                           endTime=startTime + duration,
                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        for primitive in self.__yMovementGroup:
            yAnimation.addPrimitive(primitive)
        self.__sceneAnimator.addPrimitiveAnimation(yAnimation)

        # xy movement
        xyAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                           startDrawProportion=1, endDrawProportion=1, startTime=startTime,
                           endTime=startTime + duration,
                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        for primitive in self.__xyMovementGroup:
            xyAnimation.addPrimitive(primitive)
        self.__sceneAnimator.addPrimitiveAnimation(xyAnimation)


    def toggleGripper(self, startTime, duration):
        gripperXDelta = 0.005
        gripperYDelta = gripperXDelta * (self.__videoWidth / self.__videoHeight)
        topRightAnimation = None
        bottomLeftAnimation = None
        if not self.__gripperEngaged:
            topRightAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[-gripperXDelta, gripperYDelta],
                               startDrawProportion=1, endDrawProportion=1,
                               startTime=startTime,
                               endTime=startTime + duration,
                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            bottomLeftAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[gripperXDelta, -gripperYDelta],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                   startTime=startTime,
                                                   endTime=startTime + duration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        elif self.__gripperEngaged:
            topRightAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0],
                                                   endLocation=[gripperXDelta, -gripperYDelta],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                   startTime=startTime,
                                                   endTime=startTime + duration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            bottomLeftAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0],
                                                     endLocation=[-gripperXDelta, +gripperYDelta],
                                                     startDrawProportion=1, endDrawProportion=1,
                                                     startTime=startTime,
                                                     endTime=startTime + duration,
                                                     fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        topRightAnimation.addPrimitive(self.__topRightVerticalGripperPadel)
        topRightAnimation.addPrimitive(self.__topRightHorizontalGripperPadel)
        bottomLeftAnimation.addPrimitive(self.__bottomLeftVerticalGripperPadel)
        bottomLeftAnimation.addPrimitive(self.__bottomLeftHorizontalGripperPadel)

        self.__sceneAnimator.addPrimitiveAnimation(topRightAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(bottomLeftAnimation)

        self.__gripperEngaged = not self.__gripperEngaged

    def moveEntireRobot(self, startTime,  duration, xDelta, yDelta,):


        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                        startDrawProportion=1, endDrawProportion=1,
                                        startTime=startTime,
                                        endTime=startTime + duration,
                                        fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        for primitive in self.__allGroup:
            moveAnimation.addPrimitive(primitive)
        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)



videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 20
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2b-2_axis_robot_and_gripper.mp4')

twoAxisRobot = TwoAxisRobotAndGripper(sceneAnimator, videoWidth, videoHeight, videoDuration)
twoAxisRobot.drawInAnimation(startTime=0, drawInDuration=2)
twoAxisRobot.moveGantry(startTime=2, duration=2, xGantry=20, yGantry=30)
twoAxisRobot.toggleGripper(startTime=3, duration=1)
twoAxisRobot.moveGantry(startTime=4,duration=2,xGantry=60, yGantry=80)
twoAxisRobot.toggleGripper(startTime=9, duration=1)
twoAxisRobot.moveGantry(startTime=12,duration=2,xGantry=60, yGantry=60)
twoAxisRobot.drawInChessBoard(startTime=6, boardDrawDuration=2, boardHoldDuration=2, boardSeeThroughDuration=1, boardSeeThroughHoldDuration=10)
twoAxisRobot.moveEntireRobot(startTime=14, duration=2, xDelta=-0.25, yDelta=0.0)






sceneAnimator.renderAnimation()



