import os.path
import sys
import yaml
import base64
import cv2
import cvzone
import math
import time

from visDrone.exception import AppException
from visDrone.logger import logging

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.

    :param file_path: Path to the YAML file.
    :return: Content of the YAML file as a dictionary.
    :raises AppException: If reading the file fails.
    """
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("Read yaml file successfully")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise AppException(e, sys) from e
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file. Optionally replaces the file if it already exists.

    :param file_path: Path to the YAML file.
    :param content: Content to write into the YAML file.
    :param replace: Whether to replace the file if it already exists.
    :raises AppException: If writing the file fails.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info("Successfully write_yaml_file")

    except Exception as e:
        raise AppException(e, sys)
    

def decodeImage(imgstring, fileName):
    """
    Decodes a base64-encoded image string and writes it to a file.

    :param imgstring: Base64-encoded image string.
    :param fileName: Name of the file to save the decoded image.
    """
    imgdata = base64.b64decode(imgstring)
    with open("./data/" + fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    """
    Encodes an image into a base64 string.

    :param croppedImagePath: Path to the image file to be encoded.
    :return: Base64-encoded string of the image.
    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
    

def gen_frames(model, classNames, videoSource):
    """
    Generates frames from a video source, performs object detection, and annotates the frames.

    :param model: The object detection model.
    :param classNames: List of class names for object detection.
    :param videoSource: Video source (integer for webcam or string for IP camera).
    :yield: Annotated video frames in JPEG format for streaming.
    """
    # Initialize video capture with the specified source
    cap = cv2.VideoCapture(videoSource, cv2.CAP_DSHOW if isinstance(videoSource, int) else cv2.CAP_FFMPEG) # CAP_DSHOW: To specify video source, 0: Default camera; 1 and later: External camera
    cap.set(3, 1280) # Set video width
    cap.set(4, 720) # Set video height
    cap.set(cv2.CAP_PROP_FOURCC, 0x32595559) # CAP_PROP_FOURCC: 4-character code of codec
    cap.set(cv2.CAP_PROP_FPS, 30)            # CAP_PROP_FPS: Frame rate
    
    prev_frame_time = 0
    new_frame_time = 0
    
    while True:
        success, img = cap.read() # Read a frame from the video feed
        if not success:
            break
        
        # Perform object detection
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Extract bounding box coordinates and class information
                x1, y1, x2, y2 = int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(box.xyxy[0][3])
                cls = int(box.cls[0])
                conf = math.ceil((box.conf[0] * 100)) / 100
                currentClass = classNames[cls]

                # Draw bounding box and label
                cvzone.putTextRect(img, f'{currentClass} {conf}', 
                                   (max(0, x1) + 5, max(35, y1) - 7), scale=1, thickness=1, 
                                   colorT=(255, 255, 255), colorR=(48, 25, 52), offset=5)
                cv2.rectangle(img, (x1, y1), (x2, y2), (48, 25, 52), 2)

        # Calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cv2.putText(img, f"FPS: {int(fps)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode the frame as JPEG
        (flag, encodedImage) = cv2.imencode('.jpg', img)
        if not flag:
            continue
        # Yield the frame for the streaming response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')