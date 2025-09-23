#!/usr/bin/env python3
"""
Virtual Mouse using Hand Gesture - Algorithm Demo
Demonstrates the core logic without requiring camera or display.
"""

import numpy as np
import random
import util

def simulate_hand_landmarks():
    """Generate simulated hand landmarks for testing"""
    landmarks = []
    # Create 21 hand landmarks with simulated positions
    base_positions = [
        (0.5, 0.8),    # 0: WRIST
        (0.45, 0.75),  # 1: THUMB_CMC
        (0.4, 0.65),   # 2: THUMB_MCP  
        (0.35, 0.55),  # 3: THUMB_IP
        (0.3, 0.45),   # 4: THUMB_TIP
        (0.5, 0.65),   # 5: INDEX_FINGER_MCP
        (0.5, 0.55),   # 6: INDEX_FINGER_PIP
        (0.5, 0.45),   # 7: INDEX_FINGER_DIP
        (0.5, 0.35),   # 8: INDEX_FINGER_TIP
        (0.55, 0.65),  # 9: MIDDLE_FINGER_MCP
        (0.55, 0.5),   # 10: MIDDLE_FINGER_PIP
        (0.55, 0.4),   # 11: MIDDLE_FINGER_DIP
        (0.55, 0.3),   # 12: MIDDLE_FINGER_TIP
        (0.6, 0.65),   # 13: RING_FINGER_MCP
        (0.6, 0.5),    # 14: RING_FINGER_PIP
        (0.6, 0.4),    # 15: RING_FINGER_DIP
        (0.6, 0.3),    # 16: RING_FINGER_TIP
        (0.65, 0.65),  # 17: PINKY_MCP
        (0.65, 0.55),  # 18: PINKY_PIP
        (0.65, 0.45),  # 19: PINKY_DIP
        (0.65, 0.35),  # 20: PINKY_TIP
    ]
    
    # Add some random variation
    for x, y in base_positions:
        variation_x = (random.random() - 0.5) * 0.1
        variation_y = (random.random() - 0.5) * 0.1
        landmarks.append((x + variation_x, y + variation_y))
    
    return landmarks

def analyze_gesture(landmark_list):
    """Analyze hand gesture and determine action"""
    if len(landmark_list) < 21:
        return "No hand detected"
    
    # Calculate distances and angles
    thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
    
    # Index finger angle
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    
    # Middle finger angle  
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    
    # Gesture recognition logic
    if thumb_index_dist < 50 and index_angle > 90:
        return f"Mouse Control Mode (thumb-index: {thumb_index_dist:.1f}, index angle: {index_angle:.1f}°)"
    elif index_angle < 50 and middle_angle > 90 and thumb_index_dist > 50:
        return f"Left Click (index: {index_angle:.1f}°, middle: {middle_angle:.1f}°, dist: {thumb_index_dist:.1f})"
    elif middle_angle < 50 and index_angle > 90 and thumb_index_dist > 50:
        return f"Right Click (index: {index_angle:.1f}°, middle: {middle_angle:.1f}°, dist: {thumb_index_dist:.1f})"
    elif index_angle < 50 and middle_angle < 50 and thumb_index_dist > 50:
        return f"Double Click (index: {index_angle:.1f}°, middle: {middle_angle:.1f}°, dist: {thumb_index_dist:.1f})"
    elif index_angle < 50 and middle_angle < 50 and thumb_index_dist < 50:
        return f"Screenshot (index: {index_angle:.1f}°, middle: {middle_angle:.1f}°, dist: {thumb_index_dist:.1f})"
    else:
        return f"Neutral (index: {index_angle:.1f}°, middle: {middle_angle:.1f}°, dist: {thumb_index_dist:.1f})"

def main():
    """Demo the virtual mouse gesture recognition"""
    print("=== Virtual Mouse Hand Gesture Recognition Demo ===")
    print("This demo simulates hand landmarks and shows gesture recognition.")
    print("")
    
    print("Testing various hand gestures:")
    print("-" * 50)
    
    # Test multiple scenarios
    scenarios = [
        "Normal hand position",
        "Index finger extended (pointing)",
        "Thumb and index close together", 
        "Index finger bent (click gesture)",
        "Both index and middle bent",
        "Fist gesture"
    ]
    
    for i, scenario in enumerate(scenarios):
        print(f"\n{i+1}. {scenario}:")
        
        # Generate landmarks for this scenario
        landmarks = simulate_hand_landmarks()
        
        # Modify landmarks based on scenario
        if "pointing" in scenario:
            # Extend index finger more
            landmarks[8] = (landmarks[8][0], landmarks[8][1] - 0.1)
        elif "close together" in scenario:
            # Move thumb closer to index
            landmarks[4] = (landmarks[5][0] - 0.05, landmarks[5][1])
        elif "Index finger bent" in scenario:
            # Bend index finger
            landmarks[8] = (landmarks[6][0], landmarks[6][1] + 0.05)
        elif "Both index and middle bent" in scenario:
            # Bend both fingers
            landmarks[8] = (landmarks[6][0], landmarks[6][1] + 0.05)
            landmarks[12] = (landmarks[10][0], landmarks[10][1] + 0.05)
        elif "Fist" in scenario:
            # All fingers bent
            for tip_idx in [8, 12, 16, 20]:  # Finger tips
                landmarks[tip_idx] = (landmarks[tip_idx-2][0], landmarks[tip_idx-2][1] + 0.02)
        
        # Analyze the gesture
        result = analyze_gesture(landmarks)
        print(f"   Result: {result}")
        
        # Show some key measurements
        thumb_tip = landmarks[4]
        index_mcp = landmarks[5] 
        index_tip = landmarks[8]
        
        print(f"   Key points: Thumb tip: ({thumb_tip[0]:.2f}, {thumb_tip[1]:.2f})")
        print(f"               Index MCP: ({index_mcp[0]:.2f}, {index_mcp[1]:.2f})")
        print(f"               Index tip: ({index_tip[0]:.2f}, {index_tip[1]:.2f})")
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("\nNote: In a real application, these landmarks would come from MediaPipe")
    print("hand tracking, and the mouse actions would control the actual cursor.")
    print("\nGesture Recognition Logic:")
    print("- Mouse Control: Thumb close to index finger + index extended")
    print("- Left Click: Index finger bent + middle finger extended")  
    print("- Right Click: Middle finger bent + index finger extended")
    print("- Double Click: Both index and middle fingers bent")
    print("- Screenshot: All fingers bent + thumb close to index")

if __name__ == '__main__':
    main()