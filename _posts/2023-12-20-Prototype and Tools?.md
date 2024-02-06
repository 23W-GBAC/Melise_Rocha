20.12.2023

Hello everyone, 

So I have been researching some of the Python tools I could use and what are the main things I need to do to preprocess a MRI file. 


## Python Libraries Designed for Image Processing 

### Nibabel

Nibabel stands out as a versatile Python library tailored for reading and writing neuroimaging file formats, including the used NIfTI format.

### OpenCV

OpenCV is the most widely used library in tasks of image processing, and object detection. It can be used for almost everything regarding 2D images, if used for MRI analysis, the slices should be given as input files, instead of the whole image. Pay attention that Open-CV only supports 2D vectors.

### ITKSnap

I found this very interesting software which is free and can be used for MRI file visualization, segmentation, and use its measuring tools.

### Numpy

Numpy is a powerful open-source library in Python for numerical and mathematical operations. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays. To deal with MRI files we convert them to arrays for image manipulation.

### SimpleITK

SimpleITK, or the Simple Insight Segmentation and Registration Toolkit, is a simplified layer built on top of the Insight Segmentation and Registration Toolkit (ITK). ITK is a powerful open-source software library for medical image analysis, segmentation, and registration. This library can be used in Python, but is constructed using C language, and I found it a bit difficult to find proper documentation regarding this.


## What do I need to do?

After reading some articles regarding image pre-processing I realized that I needed to include the steps mentioned below, and also some problems I found trying to design codes for them. Please notice that the codes shown here are all old codes and the final ones are covered in other post. 

### Voxel Size Normalization 

A voxel, short for "volume element," is the three-dimensional counterpart to a pixel in two-dimensional images. While a pixel represents the smallest unit of a digital image in the x and y dimensions, a voxel represents the smallest unit in three-dimensional space, encompassing the x, y, and z dimensions.

The problem is that some of the files I found in OASIS had voxel size of (1, 1, 1), while others were sized (1, 1, 1.2).

My first approach to this problem was this python code: 
```python
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

def normalize_voxel_size(img, target_voxel_size):
    nifti_img = nib.load(img)

    current_voxel_size = np.array(nifti_img.header.get_zooms()[:3])

    resizing_factor = current_voxel_size / target_voxel_size

    resampled_data = zoom(nifti_img.get_fdata(), resizing_factor)

    new_nifti_img = nib.Nifti1Image(resampled_data, affine=None)

    new_nifti_img.header.set_zooms(target_voxel_size)

    return new_nifti_img

input_nifti_path = "your_input_nifti_path.nii"
output_nifti_path = "your_output_nifti_path.nii"
target_voxel_size = (1.0, 1.0, 1.0)

normalized_image = normalize_voxel_size(input_nifti_path, target_voxel_size)

nib.save(normalized_image, output_nifti_path)


```
 The problem with this approach is that it changes the number of slices according to the original number of slices in the file. So it was creating another random variable, which leads me to the next point!

 ### All files should have the same number of slices 

 In a pre-processing step, we should make that files come out all with the same number of slices. Some images are for example (240, 176, 256)

### Bias Field Correction 

Bias field signal is a low-frequency and very smooth signal that corrupts MRI images specially those produced by old MRI machines. The SimpleITK library has a filter specially designed for this, which is the one I decided to use. For testing purposes you can use the following code:


```python
import SimpleITK as sitk

def bias_field_correction(input_image_path, output_image_path):
    # Load the image
    input_image = sitk.ReadImage(input_image_path)

    # Create N4ITK bias field correction filter
    corrector = sitk.N4BiasFieldCorrectionImageFilter()

    # Set the input image
    corrector.SetInputImage(input_image)

    # Run the correction
    output_image = corrector.GetOutput()

    # Save the corrected image
    sitk.WriteImage(output_image, output_image_path)

# Example usage
input_image_path = "input_image.nii.gz"
output_image_path = "output_image.nii.gz"
bias_field_correction(input_image_path, output_image_path)


```

### Intensity normalization 

The image is divided into multiple equally sized voxels. Each voxel in the image represents a discrete area in your sample and has an associated intensity value, so that in grayscale lower intensities appear very dark (black) and higher intensities appear very light (white). 0 is the black and 255 is the white, with all gray tones going from 0 to 255. However, looking at some images from OASIS3 dataset I realized that the intensity was not normalized, with intensities going from 0 to 750. This is not according to the normal standards and the histogram of intensity distribution was very weird. I have used the following python code to see the histogram:


```python
import nibabel as nib
import matplotlib.pyplot as plt


nifti_file_path = ""
img = nib.load(nifti_file_path)

# Get voxel data
data = img.get_fdata()

# Flatten the 3D data to a 1D array
voxel_values = data.flatten()


plt.hist(voxel_values, bins=100, color='blue', alpha=0.7)
plt.title('Voxel Intensity Histogram')
plt.xlabel('Intensity')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()


```
And the result was this: 

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/5ffc49ab-cbec-415e-abf9-26f6f562a223)

I considered using the following code for image normalization:

```python
import cv2
import nibabel as nib
import numpy as np

def normalize_intensity(img):
    # Perform intensity normalization (you can customize this based on your requirements)
    img_min = np.min(img)
    img_max = np.max(img)
    normalized_img = (img - img_min) / (img_max - img_min) * 255.0

    return normalized_img.astype(np.uint8)

nifti_file_path = 'path/to/your/file.nii.gz'
nifti_img = nib.load(nifti_file_path)
nifti_data = nifti_img.get_fdata()

normalized_data = normalize_intensity(nifti_data)
normalized_nifti_img = nib.Nifti1Image(normalized_data, nifti_img.affine)
normalized_nifti_path = 'path/to/your/normalized_file.nii.gz'
nib.save(normalized_nifti_img, normalized_nifti_path)

```

Then we can successfully normalize the intensity and save the normalized files.


### Noise Correction

Talking about noise correction is difficult as there are multiple methods to do it and it is difficult to define the most appropriate. We have two types of noise: 

#### The background noise: 

This can be removed by creating a white mask of the region with the largest contours (which will be the head for sure) and applying it in the image, so you can remove the noise.

#### The foreground image noise:

The scikit-image library restoration package counts with a number of denoising methods, these are three: 

- denoise_bilateral: This method performs bilateral filtering, which is a non-linear, edge-preserving filter. It smoothens the image while preserving edges by considering both spatial closeness and intensity similarity
- denoise_tv_chambolle: This method applies Total Variation denoising using the Chambolle algorithm. Total Variation denoising is effective for preserving edges while reducing noise.
- denoise_wavelet: This method performs denoising using wavelet thresholding. It decomposes the image into wavelet coefficients, applies thresholding to remove noise, and then reconstructs the image.

The total variation one seems to be the most appropriate as it is the one that keeps the edges the most preserved and we do not want to damage the contour of any brain region. I will leave the code I used to test three of them here: 


```python
import nibabel as nib
from skimage.restoration import denoise_bilateral, denoise_tv_chambolle, denoise_wavelet

def apply_denoising_methods(input_path):

    nifti_img = nib.load(input_path)
    nifti_data = nifti_img.get_fdata()


    denoised_bilateral = denoise_bilateral(nifti_data, sigma_color=0.1, sigma_spatial=15, channel_axis=-1)
    denoised_tv_chambolle = denoise_tv_chambolle(nifti_data, weight=0.1, channel_axis=-1)
    denoised_wavelet = denoise_wavelet(nifti_data, sigma=0.1, channel_axis=-1)


    nib.save(nib.Nifti1Image(denoised_bilateral, nifti_img.affine), "/path/to/save")
    nib.save(nib.Nifti1Image(denoised_tv_chambolle, nifti_img.affine), "/path/to/save")
    nib.save(nib.Nifti1Image(denoised_wavelet, nifti_img.affine), "/path/to/save")


input_nifti_path = '/path/to/yourfile.nii.gz'


apply_denoising_methods(input_nifti_path)

```

Honestly, I did not see a huge difference between the denoised image and the original one... But I am sure "computers will see it".

Now, I need to develop a pipeline integrating and improving some of the functions in this prototype for a full version. I will work on it during the week and comeback next week with the news!

Cheers, 

Melise Rocha
