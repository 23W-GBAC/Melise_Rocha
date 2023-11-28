

# Description

{% capture readme_content %}{% include_relative README.md %}{% endcapture %}
{{ readme_content | markdownify }}

# Dealing With Nifti Data

{% capture nifti_data_content %}{% include_relative Reading a nifti file.md %}{% endcapture %}
{{ nifti_data_content | markdownify }}
