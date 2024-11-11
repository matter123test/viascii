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
usage: main.py [-h] [-v VIDEO] [-a] [-av AUDIOVOLUME] [-i] [-rt] [-g GRAYSCALE] [-d DIMENSIONS] [-s SAVEPATH] [-r READ] [-st STARTIN] [-ed ENDIN] [-im IMAGE] [-ir] [-an ANGLE] [-c CONTRAST]

Video to ascii converter

options:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        The path of the video
  -a, --audio           Enable audio
  -av AUDIOVOLUME, --audiovolume AUDIOVOLUME
                        Change the audio volume
  -i, --inverted        Reverse the ascii grayscale string
  -rt, --rtemp          Removes created audio file
  -g GRAYSCALE, --grayscale GRAYSCALE
                        Custom grayscale string
  -d DIMENSIONS, --dimensions DIMENSIONS
                        Dimensions in the format (x,y)
  -s SAVEPATH, --savepath SAVEPATH
                        Saves the ascii frames into a text file
  -r READ, --read READ  Reads the ascii frames from a text file
  -st STARTIN, --startin STARTIN
                        Starts from a specific frame
  -ed ENDIN, --endin ENDIN
                        Ends the process on a specific frame
  -im IMAGE, --image IMAGE
                        The path of the image
  -ir, --isrgb          This only applies to images
  -an ANGLE, --angle ANGLE
                        Changes the image angle
  -c CONTRAST, --contrast CONTRAST
                        Set the contrast of the foreground text
```

Example command:

```python viascii.py -v bad_apple.mp4 --audio -rt```

With the custom dimensions (the default value is (100, 50)):

```python viascii.py bad_apple.mp4 --audio -rt --dimensions=120,70"```

Reading ascii frames from a file:

```python viascii.py -r frames.txt``` 

Converting image to ascii:

<img src=water_melon_cat.png width="100"></img>

```python viascii.py -im water_melon_cat.png --dimensions=50,100 --isrgb --contrast 10```
