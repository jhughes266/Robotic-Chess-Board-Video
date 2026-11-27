from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math


class BranchInfo:
    def __init__(self, branchText, branchLineType, textPositionProportion):
        self.branchText = branchText
        self.branchLineType = branchLineType
        self.textPositionProportion = textPositionProportion

class SmallDemoBoard:
    def __init__(self, sceneAnimator, x, y, squareWidth, pieceLayout, text, branchInfoList,
                 horizontalSpacingBetweenLines, verticalSpacingBetweenBoards, squareCoordinateTextScale, mainTextScale,
                 videoWidth, videoHeight, xPerimeterSpacingFromTop, traceBackLineColour=(0, 255, 0), dashedBranch=False, dashedBranchLengthProportion=1, dashedBranchTextProportion=1, firtColour=(255,255,255), secondColour=(0,255,0), thirdColour=(0,0,255), boardCrossThickness=20, dashedLineText=''):
        self.__sceneAnimator = sceneAnimator
        self.__x = x
        self.__y = y
        self.__squareWidth = squareWidth
        self.__squareHeight = squareWidth * videoWidth / videoHeight
        self.__text = text
        self.__branchInfoList = branchInfoList
        self.__squareCoordinateTextScale = squareCoordinateTextScale
        self.__mainTextScale = mainTextScale
        self.__mainTextScale = mainTextScale
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__traceBackLineColour = traceBackLineColour
        self.__xPerimeterSpacingFromTop = xPerimeterSpacingFromTop
        self.__dashedBranch = dashedBranch
        self.__dashedBranchLengthProportion = dashedBranchLengthProportion
        self.__dashedBranchTextProportion = dashedBranchTextProportion


        boardTopLeftX = x - 1.5 * self.__squareWidth
        boardTopLeftY = y - 1.5 * self.__squareHeight

        # Colour changing outline and black background
        self.__colourChangingOutlinePrimitives = []
        self.__flashingSelectionPrimitives = []
        xSpacingFromTopLeft = self.__xPerimeterSpacingFromTop
        ySpacingFromTopLeft = xSpacingFromTopLeft * self.__videoWidth / self.__videoHeight
        outlineTopLeftX = boardTopLeftX - xSpacingFromTopLeft
        outlineTopLeftY = boardTopLeftY - ySpacingFromTopLeft
        outlineBottomRightX = boardTopLeftX + 3 * self.__squareWidth + xSpacingFromTopLeft
        outlineBottomRightY = boardTopLeftY + 3 * self.__squareHeight + ySpacingFromTopLeft


        self.__colourChangingOutlinePrimitives.append(ColourChangeRectangle(pt1=[outlineTopLeftX, outlineTopLeftY],
                                                                            pt2=[outlineBottomRightX,
                                                                                 outlineBottomRightY],
                                                                            drawProportion=0,
                                                                            firstColour=firtColour,
                                                                            secondColour=secondColour,
                                                                            thirdColour=thirdColour,
                                                                            frameWidth=videoWidth,
                                                                            frameHeight=videoHeight, thickness=5))

        self.__flashingSelectionPrimitives.append(ColourChangeRectangle(pt1=[outlineTopLeftX, outlineTopLeftY],
                                                                        pt2=[outlineBottomRightX,
                                                                                 outlineBottomRightY],
                                                                        drawProportion=0,
                                                                        firstColour=(0,0,255),
                                                                        secondColour=(0,0,255),
                                                                        thirdColour=(0,0,255),
                                                                        frameWidth=videoWidth,
                                                                        frameHeight=videoHeight, thickness=20))

        # Cross Out
        self.__boardCrossOutPrimitives = []
        self.__boardCrossOutPrimitives.append(Line(pt1=[outlineTopLeftX, outlineTopLeftY],
                                                   pt2=[outlineBottomRightX, outlineBottomRightY],
                                                   colour=(0, 0, 255),
                                                   thickness=boardCrossThickness,
                                                   drawProportion=0,
                                                   frameWidth=videoWidth,
                                                   frameHeight=videoHeight))

        self.__boardCrossOutPrimitives.append(Line(pt1=[outlineTopLeftX, outlineBottomRightY],
                                                   pt2=[outlineBottomRightX, outlineTopLeftY],
                                                   colour=(0, 0, 255),
                                                   thickness=boardCrossThickness,
                                                   drawProportion=0,
                                                   frameWidth=videoWidth,
                                                   frameHeight=videoHeight))


        # Grid squares
        self.__gridSquaresPrimitives = []
        chessBoardDarkColour = (21, 67, 120)
        chessBoardLightColour = (89, 155, 240)
        squareIsDarkColour = True
        squareColour = None

        for i in range(3):
            for j in range(3):
                squareTopLeftX = boardTopLeftX + self.__squareWidth * i
                squareTopLeftY = boardTopLeftY + self.__squareHeight * j

                if squareIsDarkColour == True:
                    squareColour = chessBoardDarkColour
                else:
                    squareColour = chessBoardLightColour

                self.__gridSquaresPrimitives.append(FadeRectangle(pt1=[squareTopLeftX, squareTopLeftY],
                                                                  pt2=[squareTopLeftX + self.__squareWidth,
                                                                       squareTopLeftY + self.__squareHeight],
                                                                  colour=squareColour, frameWidth=videoWidth,
                                                                  frameHeight=videoHeight, thickness=1,
                                                                  lineType=cv2.LINE_8, drawProportion=0))

                squareIsDarkColour = not squareIsDarkColour


        # square coordinate text
        columnNames = ['a', 'b', 'c']
        rowNames = ['3', '2', '1']
        columnY = y + 1.5 * self.__squareHeight + ySpacingFromTopLeft / 2
        for i, columnName in enumerate(columnNames):
            columnX = x - self.__squareWidth + i * self.__squareWidth
            self.__gridSquaresPrimitives.append(
                Text(text=columnName, org=[columnX, columnY], fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                     fontScale=self.__squareCoordinateTextScale,
                     colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=True))

        columnX = x - 1.5 * self.__squareWidth - xSpacingFromTopLeft / 2
        for i, rowName in enumerate(rowNames):
            columnY = y - self.__squareHeight + i * self.__squareHeight
            self.__gridSquaresPrimitives.append(
                Text(text=rowName, org=[columnX, columnY], fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                     fontScale=self.__squareCoordinateTextScale,
                     colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=False))

        # main text
        mainTextX = x
        mainTextY = y - 1.5 * self.__squareHeight - ySpacingFromTopLeft / 2

        # We need two copies of the main text
        self.__mainText = Text(text=self.__text, org=[mainTextX, mainTextY], fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                               fontScale=self.__mainTextScale,
                               colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                               insertCursorThickness=5,
                               frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=False)

        self.__moveableMainText = Text(text=self.__text, org=[mainTextX, mainTextY], fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                                       fontScale=self.__mainTextScale,
                                       colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                                       insertCursorThickness=5,
                                       frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=False)

        # Pieces
        self.__piecesPrimitivesLayout = [[None, None, None], [None, None, None], [None, None, None]]
        for rowIdx, row in enumerate(pieceLayout):
            for colIdx, piece in enumerate(row):
                pieceName = pieceLayout[rowIdx][colIdx]
                if pieceName is None:
                    continue

                pieceTopLeftX = boardTopLeftX + self.__squareWidth * colIdx
                pieceTopLeftY = boardTopLeftY + self.__squareHeight * rowIdx
                path = '../resources/piece_images/' + pieceName + '.jpg'
                cv2.imread(path)
                self.__piecesPrimitivesLayout[rowIdx][colIdx] = (NewImage(topLeft=[pieceTopLeftX, pieceTopLeftY],
                                                                       imgPath=path,
                                                                       imageWidth=self.__squareWidth,
                                                                       colour=None, drawProportion=0, maxNumBlurs=100,
                                                                       frameWidth=videoWidth, frameHeight=videoHeight,
                                                                       onlyKeepMonoChrome=True))

        # Branches and branch text
        self.__branchesPrimitives = []
        self.__traceBackPrimitives = []
        branchIntersectionX = self.__x
        branchIntersectionY = self.__y + 1.5 * self.__squareHeight

        branchYdestination = branchIntersectionY + verticalSpacingBetweenBoards

        if len(branchInfoList) % 2 == 0:
            startXdestination = branchIntersectionX - horizontalSpacingBetweenLines / 2 - (
                        (len(branchInfoList) / 2) - 1) * horizontalSpacingBetweenLines
        else:
            startXdestination = branchIntersectionX - math.floor(
                len(branchInfoList) / 2) * horizontalSpacingBetweenLines


        if self.__dashedBranch:
            branchXdestinationPrior = startXdestination + (len(self.__branchInfoList) - 1) * horizontalSpacingBetweenLines
            branchXdestination = startXdestination + (len(self.__branchInfoList) + 3) * horizontalSpacingBetweenLines

            aDash = ySpacingFromTopLeft

            o = branchXdestinationPrior - branchIntersectionX
            a = branchYdestination - branchIntersectionY

            branchXOrigin = branchIntersectionX + aDash * (o / a)
            branchYOrigin = branchIntersectionY + ySpacingFromTopLeft
            self.__branchesPrimitives.append(DashedLine(
                pt1=[branchXOrigin, branchYOrigin],
                pt2=[branchXOrigin + (branchXdestination - branchXOrigin) *  self.__dashedBranchLengthProportion, branchYOrigin + (branchYdestination - branchYOrigin) *  self.__dashedBranchLengthProportion],
                colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight))


            effectiveProportion = self.__dashedBranchTextProportion * self.__dashedBranchLengthProportion

            textX = branchXOrigin + (branchXdestination - branchXOrigin) * effectiveProportion
            textY = branchYOrigin + (branchYdestination - branchYOrigin) * effectiveProportion
            if dashedLineText != '':
                self.__branchesPrimitives.append(
                    Text(text=dashedLineText, org=[textX, textY], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.5,
                         colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                         insertCursorThickness=5,
                         frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=True))


        for i, branchInfo in enumerate(self.__branchInfoList):
            branchXdestination = startXdestination + i * horizontalSpacingBetweenLines

            aDash = ySpacingFromTopLeft

            o = branchXdestination - branchIntersectionX
            a = branchYdestination - branchIntersectionY

            branchXOrigin = branchIntersectionX + aDash * (o / a)
            branchYOrigin = branchIntersectionY + ySpacingFromTopLeft
            # Branching lines
            if branchInfo.branchLineType == 'solid':
                self.__branchesPrimitives.append(Line(
                    pt1=[branchXOrigin, branchYOrigin],
                    pt2=[branchXdestination, branchYdestination],
                    colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth,
                    frameHeight=videoHeight))
            elif branchInfo.branchLineType == 'dashed':
                self.__branchesPrimitives.append(DashedLine(
                    pt1=[branchXOrigin, branchYOrigin],
                    pt2=[branchXdestination, branchYdestination],
                    colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth,
                    frameHeight=videoHeight))

            # Traceback lines
            self.__traceBackPrimitives.append(Line(
                pt1=[branchXdestination, branchYdestination],
                pt2=[branchXOrigin, branchYOrigin],
                colour=self.__traceBackLineColour, thickness=10, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight))

            # Branching text
            proportion = branchInfo.textPositionProportion
            textX = branchXOrigin + (branchXdestination - branchXOrigin) * proportion
            textY = branchYOrigin + (branchYdestination - branchYOrigin) * proportion
            self.__branchesPrimitives.append(
                Text(text=branchInfo.branchText, org=[textX, textY], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.5,
                     colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=True))

    def colourFlash(self, startTime, drawDuration, holdDuration, startDrawProportion, endDrawProportion):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=startDrawProportion, endDrawProportion=endDrawProportion, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=endDrawProportion, endDrawProportion=endDrawProportion,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__flashingSelectionPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInCross(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__boardCrossOutPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInTraceBack(self, startTime, drawDuration, holdDuration, lineIndex):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for i, primitive in enumerate(self.__traceBackPrimitives):
            if i == lineIndex:
                drawAnimation.addPrimitive(primitive)
                holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInBranches(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__branchesPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInChessSquare(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__gridSquaresPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInPieces(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for row in self.__piecesPrimitivesLayout:
            for primitive in row:
                if primitive is None:
                    continue
                drawAnimation.addPrimitive(primitive)
                holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInBoardOutline(self, startTime, drawDuration, holdDuration, startDrawProportion, endDrawProportion):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=startDrawProportion, endDrawProportion=endDrawProportion,
                                           startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=endDrawProportion, endDrawProportion=endDrawProportion,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__colourChangingOutlinePrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInMainText(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        drawAnimation.addPrimitive(self.__mainText)
        drawAnimation.addPrimitive(self.__moveableMainText)

        holdAnimation.addPrimitive(self.__mainText)
        holdAnimation.addPrimitive(self.__moveableMainText)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def movePiece(self, startX, startY, endX, endY, startTime, duration):

        selectedPiece = self.__piecesPrimitivesLayout[startY][startX]

        assert selectedPiece is not None, "There is no piece at the selected location"

        vanishPiece = self.__piecesPrimitivesLayout[endY][endX]

        self.__piecesPrimitivesLayout[endY][endX] = selectedPiece
        self.__piecesPrimitivesLayout[startY][startX] = None

        xSqauresDelta = endX - startX
        ySqauresDelta = endY - startY

        xDelta = xSqauresDelta * self.__squareWidth
        yDelta = ySqauresDelta * self.__squareHeight

        vanishTime = 0.5

        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + vanishTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        moveAnimation.addPrimitive(selectedPiece)
        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)

        if vanishPiece is not None:
            vanishAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0, 0],
                                               startDrawProportion=1, endDrawProportion=0,
                                               startTime=startTime,
                                               endTime=startTime + vanishTime,
                                               fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
            vanishAnimation.addPrimitive(vanishPiece)
            self.__sceneAnimator.addPrimitiveAnimation(vanishAnimation)

    def moveMainText(self, startTime, duration, xDelta, yDelta):
        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        moveAnimation.addPrimitive(self.__moveableMainText)
        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)

    def move(self, startTime, duration, xDelta, yDelta):

        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        for primitive in self.__flashingSelectionPrimitives:
            moveAnimation.addPrimitive(primitive)

        for primitive in self.__gridSquaresPrimitives:
            moveAnimation.addPrimitive(primitive)

        for primitive in self.__colourChangingOutlinePrimitives:
            moveAnimation.addPrimitive(primitive)

        for primitive in self.__branchesPrimitives:
            moveAnimation.addPrimitive(primitive)

        for primitive in self.__traceBackPrimitives:
            moveAnimation.addPrimitive(primitive)



        for row in self.__piecesPrimitivesLayout:
            for primitive in row:
                if primitive is None:
                    continue
                moveAnimation.addPrimitive(primitive)

        moveAnimation.addPrimitive(self.__mainText)
        moveAnimation.addPrimitive(self.__moveableMainText)

        for primitive in self.__boardCrossOutPrimitives:
            moveAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)


class PieceValueSum:
    def __init__(self, sceneAnimator, topLeftY, topLeftX, backGroundSqaureWidth, backGroundSqaureHeight, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps

        self.__backgroundRectangle = FadeRectangle(pt1=[topLeftX, topLeftY],
                                                   pt2=[topLeftX + backGroundSqaureWidth, topLeftY + backGroundSqaureHeight],
                                                   colour=(21, 67, 120), frameWidth=videoWidth,
                                                   frameHeight=videoHeight, thickness=50,
                                                   lineType=cv2.LINE_8, drawProportion=0)

        self.__pieceImagePrimitives = []
        self.__pieceNames = ['black_bishop', 'black_queen', 'black_king', 'white_pawn', 'white_rook', 'white_king', 'white_knight']

        pieceValues = ['-3', '-9', '-10000', '1', '5', '10,000', '3']

        pieceImageWidth = backGroundSqaureWidth / len(pieceValues)

        curY = topLeftY
        for i, name in enumerate(self.__pieceNames):
            curX = topLeftX + i * pieceImageWidth
            self.__pieceImagePrimitives.append(Image(topLeft=[curX, curY],
                                                     imgPath='../resources/piece_images/' + name + '.jpg',
                                                     imageWidth=pieceImageWidth,
                                                     colour=None, drawProportion=0, maxNumBlurs=0,
                                                     frameWidth=videoWidth, frameHeight=videoHeight,
                                                     onlyKeepMonoChrome=True))
            """
            text = ' = ' + pieceValues[i]
            print(text)
            self.__pieceImagePrimitives.append(Text(text=text, org=[curX + textXOffset, curY + (pieceImageWidth/2) * (videoWidth/videoHeight)], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.7,
                     colour=(255, 255, 255),
                     backgroundColour=(21, 67, 120), drawProportion=0, progressiveDrawMode='letterByLetter',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=False))
            """

    def drawIn(self, startTime, backgroundDrawDuration, pieceAndTextDrawDuration, videoDuration):
        drawBackgroundAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                     startDrawProportion=0, endDrawProportion=1,
                                                     startTime=startTime,
                                                     endTime=startTime + backgroundDrawDuration,
                                                     fps=self.__fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdBackgroundAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + backgroundDrawDuration,
                                           endTime=videoDuration,
                                           fps=self.__fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)


        drawBackgroundAnimation.addPrimitive(self.__backgroundRectangle)
        holdBackgroundAnimation.addPrimitive(self.__backgroundRectangle)

        self.__sceneAnimator.addPrimitiveAnimation(drawBackgroundAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdBackgroundAnimation)

        for i, primitive in enumerate(self.__pieceImagePrimitives):
            drawPieceAndTextAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                         startDrawProportion=0, endDrawProportion=1,
                                                         startTime=backgroundDrawDuration + i * pieceAndTextDrawDuration,
                                                         endTime=backgroundDrawDuration + (i+1) * pieceAndTextDrawDuration,
                                                         fps=self.__fps, frameWidth=self.__videoWidth,
                                                         frameHeight=self.__videoHeight)

            holdPieceAndTextAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                                         startDrawProportion=1, endDrawProportion=1,
                                                         startTime=backgroundDrawDuration + (i+1) * pieceAndTextDrawDuration,
                                                         endTime=videoDuration,
                                                         fps=self.__fps, frameWidth=self.__videoWidth,
                                                         frameHeight=self.__videoHeight)
            drawPieceAndTextAnimation.addPrimitive(primitive)
            holdPieceAndTextAnimation.addPrimitive(primitive)

            self.__sceneAnimator.addPrimitiveAnimation(drawPieceAndTextAnimation)
            self.__sceneAnimator.addPrimitiveAnimation(holdPieceAndTextAnimation)



videoWidth = int(3840)
videoHeight = int(2160)
fps = 30
videoDuration = 5
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='27.mp4')


textX = 0.075
# Board positions


squareWidth = .05
xPerimeterSpacingFromTop = squareWidth * 0.8 #/2

depth0horizontalSpacingBetweenLines=0.5
depth0verticalSpacingBetweenBoards=1.5 * squareWidth * (videoWidth / videoHeight)

depth1horizontalSpacingBetweenLinesA=0.2
depth1horizontalSpacingBetweenLinesB=0.2
depth1verticalSpacingBetweenBoards=1.5 * squareWidth * (videoWidth / videoHeight)

depth2horizontalSpacingBetweenLines=0.05
depth2verticalSpacingBetweenBoards=1.5 * squareWidth * (videoWidth / videoHeight)

smallDemoBoard1 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=0.35, y=0.4, squareWidth=squareWidth,
                                 pieceLayout=[['black_bishop', 'black_queen', 'black_king'],
                                              [None, None, 'white_pawn'],
                                              ['white_rook', 'white_king', 'white_knight']],
                                 text="Distance: 3",
                                 branchInfoList=[BranchInfo('c3->b1', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)
                                                 ],
                                 horizontalSpacingBetweenLines=depth0horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth0verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.125,
                                 dashedBranchTextProportion=1,
                                 secondColour=(0,0,255),
                                 dashedLineText='Other Actions')

currentTimeInAnimation = 0

drawDuration = 2
smallDemoBoard1.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard1.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard1.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)
smallDemoBoard1.drawInMainText(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)

pieceValues = PieceValueSum(sceneAnimator=sceneAnimator, topLeftY=0.1, topLeftX=0.2, backGroundSqaureWidth=0.6, backGroundSqaureHeight=.4, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)
pieceValues.drawIn(startTime=0, backgroundDrawDuration=2, pieceAndTextDrawDuration=0.125, videoDuration=videoDuration)


sceneAnimator.renderAnimation()