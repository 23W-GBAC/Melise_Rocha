---
layout: default
description: Reading MRI Nifti files using Nibabel Library-The Basics
---
# Exploring MRI Images with Nibabel in Python - Printing the header
## I am going to teach you how to use Python Nibabel Library to read MRI NIFTI files!

Medical imaging is crucial for understanding the complexities of the human body. Python offers powerful libraries like Nibabel that facilitate the manipulation and analysis of medical imaging data, particularly MRI images.

## The Nibabel Library
Nibabel is a Python library designed for working with neuroimaging data formats such as NIfTI and ANALYZE, commonly used in MRI studies. It simplifies the process of handling these images, making it an indispensable tool for researchers and practitioners in the field.

## Let's go for the coding 
 Make sure you've installed Nibabel in your Python environment (pip install nibabel) before running this code. You need to give the local path of your MRI file.
 ```python 
import nibabel as nib

# Path to your MRI image file (.nii or .nii.gz)
file_path = 'path/to/your/image.nii.gz'

# Load the MRI image using nibabel
img = nib.load(file_path)

# Access the image header
header = img.header

# Print the header information
print("=== MRI Image Header ===")
print(header)

```
## Expected output and what it means

=== MRI Image Header ===
<class 'nibabel.nifti1.Nifti1Header'> object, endian='<'
sizeof_hdr      : 348
data_type       : b''
db_name         : b''
extents         : 0
session_error   : 0
regular         : b'r'
dim_info        : 54
dim             : [  3 256 256 256   1   1   1   1]
intent_p1       : 0.0
intent_p2       : 0.0
intent_p3       : 0.0
intent_code     : none
datatype        : int16
bitpix          : 16
slice_start     : 0
pixdim          : [1.        0.9999969 1.        1.        1.        1.        1.
 1.       ]
vox_offset      : 0.0
scl_slope       : nan
scl_inter       : nan
slice_end       : 0
slice_code      : unknown
xyzt_units      : 10
cal_max         : 0.0
cal_min         : 0.0
slice_duration  : 0.0
toffset         : 0.0
glmax           : 0
glmin           : 0
descrip         : b'removed'
aux_file        : b'OAS30007_MR_d0061'
qform_code      : scanner
sform_code      : scanner
quatern_b       : 0.02209956
quatern_c       : -0.006747844
quatern_d       : -0.029405959
qoffset_x       : -96.02453
qoffset_y       : -101.31679
qoffset_z       : -141.76294
srow_x          : [ 9.9817634e-01  5.8472525e-02 -1.4785964e-02 -9.6024529e+01]
srow_y          : [-5.9068836e-02  9.9729377e-01 -4.3771345e-02 -1.0131679e+02]
srow_z          : [ 1.2186491e-02  4.4565056e-02  9.9893212e-01 -1.4176294e+02]
intent_name     : b''
magic           : b'n+1'

