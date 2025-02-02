from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from typing import List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the JSON data
json_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python (2).json')
with open(json_path, 'r') as f:
    students_data = json.load(f)

# Create a dictionary for faster lookups
marks_dict = {student['name']: student['marks'] for student in students_data}

@app.get("/api")
async def get_marks(name: List[str] = Query(..., description="Student names")):
    marks = [marks_dict.get(n, None) for n in name]
    if all(mark is None for mark in marks):
        raise HTTPException(status_code=404, detail="No valid names found")
    return {"marks": marks} 