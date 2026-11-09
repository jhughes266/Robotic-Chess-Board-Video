from multiprocessing import connection
import math
import numpy as np

from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *


class TwoAxisRobotAndGripper:
    def __init__(self, sceneAnimator, videoWidth, videoHeight, videoDuration, fps, moveablePieceName):

        self.__sceneAnimator = sceneAnimator
        self.__railTopLength = 0.35
        self.__railSideLength = videoWidth / videoHeight * self.__railTopLength
        self.__railX = (1 - self.__railTopLength) / 2 - 0.2
        self.__railY = 0.1
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
        self.__proportionOfRail = proportionOfRail
        chessBoardTopLeftX = self.__railX + (1 - proportionOfRail)/2 * self.__railTopLength
        chessBoardTopLeftY = self.__railY + (1 - proportionOfRail)/2 * self.__railSideLength
        sqaureWidth = (proportionOfRail * self.__railTopLength)/12
        squareHeight = (proportionOfRail * self.__railSideLength)/12

        self.__squareWidth = sqaureWidth
        self.__squareHeight = squareHeight

        squareWidthOffset = sqaureWidth * 0.03
        squareHeightOffset = squareHeight * 0.03
        self.__chessFadeRectangles = []

        self.__moveablePieceImageWidth = sqaureWidth
        squareToPiecePath = {
            26: "black_rook",
            27: "black_pawn",
            32: "white_pawn",
            33: "white_rook",

            38: "black_knight",
            39: "black_pawn",
            44: "white_pawn",
            45: "white_knight",

            50: "black_bishop",
            51: "black_pawn",
            56: "white_pawn",
            57: "white_bishop",

            62: "black_queen",
            63: "black_pawn",
            68: "white_pawn",
            69: "white_queen",

            74: "black_king",
            75: "black_pawn",
            80: "white_pawn",
            81: "white_king",

            86: "black_bishop",
            87: "black_pawn",
            92: "white_pawn",
            93: "white_bishop",

            98: "black_knight",
            99: "black_pawn",
            104: "white_pawn",
            105: "white_knight",

            110: "black_rook",
            111: "black_pawn",
            116: "white_pawn",
            117: "white_rook"
        }

        self.__pieces = []

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
        self.__moveablePieceImage = None
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
                currentPiecePath = None
                if squareNumber in squareToPiecePath:
                    piecePath = squareToPiecePath[squareNumber]
                    path = '../resources/piece_images/' + piecePath + '.jpg'
                    currentPiecePath = path
                    self.__pieces.append(Image(topLeft=[chessBoardTopLeftX + i * sqaureWidth, chessBoardTopLeftY + j * squareHeight], imgPath=path,
                                  imageWidth=sqaureWidth, colour=None, drawProportion=0, maxNumBlurs=100,
                                  frameWidth=videoWidth, frameHeight=videoHeight, onlyKeepMonoChrome=True))

                # Create moveable piece
                moveablePiecePath = '../resources/piece_images/' + moveablePieceName + '.jpg'
                if moveablePiecePath == currentPiecePath and self.__moveablePieceImage is None:
                    self.__moveablePieceImage = Image(topLeft=[chessBoardTopLeftX + i * sqaureWidth, chessBoardTopLeftY + j * squareHeight], imgPath=moveablePiecePath,
                                                      imageWidth=self.__moveablePieceImageWidth, colour=None,
                                                      drawProportion=0,
                                                      maxNumBlurs=100,
                                                      frameWidth=videoWidth, frameHeight=videoHeight,
                                                      onlyKeepMonoChrome=True)
                    self.__allGroup.append(self.__moveablePieceImage)

                graveYardColourFlag = not graveYardColourFlag
                bufferColourFlag = not bufferColourFlag
                chessBoardColourFlag = not chessBoardColourFlag

            graveYardColourFlag = not graveYardColourFlag
            bufferColourFlag = not bufferColourFlag
            chessBoardColourFlag = not chessBoardColourFlag

        for fadeRectangle in self.__chessFadeRectangles:
            self.__allGroup.append(fadeRectangle)

        for image in self.__pieces:
            self.__allGroup.append(image)

    def moveMoveablePiece(self, startTime, duration, xSqaureDelta, ySqaureDelta):
        pieceMove = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xSqaureDelta * self.__squareWidth, ySqaureDelta * self.__squareHeight],
                                             startDrawProportion=1, endDrawProportion=1, startTime=startTime, endTime=startTime + duration,
                                             fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        pieceMove.addPrimitive(self.__moveablePieceImage)
        self.__sceneAnimator.addPrimitiveAnimation(pieceMove)

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
        pieceVanishTime = None
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
            pieceVanishTime = boardSeeThroughEndTime
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

        pieceDraw = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                       startDrawProportion=0,
                                       endDrawProportion=1,
                                       startTime=startTime + boardDrawDuration,
                                       endTime=startTime + boardDrawDuration + boardHoldDuration / 2,
                                       fps=fps, frameWidth=self.__videoWidth,
                                       frameHeight=self.__videoHeight)

        pieceHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                       startDrawProportion=1,
                                       endDrawProportion=1,
                                       startTime=startTime + boardDrawDuration + boardHoldDuration / 2,
                                       endTime=startTime + boardDrawDuration + boardHoldDuration ,
                                       fps=fps, frameWidth=self.__videoWidth,
                                       frameHeight=self.__videoHeight)
        pieceVanish = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                       startDrawProportion=1,
                                       endDrawProportion=0,
                                       startTime=startTime + boardDrawDuration + boardHoldDuration,
                                       endTime=startTime + boardDrawDuration + boardHoldDuration + 0.1,
                                       fps=fps, frameWidth=self.__videoWidth,
                                       frameHeight=self.__videoHeight)
        for piece in self.__pieces:
            pieceDraw.addPrimitive(piece)
            pieceHold.addPrimitive(piece)
            pieceVanish.addPrimitive(piece)
        self.__sceneAnimator.addPrimitiveAnimation(pieceDraw)
        self.__sceneAnimator.addPrimitiveAnimation(pieceHold)
        self.__sceneAnimator.addPrimitiveAnimation(pieceVanish)

    def moveGantry(self, startTime, duration, xGantry=None, yGantry=None, xSquare=None, ySquare=None, xSquareOffset=0, ySquareOffset=0):
        x = None
        y = None
        if xGantry is not None:
            x = (xGantry / 120) * self.__railTopLength + self.__railX
            y = (yGantry / 120) * self.__railSideLength + self.__railY
        elif xSquare is not None:
            chessBoardTopLeftX = self.__railX + (1 - self.__proportionOfRail) / 2 * self.__railTopLength
            chessBoardTopLeftY = self.__railY + (1 - self.__proportionOfRail) / 2 * self.__railSideLength
            x = chessBoardTopLeftX + xSquare * self.__squareWidth + self.__squareWidth /2 + xSquareOffset
            y = chessBoardTopLeftY + ySquare * self.__squareHeight + self.__squareHeight /2 + ySquareOffset


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

    def drawInMoveablePiece(self, startTime, duration):


        pieceDraw = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                       startDrawProportion=0,
                                       endDrawProportion=1,
                                       startTime=startTime,
                                       endTime=startTime + duration,
                                       fps=fps, frameWidth=self.__videoWidth,
                                       frameHeight=self.__videoHeight)

        pieceDraw.addPrimitive(self.__moveablePieceImage)
        self.__sceneAnimator.addPrimitiveAnimation(pieceDraw)

class SideOnGripper:
    def __init__(self, sceneAnimator, xTopLeft, yTopLeft, scale, videoWidth, videoHeight, pieceName):
        self.__sceneAnimator = sceneAnimator
        clawLegnth = 0.025 * scale
        clawHeightDiff = 0.01 * scale
        clawSupportLength = 0.075 * scale
        clawSupportBaseLength = clawLegnth * 2
        raiserLength = 0.1 * scale
        xBaseLength = 0.025 * scale
        yBaseLength = 0.05 * scale
        xClawSupportToRaiser = 0.005 * scale
        yClawSupportToBase = xClawSupportToRaiser * videoWidth / videoHeight


        chessBoardLength = clawSupportBaseLength * 4

        self.__clawSupportLength = clawSupportLength
        self.__raiserLength = raiserLength
        self.__gripperEngaged = False

        self.__verticalY = self.__clawSupportLength * 0.3
        self.__clawX = self.__raiserLength * 0.1
        chessBoardVerticalOffset = 0.01

        imageWidth = 0.8 * clawSupportBaseLength
        # Assumes square image
        imageHeight = imageWidth * (videoWidth / videoHeight)

        self.__leftClaw = Line(pt1=[xTopLeft, yTopLeft],
                               pt2=[xTopLeft + clawLegnth, yTopLeft],
                               colour=(0, 255, 0), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightClaw = Line(pt1=[xTopLeft + clawSupportBaseLength, yTopLeft - clawHeightDiff],
                               pt2=[xTopLeft + clawSupportBaseLength - clawLegnth, yTopLeft - clawHeightDiff],
                               colour=(0, 0, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__leftClawSupport = Line(pt1=[xTopLeft, yTopLeft],
                               pt2=[xTopLeft, yTopLeft + clawSupportLength],
                               colour=(0, 255, 0), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightClawSupport = Line(pt1=[xTopLeft + clawSupportBaseLength, yTopLeft  - clawHeightDiff],
                               pt2=[xTopLeft + clawSupportBaseLength, yTopLeft + clawSupportLength],
                               colour=(0, 0, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__clawSupportBase = Line(pt1=[xTopLeft, yTopLeft + clawSupportLength],
                               pt2=[xTopLeft + clawSupportBaseLength, yTopLeft + clawSupportLength],
                               colour=(255, 255, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__raiser = Line(pt1=[xTopLeft + clawSupportBaseLength/2, yTopLeft + clawSupportLength],
                               pt2=[xTopLeft + clawSupportBaseLength/2, yTopLeft + clawSupportLength + raiserLength],
                               colour=(255, 255, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__leftBaseHorizontal = Line(pt1=[xTopLeft + clawSupportBaseLength/2 - xClawSupportToRaiser, yTopLeft + clawSupportLength + yClawSupportToBase],
                               pt2=[xTopLeft + clawSupportBaseLength/2 - xClawSupportToRaiser - xBaseLength, yTopLeft + clawSupportLength + yClawSupportToBase],
                               colour=(255, 255, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightBaseHorizontal = Line(pt1=[xTopLeft + clawSupportBaseLength/2 + xClawSupportToRaiser, yTopLeft + clawSupportLength + yClawSupportToBase],
                               pt2=[xTopLeft + clawSupportBaseLength/2 + xClawSupportToRaiser + xBaseLength, yTopLeft + clawSupportLength + yClawSupportToBase],
                               colour=(255, 255, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__leftBaseVertical = Line(pt1=[xTopLeft + clawSupportBaseLength/2 - xClawSupportToRaiser, yTopLeft + clawSupportLength + yClawSupportToBase],
                               pt2=[xTopLeft + clawSupportBaseLength/2 - xClawSupportToRaiser, yTopLeft + clawSupportLength + yClawSupportToBase + yBaseLength],
                               colour=(255, 255, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        self.__rightBaseVertical = Line(pt1=[xTopLeft + clawSupportBaseLength/2 + xClawSupportToRaiser, yTopLeft + clawSupportLength + yClawSupportToBase],
                               pt2=[xTopLeft + clawSupportBaseLength/2 + xClawSupportToRaiser, yTopLeft + clawSupportLength + yClawSupportToBase + yBaseLength],
                               colour=(255, 255, 255), thickness=5, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)


        self.__allGripperGroup = [self.__leftClaw, self.__rightClaw, self.__leftClawSupport, self.__rightClawSupport, self.__clawSupportBase, self.__raiser, self.__leftBaseHorizontal, self.__rightBaseHorizontal, self.__leftBaseVertical, self.__rightBaseVertical]

        self.__verticalGroup = [self.__leftClaw, self.__rightClaw, self.__leftClawSupport, self.__rightClawSupport, self.__clawSupportBase, self.__raiser]
        self.__leftClawGroup = [self.__leftClaw, self.__leftClawSupport]
        self.__rightClawGroup = [self.__rightClaw, self.__rightClawSupport]
        # Chess board
        self.__chessBoard = Line(pt1=[xTopLeft, yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset],
                               pt2=[xTopLeft + chessBoardLength, yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset],
                               colour=(255, 255, 255), thickness=15, drawProportion=0,frameWidth=videoWidth, frameHeight=videoHeight)
        # Chess piece
        path = '../resources/piece_images/' + pieceName + '.jpg'
        chessPieceHeightOffset = imageHeight * 0.1
        chessPieceX = xTopLeft + clawSupportBaseLength / 2 - imageWidth /2 + 0.05
        self.__chessPiece = Image(topLeft=[chessPieceX, yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset - imageHeight + chessPieceHeightOffset],
                                  imgPath=path,
                                  imageWidth=imageWidth, colour=None, drawProportion=0, maxNumBlurs=100,
                                  frameWidth=videoWidth, frameHeight=videoHeight, onlyKeepMonoChrome=True)

        magnetWidth = imageWidth * 0.2
        magentHeight = imageHeight * 0.2
        self.__topMagnet = Rectangle(pt1=[chessPieceX + imageWidth / 2 - magnetWidth / 2, yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset - magentHeight],
                                     pt2=[chessPieceX + imageWidth / 2 - magnetWidth / 2 + magnetWidth, yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset],
                                     colour=(95, 95, 95), thickness=-40, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

        self.__bottomMagnet = Rectangle(pt1=[chessPieceX + imageWidth / 2 - magnetWidth / 2,yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset],
                                         pt2=[chessPieceX + imageWidth / 2 - magnetWidth / 2 + magnetWidth, yTopLeft - self.__verticalY - clawHeightDiff - chessBoardVerticalOffset + magentHeight],
                                     colour=(95, 95, 95), thickness=-40, drawProportion=0, frameWidth=videoWidth,
                                     frameHeight=videoHeight)

        self.__chessPieceGroup = [self.__chessPiece, self.__topMagnet, self.__bottomMagnet]

    def drawInAnimation(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        drawAnimation.addPrimitive(self.__leftClaw)
        drawAnimation.addPrimitive(self.__rightClaw)
        drawAnimation.addPrimitive(self.__leftClawSupport)
        drawAnimation.addPrimitive(self.__rightClawSupport)
        drawAnimation.addPrimitive(self.__clawSupportBase)
        drawAnimation.addPrimitive(self.__raiser)
        drawAnimation.addPrimitive(self.__leftBaseHorizontal)
        drawAnimation.addPrimitive(self.__rightBaseHorizontal)
        drawAnimation.addPrimitive(self.__leftBaseVertical)
        drawAnimation.addPrimitive(self.__rightBaseVertical)
        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        holdAnimation.addPrimitive(self.__leftClaw)
        holdAnimation.addPrimitive(self.__rightClaw)
        holdAnimation.addPrimitive(self.__leftClawSupport)
        holdAnimation.addPrimitive(self.__rightClawSupport)
        holdAnimation.addPrimitive(self.__clawSupportBase)
        holdAnimation.addPrimitive(self.__raiser)
        holdAnimation.addPrimitive(self.__leftBaseHorizontal)
        holdAnimation.addPrimitive(self.__rightBaseHorizontal)
        holdAnimation.addPrimitive(self.__leftBaseVertical)
        holdAnimation.addPrimitive(self.__rightBaseVertical)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def toggle(self, startTime, verticalDuration, clawCloseDuration, holdDuration):

        if self.__gripperEngaged:
            nonClawHoldHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                 startDrawProportion=1, endDrawProportion=1,
                                                 startTime=startTime,
                                                 endTime=startTime + clawCloseDuration,
                                                 fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
            for primitive in self.__allGripperGroup:
                if (primitive not in self.__leftClawGroup):
                    if (primitive not in self.__rightClawGroup):
                        nonClawHoldHold.addPrimitive(primitive)

            rightClawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[self.__clawX, 0.0],
                                                    startDrawProportion=1, endDrawProportion=1,
                                                    startTime=startTime,
                                                    endTime=startTime + clawCloseDuration,
                                                    fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__rightClawGroup:
                rightClawAnimation.addPrimitive(primitive)

            leftClawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[-self.__clawX, 0.0],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                   startTime=startTime,
                                                   endTime=startTime + clawCloseDuration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__leftClawGroup:
                leftClawAnimation.addPrimitive(primitive)

            nonVerticalHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                 startDrawProportion=1, endDrawProportion=1,
                                                 startTime=startTime + clawCloseDuration,
                                                 endTime=startTime + clawCloseDuration+ verticalDuration,
                                                 fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__allGripperGroup:
                if primitive not in self.__verticalGroup:
                    nonVerticalHold.addPrimitive(primitive)

            verticalAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, self.__verticalY],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                   startTime=startTime + clawCloseDuration,
                                                   endTime=startTime + clawCloseDuration + verticalDuration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
            for primitive in self.__verticalGroup:
                verticalAnimation.addPrimitive(primitive)

            holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                               startDrawProportion=1, endDrawProportion=1,
                                               startTime = startTime + clawCloseDuration + verticalDuration,
                                               endTime= startTime + clawCloseDuration + verticalDuration + holdDuration,
                                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__allGripperGroup:
                holdAnimation.addPrimitive(primitive)

        else:
            nonVerticalHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                 startDrawProportion=1, endDrawProportion=1,
                                                 startTime=startTime,
                                                 endTime=startTime + verticalDuration,
                                                 fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__allGripperGroup:
                if primitive not in self.__verticalGroup:
                    nonVerticalHold.addPrimitive(primitive)

            verticalAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, -self.__verticalY],
                                               startDrawProportion=1, endDrawProportion=1,
                                               startTime=startTime,
                                               endTime=startTime + verticalDuration,
                                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
            for primitive in self.__verticalGroup:
                verticalAnimation.addPrimitive(primitive)

            nonClawHoldHold = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                 startDrawProportion=1, endDrawProportion=1,
                                                 startTime=startTime + verticalDuration,
                                                 endTime=startTime + verticalDuration + clawCloseDuration,
                                                 fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
            for primitive in self.__allGripperGroup:
                if (primitive not in self.__leftClawGroup):
                    if (primitive not in self.__rightClawGroup):
                        nonClawHoldHold.addPrimitive(primitive)


            leftClawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[self.__clawX, 0.0],
                                               startDrawProportion=1, endDrawProportion=1,
                                               startTime=startTime + verticalDuration,
                                               endTime=startTime + verticalDuration + clawCloseDuration,
                                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__leftClawGroup:
                leftClawAnimation.addPrimitive(primitive)

            rightClawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[-self.__clawX, 0.0],
                                                   startDrawProportion=1, endDrawProportion=1,
                                                    startTime=startTime + verticalDuration,
                                                    endTime=startTime + verticalDuration + clawCloseDuration,
                                                   fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__rightClawGroup:
                rightClawAnimation.addPrimitive(primitive)

            holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                               startDrawProportion=1, endDrawProportion=1,
                                               startTime=startTime + verticalDuration + clawCloseDuration,
                                               endTime=startTime + verticalDuration + clawCloseDuration + holdDuration,
                                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

            for primitive in self.__allGripperGroup:
                holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(nonVerticalHold)
        self.__sceneAnimator.addPrimitiveAnimation(verticalAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(nonClawHoldHold)
        self.__sceneAnimator.addPrimitiveAnimation(leftClawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(rightClawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

        self.__gripperEngaged = not self.__gripperEngaged

    def drawInPiece(self, startTime, drawDuration, holdDuration):
        drawChessPiece = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        holdChessPiece = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        drawChessPiece.addPrimitive(self.__chessPiece)
        drawChessPiece.addPrimitive(self.__topMagnet)
        drawChessPiece.addPrimitive(self.__bottomMagnet)
        holdChessPiece.addPrimitive(self.__chessPiece)
        holdChessPiece.addPrimitive(self.__topMagnet)
        holdChessPiece.addPrimitive(self.__bottomMagnet)
        self.__sceneAnimator.addPrimitiveAnimation(drawChessPiece)
        self.__sceneAnimator.addPrimitiveAnimation(holdChessPiece)


    def drawChessBoard(self, startTime, drawDuration, holdDuration):
        drawChessBoardAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                     startDrawProportion=1, endDrawProportion=1,
                                                     startTime=startTime + drawDuration,
                                                     endTime=startTime + drawDuration + holdDuration,
                                                     fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        drawChessBoardAnimation.addPrimitive(self.__chessBoard)
        holdAnimation.addPrimitive(self.__chessBoard)
        self.__sceneAnimator.addPrimitiveAnimation(drawChessBoardAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def moveGripper(self, startTime, xDelta, moveDuration, holdDuration):
        moveGripperAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, 0.0],
                                                     startDrawProportion=1, endDrawProportion=1,
                                                     startTime=startTime ,
                                                     endTime=startTime + moveDuration ,
                                                     fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        holdGripperAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                     startDrawProportion=1, endDrawProportion=1,
                                                     startTime=startTime + moveDuration,
                                                     endTime=startTime + moveDuration + holdDuration,
                                                     fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        for primitive in self.__allGripperGroup:
            moveGripperAnimation.addPrimitive(primitive)
            holdGripperAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(moveGripperAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdGripperAnimation)

    def movePiece(self, startTime, xDelta, moveDuration, holdDuration):
        movePieceAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, 0.0],
                                                  startDrawProportion=1, endDrawProportion=1,
                                                  startTime=startTime,
                                                  endTime=startTime + moveDuration,
                                                  fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        holdPieceAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                  startDrawProportion=1, endDrawProportion=1,
                                                  startTime=startTime + moveDuration,
                                                  endTime=startTime + moveDuration + holdDuration,
                                                  fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        for primitive in self.__chessPieceGroup:
            movePieceAnimation.addPrimitive(primitive)
            holdPieceAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(movePieceAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdPieceAnimation)

class Message:
    def __init__(self, sceneAnimator, x, y, message, videoWidth, videoHeight, fps, colour = (255,255,255), fontScale=2.7):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__text = Text(text=message, org=[x, y], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=fontScale,
                      colour=colour, drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5,
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

class NumberedAxes:
    def __init__(self, sceneAnimator, topLeftX, topLeftY, videoWidth, videoHeight, fps):

        self.__railTopLength = 0.35
        self.__railSideLength = videoWidth / videoHeight * self.__railTopLength
        self.__railX = (1 - self.__railTopLength) / 2 - 0.2

        self.__sceneAnimator = sceneAnimator
        self.__xAxisLength = 0.35
        self.__yAxisLength = videoWidth / videoHeight * self.__xAxisLength
        self.__topLeftX = topLeftX
        self.__topLeftY = topLeftY

        xDistanceFromAxisToRail = self.__railX - self.__topLeftX
        yDistanceFromAxisToRail = xDistanceFromAxisToRail * (videoWidth / videoHeight)
        self.__videoDuration = videoDuration
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps

        self.__yAxis = Line(pt1=[self.__topLeftX, self.__topLeftY], pt2=[self.__topLeftX, self.__topLeftY + self.__yAxisLength], colour=(255, 255, 255), thickness=5, drawProportion=0,
                            frameWidth=videoWidth, frameHeight=videoHeight)

        self.__xAxis = Line(pt1=[self.__topLeftX + xDistanceFromAxisToRail, self.__topLeftY + self.__yAxisLength + yDistanceFromAxisToRail],
                            pt2=[self.__topLeftX + self.__xAxisLength + xDistanceFromAxisToRail, self.__topLeftY + self.__yAxisLength + yDistanceFromAxisToRail], colour=(255, 255, 255),
                            thickness=5, drawProportion=0,
                            frameWidth=videoWidth, frameHeight=videoHeight)

        # y Axis markings
        self.__yAxisMarkingLinesAndText = []
        numberOfMarkings = 121
        # -1 because 0 is included
        ySpacing = self.__yAxisLength / (numberOfMarkings - 1)
        for i in range(numberOfMarkings):
            yAxisMarkingLength = .01
            thickness = 1

            if i % 20 == 0:
                yAxisMarkingLength = .02
                thickness = 5
                number = abs(i - (numberOfMarkings - 1))
                self.__yAxisMarkingLinesAndText.append(
                    Text(text=f"{number}", org=[self.__topLeftX - 0.025, self.__topLeftY + i * ySpacing],
                         fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.5,
                         colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                         insertCursorThickness=5,
                         frameWidth=self.__videoWidth, frameHeight=self.__videoHeight))
            elif i % 10 == 0:
                yAxisMarkingLength = .015
                thickness = 5

            self.__yAxisMarkingLinesAndText.append(Line(pt1=[self.__topLeftX, self.__topLeftY + i * ySpacing],
                                                        pt2=[self.__topLeftX + yAxisMarkingLength, self.__topLeftY + i * ySpacing],
                                                        colour=(255, 255, 255), thickness=thickness, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))



        # x Axis markings
        self.__xAxisMarkingLinesAndText = []
        numberOfMarkings = 121
        # -1 because 0 is included
        xSpacing = self.__xAxisLength / (numberOfMarkings - 1)
        for i in range(numberOfMarkings):
            xAxisMarkingLength = .01 * videoWidth / videoHeight
            thickness = 1


            if i % 20 == 0:
                xAxisMarkingLength = .02 * videoWidth / videoHeight
                thickness = 5
                number = abs(i - (numberOfMarkings - 1))
                self.__xAxisMarkingLinesAndText.append(Text(text=f"{number}",
                                                            org=[self.__topLeftX + self.__xAxisLength + xDistanceFromAxisToRail - i * xSpacing, self.__topLeftY + self.__yAxisLength + yDistanceFromAxisToRail + 0.025],
                         fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.5,
                         colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                         insertCursorThickness=5,
                         frameWidth=self.__videoWidth, frameHeight=self.__videoHeight))
            elif i % 10 == 0:
                xAxisMarkingLength = .015 * videoWidth / videoHeight
                thickness = 5

            self.__yAxisMarkingLinesAndText.append(Line(pt1=[self.__topLeftX + self.__xAxisLength + xDistanceFromAxisToRail - i * xSpacing, self.__topLeftY + self.__yAxisLength + yDistanceFromAxisToRail],
                                                        pt2=[self.__topLeftX + self.__xAxisLength + xDistanceFromAxisToRail - i * xSpacing, self.__topLeftY + self.__yAxisLength + yDistanceFromAxisToRail - xAxisMarkingLength],
                                                        colour=(255, 255, 255), thickness=thickness, drawProportion=0,
                                                        frameWidth=videoWidth, frameHeight=videoHeight))

    def drawInAxes(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__yAxis)
        drawAnimation.addPrimitive(self.__xAxis)
        holdAnimation.addPrimitive(self.__yAxis)
        holdAnimation.addPrimitive(self.__xAxis)


        for primitive in self.__yAxisMarkingLinesAndText:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        for primitive in self.__xAxisMarkingLinesAndText:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)


        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

class Arrow:
    def __init__(self, sceneAnimator, x1, y1, x2, y2, colour, thickness, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__arrowedLine = ArrowedLine(pt1=[x1,y1],
             pt2=[x2, y2],
             colour=colour, thickness=thickness, drawProportion=0, frameWidth=videoWidth,
             frameHeight=videoHeight)

    def drawInArrow(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__arrowedLine)
        holdAnimation.addPrimitive(self.__arrowedLine)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)



def graduallCarriageSlowDown(twoAxisRobot, startTime, duration, startX, endX, startY, endY, deltaT = 0.01):

    # Minus a tiny amount to make sure that it gets to the location.
    endTime = duration - 0.1
    deltaX = startX - endX
    deltaY = startY - endY
    # making sure that the robot moves at the same velocity in both axes
    # delta Y is smaller than delta X. This means delta X will be moving faster so we proportionally decrease deltaYs endTime
    # to make sure it moves at the same speed we do the opposite when the situation is reversed
    if abs(deltaX) > abs(deltaY):
        endTimeX = endTime
        endTimeY = endTime * abs(deltaY) / abs(deltaX)
    elif abs(deltaY) > abs(deltaX):
        endTimeX = endTime * abs(deltaX) / abs(deltaY)
        endTimeY = endTime
    else:
        endTimeX = endTime
        endTimeY = endTime

    if deltaX != 0:
        vx = math.log((deltaX) / np.sign(deltaX)) / endTimeX
        tShiftX = -1 * math.log(deltaX / np.sign(deltaX)) * (1 / vx)

    if deltaY != 0:
        vy = math.log((deltaY) / np.sign(deltaY)) / endTimeY
        tShiftY = -1 * math.log(deltaY / np.sign(deltaY)) * (1 / vy)

    # Split up into time steps
    for i in range(int(duration / deltaT)):
        tCur = i * deltaT
        tEnd = tCur + deltaT

        if deltaX != 0 and tCur <= endTimeX:
            xGantry = int(np.sign(deltaX) * np.exp(-vx*(tCur + tShiftX)) + endX)
        else:
            xGantry = endX

        if deltaY != 0 and tCur <= endTimeY:
            yGantry = int(np.sign(deltaY) * np.exp(-vy*(tCur + tShiftY)) + endY)
        else:
            yGantry = endY

        print(f"t:{startTime + tCur}, x:{xGantry}, y:{yGantry}")
        twoAxisRobot.moveGantry(startTime=startTime + tCur, duration=startTime + tEnd, xGantry=xGantry, yGantry=yGantry)












videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 20
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2f-PID_explanation_iii.mp4')

twoAxisRobot = TwoAxisRobotAndGripper(sceneAnimator, videoWidth, videoHeight, videoDuration, fps, moveablePieceName='white_rook')
axes = NumberedAxes(sceneAnimator=sceneAnimator, topLeftX=0.07, topLeftY=0.1, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)



finalMessage = Message(sceneAnimator=sceneAnimator, x=0.75, y=.55, message='Carriage is at goal!', videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)






twoAxisRobot.drawInAnimation(startTime=0, drawInDuration=1)
axes.drawInAxes(startTime=0, drawDuration=1, holdDuration=videoDuration)

twoAxisRobot.moveGantry(startTime=1, duration=1, xGantry=100, yGantry=60)

twoAxisRobot.moveGantry(startTime=2, duration=2, xGantry=60, yGantry=60)

twoAxisRobot.moveGantry(startTime=4, duration=2, xGantry=37, yGantry=60)

twoAxisRobot.moveGantry(startTime=6, duration=2, xGantry=24, yGantry=60)

twoAxisRobot.moveGantry(startTime=8, duration=2, xGantry=20, yGantry=60)

finalMessage.drawInText(startTime=10, drawDuration=1, holdDuration=3)



# Axes



sceneAnimator.renderAnimation()



