from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math



class PanelVisuals:
    def __init__(self, sceneAnimator, imagePath, imageWidth, topLeftX, topLeftY, videoWidth, videoHeight, fps):
        self.__sceneAnimator = sceneAnimator
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__fps = fps
        self.__panelImage = Image(topLeft=[topLeftX, topLeftY],
                                  imgPath=imagePath,
                                  imageWidth=imageWidth,
                                  colour=None, drawProportion=0, maxNumBlurs=0,
                                  frameWidth=videoWidth, frameHeight=videoHeight,
                                   onlyKeepMonoChrome=False)

        self.__columnPrimitives = []
        self.__rowPrimitives = []
        self.__numberPrimitives = []

        panelDrawTopRightX = 0.775 + 0.01
        panelDrawTopRightY = 0.21

        columnHeight = 0.36
        columnWidthList =[0.01000, 0.010000, 0.01000, 0.01000, 0.00950, 0.00950, 0.00950, 0.00950, 0.00925, 0.00925, 0.00925, 0.00925,
                          0.00925, 0.00925, 0.00925, 0.00925, 0.00925, 0.00925, 0.00910, 0.00910, 0.00910, 0.00910,
                          0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910,
                          0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910,
                          0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910,
                          0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910,
                          0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910, 0.00910]




        xSpacingToBottom = 0.004

        numberOfColumns= 71




        for i in range(numberOfColumns + 1):
            columnWidth = columnWidthList[i]
            columnTopX = panelDrawTopRightX - i * columnWidth
            columnTopY = panelDrawTopRightY

            columnBottomX = columnTopX - xSpacingToBottom
            columnBottomY = panelDrawTopRightY + columnHeight

            self.__columnPrimitives.append(Line(
                        pt1=[columnTopX, columnTopY],
                        pt2=[columnBottomX, columnBottomY],
                        colour=(0, 0, 255), thickness=5, drawProportion=0, frameWidth=videoWidth,
                        frameHeight=videoHeight))
            if i < 10:
                msg = str(i)
            else:
                msg= "."
            self.__numberPrimitives.append(Text(text=msg, org=[columnTopX - columnWidth / 2, columnTopY-0.005], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.7,
                     colour=(255, 255, 255), drawProportion=0, progressiveDrawMode='enlarge',
                     insertCursorThickness=5,
                     frameWidth=videoWidth, frameHeight=videoHeight, drawOverElementsBehind=True))

        numberOfRows = 7
        rowWidth = 0.65
        rowHeight = 0.027
        interRowSpace = 0.025

        yOffset = 0.02
        ySpacingToLeft = 0.01




        for i in range(numberOfRows):
            rowRightX = panelDrawTopRightX
            rowRightY = panelDrawTopRightY + (rowHeight + interRowSpace) * i + yOffset

            rowLeftX = panelDrawTopRightX - rowWidth
            rowLeftY = rowRightY - ySpacingToLeft

            """
            if i == 0:
                self.__rowPrimitives.append(Line(
                    pt1=[rowRightX, rowRightY - interRowSpace / 2],
                    pt2=[rowLeftX, rowLeftY - interRowSpace / 2],
                    colour=(0, 0, 0), thickness=50, drawProportion=0, frameWidth=videoWidth,
                    frameHeight=videoHeight))
            """
            self.__rowPrimitives.append(Line(
                pt1=[rowRightX, rowRightY],
                pt2=[rowLeftX, rowLeftY],
                colour=(0, 0, 255), thickness=5, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight))

            self.__rowPrimitives.append(Line(
                pt1=[rowRightX, rowRightY + rowHeight],
                pt2=[rowLeftX, rowLeftY + rowHeight],
                colour=(0, 0, 255), thickness=5, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight))

            self.__rowPrimitives.append(Line(
                pt1=[rowRightX, rowRightY + rowHeight + interRowSpace/2],
                pt2=[rowLeftX, rowLeftY + rowHeight + interRowSpace/2],
                colour=(0, 0, 0), thickness=50, drawProportion=0, frameWidth=videoWidth,
                frameHeight=videoHeight))




    def drawInPanelImage(self, startTime, drawDuration, holdDuration):
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

        drawAnimation.addPrimitive(self.__panelImage)
        holdAnimation.addPrimitive(self.__panelImage)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInColumns(self, startTime, drawDuration, holdDuration):
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

        for primitive in self.__columnPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInRows(self, startTime, drawDuration, holdDuration):
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

        for primitive in self.__rowPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)


    def drawInNumbers(self, startTime, drawDuration, holdDuration):
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

        for primitive in self.__numberPrimitives:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)




videoWidth = int(3840)
videoHeight = int(2160)
fps = 30
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration,
                               outputFile='21.mp4')

panelVisuals = PanelVisuals(sceneAnimator=sceneAnimator, imagePath='../resources/side_on_panel.jpg', imageWidth=0.8, topLeftX=0.1, topLeftY=0.1, videoWidth=videoWidth, videoHeight=videoHeight, fps=fps)

panelVisuals.drawInPanelImage(startTime=0, drawDuration=2, holdDuration=videoDuration)
panelVisuals.drawInColumns(startTime=2, drawDuration=2, holdDuration=videoDuration)
panelVisuals.drawInRows(startTime=4, drawDuration=2, holdDuration=videoDuration)
panelVisuals.drawInNumbers(startTime=6, drawDuration=2, holdDuration=videoDuration)



sceneAnimator.renderAnimation()