from fastapi import FastAPI, UploadFile, File, HTTPException
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/")
async def extract_text(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        try:
            pages = convert_from_bytes(content,poppler_path=r'C:\Program Files\poppler-25.11.0\Library\bin')
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page) + "\n"

        return {"filename": file.filename, "text": text}

    elif filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        try:
            image = Image.open(io.BytesIO(content))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")

        text = pytesseract.image_to_string(image)
        text = text.replace("\n","")
        return {"filename": file.filename, "text": text.strip()}

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload PDF or image.")
