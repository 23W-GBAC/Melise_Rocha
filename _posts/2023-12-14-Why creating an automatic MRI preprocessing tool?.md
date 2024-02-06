14.12.2023


Hey everyone!

Today I am here to talk about the main motivation behind this project.

As I was researching Alzheimer's Disease I noticed that MRI images of the brain are not usually saved as DICOM files, but NIFTI files. And the fact that they are saved in NIFTI causes a lack of effective preprocessing tools for them.

## First of all, what is a NIFTI file?

The Neuroimaging Informatics Technology Initiative (NIFTI) file format was envisioned about a decade ago as a replacement to the then widespread, yet problematic, analyze 7.5 file format. The main problem with the previous format was perhaps the lack of adequate information about orientation in space, such that the stored data could not be unambiguously interpreted. 
Perhaps the most visible consequence of the lack of orientation information was the then-reigning confusion between the left and right sides of brain images during the years in which the analyze format was dominant.
The new format was defined in two meetings of the so-called Data Format Working Group (DFWG) at the National Institutes of Health (NIH), one in 31 March and another in 02 September of 2003. NIFTI images usually
come with a header, the header is responsible for storing information regarding the image orientation and image transformations. In the NIfTI format, the first three dimensions are reserved to define the three spatial dimensions — x, y and z —, while the fourth dimension is reserved to define the time points — t. Other dimensions store voxel-specific distributional parameters and vector-based data.

## What is the difference between DICOM and NIFTI?

If you know about radiology, you have certainly already heard about the DICOM standard — Digital Imaging and Communications in Medicine (DICOM) — which is used to exchange images and information and has been around for over 20 years. The use of the DICOM format started to take off in the mid-nineties. DICOM comes with several support layers, allowing image senders and receivers to exchange information about the analyzed images.


### 1) DICOM is more widespread

DICOM is a more widely used image format in the healthcare profession, with a wide range of specialist fields deploying it, including radiology (for CT, X-Ray, MRI, Ultrasound, and RF), pathology, dermatology, endoscopy, and ophthalmology. NIFTI was created to solve a serious spatial orientation problem in neuroimaging, focusing on functional magnetic resonance imaging (fMRI). With NIFTI, neurosurgeons can quickly identify image objects, such as the right or left side of the brain, in 3D. It’s an invaluable asset when analyzing human brain images, a notoriously difficult organ to assess and annotate. 

### 2) Less metadata in NIFTI files

With a NIFTI file, you don’t need to populate the same number of tags (integer pairs) that DICOM image files require. There’s a lot less metadata to sift through and analyze.

### 3) DICOM works with 2D layers, whereas NIfTI can display 3D detail

With NIFTI files, images, and other data is stored in a 3D format. It’s specifically designed this way to overcome spatial orientation challenges of other medical image file formats.

On the other hand, DICOM image files and the associated data are made up of 2D layers. This allows you to view different slices of an image, which is especially useful when analyzing the human body and various organs. 


## Artificial Intelligence and NIFTI files

In recent years with the boom of Artificial Intelligence, a lot of AI-based software for brain image processing has been developed. I will mention briefly two of them here: Free Surfer and fMRI prep.

### FreeSurfer

FreeSurfer is a set of tools providing comprehensive and automated analyses of major regions of the human brain. It includes volumetric segmentation of most macroscopically visible brain structures, hippocampal subfield segmentation, intersubject alignment based on cortical folding patterns, white matter tract segmentation using diffusion magnetic resonance, cortical folding pattern parcellation, architectural boundary estimation from in vivo data, mapping cortical gray matter thickness, and construction of models of the human cerebral cortex surface. In the end, you will get a pre processed MRI file. masks with different brain regions already segmented and files with information regarding the volume of each structure.

### fMRI prep

fMRIPrep is a functional magnetic resonance imaging (fMRI) data preprocessing pipeline that is designed to provide an easily accessible, state-of-the-art interface that is robust to variations in scan acquisition protocols and that requires minimal user input, while providing easily interpretable and comprehensive error and output reporting. It performs basic processing steps (coregistration, normalization, unwarping, noise component extraction, segmentation, skull-stripping, etc.) providing outputs that can be easily submitted to a variety of group level analyses, including task-based or resting-state fMRI, graph theory measures, and surface or volume-based statistics of cortical regions.


### My personal experience with both

I had a NIFTI file and I tried to use both tools. In general, I would say they are very difficult to use and although there are tutorials available they did not cover most of the errors I found during the installation process. It also requires a lot of computational processing. I have a Dell notebook with 1TB disk space and 32GB RAM, using only CPU it took me 8 hours to finish one Free Surfer MRI image and 10 hours in fMRI prep.


## Why did I decide to create a preprocessing MRI tool? 

As mentioned previously it took me 8+ hours to process an MRI file using FreeSurfer and fMRIprep. While FreeSurfer and fMRIprep are powerful tools with a broad scope, I discerned that for specific tasks, especially those not requiring the segmentation of cortical regions, their application might be excessive. 

Talking about a real-world scenario, consider a situation where the ambition is to train a deep neural network model for segmenting the hippocampus. You will certainly need a preprocessing step for the images in your dataset. As the challenge arises when dealing with datasets from neuroimaging databases like OASIS3 and ADNI.  These datasets present a myriad of complexities – varying equipment, diverse professionals capturing the images, discrepancies in the number of slices, distinct voxel sizes, and a lack of standardization.

Utilizing raw images for training AI models under these circumstances becomes a formidable task. However, for me, it seems a huge waste of time using FreeSurfer and fMRI prep just to standardize images and surprisingly, while DICOM image files have garnered significant attention in the realm of fast preprocessing due to their popularity, NIFTI image files seemed to linger in the shadows.

Then, decided to try to create a preprocessor that could be faster, more accessible, and effective for my personal use. I will describe the process in this blog, so stay tuned!

Cheers, 

Melise Rocha

