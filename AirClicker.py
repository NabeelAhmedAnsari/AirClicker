import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Drawing style
drawing_style = mp.solutions.drawing_utils.DrawingSpec(thickness=2, circle_radius=3)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize camera
camera = cv2.VideoCapture(0)

# Initialize variables
x1 = y1 = x2 = y2 = 0
prev_click_time = 0
click_cooldown = 0.5  # seconds
smoothening = 0.2  # lower = smoother

# Initialize previous mouse coordinates
prev_mouse_x, prev_mouse_y = 0, 0

while True:
    ret, image = camera.read()
    if not ret:
        break

    image = cv2.flip(image, 1)
    image_height, image_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_image)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, drawing_style, drawing_style)
            
            # Get landmark positions
            landmarks = hand_landmarks.landmark
            index_x = int(landmarks[8].x * image_width)
            index_y = int(landmarks[8].y * image_height)
            thumb_x = int(landmarks[4].x * image_width)
            thumb_y = int(landmarks[4].y * image_height)

            # Draw circles
            cv2.circle(image, (index_x, index_y), 8, (0, 255, 0), -1)
            cv2.circle(image, (thumb_x, thumb_y), 8, (255, 0, 0), -1)

            # Move mouse
            screen_x = int(screen_width * landmarks[4].x)
            screen_y = int(screen_height * landmarks[4].y)

            # Smooth movement
            smoothed_x = int(prev_mouse_x + (screen_x - prev_mouse_x) * smoothening)
            smoothed_y = int(prev_mouse_y + (screen_y - prev_mouse_y) * smoothening)
            pyautogui.moveTo(smoothed_x, smoothed_y)
            prev_mouse_x, prev_mouse_y = smoothed_x, smoothed_y

            # Distance for click
            dist = ((index_y - thumb_y) ** 2 + (index_x - thumb_x) ** 2) ** 0.5
            print(f"Distance: {dist:.2f}")

            # Click if close enough and cooldown passed
            current_time = time.time()
            if dist < 40 and (current_time - prev_click_time) > click_cooldown:
                pyautogui.doubleClick()
                print("Clicked!")
                prev_click_time = current_time

    cv2.imshow("Hand Mouse", image)
    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break

camera.release()
cv2.destroyAllWindows()
