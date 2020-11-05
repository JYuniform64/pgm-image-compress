# IMAGE COMPRESSION USING SVD

A simple program to compress `.pgm` image using SVD.
For me it is used in Yale Face Database.

## Usage
```
usage: compress.py [-h] [-q] [-s SAVE] [-r RATIO | -n NUM] pgmFile

positional arguments:
  pgmFile               the pgm image to be compressed

optional arguments:
  -h, --help            show this help message and exit
  -q, --quite           compress the image without displaying
  -s SAVE, --save SAVE  save the compressed image as designated format
  -r RATIO, --ratio RATIO
                        the ratio of singular values to retain, default 0.5
  -n NUM, --num NUM     the number of singular values to retain
```