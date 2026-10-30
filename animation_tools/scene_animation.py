import cv2
import numpy as np

class SceneAnimation:
    def __init__(self, videoWidth, videoHeight, fps, videoDuration, outputFile):
        self.__primitiveAnimationList = []
        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        outputVideo = cv2.VideoWriter(outputFile, fourcc, fps, (videoWidth, videoHeight))
        self.__fps = fps
        self.__numberOfFrames = fps * videoDuration
        self.__outputFile = outputFile

    def addPrimitiveAnimation(self, primitiveAnimation):
        self.__primitiveAnimationList.append(primitiveAnimation)

    def renderAnimation(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        outputVideo = cv2.VideoWriter(self.__outputFile, fourcc, self.__fps, (self.__videoWidth, self.__videoHeight))

        for i in range(self.__numberOfFrames):
            frame = np.zeros((self.__videoHeight, self.__videoWidth, 3), np.uint8)
            for primitiveAnimation in self.__primitiveAnimationList:
                primitiveAnimation.draw(frame)

            outputVideo.write(frame)

            print(f"\rFrame {i + 1}/{self.__numberOfFrames} rendered and saved!", end="")

        outputVideo.release()
        print("\nFinished!")
