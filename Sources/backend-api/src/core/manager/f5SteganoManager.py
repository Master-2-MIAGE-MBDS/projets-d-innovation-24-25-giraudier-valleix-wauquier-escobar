from ..utils import steganography_f5 as f5
import io
from PIL import Image
import json
import re


def sign_image(image_data: bytes, user_id: str):
    f5Util = f5.SteganographyF5()

    image_stream = io.BytesIO(image_data)
    image = Image.open(image_stream).convert("RGB")

    encoded_image = f5Util.encode(image, user_id)

    return encoded_image



def verify_image(image_data: bytes):
    try:
        f5Util = f5.SteganographyF5()

        image_stream = io.BytesIO(image_data)
        image = Image.open(image_stream).convert("RGB")

        str_data = f5Util.decode(image)

    except:
        return None

    return str_data