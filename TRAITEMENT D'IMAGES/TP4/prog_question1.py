# importing the module cv2
import cv2

# reading the image using imread() function from cv2 module and converting it into gray image
readimage = cv2.imread("mecque.jpg")
# ------------
# -----------------------
grayimage = cv2.cvtColor(readimage, cv2.COLOR_BGR2GRAY)
# creating a sift object and using detectandcompute() function to detect the keypoints and descriptor from the image
siftobject = cv2.SIFT_create()
keypoint, descriptor = siftobject.detectAndCompute(grayimage, None)
# -----------------------
# keypoints The detected keypoints. A 1-by-N structure array with the following fields:
# 	pt coordinates of the keypoint [x,y]
# 	size diameter of the meaningful keypoint neighborhood
# 	angle computed orientation of the keypoint (-1 if not applicable); it's in
#   [0,360) degrees and measured relative to image coordinate system
#   (y-axis is directed downward), i.e in clockwise.
# 	response the response by which the most strong keypoints have been selected.
#   Can be used for further sorting or subsampling.
# 	octave octave (pyramid layer) from which the keypoint has been extracted.
# 	class_id object class (if the keypoints need to be clustered by an object
#   they belong to).

print(keypoint[0].pt)
print(keypoint[1].size)
print(keypoint[3].size)
print(keypoint[5].size)
print(keypoint[8].size)
print(keypoint[11].angle)
print(keypoint[0].response)
print(descriptor[12])


# drawing the keypoints and orientation of the keypoints in the image and then displaying
# the image as the output on the screen
keypointimage = cv2.drawKeypoints(
    readimage, keypoint, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)
cv2.imshow("SIFT", keypointimage)
cv2.waitKey()
cv2.imwrite("sift_keypoints.jpg", keypointimage)
