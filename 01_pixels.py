"""
Una imagen es un array de numpy: crear una imagen negra, cambiar un píxel
y pasarla de gris (1 canal) a BGR (3 canales).
"""

import cv2
import numpy as np

# COLORS IN BGR
GREEN = (0, 255, 0)
RED = (0, 0, 255)


def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def zoom(img):
    # INTER_NEAREST keeps the pixels sharp instead of blurring them
    return cv2.resize(img, (500, 500), interpolation=cv2.INTER_NEAREST)


def main():
    # BLACK IMAGE 3x3
    print("BLACK")
    img = np.zeros((3, 3), dtype=np.uint8)
    print(img)
    print("SHAPE", img.shape)
    show_image("BLACK", zoom(img))

    # UPDATE ONE PIXEL
    print("UPDATE ONE PIXEL")
    img[1, 1] = 100
    print(img)
    show_image("UPDATE ONE PIXEL", zoom(img))

    # GRAY2BGR
    print("GRAY2BGR")
    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_bgr[0, 0] = np.array(GREEN)
    img_bgr[2, 2] = np.array(RED)
    print(img_bgr)
    print("SHAPE", img_bgr.shape)
    show_image("GRAY2BGR", zoom(img_bgr))


if __name__ == "__main__":
    main()
