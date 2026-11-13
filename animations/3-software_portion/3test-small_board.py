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
    def __init__(self, sceneAnimator, x, y, squareWidth, pieceLayout, text, branchInfoList, horizontalSpacingBetweenLines, verticalSpacingBetweenBoards, squareCoordinateTextScale, mainTextScale, videoWidth, videoHeight, traceBackLineColour = (0,255,0)):
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

        # Grid squares
        self.__gridSquaresPrimitives = []
        chessBoardDarkColour = (21, 67, 120)
        chessBoardLightColour = (89, 155, 240)
        squareIsDarkColour = True
        squareColour = None
        boardTopLeftX = x - 1.5 * self.__squareWidth
        boardTopLeftY = y - 1.5 * self.__squareHeight

        for i in range(3):
            for j in range(3):
                squareTopLeftX = boardTopLeftX + self.__squareWidth * i
                squareTopLeftY = boardTopLeftY + self.__squareHeight * j


                if squareIsDarkColour == True:
                    squareColour = chessBoardDarkColour
                else:
                    squareColour = chessBoardLightColour

                self.__gridSquaresPrimitives.append(FadeRectangle(pt1=[squareTopLeftX, squareTopLeftY],
                                                                  pt2=[squareTopLeftX + self.__squareWidth, squareTopLeftY + self.__squareHeight],
                                                                  colour=squareColour, frameWidth=videoWidth, frameHeight=videoHeight, thickness=1, lineType=cv2.LINE_8, drawProportion=0))

                squareIsDarkColour = not squareIsDarkColour

        # Colour changing outline
        self.__colourChangingOutlinePrimitives = []
        xSpacingFromTopLeft = self.__squareWidth
        ySpacingFromTopLeft = self.__squareHeight
        outlineTopLeftX = boardTopLeftX - xSpacingFromTopLeft
        outlineTopLeftY = boardTopLeftY - ySpacingFromTopLeft
        outlineBottomRightX = boardTopLeftX + 3 * self.__squareWidth + xSpacingFromTopLeft
        outlineBottomRightY = boardTopLeftY + 3 * self.__squareHeight + ySpacingFromTopLeft
        self.__colourChangingOutlinePrimitives.append(ColourChangeRectangle(pt1=[outlineTopLeftX, outlineTopLeftY],
                                                                            pt2=[outlineBottomRightX, outlineBottomRightY],
                                                                            drawProportion=0,
                                                                            firstColour=(255,255,255),
                                                                            secondColour=(0,255,0),
                                                                            thirdColour=(0,0,255),
                                                                            frameWidth=videoWidth, frameHeight=videoHeight, thickness=5))
        # square coordinate text
        columnNames = ['a','b','c']
        rowNames = ['1','2','3']
        columnY = y + 1.5 * self.__squareHeight + ySpacingFromTopLeft / 2
        for i, columnName in enumerate(columnNames):
            columnX = x - self.__squareWidth  + i * self.__squareWidth
            self.__gridSquaresPrimitives.append(Text(text=columnName, org=[columnX, columnY], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=self.__squareCoordinateTextScale,
             colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5,
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
        self.__piecesPrimitivesLayout = [[None,None,None], [None,None,None], [None,None,None]]
        for rowIdx, row in enumerate(pieceLayout):
            for colIdx, piece in enumerate(row):
                pieceName = pieceLayout[rowIdx][colIdx]
                if pieceName is None:
                    continue

                pieceTopLeftX = boardTopLeftX + self.__squareWidth * colIdx
                pieceTopLeftY = boardTopLeftY + self.__squareHeight * rowIdx
                path = '../resources/piece_images/' + pieceName + '.jpg'
                cv2.imread(path)
                self.__piecesPrimitivesLayout[rowIdx][colIdx] = (Image(topLeft=[pieceTopLeftX, pieceTopLeftY],
                                                     imgPath=path,
                                                     imageWidth=self.__squareWidth,
                                                     colour=None, drawProportion=0, maxNumBlurs=100,frameWidth=videoWidth, frameHeight=videoHeight, onlyKeepMonoChrome=True))

        # Branches and branch text
        self.__branchesPrimitives = []
        self.__traceBackPrimitives = []
        branchIntersectionX = self.__x
        branchIntersectionY = self.__y + 1.5 * self.__squareHeight

        branchYdestination = branchIntersectionY + verticalSpacingBetweenBoards

        if len(branchInfoList) % 2 == 0:
            startXdestination =  branchIntersectionX - horizontalSpacingBetweenLines/2 - ((len(branchInfoList)/2)-1) * horizontalSpacingBetweenLines
        else:
            startXdestination = branchIntersectionX - math.floor(len(branchInfoList)/2) * horizontalSpacingBetweenLines


        for i, branchInfo in enumerate(self.__branchInfoList):
            branchXdestination = startXdestination + i * horizontalSpacingBetweenLines

            aDash = ySpacingFromTopLeft

            o = branchXdestination - branchIntersectionX
            a = branchYdestination - branchIntersectionY

            branchXOrigin = branchIntersectionX + aDash * (o/a)
            branchYOrigin = branchIntersectionY + ySpacingFromTopLeft
            # Branching lines
            if branchInfo.branchLineType == 'solid':
                self.__branchesPrimitives.append(Line(
                     pt1=[branchXOrigin, branchYOrigin],
                     pt2=[branchXdestination, branchYdestination],
                     colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))
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
            self.__branchesPrimitives.append(Text(text=branchInfo.branchText, org=[textX, textY], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                 colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5,
                 frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=True))

            # Traceback lines
            self.__traceBackPrimitives.append(Line(
                     pt1=[branchXdestination, branchYdestination],
                     pt2=[branchXOrigin, branchYOrigin],
                     colour=self.__traceBackLineColour, thickness=10, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

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
                                           startDrawProportion=startDrawProportion, endDrawProportion=endDrawProportion, startTime=startTime,
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

        self.__piecesPrimitivesLayout[endY][endX] = selectedPiece
        self.__piecesPrimitivesLayout[startY][startX] = None

        xSqauresDelta = endX - startX
        ySqauresDelta = endY - startY

        xDelta = xSqauresDelta * self.__squareWidth
        yDelta = ySqauresDelta * self.__squareHeight
        
        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        moveAnimation.addPrimitive(selectedPiece)

        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)

    def moveMainText(self, startTime, duration, xDelta, yDelta):
        moveAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[xDelta, yDelta],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime,
                                           endTime=startTime + duration,
                                           fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)

        moveAnimation.addPrimitive(self.__moveableMainText)
        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)

    def move(self, startTime,  duration, xDelta, yDelta):


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


videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 15
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='3test.mp4')

smallDemoBoard1 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=0.5, y=0.5, squareWidth=0.0333,
                                 pieceLayout=[['white_rook',None,None],
                                             [None,'black_bishop',None],
                                             [None,None,None]],
                                 text="TEST TEXT",
                                 branchInfoList=[BranchInfo('b1', 'solid', 0.3),
                                                 BranchInfo('b2', 'solid', 0.6),
                                                 BranchInfo('b3', 'solid', 0.3),
                                                 BranchInfo('b4', 'dashed',0.6)],
                                 horizontalSpacingBetweenLines=0.0333,
                                 verticalSpacingBetweenBoards=2*0.0333*(videoWidth/videoHeight),
                                 squareCoordinateTextScale=1,
                                 mainTextScale=1,
                                 videoWidth=videoWidth, videoHeight=videoHeight)




smallDemoBoard1.drawInChessSquare(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard1.drawInPieces(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard1.drawInBoardOutline(startTime=0, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.0, endDrawProportion=0.3333)
smallDemoBoard1.drawInBranches(startTime=6, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard1.drawInMainText(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard1.drawInTraceBack(startTime=9, drawDuration=3, holdDuration=videoDuration, lineIndex=1)


smallDemoBoard2 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=0.5, y=0.5, squareWidth=0.0333,
                                 pieceLayout=[['white_rook',None,None],
                                             [None,'black_bishop',None],
                                             [None,None,None]],
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
smallDemoBoard2.drawInBoardOutline(startTime=0, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.0, endDrawProportion=0.3333)
smallDemoBoard2.movePiece(startX=0, startY=0, endX=2, endY=1, startTime=3, duration=1)
smallDemoBoard2.movePiece(startX=2, startY=1, endX=0, endY=2, startTime=6, duration=1)
smallDemoBoard2.moveMainText(startTime=8, duration=2, xDelta=0.1, yDelta=-0.3)
smallDemoBoard2.drawInBoardOutline(startTime=6, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.3333, endDrawProportion=0.6666)



sceneAnimator.renderAnimation()