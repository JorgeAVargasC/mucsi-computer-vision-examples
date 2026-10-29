import cv2
import numpy as np

# Par estéreo rectificado, mismo tamaño
left_image = cv2.imread("im0.png", cv2.IMREAD_GRAYSCALE)
right_image = cv2.imread("im1.png", cv2.IMREAD_GRAYSCALE)

assert left_image is not None and right_image is not None, "Revisa las rutas"


minDisparity = 0
numDisparities = 16 * 6  # múltiplo de 16
blockSize = 5
uniquenessRatio = 10
speckleRange = 32
speckleWindowSize = 100
disp12MaxDiff = 1

P1 = 8 * 1 * blockSize**2  # 1 canal, porque la imagen es en gris
P2 = 32 * 1 * blockSize**2

stereo = cv2.StereoSGBM_create(
    minDisparity=minDisparity,
    numDisparities=numDisparities,
    blockSize=blockSize,
    uniquenessRatio=uniquenessRatio,
    speckleRange=speckleRange,
    speckleWindowSize=speckleWindowSize,
    disp12MaxDiff=disp12MaxDiff,
    P1=P1,
    P2=P2,
)


disparity = stereo.compute(left_image, right_image).astype(np.float32) / 16.0
disparity[disparity < minDisparity] = minDisparity  # descarta los píxeles inválidos
disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX).astype(
    np.uint8
)
cv2.imwrite("disparidad.png", disparity_normalized)
cv2.imshow("Disparidad", disparity_normalized)  # en Jupyter/Colab usa matplotlib
cv2.waitKey(0)
cv2.destroyAllWindows()
