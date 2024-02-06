from typing import Union
import numpy as np
import SimpleITK as sitk
import cv2
from skimage.restoration import denoise_tv_chambolle
import nibabel as nib
from nibabel.processing import conform

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