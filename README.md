# Introduction

viascii is a video to ascii converter

__SAMPLE VIDEOS:__

[![Video Title](https://img.youtube.com/vi/gYzZu_EXCgI/0.jpg)](https://www.youtube.com/watch?v=gYzZu_EXCgI)
[![Video Title](https://img.youtube.com/vi/21dyw6Qk27E/0.jpg)](https://www.youtube.com/watch?v=21dyw6Qk27E)

# Installation

To download the repository:

```git clone https://github.com/matter123test/viascii.git```

Then you need to install the basic dependencies to run the project on your system:

```
cd viascii
pip install -r requirements.txt
```

Finally you need to install ffmpeg, which is required for splitting audio from video files:
(setup.py will automatically download ffmpeg to the project folder)

```
python setup.py
```

# Usage

```
usage: run.py [-h] [-v VIDEO] [-a] [-av AUDIOVOLUME] [-i] [-rt] [-g GRAYSCALE] [-d DIMENSIONS] [-s SAVEPATH] [-r READ] [-st STARTIN] [-ed ENDIN] [-im IMAGE] [-ir] [-an ANGLE] [-c CONTRAST]

Video to ascii converter

options:
  -h, --help            show this help message and exit
  -v, --video VIDEO     The path of the video
  -a, --audio           Enable audio
  -av, --audiovolume AUDIOVOLUME
                        Change the audio volume
  -i, --inverted        Reverse the ascii grayscale string
  -rt, --rtemp          Removes created audio file
  -g, --grayscale GRAYSCALE
                        Custom grayscale string
  -d, --dimensions DIMENSIONS
                        Dimensions in the format (x,y)
  -s, --savepath SAVEPATH
                        Saves the ascii frames into a text file
  -r, --read READ       Reads the ascii frames from a text file
  -st, --startin STARTIN
                        Starts from a specific frame
  -ed, --endin ENDIN    Ends the process on a specific frame
  -im, --image IMAGE    The path of the image
  -ir, --isrgb          This only applies to images
  -an, --angle ANGLE    Changes the image angle
  -c, --contrast CONTRAST
                        Set the contrast of the foreground text
```

Example command:

```python run.py -v bad_apple.mp4 --audio -rt```

With the custom dimensions (the default value is (100, 50)):

```python run.py bad_apple.mp4 --audio -rt --dimensions=120,70```

Reading ascii frames from a file:

```python run.py -r frames.txt``` 

Converting image to ascii:

```python run.py -im water_melon_cat.png --dimensions=50,100 --isrgb --contrast 10```
