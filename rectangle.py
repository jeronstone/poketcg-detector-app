import cv2
import numpy as np

# Load the image
image = cv2.imread('/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/IMG_5301.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, 10, 100)

# Use morphological operations to close gaps in the edges
kernel = np.ones((5, 5), np.uint8)
edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
cv2.imshow("Contours", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sort contours by area, largest first
contours = sorted(contours, key=cv2.contourArea, reverse=True)

for contour in contours:
    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # If we find a four-sided polygon, assume it's the card
    if len(approx) == 4:
        card_corners = approx
        break

# Order the points for perspective transformation
pts = card_corners.reshape(4, 2)
rect = np.zeros((4, 2), dtype="float32")

s = pts.sum(axis=1)
rect[0] = pts[np.argmin(s)]  # Top-left
rect[2] = pts[np.argmax(s)]  # Bottom-right

diff = np.diff(pts, axis=1)
rect[1] = pts[np.argmin(diff)]  # Top-right
rect[3] = pts[np.argmax(diff)]  # Bottom-left

# Define the destination points for the warp (standard card size ratio)
width = 400
height = int(width * 1.4)  # Pokémon cards are roughly 2.5x3.5 inches

dst = np.array([
    [0, 0],
    [width - 1, 0],
    [width - 1, height - 1],
    [0, height - 1]
], dtype="float32")

# Apply perspective transform
matrix = cv2.getPerspectiveTransform(rect, dst)
cropped = cv2.warpPerspective(image, matrix, (width, height))

# Save or return the cropped image
if False:
    cv2.imwrite('./rectangle.jpg', cropped)


# Show result
if cropped is not None:
    cv2.imshow("Cropped Card", cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
