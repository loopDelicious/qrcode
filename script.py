import asyncio
import os
from dotenv import load_dotenv
from viam.logging import getLogger
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.camera import Camera
from viam.services.mlmodel import MLModelClient
from viam.services.vision import VisionClient
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import webbrowser
import subprocess

load_dotenv()
LOGGER = getLogger(__name__)

robot_api_key = os.getenv('ROBOT_API_KEY') or ''
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key=robot_api_key,
        api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)

async def get_camera_frame(camera):
    # Capture an image from the Viam camera
    image = await camera.get_image()
    
    # Convert the image to OpenCV format
    image_bytes = image.data
    np_img = np.frombuffer(image_bytes, np.uint8)
    cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    return cv_img

# async def get_camera_image():
#     # Connect to your Viam robot
#     machine = await connect()
    
#     # Access the camera by name
#     camera_1 = Camera.from_robot(machine, "camera-1")

#     # Get the image from the camera
#     camera_1_return_value = await camera_1.get_image()

#     # Convert the image to a format usable by OpenCV
#     image_bytes = camera_1_return_value.data
#     np_img = np.frombuffer(image_bytes, np.uint8)
#     cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

#     # Save or process the image as needed
#     cv2.imwrite("image.jpg", cv_img)
    
#     # Don't forget to close the machine when you're done!
#     await machine.close()
#     print("Image saved as image.jpg")
#     return cv_img

def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    threshold_image = cv2.threshold(equalized_image, 128, 255, cv2.THRESH_BINARY)[1]
    resized_image = cv2.resize(threshold_image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    return resized_image

def trigger_action_on_qr_code(qr_data, image):
    print(f"Triggering action based on QR Code: {qr_data}")
    # Check if the image is properly captured
    if image is None:
        print("Error: Image is None, cannot display")
        return
    
    # Stop the feed and open a window to show the QR code
    cv2.imshow("Detected QR Code", image)
    cv2.waitKey(1)  # Wait for a brief moment before continuing
    
    # Ensure the QR data contains a URL scheme and open it
    if not qr_data.startswith("http"):
        qr_data = "http://" + qr_data

    print(f"Opening URL: {qr_data}")
    # webbrowser.open(qr_data)
    try:
        subprocess.Popen(["xdg-open", qr_data])  # Linux
    except FileNotFoundError:
        try:
            subprocess.Popen(["open", qr_data])  # macOS
        except FileNotFoundError:
            subprocess.Popen(["start", qr_data], shell=True)  # Windows
    
    cv2.destroyAllWindows()
    exit()

def detect_qr_code(image):
    # Get the original dimensions before preprocessing
    original_height, original_width = image.shape[:2]

    processed_image = preprocess_image(image)
    processed_height, processed_width = processed_image.shape[:2]

    qr_codes = decode(processed_image)
    
    for qr_code in qr_codes:
        qr_data = qr_code.data.decode('utf-8')
        print(f"QR Code detected: {qr_data}")
        
        # Draw a rectangle around the QR code
        (x, y, w, h) = qr_code.rect
        # Scale bounding box to original image size
        scale_x = original_width / processed_width
        scale_y = original_height / processed_height
        x = int(x * scale_x)
        y = int(y * scale_y)
        w = int(w * scale_x)
        h = int(h * scale_y)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        trigger_action_on_qr_code(qr_data, image)
    
    if not qr_codes:
        print("No QR Code detected")

async def detect_qr_codes_from_feed():

    cap = cv2.VideoCapture(0) # Use the default camera (index 0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        detect_qr_code(frame)  # Detect QR codes in each frame

        # Display the frame
        cv2.imshow("Frame", frame)

        # Exit condition: press 'q' to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

async def detect_qr_codes_from_viam_camera():
    # Connect to your Viam robot
    robot = await connect()
    
    # Access the Viam camera
    camera = Camera.from_robot(robot, "camera-1")  # Replace with your actual camera name

    while True:
        # Capture the image from the Viam camera
        frame = await get_camera_frame(camera)

        if frame is None:
            print("Failed to grab frame from Viam camera")
            break

        detect_qr_code(frame)  # Detect QR codes in each frame

        # Display the frame
        cv2.imshow("Frame", frame)

        # Exit condition: press 'q' to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Close the robot connection
    await robot.close()
    cv2.destroyAllWindows()

# Test with a sample image
async def test_with_sample_image():
    # Load a known QR code image file for testing
    # sample_image = cv2.imread('./image.jpg') # Use the image captured from the camera
    # sample_image = cv2.imread('./qr_dataset/1002-v1.png') # Use a sample image from the dataset
    sample_image = cv2.imread('./pxl.jpg') # Use the image captured from the camera

    if sample_image is None:
        print("Failed to load sample image.")
        return
    
    detect_qr_code(sample_image)

# Call the function
# img = asyncio.run(get_camera_image())
# test_with_sample_image()
# asyncio.run(detect_qr_codes_from_feed())
asyncio.run(detect_qr_codes_from_viam_camera())
