from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math


class PieceValues:
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
        self.__pieceNames = ['white_pawn', 'white_knight', 'white_bishop', 'white_rook', 'white_queen', 'white_king',
                             'black_pawn', 'black_knight', 'black_bishop', 'black_rook', 'black_queen', 'black_king']

        pieceValues = ['1', '3', '3', '5', '9', '10,000', '-1', '-3', '-3', '-5', '-9', '-10,000']

        pieceImageWidth = backGroundSqaureHeight * (videoHeight / videoWidth)  * (1/6)
        startX = topLeftX
        startY = topLeftY

        whiteBlackXspacing = backGroundSqaureWidth / 2
        pieceYspacing = pieceImageWidth * videoWidth / videoHeight

        textXOffset = 2 * pieceImageWidth
        for i, name in enumerate(self.__pieceNames):
            tempY = startY + pieceYspacing * i

            if 'white' in name:
                curX = startX
                curY = tempY
            else:
                curX = startX + whiteBlackXspacing
                curY = tempY - pieceYspacing * 6
            self.__pieceImagePrimitives.append(Image(topLeft=[curX, curY],
                                                     imgPath='../resources/piece_images/' + name + '.jpg',
                                                     imageWidth=pieceImageWidth,
                                                     colour=None, drawProportion=0, maxNumBlurs=0,
                                                     frameWidth=videoWidth, frameHeight=videoHeight,
                                                     onlyKeepMonoChrome=True))

            text = ' = ' + pieceValues[i]
            print(text)
            self.__pieceImagePrimitives.append(Text(text=text, org=[curX + textXOffset, curY + (pieceImageWidth/2) * (videoWidth/videoHeight)], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.7,
                     colour=(255, 255, 255),
                     backgroundColour=(21, 67, 120), drawProportion=0, progressiveDrawMode='letterByLetter',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=False))


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
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='26.mp4')

pieceValues = PieceValues(sceneAnimator=sceneAnimator, topLeftY=0.1, topLeftX=0.2, backGroundSqaureWidth=0.6, backGroundSqaureHeight=.7, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)
pieceValues.drawIn(startTime=0, backgroundDrawDuration=2, pieceAndTextDrawDuration=0.125, videoDuration=videoDuration)



sceneAnimator.renderAnimation()