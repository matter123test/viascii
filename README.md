# Introduction

viascii is an video to ascii converter

__SAMPLE VIDEO:__

[![Video Title](https://img.youtube.com/vi/gYzZu_EXCgI/0.jpg)](https://www.youtube.com/watch?v=gYzZu_EXCgI)

# Installation Guide
To download the repository:

```git clone https://github.com/matter123test/viascii.git```

Then you need to install the basic dependencies to run the project on your system:
```
cd viascii
pip install -r requirements.txt
```

# Usage
```
usage: main.py [-h] [-a] [-i] [-rt] [-g GRAYSCALE] [-d DIMENSIONS] [-s SAVEPATH] video

Video to ascii renderer

positional arguments:
  video                 The path of the video

options:
  -h, --help            show this help message and exit
  -a, --audio           Enable audio
  -i, --inverted        Reverse the ascii grayscale string
  -rt, --rtemp          Removes created audio file
  -g GRAYSCALE, --grayscale GRAYSCALE
                        Custom grayscale string
  -d DIMENSIONS, --dimensions DIMENSIONS
                        Dimensions in the format (x, y)
  -s SAVEPATH, --savepath SAVEPATH
                        Saves the ascii frames into a text file
```

Example command:

```python viascii.py bad_apple.mp4 --audio -rt```

Or with the custom dimensions (the default value is (100, 50)):

```python viascii.py bad_apple.mp4 --audio -rt --dimensions="(120,70)"```
