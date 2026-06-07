import re

from rapidfuzz import process


# =====================================================
# BRAND → GENERIC MAPPING
# =====================================================

BRAND_MAPPING = {

    "crocin": "paracetamol",
    "dolo": "paracetamol",
    "pcm": "paracetamol",

    "brufen": "ibuprofen",

    "rosuvas": "rosuvastatin",
    "rosuva": "rosuvastatin",

    "thyroxine": "thyroxine",
    "thyrox": "thyroxine",
    "thyronorm": "thyroxine",

    "minipress": "prazosin",

    "cilacar": "cilnidipine",

    "eliquis": "apixaban",

    "cordarone": "amiodarone",

    "dytor": "torsemide"
}


# =====================================================
# MASTER DRUG LIST
# =====================================================

KNOWN_DRUGS = [

    "paracetamol",
    "ibuprofen",
    "rosuvastatin",
    "thyroxine",
    "prazosin",
    "cilnidipine",
    "apixaban",
    "amiodarone",
    "torsemide"
]


# =====================================================
# CLEAN OCR TEXT
# =====================================================

def clean_text(text: str):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s\.\-\(\)]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# =====================================================
# EXTRACT DOSAGE
# =====================================================

def extract_dose_near_word(
    text,
    index
):

    window = text[index:index + 40]

    match = re.search(
        r"(\d+(\.\d+)?)\s*mg",
        window
    )

    if match:
        return match.group(0)

    return "Unknown"


# =====================================================
# NORMALIZE DRUG NAME
# =====================================================

def normalize_drug_name(word: str):

    word = word.lower().strip()

    word = word.replace("tab", "")
    word = word.replace(".", "")
    word = word.strip()

    # =========================================
    # DIRECT BRAND MATCH
    # =========================================

    if word in BRAND_MAPPING:
        return BRAND_MAPPING[word]

    # =========================================
    # FUZZY BRAND MATCH
    # =========================================

    brand_match = process.extractOne(
        word,
        list(BRAND_MAPPING.keys()),
        score_cutoff=75
    )

    if brand_match:
        brand = brand_match[0]
        return BRAND_MAPPING[brand]

    # =========================================
    # FUZZY GENERIC MATCH
    # =========================================

    generic_match = process.extractOne(
        word,
        KNOWN_DRUGS,
        score_cutoff=80
    )

    if generic_match:
        return generic_match[0]

    return None


# =====================================================
# MAIN OCR MEDICATION EXTRACTION
# =====================================================

def extract_medications_from_ocr(raw_text: str):

    cleaned_text = clean_text(raw_text)

    words = cleaned_text.split()

    medications = []

    found = set()

    for i, word in enumerate(words):

        normalized = normalize_drug_name(word)

        if normalized:

            if normalized not in found:

                found.add(normalized)

                original_index = cleaned_text.find(word)

                dose = extract_dose_near_word(
                    cleaned_text,
                    original_index
                )

                medications.append({

                    "name": normalized,
                    "dose": dose
                })

    return medications