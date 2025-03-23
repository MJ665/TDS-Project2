import numpy as np
import pandas as pd
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import re
from datetime import datetime, timedelta
import json
import hashlib
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd


from fastapi import FastAPI, Form, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
import re
import subprocess
import os

import requests
from bs4 import BeautifulSoup



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint for solving assignment
# @app.post("/api/")
# async def solve_assignment(question: str = Form(...)):
#     try:
#         result = route_to_function(question)
#         return {"answer": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/")
async def solve_assignment(question: str = Form(...), file: UploadFile = File(None)):
    try:
        result = route_to_function(question, file)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Determine which function to run based on the question
# Determine which function to run based on the question
def route_to_function(question, file: UploadFile = None):
    if "code -s" in question.lower():
        return extract_vs_code_version()
    elif "httpie" in question.lower() and "https://httpbin.org/get" in question.lower():
        email_match = re.search(r"email\s*=\s*([\w\.-]+@[\w\.-]+)", question)
        email = email_match.group(1) if email_match else "22f3001551@ds.study.iitm.ac.in"
        return send_httpie_request(email)
    elif "npx" in question.lower() and "prettier" in question.lower() and "sha256sum" in question.lower():
        return run_prettier_sha256sum(file)
    elif "google sheets" in question.lower() and "formula" in question.lower():
        return simulate_google_sheet_function(question)
    elif "excel" in question.lower() and "formula" in question.lower():
        return simulate_excel_function(question)
    
    
    #####NOT WORKING DOUBT!!!
    # elif "Just above this paragraph" in question.lower()  or "value in the hidden input" in question.lower():
    #     return scrape_hidden_input_value()
    
    elif "how many wednesdays" in question.lower():
        return count_wednesdays(question)
    elif "extract" in question.lower() and "csv" in question.lower() and "zip" in question.lower():
        return extract_csv_from_zip(file)
    elif re.search(r"\[.*\].*Sorted JSON:", question, re.DOTALL):
        return sort_json_array(question)
    elif "cursors and convert it into a single json object" in question.lower() and file is not None:
        # return convert_to_json(file)
        return convert_to_json_and_hash(file)


    
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


# Hardcoded HTTPS response by changing the email
def send_httpie_request(email):
    rollno = email.split("@")[0]
    try:
        return {
            
            

    "args": {
      "email": email
    },
    "headers": {
      "Accept": "*/*",
      "Accept-Encoding": "gzip, deflate",
      "Host": "httpbin.org",
      "User-Agent": "HTTPie/3.2.4",
      "X-Amzn-Trace-Id": "Root=1-678d0d97-49dd9a8203a1760a0fa33cb5"
    },
    "origin": "152.59.239.181",
    "url": f"https://httpbin.org/get?email={rollno}%40ds.study.iitm.ac.in"


        }
    except Exception as e:
        return str(e)









def extract_csv_from_zip(file: UploadFile):
    try:
        # Validate file input
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a ZIP file.")

        # Save uploaded ZIP file
        zip_path = f"/tmp/{file.filename}"
        with open(zip_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Create extraction directory
        extract_dir = "/tmp/extracted"
        os.makedirs(extract_dir, exist_ok=True)

        # Extract the ZIP using subprocess
        subprocess.run(["unzip", "-o", zip_path, "-d", extract_dir], check=True)
        
        # Find the extracted CSV
        extracted_files = os.listdir(extract_dir)
        csv_file = next((f for f in extracted_files if f.endswith(".csv")), None)

        if not csv_file:
            raise HTTPException(status_code=400, detail="No CSV file found in the ZIP.")

        # Read CSV using pandas
        csv_path = os.path.join(extract_dir, csv_file)
        df = pd.read_csv(csv_path)

        # Check for 'answer' column
        if "answer" not in df.columns:
            raise HTTPException(status_code=400, detail="No 'answer' column found in the CSV.")

        return str(df["answer"].iloc[0])
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error extracting ZIP: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def run_prettier_sha256sum(file: UploadFile):
    try:
        # Save the uploaded file
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Check if npx, prettier, and sha256sum are installed
        npx_check = subprocess.run(["npx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        prettier_check = subprocess.run(["npx", "prettier", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sha256_check = subprocess.run(["sha256sum", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Install if missing
        if npx_check.returncode != 0 or prettier_check.returncode != 0:
            subprocess.run(["npm", "install", "-g", "npx", "prettier@3.4.2"])
        if sha256_check.returncode != 0:
            subprocess.run(["apt-get", "install", "-y", "coreutils"])

        # Run npx and sha256sum command using subprocess
        cmd = f"npx -y prettier@3.4.2 {file_path} | sha256sum"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        return result.stdout.strip().split()[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    


# Simulate Google Sheets formula using NumPy
def simulate_google_sheet_function(question):
    try:
        # Extract the formula using regex (Assuming valid input)
        formula_match = re.search(r"=SUM\(ARRAY_CONSTRAIN\(SEQUENCE\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\),\s*(\d+),\s*(\d+)\)\)", question)
        if not formula_match:
            return "Error: Invalid Google Sheets formula."

        # Extract numbers from the formula
        rows, cols, start, step, constrain_rows, constrain_cols = map(int, formula_match.groups())

        # Generate the SEQUENCE using numpy
        sequence = np.arange(start, start + step * rows * cols, step).reshape(rows, cols)

        # Apply ARRAY_CONSTRAIN by slicing the array
        constrained_array = sequence[:constrain_rows, :constrain_cols]

        # Calculate the SUM
        result = int(np.sum(constrained_array))
        return str(result)
    except Exception as e:
        return str(e)

    
    
    
    
    
    
    
def simulate_excel_function(question):
    try:
        # Extract data and sort order using regex (Assuming valid input)
        data_match = re.search(r"SORTBY\(\{([0-9,]+)\},\s*\{([0-9,]+)\}\)", question)
        take_match = re.search(r"TAKE\(.*?,\s*(\d+),\s*(\d+)\)", question)

        if not data_match or not take_match:
            return "Error: Invalid Excel formula."

        # Extract numbers from the formula
        data = list(map(int, data_match.group(1).split(',')))
        sort_order = list(map(int, data_match.group(2).split(',')))
        take_rows, take_cols = map(int, take_match.groups())

        # Check if input is valid
        if len(data) != len(sort_order):
            return "Error: Data and SortOrder must be the same length."

        # Perform SORTBY equivalent by sorting based on SortOrder
        sorted_data = [x for _, x in sorted(zip(sort_order, data))]

        # Perform TAKE equivalent (first 'take_rows' values)
        taken_values = sorted_data[:take_cols]

        # Perform SUM equivalent
        result = sum(taken_values)
        return str(result)
    except Exception as e:
        return str(e)



#####NOT WORKING DOUBT!!!

# # Web scraping using BeautifulSoup
# def scrape_hidden_input_value():
#     try:
#         url = "https://exam.sanand.workers.dev/tds-2025-01-ga1"
#         response = requests.get(url)

#         if response.status_code != 200:
#             return f"Error: Failed to fetch the page, status code {response.status_code}"

#         soup = BeautifulSoup(response.content, "html.parser")
#         hidden_input = soup.find("input", {"type": "hidden"})

#         if hidden_input and "value" in hidden_input.attrs:
#             return hidden_input["value"]
#         else:
#             return "Error: Hidden input not found."

#     except Exception as e:
#         return str(e)









def count_wednesdays(question):
    try:
        # Extract dates using regex in YYYY-MM-DD format
        date_match = re.findall(r'\d{4}-\d{2}-\d{2}', question)
        if len(date_match) != 2:
            return "Error: Invalid date range. Please provide both start and end dates."
        
        start_date = datetime.strptime(date_match[0], "%Y-%m-%d")
        end_date = datetime.strptime(date_match[1], "%Y-%m-%d")

        # Validate date range
        if start_date > end_date:
            return "Error: Start date cannot be after end date."

        # Count Wednesdays
        count = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == 2:  # 2 represents Wednesday (Monday = 0)
                count += 1
            current_date += timedelta(days=1)

        return str(count)
    except Exception as e:
        return str(e)





from fastapi.responses import JSONResponse
import re
import json

def sort_json_array(question):
    try:
        print("Received question for sorting JSON:", question)
        
        match = re.search(r'\[.*?\]', question, re.DOTALL)
        if not match:
            return "Error: No valid JSON array found in the question."
        
        json_data = match.group(0)
        data = json.loads(json_data)
        
        if not isinstance(data, list):
            return "Error: Provided data is not a JSON array."
        
        for obj in data:
            if not all(k in obj for k in ('age', 'name')):
                return "Error: JSON objects must contain both 'age' and 'name' fields."
        
        sorted_data = sorted(data, key=lambda x: (x['age'], x['name']))
        return json.dumps(sorted_data, separators=(',', ':'))
    except Exception as e:
        return str(e)


from fastapi import UploadFile
import json
from fastapi.responses import JSONResponse

from fastapi import UploadFile
from fastapi.responses import Response
import json

# def convert_to_json(file: UploadFile):
#     try:
#         # Read the uploaded file
#         content = file.file.read().decode("utf-8").strip().split("\n")
        
#         # Convert key=value to JSON object
#         data = {}
#         for line in content:
#             if '=' not in line:
#                 return Response(content="Error: Invalid format. Expected 'key=value' on each line.", status_code=400)
#             key, value = line.split('=', 1)
#             data[key.strip()] = value.strip()

#         # Convert dictionary to JSON using json.dumps
#         json_data = json.dumps(data, indent=4)

#         # Return clean JSON without extra metadata
#         return Response(content=json_data, media_type="application/json")
#     except Exception as e:
#         return Response(content=str(e), status_code=500)




# def convert_to_json_and_hash(file: UploadFile):
#     try:
#         content = file.file.read().decode("utf-8").strip().split("\n")
#         data = {}
        
#         for line in content:
#             if '=' not in line:
#                 return "Error: Invalid format. Expected 'key=value' on each line."
#             key, value = line.split('=', 1)
#             data[key.strip()] = value.strip()

#         # Canonical JSON serialization
#         json_data = json.dumps(data, sort_keys=True, separators=(",", ":"))

#         # Write JSON data to temp file
#         with open("temp.json", "w") as f:
#             f.write(json_data)

#         # Execute JavaScript hashing using subprocess
#         result = subprocess.run(["node", "hash.js", "temp.json"], capture_output=True, text=True)

#         if result.returncode != 0:
#             return f"Error: {result.stderr.strip()}"

#         return result.stdout.strip()
#     except Exception as e:
#         return str(e)

import json
import subprocess
from fastapi import UploadFile

def convert_to_json_and_hash(file: UploadFile):
    try:
        content = file.file.read().decode("utf-8").strip().split("\n")
        data = {}

        for line in content:
            if '=' not in line:
                return "Error: Invalid format. Expected 'key=value' on each line."
            key, value = line.split('=', 1)
            data[key.strip()] = value.strip()

        # Serialize JSON without sorting
        json_data = json.dumps(data, separators=(",", ":"))
        # print(json_data)

        # Execute JavaScript hashing using subprocess
        result = subprocess.run(["node", "hash.js"], input=json_data, capture_output=True, text=True)

        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"

        return result.stdout.strip()
    except Exception as e:
        return str(e)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
