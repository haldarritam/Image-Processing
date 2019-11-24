import os
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


def run_method(vig_red_mth, vig_aux_data, image=None, std_vig_model=None):
    '''
    Performs vignette correction.
    vig_aux_data is a dictionary containing:
        vig_red_mth: the vignette correction method to be used
        lens_model: an image representing the vignetting model for the lens (pircure of a uniform background). Can be set to None if method is auto.
        out_path: output path to write the vignette corrected images to
        vignette_tool_path: path for the auxiliary tool to perform the auto method. Can be set to None if method is lens
        matlab_path: path for the Matlab executable. Can be set to None if method is lens.
    image: image whose vignette needs to be fixed. Can be set to None if method is auto.
    '''

    out_path = vig_aux_data.get('out_path')
    vignette_tool_path = vig_aux_data.get('vignette_tool_path')
    matlab_path = vig_aux_data.get('matlab_path')

    print(vig_red_mth, out_path, vignette_tool_path, matlab_path)

    if vig_red_mth == 'auto':
            # Set up the Matlab vignette removal tool
            matlab_flags = '-nodesktop -nojvm '
            app_run_command = "-r 'vignette_removal " + out_path+"/denoise_only" + " " + out_path + "; exit;';"
            vignette_fix_run_command = "cd " + vignette_tool_path + " && " + matlab_path + " " + matlab_flags + " " + app_run_command
            # Run vignette removal tool
            os.system(vignette_fix_run_command)

    elif vig_red_mth == 'lens':
        return remove_vig(image, std_vig_model)