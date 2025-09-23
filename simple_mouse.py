#!/usr/bin/env python3
"""
Simple Virtual Mouse Demo - Basic camera capture functionality
This version works with minimal dependencies and shows the core camera functionality.
"""

import cv2
import numpy as np

def main():
    """Main function to run the virtual mouse demo"""
    print("Virtual Mouse Demo Starting...")
    print("Press 'q' to quit")
    print("Note: Full hand gesture functionality requires mediapipe, pyautogui, and pynput")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip frame horizontally (mirror effect)
            frame = cv2.flip(frame, 1)
            
            # Add instructions to the frame
            cv2.putText(frame, "Virtual Mouse Demo", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Full functionality requires:", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.putText(frame, "- mediapipe (hand detection)", (10, 130), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.putText(frame, "- pyautogui (mouse control)", (10, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.putText(frame, "- pynput (advanced mouse control)", (10, 170), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Show frame
            cv2.imshow('Virtual Mouse - Camera Feed', frame)
            
            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting...")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed")

if __name__ == '__main__':
    main()