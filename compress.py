import sys
import os
import numpy as np
from PIL import Image
import argparse

import pgm


def svd(data):
    return np.linalg.svd(data)


def dispCompressInfo(height, width, s, compressed_s_num):
    print("image height:", height, ", width:", width)
    print('singular value of image:' +
          str(s)+', compressed singular value:'+str(compressed_s_num))
    print('image size before compression:'+str(height*width/1024)+'KB')
    print('image size after compression:' +
          str(compressed_s_num*(height+width)/1024)+'KB')
    print('compression ratio:'+str(compressed_s_num*(height+width)/(height*width)))


def compressR(data, ratio=0.5):
    '''compress matrix given ratio of singular values to retain'''
    (u, s, v) = svd(data)
    compressed_s_num = int(np.ceil(s.shape[0]*ratio))
    dispCompressInfo(data.shape[0], data.shape[1],
                     s.shape[0], compressed_s_num)
    return u[:, 0:compressed_s_num], s[0:compressed_s_num], v[0:compressed_s_num, :]


def compressN(data, compressed_s_num):
    '''compress matrix given number of singular values to retain'''
    (u, s, v) = svd(data)
    dispCompressInfo(data.shape[0], data.shape[1],
                     s.shape[0], compressed_s_num)
    return u[:, 0:compressed_s_num], s[0:compressed_s_num], v[0:compressed_s_num, :]


def geneMatFromSVD(u, s, v):
    '''generate the matrix of the image using SVD'''
    height = u.shape[0]
    width = v.shape[1]
    compressed_matrix = np.zeros((height, width))
    for count in range(s.shape[0]):
        compressed_matrix += s[count] * np.matmul(
            u[:, count].reshape(height, 1), v[count, :].reshape(1, width))
    return compressed_matrix


def showImage(matrix):
    img = Image.fromarray(matrix)
    img.show()


def saveImage(matrix, form, pgmFileName, compressed_s_num):
    img = Image.fromarray(matrix).convert('L')
    filename = pgmFileName.split(
        '.')[0] + '_s_' + str(compressed_s_num) + '.' + form
    img.save(filename, form)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("pgmFile", help="the pgm image to be compressed")
    parser.add_argument("-q", "--quite", action="store_true",
                        help="compress the image without displaying")
    parser.add_argument("-s", "--save", type=str,
                        help="save the compressed image as designated format")
    group.add_argument("-r", "--ratio", type=float,
                       help="the ratio of singular values to retain, default 0.5")
    group.add_argument("-n", "--num", type=int,
                       help="the number of singular values to retain")
    args = parser.parse_args()

    with open(args.pgmFile, 'rb') as pgmf:
        data = pgm.read_pgm(pgmf)
    if args.ratio:
        (u, s, v) = compressR(data, args.ratio)
    elif args.num:
        (u, s, v) = compressN(data, args.num)
    else:
        (u, s, v) = compressR(data)

    compressed_matrix = geneMatFromSVD(u, s, v)

    if not args.quite:
        showImage(compressed_matrix)

    if args.save:
        saveImage(compressed_matrix, args.save, args.pgmFile, s.shape[0])
