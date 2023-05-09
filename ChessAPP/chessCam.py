import cv2
import numpy as np
from typing import Any, List, Optional, Tuple, Union

class ChessCam:
    def __init__(self, playerColor: int):
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
        

    def order_points(self) -> np.ndarray:
        """
        Order the points in a consistent manner (top-left, top-right, bottom-right, bottom-left).

        Returns:
            np.ndarray: The ordered points.
        """
        # Initialize an array with the same shape as the input points
        ordered_points = np.zeros((4, 2), dtype="float32")

        # Calculate the sum of the point coordinates (x, y)
        coord_sum = self.points.sum(axis=1)

        # Assign the top-left point (smallest sum) and bottom-right point (largest sum)
        ordered_points[0] = self.points[np.argmin(coord_sum)]
        ordered_points[2] = self.points[np.argmax(coord_sum)]

        # Calculate the difference between the point coordinates (x, y)
        coord_diff = np.diff(self.points, axis=1)

        # Assign the top-right point (smallest difference) and bottom-left point (largest difference)
        ordered_points[1] = self.points[np.argmin(coord_diff)]
        ordered_points[3] = self.points[np.argmax(coord_diff)]

        return ordered_points


    def four_point_transform(self, image: np.ndarray) -> np.ndarray:
        """
        Apply a perspective transformation to obtain a top-down view of the chessboard.

        Args:
            image (np.ndarray): The input image.

        Returns:
            np.ndarray: The transformed image.
        """
        # Order the points (top-left, top-right, bottom-right, bottom-left)
        ordered_points = self.order_points()
        
        # Calculate the width and height of the new image
        maxWidth, maxHeight = self.calculate_transform_dimensions(ordered_points)

        # Create the destination points for the perspective transformation
        destination_points = np.array(
            [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
            dtype="float32"
        )

        # Calculate the transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(ordered_points, destination_points)

        # Apply the perspective transformation
        transformed_image = cv2.warpPerspective(image, transformation_matrix, (maxWidth, maxHeight))

        return transformed_image

    def calculate_transform_dimensions(self, ordered_points: np.ndarray) -> Tuple[int, int]:
        """
        Calculate the dimensions of the transformed image after applying a perspective transformation.

        Args:
            ordered_points (np.ndarray): The ordered corner points of the chessboard (top-left, top-right, bottom-right, bottom-left).

        Returns:
            Tuple[int, int]: The width and height of the transformed image.
        """
        # Unpack the ordered points
        (top_left, top_right, bottom_right, bottom_left) = ordered_points

        # Calculate the width of the transformed image
        # Measure the distance between bottom-right and bottom-left points
        widthA = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
        # Measure the distance between top-right and top-left points
        widthB = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
        # The width of the transformed image is the maximum of the two distances
        maxWidth = max(int(widthA), int(widthB))

        # Calculate the height of the transformed image
        # Measure the distance between top-right and bottom-right points
        heightA = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
        # Measure the distance between top-left and bottom-left points
        heightB = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
        # The height of the transformed image is the maximum of the two distances
        maxHeight = max(int(heightA), int(heightB))

        return maxWidth, maxHeight


    def get_points(self) -> np.ndarray:
        """
        Get the four corner points of the chessboard in the image.

        Returns:
            np.ndarray: An array of 2D points representing the corners of the chessboard.
        """
        points = []
        circle_radius = 5
        circle_color = (0, 255, 0)

        def click_event(event: int, x: int, y: int, flags: int, params: Any) -> None:
            """
            Mouse click event handler to get the clicked points.

            Args:
                event (int): The type of event.
                x (int): The x-coordinate of the clicked point.
                y (int): The y-coordinate of the clicked point.
                flags (int): Additional flags for the event.
                params (Any): Additional parameters for the event.
            """
            if event == cv2.EVENT_LBUTTONDOWN:
                points.append((x, y))
                if len(points) == 4:
                    cv2.destroyWindow('image')
                else:
                    cv2.circle(frame, (x, y), circle_radius, circle_color, -1)
                    cv2.imshow('image', frame)

        # Capture frame
        ret, frame = self.cap.read()
        if not ret:
            return np.array(points)

        # Collect points until four points are clicked
        while len(points) < 4:
            # Display the resulting frame
            cv2.imshow('image', frame)
            cv2.setMouseCallback('image', click_event)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        return np.array(points)


    @staticmethod
    def empty(_: Any) -> None:
        """
        Empty function to use as a placeholder for the trackbar callback.

        Args:
            _ (Any): Placeholder argument, not used.
        """
        pass


    def filter_image(self, image: np.ndarray, lower_hsv: np.ndarray, upper_hsv: np.ndarray) -> np.ndarray:
        """
        Filter the image based on the player's color and the given HSV values.

        Args:
            image (np.ndarray): The input image.
            lower_hsv (np.ndarray): The lower HSV values for the color range.
            upper_hsv (np.ndarray): The upper HSV values for the color range.

        Returns:
            np.ndarray: The filtered image.
        """
        # If the player's color is white (0b0)
        if self.playerColor == 0b0:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            white_mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
            filtered_image = cv2.bitwise_and(image, image, mask=white_mask)
        # If the player's color is black
        else:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            black_mask = cv2.inRange(image, lower_hsv, upper_hsv)
            filtered_image = cv2.bitwise_and(gray_image, gray_image, mask=black_mask)
        
        return filtered_image


    def apply_button(self, event: int, x: int, y: int, flags: int, param: List[bool]) -> None:
        """
        Mouse click event handler for the apply button.

        Args:
            event (int): The type of event.
            x (int): The x-coordinate of the clicked point.
            y (int): The y-coordinate of the clicked point.
            flags (int): Additional flags for the event.
            param (List[bool]): A list containing a single boolean that indicates if the button was pressed.
        """
        if event == cv2.EVENT_LBUTTONUP:
            param[0] = True


    def setup_hsv(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Set up the HSV values for filtering the player's pieces.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The lower and upper HSV values for filtering the player's pieces.
        """
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

        # Continue until the Apply button is pressed
        while not button_pressed[0]:
            _, frame = self.cap.read()

            # Get the trackbar positions
            lower_h = cv2.getTrackbarPos("L - H", "Trackbars")
            lower_s = cv2.getTrackbarPos("L - S", "Trackbars")
            lower_v = cv2.getTrackbarPos("L - V", "Trackbars")

            upper_h = cv2.getTrackbarPos("U - H", "Trackbars")
            upper_s = cv2.getTrackbarPos("U - S", "Trackbars")
            upper_v = cv2.getTrackbarPos("U - V", "Trackbars")

            # Set the lower and upper HSV values
            lower_hsv_values = np.array([lower_h, lower_s, lower_v])
            upper_hsv_values = np.array([upper_h, upper_s, upper_v])

            # Filter the image
            filtered_image = self.filter_image(self.four_point_transform(frame), lower_hsv_values, upper_hsv_values)

            cv2.imshow("Filtered", filtered_image)

            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break

        cv2.destroyAllWindows()

        return lower_hsv_values, upper_hsv_values


    def filter_player_pieces(self, image: np.ndarray) -> np.ndarray:
        """
        Filters out player pieces from the given image.

        Args:
            image (np.ndarray): The input image.

        Returns:
            np.ndarray: The filtered image containing only player pieces.
        """
        top_down_image = self.four_point_transform(image)

        if self.playerColor == 0b0:
            # Filter out the white pieces
            hsv = cv2.cvtColor(top_down_image, cv2.COLOR_BGR2HSV)
            white_pieces_mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
            filtered_image = cv2.bitwise_and(top_down_image, top_down_image, mask=white_pieces_mask)
            filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        else:
            # Filter out the black pieces
            gray_image = cv2.cvtColor(top_down_image, cv2.COLOR_BGR2GRAY)
            black_pieces_mask = cv2.inRange(top_down_image, self.lower_hsv, self.upper_hsv)
            filtered_image = cv2.bitwise_and(gray_image, gray_image, mask=black_pieces_mask)

        return filtered_image


    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess the given image by filtering player pieces and applying Gaussian blur.

        Args:
            image (np.ndarray): The input image.

        Returns:
            np.ndarray: The preprocessed image.
        """
        filtered_image = self.filter_player_pieces(image)
        blurred_image = cv2.GaussianBlur(filtered_image, (21, 21), 0)
        return blurred_image

    def compute_difference(self, image_old: np.ndarray, image_new: np.ndarray) -> np.ndarray:
        """
        Compute the difference between two preprocessed images and apply thresholding, dilation, and erosion.

        Args:
            image_old (np.ndarray): The first preprocessed image.
            image_new (np.ndarray): The second preprocessed image.

        Returns:
            np.ndarray: The thresholded difference image.
        """
        diff = cv2.absdiff(image_old, image_new)
        thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        return thresh

    def get_contours(self, thresh: np.ndarray) -> List[np.ndarray]:
        """
        Extract contours from the given thresholded difference image.

        Args:
            thresh (np.ndarray): The thresholded difference image.

        Returns:
            List[np.ndarray]: A list of contours.
        """
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def calculate_exponential_decay(self, iterator: int) -> float:
        """
        Calculate the exponential decay function value for the given iterator.

        Args:
            iterator (int): The iterator value.

        Returns:
            float: The calculated decay value.
        """
        a = 1000
        b = 0.01
        return a * np.exp(-b * iterator)

    def get_move(self, image_old: np.ndarray, image_new: np.ndarray) -> List[str]:
        """
        Identifies the move made by the player between two images.

        Args:
            image_old (np.ndarray): The initial image.
            image_new (np.ndarray): The new image after the move.

        Returns:
            List[str]: The identified move.
        """
        preprocessed_old = self.preprocess_image(image_old)
        preprocessed_new = self.preprocess_image(image_new)

        thresh = self.compute_difference(preprocessed_old, preprocessed_new)
        contours = self.get_contours(thresh)

        square_width = preprocessed_old.shape[1] / 8
        square_height = preprocessed_old.shape[0] / 8

        move = []
        iterator = 0

        while len(move) < 2 and iterator < 500:
            for contour in contours:
                contour_area = cv2.contourArea(contour)

                if contour_area < self.calculate_exponential_decay(iterator):
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(preprocessed_new, (x, y), (x + w, y + h), (255, 0, 0), 2)

                x_center = x + 0.5 * w
                y_center = y + 0.5 * h

                x_value = int(x_center / square_width)
                y_value = int(y_center / square_height)

                square = chr(104 - x_value) + str(1 + y_value)
                move.append(square)
                move = list(set(move))
            iterator += 1
        cv2.imshow("new",preprocessed_new)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return move
    

    def capture_images(self) -> Optional[List[str]]:
        """
        Captures two images: initial state and new state after a move, then
        identifies the move made by the player.

        Returns:
            Optional[List[str]]: The identified move, or None if there is an error
                                 reading the video stream or file.
        """

        def wait_for_keypress() -> None:
            """
            Waits for the Enter key to be pressed.
            """
            while True:
                if cv2.waitKey(1) & 0xFF == 13:
                    break

        if not self.cap.isOpened():
            raise Exception("Error opening video stream or file")

        ret, frame = self.cap.read()

        if not ret:
            return None

        initial_image = frame.copy()

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