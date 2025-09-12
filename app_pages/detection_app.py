import streamlit as st
import cv2
import time
import numpy as np
import sys
from ultralytics import YOLO
from visDrone.exception import AppException


# Title of the application
st.title("VisDrone Detection Application")

# Sidebar menu for app features
menu = st.sidebar.radio("Choose a feature:", ["Image Detection", "Webcam Detection"])

# Image Detection
if menu == "Image Detection":
    model = YOLO("../model/visdrone_yolo12s.pt")
    st.header("📱 Upload an Image for Detection", divider="green")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Display uploaded image and results side by side
        col1, col2 = st.columns(2)
        
        # Read and decode the uploaded image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        with col1:
            st.image(img, caption="Uploaded Image", width="stretch", channels="BGR")
            
        # Perform object detection 
        with st.spinner("Detecting objects..."):
            results = model(img)
            annotated_image = results[0].plot()
            
        with col2:
            st.image(annotated_image, caption="Detection Results", width="stretch", channels="BGR")
            
        st.success("Detection complete!")
        
# Webcam Detection
elif menu == "Webcam Detection":
    model = YOLO("../model/visdrone_yolo12s.pt")
    st.header("🎥 Real-Time Detection from Webcam", divider="green")
    
    # Create two columns for Start and Stop Buttons
    col1, col2 = st.columns(2)
    start_button = col1.button("▶️ Start Webcam")
    stop_button = col2.button("⏹️ Stop Webcam")
    
    if start_button:
        video_placeholder = st.empty()  # Placeholder for displaying video frames
        fps_placeholder = st.empty()  # Placeholder for displaying FPS value

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Open default webcam
        cap.set(3, 1280)  # Set frame width
        cap.set(4, 720)   # Set frame height
        cap.set(cv2.CAP_PROP_FOURCC, 0x32595559) # CAP_PROP_FOURCC: 4-character code of codec
        cap.set(cv2.CAP_PROP_FPS, 30)            # CAP_PROP_FPS: Frame rate
        
        prev_frame_time = 0 # Previous frame time
        
        try:
            while cap.isOpened():
                if stop_button: # Check if Stop button is pressed
                    st.info("Webcam stopped")
                    break
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to read from webcam")
                    break
            
                # Perform detection/tracking using YOLO model
                results =model.track(source=frame, verbose=False, device="cuda", stream=True, persist=True)
                for res in results:
                    annotated_frame = res.plot() # Annotate the frame with detection results
                    
                # Calculate FPS
                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time != 0 else 0
                prev_frame_time = new_frame_time
            
                # Update the video placeholder with the annotated frame
                video_placeholder.image(annotated_frame, width="stretch", channels="BGR")
                
                # Update the FPS placeholder with the current FPS value
                fps_placeholder.markdown(f"**FPS:** {int(fps)}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            raise AppException(e, sys)
        
        finally:
            cap.release() # Release webcam resource when done
            st.info("Webcam stopped")
            
# IP Webcam Detection
elif menu == "IP Webcam Detection":
    model = YOLO("../model/visdrone_yolo12s.pt")
    st.header("🧿 Real-Time Detection from IP Webcam", divider="green")

    # Create two columns for Start and Stop Buttons
    col1, col2 = st.columns(2)
    start_button = col1.button("▶️ Start IP Webcam")
    stop_button = col2.button("⏹️ Stop IP Webcam")

    ip_url = st.text_input("Enter IP Webcam URL (e.g., http://192.168.100.4:8080/video):")

    if start_button and ip_url:
        video_placeholder = st.empty()  # Placeholder for displaying video frames
        fps_placeholder = st.empty()  # Placeholder for displaying FPS value
        
        cap = cv2.VideoCapture(ip_url, cv2.CAP_FFMPEG)  # Open IP webcam feed
        cap.set(3, 640)  # Reduce resolution to 640x480 for performance
        cap.set(4, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Increase buffer size
        cap.set(cv2.CAP_PROP_FPS, 30)  # Limit FPS
        
        prev_frame_time = 0 # Previous frame time

        try:
            while cap.isOpened():
                if stop_button:  # Check if Stop button is pressed
                    st.info("IP Webcam stopped")
                    break

                ret, frame = cap.read()
                if not ret:
                    st.warning("Failed to read from IP webcam. Skipping frame...")
                    continue  # Skip bad frames instead of breaking the loop

                # Perform detection using YOLO model
                try:
                    results = model.track(source=frame, verbose=False, device="cuda", stream=True, persist=True)
                    for res in results:
                        annotated_frame = res.plot()  # Annotate the frame with detection results
                        
                    # Calculate FPS
                    new_frame_time = time.time()
                    fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time != 0 else 0
                    prev_frame_time = new_frame_time   

                    # Update the video placeholder with the annotated frame
                    video_placeholder.image(annotated_frame, width="stretch", channels="BGR")
                    
                    # Update the FPS placeholder with the current FPS value
                    fps_placeholder.markdown(f"**FPS:** {int(fps)}")
                    
                except Exception as e:
                    st.warning(f"Error during YOLO detection: {str(e)}. Skipping this frame...")

                # Add delay for stability
                time.sleep(0.05)  # Add a 50 ms delay to reduce system load

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            raise AppException(e, sys)

        finally:
            cap.release()  # Release IP webcam resource when done
            st.info("IP Webcam stopped")

    elif start_button and not ip_url:
        st.error("Please enter a valid IP Webcam URL.")