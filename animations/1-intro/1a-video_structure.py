from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='1a-video_structure.mp4')

# Animation primitives
# Table
line1 = Line(pt1=[0.1,0.2], pt2=[0.9,0.2], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line2 = Line(pt1=[0.1,0.2], pt2=[0.1,0.8], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line3 = Line(pt1=[0.1,0.3], pt2=[0.9,0.3], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line4 = Line(pt1=[0.9,0.2], pt2=[0.9,0.8], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line5 = Line(pt1=[0.1,0.8], pt2=[0.9,0.8], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line6 = Line(pt1=[0.3,0.2], pt2=[0.3,0.8], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line7 = Line(pt1=[0.5,0.2], pt2=[0.5,0.8], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
line8 = Line(pt1=[0.7,0.2], pt2=[0.7,0.8], colour=(255,255,255),thickness=5, drawProportion=0, frameWidth=videoWidth, frameHeight=videoHeight)
# Text
# Title
tableTitle = Text(text="Video Structure", org=[0.5,0.1], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=5, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
# Column Titles
column1Heading = Text(text="Robotic Components", org=[0.2,0.25], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column2Heading = Text(text="Software Components", org=[0.4,0.25], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column3aHeading = Text(text="How All Components", org=[0.6,0.23], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column3bHeading = Text(text="Work Together", org=[0.6,0.27], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column4Heading = Text(text="Project Showcase", org=[0.8,0.25], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2.3, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
# Column Contents
# Column 1
column1aContents = Text(text="i. Physical parts", org=[0.2,0.35], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column1bContents = Text(text="ii. How pieces are moved", org=[0.2,0.40], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column1cContents = Text(text="around", org=[0.2,0.43], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
# Column 2
column2aContents = Text(text="i. User input into game", org=[0.4,0.35], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column2bContents = Text(text="ii. Determining what", org=[0.4,0.40], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column2cContents = Text(text="moves the robot makes", org=[0.4,0.43], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column2dContents = Text(text="iii. How to get pieces from", org=[0.4,0.48], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column2eContents = Text(text="from one location to", org=[0.4,0.51], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column2fContents = Text(text="another", org=[0.4,0.54], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
# Column 3
column3aContents = Text(text="i. How all the robotic and", org=[0.6,0.35], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column3bContents = Text(text="software components", org=[0.6,0.38], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column3cContents = Text(text="work together", org=[0.6,0.41], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
# Column 4
column4aContents = Text(text="i. Demonstration of the", org=[0.8,0.35], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)
column4bContents = Text(text="robotic chess board", org=[0.8,0.38], fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, colour=(255,255,255), drawProportion=0, progressiveDrawMode='letterByLetter', insertCursorThickness=10, frameWidth=videoWidth, frameHeight=videoHeight)





# Animations
# Heading ################################################################################################################
drawHeading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=0, endTime=1, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawHeading.addPrimitive(tableTitle)

holdHeading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=1, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdHeading.addPrimitive(tableTitle)


# Table ################################################################################################################
drawLine1 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=1, endTime=2, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine1.addPrimitive(line1)
drawLine2 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=1.6, endTime=2.6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine2.addPrimitive(line2)
drawLine3 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=1.2, endTime=2.2, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine3.addPrimitive(line3)
drawLine4 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=2.4, endTime=3.4, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine4.addPrimitive(line4)
drawLine5 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=1.4, endTime=2.4, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine5.addPrimitive(line5)
drawLine6 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=1.8, endTime=2.8, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine6.addPrimitive(line6)
drawLine7 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=2, endTime=3, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine7.addPrimitive(line7)
drawLine8 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=2.2, endTime=3.2, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawLine8.addPrimitive(line8)


holdLine1 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=2, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine1.addPrimitive(line1)
holdLine2 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=2.6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine2.addPrimitive(line2)
holdLine3 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=2.2, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine3.addPrimitive(line3)
holdLine4 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=3.4, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine4.addPrimitive(line4)
holdLine5 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=2.4, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine5.addPrimitive(line5)
holdLine6 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=2.8, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine6.addPrimitive(line6)
holdLine7 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=3, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine7.addPrimitive(line7)
holdLine8 = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=1, endDrawProportion=1, startTime=3.2, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdLine8.addPrimitive(line8)

# Table Contents ################################################################################################################
drawColumn1Heading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn1Heading.addPrimitive(column1Heading)
drawColumn2Heading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2Heading.addPrimitive(column2Heading)
drawColumn3aHeading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn3aHeading.addPrimitive(column3aHeading)
drawColumn3bHeading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn3bHeading.addPrimitive(column3bHeading)
drawColumn4Heading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn4Heading.addPrimitive(column4Heading)


drawColumn1aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn1aContents.addPrimitive(column1aContents)
drawColumn1bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn1bContents.addPrimitive(column1bContents)
drawColumn1cContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn1cContents.addPrimitive(column1cContents)
drawColumn2aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2aContents.addPrimitive(column2aContents)
drawColumn2bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2bContents.addPrimitive(column2bContents)
drawColumn2cContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2cContents.addPrimitive(column2cContents)
drawColumn2dContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2dContents.addPrimitive(column2dContents)
drawColumn2eContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2eContents.addPrimitive(column2eContents)
drawColumn2fContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn2fContents.addPrimitive(column2fContents)
drawColumn3aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn3aContents.addPrimitive(column3aContents)
drawColumn3bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn3bContents.addPrimitive(column3bContents)
drawColumn3cContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn3cContents.addPrimitive(column3cContents)
drawColumn4aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn4aContents.addPrimitive(column4aContents)
drawColumn4bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=4, endTime=6, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
drawColumn4bContents.addPrimitive(column4bContents)


holdColumn1Heading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn1Heading.addPrimitive(column1Heading)
holdColumn2Heading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2Heading.addPrimitive(column2Heading)
holdColumn3aHeading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn3aHeading.addPrimitive(column3aHeading)
holdColumn3bHeading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn3bHeading.addPrimitive(column3bHeading)
holdColumn4Heading = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn4Heading.addPrimitive(column4Heading)


holdColumn1aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn1aContents.addPrimitive(column1aContents)
holdColumn1bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn1bContents.addPrimitive(column1bContents)
holdColumn1cContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn1cContents.addPrimitive(column1cContents)
holdColumn2aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2aContents.addPrimitive(column2aContents)
holdColumn2bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2bContents.addPrimitive(column2bContents)
holdColumn2cContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2cContents.addPrimitive(column2cContents)
holdColumn2dContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2dContents.addPrimitive(column2dContents)
holdColumn2eContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2eContents.addPrimitive(column2eContents)
holdColumn2fContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn2fContents.addPrimitive(column2fContents)
holdColumn3aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn3aContents.addPrimitive(column3aContents)
holdColumn3bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn3bContents.addPrimitive(column3bContents)
holdColumn3cContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn3cContents.addPrimitive(column3cContents)
holdColumn4aContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn4aContents.addPrimitive(column4aContents)
holdColumn4bContents = PrimitiveAnimation(startLocation=[0.0,0.0], endLocation=[0.0, 0.0], startDrawProportion=0, endDrawProportion=1, startTime=6, endTime=videoDuration, fps=fps, frameWidth=videoWidth, frameHeight=videoHeight)
holdColumn4bContents.addPrimitive(column4bContents)


# Animation rendering
sceneAnimator.addPrimitiveAnimation(drawHeading)
sceneAnimator.addPrimitiveAnimation(holdHeading)

sceneAnimator.addPrimitiveAnimation(drawLine1)
sceneAnimator.addPrimitiveAnimation(drawLine2)
sceneAnimator.addPrimitiveAnimation(drawLine3)
sceneAnimator.addPrimitiveAnimation(drawLine4)
sceneAnimator.addPrimitiveAnimation(drawLine5)
sceneAnimator.addPrimitiveAnimation(drawLine6)
sceneAnimator.addPrimitiveAnimation(drawLine7)
sceneAnimator.addPrimitiveAnimation(drawLine8)
sceneAnimator.addPrimitiveAnimation(holdLine1)
sceneAnimator.addPrimitiveAnimation(holdLine2)
sceneAnimator.addPrimitiveAnimation(holdLine3)
sceneAnimator.addPrimitiveAnimation(holdLine4)
sceneAnimator.addPrimitiveAnimation(holdLine5)
sceneAnimator.addPrimitiveAnimation(holdLine6)
sceneAnimator.addPrimitiveAnimation(holdLine7)
sceneAnimator.addPrimitiveAnimation(holdLine8)

sceneAnimator.addPrimitiveAnimation(drawColumn1Heading)
sceneAnimator.addPrimitiveAnimation(drawColumn2Heading)
sceneAnimator.addPrimitiveAnimation(drawColumn3aHeading)
sceneAnimator.addPrimitiveAnimation(drawColumn3bHeading)
sceneAnimator.addPrimitiveAnimation(drawColumn4Heading)

sceneAnimator.addPrimitiveAnimation(drawColumn1aContents)
sceneAnimator.addPrimitiveAnimation(drawColumn1bContents)
sceneAnimator.addPrimitiveAnimation(drawColumn1cContents)
sceneAnimator.addPrimitiveAnimation(drawColumn2aContents)
sceneAnimator.addPrimitiveAnimation(drawColumn2bContents)
sceneAnimator.addPrimitiveAnimation(drawColumn2cContents)
sceneAnimator.addPrimitiveAnimation(drawColumn2dContents)
sceneAnimator.addPrimitiveAnimation(drawColumn2eContents)
sceneAnimator.addPrimitiveAnimation(drawColumn2fContents)
sceneAnimator.addPrimitiveAnimation(drawColumn3aContents)
sceneAnimator.addPrimitiveAnimation(drawColumn3bContents)
sceneAnimator.addPrimitiveAnimation(drawColumn3cContents)
sceneAnimator.addPrimitiveAnimation(drawColumn4aContents)
sceneAnimator.addPrimitiveAnimation(drawColumn4bContents)

sceneAnimator.addPrimitiveAnimation(holdColumn1Heading)
sceneAnimator.addPrimitiveAnimation(holdColumn2Heading)
sceneAnimator.addPrimitiveAnimation(holdColumn3aHeading)
sceneAnimator.addPrimitiveAnimation(holdColumn3bHeading)
sceneAnimator.addPrimitiveAnimation(holdColumn4Heading)

sceneAnimator.addPrimitiveAnimation(holdColumn1aContents)
sceneAnimator.addPrimitiveAnimation(holdColumn1bContents)
sceneAnimator.addPrimitiveAnimation(holdColumn1cContents)
sceneAnimator.addPrimitiveAnimation(holdColumn2aContents)
sceneAnimator.addPrimitiveAnimation(holdColumn2bContents)
sceneAnimator.addPrimitiveAnimation(holdColumn2cContents)
sceneAnimator.addPrimitiveAnimation(holdColumn2dContents)
sceneAnimator.addPrimitiveAnimation(holdColumn2eContents)
sceneAnimator.addPrimitiveAnimation(holdColumn2fContents)
sceneAnimator.addPrimitiveAnimation(holdColumn3aContents)
sceneAnimator.addPrimitiveAnimation(holdColumn3bContents)
sceneAnimator.addPrimitiveAnimation(holdColumn3cContents)
sceneAnimator.addPrimitiveAnimation(holdColumn4aContents)
sceneAnimator.addPrimitiveAnimation(holdColumn4bContents)

sceneAnimator.renderAnimation()


