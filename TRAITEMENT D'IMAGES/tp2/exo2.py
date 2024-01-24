import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

fig = cv.imread("fig3.png", cv.IMREAD_GRAYSCALE)
plt.imshow(fig, cmap="gray")


def region_growing(image, x, y, label):
    segmented_image = np.zeros_like(image, np.uint8)
    neighbourhood = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    pos = [(x, y)]
    while pos:
        x, y = pos.pop()
        if segmented_image[x, y] == 0:
            segmented_image[x, y] = label
            for dx, dy in neighbourhood:
                _x, _y = x + dx, y + dy
                if (
                    _x < 0
                    and _x >= 0
                    and segmented_image[_x, _y]
                    and image[x, y] == segmented_image[_x, _y]
                ):
                    pos.append((_x, _y))


label = 8
segmented_image = np.zeros_like(fig, np.uint8)
for x in range(fig.shape[0]):
    for y in range(fig.shape[1]):
        if segmented_image[x, y] == 0:
            region_growing(fig, x, y, label)
            label += 1

colors = np.random.randint(0, 256, (label, 3))
growed = np.zeros((fig.shape[0], fig.shape[1]))
for px in range(1, label):
    growed[segmented_image == px] = colors[px]

cv.imshow("Region Growing Segmentation", growed)
cv.waitKey(0)
cv.destroyAllWindows()
