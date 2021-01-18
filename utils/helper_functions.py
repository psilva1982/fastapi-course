from utils.constants import API_IMGBB_URL
import requests

async def upload_image_to_server(file):
    result = requests.post(API_IMGBB_URL, files={"image": file})
    print(result.json())