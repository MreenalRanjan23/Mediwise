from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from clinical.clinical_pipeline import analyze_case


# =================================================
# ROUTER
# =================================================

router = APIRouter()


# =================================================
# REQUEST SCHEMA
# =================================================

class ClinicalRequest(BaseModel):

    drugs: List[str]

    age: int = 30

    sex: Optional[str] = "M"

    liver_disease: bool = False
    kidney_disease: bool = False

    smoker: bool = False
    alcohol_use: bool = False

    conditions: List[str] = []

    creatinine: float = 1.0

    alt: float = 30.0
    ast: float = 30.0


# =================================================
# MAIN CLINICAL ANALYSIS ENDPOINT
# =================================================

@router.post("/analyze")

def analyze_medication_plan(payload: ClinicalRequest):

    result = analyze_case(payload.dict())

    return {

        "success": True,

        "results": result
    }