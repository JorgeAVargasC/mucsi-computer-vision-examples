"""
Mostrar la cámara en vivo y reaccionar al ratón con cv2.setMouseCallback:
clic derecho muestra/oculta el número de frame, clic izquierdo cierra.
"""

import cv2

CAMERA = 0


def main():
    clicked = False
    show_frame_number = False

    def on_mouse(event, x, y, flags, param):
        nonlocal clicked, show_frame_number
        if event == cv2.EVENT_LBUTTONUP:
            print("cv2.EVENT_LBUTTONUP")
            clicked = True

        if event == cv2.EVENT_RBUTTONUP:
            print("cv2.EVENT_RBUTTONUP")
            show_frame_number = not show_frame_number

    camera_capture = cv2.VideoCapture(CAMERA)

    cv2.namedWindow("MyWindow")
    cv2.setMouseCallback("MyWindow", on_mouse)

    print("Showing camera feed. Click window or press any key to stop.")
    print("Right click: show/hide the frame number.")

    frame_number = 0
    success, frame = camera_capture.read()

    while success and cv2.waitKey(1) == -1 and not clicked:
        frame_number += 1
        if show_frame_number:
            cv2.putText(
                frame,
                f"Frame: {frame_number}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        cv2.imshow("MyWindow", frame)
        success, frame = camera_capture.read()

    cv2.destroyWindow("MyWindow")
    camera_capture.release()


if __name__ == "__main__":
    main()
