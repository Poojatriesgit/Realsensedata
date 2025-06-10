# RealSense RGB-D Image Capture Tool

This Python script captures synchronized RGB and depth frames using an Intel RealSense camera. It shows a live video stream and lets you save individual frames with a mouse click. Useful for creating datasets for 3D vision, machine learning, and robotics.

## Features

- Streams real-time RGB and depth video.
- Aligns depth frames with the color stream.
- Saves:
  - Color images as `.png`
  - Depth images as `.npy` (NumPy format)
- Uses a mouse click to trigger saves.
- Adds a frame offset for custom file naming.
- Automatically handles camera intrinsics and depth scaling.

## Requirements

- Python 3.7 or higher
- Intel RealSense camera
- Intel RealSense SDK
- Python packages:
  - `opencv-python`
  - `numpy`
  - `pyrealsense2`

## Installation

Install the required Python libraries:

```bash
pip install opencv-python numpy pyrealsense2
