"""
Grabar 10 segundos de la cámara en un archivo .avi sin comprimir (I420).
"""

from pathlib import Path

import cv2

HERE = Path(__file__).parent

CAMERA = 0  # 0 is the built-in camera; an external USB camera is usually 1.
OUTPUTS_DIR = HERE / "outputs"
OUTPUT_PATH = str(OUTPUTS_DIR / f"{Path(__file__).stem}.avi")


def main():
    OUTPUTS_DIR.mkdir(exist_ok=True)
    camera_capture = cv2.VideoCapture(CAMERA)
    fps = 30  # An assumption
    size = (
        int(camera_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    video_writer = cv2.VideoWriter(
        OUTPUT_PATH, cv2.VideoWriter_fourcc("I", "4", "2", "0"), fps, size
    )
    success, frame = camera_capture.read()
    num_frames_remaining = 10 * fps - 1  # 10 seconds of frames

    while success and num_frames_remaining > 0:
        video_writer.write(frame)
        success, frame = camera_capture.read()
        num_frames_remaining -= 1

    camera_capture.release()
    video_writer.release()
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
