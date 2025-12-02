import regex as re
from langdetect import detect

URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\S+@\S+")
NON_PRINT_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
MULTI_SPACES_RE = re.compile(r"\s+")
EMOJI_RE = re.compile(r"\p{So}+", re.UNICODE)

def detect_lang_safe(text):
    try:
        return detect(text)
    except:
        return "unknown"

def clean_text(text):
    text = str(text)
    text = URL_RE.sub(" ", text)
    text = EMAIL_RE.sub(" ", text)
    text = NON_PRINT_RE.sub(" ", text)
    text = EMOJI_RE.sub(" ", text)
    text = re.sub(r"[^\p{L}\p{N}\s\.,!?;:()-]", " ", text)
    text = MULTI_SPACES_RE.sub(" ", text).strip()
    return text.lower()