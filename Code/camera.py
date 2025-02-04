import cv2

def main():
    # Open the first camera device available
    capture = cv2.VideoCapture(1)

    if not capture.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = capture.read()

        if not ret:
            print("Error: Failed to capture frame")
            break

        # Display the resulting frame
        cv2.imshow('Camera', frame)

        # Check for user input to stop the video feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture object and close the OpenCV window
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
