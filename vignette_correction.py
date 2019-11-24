import os

def run_method(vig_red_mth, vig_aux_data, image=None):
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

    lens_model = vig_aux_data.get('lens_model')
    out_path = vig_aux_data.get('out_path')
    vignette_tool_path = vig_aux_data.get('vignette_tool_path')
    matlab_path = vig_aux_data.get('matlab_path')

    print(vig_red_mth, lens_model, out_path, vignette_tool_path, matlab_path)

    if vig_red_mth == 'auto':
            # Set up the Matlab vignette removal tool
            matlab_flags = '-nodesktop -nojvm '
            app_run_command = "-r 'vignette_removal " + out_path+"/denoise_only" + " " + out_path + "; exit;';"
            vignette_fix_run_command = "cd " + vignette_tool_path + " && " + matlab_path + " " + matlab_flags + " " + app_run_command
            # Run vignette removal tool
            os.system(vignette_fix_run_command)

    elif vig_red_mth == 'lens':
        print("Using lens model for vignette removal")
