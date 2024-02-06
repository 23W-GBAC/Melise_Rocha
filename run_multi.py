import os
import shutil
from utils import image_processing

def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".nii.gz"):
            input_path = os.path.join(input_folder, filename)
            output_filename = filename.replace(".nii.gz", "_normalized_image.nii.gz")
            output_path = os.path.join(output_folder, output_filename)

            
            processed_image = image_processing(input_path)

            
            with open(output_path, "wb") as output_file:
                output_file.write(processed_image)

            print(f"Processed {filename} and saved as {output_filename}")


input_folder = "/home/enacom/Segmentação_fissura_coroide_esquerdo"
output_folder = "/home/enacom/Downloads/teste_preprocessing"


process_images(input_folder, output_folder)
