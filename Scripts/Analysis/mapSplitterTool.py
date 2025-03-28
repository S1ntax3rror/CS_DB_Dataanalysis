import cv2
import pyperclip


# Initialize variables
start_point = None
end_point = None
start_point_off = None
end_point_off = None
current_point = None
cropping = False

def mouse_callback(event, x, y, flags, param):
    global start_point, end_point, start_point_off, end_point_off, current_point, cropping

    # Get the current window size
    window_width, window_height = cv2.getWindowImageRect("Image")[2:4]

    # Calculate aspect ratios
    x_ratio = window_width / image.shape[0]
    y_ratio = window_height / image.shape[1]

    orig_x = int(x / x_ratio)
    orig_y = int(y / y_ratio)

    if event == cv2.EVENT_LBUTTONDOWN:  # Start drawing rectangle
        start_point = (orig_x, orig_y)
        start_point_off = (x, y)
        current_point = (x, y)
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE and cropping:  # Update endpoint dynamically
        current_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:  # Finalize rectangle
        end_point = (orig_x, orig_y)
        end_point_off = (x, y)
        cropping = False
        # print(f"Original coordinates: Top-left: {start_point}, Bottom-right: {end_point}")
        print(f"OFF coordinates: Top-left: {start_point_off}, Bottom-right: {end_point_off}")
        copystring = ("(" + str(start_point_off[0]) + "," +  str(start_point_off[1]) + ")" +
                      "," + str(end_point_off[0]-start_point_off[0]) + "," + str(end_point_off[1]-start_point_off[1]))
        pyperclip.copy(copystring)
        print(copystring.strip(" "))

# Load the image
image = cv2.imread("../../Resources/maps/de_nuke.png")
clone = image.copy()

# Create a resizable window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1500, 1000)
cv2.setMouseCallback("Image", mouse_callback)
print(cv2.getWindowImageRect("Image")[2:4])

while True:
    temp_image = clone.copy()

    if start_point and current_point:  # Draw rectangle dynamically
        cv2.rectangle(temp_image, start_point_off, current_point, (0, 255, 0), 2)

    cv2.imshow("Image", temp_image)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Exit on pressing 'ESC'
        break

cv2.destroyAllWindows()


"../../Resources/maps/de_mirage.png"