import pyrealsense2 as rs
import numpy as np
import cv2
import os

# Set up the RealSense pipeline
pipeline = rs.pipeline()

# Configure the pipeline to stream color and depth frames
config = rs.config()
color_stream=config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 6)  # Color stream
depth_stream=config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)  # Depth stream
#left_ir=config.enable_stream(rs.stream.infrared, 1, 1280,720, rs.format.y8, 6)
align_to = rs.stream.color
align = rs.align(align_to)

# Start streaming
profile=pipeline.start(config)
depth_stream = profile.get_stream(rs.stream.depth)
intrinsics = depth_stream.as_video_stream_profile().get_intrinsics()
depth_sensor = profile.get_device().first_depth_sensor()
if depth_sensor.supports(rs.option.depth_units):
    depth_sensor.set_option(rs.option.depth_units,0.001)
if depth_sensor.supports(rs.option.laser_power):
    # Set laser power to 0 to disable the projector
    depth_sensor.set_option(rs.option.laser_power, 100)
# Create a directory to save the images
save_dir_image = r'C:\Users\pooja\OneDrive\Desktop\data\output_image'
save_dir_depth = r'C:\Users\pooja\OneDrive\Desktop\data\output_depth'

frame_count = 0
frame_offset = 47
# Callback function for mouse click event
def save_image_on_click(event, x, y, flags, param):
    global color_image, depth_image, frame_count, save_dir
    # Check if the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Save the color image
        color_filename = os.path.join(save_dir_image, f"test_{frame_count+frame_offset:04d}.png")
        cv2.imwrite(color_filename, color_image)

        npy_depth_filename = os.path.join(save_dir_depth, f"depth_raw_{frame_count+frame_offset:04d}.npy")
        np.save(npy_depth_filename, depth_image)

        # Increment frame count
    
        print(f"Frame {frame_count+frame_offset} saved!")
        frame_count += 1
# Set up the OpenCV window and bind mouse callback
cv2.namedWindow("RealSense Video Feed")
cv2.setMouseCallback("RealSense Video Feed", save_image_on_click)

try:
    while True:
        # Wait for a coherent pair of frames: color and depth
        frames = pipeline.wait_for_frames()
        frames = align.process(frames)
        # Get the color and depth frames
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        # Convert the color frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Convert the depth frame to a numpy array (depth values in mm)
        depth_image = np.asanyarray(depth_frame.get_data())
        # Display the color frame
        cv2.imshow("RealSense Video Feed", color_image)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline
    pipeline.stop()

    # Close OpenCV windows
    cv2.destroyAllWindows()
