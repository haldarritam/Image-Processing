# import numpy as np

# from PIL import Image
# from rawpy import Raw

# filename = 'test_img.cr2'
# raw_image = Raw(filename)
# buffered_image = np.array(raw_image.to_buffer())
# image = Image.frombytes('RGB', (raw_image.metadata.width, raw_image.metadata.height), buffered_image)
# image.save('image.png', format='png')

import rawpy
import imageio
from PIL import Image, ImageDraw
import cv2

path = 'test_img.CR2'
with rawpy.imread(path) as raw:
    rgb = raw.postprocess(use_camera_wb=True)
# imageio.imsave('default.png', rgb)


# Load image:
# input_image = Image.open("test_img.png")
# input_pixels = input_image.load()

print("FINISHED")
output = cv2.GaussianBlur(rgb, (5,5), 1, 1)

imageio.imsave('piece_of_shit.png', output)


# # Box Blur kernel
# box_kernel = [[1 / 9, 1 / 9, 1 / 9],
#               [1 / 9, 1 / 9, 1 / 9],
#               [1 / 9, 1 / 9, 1 / 9]]

# # Gaussian kernel
# gaussian_kernel = [[1 / 256, 4  / 256,  6 / 256,  4 / 256, 1 / 256],
#                    [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
#                    [6 / 256, 24 / 256, 36 / 256, 24 / 256, 6 / 256],
#                    [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
#                    [1 / 256, 4  / 256,  6 / 256,  4 / 256, 1 / 256]]

# # Select kernel here:
# kernel = gaussian_kernel

# # Middle of the kernel
# offset = len(kernel) // 2

# # Create output image
# output_image = Image.new("RGB", input_image.size)
# draw = ImageDraw.Draw(output_image)

# # Compute convolution between intensity and kernels
# for x in range(offset, input_image.width - offset):
#     print(x)
#     for y in range(offset, input_image.height - offset):
#         acc = [0, 0, 0]
#         for a in range(len(kernel)):
#             for b in range(len(kernel)):
#                 xn = x + a - offset
#                 yn = y + b - offset
#                 pixel = input_pixels[xn, yn]
#                 acc[0] += pixel[0] * kernel[a][b]
#                 acc[1] += pixel[1] * kernel[a][b]
#                 acc[2] += pixel[2] * kernel[a][b]

#         draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))
    
# output_image.save("output.png")