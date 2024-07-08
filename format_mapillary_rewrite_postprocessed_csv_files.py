
import os
import csv

def load_required_image_names(file_path):
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f)

def filter_and_renumber_csv(full_csv_path, required_image_names, output_path):
    with open(full_csv_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        writer.writerow(header)
        
        new_rows = []
        for idx, row in enumerate(reader):
            image_name = row[1]  # Assuming the image name is the second column
            if image_name in required_image_names:
                new_row = [len(new_rows)] + row[1:]  # Update the first column to be the new index
                new_rows.append(new_row)
        
        writer.writerows(new_rows)

def main():
    city = 'sf'
    if city == 'cph':
        base_dir = '/scratch/saishubodh/segments_data/VPR-datasets-downloader_MSLS_CPH/datasets/mapillary_sls/msls_images_val/train_val/cph'
    elif city == 'sf':
        base_dir = '/scratch/saishubodh/segments_data/VPR-datasets-downloader_MSLS_SF/datasets/mapillary_sls/msls_images_val/train_val/sf'
    
    # Load required image names
    required_image_names = load_required_image_names(f'/home/saishubodh/2023/segment_vpr/VPR-datasets-downloader/msls_npy_files/database_{city}_image_names.csv')
    required_image_names.update(load_required_image_names(f'/home/saishubodh/2023/segment_vpr/VPR-datasets-downloader/msls_npy_files/query_{city}_image_names.csv'))
    
    # Define paths to full CSV files and output paths
    csv_files = [
        ('database/raw.csv', f'{base_dir}/database/raw_filtered.csv'),
        ('query/raw.csv', f'{base_dir}/query/raw_filtered.csv'),
        ('database/postprocessed.csv', f'{base_dir}/database/postprocessed_filtered.csv'),
        ('query/postprocessed.csv', f'{base_dir}/query/postprocessed_filtered.csv')
    ]
    
    for full_csv_rel_path, output_path in csv_files:
        full_csv_path = os.path.join(base_dir, full_csv_rel_path)
        filter_and_renumber_csv(full_csv_path, required_image_names, output_path)

if __name__ == "__main__":
    main()
