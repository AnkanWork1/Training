from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path
import uuid

from evaluation.rag_eval import context_answer_generator
from pipelines.sql_pipeline import run_sql_pipeline

app = FastAPI(title="Multimodal RAG + SQL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = BASE_DIR / "tmp_images"
TMP_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------
# TEXT RAG
# -------------------------------------------------------
@app.post("/ask")
def ask(question: str = Form(...), top_k: int = Form(10)):

    result = context_answer_generator(question, top_k)

    return {
        "type": "text",
        "question": question,
        "answer": result["answer"],
        "image": result["image_used"],
        "metrics": result["metrics"]
    }


# -------------------------------------------------------
# IMAGE RAG
# -------------------------------------------------------
@app.post("/ask-image")
def ask_image(file: UploadFile = File(...), top_k: int = Form(10)):

    suffix = Path(file.filename).suffix
    img_path = TMP_DIR / f"{uuid.uuid4().hex}{suffix}"

    with open(img_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = context_answer_generator(str(img_path), top_k)

    return {
        "type": "image",
        "image_query": file.filename,
        "answer": result["answer"],
        "image": result["image_used"],
        "metrics": result["metrics"]
    }


# -------------------------------------------------------
# SQL QA
# -------------------------------------------------------
@app.post("/ask-sql")
def ask_sql(
    db_path: str = Form(...),
    question: str = Form(...)
):

    result = run_sql_pipeline(db_path, question)

    return {
        "type": "sql",
        "question": question,
        "sql": result["sql"],
        "columns": result["columns"],
        "rows": result["rows"],
        "summary": result["summary"]
    }
