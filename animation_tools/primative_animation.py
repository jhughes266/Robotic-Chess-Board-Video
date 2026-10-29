class PrimitiveAnimation:
    def __init__(self, startLocation, endLocation, startColour, endColour, startDrawPercentage, endDrawPercentage, startTime, duration, fps):
        self.__primitiveList = []
        self.__startLocation = startLocation
        self.__endLocation = endLocation
        self.__startColour = startColour
        self.__endColour = endColour
        self.__startDrawPercentage = startDrawPercentage
        self.__endDrawPercentage = endDrawPercentage
        self.__startTime = startTime
        self.__duration = duration
        self.__fps = fps