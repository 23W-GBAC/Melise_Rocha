Hello!!

I am here to present the final version of my MRI preprocessor pipeline. As I had already finished the python code for it, carefully explained [here](https://23w-gbac.github.io/Melise_Rocha/2023/12/28/Explaining-each-of-the-functions-in-the-pipeline.html).

The Pipeline will do the steps described in the workflow below: 

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/c6a6b13a-8407-443d-af29-5271b302e9e2)


At first I was using the code below to run the preprocessor: 

```python

from utils import image_processing


img_path = "path/to/my/niftifile.nii.gz"

processed_image = image_processing(img_path)

nifti_img = nib.Nifti1Image(processed_image, affine=None)   

nib.save(nifti_img, '/path/to/save/processedimage.nii.gz')

```
However, I identified two problems with this code and I will cover how I adressed it to develop the final solution!

1) It was not very user-friendly or attractive to the final customers
2) I could not apply this to a large dataset! It only works for single files, and regarding image processing we will deal with multiple files at the same time most of the time!

## Creating a HTML webpage for the project 

I was actually having a class about Flask when I clicked that I could use it to create a simple page where the person can just upload a file from the computer and then Download the image already preprocessed! This would make everything easier and very user friendly! 

So I built a Flask application that allows you to: 

1) Select a file from your computer - only accepts .nii.gz extension - which is the NIFTI extension
2) Click on ```upload``` button and this will automatically start the preprocessing step, which takes roughly 1 and a half minute
3) The image will automatically be saved in the Downloads folder of your computer with the original filename + "_normalized_image.nii.gz"
4) If you click in Download button it will also Download it in Downloads folder.

Here you can see the screen visible to the user: 

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/c67d8fc7-46a2-46d9-8fda-a45467e899d7)

And after finishing the processing: 

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/ef7f88f5-c8db-425d-a12f-0db54e82c8bf)


I had everything ready to make the website online and available for everyone! I have tried [pythonanywhere.com](https://www.pythonanywhere.com/) but the libraries required exceeded the space I could use for free in their sever! 

Then, I tried [Heroku](https://www.heroku.com) but I could not create an account and this seems to be a global problem! 

For now, the application is only accesible by cloning the [github project](https://github.com/23W-GBAC/Melise_Rocha) and using the IDE you prefer to run the script app.py, so it will use your local machine as the host!

I will try to find other possibilities and comeback with updates!

## Creating a run_multi.py 

Thinking about a real scenario situation, where multiple files need to be pre processed at the same time I created the ```run_multi.py``` script, which is shown below: 

```python
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


input_folder = "/path/to/input_folder"
output_folder = "/path/to/output_folder"


process_images(input_folder, output_folder)
```
This code will iterate through each .nii.gz file in a input folder, and save it as already preprocessed images with the original filename + "_normalized_image.nii.gz" in the output folder! So you can process a whole dataset just using this script! Very fast and practical isn't it? 

## Showcasing images before and after preprocessing

Here I will show some slices of images before and after being preprocessed by the pipeline described in this post! It is interesting that those images were in the "LAS" orientation before and the code fixed it to the "RAS" orientation!

Example 1: Comparing The Coronal View

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/96903fb6-ff88-4735-894f-4f3bd93a1f86)

Example 2: Comparing the Axial View


![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/caf59f04-354d-4415-b716-e939cc36ed11)

Example 3: Comparing the Sagittal View

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/e9e830d1-61aa-4889-b96f-db29de1d4692)


The images are visible better and the most important is that they will be all following the same standard! Therefore, they can be easily used to train any Artificial Intelligence model! 

## Where to find the scripts?

Although the project is not available online yet, you can find all the scripts to use this application in the [github project](https://github.com/23W-GBAC/Melise_Rocha)! 

Feel free to comment if you have any question! 

Cheers,

Melise Rocha
