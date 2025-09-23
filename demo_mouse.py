#!/usr/bin/env python3
"""
Virtual Mouse using Hand Gesture - Simplified Demo Version
This version demonstrates the application structure and can run without display dependencies.
"""

import cv2
import numpy as np
import random
import util

# Mock classes to replace unavailable dependencies
class MockMediapipe:
    """Mock mediapipe for demonstration"""
    class solutions:
        class hands:
            class Hands:
                def __init__(self, **kwargs):
                    print("Mock MediaPipe Hands initialized")
                    
                def process(self, image):
                    # Return mock hand landmarks
                    return MockHandResult()
                
        class drawing_utils:
            @staticmethod
            def draw_landmarks(image, landmarks, connections):
                # Mock drawing - just add text
                cv2.putText(image, "Mock Hand Landmarks", (10, 200), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
        HAND_CONNECTIONS = []  # Mock connections
        
        class HandLandmark:
            INDEX_FINGER_TIP = 8

class MockHandResult:
    """Mock hand detection result"""
    def __init__(self):
        # Create 21 mock landmarks (standard hand model)
        self.multi_hand_landmarks = [MockHandLandmarks()] if random.random() > 0.3 else None

class MockHandLandmarks:
    """Mock hand landmarks"""
    def __init__(self):
        # Create 21 mock landmarks with random but reasonable positions
        self.landmark = []
        for i in range(21):
            self.landmark.append(MockLandmark(
                x=0.3 + random.random() * 0.4,  # Center region
                y=0.3 + random.random() * 0.4   # Center region
            ))

class MockLandmark:
    """Mock individual landmark"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockMouse:
    """Mock mouse controller"""
    class Button:
        left = "left"
        right = "right"
        
    def press(self, button):
        print(f"Mock mouse press: {button}")
        
    def release(self, button):
        print(f"Mock mouse release: {button}")

class MockPyAutoGUI:
    """Mock pyautogui functionality"""
    @staticmethod
    def size():
        return (1920, 1080)  # Mock screen size
        
    @staticmethod
    def moveTo(x, y, duration=0.001):
        print(f"Mock mouse move to: ({x}, {y})")
        
    @staticmethod
    def doubleClick():
        print("Mock double click")
        
    @staticmethod
    def screenshot():
        print("Mock screenshot taken")
        return MockImage()

class MockImage:
    """Mock image for screenshot"""
    def save(self, filename):
        print(f"Mock image saved as: {filename}")

# Initialize mock objects
mp = MockMediapipe()
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)
mouse = MockMouse()
pyautogui = MockPyAutoGUI()

screen_width, screen_height = pyautogui.size()

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x, y, duration=0.001)

def is_left_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        thumb_index_dist > 50
    )

def is_double_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist > 50
    )

def is_screenshot(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist < 50
    )

def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if util.get_distance([landmark_list[4], landmark_list[5]]) < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
            cv2.putText(frame, "Mouse Control Mode", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.press(MockMouse.Button.left)
            mouse.release(MockMouse.Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(MockMouse.Button.right)
            mouse.release(MockMouse.Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def main():
    print("Virtual Mouse Application Starting...")
    print("Demo mode - using mock dependencies")
    print("Press 'q' to quit the application")
    
    draw = mp.solutions.drawing_utils
    
    # Try to open camera, fallback to mock video if not available
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Camera not available - running in simulation mode")
        # Create a black frame for demo
        mock_frame = True
    else:
        print("Camera opened successfully")
        mock_frame = False

    frame_count = 0
    try:
        while True:
            if mock_frame:
                # Create a simulated frame
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                frame_count += 1
                
                # Add some visual elements to simulate video
                cv2.circle(frame, (320 + int(50 * np.sin(frame_count * 0.1)), 240), 20, (0, 255, 0), -1)
                cv2.putText(frame, "Simulated Camera Feed", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Frame: {frame_count}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                ret = True
            else:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame")
                    break
                frame = cv2.flip(frame, 1)
            
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            # Add instruction text
            cv2.putText(frame, "Virtual Mouse Demo", (10, frame.shape[0] - 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow('Virtual Mouse - Hand Gesture Control', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting application...")
                break
                
            # In simulation mode, limit frames
            if mock_frame and frame_count > 300:  # Stop after 300 frames in simulation
                print("Simulation complete")
                break
                
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if not mock_frame:
            cap.release()
        cv2.destroyAllWindows()
        print("Application closed successfully")

if __name__ == '__main__':
    main()