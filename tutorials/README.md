# Getting Started

## Installation

SuperAnnotate Python SDK is available on PyPI.  

```
pip install superannotate
```

To support COCO annotation format converters following packages need to be installed

```Python
pip install "git+https://github.com/cocodataset/panopticapi.git"
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
```

The package officially supports *Python 3.6+* and was tested under *Linux* and *Windows (Anaconda)* platforms.

## Authorization


Note that SDK functions work within the team scope of SuperAnnotate web platform thus a team level authorization is required.   
Follow the steps below to authorize SDK in a given team scope  

1. Get the authorization token from team’s [settings page](https://app.superannotate.com/team)  
![token](/figures/token.gif)  
Note that the token section is available only for team owners with *PRO* membership.   

2. Run `superannotate init` in terminal and plug obtained token as requested.  
This will authorize SDK and create config file with provided token in default location *~/.superannotate/config.json*.  

## Tutorials

As SDK is installed and initialized you can check through *jupyter notebooks* below on multiple examples of SDK functionalities.  

* [Working with Projects](./projects.ipynb)
* [Working with Images](./images.ipynb)
* [Working with Videos](./videos.ipynb)
* [Working with Annotations](./annotations.ipynb)
* [Working with Annotation Formats](./convertors.ipynb)
* [Working with Exported Annotations](./analytics.ipynb)
* [Working with Prediction Models](./models.ipynb)

