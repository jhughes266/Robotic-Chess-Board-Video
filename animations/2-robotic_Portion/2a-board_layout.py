from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 11


sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2a-board_layout.mp4')
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
# Drawing the chess board
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
topLeft = [((1 - (12 * squareWidth))/ 2) + 2 * squareWidth, ((1 - (12 * squareHeight )) / 2) + 2 * squareHeight -.05]
drawDuration = 2.2
lightSquare = True
# Dictionary to store all the piece path files
squareToPiecePath = {
    0: "black_rook",
    1: "black_pawn",
    6: "white_pawn",
    7: "white_rook",

    8: "black_knight",
    9: "black_pawn",
    14: "white_pawn",
    15: "white_knight",

    16: "black_bishop",
    17: "black_pawn",
    22: "white_pawn",
    23: "white_bishop",

    24: "black_queen",
    25: "black_pawn",
    30: "white_pawn",
    31: "white_queen",

    32: "black_king",
    33: "black_pawn",
    38: "white_pawn",
    39: "white_king",

    40: "black_bishop",
    41: "black_pawn",
    46: "white_pawn",
    47: "white_bishop",

    48: "black_knight",
    49: "black_pawn",
    54: "white_pawn",
    55: "white_knight",

    56: "black_rook",
    57: "black_pawn",
    62: "white_pawn",
    63: "white_rook"
}
for i in range(8):
    for j in range(8):
        # Squares
        squareIdx = (i * 8 + j)
        startTime = (squareIdx/64) * drawDuration
        squareDrawDuration = (drawDuration/64)
        if lightSquare:
            colour = (89,155,240)
        else:
            colour = (21,67,120)

        lightSquare = not lightSquare

        chessSquare = Rectangle(pt1=[topLeft[0] + i * squareWidth , topLeft[1] + j* squareHeight], pt2=[topLeft[0] + (i + 1) * squareWidth , topLeft[1] + (j + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
        chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        chessSquareAnimation.addPrimitive(chessSquare)

        chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
        chessSquareHoldAnimation.addPrimitive(chessSquare)

        sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
        sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)
        # Pieces
        if squareIdx in squareToPiecePath:
            piecePath = squareToPiecePath[squareIdx]
            path = '../resources/piece_images/' + piecePath + '.jpg'
            image = Image(topLeft=[topLeft[0] + i * squareWidth , topLeft[1] + j* squareHeight], imgPath=path, imageWidth=squareWidth, colour=None, drawProportion=0, maxNumBlurs=100, frameWidth=videoWidth, frameHeight=videoHeight, onlyKeepMonoChrome=True)

            imageDraw = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth,frameHeight=videoHeight)
            imageDraw.addPrimitive(image)

            imageHold = PrimitiveAnimation(startLocation=[0.0, .0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration, endTime=videoDuration, fps=fps, frameWidth=videoWidth,frameHeight=videoHeight)
            imageHold.addPrimitive(image)

            sceneAnimator.addPrimitiveAnimation(imageDraw)
            sceneAnimator.addPrimitiveAnimation(imageHold)


    lightSquare = not lightSquare

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
#Drawing the graveyard squares
# Left strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
topLeft = [((1 - (12 * squareWidth))/ 2) , ((1 - (12 * squareHeight )) / 2) -.05]
drawDuration = 0.5
drawOffsetTime = 3
lightSquare = True
for i in range(11):
    startTime = (i/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (0, 0, 125)
    else:
        colour = (0, 0, 255)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] , topLeft[1] + i * squareHeight], pt2=[topLeft[0] + squareWidth , topLeft[1] + (i + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)

# Bottom Strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
drawOffsetTime += 11 * (drawDuration / 12)

for i in range(11):
    startTime = (i/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (0, 0, 125)
    else:
        colour = (0, 0, 255)

    lightSquare = not lightSquare
    chessSquare = Rectangle(pt1=[topLeft[0] + i * squareWidth , topLeft[1] + 11 * squareHeight], pt2=[topLeft[0] + (i + 1) * squareWidth , topLeft[1] + (11 + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)

# right strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
drawOffsetTime += 11 * (drawDuration / 12)

for enIdx, i in enumerate(range(11,0,-1)):
    startTime = (enIdx/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (0, 0, 125)
    else:
        colour = (0, 0, 255)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] + 11 * squareWidth , topLeft[1] + i * squareHeight], pt2=[topLeft[0] + 12 * squareWidth , topLeft[1] + (i + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)

# Top Strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
drawOffsetTime += 11 * (drawDuration / 12)
textEndTime = None
for enIdx, i in enumerate(range(11,0,-1)):
    startTime = (enIdx/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (0, 0, 125)
    else:
        colour = (0, 0, 255)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] + i * squareWidth , topLeft[1]], pt2=[topLeft[0] + (i + 1) * squareWidth , topLeft[1] + squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)
    textEndTime = startTime+squareDrawDuration

textDrawStartTime = 3
textLocation = [0.175, 0.4]
text = Text(text="Captured piece storage", org=textLocation, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, colour=(0, 0, 255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5, frameWidth=videoWidth, frameHeight=videoHeight)

textDraw = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime+0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textDraw.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textDraw)


textHold = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime+0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textHold.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textHold)

textVanish = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime-0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textVanish.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textVanish)
""


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
#Drawing the buffer squares
# Left strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
topLeft = [((1 - (12 * squareWidth))/ 2) + squareWidth , ((1 - (12 * squareHeight )) / 2) +squareHeight -.05]
drawDuration = 0.5
drawOffsetTime = 5
lightSquare = True
textDrawStartTime = drawOffsetTime
for i in range(10):
    startTime = (i/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (192, 192, 192)
    else:
        colour = (125, 125, 125)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] , topLeft[1] + i * squareHeight], pt2=[topLeft[0] + squareWidth , topLeft[1] + (i + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)

# Bottom Strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
drawOffsetTime += 11 * (drawDuration / 12)
lightSquare = not lightSquare
for i in range(10):
    startTime = (i/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (192, 192, 192)
    else:
        colour = (125, 125, 125)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] + i * squareWidth , topLeft[1] + 9 * squareHeight], pt2=[topLeft[0] + (i + 1) * squareWidth , topLeft[1] + (9 + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)

# right strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
drawOffsetTime += 11 * (drawDuration / 12)
lightSquare = not lightSquare
for enIdx, i in enumerate(range(9,0,-1)):
    startTime = (enIdx/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (192, 192, 192)
    else:
        colour = (125, 125, 125)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] + 9 * squareWidth , topLeft[1] + i * squareHeight], pt2=[topLeft[0] + 10 * squareWidth , topLeft[1] + (i + 1) * squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)
    textEndTime = startTime+squareDrawDuration


# Top Strip
squareWidth = 0.03
squareHeight = (videoWidth / videoHeight) * squareWidth
drawOffsetTime += 11 * (drawDuration / 12)
textEndTime = None
for enIdx, i in enumerate(range(9,0,-1)):
    startTime = (enIdx/ 11) * drawDuration + drawOffsetTime
    squareDrawDuration = (drawDuration / 12)
    if lightSquare:
        colour = (192, 192, 192)
    else:
        colour = (125, 125, 125)

    lightSquare = not lightSquare

    chessSquare = Rectangle(pt1=[topLeft[0] + i * squareWidth , topLeft[1]], pt2=[topLeft[0] + (i + 1) * squareWidth , topLeft[1] + squareHeight], colour=colour, thickness=-1, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation = PrimitiveAnimation(startLocation=[0.0, 0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=startTime, endTime=startTime+squareDrawDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareAnimation.addPrimitive(chessSquare)

    chessSquareHoldAnimation = PrimitiveAnimation(startLocation=[0.3, .3], endLocation=[0.3, 0.3], startDrawProportion=1, endDrawProportion=1, startTime=startTime+squareDrawDuration , endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
    chessSquareHoldAnimation.addPrimitive(chessSquare)

    sceneAnimator.addPrimitiveAnimation(chessSquareAnimation)
    sceneAnimator.addPrimitiveAnimation(chessSquareHoldAnimation)
    textEndTime = startTime + squareDrawDuration


textLocation = [0.175, 0.4]
text = Text(text="Visual buffer", org=textLocation, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, colour=(192,192,192), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5, frameWidth=videoWidth, frameHeight=videoHeight)

textDraw = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime+0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textDraw.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textDraw)


textHold = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime+0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textHold.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textHold)

textVanish = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime-0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textVanish.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textVanish)
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
#12 * 12 grid squares label
textDrawStartTime = 8
textEndTime = 11
textLocation = [0.5, 0.075]
text = Text(text="12 Squares", org=textLocation, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5, frameWidth=videoWidth, frameHeight=videoHeight)

textDraw = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime+0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textDraw.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textDraw)


textHold = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime+0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textHold.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textHold)

textVanish = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime-0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textVanish.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textVanish)


textLocation = [.75, 0.45]
text = Text(text="12 Squares", org=textLocation, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=5, frameWidth=videoWidth, frameHeight=videoHeight)

textDraw = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime+0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textDraw.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textDraw)


textHold = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime+0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textHold.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textHold)

textVanish = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime-0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
textVanish.addPrimitive(text)
sceneAnimator.addPrimitiveAnimation(textVanish)



# 1
line = Line(pt1=[0.32,0.075], pt2=[0.425,0.075], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# 2
line = Line(pt1=[0.32,0.075], pt2=[0.32,0.075+.05], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# 3
line = Line(pt1=[1 - 0.32,0.075], pt2=[ 1 - 0.425,0.075], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# 4
line = Line(pt1=[1-0.32,0.075], pt2=[1-0.32,0.075+.05], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)


# 5
line = Line(pt1=[0.75-.033,0.13], pt2=[0.75-.033,0.425], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# 6
line = Line(pt1=[0.715-.033,0.13], pt2=[0.75-.033,0.13], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# 7
line = Line(pt1=[0.75-.033,.77], pt2=[0.75-.033,.5], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# 8
line = Line(pt1=[0.715-.033,.77], pt2=[0.75-.033,.77], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)

lineDrawAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=0, endDrawProportion=1, startTime=textDrawStartTime, endTime=textDrawStartTime + 0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineDrawAnimation.addPrimitive(line)

lineHoldAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=1, startTime=textDrawStartTime + 0.5, endTime=textEndTime-0.5, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineHoldAnimation.addPrimitive(line)

lineVanishAnimation = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0,0.0], startDrawProportion=1, endDrawProportion=0, startTime=textEndTime - 0.5, endTime=textEndTime, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
lineVanishAnimation.addPrimitive(line)

sceneAnimator.addPrimitiveAnimation(lineDrawAnimation)
sceneAnimator.addPrimitiveAnimation(lineHoldAnimation)
sceneAnimator.addPrimitiveAnimation(lineVanishAnimation)

# render the animation
sceneAnimator.renderAnimation()

