import math

import cv2
import numpy as np
from abc import ABC, abstractmethod

class PrimitiveElement:
    def __init__(self, position, colour, drawProportion):
        self.position = position
        self.colour = colour
        self.drawProportion = drawProportion

    def toPixel(self, position, frame):
        frameHeight, frameWidth = frame.shape[0], frame.shape[1]
        pixelPosition = [frameWidth * position[0], frameHeight * position[1]]
        return pixelPosition

    @abstractmethod
    def draw(self, frame):
        pass

    @abstractmethod
    def updatePosition(sel, delta):
        pass

class Line(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(pt1, colour, drawProportion)
        self.pt2 = pt2
        self.thickness = thickness
        self.lineType = lineType

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

        self.pt2[0]  += delta[0]
        self.pt2[1] += delta[1]

    def draw(self, frame):
        pt1 = self.toPixel(self.position, frame)
        pt2 = self.toPixel(self.pt2, frame)

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
    def __init__(self, pt1, pt2, colour, thickness=1, lineType=8, drawProportion=1):
        super().__init__(pt1=pt1, pt2=pt2, colour=colour, thickness=thickness, lineType=lineType, drawProportion=drawProportion)

    def draw(self, frame):
        pt1 = self.toPixel(self.position, frame)
        pt2 = self.toPixel(self.pt2, frame)

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
    def __init__(self, pt1, pt2, colour, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(pt1, colour, drawProportion)
        self.pt2 = pt2
        self.thickness = thickness
        self.lineType = lineType

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

        self.pt2[0]  += delta[0]
        self.pt2[1] += delta[1]

    def draw(self, frame):

        pt1 = self.toPixel(self.position, frame)
        pt2 = self.toPixel(self.pt2, frame)

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
    def __init__(self, center, axes, angle, startAngle, endAngle, colour, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(center, colour, drawProportion)
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
        centre = self.toPixel(self.position, frame)

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
    def __init__(self, text, org, fontFace, fontScale, colour, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(org, colour, drawProportion)
        self.text = text
        self.fontFace = fontFace
        self.fontScale = fontScale
        self.thickness = thickness
        self.lineType = lineType

    def updatePosition(self, delta):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

    def draw(self, frame):
        org = self.toPixel(self.position, frame)

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

class Image(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, thickness, lineType, drawProportion):
        super().__init__(pt1, colour, drawProportion)