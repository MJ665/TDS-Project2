



from fastapi import FastAPI, Form, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
import re
import subprocess
import os

import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint for solving assignment
@app.post("/api/")
async def solve_assignment(question: str = Form(...)):
    try:
        result = route_to_function(question)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Determine which function to run based on the question
def route_to_function(question):
    if "code -s" in question.lower():
        return extract_vs_code_version()
    elif "httpie" in question.lower() and "https://httpbin.org/get" in question.lower():
        return send_httpie_request()
    else:
        return "Unsupported question. Please provide a valid input."


# Extract VS Code version using subprocess
def extract_vs_code_version():
    # try:
    #     result = subprocess.run(["code", "-s"], capture_output=True, text=True)
    #     if result.returncode == 0:
    #         return result.stdout.strip()
    #     else:
    #         return result.stderr.strip() or "Error retrieving VS Code version."
    # except Exception as e:
    #     return str(e)
# Extract VS Code version by reading from GA1codeS.txt

    try:
        file_path = './GA1/GA1codeS.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            return "Error: GA1codeS.txt not found."
    except Exception as e:
        return str(e)



# Send HTTPS request using requests library instead of httpie
def send_httpie_request():
    try:
        response = requests.get("https://httpbin.org/get", params={"email": "22f3001551@ds.study.iitm.ac.in"})
        return response.json()
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
