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
                                                   colour=(89, 155, 240), frameWidth=videoWidth,
                                                   frameHeight=videoHeight, thickness=1,
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


    def drawIn(self, startTime, drawDuration, holdDuration):
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


        drawAnimation.addPrimitive(self.__backgroundRectangle)
        holdAnimation.addPrimitive(self.__backgroundRectangle)

        for primitive in self.__pieceImagePrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)


videoWidth = int(3840)
videoHeight = int(2160)
fps = 30
videoDuration = 3
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='21.mp4')

pieceValues = PieceValues(sceneAnimator=sceneAnimator, topLeftY=0.1, topLeftX=0.2, backGroundSqaureWidth=0.6, backGroundSqaureHeight=.5, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)
pieceValues.drawIn(startTime=0, drawDuration=2, holdDuration=videoDuration)



sceneAnimator.renderAnimation()