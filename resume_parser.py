import pdfplumber
import re
from synonyms import SYNONYM_MAP

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text.strip()

def clean_text(text):
    text = text.lower()
    # Keep alphabets, digits, spaces, parentheses, hyphens
    text = re.sub(r'[^a-z0-9\s\(\)\-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_synonyms(text):
    return " ".join(SYNONYM_MAP.get(w, w) for w in text.split())

def apply_skill_weighting(text, skills, weight=3):
    words = []
    for w in text.split():
        words.append(w)
        if w in skills:
            words.extend([w] * (weight - 1))
    return " ".join(words)

def extract_years_of_experience(text):
    matches = re.findall(r'(\d+)\s*(years|year|yrs|yr)', text)
    return max([int(m[0]) for m in matches], default=0)
