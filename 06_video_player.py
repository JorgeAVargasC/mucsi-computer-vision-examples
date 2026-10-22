"""
Reproductor de vídeo con teclado: pausar/reanudar, guardar el frame actual
como imagen y salir.
"""

from pathlib import Path

import cv2

HERE = Path(__file__).parent

VIDEO_PATH = str(HERE / "assets" / "MyInputVid.avi")
OUTPUTS_DIR = HERE / "outputs" / Path(__file__).stem

MAX_DISPLAY_WIDTH = 320

KEY_SPACE = ord(" ")
KEY_SAVE = ord("s")
KEY_QUIT = ord("q")


def main():
    video_capture = cv2.VideoCapture(VIDEO_PATH)
    if not video_capture.isOpened():
        print(f"Could not open video: {VIDEO_PATH}")
        return

    fps = video_capture.get(cv2.CAP_PROP_FPS) or 30
    delay = max(1, int(1000 / fps))
    cv2.namedWindow("MyWindow")

    print("Space: pause/resume | S: save current frame | Q: quit")

    paused = False
    saved_count = 0
    success, frame = video_capture.read()

    while success:
        height, width = frame.shape[:2]
        scale = min(1.0, MAX_DISPLAY_WIDTH / width)
        display = cv2.resize(frame, (int(width * scale), int(height * scale)))
        cv2.imshow("MyWindow", display)
        key = cv2.waitKey(delay) & 0xFF

        if key == KEY_QUIT:
            break
        if key == KEY_SPACE:
            paused = not paused
        if key == KEY_SAVE:
            OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
            path = OUTPUTS_DIR / f"frame_{saved_count:04d}.png"
            cv2.imwrite(str(path), frame)
            saved_count += 1
            print(f"Saved {path}")

        # While paused the same frame stays on screen; reading only
        # resumes afterwards, so no frames are skipped.
        if not paused:
            success, frame = video_capture.read()

    cv2.destroyWindow("MyWindow")
    video_capture.release()


if __name__ == "__main__":
    main()
