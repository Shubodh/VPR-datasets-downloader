

import numpy as np
import os

def save_city_image_names(base_path, city, image_names, query_or_ref):
    # Prepare file path
    if query_or_ref == 'query':
        file_path = os.path.join(base_path, f'query_{city}_image_names.csv')
    else:
        file_path = os.path.join(base_path, f'database_{city}_image_names.csv')
    
    # Write to CSV
    with open(file_path, 'w') as f:
        for name in image_names:
            f.write(f"{name}\n")
    print(f"File written: {file_path}")

def process_images(npy_file_path, query_or_ref):
    base_path = os.path.dirname(npy_file_path)
    # Load the npy file
    if query_or_ref == 'query':
        qIdx = np.load(base_path+'/msls_val_qIdx.npy')

        # hard coded query image names.
        qImages_all = np.load(npy_file_path)  #Has 747 images, 7 unnecessary images
        data = qImages_all[qIdx]# Has 740 images    #print(len(msls_dataset.qImages[msls_dataset.qIdx]))
    else:
        data = np.load(npy_file_path)
    
    # Prepare lists to store image names by city
    cph_images = []
    sf_images = []
    
    # Process each entry
    for entry in data:
        parts = entry.split('/')
        if len(parts) > 2:
            city = parts[1]  # the city part
            image_name = parts[-1].split('.')[0]  # the image name without extension
            
            if city == 'cph':
                cph_images.append(image_name)
            elif city == 'sf':
                sf_images.append(image_name)
    
    # Save to respective files
    save_city_image_names(base_path, 'cph', cph_images, query_or_ref)
    save_city_image_names(base_path, 'sf', sf_images, query_or_ref)

# Specify the path to the npy file


# This code rewrites the npy files into simple csv files such that it doesn't have 1000s of query images and instead just has some 500 or so as used in standard VPR benchmarls

query_or_ref = 'query'

db_npy_path = '/home/saishubodh/2023/segment_vpr/VPR-datasets-downloader/msls_npy_files/msls_val_dbImages.npy'
query_np_path = '/home/saishubodh/2023/segment_vpr/VPR-datasets-downloader/msls_npy_files/msls_val_qImages.npy'


if query_or_ref == 'query':
    process_images(query_np_path, 'query')
else:
    process_images(db_npy_path, 'ref')
