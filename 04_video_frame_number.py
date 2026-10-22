"""
Leer un vídeo frame a frame con cv2.VideoCapture, escribir el número de
cada frame en el centro y guardarlo con cv2.VideoWriter.
"""

import cv2

INPUT_PATH = "MyInputVid.avi"
OUTPUT_PATH = "04_output.mp4"


def main():
    video_capture = cv2.VideoCapture(INPUT_PATH)

    fps = video_capture.get(cv2.CAP_PROP_FPS)

    size = (
        int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )

    video_writer = cv2.VideoWriter(
        OUTPUT_PATH,
        cv2.VideoWriter_fourcc(*"mp4v"),  # Compressed codec (I420 is raw).
        fps,
        size,
    )

    success, frame = video_capture.read()
    frame_number = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    thickness = 3

    while success:  # Loop until there are no more frames.
        text = str(frame_number)
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        cv2.putText(
            frame,
            text,
            ((size[0] - text_w) // 2, (size[1] + text_h) // 2),  # Centered.
            font,
            font_scale,
            (0, 255, 0),  # Color (BGR).
            thickness,
            cv2.LINE_AA,
        )
        video_writer.write(frame)
        frame_number += 1
        success, frame = video_capture.read()

    video_capture.release()
    video_writer.release()
    print(f"Saved {OUTPUT_PATH} ({frame_number} frames)")


if __name__ == "__main__":
    main()
