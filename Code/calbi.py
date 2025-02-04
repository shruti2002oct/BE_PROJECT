import cv2
import numpy as np
import pickle

# Initialize global variables
points = []
capturing_points = True

def click_event(event, x, y, flags, params):
    global points, capturing_points
    if event == cv2.EVENT_LBUTTONDOWN and capturing_points:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(frame_copy, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('Frame', frame_copy)

        if len(points) == 4:
            capturing_points = False
            cv2.destroyAllWindows()
            file_path = 'calibration.pkl'
            with open(file_path, 'wb') as file:
                pickle.dump(points, file)

def getBoard(frame, points):
    # Define the desired output board dimensions
    width, height = int(1366), int(768)

    # Define the destination points for perspective transformation
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Convert cornerPoints to the correct data type
    pts1 = np.float32(points)

    # Compute the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Apply the perspective transformation to the input image
    warped_frame = cv2.warpPerspective(frame, matrix, (width, height))
    
    return warped_frame

def main():
    global frame, frame_copy, capturing_points
    video_path = 'videoTest.mp4'  # Update with your file path
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or adjust accordingly
    cap.set(3,1280)
    cap.set(4,720)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        frame_copy = frame.copy()
        cv2.imshow('Frame', frame_copy)

        if capturing_points:
            cv2.setMouseCallback('Frame', click_event)
        else:
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
