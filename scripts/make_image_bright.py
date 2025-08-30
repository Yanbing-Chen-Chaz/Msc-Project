#This script enhances the brightness of TIFF images in a specified folder
# by stretching the pixel values to cover the full range of the data type.
import os
import tifffile
import numpy as np

# set input and output folders (use your actual paths)
input_folder = 'desktop/Hela2'
output_folder = 'desktop/Hela2_8'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.tif'):
        filepath = os.path.join(input_folder, filename)
        
        # read the TIFF image
        img = tifffile.imread(filepath)
        dtype = img.dtype
        img_float = img.astype(np.float32)

        # stretch the pixel values to cover the full range
        p1, p99 = np.percentile(img_float, (1, 99))
        img_stretched = np.clip((img_float - p1) / (p99 - p1), 0, 1)

        # map the stretched values back to the original data type
        if np.issubdtype(dtype, np.integer):
            max_val = np.iinfo(dtype).max
        else:
            max_val = 1.0
        output_img = (img_stretched * max_val).astype(dtype)

        # save the result
        out_path = os.path.join(output_folder, filename)
        tifffile.imwrite(out_path, output_img)

        print(f"Enhanced and saved: {out_path}")