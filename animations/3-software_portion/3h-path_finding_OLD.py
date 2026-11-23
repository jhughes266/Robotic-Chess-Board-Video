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
                 videoWidth, videoHeight, xPerimeterSpacingFromTop, traceBackLineColour=(0, 255, 0), dashedBranch=False, dashedBranchLengthProportion=1, dashedBranchTextProportion=1):
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
                                                                            firstColour=(255, 255, 255),
                                                                            secondColour=(255, 0, 255),
                                                                            thirdColour=(255, 0, 255),
                                                                            frameWidth=videoWidth,
                                                                            frameHeight=videoHeight, thickness=5))

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
            self.__branchesPrimitives.append(
                Text(text="Other moves", org=[textX, textY], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.5,
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
            # Branching text
            proportion = branchInfo.textPositionProportion
            textX = branchXOrigin + (branchXdestination - branchXOrigin) * proportion
            textY = branchYOrigin + (branchYdestination - branchYOrigin) * proportion
            self.__branchesPrimitives.append(
                Text(text=branchInfo.branchText, org=[textX, textY], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.5,
                     colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=True))

            # Traceback lines
            self.__traceBackPrimitives.append(Line(
                pt1=[branchXdestination, branchYdestination],
                pt2=[branchXOrigin, branchYOrigin],
                colour=self.__traceBackLineColour, thickness=10, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight))




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

        for primitive in self.__gridSquaresPrimitives:
            moveAnimation.addPrimitive(primitive)

        for primitive in self.__colourChangingOutlinePrimitives:
            moveAnimation.addPrimitive(primitive)

        for primitive in self.__branchesPrimitives:
            moveAnimation.addPrimitive(primitive)

        for row in self.__piecesPrimitivesLayout:
            for primitive in row:
                if primitive is None:
                    continue
                moveAnimation.addPrimitive(primitive)

        moveAnimation.addPrimitive(self.__mainText)
        moveAnimation.addPrimitive(self.__moveableMainText)

        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)



class Message:
    def __init__(self, sceneAnimator, x, y, message, colour, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__text = Text(text=message, org=[x, y], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3,
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


    def move(self, startTime, duration, xDelta, yDelta):

        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        moveAnimation.addPrimitive(self.__text)

        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)


class EntireAnimationMover:
    def __init__(self, sceneAnimator):
        self.__sceneAnimator = sceneAnimator
        self.__entitiesToBeMoved = []

    def addEntityToMoveList(self, entity):
        self.__entitiesToBeMoved.append(entity)

    def move(self, startTime, duration, xDelta, yDelta):
        for entity in self.__entitiesToBeMoved:
            entity.move(startTime, duration, xDelta, yDelta)


videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 25
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='3h-path_finding.mp4')

entireAnimationMover = EntireAnimationMover(sceneAnimator)

textX = 0.075
# Board positions
board1x = 0.5
board1y = 0.15
# Turns
white1 = Message(sceneAnimator=sceneAnimator, x=textX, y=board1y, message='Whites Turn', colour=(255,255,255), videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)
entireAnimationMover.addEntityToMoveList(white1)

squareWidth = 1 / (4*12)
xPerimeterSpacingFromTop = squareWidth * 0.8 #/2

depth0horizontalSpacingBetweenLines=0.5
depth0verticalSpacingBetweenBoards=1.5 * squareWidth * (videoWidth / videoHeight)

depth1horizontalSpacingBetweenLinesA=0.1
depth1horizontalSpacingBetweenLinesB=0.2
depth1verticalSpacingBetweenBoards=1.5 * squareWidth * (videoWidth / videoHeight)

depth2horizontalSpacingBetweenLines=0.05
depth2verticalSpacingBetweenBoards=1.5 * squareWidth * (videoWidth / videoHeight)

smallDemoBoard1 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board1x, y=board1y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', 'black_king'],
                                              ['black_queen', None, 'white_rook'],
                                              ['white_king', None, 'white_knight']],
                                 text="TEST TEXT",
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
                                 dashedBranchTextProportion=1)
entireAnimationMover.addEntityToMoveList(smallDemoBoard1)


smallDemoBoard2 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board1x, y=board1y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', 'black_king'],
                                              ['black_queen', None, 'white_rook'],
                                              ['white_king', None, 'white_knight']],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('c1->c2', 'solid', 0.6),
                                                 BranchInfo('b1->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth1horizontalSpacingBetweenLinesB,
                                 verticalSpacingBetweenBoards=depth1verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.15,
                                 dashedBranchTextProportion=1
                                 )
entireAnimationMover.addEntityToMoveList(smallDemoBoard2)

smallDemoBoard3 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board1x, y=board1y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', 'black_king'],
                                              ['black_queen', None, 'white_rook'],
                                              ['white_king', None, 'white_knight']],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('a2->a3', 'solid', 0.6),
                                                 BranchInfo('c1->c2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth1horizontalSpacingBetweenLinesA,
                                 verticalSpacingBetweenBoards=depth1verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.3,
                                 dashedBranchTextProportion=1
                                 )
entireAnimationMover.addEntityToMoveList(smallDemoBoard3)



currentTimeInAnimation = 0
#Draw in the first 3 chess boards 1 will be the root the others will be transported down branches
drawDuration = 2
smallDemoBoard1.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard1.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard1.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard2.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard2.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard2.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard3.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard3.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard3.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)
white1.drawInText(startTime=currentTimeInAnimation,drawDuration=drawDuration, holdDuration=videoDuration)
currentTimeInAnimation += drawDuration


# board 3 move to place
moveDuration = 2
smallDemoBoard3.movePiece(startX=2, startY=2, endX=1, endY=0, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board3xDelta = -depth0horizontalSpacingBetweenLines/2
board3yDelta = depth0verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard3.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board3xDelta, yDelta=board3yDelta)
currentTimeInAnimation += boardMoveDuration


# Board 2 move to place
moveDuration = 2
smallDemoBoard2.movePiece(startX=2, startY=1, endX=0, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board2xDelta = depth0horizontalSpacingBetweenLines/2
board2yDelta = depth0verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard2.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board2xDelta, yDelta=board2yDelta)
currentTimeInAnimation += boardMoveDuration

# Draw in branches down to 1 depth
branchDrawDuration = 2
smallDemoBoard1.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += branchDrawDuration



"""
# Create and draw in new boards 4,5,6,7,
board4And5x = board1x + board2xDelta + 0.0035
#added a small vertical offset as it was slightly unaligned
board4And5y = board1y + board2yDelta + 0.003

board6And7x = board1x + board3xDelta - 0.0035
board6And7y =  board1y + board3yDelta + 0.003

smallDemoBoard4 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board4And5x, y=board4And5y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', 'black_king'],
                                              ['white_rook', None, None],
                                              ['white_king', None, 'white_knight']],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('c2->a2', 'solid', 0.8),
                                                 BranchInfo('a3->b3', 'solid', 0.8)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.35,
                                 dashedBranchTextProportion=1
                                 )

smallDemoBoard5 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board4And5x, y=board4And5y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', 'black_king'],
                                              ['white_rook', None, None],
                                              ['white_king', None, 'white_knight']],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('a2->c2', 'solid', 0.8),
                                                 BranchInfo('c3->b1', 'solid', 0.8)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.35,
                                 dashedBranchTextProportion=1
                                 )

smallDemoBoard6 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board6And7x, y=board6And7y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'white_knight', 'black_king'],
                                              ['black_queen', None, 'white_rook'],
                                              ['white_king', None, None]],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('a3->a2', 'solid', 0.8),
                                                 BranchInfo('a3->b3', 'solid', .8)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.35,
                                 dashedBranchTextProportion=1
                                 )

smallDemoBoard7 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board6And7x, y=board6And7y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'white_knight', 'black_king'],
                                              ['black_queen', None, 'white_rook'],
                                              ['white_king', None, None]],
                                 text="Value: -10,000",
                                 branchInfoList=[],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

# draw in board 4,5,6 and 7
drawDuration = .5

black1 = Message(sceneAnimator=sceneAnimator, x=textX, y=board4And5y, message='Blacks Turn', colour=(255,255,255), videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)
black1.drawInText(startTime=currentTimeInAnimation,drawDuration=drawDuration, holdDuration=videoDuration)
currentTimeInAnimation += drawDuration

smallDemoBoard4.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard4.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard4.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard5.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard5.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard5.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard6.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard6.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard6.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard7.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard7.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard7.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)



# board 7 move to place
moveDuration = 2
smallDemoBoard7.movePiece(startX=0, startY=1, endX=0, endY=2, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board7xDelta = -depth1horizontalSpacingBetweenLinesA/2
board7yDelta = depth0verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard7.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board7xDelta, yDelta=board7yDelta)
currentTimeInAnimation += boardMoveDuration

# board 6 move to place
moveDuration = 2
smallDemoBoard6.movePiece(startX=2, startY=0, endX=2, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board6xDelta = +depth1horizontalSpacingBetweenLinesA/2
board6yDelta = depth0verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard6.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board6xDelta, yDelta=board6yDelta)
currentTimeInAnimation += boardMoveDuration

# board 5 move to place
moveDuration = 2
smallDemoBoard5.movePiece(startX=2, startY=0, endX=2, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board5xDelta = -depth1horizontalSpacingBetweenLinesB/2
board5yDelta = depth0verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard5.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board5xDelta, yDelta=board5yDelta)
currentTimeInAnimation += boardMoveDuration

# board 4 move to place
moveDuration = 2
smallDemoBoard4.movePiece(startX=1, startY=0, endX=0, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board4xDelta = +depth1horizontalSpacingBetweenLinesB/2
board4yDelta = depth0verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard4.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board4xDelta, yDelta=board4yDelta)
currentTimeInAnimation += boardMoveDuration

# Draw in branches down to 2 depth
branchDrawDuration = 2
smallDemoBoard3.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
smallDemoBoard2.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += branchDrawDuration




# Create and draw in new boards 8,9,10,11,12,13
board9And8x = board4And5x + board4xDelta + 0.002
board9And8y = board4And5y + board4yDelta + 0.003

board11And10x = board4And5x + board5xDelta - 0.0015
board11And10y = board4And5y + board5yDelta + 0.0025

board13And12x = board6And7x + board6xDelta + 0.001
board13And12y = board6And7y + board6yDelta + 0.003




smallDemoBoard8 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board9And8x, y=board9And8y, squareWidth=squareWidth,
                                 pieceLayout=[[None, None, 'black_king'],
                                              ['black_bishop', None, None],
                                              ['white_king', None, 'white_knight']],
                                 text="Value: 0",
                                 branchInfoList=[BranchInfo('c3->b3', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard9 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board9And8x, y=board9And8y, squareWidth=squareWidth,
                                 pieceLayout=[[None, None, 'black_king'],
                                              ['black_bishop', None, None],
                                              ['white_king', None, 'white_knight']],
                                 text="Value: 3",
                                 branchInfoList=[BranchInfo('c3->b3', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard10 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board11And10x, y=board11And10y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', None],
                                              ['white_rook', None, 'black_king'],
                                              ['white_king', None, 'white_knight']],
                                 text="Value: 8",
                                 branchInfoList=[BranchInfo('c3->b3', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard11 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board11And10x, y=board11And10y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', None],
                                              ['white_rook', None, 'black_king'],
                                              ['white_king', None, 'white_knight']],
                                 text="Value: 10,005",
                                 branchInfoList=[BranchInfo('c3->b3', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard12 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board13And12x, y=board13And12y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'white_knight', None],
                                              ['black_queen', None, 'black_king'],
                                              ['white_king', None, None ]],
                                 text="Value: -6",
                                 branchInfoList=[BranchInfo('c3->b3', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard13 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board13And12x, y=board13And12y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'white_knight', None],
                                              ['white_rook', None, 'black_king'],
                                              ['white_king', None, None ]],
                                 text="Value: 3",
                                 branchInfoList=[BranchInfo('c3->b3', 'solid', 0.6),
                                                 BranchInfo('c2->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth2horizontalSpacingBetweenLines,
                                 verticalSpacingBetweenBoards=depth2verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight)
# draw in board 8,9,10,11,12,13
drawDuration = .5
timeUntilFinalPositionHighlight = 26
finalPositionOutLineDrawInFinished = currentTimeInAnimation + drawDuration
smallDemoBoard8.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard8.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard8.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=timeUntilFinalPositionHighlight, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard9.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard9.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard9.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=timeUntilFinalPositionHighlight, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard10.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard10.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard10.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=timeUntilFinalPositionHighlight, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard11.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard11.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard11.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=timeUntilFinalPositionHighlight, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard12.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard12.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard12.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=timeUntilFinalPositionHighlight, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

smallDemoBoard13.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard13.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoard13.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=timeUntilFinalPositionHighlight, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)

white2 = Message(sceneAnimator=sceneAnimator, x=textX, y=board9And8y, message='Whites Turn', colour=(255,255,255), videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)

white2.drawInText(startTime=currentTimeInAnimation,drawDuration=drawDuration, holdDuration=videoDuration)

currentTimeInAnimation += drawDuration

# board 13 move to place
moveDuration = 2
smallDemoBoard13.movePiece(startX=0, startY=2, endX=0, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board13xDelta = -depth2horizontalSpacingBetweenLines
board13yDelta = depth2verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard13.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board13xDelta, yDelta=board13yDelta)
currentTimeInAnimation += boardMoveDuration

# board 12 move to place
moveDuration = 2
smallDemoBoard12.movePiece(startX=0, startY=2, endX=1, endY=2, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board12xDelta = depth2horizontalSpacingBetweenLines
board12yDelta = depth2verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard12.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board12xDelta, yDelta=board12yDelta)
currentTimeInAnimation += boardMoveDuration

# board 11 move to place
moveDuration = 2
smallDemoBoard11.movePiece(startX=0, startY=1, endX=2, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board11xDelta = -depth2horizontalSpacingBetweenLines
board11yDelta = depth2verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard11.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board11xDelta, yDelta=board11yDelta)
currentTimeInAnimation += boardMoveDuration

# board 10 move to place
moveDuration = 2
smallDemoBoard10.movePiece(startX=2, startY=2, endX=1, endY=0, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board10xDelta = depth2horizontalSpacingBetweenLines
board10yDelta = depth2verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard10.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board10xDelta, yDelta=board10yDelta)
currentTimeInAnimation += boardMoveDuration

# board 9 move to place
moveDuration = 2
smallDemoBoard9.movePiece(startX=2, startY=2, endX=0, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board9xDelta = -depth2horizontalSpacingBetweenLines
board9yDelta = depth2verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard9.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board9xDelta, yDelta=board9yDelta)
currentTimeInAnimation += boardMoveDuration

# board 8 move to place
moveDuration = 2
smallDemoBoard8.movePiece(startX=0, startY=2, endX=1, endY=2, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
boardMoveDuration = 2
board8xDelta = depth2horizontalSpacingBetweenLines
board8yDelta = depth2verticalSpacingBetweenBoards + squareWidth*4*(videoWidth / videoHeight)
smallDemoBoard8.move(startTime=currentTimeInAnimation, duration=boardMoveDuration, xDelta=board8xDelta, yDelta=board8yDelta)
currentTimeInAnimation += boardMoveDuration


# Draw in branches down to 3 depth
branchDrawDuration = 2
smallDemoBoard4.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
smallDemoBoard5.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
smallDemoBoard6.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
smallDemoBoard7.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)

currentTimeInAnimation += branchDrawDuration
print(f"The current animation time is {currentTimeInAnimation}.\nThe outline finished drawing at {finalPositionOutLineDrawInFinished}.\nThe 'timeUntilFinalPositionHighlight' should be set to {currentTimeInAnimation - finalPositionOutLineDrawInFinished}.")


# Make the final positions flash pink
numberOfFlashes = 5
cycleDuration = 1
for i in range(numberOfFlashes):
    holdDuration = cycleDuration/2
    smallDemoBoard8.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=cycleDuration/2, holdDuration=holdDuration, startDrawProportion=0.3333, endDrawProportion=0.66666)
    smallDemoBoard9.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=cycleDuration/2, holdDuration=holdDuration, startDrawProportion=0.3333, endDrawProportion=0.66666)
    smallDemoBoard10.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=cycleDuration/2, holdDuration=holdDuration, startDrawProportion=0.3333, endDrawProportion=0.66666)
    smallDemoBoard11.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=cycleDuration/2, holdDuration=holdDuration, startDrawProportion=0.3333, endDrawProportion=0.66666)
    smallDemoBoard12.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=cycleDuration/2, holdDuration=holdDuration, startDrawProportion=0.3333, endDrawProportion=0.66666)
    smallDemoBoard13.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=cycleDuration/2, holdDuration=holdDuration, startDrawProportion=0.3333, endDrawProportion=0.66666)

    if i + 1 == numberOfFlashes:
        holdDuration=videoDuration
    smallDemoBoard8.drawInBoardOutline(startTime=currentTimeInAnimation+cycleDuration/2, drawDuration=cycleDuration/2, holdDuration=holdDuration,
                                       startDrawProportion=0.66666, endDrawProportion=0.33333)
    smallDemoBoard9.drawInBoardOutline(startTime=currentTimeInAnimation+cycleDuration/2, drawDuration=cycleDuration/2, holdDuration=holdDuration,
                                       startDrawProportion=0.66666, endDrawProportion=0.33333)
    smallDemoBoard10.drawInBoardOutline(startTime=currentTimeInAnimation+cycleDuration/2, drawDuration=cycleDuration/2, holdDuration=holdDuration,
                                        startDrawProportion=0.66666, endDrawProportion=0.33333)
    smallDemoBoard11.drawInBoardOutline(startTime=currentTimeInAnimation+cycleDuration/2, drawDuration=cycleDuration/2, holdDuration=holdDuration,
                                        startDrawProportion=0.66666, endDrawProportion=0.33333)
    smallDemoBoard12.drawInBoardOutline(startTime=currentTimeInAnimation+cycleDuration/2, drawDuration=cycleDuration/2, holdDuration=holdDuration,
                                        startDrawProportion=0.66666, endDrawProportion=0.33333)
    smallDemoBoard13.drawInBoardOutline(startTime=currentTimeInAnimation+cycleDuration/2, drawDuration=cycleDuration/2, holdDuration=holdDuration,
                                        startDrawProportion=0.66666, endDrawProportion=0.33333)

    currentTimeInAnimation += cycleDuration


# Draw in the final position values
textDrawDuration = 1
currentTimeInAnimation += 1
smallDemoBoard7.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
smallDemoBoard13.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
smallDemoBoard12.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
smallDemoBoard11.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
smallDemoBoard10.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
smallDemoBoard9.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
smallDemoBoard8.drawInMainText(startTime=currentTimeInAnimation, drawDuration=textDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += 1
print(currentTimeInAnimation)

# Passing the position values back up the tree
# 3 depth
textMoveDuration = 2
smallDemoBoard9.moveMainText(startTime=currentTimeInAnimation, duration=textMoveDuration, xDelta=-board9xDelta, yDelta=-board9yDelta)
currentTimeInAnimation += textMoveDuration

smallDemoBoard11.moveMainText(startTime=currentTimeInAnimation, duration=textMoveDuration, xDelta=-board11xDelta, yDelta=-board11yDelta)
currentTimeInAnimation += textMoveDuration

smallDemoBoard13.moveMainText(startTime=currentTimeInAnimation, duration=textMoveDuration, xDelta=-board13xDelta, yDelta=-board13yDelta)
currentTimeInAnimation += textMoveDuration

# 2 depth
smallDemoBoard9.moveMainText(startTime=currentTimeInAnimation, duration=textMoveDuration, xDelta=-board4xDelta, yDelta=-board4yDelta)
currentTimeInAnimation += textMoveDuration

smallDemoBoard7.moveMainText(startTime=currentTimeInAnimation, duration=textMoveDuration, xDelta=-board7xDelta, yDelta=-board7yDelta)
currentTimeInAnimation += textMoveDuration

# 1 depth
smallDemoBoard9.moveMainText(startTime=currentTimeInAnimation, duration=textMoveDuration, xDelta=-board2xDelta, yDelta=-board2yDelta)
currentTimeInAnimation += textMoveDuration
print(currentTimeInAnimation)

# Demonstrating the chose move
smallDemoBoardFinalMove = SmallDemoBoard(sceneAnimator=sceneAnimator, x=board1x, y=board1y, squareWidth=squareWidth,
                                 pieceLayout=[[None, 'black_bishop', 'black_king'],
                                              ['black_queen', None, 'white_rook'],
                                              ['white_king', None, 'white_knight']],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('c1->c2', 'solid', 0.6),
                                                 BranchInfo('b1->a2', 'solid', 0.6)],
                                 horizontalSpacingBetweenLines=depth1horizontalSpacingBetweenLinesB,
                                 verticalSpacingBetweenBoards=depth1verticalSpacingBetweenBoards,
                                 squareCoordinateTextScale=1.5,
                                 mainTextScale=1.5,
                                 xPerimeterSpacingFromTop=xPerimeterSpacingFromTop,
                                 videoWidth=videoWidth, videoHeight=videoHeight,
                                 dashedBranch=True,
                                 dashedBranchLengthProportion=0.15,
                                 dashedBranchTextProportion=1
                                 )

drawDuration = 2
smallDemoBoardFinalMove.drawInChessSquare(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoardFinalMove.drawInPieces(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration)
smallDemoBoardFinalMove.drawInBoardOutline(startTime=currentTimeInAnimation, drawDuration=drawDuration, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)
currentTimeInAnimation += drawDuration

moveDuration = 2
smallDemoBoardFinalMove.movePiece(startX=2, startY=1, endX=0, endY=1, startTime=currentTimeInAnimation, duration=moveDuration)
currentTimeInAnimation += moveDuration
print(currentTimeInAnimation)





branchDrawDuration = 2
smallDemoBoard3.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
# draw branches from board 4
smallDemoBoard2.drawInBranches(startTime=currentTimeInAnimation, drawDuration=branchDrawDuration, holdDuration=videoDuration)
currentTimeInAnimation += branchDrawDuration





#smallDemoBoard1.drawInMainText(startTime=0, drawDuration=3, holdDuration=videoDuration)
#smallDemoBoard1.drawInTraceBack(startTime=9, drawDuration=3, holdDuration=videoDuration, lineIndex=1)
smallDemoBoard2 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=0.5, y=0.5, squareWidth=0.0333,
                                 pieceLayout=[['white_rook', None, None],
                                              [None, 'black_bishop', None],
                                              [None, None, None]],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('b1', 'solid', 0.3),
                                                 BranchInfo('b2', 'solid', 0.6),
                                                 BranchInfo('b3', 'solid', 0.3),
                                                 BranchInfo('b4', 'dashed', 0.6)],
                                 horizontalSpacingBetweenLines=0.0333,
                                 verticalSpacingBetweenBoards=2 * 0.0333 * (videoWidth / videoHeight),
                                 squareCoordinateTextScale=1,
                                 mainTextScale=1,
                                 videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard2.move(startTime=4, duration=2, xDelta=0.1, yDelta=0.2)
smallDemoBoard2.drawInMainText(startTime=6, drawDuration=1, holdDuration=videoDuration)
smallDemoBoard2.drawInChessSquare(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard2.drawInPieces(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard2.drawInBoardOutline(startTime=0, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.0,
                                   endDrawProportion=0.3333)
smallDemoBoard2.movePiece(startX=0, startY=0, endX=2, endY=1, startTime=3, duration=1)
smallDemoBoard2.movePiece(startX=2, startY=1, endX=0, endY=2, startTime=6, duration=1)
smallDemoBoard2.moveMainText(startTime=8, duration=2, xDelta=0.1, yDelta=-0.3)
smallDemoBoard2.drawInBoardOutline(startTime=6, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.3333,
                                   endDrawProportion=0.6666)
"""
sceneAnimator.renderAnimation()