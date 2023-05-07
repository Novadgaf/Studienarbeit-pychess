import cv2
import numpy as np

class ChessCam:
    def __init__(self, playerColor):
        self.playerColor = playerColor
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        # Check if the camera is opened successfully
        if not self.cap.isOpened():
            raise Exception("Error opening video stream or file")
        # Set the resolution to 1920x1080
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.points = self.get_points()
        self.lower_hsv, self.upper_hsv = self.setup_hsv()
        


    def order_points(self, points):
        rect = np.zeros((4, 2), dtype="float32")
        s = points.sum(axis=1)
        rect[0] = points[np.argmin(s)]
        rect[2] = points[np.argmax(s)]
        diff = np.diff(points, axis=1)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]
        return rect


    def four_point_transform(self, image):
        rect = self.order_points(self.points)
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped


    def get_points(self):
        # Define the four corners of the object in the image
        points = []
        def click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                points.append((x, y))
                if len(points) == 4:
                    cv2.destroyWindow('image')
                else:
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                    cv2.imshow('image', frame)

        # Capture frame
        ret, frame = self.cap.read()
        if not ret:
                return np.array(points)
        
        while len(points) < 4:
            # Display the resulting frame
            cv2.imshow('image', frame)
            cv2.setMouseCallback('image', click_event)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        return np.array(points)

    def empty(self, _):
        pass

    def filter_image(self, image, lower_hsv, upper_hsv):
        if self.playerColor == 0b0:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask_white = cv2.inRange(hsv, lower_hsv, upper_hsv)
            filtered = cv2.bitwise_and(image, image, mask=mask_white)
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            mask_black = cv2.inRange(image, lower_hsv, upper_hsv)
            filtered = cv2.bitwise_and(gray, gray, mask=mask_black)
        return filtered

    def apply_button(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            param[0] = True

    def setup_hsv(self):

        cv2.namedWindow("Trackbars")
        cv2.namedWindow("Filtered")

        # Create trackbars for lower HSV values
        cv2.createTrackbar("L - H", "Trackbars", 0, 179, self.empty)
        cv2.createTrackbar("L - S", "Trackbars", 0, 255, self.empty)
        cv2.createTrackbar("L - V", "Trackbars", 0, 255, self.empty)

        # Create trackbars for upper HSV values
        cv2.createTrackbar("U - H", "Trackbars", 179, 179, self.empty)
        cv2.createTrackbar("U - S", "Trackbars", 255, 255, self.empty)
        cv2.createTrackbar("U - V", "Trackbars", 255, 255, self.empty)

        button_pressed = [False]
        cv2.setMouseCallback("Filtered", self.apply_button, button_pressed)

        while not button_pressed[0]:
            _, frame = self.cap.read()
            
            # Get the trackbar positions
            l_h = cv2.getTrackbarPos("L - H", "Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "Trackbars")

            u_h = cv2.getTrackbarPos("U - H", "Trackbars")
            u_s = cv2.getTrackbarPos("U - S", "Trackbars")
            u_v = cv2.getTrackbarPos("U - V", "Trackbars")

            # Set the lower and upper HSV values
            lower_hsv = np.array([l_h, l_s, l_v])
            upper_hsv = np.array([u_h, u_s, u_v])

            # Filter the image
            filtered = self.filter_image(self.four_point_transform(frame), lower_hsv, upper_hsv)

            cv2.imshow("Filtered", filtered)

            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break
        
        cv2.destroyAllWindows()

        return lower_hsv, upper_hsv

    def filter_player_pieces(self, image):
        topdown = self.four_point_transform(image)
        cv2.imshow("TOPDOWN",topdown)
        cv2.waitKey(0)
        

        if self.playerColor == 0b0:
            # Filter out the white pieces
            hsv = cv2.cvtColor(topdown, cv2.COLOR_BGR2HSV)
            mask_white = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
            filtered = cv2.bitwise_and(topdown, topdown, mask=mask_white)
        else:
            # Filter out the black pieces
            gray = cv2.cvtColor(topdown, cv2.COLOR_BGR2GRAY)
            mask_black = cv2.inRange(topdown, self.lower_hsv, self.upper_hsv)
            filtered = cv2.bitwise_and(gray, gray, mask=mask_black)
        
        return filtered


    def get_move(self, imageOld, imageNew):
        filteredOld = self.filter_player_pieces(imageOld)
        filteredNew = self.filter_player_pieces(imageNew)
        cv2.imshow("old",filteredOld)
        cv2.imshow("new",filteredNew)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Apply a Gaussian blur to reduce noise
        blurredOld = cv2.GaussianBlur(filteredOld, (21, 21), 0)
        blurredNew = cv2.GaussianBlur(filteredNew, (21, 21), 0)

        # Calculate the difference between the two frames
        diff = cv2.absdiff(blurredOld, blurredNew)
        # Threshold the difference image to remove small changes
        thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow("diff",diff)
        cv2.imshow("thresh",thresh)
        
        # Apply a series of dilations and erosions to remove noise
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        cv2.imshow("dilate",thresh)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        
        cv2.imshow("erode",thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours
        square_width = filteredOld.shape[1] / 8
        square_height = filteredOld.shape[0] / 8

        move = []
        def f(x):
            a = 1000
            b = 0.01
            return a * np.exp(-b * x)
        
        iterator = 0
        while (len(move) < 2 and iterator<500):
            print(f"iteration: {iterator} equals cont area of {f(iterator)} len move = {len(move)}")
            for contour in contours:
                # If the contour is too small, ignore it
                if cv2.contourArea(contour) < f(iterator):
                    print(cv2.contourArea(contour))
                    continue

                # Compute the bounding box for the contour
                (x, y, w, h) = cv2.boundingRect(contour)

                # Draw the bounding box on the frame
                cv2.rectangle(filteredNew, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Calculate the starting and ending squares of the move
                xvalue = int((x+0.5*w) / square_width)
                yvalue = int((y+0.5*h) / square_height)
                square = chr(97 + xvalue) + str(8- yvalue)
                move.append(square)
                move = list(set(move))
            iterator += 1
        cv2.imshow("new",filteredNew)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return move
    
    def capture_images(self):
        def wait_for_keypress():
            while True:
                if cv2.waitKey(1) & 0xFF == 13:
                    break

        if not self.cap.isOpened():
            raise Exception("Error opening video stream or file")

        
        #ret, frame = self.cap.read()
        #
        #if not ret:
        #    return None
        #
        #initial_image = frame.copy()
        print("Press Enter to capture the new image.")
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            cv2.imshow('image', frame)

            if cv2.waitKey(1) & 0xFF == 13:
                initial_image = frame.copy()
                break

        print("Press Enter to capture the new image.")
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            cv2.imshow('image', frame)

            if cv2.waitKey(1) & 0xFF == 13:
                new_image = frame.copy()
                break

        cv2.destroyAllWindows()

        return self.get_move(initial_image, new_image)