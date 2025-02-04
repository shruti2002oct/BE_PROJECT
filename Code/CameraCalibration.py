import cv2
import numpy as np

# Initialize global variables
points = []
capturing_points = True

def click_event(event, x, y, flags, params):
    global points, capturing_points
    if event == cv2.EVENT_LBUTTONDOWN and capturing_points:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('Frame', frame)

        if len(points) == 4:
            capturing_points = False
            cv2.destroyAllWindows()
            process_live_feed()
            # getBoard(points)

def process_live_feed():
    global frame
    pts1 = np.float32([points[0], points[1], points[2], points[3]])
    width_A = np.sqrt(((points[2][0] - points[3][0]) ** 2) + ((points[2][1] - points[3][1]) ** 2))
    width_B = np.sqrt(((points[1][0] - points[0][0]) ** 2) + ((points[1][1] - points[0][1]) ** 2))
    width = max(int(width_A), int(width_B))

    height_A = np.sqrt(((points[1][0] - points[2][0]) ** 2) + ((points[1][1] - points[2][1]) ** 2))
    height_B = np.sqrt(((points[0][0] - points[3][0]) ** 2) + ((points[0][1] - points[3][1]) ** 2))
    height = max(int(height_A), int(height_B))

    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    warped_frame = cv2.warpPerspective(frame, matrix, (width, height))
    cv2.imshow("Warped Frame", warped_frame)

# def getBoard(img):
#     global points, capturing_points
#     width, height = int(800 * 1.2), int(600 * 1.2)
#     ptsl = np.float32(cornerPoints)
#     pts2 = np.float32([[0, 0), [width, 0], [0, height], [width, height]])
#     matrix = cv2.getPerspectiveTransform(pts1, pts2)
#     imgOutput = cv2.warpPerspective(img, matrix, (width, height))
#     for x in range(4):
#         cv2.circle(img, (cornerPoints[x][0], cornerPoints[x][1]), 15, (0, 255, 0), cV2.FILLED)
#     return imgOutput

def getBoard(cornerPoints):
    global frame
    img = frame
    # Define the desired output board dimensions
    width, height = int(800 * 1.5), int(450 * 1.5)

    # Define the destination points for perspective transformation
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Convert cornerPoints to the correct data type
    pts1 = np.float32(cornerPoints)

    # Compute the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Apply the perspective transformation to the input image
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))

    # Visualize the corner points on the input image (for debugging)
    for x in range(4):
        cv2.circle(img, (cornerPoints[x][0], cornerPoints[x][1]), 15, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Warped Frame", imgOutput)

# Start video capture
  # Adjust the device index as needed

frame = cv2.imread('camrato.jpeg') 
cv2.imshow('Frame', frame)
cv2.setMouseCallback('Frame', click_event)
cv2.waitKey(0)


cv2.destroyAllWindows()
