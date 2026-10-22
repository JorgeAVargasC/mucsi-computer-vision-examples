"""
Pasar una imagen de color a gris y dibujar píxel a píxel, en color, una
diagonal y un coseno sobre ella.
"""

import math
import cv2

CAT_PATH = "cat.jpg"

# COLORS IN BGR
GREEN = (0, 255, 0)


def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    cat_color = cv2.imread(CAT_PATH)
    show_image("CAT COLOR", cat_color)

    # FIRST: COLOR TO BLACK AND WHITE
    print("COLOR TO GRAY")
    cat_gray = cv2.cvtColor(cat_color, cv2.COLOR_BGR2GRAY)
    print("SHAPE", cat_color.shape, "->", cat_gray.shape)
    show_image("CAT GRAY", cat_gray)

    height, width = cat_gray.shape

    # GRAY IMAGE WITH 3 CHANNELS SO WE CAN DRAW IN COLOR ON TOP OF IT
    cat_gray_bgr = cv2.cvtColor(cat_gray, cv2.COLOR_GRAY2BGR)

    # SECOND: DRAW DIAGONAL
    print("DRAW DIAGONAL")
    cat_diagonal = cat_gray_bgr.copy()

    m = height / width

    for x in range(width):
        y = int(m * x)
        cat_diagonal[y][x] = GREEN

    show_image("CAT DIAGONAL", cat_diagonal)

    # THIRD: DRAW COS
    print("DRAW COS")
    cat_cos = cat_gray_bgr.copy()

    A = height / 2  # 150 pixels
    C = height / 2  # 150 pixels
    T = width  # 600 pixels

    omega = 2 * math.pi / T

    for x in range(width):
        y = A * math.cos(omega * x) + C

        y = int(y)

        y = max(0, min(height - 1, y))

        cat_cos[y][x] = GREEN

    show_image("CAT COS", cv2.resize(cat_cos, (width * 2, height * 2)))


if __name__ == "__main__":
    main()
