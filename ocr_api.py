from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import uvicorn
import shutil
import os

app = FastAPI()

# ✅ Correct and only initialization — CPU only
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ocr.ocr(file_location, cls=True)

    formatted = []
    for line in result[0]:
        text = line[1][0]
        score = line[1][1]
        box = line[0]
        formatted.append({
            "text": text,
            "confidence": score,
            "bounding_box": box
        })

    os.remove(file_location)
    return JSONResponse(content={"results": formatted})
