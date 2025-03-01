import cv2
import numpy as np

def preprocess_frame(frame):
    """
    Preprocess the input frame by converting it to grayscale, applying Gaussian blur, 
    and using Canny edge detection.

    Parameters:
        frame (numpy.ndarray): The current video frame.

    Returns:
        numpy.ndarray: The preprocessed frame with edges highlighted.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    return edges

def region_of_interest(edges, width, height):
    """
    Mask the edges image to focus on the region of interest (the road area).

    Parameters:
        edges (numpy.ndarray): The edge-detected frame.
        width (int): Width of the frame.
        height (int): Height of the frame.

    Returns:
        numpy.ndarray: The masked frame.
    """
    # Define a polygonal region of interest
    roi = np.array([[
        (int(width * 0.1), height),  # Bottom-left corner
        (int(width * 0.4), int(height * 0.6)),  # Top-left corner
        (int(width * 0.6), int(height * 0.6)),  # Top-right corner
        (int(width * 0.9), height)  # Bottom-right corner
    ]], dtype=np.int32)

    # Create a blank mask and fill the region of interest
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, roi, 255)

    # Apply the mask to the edges
    masked_edges = cv2.bitwise_and(edges, mask)

    return masked_edges

def detect_lanes(frame):
    """
    Detect lane lines in the frame using Hough Line Transform.

    Parameters:
        frame (numpy.ndarray): The current video frame.

    Returns:
        list: A list of lane lines as (x1, y1, x2, y2).
    """
    # Preprocess the frame
    edges = preprocess_frame(frame)

    # Get frame dimensions
    height, width = frame.shape[:2]

    # Focus on the region of interest
    roi_edges = region_of_interest(edges, width, height)

    # Hough Line Transform parameters
    rho = 1  # Distance resolution in pixels
    theta = np.pi / 180  # Angular resolution in radians
    threshold = 50  # Minimum number of votes to detect a line
    min_line_length = 40  # Minimum line length
    max_line_gap = 100  # Maximum allowed gap between line segments

    # Detect lines
    lines = cv2.HoughLinesP(
        roi_edges, rho, theta, threshold,
        np.array([]), minLineLength=min_line_length, maxLineGap=max_line_gap
    )

    if lines is not None:
        lane_lines = [(x1, y1, x2, y2) for line in lines for x1, y1, x2, y2 in line]
        return lane_lines

    return []

def draw_lanes(frame, lane_lines):
    """
    Draw the detected lane lines on the frame.

    Parameters:
        frame (numpy.ndarray): The current video frame.
        lane_lines (list): List of detected lane lines as (x1, y1, x2, y2).

    Returns:
        numpy.ndarray: The frame with lane lines drawn.
    """
    annotated_frame = frame.copy()

    # Draw each lane line
    for x1, y1, x2, y2 in lane_lines:
        cv2.line(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 5)  # Blue lines

    return annotated_frame
