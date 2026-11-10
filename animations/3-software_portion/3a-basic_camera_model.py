from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
import math

class CameraModel:
    def __init__(self, sceneAnimator, xTopLeft, yTopLeft, xAcross, yDown, numberOfPanelColumns, numberOfPanelRows, panelFrameHeight, apertureAngleFromHorizontal,apertureDistanceFromPlane, videoWidth, videoHeight, videoDuration, cameraImage=None, lineThroguhApertureLength=None, backgroundColour = (0, 0, 0), reverseLineThroughAperture = False):
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
        self.__lineThroughApertureLength = lineThroguhApertureLength
        self.__backgroundColour = backgroundColour
        self.__reverseLineThroughAperture = reverseLineThroughAperture

        self.__panelPrimitiveOutlineList = []
        self.__panelPrimitiveGridList = []
        self.__panelPrimitivePixelsGridList = []
        self.__lineThroughAperturePrimitiveList = []
        self.__aperturePrimitiveList = []

        self.__generateAperture()
        self.__generateSensorPanelOutlinePrimitives()
        self.__generateSensorPanelPixelsGridLines(numberOfColumns=numberOfPanelColumns, numberOfRows=numberOfPanelRows, cameraImage=cameraImage)


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

    def __generateSensorPanelPixelsGridLines(self, numberOfColumns, numberOfRows, cameraImage):
        topLength = math.sqrt(self.__xAcross ** 2 + self.__yDown** 2)
        columnWidth = topLength / numberOfColumns
        xAcrossColumn = columnWidth * (self.__xAcross / topLength)
        yDownColumn = columnWidth * (self.__yDown / topLength)

        # Columns
        for i in range(numberOfColumns):
            columnX = self.__xTopLeft + i * xAcrossColumn
            columnY = self.__yTopLeft + i * yDownColumn
            self.__panelPrimitiveGridList.append(Line(pt1=[columnX, columnY],
                                                      pt2=[columnX, columnY + self.__panelFrameHeight],
                                                      colour=(255, 255, 255), thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

        rowHeight = self.__panelFrameHeight / numberOfRows

        # Rows
        for i in range(numberOfRows):
            rowX = self.__xTopLeft
            rowY = self.__yTopLeft + i * rowHeight
            self.__panelPrimitiveGridList.append(Line(pt1=[rowX, rowY],
                                                      pt2=[rowX + self.__xAcross, rowY + self.__yDown],
                                                      colour=(255, 255, 255), thickness=5, drawProportion=0,
                                                      frameWidth=videoWidth, frameHeight=videoHeight))

        if cameraImage is None:
            return

        # Camera image and lines through aperture
        for i, row in enumerate(self.__cameraImage):
            for j, pixelValue in enumerate(row):

                if tuple(pixelValue) == self.__backgroundColour:
                    continue

                topLeftX = self.__xTopLeft + j * xAcrossColumn
                topLeftY = self.__yTopLeft + j * yDownColumn + i * rowHeight

                points = np.array([[topLeftX, topLeftY],
                                   [topLeftX + xAcrossColumn, topLeftY + yDownColumn],
                                   [topLeftX + xAcrossColumn, topLeftY + yDownColumn + rowHeight],
                                   [topLeftX, topLeftY + rowHeight]])



                self.__panelPrimitivePixelsGridList.append(FilledPolygon(pts=points,
                                                                         colour=pixelValue,
                                                                         frameWidth=videoWidth,
                                                                         frameHeight=videoHeight,
                                                                         drawProportion=0))

                pixelCenterX = topLeftX + xAcrossColumn / 2
                pixelCenterY = topLeftY + yDownColumn + rowHeight / 2


                oSub = self.__apertureY - pixelCenterY
                aSub = self.__apertureX - pixelCenterX
                hSub = math.sqrt((self.__apertureX - pixelCenterX)**2 + (self.__apertureY - pixelCenterY)**2)

                h = self.__lineThroughApertureLength
                o = h * (oSub/hSub)
                a = h * (aSub/hSub)

                endLineX = pixelCenterX + a
                endLineY = pixelCenterY + o

                pt1 = [endLineX, endLineY]
                pt2 = [pixelCenterX, pixelCenterY]
                if self.__reverseLineThroughAperture:
                    pt1 = [pixelCenterX, pixelCenterY]
                    pt2 = [endLineX, endLineY]


                self.__lineThroughAperturePrimitiveList.append(Line(pt1=pt1,
                                                      pt2=pt2,
                                                      colour=pixelValue, thickness=5, drawProportion=0,
                                                      frameWidth=videoWidth, frameHeight=videoHeight))

    def __generateAperture(self):
        panelCenterX = self.__xTopLeft + self.__xAcross/2
        panelCenterY = self.__yTopLeft + (self.__panelFrameHeight/2 + self.__panelFrameHeight/2 + self.__yDown)/2

        apetureXpixelDelta = self.__apertureDistanceFromPlane * math.cos(math.radians(self.__apertureAngleFromHorizontal))
        apetureYpixelDelta = self.__apertureDistanceFromPlane * math.sin(math.radians(self.__apertureAngleFromHorizontal))

        apetureX = panelCenterX + apetureXpixelDelta / self.__videoWidth
        apetureY = panelCenterY + apetureYpixelDelta / self.__videoHeight

        self.__apertureX = apetureX
        self.__apertureY = apetureY

        self.__aperturePrimitiveList.append(Ellipse(center=[apetureX, apetureY], axes=(5, 5), angle=0, startAngle=30, endAngle=390, colour=(0, 0, 255), thickness=5,
                drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight))

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

    def drawInLinesThroughAperture(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__lineThroughAperturePrimitiveList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        for primitive in self.__lineThroughAperturePrimitiveList:
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

class Stylus:
    def __init__(self, sceneAnimator, xBottomLeft, yBottomLeft, greenTipXLength, greenTipYLength, whiteHandleYLength, videoWidth, videoHeight):
        self.__sceneAnimator = sceneAnimator
        self.__xBottomLeft = xBottomLeft
        self.__yBottomLeft = yBottomLeft
        self.__greenTipXLength = greenTipXLength
        self.__greenTipYLength = greenTipYLength
        self.__whiteHandleYLength = whiteHandleYLength
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight

        self.__greenTipFull = FadeRectangle(
            pt1=[xBottomLeft, yBottomLeft - greenTipYLength],
            pt2=[xBottomLeft + greenTipXLength, yBottomLeft],
            colour=(0, 255, 0), frameWidth=videoWidth, frameHeight=videoHeight, thickness=5, lineType=cv2.LINE_8,
            drawProportion=0)

        self.__greenTipLeft = FadeRectangle(
            pt1=[xBottomLeft, yBottomLeft - greenTipYLength],
            pt2=[xBottomLeft + greenTipXLength / 2, yBottomLeft ],
            colour=(0, 255, 0), frameWidth=videoWidth, frameHeight=videoHeight, thickness=5, lineType=cv2.LINE_8, drawProportion=0)

        self.__greenTipRight = FadeRectangle(
            pt1=[xBottomLeft + greenTipXLength / 2, yBottomLeft - greenTipYLength],
            pt2=[xBottomLeft + greenTipXLength, yBottomLeft],
            colour=(0, 255, 0), frameWidth=videoWidth, frameHeight=videoHeight, thickness=5, lineType=cv2.LINE_8,
            drawProportion=0)

        self.__whiteHandle = FadeRectangle(
            pt1=[xBottomLeft, yBottomLeft - greenTipYLength - whiteHandleYLength],
            pt2=[xBottomLeft + greenTipXLength, yBottomLeft - greenTipYLength],
            colour=(255, 255, 255), frameWidth=videoWidth, frameHeight=videoHeight, thickness=1, lineType=cv2.LINE_8, drawProportion=0)

        self.__stylusHandleAndGreenTipPrimitiveList = [self.__whiteHandle, self.__greenTipFull]
        self.__stylusHandleLeftTipPrimitiveList = [self.__greenTipLeft]
        self.__stylusHandleRightTipPrimitiveList = [self.__greenTipRight]



    def drawInStylusTipAndHandle(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__stylusHandleAndGreenTipPrimitiveList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)

    def drawInStylusLeftTip(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__stylusHandleLeftTipPrimitiveList:
            drawAnimation.addPrimitive(primitive)
            holdAnimation.addPrimitive(primitive)

        self.__sceneAnimator.addPrimitiveAnimation(drawAnimation)
        self.__sceneAnimator.addPrimitiveAnimation(holdAnimation)


    def drawInStylusRightTip(self, startTime, drawDuration, holdDuration):
        drawAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=0, endDrawProportion=1, startTime=startTime,
                                           endTime=startTime + drawDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        holdAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0],
                                           startDrawProportion=1, endDrawProportion=1,
                                           startTime=startTime + drawDuration,
                                           endTime=startTime + drawDuration + holdDuration,
                                           fps=fps, frameWidth=self.__videoWidth, frameHeight=self.__videoHeight)

        for primitive in self.__stylusHandleRightTipPrimitiveList:
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
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [0,0,255], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
[[255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0], [255,0,0]],
               ]
cameraModel = CameraModel(sceneAnimator=sceneAnimator, xTopLeft=.2, yTopLeft=0.6, xAcross=0.1, yDown=0.1, numberOfPanelRows=7, numberOfPanelColumns=14, panelFrameHeight=0.2, apertureAngleFromHorizontal=-30, apertureDistanceFromPlane=400, videoWidth=videoWidth, videoHeight=videoHeight, videoDuration=videoDuration, cameraImage=cameraImage, lineThroguhApertureLength=.5, backgroundColour=(255, 0, 0), reverseLineThroughAperture=True)

stylus = Stylus(sceneAnimator=sceneAnimator, xBottomLeft=0.5, yBottomLeft=0.5, greenTipXLength=0.05, greenTipYLength=0.1, whiteHandleYLength=0.3, videoWidth=videoWidth, videoHeight=videoHeight)

stylus.drawInStylusTipAndHandle(startTime=0, drawDuration=2, holdDuration=videoDuration)
stylus.drawInStylusLeftTip(startTime=2.1, drawDuration=.1, holdDuration=videoDuration)
cameraModel.drawInLinesThroughAperture(startTime=0, drawDuration=8, holdDuration=1)
cameraModel.drawInPixels(startTime=4, drawDuration=1, holdDuration=videoDuration)
cameraModel.drawInAperture(startTime=0, drawDuration=1, holdDuration=videoDuration)
cameraModel.drawInSensorPanel(startTime=0, drawDuration=1, holdDuration=videoDuration)


stylus.drawInStylusRightTip(startTime=2.1, drawDuration=.1, holdDuration=videoDuration)





sceneAnimator.renderAnimation()