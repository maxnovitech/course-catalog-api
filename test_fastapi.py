from __future__ import annotations
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def test(is_elective: bool | None = None):
    return {}
