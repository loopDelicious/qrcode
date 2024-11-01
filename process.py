import asyncio
import os
from dotenv import load_dotenv
from viam.logging import getLogger
from viam.robot.client import RobotClient
from viam.services.vision import Vision
import subprocess
import urllib.parse

load_dotenv()
LOGGER = getLogger(__name__)

robot_api_key = os.getenv('ROBOT_API_KEY') or ''
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''
camera_name = os.getenv("CAMERA_NAME", "")
vision_name = os.getenv("VISION_NAME", "")

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key=robot_api_key,
        api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)

async def main():
    machine = await connect()

    vision = Vision.from_robot(machine, vision_name)

    while True:
        try:
            # Detect QR codes from the camera
            detections = await vision.get_detections_from_camera(camera_name)
            
            # Check if QR codes found
            if not detections:
                LOGGER.info("No QR code detected yet.")
                await asyncio.sleep(1)  # Wait and retry
                continue

            # Process each detection as found
            for detection in detections:
                qr_data = detection.class_name
                LOGGER.info(f"QR Code detected: {qr_data}")

            # Validate QR data format as a URL
            parsed_url = urllib.parse.urlparse(qr_data)
            if not parsed_url.scheme:
                qr_data = "http://" + qr_data
                parsed_url = urllib.parse.urlparse(qr_data)
            LOGGER.info(f"Parsed URL: {qr_data}")

            # Ensure the URL is well-formed and open it
            if parsed_url.scheme in ("http", "https") and parsed_url.netloc:
                LOGGER.info(f"Valid URL detected: {qr_data}")
                try:
                    subprocess.Popen(["xdg-open", qr_data])  # Linux
                except FileNotFoundError:
                    try:
                        subprocess.Popen(["open", qr_data])  # macOS
                    except FileNotFoundError:
                        subprocess.Popen(["start", qr_data], shell=True)  # Windows
                    except Exception as e:
                        LOGGER.warning(f"Cannot open browser: {e}")
                break  # Quit after successfully opening the URL
            else:
                LOGGER.warning(f"Invalid URL format: {qr_data}")
        except Exception as e:
            LOGGER.warning(f"Error during image capture or QR code processing: {e}")

        await asyncio.sleep(1)
        
if __name__ == '__main__':
    asyncio.run(main())