import cv2
from pyzbar.pyzbar import decode
from PIL import Image

# Load the image using OpenCV
image_path = './qr_dataset/1002-v1.png'
image = cv2.imread(image_path)

# Decode the QR codes
qr_codes = decode(image)

# Loop through the detected QR codes
for qr_code in qr_codes:
    # Get the bounding box and data of the QR code
    (x, y, w, h) = qr_code.rect
    qr_data = qr_code.data.decode("utf-8")
    qr_type = qr_code.type
    
    # Print the QR code data and type
    print(f"QR Code Data: {qr_data}")
    print(f"QR Code Type: {qr_type}")
    
    # Draw a bounding box around the QR code (optional)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the image with bounding boxes (optional)
cv2.imshow("QR Code Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
