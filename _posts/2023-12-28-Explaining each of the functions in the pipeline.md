
28.12.2023

Hello Everyone!!

Today I am here to describe each of the functions in the pipeline separately and in details! 

To use the functions in this post you will need the following libraries and imports: 

```python
from typing import Union
import numpy as np
import SimpleITK as sitk
import cv2
from skimage.restoration import denoise_tv_chambolle
import nibabel as nib
from nibabel.processing import conform
```

## The auxiliary functions 

I have created two auxiliary functions to convert from a numpy array to Sitk Image object and vice versa. This is because to work with SimpleITK library you need to have sitk image and to work with other libraries you would need a numpy array. So I constantly needed to covert the files and outputs between those two libraries. Below are the two auxiliary functions: 

```python
def sitk_to_ndarray(src: sitk.Image) -> np.ndarray:
    """
    Converts a SimpleITK Image to a NumPy array.
    Parameters
    ----------
    src : sitk.Image
        The input SimpleITK Image.
    Returns
    -------
    np.ndarray
        The converted NumPy array.
    """
    img = sitk.GetArrayFromImage(src)
    return img

```
This function converts a SimpleITK Image to a NumPy array. 

```sitk.GetArrayFromImage(src)```: This line extracts the pixel data from the SimpleITK image src and converts it into a NumPy array. It is a function already implemented in SimpleITK library.

The second one is accepting two inputs, a numpy array that will be converted to a SimpleITK image and a SimpleITK image that can change the datatype. Changing the SimpleITK data image type is important because some libraries will only work with specific data types, OpenCV for example mostly works with UINT8 data type. 

```python
def ndarray_to_sitk(
    src: Union[np.ndarray, sitk.Image], dtype=sitk.sitkFloat32
) -> tuple[sitk.Image, sitk.Image]:
    """
    Converts a NumPy array or SimpleITK Image to SimpleITK Image.
    Parameters
    ----------
    src : Union[np.ndarray, sitk.Image]
        The input NumPy array or SimpleITK Image.
    dtype : int or sitk.PixelIDValueEnum, optional
        The desired pixel type of the output image.
        Defaults to sitk.sitkFloat32.
    Returns
    -------
    tuple[sitk.Image, sitk.Image]
        A tuple of the input image and the converted image.
    Raises
    ------
    ValueError
        If the src image is not of types numpy.ndarray or SimpleITK.Image.
    """
    if isinstance(src, np.ndarray):
        input_img = sitk.GetImageFromArray(src)
        converted = sitk.Cast(input_img, dtype)
    elif isinstance(src, sitk.Image):
        input_img = deepcopy(src)
        converted = sitk.Cast(src, dtype)
    else:
        raise ValueError(
            "The src image must be of types numpy.ndarray or"
            "SimpleITK.Image "
        )
    return input_img, converted
```

If the input image is a numpy array it will use the function ```sitk.GetImageFromArray``` to get the sitk image from the array. If the input image is a sitk image already it will only change the datatype using the ```sitk.Cast``` function. 

If you want to convert straight away a nifti image from your computer to a SimpleITK image or to a numpy array you can use the following: 

```python
# Nifti to Numpy

import nibabel as nib

img = nib.load("path/to/your/niftiimage.nii.gz")

img_array = img.get_fdata() # Here you get the numpy array 

```

```python
# Nifti to Simple ITK

import SimpleITK as sitk


image_path = 'path/to/your/niftiimage.nii.gz'

image = sitk.ReadImage(image_path) # Already read as a sitk image

```
## Image Processing Functions 

### Background Stripping 

This is a very good strategy to remove noise from the background, as the background is not necessary. Using this function you will get a "head mask" that you can use to extract the foreground, but I will explain everything in details. 

First of all. the function: 

```python
def background_stripping(
    src: Union[np.ndarray, sitk.Image]
) -> tuple[np.ndarray, np.ndarray]:
    """
    Performs background stripping on a 3D image to separate the
    foreground.
    Parameters
    ----------
    src : Union[np.ndarray, sitk.Image]
        The input 3D image as a NumPy array or SimpleITK Image.
    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing the segmented image and the head mask as
        NumPy arrays.
    """
    raw, img = ndarray_to_sitk(src=src, dtype=sitk.sitkFloat32)
    transformed = sitk.LiThreshold(img, 0, 1)
    transformed = sitk.BinaryMorphologicalClosing(
        image1=transformed, kernelRadius=(3, 3, 3)
    )
    head_mask = sitk.BinaryFillhole(transformed)
    segmented_img = sitk.Mask(image=raw, maskImage=head_mask)

    return sitk_to_ndarray(segmented_img), sitk_to_ndarray(head_mask)
```

1) It will accept a SimpleITK image and a numpy array as input, which is then converted to a SimpleITK image.
2) It will perform a simple thresholding operation using the filter ```sitk.LiThreshold```. For those of you who are not familiar with thresholding operations, it sets a "threshold value" if the voxel intensity is below that value it is converted to black and if it is above it is converted to white. So. you get a binary (black and white image). The optimal threshold is already automatically calculated by the ```sitk.LiThreshold```.   
3) After the threshold I have noticed some small holes in the mask due to the automatic threshold that was set. I asked ChatGPT what I could do to fill the holes and he showed me the ```sitk.BinaryMorphologicalClosing```image filter. The closing operation dilates an image and then erodes the dilated image, using the same structuring element for both operations. Morphological closing is useful for filling small holes in an image while preserving the shape and size of large holes and objects in the image.
4) The ```sitk.BinaryFillhole``` will "double ensure that there is not even a single small hole in the head mask generated"
5) The code will then return the mask and the mask applied to the image as the segmented image.

Just to clarify: In the context of image processing and computer vision, a mask is indeed a binary file or, more commonly, a binary image representing areas of interest within an image or a defined spatial region. A mask essentially serves as a stencil or a template that indicates which parts of an image should be included or excluded in further processing or analysis. When you multiply an image by a mask you will extract the region in the image represented by the mask!

Example of head mask generated by this code: 

![image](https://github.com/23W-GBAC/Melise_Rocha/assets/127310708/00067c9b-8d66-4d4a-b1b6-5638314271cb)

### Bias Field Correction

Bias field signal is a low-frequency and very smooth signal that corrupts MRI images specially those produced by old MRI machines. Image processing algorithms such as segmentation, texture analysis or classification that use the graylevel values of image pixels will not produce satisfactory results. A pre-processing step is needed to correct for the bias field signal before submitting corrupted MRI images to such algorithms or the algorithms should be modified.

I used the following function for Bias Field Correction: 

```python
def bias_field_correction(
    src: Union[np.ndarray, sitk.Image],
    head_mask: Union[np.ndarray, sitk.Image] = None,
    shrinkFactor: int = 4,
):
    """
    Performs bias field correction on a 3D image.
    Parameters
    ----------
    src : Union[np.ndarray, sitk.Image]
        The input 3D image as a NumPy array or SimpleITK Image.
    head_mask : Union[np.ndarray, sitk.Image], optional
        The head mask as a NumPy array or SimpleITK Image. Defaults to None.
    shrinkFactor : int, optional
        The shrink factor for downsampling the image. Defaults to 4.
    Returns
    -------
    np.ndarray
        The bias field corrected image as a NumPy array.
    """
    _, img = ndarray_to_sitk(src=src, dtype=sitk.sitkFloat32)
    transformed = sitk.RescaleIntensity(img, 0, 255)
    if isinstance(head_mask, np.ndarray) or isinstance(head_mask, sitk.Image):
        _, head_mask = ndarray_to_sitk(src=head_mask, dtype=sitk.sitkUInt8)
        head_mask = sitk.RescaleIntensity(head_mask, 0, 255)
    else:
        head_mask = sitk.LiThreshold(img, 0, 1)

    transformed = sitk.Shrink(img, [shrinkFactor] * transformed.GetDimension())
    mask_image = sitk.Shrink(
        head_mask, [shrinkFactor] * transformed.GetDimension()
    )

    bias_corrector = sitk.N4BiasFieldCorrectionImageFilter()

    _ = bias_corrector.Execute(transformed, mask_image)

    log_bias_field = bias_corrector.GetLogBiasFieldAsImage(img)
    corrected_image_full_resolution = img / sitk.Exp(log_bias_field)

    return sitk_to_ndarray(corrected_image_full_resolution)
```

1) It will accept a SimpleITK image and a numpy array as input, which is then converted to a SimpleITK image.
2) There is the optional headmask parameter to limit the area of Bias Field correction.
3) Normalization of image intensities from 0-255 using the ```sitk.RescaleIntensity```
4) The downsampling ocurring in ```transformed = sitk.Shrink(img, [shrinkFactor] * transformed.GetDimension())``` is not mandatory and it is only being used to save computational power, as I want a fast tool.
5) The N4BiasFieldCorrectionImageFilter from SimpleITK is applied to the downsampled image using the head mask if provided. This step estimates and removes the bias field from the image.
6) The bias-corrected image is reconstructed to the original resolution by dividing it by the exponential of the log bias field.

There is not visible difference between the original image and the bias field corrected one!




### Denoising the foreground

I used the already implemented ```denoise_tv_chambolle```  function from ```scikit-image```. This function is specifically designed to remove noise from images using the Total Variation denoising method. The Total Variation method works by minimizing the total variation of the image, which represents the sum of the gradients of the image intensity. The basic idea is that smooth regions of the image have low total variation, while edges and details have higher total variation. The ```denoise_tv_chambolle``` function is based on Chambolle's algorithm, which is an efficient iterative method for solving Total Variation denoising problems.

```python
def tv_chambolle(
    img: np.ndarray,
    weight: float = 0.06,
    channel_axis: int = -1,
    **kwargs: any,
) -> np.ndarray:
    """
    Applies total variation denoising using the Chambolle method.
    Parameters
    ----------
    img : np.ndarray
        The input image.
    weight : float, optional
        The weight parameter of the denoising algorithm. Defaults to 0.06.
    channel_axis : int, optional
        The axis corresponding to the color channels. Defaults to -1.
    **kwargs : Any
        Additional keyword arguments.
    Returns
    -------
    np.ndarray
        The denoised image.
    """
    tv = denoise_tv_chambolle(
        image=img, weight=weight, channel_axis=channel_axis, **kwargs
    )
    return tv
```
You will give an input image, decide the weight parameter (The greater the weight, the more denoising (at the expense of fidelity to image).) and the channel_axis is set to -1 because the MRI image is RGB, meaning 3 color channels, and this function can only deal with gray-scale images with only one color channel. Setting to -1 means considering only one color channel out of the three.

### Normalizing and applying CLAHE

I created a function that normalizes the image and also applies the CLAHE ( Contrast Limited Adaptive Histogram Equalization). Enhancing the contrast of an image is a common task. One technique to achieve this is Histogram Equalization (HE), which redistributes pixel intensities to cover the entire dynamic range of the image. However, traditional HE doesn't always perform well in situations where the image has regions with varying contrast levels. Contrast Limited Adaptive Histogram Equalization (CLAHE) addresses this limitation by performing HE locally, thereby preserving local contrast. CLAHE is an extension of Histogram Equalization that limits the amplification of the histogram through the specification of a clipping limit. This ensures that the contrast enhancement does not lead to noise amplification or artifacts in regions with low contrast. By dividing the image into small tiles, CLAHE computes a separate histogram for each tile and redistributes pixel values based on these local histograms.

```python
def equalize_adptive_3D(
    src: np.ndarray,
    clipLimit: float = 0.03,
    tileGridSize: tuple = (8, 8),
    **kwargs
) -> np.ndarray:
    equalized_data = np.zeros_like(src)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)

    # Loop through the channels (assuming the last dimension represents channels)
    for idx in range(src.shape[-1]):
        # Normalize the image to the range [0, 255]
        img = cv2.normalize(
            src[..., idx],
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX,
            dtype=cv2.CV_32F,
        )
        img = img.astype(np.uint8)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        equalized_data[..., idx] = clahe.apply(img).astype(np.float64)

    return equalized_data
```
1) The function will take as input a numpy array.
2) It initializes an output array equalized_data with the same shape as the input using the ```np.zeros_like(src)```
3) It creates a CLAHE object using ```cv2.createCLAHE```, specifying the clipLimit and tileGridSize
4) Normalize each channel of the image using ```cv2.normalize```
5) Applies CLAHE to the normalized image using ```clahe.apply```and save it to the equalized_data array created in the beggining

## Voxel size normalization, number of slices normalization and fixing orientation error 

For me, this was the most difficult part! Until I found a function from nibabel library that could do it for me and I just used it.

```python
from nibabel.processing import conform

nibabel.processing.conform(from_img, out_shape=(256, 256, 256), voxel_size=(1.0, 1.0, 1.0), order=3, cval=0.0, orientation='RAS', out_class=None)
```
You can select the number of slices using the out_shape parameter and the voxel size!

## Joining everything 

I created the following function for joining everything together: 

```python

def image_processing(file_path):
    img_path = nib.load(file_path)
    img_conformed = conform(from_img=img_path, orientation="RAS", order=0)
    img_conformed_array = img_conformed.get_fdata()
    segmented_img, head_mask = background_stripping(img_conformed_array)
    bias_corrected_img = bias_field_correction(src=segmented_img)
    denoised_img = tv_chambolle(img=bias_corrected_img)
    normalized_image = equalize_adptive_3D(src=denoised_img)
    nifti_img = nib.Nifti1Image(normalized_image, affine=None)

    return nifti_img
```
As you can see, you can give one image as input and then it will perform all the process mentioned in this code and return the final image already pre-processed! 

Cheers, 

Melise Rocha


