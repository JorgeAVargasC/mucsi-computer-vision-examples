"""
Leer la misma imagen con los tres modos de cv2.imread (color, gris y sin
cambios), comparar sus canales y guardar los resultados en outputs/.
"""

from pathlib import Path

import cv2

HERE = Path(__file__).parent
CAT_PATH = str(HERE / "assets" / "cat.jpg")
OUTPUTS_DIR = HERE / "outputs" / Path(__file__).stem


def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save(name, img):
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUTPUTS_DIR / name), img)
    print(f"SAVED {name}")


def main():
    # IMREAD_COLOR is the default value, always 3 channels (BGR)
    print("COLOR")
    img_color = cv2.imread(CAT_PATH, cv2.IMREAD_COLOR)
    print("SHAPE", img_color.shape)
    save("cat_color.png", img_color)
    show_image("COLOR", img_color)

    # IMREAD_GRAYSCALE, 1 channel
    print("GRAY")
    img_gray = cv2.imread(CAT_PATH, cv2.IMREAD_GRAYSCALE)
    print("SHAPE", img_gray.shape)
    save("cat_gray.png", img_gray)
    show_image("GRAY", img_gray)

    # IMREAD_UNCHANGED, keeps the channels of the file (alpha included)
    print("UNCHANGED")
    img_unchanged = cv2.imread(CAT_PATH, cv2.IMREAD_UNCHANGED)
    print("SHAPE", img_unchanged.shape)
    save("cat_unchanged.png", img_unchanged)
    show_image("UNCHANGED", img_unchanged)


if __name__ == "__main__":
    main()
