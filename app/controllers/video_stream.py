import cv2
from controllers.lane_detection import detect_lanes, draw_lanes

class VideoStream:
    def __init__(self, video_source=0):
        """
        Initialize the VideoStream class.
        
        Parameters:
            video_source (str or int): Path to the video file or device index for webcam (default is 0 for the primary webcam).
        """
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)

        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video source: {video_source}")

    def generate_frames(self):
        """
        Generate frames for video streaming.
        
        Yields:
            bytes: Encoded frame as JPEG.
        """
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Process the frame for lane detection
            lane_lines = detect_lanes(frame)
            processed_frame = draw_lanes(frame, lane_lines)

            # Encode the frame in JPEG format
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()

            # Yield the frame in the format required by a Flask Response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def release(self):
        """
        Release the video capture resource.
        """
        if self.cap.isOpened():
            self.cap.release()
