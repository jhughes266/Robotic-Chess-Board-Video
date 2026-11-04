from multiprocessing import connection

from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *


class TwoAxisRobotAndGripper:
    def __init__(self, sceneAnimator, videoWidth, videoHeight, videoDuration):
        self.__sceneAnimator = sceneAnimator
        self.__railTopLegnth = 0.35
        self.__railSideLength = videoWidth / videoHeight * self.__railTopLegnth
        self.__railX = (1 - self.__railTopLegnth)/2
        self.__railY = 0.2
        self.__videoDuration = videoDuration
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        # Keeps track of the time elapsed in the animation
        self.__currentAnimationTime = 0
        self.__gripperEngaged = False
        # Rails
        self.__topRail = Line(pt1=[self.__railX, self.__railY], pt2=[self.__railX + self.__railTopLegnth, self.__railY], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)
        self.__bottomRail = Line(pt1=[self.__railX, self.__railY + self.__railSideLength], pt2=[self.__railX + self.__railTopLegnth, self.__railY + self.__railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightRail = Line([self.__railX + self.__railTopLegnth , self.__railY], pt2=[self.__railX + self.__railTopLegnth , self.__railY + self.__railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)
        self.__leftRail = Line(pt1=[self.__railX, self.__railY], pt2=[self.__railX, self.__railY + self.__railSideLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                              frameWidth=videoWidth, frameHeight=videoHeight)

        # Carriage
        carriageTopLegnth = 0.05
        carriageSideLength = videoWidth / videoHeight * carriageTopLegnth
        carriageX = ((self.__railX + self.__railX + self.__railTopLegnth) / 2) - (carriageTopLegnth / 2)
        carriageY = ((self.__railY + self.__railY + self.__railSideLength) / 2) - (carriageSideLength / 2)
        self.__carriage = Rectangle(pt1=[carriageX, carriageY], pt2=[carriageX + carriageTopLegnth, carriageY + carriageSideLength], colour=(255, 255, 255), thickness=10, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

        # Carriage Connections
        connectionVerticalLength = self.__railSideLength
        connectionHorizontalLength = self.__railTopLegnth
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
        self.__carriageCentreX = ((self.__railX + self.__railX + self.__railTopLegnth) / 2)
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
        self.__carriageCentreX = ((self.__railX + self.__railX + self.__railTopLegnth) / 2)
        self.__carriageCentreY = ((self.__railY + self.__railY + self.__railSideLength) / 2)

        xDistanceToGripperTopLeft = 0.0125
        yDistanceToGripperTopLeft = xDistanceToGripperTopLeft * (videoWidth / videoHeight)

        gripperXPaddelLength = 0.03
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

    def drawInAnimation(self):
        drawInTime = 2
        self.__currentAnimationTime += drawInTime
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                             startDrawProportion=0, endDrawProportion=1, startTime=0, endTime=drawInTime,
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
                                           startDrawProportion=1, endDrawProportion=1, startTime=drawInTime, endTime=self.__videoDuration,
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


        sceneAnimator.addPrimitiveAnimation(drawAnimation)
        sceneAnimator.addPrimitiveAnimation(holdAnimation)
    
    def moveGantry(self, xGantry, yGantry, duration):
        x = (xGantry / 120) * self.__railTopLegnth + self.__railX
        y = (yGantry / 120) * self.__railSideLength + self.__railY

        xDelta = x - self.__carriageCentreX
        yDelta = y - self.__carriageCentreY
        self.__carriageCentreX += xDelta
        self.__carriageCentreY += yDelta

        # x movement
        xAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, 0.0],
                           startDrawProportion=1, endDrawProportion=1, startTime=self.__currentAnimationTime, endTime=self.__currentAnimationTime + duration,
                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        for primitive in self.__xMovementGroup:
            xAnimation.addPrimitive(primitive)
        sceneAnimator.addPrimitiveAnimation(xAnimation)

        # y movement
        yAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, yDelta],
                           startDrawProportion=1, endDrawProportion=1, startTime=self.__currentAnimationTime,
                           endTime=self.__currentAnimationTime + duration,
                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        for primitive in self.__yMovementGroup:
            yAnimation.addPrimitive(primitive)
        sceneAnimator.addPrimitiveAnimation(yAnimation)

        # xy movement
        xyAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                           startDrawProportion=1, endDrawProportion=1, startTime=self.__currentAnimationTime,
                           endTime=self.__currentAnimationTime + duration,
                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        for primitive in self.__xyMovementGroup:
            xyAnimation.addPrimitive(primitive)
        sceneAnimator.addPrimitiveAnimation(xyAnimation)

        self.__currentAnimationTime += duration

    def toggleGripper(self, duration):
        gripperXDelta = 0.01
        gripperYDelta = gripperXDelta * (self.__videoWidth / self.__videoHeight)
        topRightAnimation = None
        bottomLeftAnimation = None
        if not self.__gripperEngaged:
            topRightAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[-gripperXDelta, gripperYDelta],
                               startDrawProportion=1, endDrawProportion=1,
                               startTime=self.__currentAnimationTime,
                               endTime=self.__currentAnimationTime + duration,
                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            bottomLeftAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[gripperXDelta, -gripperYDelta],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                   startTime=self.__currentAnimationTime,
                                                   endTime=self.__currentAnimationTime + duration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        elif self.__gripperEngaged:
            topRightAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0],
                                                   endLocation=[gripperXDelta, -gripperYDelta],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                   startTime=self.__currentAnimationTime,
                                                   endTime=self.__currentAnimationTime + duration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            bottomLeftAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0],
                                                     endLocation=[-gripperXDelta, +gripperYDelta],
                                                     startDrawProportion=1, endDrawProportion=1,
                                                     startTime=self.__currentAnimationTime,
                                                     endTime=self.__currentAnimationTime + duration,
                                                     fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        topRightAnimation.addPrimitive(self.__topRightVerticalGripperPadel)
        topRightAnimation.addPrimitive(self.__topRightHorizontalGripperPadel)
        bottomLeftAnimation.addPrimitive(self.__bottomLeftVerticalGripperPadel)
        bottomLeftAnimation.addPrimitive(self.__bottomLeftHorizontalGripperPadel)

        sceneAnimator.addPrimitiveAnimation(topRightAnimation)
        sceneAnimator.addPrimitiveAnimation(bottomLeftAnimation)

        self.__gripperEngaged = not self.__gripperEngaged
        self.__currentAnimationTime += duration

    def moveEntireRobot(self, xDelta, yDelta, duration):


        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                        startDrawProportion=1, endDrawProportion=1,
                                        startTime=self.__currentAnimationTime,
                                        endTime=self.__currentAnimationTime + duration,
                                        fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        for primitive in self.__allGroup:
            moveAnimation.addPrimitive(primitive)
        sceneAnimator.addPrimitiveAnimation(moveAnimation)

        self.__currentAnimationTime += duration


videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2b-2_axis_robot_and_gripper.mp4')
twoAxisRobot = TwoAxisRobotAndGripper(sceneAnimator, videoWidth, videoHeight, videoDuration)
twoAxisRobot.drawInAnimation()
twoAxisRobot.moveGantry(0, 0, 1)
twoAxisRobot.moveEntireRobot(0.2,0.2,1)
twoAxisRobot.toggleGripper(duration=1)
twoAxisRobot.moveGantry(60, 80, 1)
twoAxisRobot.toggleGripper(duration=1)
twoAxisRobot.moveGantry(60, 60, 1)
twoAxisRobot.moveEntireRobot(-0.2,-0.1,1)
twoAxisRobot.moveEntireRobot(0,-0.1,1)


testFadeRectangle = FadeRectangle(pt1 = [0.0, 0.0], pt2=[0.1, 0.1], colour=(0,0,255), frameWidth=videoWidth, frameHeight=videoHeight, thickness=10, lineType=cv2.LINE_8, drawProportion=1)
fadeRectangleAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                        startDrawProportion=1, endDrawProportion=0,
                                        startTime=0,
                                        endTime=4,
                                        fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
fadeRectangleAnimation.addPrimitive(testFadeRectangle)
sceneAnimator.addPrimitiveAnimation(fadeRectangleAnimation)


sceneAnimator.renderAnimation()



