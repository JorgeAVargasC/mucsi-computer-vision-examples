"""
Marcar regiones de 4 esquinas con el ratón sobre un frame de cada segundo
del vídeo y escribir un vídeo nuevo con esas regiones pintadas encima.
Las líneas se pintan a mano, píxel a píxel, sin usar cv2.line.
"""

import cv2
import numpy as np

# COLORS IN BGR
GREEN = (0, 255, 0)
RED = (0, 0, 255)


INPUT_PATH = "MyInputVid.avi"
OUTPUT_PATH = "08_output.mp4"

WINDOW_NAME = "MyWindow"
MAX_DISPLAY_HEIGHT = 720
BORDER_THICKNESS = 4
MARKER_RADIUS = 6
ESC_KEY = 27


def main():
    video_capture, frame = _open_video(INPUT_PATH)
    if video_capture is None:
        return

    height, width = frame.shape[:2]
    scale = min(1.0, MAX_DISPLAY_HEIGHT / height)

    fps = video_capture.get(cv2.CAP_PROP_FPS) or 30
    frames_per_second = max(1, round(fps))

    regions = []  # Finished regions as 4 corners (x, y), in frame coordinates.
    corners = []  # Corners clicked so far for the region being selected.

    _open_window(regions, corners, width, height, scale)
    video_writer = _create_video_writer(fps, width, height)

    print("Left click: the 4 corners of a region | Right click: undo")
    print("Press any key to go to the next second | ESC: stop selecting.")

    num_frames = 0
    num_regions = 0
    selecting = True
    success = True

    while success:  # Loop until there are no more frames.
        # FIRST: SELECT THE REGIONS ON ONE FRAME OF EVERY SECOND
        if selecting and num_frames % frames_per_second == 0:
            print(f"Second {num_frames // frames_per_second}")
            key = _select_regions(frame, regions, corners, scale)
            num_regions += len(regions)
            if key == ESC_KEY:
                # The rest of the video is written without regions.
                selecting = False
                cv2.destroyWindow(WINDOW_NAME)

        # SECOND: WRITE THE FRAMES OF THAT SECOND WITH ITS REGIONS ON TOP
        _draw_regions(frame, regions)
        video_writer.write(frame)
        num_frames += 1
        if not selecting and num_frames % frames_per_second == 0:
            regions.clear()
        success, frame = video_capture.read()

    cv2.destroyAllWindows()
    video_capture.release()
    video_writer.release()
    print(f"Saved {OUTPUT_PATH} ({num_frames} frames, {num_regions} regions)")


# ---------- VIDEO ----------


def _open_video(path):
    # Returns the capture and its first frame, or (None, None) on failure.
    video = cv2.VideoCapture(path)
    if not video.isOpened():
        print(f"Could not open video: {path}")
        return None, None

    success, frame = video.read()
    if not success:
        print(f"Could not read any frame from: {path}")
        video.release()
        return None, None

    return video, frame


def _create_video_writer(fps, width, height):
    return cv2.VideoWriter(
        OUTPUT_PATH,
        cv2.VideoWriter_fourcc(*"mp4v"),  # Compressed codec (I420 is raw).
        fps,
        (width, height),
    )


# ---------- MOUSE ----------


def _open_window(regions, corners, width, height, scale):
    def on_mouse(event, x, y, flags, param):
        point = _to_frame_coordinates(x, y, width, height, scale)
        if event == cv2.EVENT_LBUTTONUP:
            _add_corner(point, regions, corners)
        if event == cv2.EVENT_RBUTTONUP:
            _undo(regions, corners)

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)


def _to_frame_coordinates(x, y, width, height, scale):
    # The window shows a resized frame, so the click is mapped back
    # to the coordinates of the original frame.
    x = max(0, min(width - 1, int(x / scale)))
    y = max(0, min(height - 1, int(y / scale)))
    return x, y


def _add_corner(point, regions, corners):
    # The fourth corner closes the region.
    corners.append(point)
    if len(corners) == 4:
        regions.append(tuple(corners))
        corners.clear()
        print(f"  Region {len(regions)}: {regions[-1]}")


def _undo(regions, corners):
    # Removes the last corner, or the last region if there are no corners.
    if corners:
        corners.pop()
    elif regions:
        print(f"  Removed region {len(regions)}: {regions.pop()}")


# ---------- SELECTION ----------


def _select_regions(frame, regions, corners, scale):
    # Shows the frame until a key is pressed, while the mouse fills
    # `regions`. Returns the pressed key.
    regions.clear()
    corners.clear()

    key = -1
    while key == -1:
        _show_preview(frame, regions, corners, scale)
        key = cv2.waitKey(1)

    corners.clear()  # An unfinished region is discarded.
    return key


def _show_preview(frame, regions, corners, scale):
    # Everything is drawn on a copy, so the original frame stays clean.
    preview = frame.copy()
    _draw_regions(preview, regions)
    _draw_unfinished_region(preview, corners)

    height, width = preview.shape[:2]
    display_size = (int(width * scale), int(height * scale))
    cv2.imshow(WINDOW_NAME, cv2.resize(preview, display_size))


# ---------- DRAWING ----------


def _draw_regions(frame, regions):
    # Each side is drawn separately, from one corner to the next one.
    for corners in regions:
        for i in range(4):
            _draw_line(frame, corners[i], corners[(i + 1) % 4])


def _draw_unfinished_region(frame, corners):
    # Sides of the region being selected that are already known.
    for start, end in zip(corners, corners[1:]):
        _draw_line(frame, start, end)
    for corner in corners:
        _draw_marker(frame, corner)


def _draw_line(frame, start, end):
    # The line is a small block of green pixels painted on every point
    # between its two ends.
    (x1, y1), (x2, y2) = start, end
    num_points = max(abs(x2 - x1), abs(y2 - y1)) + 1
    xs = np.linspace(x1, x2, num_points).round().astype(int)
    ys = np.linspace(y1, y2, num_points).round().astype(int)
    for x, y in zip(xs, ys):
        _paint_square(frame, x, y, BORDER_THICKNESS // 2, GREEN)


def _draw_marker(frame, corner):
    x, y = corner
    _paint_square(frame, x, y, MARKER_RADIUS, RED)


def _paint_square(frame, x, y, half_size, color):
    # Square centered on (x, y), cut off at the top and left borders
    # (numpy already cuts it off at the bottom and right ones).
    top, left = max(0, y - half_size), max(0, x - half_size)
    frame[top : y + half_size + 1, left : x + half_size + 1] = color


if __name__ == "__main__":
    main()
