import cv2
import numpy as np

######
img = cv2.imread('piece_of_shit_orig.tiff')
rows, cols = img.shape[:2]

# generating vignette mask using Gaussian kernels
kernel_x = cv2.getGaussianKernel(cols,cols/3)
kernel_y = cv2.getGaussianKernel(rows,rows/3)

kernel = kernel_y * kernel_x.T
mask = 1 - 255 * kernel / np.linalg.norm(kernel)
#mask /= mask[rows//2, cols//2] 

cv2.imshow('mask', mask)

#print(mask[rows//2, cols//2])

output = np.copy(img)

# applying the mask to each channel in the input image
for i in range(3):
    output[:,:,i] = (output[:,:,i] * mask)


#print(output)
np.clip(output, a_min=0, a_max=255)

cv2.imwrite( 'original.tiff', img)
cv2.imwrite( 'vignette.tiff', output)

# cv2.imshow('Original', img)
# cv2.imshow('Vignette', output)
# cv2.waitKey(0)