import numpy as np
import rawpy
import imageio
from PIL import Image, ImageDraw
import cv2
import time

kernel = np.ones((5, 5), np.float32) / 25

num_image = 1
for img_num in range(1, num_image + 1):

    # Timer
    milestone_1 = time.time()

    path = "test_img_" + str(img_num) + ".CR2"
    # path = "colour_test.CR2"

    with rawpy.imread(path) as raw:
        rgb = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    # Timer
    milestone_2 = time.time()

    # output = cv2.GaussianBlur(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), (5,5), 0)
    # output = cv2.filter2D(rgb,-1,kernel)
    output = cv2.medianBlur(rgb,5)

    milestone_3 = time.time()

    # imageio.imsave('piece_of_shit.tiff', rgb)
    cv2.imwrite( 'piece_of_shit.tiff', output)

    # Timer
    milestone_4 = time.time()

    print("%d --> %0.3f | %0.3f | %0.3f" % (img_num, (milestone_2 - milestone_1), (milestone_3 - milestone_2), (milestone_4 - milestone_3)))
