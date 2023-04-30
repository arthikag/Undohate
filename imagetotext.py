from PIL import Image
import pytesseract
import os

UPLOAD_FOLDER_IMAGE = "UserImage"

pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"

def  get_image_transcription(path):

    text = pytesseract.image_to_string(Image.open(os.path.join(UPLOAD_FOLDER_IMAGE, path)), lang="eng")

    return text[:-2]

if __name__ == "__main__":
    path = "test3.png"
    print("\nFull text:", get_image_transcription(path))