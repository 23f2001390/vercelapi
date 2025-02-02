import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Load marks data from marks.json at module load time.
# (Since the file is bundled with your deployment, this is allowed.)
with open("marks.json", "r") as f:
    marks_data = json.load(f)

app = FastAPI()

# Enable CORS to allow GET requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],          # Only GET is needed
    allow_headers=["*"],
)

@app.get("/api")
def get_marks(name: List[str] = Query(...)):
    """
    Accepts one or more 'name' query parameters.
    Returns the marks for those student names in the same order.
    If a name is not found in the marks data, it returns null for that name.
    
    Examples:
    - /api?name=Alice
    - /api?name=Alice&name=Bob
    """
    # Look up the mark for each requested name.
    result = [marks_data.get(n, None) for n in name]
    return {"marks": result}
