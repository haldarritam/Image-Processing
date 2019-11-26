#!/usr/bin/env bash

# ----- All noise reduction methods with lens profile vignette removal -----
echo Low-pass and lens
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/low_pass-lens \
-vig_red_mth lens -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth low-pass
echo ----------

echo Average and lens
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/average-lens \
-vig_red_mth lens -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth average
echo ----------

echo Median and lens
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/median-lens \
-vig_red_mth lens -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth median
echo ----------

# ----- All noise reduction methods with automatic vignette removal -----
echo Low-pass and auto 
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/low_pass-auto \
-vig_red_mth auto -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth low-pass
echo ----------

echo Average and auto
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/average-auto \
-vig_red_mth auto -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth average
echo ----------

echo Median and auto
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/median-auto \
-vig_red_mth auto -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth median
echo ----------

# ----- Only noise reduction -----
echo Low-pass
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/low_pass \
-vig_red_mth none -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth low-pass
echo ----------

echo Average
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/average \
-vig_red_mth none -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth average
echo ----------

echo Median
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/median \
-vig_red_mth none -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth median
# echo ----------

# ----- Only vignette removal -----

echo Lens
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/lens \
-vig_red_mth lens -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth none
echo ----------

echo Auto
time python main.py -in_path /Users/FelipeClark/Desktop/Image-Processing/orig_images/0182 \
-out_path /Users/FelipeClark/Desktop/Image-Processing/out_images/auto \
-vig_red_mth auto -lens_model /Users/FelipeClark/Desktop/Image-Processing/orig_images/vignette_model/_D3_0182.CR2 \
-noise_red_mth none
echo ----------
