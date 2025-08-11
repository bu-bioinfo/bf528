---
title: "Using Conda with VSCode and Jupyter Notebooks"
layout: single
---

# Overview

It can be helpful to work directly in VSCode and Jupyter Notebooks when developing
your pipelines. This will enable you to take advantage of both the features of VSCode
and Jupyter Notebooks to make your development process more efficient. 

Just like for our nextflow processes, we will want to carefully define a conda
environment for the analysis we will be performing in our jupyter notebooks. These
analyses being done in your notebook can often be some of the most biologically 
relevant and interesting results. It is critically important that these analyses
are reproducible and transparent. 

## VSCode Requirements

You will need to install the following extensions for VSCode:

- Python
- Jupyter Notebook

You can install these extensions by opening the extensions view in VSCode
(View > Extensions) and searching for the extensions listed above. 

## Conda Environment

We will again be utilizing YML files to define our conda environments. In 
addition to the packages we need for our analysis, we will also need to install
the ipykernel package to enable our jupyter notebook to access the conda environment.

An example YML file may look something like:

```yml
name: notebook_env
channels:
  - conda-forge
  - bioconda
dependencies:
  - ipykernel
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - scanpy
  ```

You will then need to manually create the conda environment. Assuming you had
saved the file as `notebook_env.yml`, you can create the environment by running:

```bash
conda env create -f notebook_env.yml
```


## VSCode

If you open up VSCode, you can make a jupyter notebook. All this entails is
making a new file and saving it with a `.ipynb` extension. The jupyter extension
will automatically recognize this as a jupyter notebook and enable all of the
standard jupyter notebook features. 

