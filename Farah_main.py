# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 21:38:07 2020

@author: MajidKhoshrou
"""

import skimage
import numpy
from skimage.morphology import closing, square
import matplotlib.pyplot as plt
from matplotlib import cm

from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
import numpy as np


im = skimage.io.imread(f'C:/Users/MajidKhoshrou/Documents/python_scripts/Farah/images/img1.jpg', as_gray=True)
im = skimage.util.invert(im)
skimage.io.imshow(im)

x = numpy.argmax(numpy.sum(im, axis=0))
y = numpy.argmax(numpy.sum(im, axis=1))

im2 = numpy.zeros(im.shape)
im2[:,x]=im[:,x]
im2[y,:]=im[y,:]
skimage.io.imshow(im2)


temp = np.array([1,1,1,1])
result = skimage.feature.match_template(im,temp)
ij = numpy.unravel_index(numpy.argmax(result), result.shape)
x, y = ij[::-1]

thresh=.7
im2 = im > thresh
skimage.io.imshow(im2)

im2 = skimage.morphology.dilation(im)
skimage.io.imshow(im2)

im3 = im-im2
skimage.io.imshow(im3)




