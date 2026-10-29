import numpy as np
import cv2
from matplotlib import pyplot as plt

original = cv2.imread("./statue_small.jpg")
img = original.copy()

# mask: 0 fondo, 1 objeto, 2 prob fondo, 3 prob objeto
mask = np.zeros(img.shape[:2], np.uint8)
print(mask)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# rect del objeto, lo de fuera es fondo
x = 100
y = 1
width = 421
height = 378
rect = (x, y, width, height)

# 1er procesamiento con rect
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# quitar el cielo azul bajo el codo
azul_min = (200, 140, 50)
azul_max = (255, 210, 130)

cielo = cv2.inRange(original, azul_min, azul_max)


mask[cielo > 0] = cv2.GC_BGD

# 2do procesamiento con la mask corregida
cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

# fondo -> 0, objeto -> 1
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
img = img * mask2[:, :, np.newaxis]

plt.subplot(121)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # BGR -> RGB
plt.title("grabcut")
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
plt.title("original")
plt.xticks([])
plt.yticks([])

plt.show()
