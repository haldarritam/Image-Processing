import os

vignette_tool_path = '~/Desktop/Image-Processing/vignette_correction'
matlab_path = '/Applications/MATLAB_R2019b.app/bin/matlab '
matlab_flags = '-nodesktop -nojvm '
app_run_command = "-r 'vignette_removal '~/Desktop/Image-Processing/out_images/denoise_only' '~/Desktop/Image-Processing/out_images'; exit;';"

vignette_fix_run_command = "cd " + vignette_tool_path + " && " + matlab_path + matlab_flags + app_run_command

os.system(vignette_fix_run_command)