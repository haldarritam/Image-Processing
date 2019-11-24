import numpy as np
import rawpy
import imageio
from PIL import Image, ImageDraw
import cv2
import time

path = "apprt_1.2_uniform_same_exp.CR2"
with rawpy.imread(path) as raw:
  rgb = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)
  brg = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
  gray = cv2.cvtColor(brg, cv2.COLOR_BGR2GRAY)


print(brg.shape, gray.shape)

cv2.imwrite( 'apprt_1.2_uniform_same_exp.jpg', gray)