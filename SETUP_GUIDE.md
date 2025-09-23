# Virtual Mouse using Hand Gesture - Setup Guide

## Overview
This project implements a virtual mouse that can be controlled using hand gestures detected through a camera. The application uses computer vision to track hand landmarks and interprets various gestures as mouse actions.

## Features
- **Mouse Control**: Move cursor by pointing with index finger
- **Left Click**: Bend index finger while keeping middle finger extended
- **Right Click**: Bend middle finger while keeping index finger extended  
- **Double Click**: Bend both index and middle fingers
- **Screenshot**: Make a fist with thumb close to index finger

## Requirements

### Required Dependencies
- **OpenCV** (`cv2`) - For camera input and image processing
- **MediaPipe** (`mediapipe`) - For hand landmark detection
- **PyAutoGUI** (`pyautogui`) - For mouse control and screen interaction
- **PyInput** (`pynput`) - For advanced mouse control
- **NumPy** (`numpy`) - For mathematical calculations

### Installation

#### Option 1: Using pip
```bash
pip install opencv-python mediapipe pyautogui pynput numpy
```

#### Option 2: Using conda
```bash
conda install -c conda-forge opencv pyautogui pynput numpy
# Note: mediapipe may need to be installed via pip
pip install mediapipe
```

#### Option 3: System packages (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-opencv python3-numpy
pip install mediapipe pyautogui pynput
```

## Files in Repository

### Main Application Files
- **`mouse.py`** - Main application with full functionality
- **`virtual mouse TEST/mouse.py`** - Alternative version for testing
- **`util.py`** - Utility functions for angle and distance calculations

### Demo Files
- **`simple_mouse.py`** - Basic camera test without hand tracking
- **`demo_mouse.py`** - Full demo with mock dependencies  
- **`algorithm_demo.py`** - Algorithm demonstration without camera/display

### Documentation
- **`mouse comment/`** - Directory with commented versions explaining the code
- **`README.md`** - This setup guide

## Running the Application

### Full Application (requires all dependencies)
```bash
python3 mouse.py
```

### Demo Versions (for testing/development)
```bash
# Test camera functionality only
python3 simple_mouse.py

# Test with mock hand tracking (no camera needed)
python3 demo_mouse.py

# Test gesture recognition algorithms (no camera/display needed)
python3 algorithm_demo.py
```

## Usage Instructions

1. **Start the application**: Run `python3 mouse.py`
2. **Position yourself**: Sit in front of the camera with good lighting
3. **Hand position**: Keep your hand visible in the camera frame
4. **Control mouse**: 
   - Point with index finger to move cursor
   - Make gestures for clicks (see Features section)
5. **Exit**: Press 'q' key to quit

## Gesture Guide

| Gesture | Action | Description |
|---------|--------|-------------|
| Point with index finger (thumb close) | Mouse movement | Move cursor around screen |
| Bend index finger | Left click | Click on items |
| Bend middle finger | Right click | Context menus |
| Bend both index & middle | Double click | Open files/apps |
| Make fist (thumb close to index) | Screenshot | Capture screen |

## Troubleshooting

### Camera Issues
- Ensure camera is connected and not used by other applications
- Try different camera indices: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`
- Check camera permissions

### Import Errors
- Install missing dependencies: `pip install <package_name>`
- For OpenCV issues on Linux: `sudo apt-get install python3-opencv`
- For display issues: Ensure you have a GUI environment

### Performance Issues
- Ensure good lighting for hand detection
- Reduce MediaPipe model complexity in code
- Close other camera applications

### Hand Detection Problems
- Keep hand clearly visible and well-lit
- Avoid busy backgrounds
- Ensure hand is at appropriate distance from camera

## Development Notes

### Algorithm Details
The application uses MediaPipe to detect 21 hand landmarks, then calculates:
- **Distances** between key points (thumb tip to index finger base)
- **Angles** between finger segments to detect bent/extended fingers
- **Gesture classification** based on these measurements

### Code Structure
- `find_finger_tip()` - Locates index finger tip for cursor movement
- `is_left_click()`, `is_right_click()`, etc. - Gesture recognition functions
- `detect_gesture()` - Main gesture processing and action execution
- `main()` - Camera loop and application control

### Customization
You can modify gesture sensitivity by adjusting thresholds in the recognition functions:
- Distance thresholds (currently 50 pixels)
- Angle thresholds (currently 50-90 degrees)
- MediaPipe confidence settings

## Security Notes
- The application requires camera access
- Mouse control permissions may need to be granted on some systems
- Screenshots are saved in the current directory

## Platform Support
- **Linux**: Full support with proper dependencies
- **Windows**: Full support 
- **macOS**: Full support (may need additional permissions)

## License
This project is open source. Please check the repository for license details.