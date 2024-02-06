18.01.2024

Hello everyone, 

I am here today to give an overview of the project, covering the advantages and disadvantages!

## From where I left 

Coming back to what I talked about in [this](https://23w-gbac.github.io/Melise_Rocha/2023/12/14/Why-creating-an-automatic-MRI-preprocessing-tool.html) post, I have experienced using FreeSurfer and fMRIprep for neurological imaging preprocessing, Although these are robust pipelines they take a very long time (8+ hours) to process a NIFTI Image file.

I have future plans to train deep neural network models, for example the UNET, for segmenting different brain regions. As you guys probably know deep neural networks need a lot of data to be trained. If I wanted to use it to process 100 MRI files it would take me 800 hours (33 days!), this amount of time is unbelievable!

I did not know any libraries appropriate for 3D file manipulation, except for the nibabel one! So I needed to learn how to work with a number of other python libraries (SimpleITK, scikit-image, OpenCV and Numpy) to create a preprocessing pipeline with the features I wanted.



## How long it took to be ready? 

In general, it took me one month to finish this project - around 45 working hours - most of this time I spent researching about the libraries and whether they already had pre-made functions to perform the steps I needed to! It was difficult to come up with the best version of each function. 

## The result 

I was able to create a pipeline with amazing results, as showcased in this [post](https://23w-gbac.github.io/Melise_Rocha/2024/01/07/The-final-result.html), which will process an image in 1 minute and 30 seconds, as opposed to 8 hours from other pipelines. Making it a great tool for basic image preprocessing in AI training!

## Best Advantages 

1) Significant Time Savings: The most notable advantage of our preprocessing pipeline is its efficiency. While traditional methods such as FreeSurfer and fMRIprep take upwards of 8 hours to process a single NIFTI image file, our pipeline can accomplish the same task in just 1 minute and 30 seconds. This represents an astonishing time reduction of over 95%.
   
2) Customization and Flexibility: a lot of functions in the pipeline come with parameters that can be selected by the user, such as voxel size, image size, weight of denoising method and bias field correction! Allowing for some changes if the user is not satisfied with the result.
   
3) Scalability: it does not matter which brain region I will segment, I can use the same pipeline to preprocess all of the files! There is also the possibility to process a whole dataset just with one script!
   
4) Standardization: I am sure the same preprocessing steps will be followed for every image which is FUNDAMENTAL for dataset construction in Artificial Intelligence!
   
5) Efficiency: I can allocate time for further research if I automate the preprocessing step and do not need to monitor it!

"As nothing is only flowers..." - In Portuguese, we say "Como nada é só flores..." literally translating  To give the bad news - I will also cover the downsides of this project:

## Disadvantages 

1) Changes are difficult to make and at the moment require a lot of technical knowledge so it is not very user-friendly
   
2) A lot of updates will need to be made to keep up with the most recent tools of image processing from different libraries
   
3) It is not available online yet

## There is room for improvement

1) Making the choices and parameters easier to set through a configuration file instead of direct changes to the code
   
2) Develop an optional tool to also apply the preprocessing steps to already manually segmented masks
   
3) Adding more preprocessing steps - for example more denoising methods - so the user can choose the best fit!
   
4) Collaborating with domain experts: Partnering with neuroscientists, radiologists, and other domain experts can enrich the pipeline's functionality by incorporating domain-specific knowledge and insights. 

## Final Thoughts

I would say it was definitely worth developing it, as now I do not need to worry about any processing step, I do not need to run multiple functions and I can process a whole dataset just with a run command in an IDE and go out to do anything else! A lot of time is being saved for me and the tool is very straight forward and practical for developers already used to coding.


