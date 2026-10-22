"""
Filtros paso alto (HPF) en el dominio espacial: convolución con kernels de
3x3 y 5x5, y HPF restando a la imagen su versión desenfocada (Gaussian).
"""

import cv2
import numpy as np
from scipy import ndimage

IMG_PATH = "statue_small.jpg"


def main() -> None:
    kernel_3x3 = np.array(
        [
            [-2, 0, 2],
            [-1, 0, 1],
            [-2, 0, 2],
        ]
    )
    kernel_5x5 = np.array(
        [
            [-1, -1, -1, -1, -1],
            [-1, 1, 2, 1, -1],
            [-1, 2, 4, 2, -1],
            [-1, 1, 2, 1, -1],
            [-1, -1, -1, -1, -1],
        ]
    )
    img = cv2.imread(IMG_PATH, cv2.IMREAD_GRAYSCALE)
    k3 = ndimage.convolve(img, kernel_3x3)
    k5 = ndimage.convolve(img, kernel_5x5)
    blurred = cv2.GaussianBlur(img, (17, 17), 0)
    g_hpf = img - blurred
    cv2.imshow("3x3", k3)
    cv2.imshow("5x5", k5)
    cv2.imshow("blurred", blurred)
    cv2.imshow("g_hpf", g_hpf)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
