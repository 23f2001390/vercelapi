import os
import json
from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Use a relative path to load marks.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
marks_path = os.path.join(BASE_DIR, "marks.json")

try:
    with open(marks_path, "r") as f:
        marks_list = json.load(f)
    # Convert list to name->marks mapping
    marks_data = {item["name"]: item["marks"] for item in marks_list}
except Exception as e:
    # Log the error (in production you might use a logger)
    print("Error loading marks.json:", e)
    marks_data = {}

app = FastAPI()

# Enable CORS so GET requests from any origin are allowed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api")
def get_marks(name: List[str] = Query(...)):
    """
    Returns the marks for the provided names (in the same order as given).
    If a name is not found, its mark will be returned as null.
    """
    result = [marks_data.get(n, None) for n in name]
    return {"marks": result}
