import numpy as np
import cv2
from matplotlib import pyplot as plt

# Code from:
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html

# Prepared for M1IV students, by Prof. Slimane Larabi
#===================================================

img1 = cv2.imread('imquery.png',0)          # queryImage
img2 = cv2.imread('imModel.jpg',0) # trainImage

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
print(des1[0],kp1[0].pt)

# BFMatcher with default params

# create BFMatcher object
bf = cv2.BFMatcher()

# Match descriptors.
matches = bf.match(des1,des2)

# sort the matches based on distance
matches = sorted(matches, key=lambda val: val.distance)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:5], None, flags=2)

plt.imshow(img3),plt.show()