"""
Transformada de Fourier con OpenCV (cv2.dft): ver el espectro de magnitud y
aplicar un filtro paso bajo (LPF) con una máscara que solo deja pasar las
frecuencias bajas del centro. El resultado es la imagen desenfocada.
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

CAT_PATH = "cat.jpg"


def main() -> None:
    img_color = cv2.imread(CAT_PATH)
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude_spectrum = 20 * np.log(
        cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
    )

    plt.subplot(121), plt.imshow(img, cmap="gray")
    plt.title("Input Image"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude_spectrum, cmap="gray")
    plt.title("Magnitude Spectrum"), plt.xticks([]), plt.yticks([])
    plt.show()
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols, 2), np.uint8)
    mask[crow - 30 : crow + 30, ccol - 30 : ccol + 30] = 1

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    plt.subplot(121), plt.imshow(img, cmap="gray")
    plt.title("Input Image"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img_back, cmap="gray")
    plt.title("Image after LPF"), plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == "__main__":
    main()
