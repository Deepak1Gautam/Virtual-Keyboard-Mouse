import cv2
import os
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(
        self,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):

        # Project ka main folder
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # Model file ka complete path
        model_path = os.path.join(
            base_dir,
            "assets",
            "hand_landmarker.task"
        )

        # MediaPipe model setup
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        # Hand detector
        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.timestamp = 0
        self.results = None


    def find_hands(self, frame, draw=True):

        # BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp
        self.timestamp += 1

        # Detect hand
        self.results = self.detector.detect_for_video(
            mp_image,
            self.timestamp
        )

        # Draw landmarks
        if self.results.hand_landmarks:

            for hand in self.results.hand_landmarks:

                height, width, _ = frame.shape

                for landmark in hand:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    if draw:

                        cv2.circle(
                            frame,
                            (x, y),
                            5,
                            (0, 255, 0),
                            cv2.FILLED
                        )

        return frame, self.results


    def find_position(
        self,
        frame,
        hand_number=0
    ):

        landmark_list = []

        if (
            self.results
            and self.results.hand_landmarks
        ):

            hand = self.results.hand_landmarks[
                hand_number
            ]

            height, width, _ = frame.shape

            for landmark_id, landmark in enumerate(hand):

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                landmark_list.append(
                    [
                        landmark_id,
                        x,
                        y
                    ]
                )

        return landmark_list


    # =====================================
    # FINGER DETECTION
    # =====================================

    def fingers_up(self, landmarks):

        fingers = []


        # =========================
        # THUMB
        # =========================

        if landmarks[4][1] < landmarks[3][1]:

            fingers.append(1)

        else:

            fingers.append(0)


        # =========================
        # INDEX FINGER
        # =========================

        if landmarks[8][2] < landmarks[6][2]:

            fingers.append(1)

        else:

            fingers.append(0)


        # =========================
        # MIDDLE FINGER
        # =========================

        if landmarks[12][2] < landmarks[10][2]:

            fingers.append(1)

        else:

            fingers.append(0)


        # =========================
        # RING FINGER
        # =========================

        if landmarks[16][2] < landmarks[14][2]:

            fingers.append(1)

        else:

            fingers.append(0)


        # =========================
        # PINKY FINGER
        # =========================

        if landmarks[20][2] < landmarks[18][2]:

            fingers.append(1)

        else:

            fingers.append(0)


        return fingers