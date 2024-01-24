import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("image072.png", cv2.IMREAD_COLOR)
img2 = cv2.imread("image092.png", cv2.IMREAD_COLOR)

box_coordinates = []
padding = 50


def draw_rect(event, x, y, flags, param):
    global box_coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        box_coordinates = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:
        box_coordinates.append((x, y))


cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_rect)

while True:
    img_copy = img.copy()
    # Dessiner la boîte rouge dans l'image de référence
    if len(box_coordinates) == 2:
        red_cords = {
            "p1": (box_coordinates[0][0], box_coordinates[0][1]),
            "p2": (box_coordinates[1][0], box_coordinates[1][1]),
        }
        cv2.rectangle(
            img_copy,
            red_cords["p1"],
            red_cords["p2"],
            (0, 0, 255),
            2,
        )

        # Dessiner la boîte verte dans l'image à rechercher
        green_cords = {
            "p1": (box_coordinates[0][0] - padding, box_coordinates[0][1] - padding),
            "p2": (box_coordinates[1][0] + padding, box_coordinates[1][1] + padding),
        }
        cv2.rectangle(
            img2,
            (green_cords["p1"]),
            (green_cords["p2"]),
            (0, 255, 0),
            2,
        )

        red_size = (
            red_cords["p2"][0] - red_cords["p1"][0],
            red_cords["p2"][1] - red_cords["p1"][1],
        )
        green_size = (
            green_cords["p2"][0] - green_cords["p1"][0],
            green_cords["p2"][1] - green_cords["p1"][1],
        )

    cv2.imshow("image", img_copy)

    # Sortir de la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

red_img = img[
    red_cords["p1"][1] : red_cords["p2"][1],
    red_cords["p1"][0] : red_cords["p2"][0],
]

# Animation de la boîte rouge se déplaçant dans l'image à rechercher
min_mse = float("inf")
min_mse_point = None

for y in range(green_size[1] - red_size[1]):
    for x in range(green_size[0] - red_size[0]):
        img2_copy = img2.copy()

        # Dessiner la boîte rouge à chaque position dans la boite verte

        cv2.rectangle(
            img2_copy,
            (x + green_cords["p1"][0], y + green_cords["p1"][1]),
            (
                x + green_cords["p1"][0] + red_size[0],
                y + green_cords["p1"][1] + red_size[1],
            ),
            (0, 0, 255),
            2,
        )

        block = img2[
            y + green_cords["p1"][1] : y + green_cords["p1"][1] + red_size[1],
            x + green_cords["p1"][0] : x + green_cords["p1"][0] + red_size[0],
        ]

        mse = np.sum((red_img.astype("float") - block.astype("float")) ** 2)
        if mse < min_mse:
            min_mse = mse
            min_mse_point = (x + green_cords["p1"][0], y + green_cords["p1"][1])

        cv2.putText(
            img2_copy,
            f"MSE : {mse}",
            (x + green_cords["p1"][0], y + green_cords["p1"][1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
        )

        cv2.imshow("Image 2 Animation", img2_copy)
        cv2.waitKey(1)  # Délai entre chaque frame (en ms)

        # Quand je termine on dessine le mse_min_point
img2_copy = cv2.imread("image092.png", cv2.IMREAD_COLOR)
cv2.rectangle(
    img2_copy,
    min_mse_point,
    (min_mse_point[0] + red_size[0], min_mse_point[1] + red_size[1]),
    (0, 0, 255),
    2,
)

cv2.putText(
    img2_copy,
    f"MSE : {min_mse}",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 0),
    2,
)
while True:
    cv2.imshow("Image 2 Animation", img2_copy)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
