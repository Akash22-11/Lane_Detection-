import os
import cv2
import numpy as np


WIDTH, HEIGHT = 960, 540
VANISHING_POINT = (WIDTH // 2 + 20, int(HEIGHT * 0.55))


def make_frame(frame_idx=0, dash_offset=0):
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Sky
    img[:, :] = (180, 140, 90)  # BGR -- light blue-ish sky

    # horizon
    horizon = int(HEIGHT * 0.55)
    img[horizon:, :] = (60, 110, 60)

    # Road (trapezoid)
    road_pts = np.array([
        [int(WIDTH * 0.30), HEIGHT],
        [VANISHING_POINT[0] - 15, VANISHING_POINT[1]],
        [VANISHING_POINT[0] + 15, VANISHING_POINT[1]],
        [int(WIDTH * 0.75), HEIGHT],
    ], dtype=np.int32)
    cv2.fillPoly(img, [road_pts], (70, 70, 70))

    # Left solid lane line
    left_line = np.array([
        [int(WIDTH * 0.32), HEIGHT],
        [VANISHING_POINT[0] - 12, VANISHING_POINT[1]],
    ])
    cv2.line(img, tuple(left_line[0]), tuple(left_line[1]), (255, 255, 255), 6)

    # Right dashed lane line
    right_top = (VANISHING_POINT[0] + 12, VANISHING_POINT[1])
    right_bottom = (int(WIDTH * 0.73), HEIGHT)
    num_dashes = 8
    for i in range(num_dashes):
        t0 = (i + dash_offset) / num_dashes
        t1 = t0 + 0.5 / num_dashes
        if t1 > 1:
            continue
        p0 = (
            int(right_top[0] + (right_bottom[0] - right_top[0]) * t0),
            int(right_top[1] + (right_bottom[1] - right_top[1]) * t0),
        )
        p1 = (
            int(right_top[0] + (right_bottom[0] - right_top[0]) * t1),
            int(right_top[1] + (right_bottom[1] - right_top[1]) * t1),
        )
        cv2.line(img, p0, p1, (255, 255, 255), 6)

    # Add a couple of "other vehicles"
    cv2.rectangle(img, (50, horizon - 40), (150, horizon - 5), (40, 40, 160), -1)

    # Add subtle Gaussian noise
    noise = np.random.normal(0, 4, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return img


def generate_image(path="images/sample_road.jpg"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    frame = make_frame()
    cv2.imwrite(path, frame)
    print(f"Saved test image -> {path}")


def generate_video(path="videos/sample_road.mp4", n_frames=60, fps=20):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(path, fourcc, fps, (WIDTH, HEIGHT))

    for i in range(n_frames):
        dash_offset = (i / n_frames) % 1.0
        frame = make_frame(frame_idx=i, dash_offset=dash_offset)
        writer.write(frame)

    writer.release()
    print(f"Saved test video -> {path} ({n_frames} frames @ {fps}fps)")


if __name__ == "__main__":
    generate_image()
    generate_video()
