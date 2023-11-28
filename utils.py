import nibabel as nib

def read_nifti_file(file_path):
    try:
        nifti_img = nib.load(file_path)
        return nifti_img
    except Exception as e:
        print(f"Error reading NIfTI file: {e}")
        return None
