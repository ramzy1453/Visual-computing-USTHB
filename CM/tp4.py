import cv2
import numpy as np
from math import inf
import time
from utils import *

padding = 16
min_value = 50

img1 = cv2.imread("image072.png")
gray_frame_1 = cv2.cvtColor(img1, cv2.COLOR_BGR2YCrCb)[:, :, 0]

img2 = cv2.imread("image092.png")
gray_frame_2 = cv2.cvtColor(img2, cv2.COLOR_BGR2YCrCb)[:, :, 0]

border_img_1, border_img_1_gray, border_img_2 = make_images(padding)

block_one = []
block_two = []


start = time.time()

residual_frame = np.zeros((1080 + 128, 1920 + 128)).astype(np.uint8)


def dico_search(block1, block1_one_kordds, step, i, j, block_one, block_two):
    block = block1_one_kordds
    while step >= 1:
        kord = []
        minimum = inf
        kord.append(
            [block[0] - step, block[1] - step, block[2] - step, block[3] - step]
        )
        kord.append(
            [block[0] - step, block[1] - step, block[2] + step, block[3] + step]
        )
        kord.append([block[0] - step, block[1] - step, block[2], block[3]])
        kord.append(
            [block[0] + step, block[1] + step, block[2] + step, block[3] + step]
        )
        kord.append([block[0] + step, block[1] + step, block[2], block[3]])
        kord.append(
            [block[0] + step, block[1] + step, block[2] - step, block[3] - step]
        )
        kord.append([block[0], block[1], block[2] - step, block[3] - step])
        kord.append([block[0], block[1], block[2], block[3]])
        kord.append([block[0], block[1], block[2] + step, block[3] + step])

        for one_kord in kord:
            neighbour = border_img_1_gray[
                one_kord[0] : one_kord[1], one_kord[2] : one_kord[3]
            ]
            mse = MSE(neighbour, block1)
            if mse < minimum:
                minimum = mse
                block = one_kord

        step = step // 2
    if minimum > min_value:
        similar_neighbor = border_img_1_gray[block[0] : block[1], block[2] : block[3]]
        residual_frame_ = block1 - similar_neighbor
        residual_frame[i : i + padding, j : j + padding] = residual_frame_

        block_one.append(block1_one_kordds)
        block_two.append(block)


for i in range(0, gray_frame_2.shape[0] - padding, padding):
    for j in range(0, gray_frame_2.shape[1] - padding, padding):
        block1 = gray_frame_2[i : (i + padding), (j) : (j + padding)]
        block1_one_kordds = [
            i + padding * 4,
            (i + padding) + padding * 4,
            j + padding * 4,
            (j + padding) + padding * 4,
        ]
        step = padding * 4
        dico_search(block1, block1_one_kordds, step, i, j, block_one, block_two)


# for pixel in block_one:
#     img1 = cv2.rectangle(
#         border_img_1, (pixel[2], pixel[0]), (pixel[3], pixel[1]), (0, 255, 255), 4
#     )

for subpixel in block_two:
    img2 = cv2.rectangle(
        img2,
        (subpixel[2] - padding * 4, subpixel[0] - padding * 4),
        (subpixel[3] - padding * 4, subpixel[1] - padding * 4),
        (255, 255, 0),
        4,
    )


# cv2.imshow("FRAME 1", img1)
cv2.imshow("FRAME 2", img2)
cv2.waitKey(0)
