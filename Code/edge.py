import cv2
import numpy as np
from FindBalloon import *
from detectHit import *
from calbi import *


def main():
    # Create a VideoCapture object to capture video from the camera
    video_path = 'videoTest.mp4'  # Update with your file path
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)# Use 0 for the default camera (usually webcam)
    points = pickle.load(open('calibration.pkl','rb'))
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break


        frame = getBoard(frame,points)
        
        # Find balloons and bounding boxes in the frame
        imgBalloons, bboxs = findBalloons(frame)

        # Detect hits on balloons
        frame = detectHit(frame, bboxs)

        # Resize the balloon image for display


        # Display Sobel Edge Detection Images (for balloons)
        cv2.imshow('Balloons', imgBalloons)

        # Display the processed frame with detected hits
        cv2.imshow('Processed Frame', frame)

        # Check for user input to exit (press 'q' to quit)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
