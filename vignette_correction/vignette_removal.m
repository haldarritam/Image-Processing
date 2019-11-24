function vignette_removal(in_path, out_path)

% setting
addpath(genpath('.'));
addpath(in_path);
addpath(out_path);

if in_path(end) ~= "/"
    full_file_path = in_path + "/*.tif";
else
    full_file_path = in_path + "*.tif";
end

files = dir(full_file_path);

for file = files'
    % read and process the image
    im=imread(in_path+"/"+file.name);
    [im_vign_corrected,~]=vignCorrection_nonPara(im,0.25);
    
    
    
    if out_path(end) ~= "/"
    output_file = out_path+"/"+file.name;
    else
    output_file = out_path+file.name;
    end
 
    imwrite(im_vign_corrected, output_file);
end