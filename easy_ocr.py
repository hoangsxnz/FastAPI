import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

async def plot_img(IMAGE_PATH: str):
    img = cv2.imread(IMAGE_PATH)
    # init easy ocr reader
    reader = easyocr.Reader(['en', 'vi'])
    # read image into a list, containing 4 coordinates [x,y], text and model confident level
    text = reader.readtext(img)

    for line in text:
        top_left = tuple([int(val) for val in line[0][0]])
        top_right = tuple([int(val) for val in line[0][1]])
        bottom_left = tuple([int(val) for val in line[0][3]])
        bottom_right = tuple([int(val) for val in line[0][2]])
        text = line[1]
        font = cv2.FONT_ITALIC
        img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 1)
        img = cv2.putText(img, text, bottom_left, font, 0.3, (255,0,0), 1, cv2.LINE_AA)

    plt.figure(figsize=(10,10))
    plt.imshow(img)
    plt.show()

async def extract_text(img: np.ndarray):
    reader = easyocr.Reader(['en', 'vi'])
    # read image into a list containing text only
    text = reader.readtext(img, detail=0, paragraph=True)
    string = ' '.join([str(item) for item in text])
    return string
    