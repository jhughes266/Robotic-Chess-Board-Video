from animation_tools.elements import *
from animation_tools.primative_animation import *
from animation_tools.scene_animation import *
videoWidth = 3840
videoHeight = 2160
fps = 30
videoDuration = 10
sceneAnimator = SceneAnimation(videoWidth=videoWidth, videoHeight=videoHeight, fps=fps, videoDuration=videoDuration, outputFile='2a-board_layout.mp4')


sceneAnimator.renderAnimation()