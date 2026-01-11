from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from app.db import get_cursor, connection
from app.logger import logger
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

def ingest_pdf(path: str):
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return

    try:
        reader = PdfReader(path)
        cur = get_cursor()
        logger.info(f"Starting ingestion for PDF: {path}")

        for page_no, page in enumerate(reader.pages):
            text = page.extract_text()
            
            if not text:
                logger.warning(f"No text found on page {page_no} of {path}. Skipping.")
                continue

            chunks = chunk_text(text)

            for chunk in chunks:
                embedding = model.encode(chunk).tolist()
                cur.execute(
                    "INSERT INTO documents (content, embedding, source, page) VALUES (%s, %s, %s, %s)",
                    (chunk, embedding, path, page_no)
                )
    
        connection.commit()
        logger.info(f"PDF {path} ingested successfully.")
    except Exception as e:
        logger.error(f"Ingestion failed for {path}: {e}")

if __name__ == "__main__":
    pdf_path = "/home/ottokevin/Desktop/RAG Technique/datasets/resume.pdf"
    ingest_pdf(pdf_path)
