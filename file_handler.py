import pytesseract
from PIL import Image
import pdfplumber

def extract_text_from_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text(path):
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.lower().endswith((".png",".jpg","jpeg")):
        return extract_text_from_image(path)
    return ""