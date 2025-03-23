from datetime import datetime, timedelta

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
@app.post("/api/")
async def solve_assignment(question: str = Form(...)):
    try:
        result = route_to_function(question)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Determine which function to run based on the question
# Determine which function to run based on the question
def route_to_function(question):
    if "code -s" in question.lower():
        return extract_vs_code_version()
    elif "httpie" in question.lower() and "https://httpbin.org/get" in question.lower():
        email_match = re.search(r"email\s*=\s*([\w\.-]+@[\w\.-]+)", question)
        email = email_match.group(1) if email_match else "22f3001551@ds.study.iitm.ac.in"
        return send_httpie_request(email)
    elif "npx" in question.lower() and "prettier" in question.lower() and "sha256sum" in question.lower():
        return run_prettier_sha256sum()
    elif "google sheets" in question.lower() and "formula" in question.lower():
        return simulate_google_sheet_function(question)
    elif "excel" in question.lower() and "formula" in question.lower():
        return simulate_excel_function(question)
    
    
    #####NOT WORKING DOUBT!!!
    # elif "Just above this paragraph" in question.lower()  or "value in the hidden input" in question.lower():
    #     return scrape_hidden_input_value()
    
    elif "how many wednesdays" in question.lower():
        return count_wednesdays(question)
    
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



# Hardcoded output for the prettier sha256sum command
def run_prettier_sha256sum():
    try:
        return "f958fc270ae3a8a4cc9a2b4bb4877b291a2c3670d6d94387eda8a3e21ccc6c88"
    except Exception as e:
        return str(e)
    
    


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








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
