import re


class TextPreprocessor:
    """
    Clean and preprocess resume text.
    """

    def clean_text(self, text):

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()