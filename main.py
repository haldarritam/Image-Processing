import argparse
import os
import vignette_correction
import cv2
import numpy as np
import rawpy


def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    auto_result = hisEqulColor(auto_result)
    return (auto_result, alpha, beta)




def hisEqulColor(img):
    ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    channels=cv2.split(ycrcb)

    brightness = np.sum(channels[2]) / (255 * channels[2].shape[0] * channels[2].shape[1])
    minimum_brightness = 0.35
    ratio = brightness / minimum_brightness
    if ratio < 1:
        channels[2] = cv2.convertScaleAbs(channels[2], alpha = 1/ ratio, beta = 0)

    cv2.merge(channels,ycrcb)
    cv2.cvtColor(ycrcb,cv2.COLOR_HSV2BGR,img)
    return img

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

    vig_aux_data = {'lens_model': lens_model, 'in_path': in_path, 'vignette_tool_path': vignette_tool_path, 'matlab_path': matlab_path}

    # Auxiliary variagles
    kernel = np.ones((5, 5), np.float32) / 25
    if vig_red_mth == 'lens':
        std_vig_model = vignette_correction.load_vig_model(lens_model)

    file_type = ".CR2"
    noise_reduction_enabled = noise_red_mth == 'low-pass' or noise_red_mth == 'average' or noise_red_mth == 'median'
    auto_vig_output = in_path
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized = False



    # ----- Auto Vignette Removal-----
    if vig_red_mth == 'auto':
        # ----- Converting file types to TIF so Matlab can read the images -----
        for filename in os.listdir(in_path):
            if filename.endswith(file_type):
                with rawpy.imread(in_path + filename) as raw:
                    image = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)
                    brg_out = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    brg_out = cv2.resize(brg_out, (0,0), fx=0.5, fy = 0.5)
                    # brg_out = automatic_brightness_and_contrast(brg_out)[0]
                    equalized = True
                    cv2.imwrite(in_path + filename.split('.')[0] + ".tif", brg_out)

                    if not noise_reduction_enabled:
                        auto_vig_output = out_path

        file_type = ".tif"

        
        vignette_correction.run_method(vig_red_mth, vig_aux_data, auto_vig_output)

    # ----- Further Processing -----
    if noise_reduction_enabled or vig_red_mth == 'lens':
        for filename in os.listdir(in_path):
            if filename.endswith(file_type):
                is_raw = False
                if vig_red_mth != 'auto':
                    raw = rawpy.imread(in_path + filename)
                    image = raw.postprocess(use_camera_wb=True, output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)
                    is_raw = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                else:
                    image = cv2.imread(in_path + filename)

                # ----- Lens Model Vignette Removal -----
                if vig_red_mth == 'lens':
                    image = vignette_correction.run_method(vig_red_mth, vig_aux_data, auto_vig_output, image, std_vig_model)
                    
                if not equalized:
                    image = automatic_brightness_and_contrast(image)[0]

                # ----- Noise Reduction-----
                if noise_red_mth == 'low-pass':
                    print("Low pass")
                    image = cv2.GaussianBlur(image, (5,5), 0)
                elif noise_red_mth == 'average':
                    print("Average")
                    image = cv2.filter2D(image,-1,kernel)
                elif noise_red_mth == 'median':
                    print("Median")
                    image = cv2.medianBlur(image,5)
                else:
                    print("No noise filtering method will run.")

                # ----- Save results -----
                if is_raw:
                    raw.close()
                
                cv2.imwrite(out_path + filename.split('.')[0] + ".tif", image)

            