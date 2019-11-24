from __future__ import division
import numpy as np
from PIL import Image
import cv2
import rawpy

def correct_channel(img_array, channel, std_vig_model):
  img_channel = img_array[:, :, channel]
  
  #Standardise array.
  img_max = np.amax(img_channel) 
  std_img = img_channel / img_max

  #Divide the two arrays to remove vignetting.
  corrected_img = std_img / std_vig_model

  #Standardise corrected array.
  corrected_max = np.amax(corrected_img) 
  std_corrected = corrected_img / corrected_max

  #Reconstruct the output image.
  output_img_channel = std_corrected * img_max  

  return output_img_channel

def remove_vig(img_array, std_vig_model):
  r = correct_channel(img_array, 0, std_vig_model)
  g = correct_channel(img_array, 1, std_vig_model)
  b = correct_channel(img_array, 2, std_vig_model)

  rgbArray = np.zeros((r.shape[0], r.shape[1], 3), 'uint8')
  rgbArray[..., 0] = r
  rgbArray[..., 1] = g
  rgbArray[..., 2] = b

  return rgbArray
    

def load_vig_model(model):
  #Import a grayscale test image of a uniform background.
  with rawpy.imread(model) as raw:
    rgb = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)

  vig_model_grey = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

  #Standardise grayscale array by setting max pixel value to 1.
  max_vig_model = np.amax(vig_model_grey) 
  std_vig_model = vig_model_grey / max_vig_model

  return std_vig_model


def lens_based_vign_removal(path, out_path, std_vig_model):
  #Import the image we wish to remove the vignette effect from.
  with rawpy.imread(path) as raw:
    img_array = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)

  out_img = remove_vig(img_array, std_vig_model)

  brg_out = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
  cv2.imwrite(out_path, brg_out)


if __name__ == "__main__":

  model = "apprt_1.2_uniform_same_exp.CR2"
  img = "apprt_1.2_image.CR2"
  img_out = "lens_based_test.tif"
  
  vign_model = load_vig_model(model)

  lens_based_vign_removal(img, img_out, vign_model)

