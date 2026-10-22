"""
Grabar 10 segundos de la cámara en un archivo .avi sin comprimir (I420).
"""

import cv2

CAMERA = 0  # 0 is the built-in camera; an external USB camera is usually 1.
OUTPUT_PATH = "05_output.avi"


def main():
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
