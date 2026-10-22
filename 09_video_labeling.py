"""
Etiquetador de vídeo: reproducir, pausar y avanzar frame a frame con las
flechas, marcar una caja con dos clics y guardar un vídeo nuevo donde cada
frame lleva la última caja marcada hasta ese momento.
"""

from pathlib import Path

import cv2
from cv2.typing import MatLike

HERE = Path(__file__).parent
INPUT_PATH = str(HERE / "assets" / "dog.mp4")
OUTPUTS_DIR = HERE / "outputs"
OUTPUT_PATH = str(OUTPUTS_DIR / f"{Path(__file__).stem}.mp4")

VIDEO_WINDOW = "video"

# Arrow key codes from cv2.waitKeyEx: Windows, Linux and macOS.
PREVIOUS_FRAME_KEYS = (2424832, 65361, 63234)
NEXT_FRAME_KEYS = (2555904, 65363, 63235)
PAUSE_KEY = ord(" ")
QUIT_KEYS = (ord("q"), ord("Q"))

PAUSED_DELAY_MS = 20

# COLORS IN BGR
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)

FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.4
THICKNESS = 1

MARGIN = 8  # Gap between the panel and the frame border.
PADDING = 5  # Gap between the panel border and the text.
LINE_GAP = 6

MENU_LINES = (
    "Espacio: Pausar / Reproducir",
    "<- / ->: Frame anterior / siguiente",
    "Click izq: Etiquetar",
    "Q: Guardar y salir",
)

Point = tuple[int, int]
Box = tuple[Point, Point]


# ---------- DRAWING ----------


def draw_box(image: MatLike, pt1: Point, pt2: Point) -> None:
    """
    Draw a box from two opposite corners
    """

    x1, y1 = pt1
    x2, y2 = pt2

    p1 = (x1, y1)
    p2 = (x2, y1)
    p3 = (x2, y2)
    p4 = (x1, y2)

    cv2.line(image, p1, p2, GREEN)
    cv2.line(image, p2, p3, GREEN)
    cv2.line(image, p3, p4, GREEN)
    cv2.line(image, p4, p1, GREEN)


def draw_click_point(frame: MatLike, pt: Point) -> None:
    cv2.circle(frame, pt, 4, RED, -1)


def draw_text_panel(
    frame: MatLike, lines: tuple[str, ...], align_right: bool = False
) -> None:
    """
    Draw the lines over a black panel in the top left or top right corner
    """

    sizes = [
        cv2.getTextSize(line, FONT_FACE, FONT_SCALE, THICKNESS) for line in lines
    ]
    text_width = max(width for (width, _), _ in sizes)
    (_, text_height), baseline = sizes[0]
    line_height = text_height + baseline + LINE_GAP

    panel_width = text_width + 2 * PADDING
    panel_height = len(lines) * line_height - LINE_GAP + 2 * PADDING

    x = frame.shape[1] - panel_width - MARGIN if align_right else MARGIN
    y = MARGIN

    cv2.rectangle(frame, (x, y), (x + panel_width, y + panel_height), BLACK, -1)

    for i, line in enumerate(lines):
        cv2.putText(
            img=frame,
            text=line,
            org=(x + PADDING, y + PADDING + text_height + i * line_height),
            fontFace=FONT_FACE,
            fontScale=FONT_SCALE,
            color=GREEN,
            thickness=THICKNESS,
            lineType=cv2.LINE_AA,
        )


def draw_menu(frame: MatLike) -> None:
    draw_text_panel(frame, MENU_LINES, align_right=True)


def draw_status(
    frame: MatLike, frame_number: int, total_frames: int, paused: bool
) -> None:
    state = "EN PAUSA" if paused else "REPRODUCIENDO"

    draw_text_panel(frame, (f"Frame: {frame_number} / {total_frames}", state))


# ---------- VIDEO ----------


def add_click_point(event: int, x: int, y: int, flags: int, param: list[Point]) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))


def read_frame(video: cv2.VideoCapture, frame_number: int) -> MatLike | None:
    """
    Read the given frame (the first one is 1), or None if it does not exist
    """

    if frame_number < 1:
        return None

    # While playing the video is already at the next frame: only jump if needed.
    if video.get(cv2.CAP_PROP_POS_FRAMES) != frame_number - 1:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)

    success, frame = video.read()

    return frame if success else None


def box_for_frame(labels: dict[int, Box], frame_number: int) -> Box | None:
    """
    Box of the closest labeled frame at or before the given one, or None
    """

    labeled_frames = [number for number in labels if number <= frame_number]

    return labels[max(labeled_frames)] if labeled_frames else None


def show_preview(
    frame: MatLike,
    box: Box | None,
    click_points: list[Point],
    frame_number: int,
    total_frames: int,
    paused: bool,
) -> None:
    preview = frame.copy()

    for pt in click_points:
        draw_click_point(preview, pt)

    if box is not None:
        draw_box(preview, *box)

    draw_status(preview, frame_number, total_frames, paused)
    draw_menu(preview)

    cv2.imshow(VIDEO_WINDOW, preview)


def save_labeled_video(video: cv2.VideoCapture, labels: dict[int, Box]) -> None:
    """
    Write every frame of the video, each one with the last box labeled so far
    """

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS) or 30

    OUTPUTS_DIR.mkdir(exist_ok=True)
    writer = cv2.VideoWriter(
        OUTPUT_PATH, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    # Back to the start, then read in order: faster than jumping to each frame.
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_number = 1
    box: Box | None = None
    success, frame = video.read()

    while success:
        # A labeled frame replaces the box; the others keep the previous one.
        box = labels.get(frame_number, box)

        if box is not None:
            draw_box(frame, *box)

        writer.write(frame)

        frame_number += 1
        success, frame = video.read()

    writer.release()

    print(f"Saved {OUTPUT_PATH} ({len(labels)} frames labeled by hand)")


def main() -> None:
    video = cv2.VideoCapture(INPUT_PATH)

    frame_number = 1
    frame = read_frame(video, frame_number)

    if frame is None:
        print(f"Could not read any frame from: {INPUT_PATH}")
        video.release()
        return

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    playing_delay_ms = int(1000 / (video.get(cv2.CAP_PROP_FPS) or 30))

    click_points: list[Point] = []

    # Only the frames labeled by hand: the ones in between reuse the previous box.
    labels: dict[int, Box] = {}

    # Start paused so the first frame can be labeled before the video runs.
    paused = True

    cv2.namedWindow(VIDEO_WINDOW)
    cv2.setMouseCallback(VIDEO_WINDOW, add_click_point, click_points)

    while True:
        show_preview(
            frame,
            box_for_frame(labels, frame_number),
            click_points,
            frame_number,
            total_frames,
            paused,
        )

        # waitKeyEx, unlike waitKey, also reports the arrow keys.
        key = cv2.waitKeyEx(PAUSED_DELAY_MS if paused else playing_delay_ms)

        # A click pauses the video: both corners must land on the same frame.
        if click_points:
            paused = True

        if len(click_points) >= 2:
            labels[frame_number] = (click_points[0], click_points[1])
            click_points.clear()

        if key in QUIT_KEYS:
            break

        if key == PAUSE_KEY:
            paused = not paused
            click_points.clear()

        step = 0

        if key in PREVIOUS_FRAME_KEYS or key in NEXT_FRAME_KEYS:
            step = 1 if key in NEXT_FRAME_KEYS else -1
            paused = True
        elif not paused:
            step = 1

        if step != 0:
            new_frame = read_frame(video, frame_number + step)

            # At the first or last frame there is nowhere to go: stay put.
            if new_frame is None:
                paused = True
            else:
                frame = new_frame
                frame_number += step
                click_points.clear()

    cv2.destroyAllWindows()

    save_labeled_video(video, labels)
    video.release()


if __name__ == "__main__":
    main()
