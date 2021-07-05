import cv2
import numpy as np


def detectQRCode(img):
    # convert to greyscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # slight blur to remove fine noise
    blur = cv2.blur(grey, (3, 3))
    # canny edge detection
    edges = cv2.Canny(blur, 40, 140)
    # blur edges
    edges_blurred = cv2.blur(edges, (3, 3))
    # threshold 
    _, threshold = cv2.threshold(edges_blurred, 20, 255, cv2.THRESH_BINARY)
    # dilate with 5x5 kernel
    dilated = cv2.dilate(threshold, np.ones((5, 5), "uint8"))

    # get biggest connected component:
    # get list of connected components & their sizes
    _, output, stats, _ = cv2.connectedComponentsWithStats(dilated, connectivity=4)
    # find index of component with largest size
    sizes = stats[:, -1]

    try:
        biggest_shape_index = np.where(sizes == np.amax(sizes[2:]))[0][0]
    except ValueError:
        # no components in image, array size is 0
        # no box will be drawn
        return None

    # create new image where only the pixels of the biggest shape are white
    connected = np.zeros(output.shape)
    connected[output == biggest_shape_index] = 255

    # get bounding box of shape:
    # find contours
    contours, _ = cv2.findContours(connected.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # get rectangle bounding box
    box = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(box)
    box = np.int0(box)

    cv2.imshow("processed", connected)
    return box


if __name__ == "__main__":
    choice = input("Choose video input source:\n\t[1] Webcam\n\t[2] Example mp4\n>>> ")

    while choice not in ("1", "2"):
        choice = input("please choose either 1 or 2 >>> ")
    
    cap = cv2.VideoCapture(0)

    if choice == "2":
        # if you want to try your own mp4, change this filename
        cap = cv2.VideoCapture("example_input.mp4")
        
    print("press q to quit")
        
    while(True):
        ret, frame = cap.read()

        if frame is None:
            break

        # resize frame to be at most max_dim x max_dim
        max_dim = 1000
        h, w, _ = frame.shape
        if h > max_dim and w > max_dim:
            if h > w:
                scale = max_dim / h
            else:
                scale = max_dim / w

            dims = (int(w * scale), int(h* scale))
            frame = cv2.resize(frame, dims)
        
        # get bounding box
        bounding_box = detectQRCode(frame)

        if bounding_box is not None:
            cv2.drawContours(frame, [bounding_box], 0, (0, 255, 0), thickness=3)

        cv2.imshow("detected", frame)

        # stop if q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
