# QR Code Detection with Viam Camera

This project uses the Viam Python SDK to capture images from a Viam robot camera, detect QR codes in the image using Pyzbar, and display the results using OpenCV.

## Get Started

- **Install dependencies** using `pip install -r requirements.txt`.
- **Configure environment variables** using a `.env` file.
- **Run the script** using `python script.py`.

### Prerequisites

- Python 3.8 or higher installed on your system.
- A working Viam robot with a camera configured.
- Internet access to install required packages.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Python Virtual Environment

Use a virtual environment to manage dependencies. You can create and activate one as follows:

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages listed in `requirements.txt` by running:

```bash
pip install -r requirements.txt
```

The dependencies include:

- [`opencv-python`](https://pypi.org/project/opencv-python/) for computer vision tasks
- [`pyzbar`](https://pypi.org/project/pyzbar/) for QR code detection
- [`viam-sdk`](https://python.viam.dev/) for integrating with Viam robot camera

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```makefile
ROBOT_API_KEY=<your_robot_api_key>
ROBOT_API_KEY_ID=<your_robot_api_key_id>
ROBOT_ADDRESS=<your_robot_address>
```

Replace `<your_robot_api_key>`, `<your_robot_api_key_id>`, and `<your_robot_address>` with the appropriate values for your Viam robot.

### 5. Run the Script

Once the dependencies are installed and the environment variables are configured, you can run the script using:

```bash
python script.py
```

This will connect to your Viam robot camera, capture images, and detect QR codes in the live feed. Then press the `q` key to exit the live feed window.
