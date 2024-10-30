## To run on Viam

Follow step-by-step instructions in this tutorial: **[Use a QR code scanner](https://codelabs.viam.com/guide/qrcode/index.html?index=..%2F..index#0)**.

<img width="1412" alt="Screenshot 2024-10-30 at 11 08 13 AM" src="https://github.com/user-attachments/assets/148565a9-9a0c-41a1-b65e-ea97e1de5a75">

### QR code scanner

This module implements the [rdk vision API](https://docs.viam.com/appendix/apis/services/vision/) in a `joyce:vision:pyzbar` model.

With this model, you can manage a vision service to detect and decode QR codes.

### Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `joyce:vision:pyzbar` model from the [`pyzbar`](https://app.viam.com/module/joyce/pyzbar) module.

### Configure your service

> [!NOTE]  
> Before configuring your sensor, you must [create a machine](https://docs.viam.com/cloud/machines/#add-a-new-machine).

- Navigate to the **CONFIGURE** tab of your robot’s page in [the Viam app](https://app.viam.com/).
- Click on the **+** icon in the left-hand menu and select **Service**.
- Select the `vision` type, then select the `pyzbar` module. 
- Enter a name for your vision service and click **Create**.

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).
---

## To run locally

This project uses the Viam Python SDK to capture images from a Viam robot camera, detect QR codes in the image using Pyzbar, and display the results using OpenCV.

### Get Started

- **Install dependencies** using `pip install -r requirements.txt`.
- **Configure environment variables** using a `.env` file.
- **Run the script** using `python script.py`.

### Prerequisites

- Python 3.8 or higher installed on your system.
- A working Viam robot with a camera configured.
- Internet access to install required packages.

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

#### 2. Set Up a Python Virtual Environment

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

#### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages listed in `requirements.txt` by running:

```bash
pip install -r requirements.txt
```

The dependencies include:

- [`opencv-python`](https://pypi.org/project/opencv-python/) for computer vision tasks
- [`pyzbar`](https://pypi.org/project/pyzbar/) for QR code detection
- [`viam-sdk`](https://python.viam.dev/) for integrating with Viam robot camera

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```makefile
ROBOT_API_KEY=<your_robot_api_key>
ROBOT_API_KEY_ID=<your_robot_api_key_id>
ROBOT_ADDRESS=<your_robot_address>
```

Replace `<your_robot_api_key>`, `<your_robot_api_key_id>`, and `<your_robot_address>` with the appropriate values for your Viam robot from the [Viam app](https://app.viam.com/robots).

#### 5. Run the Script

Once the dependencies are installed and the environment variables are configured, you can run the script using:

```bash
python script.py
```

This will connect to your Viam robot camera, capture images, and detect QR codes in the live feed. Then press the `q` key to exit the live feed window.
