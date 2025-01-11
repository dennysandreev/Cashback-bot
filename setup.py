# setup.py
import spacy

def download_model():
    spacy.cli.download("ru_core_news_sm")

if __name__ == "__main__":
    download_model()
