#!/bin/bash
# Virtual Mouse Application Runner
# This script attempts to run the virtual mouse application with proper setup

echo "=== Virtual Mouse Application ==="
echo "Checking system and dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "mouse.py" ]; then
    echo "Error: mouse.py not found. Please run this script from the project directory."
    exit 1
fi

echo "✓ Project files found"

# Function to check if a Python module exists
check_module() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# Check dependencies
echo "Checking dependencies..."

MISSING_DEPS=""

if ! check_module "cv2"; then
    echo "⚠ OpenCV (cv2) not found"
    MISSING_DEPS="$MISSING_DEPS opencv-python"
else
    echo "✓ OpenCV found"
fi

if ! check_module "numpy"; then
    echo "⚠ NumPy not found"
    MISSING_DEPS="$MISSING_DEPS numpy"
else
    echo "✓ NumPy found"
fi

if ! check_module "mediapipe"; then
    echo "⚠ MediaPipe not found"
    MISSING_DEPS="$MISSING_DEPS mediapipe"
else
    echo "✓ MediaPipe found"
fi

if ! check_module "pyautogui"; then
    echo "⚠ PyAutoGUI not found"
    MISSING_DEPS="$MISSING_DEPS pyautogui"
else
    echo "✓ PyAutoGUI found"
fi

if ! check_module "pynput"; then
    echo "⚠ PyInput not found"
    MISSING_DEPS="$MISSING_DEPS pynput"
else
    echo "✓ PyInput found"
fi

# If dependencies are missing, offer alternatives
if [ ! -z "$MISSING_DEPS" ]; then
    echo ""
    echo "Missing dependencies:$MISSING_DEPS"
    echo ""
    echo "Options:"
    echo "1. Install dependencies: pip install$MISSING_DEPS"
    echo "2. Run algorithm demo (no dependencies needed): python3 algorithm_demo.py"
    echo "3. Try system packages: sudo apt-get install python3-opencv python3-numpy"
    echo ""
    
    read -p "Do you want to run the algorithm demo instead? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Running algorithm demo..."
        python3 algorithm_demo.py
        exit 0
    else
        echo "Please install the missing dependencies and try again."
        exit 1
    fi
fi

# Check display environment
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    echo "⚠ No display environment detected"
    echo "The application requires a GUI environment to show the camera feed."
    echo ""
    read -p "Do you want to run the algorithm demo instead? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Running algorithm demo..."
        python3 algorithm_demo.py
        exit 0
    fi
fi

# All checks passed, run the application
echo ""
echo "All dependencies found! Starting virtual mouse application..."
echo ""
echo "Instructions:"
echo "- Point with your index finger to move the mouse"
echo "- Make gestures for clicks (see SETUP_GUIDE.md for details)"
echo "- Press 'q' to quit"
echo ""

# Set proper Python path for system OpenCV if needed
export PYTHONPATH="/usr/lib/python3/dist-packages:$PYTHONPATH"

# Run the application
python3 mouse.py