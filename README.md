# Melise_Rocha
# How can we improve MRI images quality?
Preprocessing MRI images to enhance their quality and remove noise is a critical step in preparing the data for computational analysis. Several techniques are employed in this preprocessing stage to ensure the reliability and accuracy of subsequent computational processes. Here are some of the pre-processing steps we can do using python programming language to increase image quality:Overview

## Noise Reduction: 
Utilize Gaussian smoothing, median filtering, and wavelet denoising techniques to reduce inherent noise in MRI images.
Techniques:

Gaussian Smoothing: This method uses a Gaussian filter to blur the image slightly, reducing high-frequency noise while preserving structural information.

Median Filtering: It replaces each pixel's value with the median value of neighboring pixels, effective in reducing impulse noise or salt-and-pepper artifacts.

Wavelet Denoising: Utilizes wavelet transforms to decompose the image into different frequency components, allowing selective denoising in specific frequency bands.

## Bias Field Correction
Bias fields cause intensity variations across an MRI image due to imperfections in the imaging process. Correcting this bias is essential for accurate analysis and segmentation of structures within the image.

Methods:
N4ITK Correction: Non-parametric non-uniform intensity normalization (N4ITK) is an algorithm that estimates and corrects intensity non-uniformity in MRI images.

Polynomial Fitting: This method fits a polynomial surface to the intensity variations within the image, allowing for correction based on this modeled bias field.

## Image Registration
Image registration involves aligning multiple MRI images, sequences, or images from different time points/modalities to a common reference space. Accurate registration is crucial for combining information and performing comparative analysis.

Techniques:
Rigid Registration: Aligns images by translation, rotation, and scaling without distorting the image.

Affine Registration: More flexible than rigid registration, allowing for shearing and non-uniform scaling in addition to translation and rotation.

Nonlinear Registration: Accommodates more complex deformations in images, crucial when aligning images with substantial anatomical differences.

Intensity Normalization
Standardizing intensity values across MRI scans or subjects ensures consistency, facilitating accurate comparison and analysis between different datasets.

## Normalization Methods:
Z-Score Normalization: Rescales intensities to have a mean of zero and a standard deviation of one, making the data comparable across scans.

Histogram Matching: Matches the intensity distributions of different images, aligning their histograms to a reference image's histogram.

I aim to create a pipeline performing all these steps in an MRI file. 
