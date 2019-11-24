import argparse
import os
import vignette_correction
import cv2
import numpy as np
import rawpy

if __name__ == "__main__":
    # ----- Command line argument parser -----
    parser = argparse.ArgumentParser(description='Batch Image Editor', fromfile_prefix_chars='@')
    parser.add_argument('-in_path', help='Path for the input images.', default='/Users/FelipeClark/Desktop/Image-Processing/orig_images',type=str, metavar='default=/Users/FelipeClark/Desktop/Image-Processing/orig_images')
    parser.add_argument('-out_path', help='Path where output images will be written to.', default='/Users/FelipeClark/Desktop/Image-Processing/out_images', type=str, metavar='default=/Users/FelipeClark/Desktop/Image-Processing/out_images')
    parser.add_argument('-vig_tool_path', help='Path to the vignette removal tool.', default='/Users/FelipeClark/Desktop/Image-Processing/vignette_correction', type=str, metavar="default='/Users/FelipeClark/Desktop/Image-Processing/vignette_correction'")
    parser.add_argument('-matlab_path', help='Path to the Matlab executable.', default='/Applications/MATLAB_R2019b.app/bin/matlab', type=str, metavar="default='/Applications/MATLAB_R2019b.app/bin/matlab'")
    parser.add_argument('-vig_red_mth', help='Vignette reduction method: [lens][auto].', default='auto', type=str, metavar="default=auto")
    parser.add_argument('-lens_model', help='Lens vignette model file.', type=str, metavar="No default. Mandatory if -vig_red_mth is 'lens'")
    parser.add_argument('-noise_red_mth', help='Noise reduction method: [low-pass][average][median]', default='average', type=str, metavar="default=average")

    # Reading command line arguments
    args = vars(parser.parse_args())  
    vignette_tool_path = args['vig_tool_path']
    matlab_path = args['matlab_path']
    in_path = args['in_path']
    out_path = args['out_path']
    vig_red_mth = args['vig_red_mth']
    lens_model = args['lens_model']
    noise_red_mth = args['noise_red_mth']

    # Validating and formatting command line options
    if not in_path.endswith("/"):
        in_path += "/"

    if not out_path.endswith("/"):
        out_path += "/"

    if vig_red_mth == 'lens' and lens_model == None:
        print("Lens model image file is required for the chosen vignette removal method.\n" +
              "Please provide a lens model image using the -lens_model parameter. Use -help for further assistance.\nAborting...")
        quit()

    vig_aux_data = {'lens_model': lens_model, 'out_path': out_path, 'vignette_tool_path': vignette_tool_path, 'matlab_path': matlab_path}

    # Auxiliary variagles
    kernel = np.ones((5, 5), np.float32) / 25
    if vig_red_mth == 'lens':
        std_vig_model = vignette_correction.load_vig_model(lens_model)

    for filename in os.listdir(in_path):
        if filename.endswith(".CR2"): 
            with rawpy.imread(in_path + filename) as raw:
                image = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)

            # ----- Noise Reduction-----
            if noise_red_mth == 'low-pass':
                print("Low pass")
                image = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), (5,5), 0)
            elif noise_red_mth == 'average':
                print("Average")
                image = cv2.filter2D(image,-1,kernel)
            elif noise_red_mth == 'median':
                print("Median")
                image = cv2.medianBlur(image,5)
            else:
                print("No noise filtering method will run.")

            brg_out = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(out_path + "denoise_only/" + filename.split('.')[0] + ".tif", brg_out)


            # ----- Lens Model Vignette Removal -----
            if vig_red_mth == 'lens':
                out_img = vignette_correction.run_method(vig_red_mth, vig_aux_data, image, std_vig_model)

                brg_out = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
                cv2.imwrite(out_path + filename.split('.')[0] + ".tif", brg_out)


    if vig_red_mth == 'auto':
        # ----- Auto Vignette Removal-----
        vignette_correction.run_method(vig_red_mth, vig_aux_data)
            
