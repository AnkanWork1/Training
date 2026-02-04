import re


def clean_text(text: str):

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text
