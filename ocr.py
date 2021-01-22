import cv2
import sys
import requests

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40


def resize_image(image_path:str):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None

def kakao_ocr_request(image_path:str,api_key:str):
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(api_key)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})

def ocr(image_path):
    api_key = "416f6ae5debd19567f3d8df0d9b93c89" # api key
    resize_image_path = resize_image(image_path)
    if resize_image_path is not None:
        image_path = resize_image_path
        print("iamge resizing")
    result = kakao_ocr_request(image_path,api_key=api_key).json() # type : dict
    data = ""
    for r in result['result']:
        for text in r['recognition_words']:
            data += text+" "

    return data