from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import List, Optional

from PIL import Image

import pytesseract

import io


# =================================================
# OCR NORMALIZER
# =================================================

from clinical.drug_normalizer import (
    extract_medications_from_ocr
)

# =================================================
# OCR ROUTES
# =================================================

from api.routes.ocr import router as ocr_router

# =================================================
# CLINICAL AI ROUTES
# =================================================

from api.clinical_routes import router as clinical_router

# =================================================
# ENGINES
# =================================================

from clinical.counterfactual_engine import (
    CounterfactualEngine
)

from clinical.patient_profile import (
    PatientProfile
)

# =================================================
# INITIALIZE FASTAPI
# =================================================

app = FastAPI(
    title="MediWise API",
    description="AI-powered medication intelligence system",
    version="2.0"
)

# =================================================
# CORS CONFIG
# =================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================
# REGISTER ROUTERS
# =================================================

# Clinical AI Routes

app.include_router(
    clinical_router,
    prefix="/clinical",
    tags=["Clinical AI"]
)

# OCR Routes

app.include_router(
    ocr_router,
    prefix="/ocr",
    tags=["OCR"]
)

# =================================================
# INITIALIZE COUNTERFACTUAL ENGINE
# =================================================

engine = CounterfactualEngine(
    "data/raw/drug_metadata.csv",
    "data/raw/drug_interactions.csv"
)

# =================================================
# REQUEST MODELS
# =================================================

class MedicationRequest(BaseModel):

    drugs: List[str]

    age: int

    sex: Optional[str] = None

    weight: Optional[float] = None

    liver_disease: bool = False

    kidney_disease: bool = False

    pregnant: bool = False

    lactating: bool = False

    allergies: Optional[List[str]] = []

    conditions: Optional[List[str]] = []

    smoker: bool = False

    alcohol_use: bool = False

    occupation: Optional[str] = None

    creatinine: Optional[float] = None

    alt: Optional[float] = None

    ast: Optional[float] = None


class RemoveDrugRequest(BaseModel):

    drugs: List[str]

    remove_drug: str

    age: int

    sex: Optional[str] = None

    weight: Optional[float] = None

    liver_disease: bool = False

    kidney_disease: bool = False

    pregnant: bool = False

    lactating: bool = False

    allergies: Optional[List[str]] = []

    conditions: Optional[List[str]] = []

    smoker: bool = False

    alcohol_use: bool = False

    occupation: Optional[str] = None

    creatinine: Optional[float] = None

    alt: Optional[float] = None

    ast: Optional[float] = None


class ReplaceDrugRequest(BaseModel):

    drugs: List[str]

    old_drug: str

    new_drug: str

    age: int

    sex: Optional[str] = None

    weight: Optional[float] = None

    liver_disease: bool = False

    kidney_disease: bool = False

    pregnant: bool = False

    lactating: bool = False

    allergies: Optional[List[str]] = []

    conditions: Optional[List[str]] = []

    smoker: bool = False

    alcohol_use: bool = False

    occupation: Optional[str] = None

    creatinine: Optional[float] = None

    alt: Optional[float] = None

    ast: Optional[float] = None

# =================================================
# HELPER → BUILD PATIENT PROFILE
# =================================================

def build_patient(request):

    return PatientProfile(

        age=request.age,

        sex=request.sex,

        weight=request.weight,

        liver_disease=request.liver_disease,

        kidney_disease=request.kidney_disease,

        pregnant=request.pregnant,

        lactating=request.lactating,

        allergies=request.allergies,

        conditions=request.conditions,

        smoker=request.smoker,

        alcohol_use=request.alcohol_use,

        occupation=request.occupation,

        creatinine=request.creatinine,

        alt=request.alt,

        ast=request.ast
    )

# =================================================
# ROOT ENDPOINT
# =================================================

@app.get("/")
def root():

    return {
        "message": "MediWise API is running"
    }

# =================================================
# ANALYZE MEDICATION PLAN
# =================================================

@app.post("/analyze")
def analyze_medication(
    request: MedicationRequest
):

    patient = build_patient(request)

    result = engine.analyze_plan(
        request.drugs,
        patient
    )

    return result

# =================================================
# SIMULATE REMOVING A DRUG
# =================================================

@app.post("/simulate/remove-drug")
def simulate_remove_drug(
    request: RemoveDrugRequest
):

    patient = build_patient(request)

    result = engine.simulate_remove_drug(
        request.drugs,
        request.remove_drug,
        patient
    )

    return result

# =================================================
# SIMULATE REPLACING A DRUG
# =================================================

@app.post("/simulate/replace-drug")
def simulate_replace_drug(
    request: ReplaceDrugRequest
):

    patient = build_patient(request)

    result = engine.simulate_replace_drug(
        request.drugs,
        request.old_drug,
        request.new_drug,
        patient
    )

    return result

# =================================================
# OCR IMAGE EXTRACTION ENDPOINT
# =================================================

@app.post("/ocr/extract")
async def extract_prescription_ocr(

    file: UploadFile = File(...)
):

    # =============================================
    # READ FILE
    # =============================================

    contents = await file.read()

    # =============================================
    # OPEN IMAGE
    # =============================================

    image = Image.open(
        io.BytesIO(contents)
    )

    # =============================================
    # OCR TEXT EXTRACTION
    # =============================================

    raw_text = pytesseract.image_to_string(
        image
    )

    # =============================================
    # MEDICATION EXTRACTION
    # =============================================

    medications = extract_medications_from_ocr(
        raw_text
    )

    # =============================================
    # RESPONSE
    # =============================================

    return {

        "success": True,

        "raw_text": raw_text,

        "medications": medications
    }

# =================================================
# OCR EXTRACTION TEST ROUTE
# =================================================

@app.post("/ocr/test-extraction")
def test_ocr_extraction(payload: dict):

    raw_text = payload.get("raw_text", "")

    medications = extract_medications_from_ocr(
        raw_text
    )

    return {

        "success": True,

        "medications": medications
    }