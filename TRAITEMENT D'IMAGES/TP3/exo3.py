import numpy as np
import cv2


image = cv2.imread("images/image2.png", cv2.IMREAD_GRAYSCALE)

filter_2D = np.array(
    [
        [[1], [4], [6], [4], [1]],
        [[4], [16], [24], [16], [4]],
        [[6], [24], [36], [24], [6]],
        [[4], [16], [24], [16], [4]],
        [[1], [4], [6], [4], [1]],
    ]
) * (1 / 256)
convolved_image = cv2.filter2D(image, -1, filter_2D)
cv2.imshow("Original Image", image)
cv2.imshow("Convolved Image", convolved_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

gaussian_y = np.array([[1], [4], [6], [4], [1]])
gaussian_x = np.array([[1, 4, 6, 4, 1]])
gaussian_2D = np.dot(gaussian_y, gaussian_x) * (1 / 256)
convolved_image = cv2.filter2D(image, -1, gaussian_2D)
cv2.imshow("Original Image", image)
cv2.imshow("Convolved Image", convolved_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
