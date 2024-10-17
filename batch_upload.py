import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

# Specify directory from which to upload data, and credentials
my_data_directory = "./qr_dataset"
robot_api_key = os.getenv('ROBOT_API_KEY') or ''
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''
part_id= os.getenv('PART_ID') or '' # This is the part_id of the part you want to upload data to, or random one

async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        payload=api_key,
      ),
      auth_entity=api_key_id
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client

    # Get the list of files and limit to the first 20
    file_list = os.listdir(my_data_directory)[:20]

    for file_name in file_list:
        await data_client.file_upload_from_path(
            part_id=part_id,
            tags=["qr"],
            filepath=os.path.join(my_data_directory, file_name)
        )

    viam_client.close()

if __name__ == "__main__":
    asyncio.run(main())