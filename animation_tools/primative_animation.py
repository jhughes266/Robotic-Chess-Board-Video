import math


class PrimitiveAnimation:
    def __init__(self, startLocation, endLocation, startDrawProportion, endDrawProportion, startTime, endTime, fps, frameWidth, frameHeight):
        self.__primitiveList = []
        self.__startLocation = startLocation
        self.__endLocation = endLocation
        self.__startDrawProportion = startDrawProportion
        self.__endDrawProportion = endDrawProportion
        self.__startTime = startTime
        self.__duration = endTime - startTime
        self.__fps = fps
        self.__frameWidth = frameWidth
        self.__frameHeight = frameHeight
        self.__frameNumber = 0
        self.__pixelDelta = self.__determinepixelDelta()
        self.__drawPropDelta = self.__determineDrawProportionDelta()

    def addPrimitive(self, primitive):
        self.__primitiveList.append(primitive)

    def __toPixel(self, position):
        pixelPosition = [self.__frameWidth * position[0], self.__frameHeight * position[1]]
        return pixelPosition

    def __determinepixelDelta(self):
        startLocation = self.__toPixel(self.__startLocation)
        endLocation = self.__toPixel(self.__endLocation)
        A = endLocation[0] - startLocation[0]
        O = endLocation[1] - startLocation[1]
        H = math.sqrt((A) ** 2 + (O) ** 2)
        if H == 0:
            delta = [0,0]
            return delta
        numFramesInAnimation = self.__fps * self.__duration
        # Need to minus 1 as there is 1 less updates then there is frames in the animation.
        numDeltas = numFramesInAnimation - 1
        deltaLength = H / numDeltas
        xDelta = deltaLength * (A / H)
        yDetla = deltaLength * (O / H)
        delta = [xDelta, yDetla]
        return delta

    def __determineDrawProportionDelta(self):
        numFramesInAnimation = self.__fps * self.__duration
        # Need to minus 1 as there is 1 less updates then there is frames in the animation.
        numDeltas = numFramesInAnimation - 1
        drawPropDif = self.__endDrawProportion - self.__startDrawProportion
        delta = drawPropDif / numDeltas
        return delta


    def draw(self, frame):
        timeStamp = (self.__frameNumber)/self.__fps
        for primitive in self.__primitiveList:
            if timeStamp >= self.__startTime and timeStamp < (self.__startTime + self.__duration):
                primitive.draw(frame)
                primitive.updatePosition(delta = self.__pixelDelta)
                primitive.updateDrawProportion(delta=self.__drawPropDelta)

        self.__frameNumber += 1


