# Copyright 2024 ritik
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import requests
import numpy as np

def start_video_processing(motion_detected_callback):
    """Starts continuous video processing from the webcam.

    Args:
        motion_detected_callback (function): A function to be called when motion is detected, 
                                             takes the captured frame as input. 
    """
    cap = cv2.VideoCapture(0)  # Open the webcam
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=50)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame. Exiting.")
            break

        # Motion Detection
        fg_mask = background_subtractor.apply(frame)
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
        fg_mask = cv2.erode(fg_mask, None, iterations=2)  # Reduce noise (optional)
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)  # Reduce noise (optional)

        # Check for significant Motion
        if detect_significant_motion(fg_mask):
            motion_detected_callback(frame) 

        # Display (optional - for debugging)
        cv2.imshow('Frame', frame)
        cv2.imshow('Motion Mask', fg_mask)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# The callback function to be called when motion is detected
def detect_significant_motion(mask):
    """Determines if significant motion is detected.

    Args:
        mask (numpy.ndarray): The foreground mask.

    Returns:
        bool: True if significant motion is detected, False otherwise.
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    MIN_CONTOUR_AREA = 500  # Adjust this threshold

    for contour in contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            return True
    return False



def handle_motion(image):
    """Handles the action to take when motion is detected.

    Args:
        image (numpy.ndarray): Captured image frame.
    """
    _, img_encoded = cv2.imencode('.jpg', image)  # Encode image as JPEG
    response = requests.post('http://127.0.0.1:5000/process-image', 
    data=img_encoded.tobytes())  # Send to Flask route
