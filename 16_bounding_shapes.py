import cv2
import numpy as np

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)

img = cv2.pyrDown(cv2.imread("hammer.jpg", cv2.IMREAD_UNCHANGED))
ret, thresh = cv2.threshold(
    cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY
)

contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    # encontrar las coordenadas del cuadrado delimitador
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(img, (x, y), (x + w, y + h), GREEN, 2)
    # encontrar el área mínima
    rect = cv2.minAreaRect(c)
    # calcular las coordenadas del rectángulo de área mínima
    box = cv2.boxPoints(rect)
    # normalizar las coordenadas a enteros
    box = np.int32(box)
    # dibujar contornos
    cv2.drawContours(img, [box], 0, RED, 3)
    # calcular el centro y radio del circulo mínimo
    (x, y), radius = cv2.minEnclosingCircle(c)
    # cast a enteros
    center = (int(x), int(y))
    radius = int(radius)
    # dibujar el círculo
    img = cv2.circle(img, center, radius, YELLOW, 2)

cv2.drawContours(img, contours, -1, BLUE, 1)
cv2.imshow("contours", img)
cv2.waitKey()
cv2.destroyAllWindows()
