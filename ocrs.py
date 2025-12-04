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
            pages = convert_from_bytes(content)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid PDF file")

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
        return {"filename": file.filename, "text": text.strip('\n')}

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload PDF or image.")
