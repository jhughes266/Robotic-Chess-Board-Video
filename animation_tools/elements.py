import math
import copy
import cv2
import numpy as np
from abc import ABC, abstractmethod

class PrimitiveElement:
    def __init__(self, position, colour, drawProportion, sampleFrame):
        self.position = self.toPixel(position, sampleFrame)
        self.colour = colour
        self.drawProportion = drawProportion

    def toPixel(self, position, frame):
        frameHeight, frameWidth = frame.shape[0], frame.shape[1]
        pixelPosition = [frameWidth * position[0], frameHeight * position[1]]
        return pixelPosition

    def updateDrawProportion(self, newProportion):
        self.drawProportion = min(max(newProportion, 0),1)

    @abstractmethod
    def draw(self, frame):
        pass

    @abstractmethod
    def updatePosition(sel, delta):
        pass

class Line(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, sampleFrame, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(pt1, colour, drawProportion, sampleFrame)
        self.pt2 = self.toPixel(pt2, sampleFrame)
        self.thickness = thickness
        self.lineType = lineType

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

        self.pt2[0]  += delta[0]
        self.pt2[1] += delta[1]

    def draw(self, frame):
        pt1 = copy.deepcopy(self.position)
        pt2 = copy.deepcopy(self.pt2)

        fullOpposite = pt2[0] - pt1[0]
        fullAdjacent = pt2[1] - pt1[1]
        fullHypotenuse = math.sqrt((fullOpposite) ** 2 + (fullAdjacent) ** 2)

        propHypotenuse = fullHypotenuse * self.drawProportion
        propOpposite = propHypotenuse * (fullOpposite / fullHypotenuse)
        propAdjacent = propHypotenuse * (fullAdjacent / fullHypotenuse)

        pt2[0] = pt1[0] + propOpposite
        pt2[1] = pt1[1] + propAdjacent

        cv2.line(img=frame,
                 pt1=(int(pt1[0]), int(pt1[1])),
                 pt2=(int(pt2[0]), int(pt2[1])),
                 color=self.colour,
                 thickness=self.thickness,
                 lineType=self.lineType)

class ArrowedLine(Line):
    def __init__(self, pt1, pt2, colour, sampleFrame, thickness=1, lineType=8, drawProportion=1):
        super().__init__(pt1=pt1, pt2=pt2, colour=colour, thickness=thickness, lineType=lineType, drawProportion=drawProportion, sampleFrame=sampleFrame)

    def draw(self, frame):
        pt1 = copy.deepcopy(self.position)
        pt2 = copy.deepcopy(self.pt2)

        fullOpposite = pt2[0] - pt1[0]
        fullAdjacent = pt2[1] - pt1[1]
        fullHypotenuse = math.sqrt((fullOpposite) ** 2 + (fullAdjacent) ** 2)

        propHypotenuse = fullHypotenuse * self.drawProportion
        propOpposite = propHypotenuse * (fullOpposite / fullHypotenuse)
        propAdjacent = propHypotenuse * (fullAdjacent / fullHypotenuse)

        pt2[0] = pt1[0] + propOpposite
        pt2[1] = pt1[1] + propAdjacent

        cv2.arrowedLine(img=frame,
                        pt1=(int(pt1[0]), int(pt1[1])),
                        pt2=(int(pt2[0]), int(pt2[1])),
                        color=self.colour,
                        thickness=self.thickness,
                        line_type=self.lineType)

class Rectangle(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, sampleFrame, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(pt1, colour, drawProportion, sampleFrame=sampleFrame)
        self.pt2 = self.toPixel(pt2, sampleFrame)
        self.thickness = thickness
        self.lineType = lineType

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

        self.pt2[0]  += delta[0]
        self.pt2[1] += delta[1]

    def draw(self, frame):
        pt1 = self.position
        pt2 = self.pt2

        perimeterLength = 2 * (pt2[0] - pt1[0] + pt2[1] - pt1[1])

        line1Length = pt2[0] - pt1[0]
        line2Length = pt2[1] - pt1[1]
        line3Length = line1Length
        line4Length = line2Length

        propPerimeterLength = perimeterLength * self.drawProportion
        remainingPropPerimeterLength = propPerimeterLength

        if (remainingPropPerimeterLength >= 0):

            cv2.line(img=frame,
                     pt1=(int(pt1[0]), int(pt1[1])),
                     pt2=(int(pt1[0] + min(remainingPropPerimeterLength, line1Length)), int(pt1[1])),
                     color=self.colour,
                     thickness=self.thickness,
                     lineType=self.lineType)

            remainingPropPerimeterLength -= line1Length

        if (remainingPropPerimeterLength >= 0):
            cv2.line(img=frame,
                     pt1=(int(pt2[0]), int(pt1[1])),
                     pt2=(int(pt2[0]), int(pt1[1] + min(remainingPropPerimeterLength, line2Length))),
                     color=self.colour,
                     thickness=self.thickness,
                     lineType=self.lineType)

            remainingPropPerimeterLength -= line2Length

        if (remainingPropPerimeterLength >= 0):
            cv2.line(img=frame,
                     pt1=(int(pt2[0]), int(pt2[1])),
                     pt2=(int(pt2[0] - min(remainingPropPerimeterLength, line3Length)), int(pt2[1])),
                     color=self.colour,
                     thickness=self.thickness,
                     lineType=self.lineType)

            remainingPropPerimeterLength -= line3Length

        if (remainingPropPerimeterLength >= 0):
            cv2.line(img=frame,
                     pt1=(int(pt1[0]), int(pt2[1])),
                     pt2=(int(pt1[0]), int(pt2[1] - min(remainingPropPerimeterLength, line4Length))),
                     color=self.colour,
                     thickness=self.thickness,
                     lineType=self.lineType)

class Ellipse(PrimitiveElement):
    def __init__(self, center, axes, angle, startAngle, endAngle, colour, sampleFrame, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(center, colour, drawProportion, sampleFrame=sampleFrame)
        self.axes = axes
        self.angle = angle
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.thickness = thickness
        self.lineType = lineType

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

    def draw(self, frame):
        centre = self.position

        totalAngle = self.endAngle - self.startAngle
        propAngle = totalAngle * self.drawProportion
        newAngle = self.startAngle + propAngle
        cv2.ellipse(img=frame,
                    center=(int(centre[0]), int(centre[1])),
                    axes=self.axes,
                    angle=self.angle,
                    startAngle=self.startAngle,
                    endAngle=newAngle,
                    color=self.colour,
                    thickness=self.thickness,
                    lineType=self.lineType)

class Text(PrimitiveElement):
    def __init__(self, text, org, fontFace, fontScale, colour, sampleFrame,  backgroundColour=(0,0,0), thickness=1, lineType=cv2.LINE_8, drawProportion=1, progressiveDrawMode='enlarge', insertCursorThickness=1):
        super().__init__(org, colour, drawProportion, sampleFrame=sampleFrame)
        self.text = text
        self.fontFace = fontFace
        self.fontScale = fontScale
        self.backgroundColour = backgroundColour
        self.thickness = thickness
        self.lineType = lineType
        self.progressiveDrawMode = progressiveDrawMode
        self.insertCursorThickness = insertCursorThickness

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

    def draw(self, frame):
        org = copy.deepcopy(self.position)
        if self.progressiveDrawMode == 'enlarge':

            propScale = self.fontScale * self.drawProportion

            retVal, baseLine = cv2.getTextSize(self.text, fontFace=self.fontFace, fontScale=propScale, thickness=self.thickness)
            textWidth, textHeight = retVal[0], retVal[1]

            org[0] -= textWidth / 2
            org[1] -= textHeight / 2

            cv2.putText(img=frame,
                        text=self.text,
                        org=(int(org[0]), int(org[1])),
                        fontFace=self.fontFace,
                        fontScale=propScale,
                        color=self.colour,
                        thickness=self.thickness,
                        lineType=self.lineType
                        )
        elif self.progressiveDrawMode == 'letterByLetter':
            retVal, baseLine = cv2.getTextSize(self.text, fontFace=self.fontFace, fontScale=self.fontScale, thickness=self.thickness)
            textWidth, textHeight = retVal[0], retVal[1]

            pixelsRevealed = textWidth * self.drawProportion
            pixelsHidden = textWidth - pixelsRevealed

            cv2.putText(img=frame,
                        text=self.text,
                        org=(int(org[0]), int(org[1])),
                        fontFace=self.fontFace,
                        fontScale=self.fontScale,
                        color=self.colour,
                        thickness=self.thickness,
                        lineType=self.lineType
                        )

            cv2.rectangle(img=frame,
                          pt1=(int(org[0] + pixelsRevealed), int(org[1] - textHeight)),
                          pt2=(int(org[0] + pixelsRevealed + self.insertCursorThickness), int(org[1])),
                          color=self.colour,
                          thickness=-1,
                          lineType=self.lineType)

            cv2.rectangle(img=frame,
                          pt1=(int(org[0] + pixelsRevealed + self.insertCursorThickness + 1), int(org[1] - textHeight)),
                          pt2=(int(org[0] + textWidth), int(org[1])),
                          color=self.backgroundColour,
                          thickness=-1,
                          lineType=self.lineType)


class Image(PrimitiveElement):
    def __init__(self, topLeft, imgPath, imageWidth, sampleFrame, colour=None, backgroundColour=(0,0,0), drawProportion=1, maxNumBlurs = 1):
        super().__init__(topLeft, colour, drawProportion, sampleFrame=sampleFrame)
        self.imgPath = imgPath
        self.image = cv2.imread(imgPath)
        self.imageWidth = imageWidth
        self.backgroundColour = backgroundColour
        self.maxNumBlurs = maxNumBlurs

    def updatePosition(self, delta):
        # x, y switch because of slicing
        self.position[1] += delta[0]
        self.position[0] += delta[1]

    def draw(self, frame):
        topLeft = self.position

        newPixelWidth = int(frame.shape[1] * self.imageWidth)
        oldPixelWidth = self.image.shape[1]
        newPixelHeight = int((newPixelWidth / oldPixelWidth) * self.image.shape[0])

        newImage = cv2.resize(self.image, (newPixelWidth, newPixelHeight))

        for i in range(int(self.maxNumBlurs - self.drawProportion * self.maxNumBlurs)):
            newImage = cv2.blur(newImage, (10,10))

        frameDrawSection = frame[int(topLeft[0]) : (int(topLeft[0]) + newPixelHeight), int(topLeft[1]) : (int(topLeft[1]) + newPixelWidth)]

        difference = newImage - frameDrawSection

        propDifference = difference * self.drawProportion

        propNewImage = propDifference + frameDrawSection

        frame[int(topLeft[0]): (int(topLeft[0]) + newPixelHeight), int(topLeft[1]): (int(topLeft[1]) + newPixelWidth)] = propNewImage


