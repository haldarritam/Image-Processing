import argparse
import os
import vignette_correction

if __name__ == "__main__":
    # ----- Command line argument parser -----
    parser = argparse.ArgumentParser(description='Batch Image Editor', fromfile_prefix_chars='@')
    parser.add_argument('-in_path', help='Path for the input images.', default='/Users/FelipeClark/Desktop/Image-Processing/orig_images',type=str, metavar='default=/Users/FelipeClark/Desktop/Image-Processing/orig_images')
    parser.add_argument('-out_path', help='Path where output images will be written to.', default='/Users/FelipeClark/Desktop/Image-Processing/out_images', type=str, metavar='default=/Users/FelipeClark/Desktop/Image-Processing/out_images')
    parser.add_argument('-vig_tool_path', help='Path to the vignette removal tool.', default='/Users/FelipeClark/Desktop/Image-Processing/vignette_correction', type=str, metavar="default='/Users/FelipeClark/Desktop/Image-Processing/vignette_correction'")
    parser.add_argument('-matlab_path', help='Path to the Matlab executable.', default='/Applications/MATLAB_R2019b.app/bin/matlab', type=str, metavar="default='/Applications/MATLAB_R2019b.app/bin/matlab'")
    parser.add_argument('-vig_red_mth', help='Vignette reduction method: [lens][auto].', default='auto', type=str, metavar="default=auto")
    parser.add_argument('-lens_model', help='Lens vignette model file.', type=str, metavar="No default. Mandatory if -vig_red_mth is 'lens'")

    # Reading command line arguments
    args = vars(parser.parse_args())  
    vignette_tool_path = args['vig_tool_path']
    matlab_path = args['matlab_path']
    in_path = args['in_path']
    out_path = args['out_path']
    vig_red_mth = args['vig_red_mth']
    lens_model = args['lens_model']

    # Validating command line options
    if vig_red_mth == 'lens' and lens_model == None:
        print("Lens model image file is required for the chosen vignette removal method.\n" +
              "Please provide a lens model image using the -lens_model parameter. Use -help for further assistance.\nAborting...")
        quit()

    vig_aux_data = {'lens_model': lens_model, 'out_path': out_path, 'vignette_tool_path': vignette_tool_path, 'matlab_path': matlab_path}


    for filename in os.listdir(in_path):
        if filename.endswith(".cr2"): 
            # ----- Noise Reduction-----

            # ----- Lens Model Vignette Removal -----
            image = None # TODO: image must be updated to the opened image matrix
            if vig_red_mth == 'lens':
                vignette_correction.run_method(vig_red_mth, vig_aux_data, image)


    if vig_red_mth == 'auto':
        # ----- Auto Vignette Removal-----
        vignette_correction.run_method(vig_red_mth, vig_aux_data)
            
