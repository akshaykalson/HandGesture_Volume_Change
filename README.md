# Hand Gesture Volume Control

This project enables real-time hand gesture controlled volume adjustment using OpenCV, Mediapipe, and PyCaw. By dynamically interpreting hand gestures captured through the webcam feed, it adjusts the system volume accordingly.

## Features

- Detects hand landmarks using the Mediapipe library.
- Calculates the distance between two specific landmarks to determine hand gesture.
- Maps hand gesture distance to system volume using PyCaw library.
- Provides real-time feedback through OpenCV visualization.
- Adjustable parameters for volume range and gesture sensitivity.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies:
3. Run the `volume_control.py` script.

## Usage

- Ensure your webcam is properly connected and functioning.
- Run the `volume_control.py` script.
- Adjust the system volume by moving your hand closer or farther apart.
