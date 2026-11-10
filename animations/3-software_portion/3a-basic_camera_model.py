from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math

class CameraModel:
    def __init__(self, sceneAnimator, xTopLeft, yTopLeft, xAcross, yDown, numberOfPanelColumns, numberOfPanelRows, panelFrameHeight, apertureAngleFromHorizontal,apertureDistanceFromPlane, videoWidth, videoHeight, videoDuration, cameraImage=None):
        self.__sceneAnimator = sceneAnimator
        self.__xTopLeft = xTopLeft
        self.__yTopLeft = yTopLeft
        self.__xAcross = xAcross
        self.__yDown = yDown
        self.__panelFrameHeight = panelFrameHeight
        self.__apertureAngleFromHorizontal = apertureAngleFromHorizontal
        self.__apertureDistanceFromPlane = apertureDistanceFromPlane
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__videoDuration = videoDuration
        self.__cameraImage = cameraImage

        self.__panelPrimitiveOutlineList = []
        self.__panelPrimitiveGridList = []
        self.__panelPrimitivePixelsGridList = []
        self.__aperturePrimitiveList = []

        self.__generateSensorPanelOutlinePrimitives()
        self.__generateSensorPanelPixelsGrid(numberOfColumns=numberOfPanelColumns, numberOfRows=numberOfPanelRows, cameraImage=cameraImage)
        self.__generateAperture()

    def __generateSensorPanelOutlinePrimitives(self):
        self.__panelPrimitiveOutlineList.append(Line(pt1=[self.__xTopLeft, self.__yTopLeft],
                       pt2=[self.__xTopLeft + self.__xAcross, self.__yTopLeft + self.__yDown],
                       colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

        self.__panelPrimitiveOutlineList.append(Line(pt1=[self.__xTopLeft, self.__yTopLeft],
                                                     pt2=[self.__xTopLeft, self.__yTopLeft + self.__panelFrameHeight],
                                                     colour=(255, 255, 255), thickness=5, drawProportion=0,
                                                     frameWidth=videoWidth, frameHeight=videoHeight))

        self.__panelPrimitiveOutlineList.append(Line(pt1=[self.__xTopLeft, self.__yTopLeft + self.__panelFrameHeight],
                                                     pt2=[self.__xTopLeft + self.__xAcross, self.__yTopLeft + self.__panelFrameHeight + self.__yDown],
                                                     colour=(255, 255, 255), thickness=5, drawProportion=0,
                                                     frameWidth=videoWidth, frameHeight=videoHeight))

        self.__panelPrimitiveOutlineList.append(Line(pt1=[self.__xTopLeft + self.__xAcross, self.__yTopLeft + self.__yDown],
                                                     pt2=[self.__xTopLeft + self.__xAcross,
                                                          self.__yTopLeft + self.__panelFrameHeight + self.__yDown],
                                                     colour=(255, 255, 255), thickness=5, drawProportion=0,
                                                     frameWidth=videoWidth, frameHeight=videoHeight))

    def __generateSensorPanelPixelsGrid(self, numberOfColumns, numberOfRows, cameraImage):
        topLength = math.sqrt(self.__xAcross ** 2 + self.__yDown** 2)
        columnWidth = topLength / numberOfColumns
        xAcrossColumn = columnWidth * (self.__xAcross / topLength)
        yDownColumn = columnWidth * (self.__yDown / topLength)

        for i in range(numberOfColumns):
            columnX = self.__xTopLeft + i * xAcrossColumn
            columnY = self.__yTopLeft + i * yDownColumn
            self.__panelPrimitiveGridList.append(Line(pt1=[columnX, columnY],
                                                      pt2=[columnX, columnY + self.__panelFrameHeight],
                                                      colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

        rowHeight = self.__panelFrameHeight / numberOfRows

        for i in range(numberOfRows):
            rowX = self.__xTopLeft
            rowY = self.__yTopLeft + i * rowHeight
            self.__panelPrimitiveGridList.append(Line(pt1=[rowX, rowY],
                                                      pt2=[rowX + self.__xAcross, rowY + self.__yDown],
                                                      colour=(255, 255, 255), thickness=5, drawProportion=0,
                                                      frameWidth=videoWidth, frameHeight=videoHeight))

        if cameraImage is None:
            return

        for i, row in enumerate(self.__cameraImage):
            for j, pixelValue in enumerate(row):
                topLeftX = self.__xTopLeft + j * xAcrossColumn
                topLeftY = self.__yTopLeft + j * yDownColumn + i * rowHeight

                points = np.array([[topLeftX, topLeftY],
                                   [topLeftX + xAcrossColumn, topLeftY + yDownColumn],
                                   [topLeftX + xAcrossColumn, topLeftY + yDownColumn + rowHeight],
                                   [topLeftX, topLeftY + rowHeight]])

                pixelCenterX = topLeftX + xAcrossColumn/2
                pixelCenterY = topLeftY + yDownColumn + rowHeight/2

                self.__panelPrimitivePixelsGridList.append(FilledPolygon(pts=points,
                                                                         colour=pixelValue,
                                                                         frameWidth=videoWidth,
                                                                         frameHeight=videoHeight,
                                                                         drawProportion=0))

                self.__panelPrimitivePixelsGridList.append(Ellipse(center=[pixelCenterX, pixelCenterY], axes=(1, 1), angle=0, startAngle=30, endAngle=390, colour=(255, 255, 255), thickness=5,
                drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

    def __generateAperture(self):
        panelCenterX = self.__xTopLeft + self.__xAcross/2
        panelCenterY = self.__yTopLeft + (self.__panelFrameHeight/2 + self.__panelFrameHeight/2 + self.__yDown)/2

        appetureXpixelDelta = self.__apertureDistanceFromPlane * math.cos(math.radians(self.__apertureAngleFromHorizontal))
        appetureYpixelDelta = self.__apertureDistanceFromPlane * math.sin(math.radians(self.__apertureAngleFromHorizontal))

        appetureX = panelCenterX + appetureXpixelDelta / self.__videoWidth
        appetureY = panelCenterY + appetureYpixelDelta / self.__videoHeight
        self.__aperturePrimitiveList.append(Ellipse(center=[appetureX, appetureY], axes=(5, 5), angle=0, startAngle=30, endAngle=390, colour=(0, 0, 255), thickness=5,
                drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

        self.__aperturePrimitiveList.append(Line(pt1=[panelCenterX, panelCenterY],
             pt2=[appetureX, appetureY],
             colour=(255, 255, 255), thickness=5, drawProportion=0,
             frameWidth=videoWidth, frameHeight=videoHeight))

    def drawInSensorPanel(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__panelPrimitiveOutlineList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        for primitive in self.__panelPrimitiveGridList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInPixels(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__panelPrimitivePixelsGridList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        for primitive in self.__panelPrimitivePixelsGridList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInAperture(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__aperturePrimitiveList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)


        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)






videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='3a-basic_camera_model.mp4')
cameraImage = [[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [0,255,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
               ]
cameraModel = CameraModel(sceneAnimator=sceneAnimator, xTopLeft=.4, yTopLeft=0.2, xAcross=0.1, yDown=0.1, numberOfPanelRows=7, numberOfPanelColumns=14, panelFrameHeight=0.2, apertureAngleFromHorizontal=-30, apertureDistanceFromPlane=400, videoWidth=videoWidth, videoHeight=videoHeight, videoDuration=videoDuration, cameraImage=cameraImage)

cameraModel.drawInAperture(startTime=0, drawDuration=1, holdDuration=videoDuration)
cameraModel.drawInPixels(startTime=1, drawDuration=1, holdDuration=videoDuration)
cameraModel.drawInSensorPanel(startTime=0, drawDuration=1, holdDuration=videoDuration)






sceneAnimator.renderAnimation()