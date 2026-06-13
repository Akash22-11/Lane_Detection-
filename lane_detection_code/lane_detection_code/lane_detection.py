import cv2
import numpy as np


def to_grayscale(image):
    """Convert a BGR image to single-channel grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_gaussian_blur(image, kernel_size=5):
    """Smooth the image to suppress high-frequency noise before edge detection."""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def detect_edges(image, low_threshold=50, high_threshold=150):
    """Run the Canny edge detector."""
    return cv2.Canny(image, low_threshold, high_threshold)


def region_of_interest(image, vertices=None):
    mask = np.zeros_like(image)
    height, width = image.shape[:2]

    if vertices is None:
        vertices = np.array([[
            (int(width * 0.05), height),
            (int(width * 0.45), int(height * 0.6)),
            (int(width * 0.55), int(height * 0.6)),
            (int(width * 0.95), height)
        ]], dtype=np.int32)

    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(image, mask)


def hough_transform(masked_edges):
    
    return cv2.HoughLinesP(
        masked_edges,
        rho=2,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=40,
        maxLineGap=100
    )


def make_line_points(image, slope_intercept):
    """Convert a (slope, intercept) pair into pixel endpoints spanning the ROI."""
    slope, intercept = slope_intercept
    height = image.shape[0]

    y1 = height
    y2 = int(height * 0.6)

    if abs(slope) < 1e-3:
        slope = 1e-3 if slope >= 0 else -1e-3

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):

    left_fits = []
    right_fits = []

    if lines is None:
        return None, None

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        if x2 == x1:
            continue  

        slope, intercept = np.polyfit((x1, x2), (y1, y2), 1)

        # Filter out near-horizontal lines 
        if abs(slope) < 0.3:
            continue

        if slope < 0:
            left_fits.append((slope, intercept))
        else:
            right_fits.append((slope, intercept))

    left_line = make_line_points(image, np.average(left_fits, axis=0)) if left_fits else None
    right_line = make_line_points(image, np.average(right_fits, axis=0)) if right_fits else None
    return left_line, right_line


def draw_lane_lines(image, left_line, right_line, line_color=(0, 255, 0), thickness=10):
    """Draw the detected lane lines on a transparent overlay."""
    overlay = np.zeros_like(image)

    for line in (left_line, right_line):
        if line is not None:
            x1, y1, x2, y2 = line
            cv2.line(overlay, (x1, y1), (x2, y2), line_color, thickness)

    return overlay


def draw_lane_fill(image, left_line, right_line, fill_color=(0, 200, 0), alpha=0.3):
    """
    Fill the polygon between the left and right lane lines to visualize
    the drivable corridor -- useful for path-planning visualization.
    """
    overlay = image.copy()

    if left_line is not None and right_line is not None:
        lx1, ly1, lx2, ly2 = left_line
        rx1, ry1, rx2, ry2 = right_line
        pts = np.array([[lx1, ly1], [lx2, ly2], [rx2, ry2], [rx1, ry1]], dtype=np.int32)
        cv2.fillPoly(overlay, [pts], fill_color)
        image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    return image


class LaneSmoother:

    def __init__(self, buffer_size=8):
        self.buffer_size = buffer_size
        self.left_history = []
        self.right_history = []

    def update(self, left_line, right_line):
        if left_line is not None:
            self.left_history.append(left_line)
            self.left_history = self.left_history[-self.buffer_size:]
        if right_line is not None:
            self.right_history.append(right_line)
            self.right_history = self.right_history[-self.buffer_size:]

        smoothed_left = np.mean(self.left_history, axis=0).astype(int) if self.left_history else None
        smoothed_right = np.mean(self.right_history, axis=0).astype(int) if self.right_history else None
        return smoothed_left, smoothed_right


def process_frame(frame, smoother=None, draw_fill=True):

    gray = to_grayscale(frame)
    blurred = apply_gaussian_blur(gray)
    edges = detect_edges(blurred)
    masked_edges = region_of_interest(edges)
    lines = hough_transform(masked_edges)

    left_line, right_line = average_slope_intercept(frame, lines)

    if smoother is not None:
        left_line, right_line = smoother.update(left_line, right_line)

    result = frame.copy()
    if draw_fill:
        result = draw_lane_fill(result, left_line, right_line)

    lane_overlay = draw_lane_lines(result, left_line, right_line)
    result = cv2.addWeighted(result, 1.0, lane_overlay, 1.0, 0)

    return result


def process_frame_debug(frame):

    gray = to_grayscale(frame)
    blurred = apply_gaussian_blur(gray)
    edges = detect_edges(blurred)
    masked_edges = region_of_interest(edges)
    lines = hough_transform(masked_edges)
    left_line, right_line = average_slope_intercept(frame, lines)

    result = draw_lane_fill(frame.copy(), left_line, right_line)
    lane_overlay = draw_lane_lines(result, left_line, right_line)
    final = cv2.addWeighted(result, 1.0, lane_overlay, 1.0, 0)

    return {
        "original": frame,
        "gray": gray,
        "blurred": blurred,
        "edges": edges,
        "masked_edges": masked_edges,
        "final": final,
    }
