"""
Transformada de Fourier con numpy (np.fft): ver el espectro de magnitud y
aplicar un filtro paso alto (HPF) poniendo a cero las frecuencias bajas
del centro. Lo que queda son los bordes.
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

CAT_PATH = "cat.jpg"


def main() -> None:
    img_color = cv2.imread(CAT_PATH)
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))

    plt.subplot(121), plt.imshow(img, cmap="gray")
    plt.title("Input Image"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude_spectrum, cmap="gray")
    plt.title("Magnitude Spectrum"), plt.xticks([]), plt.yticks([])
    plt.show()
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    fshift[crow - 30 : crow + 30, ccol - 30 : ccol + 30] = 0
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    plt.subplot(131), plt.imshow(img, cmap="gray")
    plt.title("Input Image"), plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(img_back, cmap="gray")
    plt.title("Image after HPF"), plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(img_back)
    plt.title("Result in JET"), plt.xticks([]), plt.yticks([])

    plt.show()


if __name__ == "__main__":
    main()
