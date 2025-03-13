import utils.image_handler as image_handler
import SimpleITK as sitk
import pandas as pd
import os
from tqdm import tqdm

def patching(data: dict):
    print(data)
    DATA_DIR = data['data']
    CSV_PATH = data['csv']
    OUTPUT_PATH = data['out']
    annots = pd.read_csv(CSV_PATH)
    files = [file for file in os.listdir(DATA_DIR) if file[-4:] == '.mhd']
    cube_dimensions = (50, 50, int(50*0.57))

    for file in tqdm(files):
        coord_rows = annots[annots['seriesuid']==file[:-4]]

        for index, row in enumerate(coord_rows.iterrows()):
            x,y,z = row[1][1:4]

            patch, start_index, extract_size = image_handler.extract_cube(
                os.path.join(DATA_DIR, file),
                (x, y, z),
                cube_dimensions
                )
            path = os.path.join(OUTPUT_PATH, file[:-4]+"_"+str(index)+".mhd")
            
            try:
                sitk.WriteImage(patch, path)
            except RuntimeError as e:
                print(f"{file} - {index}: One patch failed")