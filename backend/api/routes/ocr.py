from fastapi import APIRouter, UploadFile, File
import shutil
import os

from ocr.ocr_engine import OCREngine
from ocr.prescription_parser import PrescriptionParser
from ocr.lab_parser import LabParser

router = APIRouter()

ocr_engine = OCREngine()
parser = PrescriptionParser()
lab_parser = LabParser()


@router.post("/extract")

async def extract_prescription(
    file: UploadFile = File(...)
):

    upload_path = f"temp/{file.filename}"

    os.makedirs("temp", exist_ok=True)

    with open(upload_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    if file.filename.endswith(".pdf"):

        text = ocr_engine.extract_from_pdf(
            upload_path
        )

    else:

        text = ocr_engine.extract_from_image(
            upload_path
        )

    medications = parser.extract_medications(
        text
    )

    labs = lab_parser.extract_lab_values(
        text
    )

    return {

        "success": True,

        "raw_text": text,

        "medications": medications,

        "lab_values": labs
    }