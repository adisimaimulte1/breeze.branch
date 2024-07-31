import cv2
import mediapipe as mp

class HandRecognition():
    def __init__(self):
        # Initialize Mediapipe Hands
        self. mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.8)
        self.mp_draw = mp.solutions.drawing_utils

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        self.hand_x = 0
        self.hand_y = 0

    # Function to count fingers
    def count_fingers(self, hand_landmarks):
        # List to hold which fingers are up
        fingers = []

        # Thumb: Check if the thumb is to the left (right hand) or right (left hand) of the hand's center
        if hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # For fingers: Check if the tip is above the pip joint in y-coordinate
        for i in range(1, 6):
            tip_id = i * 4
            pip_id = tip_id - 2

            if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[pip_id].y:
                fingers.append(1)
            else:
                fingers.append(0)

        finger_number = fingers.count(1) - 1
        return finger_number if finger_number >= 0 else 0

    def update(self):
        success, img = self.cap.read()

        if not success:
            return None

        # Convert the frame to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = self.hands.process(img_rgb)

        # If hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Count fingers
                fingers_up = self.count_fingers(hand_landmarks)

                # Get hand position (using the wrist landmark for simplicity)
                self.hand_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * img.shape[1])
                self.hand_y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * img.shape[0])

                # Display the count on the frame
                cv2.putText(img, f'Fingers: {fingers_up}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
                cv2.putText(img, f'Position: ({self.hand_x}, {self.hand_y})', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show the frame
        cv2.imshow("Hand Tracking", img)

    def getHandPosition(self):
        return (self.hand_x, self.hand_y)
    
    def exit(self):
        # Release the webcam and close windows
        self.cap.release()
        cv2.destroyAllWindows()
