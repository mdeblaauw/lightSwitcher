# lightSwitcher

## This repo is tested on built with Python3

## Setup Snowboy model for hot word detection

You can use the Snowboy resources from this repo or set it up yourself using the following steps:

1. brew install swig portaudio sox.
2. Make sure to install packages from requirements.txt from this repo.
3. git clone <https://github.com/Kitt-AI/snowboy.git>.
4. cd to snowboy/swig/Python3 and enter command make (This makes a python wrapper).
5. open snowboy/examples/Python3/snowboydecoder.py.
6. change "from . import snowboydetect" to "import snowboydetect" and save.
7. copy files from "snowboy/swig/Python3/" to your project dictionary.
8. copy dictionary snowboy/resources to your project dictionary (This dictionary contains the hot word models).
9. copy file "snowboydecoder.py" and "demo.py" from "snowboy/examples/Python3/snowboydecoder.py" to your project dictionary.
10. You can now test snowboy by running "demo.py sources/models/snowboy.umdl" in command line.