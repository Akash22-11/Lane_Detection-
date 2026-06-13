import argparse
import cv2
import numpy as np

from lane_detection import process_frame, process_frame_debug, LaneSmoother


def run_on_image(input_path, output_path, draw_fill=True):
    frame = cv2.imread(input_path)
    if frame is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    annotated = process_frame(frame, smoother=None, draw_fill=draw_fill)
    cv2.imwrite(output_path, annotated)
    print(f"Annotated image written -> {output_path}")


def run_on_video(input_path, output_path, draw_fill=True):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 20
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    smoother = LaneSmoother(buffer_size=8)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        annotated = process_frame(frame, smoother=smoother, draw_fill=draw_fill)
        writer.write(annotated)
        frame_count += 1

    cap.release()
    writer.release()
    print(f"Annotated video written -> {output_path} ({frame_count} frames)")


def run_debug_figure(input_path, output_path):
    """Builds a labeled grid showing each pipeline stage side-by-side."""
    frame = cv2.imread(input_path)
    if frame is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    stages = process_frame_debug(frame)

    h, w = frame.shape[:2]
    thumb_w, thumb_h = w // 3, h // 3

    def to_bgr_thumb(img, label):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        thumb = cv2.resize(img, (thumb_w, thumb_h))
        cv2.putText(thumb, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return thumb

    order = [
        ("original", "1. Original"),
        ("gray", "2. Grayscale"),
        ("blurred", "3. Gaussian Blur"),
        ("edges", "4. Canny Edges"),
        ("masked_edges", "5. ROI Mask"),
        ("final", "6. Lane Overlay"),
    ]

    thumbs = [to_bgr_thumb(stages[key], label) for key, label in order]

    row1 = np.hstack(thumbs[0:3])
    row2 = np.hstack(thumbs[3:6])
    grid = np.vstack([row1, row2])

    cv2.imwrite(output_path, grid)
    print(f"Pipeline-stage figure written -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Road lane-line detection pipeline")
    parser.add_argument("--mode", choices=["image", "video", "debug"], required=True,
                    help="image: process a single image | video: process a video file | "
                            "debug: generate a pipeline-stages figure")
    parser.add_argument("--input", required=True, help="Path to input image/video")
    parser.add_argument("--output", required=True, help="Path to write annotated output")
    parser.add_argument("--no-fill", action="store_true",
                        help="Disable the shaded drivable-area overlay")
    args = parser.parse_args()

    if args.mode == "image":
        run_on_image(args.input, args.output, draw_fill=not args.no_fill)
    elif args.mode == "video":
        run_on_video(args.input, args.output, draw_fill=not args.no_fill)
    elif args.mode == "debug":
        run_debug_figure(args.input, args.output)


if __name__ == "__main__":
    main()
