---
layout: default
description: Usin Python to plot the conten of MRI Nifti files 
---
December 12th 2023

In this tutorial I will teach you how to use Python to plot the slices of an MRI file. Keep in mind the following that in a position (x, y, z):

* x = axes1/ sagittal plane
* y = axes2/ coronal plane
* z = axes3/ axial plane

# Let's go coding!

Make sure to have nibabel and matplotlib.pylot libraries installed. 

```python
import nibabel as nib
import matplotlib.pyplot as plt

file = nib.load("/path/to/yout/niftifile.nii.gz")
img_data = file.get_fdata()

slice_index = 130 # Select the slice you want to see

# Plot the slices
plt.figure(figsize=(10, 5))

# Plot along the x-axis
plt.subplot(131)
plt.imshow(img_data[slice_index, :, :], cmap='gray')
plt.title(f'Sagittal {slice_index}')

# Plot along the y-axis
plt.subplot(132)
plt.imshow(img_data[:, slice_index, :], cmap='gray')
plt.title(f'Coronal {slice_index}')

# Plot along the z-axis
plt.subplot(133)
plt.imshow(img_data[:, :, slice_index], cmap='gray')
plt.title(f'Axial {slice_index}')

plt.tight_layout()
plt.show()

```
You should expect to see something similar to it:

![download (15)](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/be11ad4c-3fea-4d3a-86bd-fe54ef17502e)

# Why this code works?
The image is first loaded using nib.load(), then we extract the data from it using get_fdata() function. After it, we have to decide which slice we want to see, remember python is a zero based language so if my image has 256 slices it will count from 0-255. Therefore slice 130, actually displays slice 129 counting from 1 to 256!
After that, we use matplolib.pyplot to plot the images, and select the color map as gray, you can also try cmap = 'bone', it is pretty cool. 

# What if I want to see all slices? 
Then you would need another library, called NiLearn.

```python
from nilearn import image as nii
from nilearn import plotting

img = nii.mean_img(
    "/path/to/yout/niftifile.nii.gz"
)
view = plotting.view_img(img, cmap='gray')
view.open_in_browser()

```
This code will pop a browse viewer of your MRI file.
