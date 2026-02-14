"""DevKB API - REST API Wrapper"""
import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DevKB API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.getenv("DATABASE_PATH", "./data/snippets.db")


def get_db():
    """Get database connection"""
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class SnippetCreate(BaseModel):
    code: str
    title: str = None
    language: str = None
    tags: str = None


@app.get("/")
def root():
    return {"message": "DevKB API", "version": "1.0.0"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/snippets")
def list_snippets():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snippets ORDER BY created_at DESC")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


@app.post("/api/snippets")
def create_snippet(snippet: SnippetCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO snippets (code, title, language, tags) VALUES (?, ?, ?, ?)",
        (snippet.code, snippet.title, snippet.language, snippet.tags)
    )
    conn.commit()
    snippet_id = cursor.lastrowid
    conn.close()
    return {"id": snippet_id, "message": "Snippet created"}


@app.get("/api/snippets/{snippet_id}")
def get_snippet(snippet_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snippets WHERE id = ?", (snippet_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return dict(row)


@app.delete("/api/snippets/{snippet_id}")
def delete_snippet(snippet_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    conn.close()
    return {"message": "Snippet deleted"}


@app.get("/api/search")
def search_snippets(q: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM snippets WHERE code LIKE ? OR title LIKE ? OR tags LIKE ?",
        (f"%{q}%", f"%{q}%", f"%{q}%")
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
