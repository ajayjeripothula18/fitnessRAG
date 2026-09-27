import re
from typing import List
from app.core.config import settings

# Medical keywords that should trigger a disclaimer
MEDICAL_KEYWORDS = [
    # Symptoms
    "chest pain",
    "shortness of breath",
    "difficulty breathing",
    "heart attack",
    "stroke",
    "cancer",
    "tumor",
    "diabetes",
    "hypertension",
    "high blood pressure",
    "seizure",
    "epilepsy",
    "asthma attack",
    "allergic reaction",
    "anaphylaxis",
    "suicide",
    "self-harm",
    "depression",
    "anxiety",
    "panic attack",
    # Medical conditions
    "disease",
    "illness",
    "infection",
    "virus",
    "bacteria",
    "antibiotics",
    "prescription",
    "medication",
    "drug",
    "dosage",
    "side effects",
    # Body parts in medical context
    "heart",
    "lung",
    "brain",
    "liver",
    "kidney",
    "spine",
    "spinal cord",
]

# Dangerous/harmful content that should be blocked
DANGEROUS_KEYWORDS = [
    # Self-harm
    "suicide",
    "self-harm",
    "cutting",
    " overdose",
    "hanging",
    # Extreme diets
    "tapeworm",
    "bleach",
    "drinking alcohol to lose weight",
    # Harmful exercises
    "cliff jumping",
    "base jumping without training",
    # Dangerous supplements
    "dnp",
    "2,4-dinitrophenol",
    "ephedra",
    "yohimbine in high doses",
]


def check_medical_content(text: str) -> bool:
    """
    Check if text contains medical keywords that require disclaimer.
    Returns True if medical content detected.
    """
    text_lower = text.lower()
    for keyword in MEDICAL_KEYWORDS:
        if keyword in text_lower:
            return True
    return False


def check_dangerous_content(text: str) -> bool:
    """
    Check if text contains dangerous content that should be blocked.
    Returns True if dangerous content detected.
    """
    text_lower = text.lower()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in text_lower:
            return True
    # Additional pattern matching for harmful instructions
    harmful_patterns = [
        r"how to (?:make|create|build) (?:a bomb|explosive|weapon)",
        r"instructions? for (?:self-harm|suicide)",
        r"ways? to (?:hurt|harm|kill) yourself",
    ]
    for pattern in harmful_patterns:
        if re.search(pattern, text_lower):
            return True
    return False


def get_medical_disclaimer() -> str:
    """
    Return a medical disclaimer for safe completion.
    """
    return (
        "I'm not a licensed healthcare professional. For medical advice, diagnoses, "
        "or treatment, please consult with a qualified healthcare provider. "
        "If you're experiencing a medical emergency, call emergency services immediately."
    )


def get_dangerous_content_response() -> str:
    """
    Return a response for dangerous content.
    """
    return (
        "I cannot provide guidance on harmful or dangerous activities. "
        "If you're having thoughts of self-harm, please reach out to a mental health professional "
        "or contact a crisis helpline immediately. Your safety is important."
    )
