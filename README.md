# Gesture-Controlled Mouse using Computer Vision and AI

## Overview

This project utilizes computer vision techniques and artificial intelligence (AI) libraries to enable users to control their computer mouse through specific hand gestures. The focus is on enhancing accessibility for individuals who may have difficulty controlling a standard mouse.

## Libraries Used

- **OpenCV:** Core component for capturing video from the webcam, image processing, and displaying the output to the user.
- **MediaPipe:** Provides robust models for hand tracking, playing a critical role in identifying hand landmarks in real-time.
- **PyAutoGUI:** Empowers the system to simulate mouse movements and clicks, translating the hand gestures into actionable commands.
- **NumPy:** Assists in complex numerical operations, including coordinate transformations and the implementation of smoothing algorithms for stable output.

## Functionality

Using a standard webcam, the system captures video input and processes it through OpenCV and MediaPipe for hand landmark detection. Key finger positions are monitored to discern gestures designated for mouse actions. PyAutoGUI translates these gestures into mouse movements, clicks, and scrolls on the user’s computer.

## Supported Gestures

- **Left Click:** Bringing thumb and index finger close together.
- **Right Click:** Bringing thumb and middle finger close together.
- **Scrolling:** Moving the index finger upward or downward relative to the middle finger.

## Highlights

- **Hand Tracking:** Visual confirmation of the system’s ability to detect and track the hand’s position and finger landmarks accurately.
- **Gesture Recognition:** Reliable recognition of different gestures with visual feedback on the screen, displaying hand landmark overlays.
- **Mouse Control:** Real-time cursor movement on the screen, aligned with the user's hand movements, and responsive clicking and scrolling based on the recognized gestures.
