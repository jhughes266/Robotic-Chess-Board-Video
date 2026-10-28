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

class Rectangle(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, thickness, lineType, drawProportion):
        super().__init__(pt1, colour, drawProportion)

class Ellipse(PrimitiveElement):
    def __init__(self, center, axes, angle, startAngle, endAngle, colour, thickness, lineType, drawProportion):
        super().__init__(center, colour, drawProportion)

class Text(PrimitiveElement):
    def __init__(self, text, org, fontFace, fontScale, colour, thickness, lineType, drawProportion):
        super().__init__(org, colour, drawProportion)

class Image(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, thickness, lineType, drawProportion):
        super().__init__(pt1, colour, drawProportion)