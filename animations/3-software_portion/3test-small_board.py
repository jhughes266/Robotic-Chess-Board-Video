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
    def __init__(self, sceneAnimator, x, y, squareWidth, pieceLayout, text, branchInfoList, horizontalSpacingBetweenLines, verticalSpacingBetweenBoards, videoWidth, videoHeight):
        self.__sceneAnimator = sceneAnimator
        self.__x = x
        self.__y = y
        self.__squareWidth = squareWidth
        self.__squareHeight = squareWidth * videoWidth / videoHeight
        self.__text = text
        self.__branchInfoList = branchInfoList
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight

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
        branchXOrigin = self.__x
        branchYOrigin = self.__y + 1.5 * self.__squareHeight

        branchYdestination = branchYOrigin + verticalSpacingBetweenBoards
        if len(branchInfoList) % 2 == 0:
            startXdestination =  branchXOrigin - horizontalSpacingBetweenLines/2 - ((len(branchInfoList)/2)-1) * horizontalSpacingBetweenLines
        else:
            startXdestination = branchXOrigin - math.floor(len(branchInfoList)/2) * horizontalSpacingBetweenLines


        for i, branchInfo in enumerate(self.__branchInfoList):
            branchXdestination = startXdestination + i * horizontalSpacingBetweenLines
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

    def move(self, startTime,  duration, xDelta, yDelta,):


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

        self.__sceneAnimator.addPrimitiveAnimation(moveAnimation)


videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='3test.mp4')

smallDemoBoard1 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=0.5, y=0.5, squareWidth=0.0333,
                                 pieceLayout=[['white_rook',None,None],
                                             [None,'black_bishop',None],
                                             [None,None,None]],
                                 text=None,
                                 branchInfoList=[BranchInfo('b1', 'solid', 0.3),
                                                 BranchInfo('b2', 'solid', 0.6),
                                                 BranchInfo('b3', 'solid', 0.3),
                                                 BranchInfo('b4', 'dashed',0.6)],
                                 horizontalSpacingBetweenLines=0.0333,
                                 verticalSpacingBetweenBoards=2*0.0333*(videoWidth/videoHeight),
                                 videoWidth=videoWidth, videoHeight=videoHeight)




smallDemoBoard1.drawInChessSquare(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard1.drawInPieces(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard1.drawInBoardOutline(startTime=0, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.0, endDrawProportion=0.3333)
smallDemoBoard1.drawInBranches(startTime=6, drawDuration=3, holdDuration=videoDuration)
#smallDemoBoard1.move(startTime=4, duration=2, xDelta=0.1, yDelta=0.2)

"""
smallDemoBoard2 = SmallDemoBoard(sceneAnimator=sceneAnimator, x=0.5, y=0.5, squareWidth=0.0333,
                                 pieceLayout=[['white_rook',None,None],
                                             [None,'black_bishop',None],
                                             [None,None,None]],
                                 text=None, branchInfoList=None, videoWidth=videoWidth, videoHeight=videoHeight)

smallDemoBoard2.move(startTime=4, duration=2, xDelta=0.1, yDelta=0.2)
smallDemoBoard2.drawInChessSquare(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard2.drawInPieces(startTime=0, drawDuration=3, holdDuration=videoDuration)
smallDemoBoard2.drawInBoardOutline(startTime=0, drawDuration=3, holdDuration=videoDuration, startDrawProportion=0.0, endDrawProportion=0.3333)
smallDemoBoard2.movePiece(startX=0, startY=0, endX=2, endY=1, startTime=3, duration=1)
smallDemoBoard2.movePiece(startX=2, startY=1, endX=0, endY=2, startTime=6, duration=1)
"""


sceneAnimator.renderAnimation()