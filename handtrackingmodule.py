"""
Hand Tracking Module
--------------------
A simple Python script using MediaPipe and OpenCV to detect and track hands in real time.

Features:
- Detects up to 2 hands in the webcam feed.
- Draws hand landmarks and connections.
- Prints landmark positions (id, x, y).
- Displays real-time FPS on the video feed.

Author: Jeshwanth Ganesh
"""

import cv2 as cv
import mediapipe as mp
import time


class HandDetector:
    """
    A class for detecting and tracking hands using MediaPipe.
    """

    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        """
        Initializes the hand detection model.

        Parameters:
        - mode (bool): Static mode or live tracking mode.
        - max_hands (int): Maximum number of hands to detect.
        - detection_con (float): Minimum detection confidence.
        - track_con (float): Minimum tracking confidence.
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def findHands(self, img, draw=True):
        """
        Detects hands and draws landmarks on the given image.

        Parameters:
        - img: The BGR image frame.
        - draw (bool): Whether to draw landmarks.

        Returns:
        - img: The image with (optional) drawn landmarks.
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, hand_no=0, draw=True):
        """
        Extracts hand landmark positions.

        Parameters:
        - img: The image frame.
        - hand_no (int): Index of the hand to process.
        - draw (bool): Whether to draw landmark points.

        Returns:
        - lmList: List of [id, x, y] for each landmark.
        """
        lmList = []
        if self.results and self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 8, (255, 0, 255), cv.FILLED)
        return lmList


def main():
    """
    Runs the webcam stream and applies hand detection.
    """
    pTime = 0
    cTime = 0

    cap = cv.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from webcam.")
            break

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=True)

        if lmList:
            print(lmList)  # Example: prints position of landmark 

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime

        # Display FPS on image
        cv.putText(img, f'FPS: {int(fps)}', (10, 70),
                   cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)

        cv.imshow("Hand Tracking", img)
        if cv.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
