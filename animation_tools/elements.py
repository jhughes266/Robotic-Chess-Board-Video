import math
import copy
import cv2
import numpy as np
from abc import ABC, abstractmethod

class PrimitiveElement:
    def __init__(self, position, colour, drawProportion, frameWidth, frameHeight):
        self._frameWidth = frameWidth
        self._frameHeight = frameHeight
        self._position = self._toPixel(position)
        self._colour = colour
        self._drawProportion = drawProportion

    def _toPixel(self, position):
        pixelPosition = [self._frameWidth * position[0], self._frameHeight * position[1]]
        return pixelPosition

    def updateDrawProportion(self, delta):
        self._drawProportion += delta
        self._drawProportion = min(max(self._drawProportion, 0), 1)
        # Deal with any proportions that are close very close to zero
        if self._drawProportion < 0.000001:
            self._drawProportion = 0

    @abstractmethod
    def draw(self, frame):
        pass

    @abstractmethod
    def updatePosition(sel, delta):
        pass

class Line(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, frameWidth, frameHeight, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(position=pt1, colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self._pt2 = self._toPixel(pt2)
        self._thickness = thickness
        self._lineType = lineType

    def updatePosition(self, delta):
        self._position[0] += delta[0]
        self._position[1] += delta[1]

        self._pt2[0]  += delta[0]
        self._pt2[1] += delta[1]

    def draw(self, frame):
        if self._drawProportion == 0:
            return
        pt1 = copy.deepcopy(self._position)
        pt2 = copy.deepcopy(self._pt2)

        fullOpposite = pt2[0] - pt1[0]
        fullAdjacent = pt2[1] - pt1[1]
        fullHypotenuse = math.sqrt((fullOpposite) ** 2 + (fullAdjacent) ** 2)

        propHypotenuse = fullHypotenuse * self._drawProportion
        propOpposite = propHypotenuse * (fullOpposite / fullHypotenuse)
        propAdjacent = propHypotenuse * (fullAdjacent / fullHypotenuse)

        pt2[0] = pt1[0] + propOpposite
        pt2[1] = pt1[1] + propAdjacent

        cv2.line(img=frame,
                 pt1=(int(pt1[0]), int(pt1[1])),
                 pt2=(int(pt2[0]), int(pt2[1])),
                 color=self._colour,
                 thickness=self._thickness,
                 lineType=self._lineType)

class FilledPolygon(PrimitiveElement):
    def __init__(self, pts, colour, frameWidth, frameHeight, backgroundColour = (0,0,0), drawProportion=1):
        super().__init__(position=pts[0], colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self.__pts = []
        self.__backgroundColour = backgroundColour
        for i, pt in enumerate(pts):
            self.__pts.append(self._toPixel([float(pt[0]), float(pt[1])]))

        self.__pts = np.array(self.__pts, dtype=np.int64)


    def updatePosition(self, delta):
        for pt in self.__pts:
            pt[0] += delta[0]
            pt[1] += delta[1]



    def draw(self, frame):
        if self._drawProportion == 0:
            return
        colourDif = np.array(self._colour) - np.array(self.__backgroundColour)
        colourDrawProp = colourDif * self._drawProportion
        currentColour = tuple(np.array(self.__backgroundColour) + colourDrawProp)
        currentColour = (int(currentColour[0]), int(currentColour[1]), int(currentColour[2]))
        cv2.fillPoly(img=frame, pts=[self.__pts], color=currentColour)

class ArrowedLine(Line):
    def __init__(self, pt1, pt2, colour, frameWidth, frameHeight, thickness=1, lineType=8, drawProportion=1):
        super().__init__(pt1=pt1, pt2=pt2, colour=colour, thickness=thickness, lineType=lineType, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)

    def draw(self, frame):
        if self._drawProportion == 0:
            return
        pt1 = copy.deepcopy(self._position)
        pt2 = copy.deepcopy(self._pt2)

        fullOpposite = pt2[0] - pt1[0]
        fullAdjacent = pt2[1] - pt1[1]
        fullHypotenuse = math.sqrt((fullOpposite) ** 2 + (fullAdjacent) ** 2)

        propHypotenuse = fullHypotenuse * self._drawProportion
        propOpposite = propHypotenuse * (fullOpposite / fullHypotenuse)
        propAdjacent = propHypotenuse * (fullAdjacent / fullHypotenuse)

        pt2[0] = pt1[0] + propOpposite
        pt2[1] = pt1[1] + propAdjacent

        cv2.arrowedLine(img=frame,
                        pt1=(int(pt1[0]), int(pt1[1])),
                        pt2=(int(pt2[0]), int(pt2[1])),
                        color=self._colour,
                        thickness=self._thickness,
                        line_type=self._lineType)

class Rectangle(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, frameWidth, frameHeight, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(position=pt1, colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self.__pt2 = self._toPixel(pt2)
        self.__thickness = thickness
        self.__lineType = lineType

    def updatePosition(self, delta):
        self._position[0] += delta[0]
        self._position[1] += delta[1]

        self.__pt2[0]  += delta[0]
        self.__pt2[1] += delta[1]

    def draw(self, frame):
        if self._drawProportion == 0:
            return
        pt1 = self._position
        pt2 = self.__pt2

        perimeterLength = 2 * (pt2[0] - pt1[0] + pt2[1] - pt1[1])

        line1Length = pt2[0] - pt1[0]
        line2Length = pt2[1] - pt1[1]
        line3Length = line1Length
        line4Length = line2Length

        propPerimeterLength = perimeterLength * self._drawProportion
        remainingPropPerimeterLength = propPerimeterLength

        if self.__thickness < 0:
            cv2.rectangle(img=frame,
                          pt1=(int(pt1[0]), int(pt1[1])),
                          pt2=(int(pt2[0]), int(pt2[1])),
                          color=self._colour,
                          thickness=self.__thickness,
                          lineType=self.__lineType)
            return

        if (remainingPropPerimeterLength >= 0):

            cv2.line(img=frame,
                     pt1=(int(pt1[0]), int(pt1[1])),
                     pt2=(int(pt1[0] + min(remainingPropPerimeterLength, line1Length)), int(pt1[1])),
                     color=self._colour,
                     thickness=self.__thickness,
                     lineType=self.__lineType)

            remainingPropPerimeterLength -= line1Length

        if (remainingPropPerimeterLength >= 0):
            cv2.line(img=frame,
                     pt1=(int(pt2[0]), int(pt1[1])),
                     pt2=(int(pt2[0]), int(pt1[1] + min(remainingPropPerimeterLength, line2Length))),
                     color=self._colour,
                     thickness=self.__thickness,
                     lineType=self.__lineType)

            remainingPropPerimeterLength -= line2Length

        if (remainingPropPerimeterLength >= 0):
            cv2.line(img=frame,
                     pt1=(int(pt2[0]), int(pt2[1])),
                     pt2=(int(pt2[0] - min(remainingPropPerimeterLength, line3Length)), int(pt2[1])),
                     color=self._colour,
                     thickness=self.__thickness,
                     lineType=self.__lineType)

            remainingPropPerimeterLength -= line3Length

        if (remainingPropPerimeterLength >= 0):
            cv2.line(img=frame,
                     pt1=(int(pt1[0]), int(pt2[1])),
                     pt2=(int(pt1[0]), int(pt2[1] - min(remainingPropPerimeterLength, line4Length))),
                     color=self._colour,
                     thickness=self.__thickness,
                     lineType=self.__lineType)


class FadeRectangle(PrimitiveElement):
    def __init__(self, pt1, pt2, colour, frameWidth, frameHeight, thickness=1, lineType=cv2.LINE_8, drawProportion=1, backgroundColour = (0,0,0)):
        super().__init__(position=pt1, colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self.__pt2 = self._toPixel(pt2)
        self.__thickness = thickness
        self.__lineType = lineType
        self.__backgroundColour = backgroundColour

    def updatePosition(self, delta):
        self._position[0] += delta[0]
        self._position[1] += delta[1]

        self.__pt2[0]  += delta[0]
        self.__pt2[1] += delta[1]

    def draw(self, frame):
        pt1 = self._position
        pt2 = self.__pt2
        if self._drawProportion  <= 0.5:
            tempDrawProportion = self._drawProportion / 0.5
            colourDiff = np.array(self._colour) - np.array(self.__backgroundColour)
            currentColour = tuple(np.array(self.__backgroundColour) + tempDrawProportion * colourDiff)
            cv2.rectangle(img=frame,
                          pt1=(int(pt1[0]), int(pt1[1])),
                          pt2=(int(pt2[0]), int(pt2[1])),
                          color=currentColour,
                          thickness=self.__thickness,
                          lineType=self.__lineType)
        else:
            tempDrawProportion = (self._drawProportion - 0.5) / 0.5
            colourDiff = np.array(self._colour) - np.array(self.__backgroundColour)
            currentColour = tuple(np.array(self.__backgroundColour) + tempDrawProportion * colourDiff)
            # Outline
            cv2.rectangle(img=frame,
                          pt1=(int(pt1[0]), int(pt1[1])),
                          pt2=(int(pt2[0]), int(pt2[1])),
                          color=currentColour,
                          thickness=-self.__thickness,
                          lineType=self.__lineType)

            cv2.rectangle(img=frame,
                          pt1=(int(pt1[0]), int(pt1[1])),
                          pt2=(int(pt2[0]), int(pt2[1])),
                          color=self._colour,
                          thickness=self.__thickness,
                          lineType=self.__lineType)



class Ellipse(PrimitiveElement):
    def __init__(self, center, axes, angle, startAngle, endAngle, colour, frameWidth, frameHeight, thickness=1, lineType=cv2.LINE_8, drawProportion=1):
        super().__init__(position=center, colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self.__axes = axes
        self.__angle = angle
        self.__startAngle = startAngle
        self.__endAngle = endAngle
        self.__thickness = thickness
        self.__lineType = lineType

    def updatePosition(self, delta):
        self._position[0] += delta[0]
        self._position[1] += delta[1]

    def draw(self, frame):
        if self._drawProportion == 0:
            return
        centre = self._position

        totalAngle = self.__endAngle - self.__startAngle
        propAngle = totalAngle * self._drawProportion
        newAngle = self.__startAngle + propAngle
        cv2.ellipse(img=frame,
                    center=(int(centre[0]), int(centre[1])),
                    axes=self.__axes,
                    angle=self.__angle,
                    startAngle=self.__startAngle,
                    endAngle=newAngle,
                    color=self._colour,
                    thickness=self.__thickness,
                    lineType=self.__lineType)

class Text(PrimitiveElement):
    def __init__(self, text, org, fontFace, fontScale, colour, frameWidth, frameHeight,  backgroundColour=(0,0,0), thickness=1, lineType=cv2.LINE_8, drawProportion=1, progressiveDrawMode='enlarge', insertCursorThickness=1):
        super().__init__(position=org,colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self.__text = text
        self.__fontFace = fontFace
        self.__fontScale = fontScale
        self.__backgroundColour = backgroundColour
        self.__thickness = thickness
        self.__lineType = lineType
        self.__progressiveDrawMode = progressiveDrawMode
        self.__insertCursorThickness = insertCursorThickness

    def updatePosition(self, delta):
        self._position[0] += delta[0]
        self._position[1] += delta[1]

    def draw(self, frame):
        if self._drawProportion == 0:
            return
        org = copy.deepcopy(self._position)
        if self.__progressiveDrawMode == 'enlarge':

            propScale = self.__fontScale * self._drawProportion

            retVal, baseLine = cv2.getTextSize(self.__text, fontFace=self.__fontFace, fontScale=propScale, thickness=self.__thickness)
            textWidth, textHeight = retVal[0], retVal[1]

            org[0] -= textWidth / 2
            org[1] += textHeight / 2

            cv2.putText(img=frame,
                        text=self.__text,
                        org=(int(org[0]), int(org[1])),
                        fontFace=self.__fontFace,
                        fontScale=propScale,
                        color=self._colour,
                        thickness=self.__thickness,
                        lineType=self.__lineType
                        )
        elif self.__progressiveDrawMode == 'letterByLetter':
            retVal, baseLine = cv2.getTextSize(self.__text, fontFace=self.__fontFace, fontScale=self.__fontScale, thickness=self.__thickness)
            textWidth, textHeight = retVal[0], retVal[1]

            pixelsRevealed = textWidth * self._drawProportion
            pixelsHidden = textWidth - pixelsRevealed

            org[0] -= textWidth / 2
            org[1] += textHeight / 2

            cv2.putText(img=frame,
                        text=self.__text,
                        org=(int(org[0]), int(org[1])),
                        fontFace=self.__fontFace,
                        fontScale=self.__fontScale,
                        color=self._colour,
                        thickness=self.__thickness,
                        lineType=self.__lineType
                        )

            cv2.rectangle(img=frame,
                          pt1=(int(org[0] + pixelsRevealed), int(org[1] - textHeight)),
                          pt2=(int(org[0] + pixelsRevealed + self.__insertCursorThickness), int(org[1])),
                          color=self._colour,
                          thickness=-1,
                          lineType=self.__lineType)

            cv2.rectangle(img=frame,
                          pt1=(int(org[0] + pixelsRevealed + self.__insertCursorThickness + 1), int(org[1] - textHeight)),
                          pt2=(int(org[0] + textWidth), int(org[1] + 0.3 * textHeight)),
                          color=self.__backgroundColour,
                          thickness=-1,
                          lineType=self.__lineType)


class Image(PrimitiveElement):
    def __init__(self, topLeft, imgPath, imageWidth, frameWidth, frameHeight, colour=None, backgroundColour=(0,0,0), drawProportion=1, maxNumBlurs = 1, onlyKeepMonoChrome = False):
        super().__init__(position=topLeft,colour=colour, drawProportion=drawProportion, frameWidth=frameWidth, frameHeight=frameHeight)
        self.__imgPath = imgPath
        self.__image = cv2.imread(imgPath)
        self.__imageWidth = imageWidth
        self.__backgroundColour = backgroundColour
        self.__maxNumBlurs = maxNumBlurs
        self.__onlyKeepMonoChrome = onlyKeepMonoChrome

    def updatePosition(self, delta):
        # x, y switch because of slicing
        self._position[1] += delta[1]
        self._position[0] += delta[0]

    def draw(self, frame):
        if self._drawProportion == 0:
            return

        topLeft = self._position

        newPixelWidth = int(frame.shape[1] * self.__imageWidth)
        oldPixelWidth = self.__image.shape[1]
        newPixelHeight = int((newPixelWidth / oldPixelWidth) * self.__image.shape[0])

        newImage = cv2.resize(self.__image, (newPixelWidth, newPixelHeight))

        frameDrawSection = frame[int(topLeft[1]): (int(topLeft[1]) + newPixelHeight), int(topLeft[0]): (int(topLeft[0]) + newPixelWidth)]

        if self.__onlyKeepMonoChrome:
            #location of the black and white pixels
            whiteMask = np.where(np.sum(np.where(newImage == 255, 1, 0), axis=2) == 3, 1, 0)
            blackMask = np.where(np.sum(np.where(newImage == 0, 1, 0), axis=2) == 3, 1, 0)
            # sum masks any element that equals 1 corresponds to a black pixel
            totalMask = blackMask + whiteMask
            # create a 3d mask with each channel identical. It means any element that is 1 we want to keep and any that
            # is zero becomes the backgroun
            totalMask3d = np.ones_like(newImage)
            totalMask3d[:,:, 0] = totalMask
            totalMask3d[:, :, 1] = totalMask
            totalMask3d[:, :, 2] = totalMask
            # any element that is included and any that is zero becomes the background
            newImage = np.where(totalMask3d == 1, newImage * self._drawProportion, frameDrawSection)

        difference = newImage - frameDrawSection

        propDifference = difference * self._drawProportion

        propNewImage = propDifference + frameDrawSection

        for i in range(int(self.__maxNumBlurs - self._drawProportion * self.__maxNumBlurs)):
            propNewImage = cv2.blur(propNewImage, (10,10))


        frame[int(topLeft[1]): (int(topLeft[1]) + newPixelHeight), int(topLeft[0]): (int(topLeft[0]) + newPixelWidth)] = propNewImage



