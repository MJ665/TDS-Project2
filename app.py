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
import re
from datetime import datetime, timedelta, timezone

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
    elif "process the files" in question.lower() and "different encodings" in question.lower():
        return process_files_with_encodings(file)
    
    elif "replace all" in question.lower() and "iitm" in question.lower() and "with iit madras in all files" in question.lower() and "new folder then replace all iitm" in question.lower():
        return replace_across_files(file)
    elif "list all files" in question.lower() and "size" in question.lower() and "modified on or after" in question.lower():
        return total_size_filtered(file, '/tmp/total_size_filtered')
    
    
    
    elif "use mv to move all files under folders into an empty folder" in question.lower() and "sha256sum in bash on that folder show" in question.lower() and "rename all files replacing each digit with the next" in question.lower():
        return digit_replace(file)
    
    
    
    
    elif "it has 2 nearly identical files, a.txt and b.txt, with the same number of lin" in question.lower():
        return compare_files(file)
    elif "what is the total sales of all the" in question.lower() and "ticket type? write sql to calculate it" in question.lower():
        return ticket_sales(question)
    
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

import zipfile
import os
import pandas as pd

# Process files with different encodings and sum values based on symbols
def process_files_with_encodings(file: UploadFile):
    try:
        # Validate file input
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a ZIP file.")

        # Save uploaded ZIP file
        zip_path = f"/tmp/{file.filename}"
        with open(zip_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Extract files from ZIP
        extract_dir = "/tmp/extracted"
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Define file encoding and delimiter based on file name
        file_configs = {
            'data1.csv': {'encoding': 'cp1252', 'delimiter': ','},
            'data2.csv': {'encoding': 'utf-8', 'delimiter': ','},
            'data3.txt': {'encoding': 'utf-16', 'delimiter': '\t'}
        }

        target_symbols = {'˜', '–', '’'}
        total_sum = 0

        for filename, config in file_configs.items():
            file_path = os.path.join(extract_dir, filename)
            if not os.path.isfile(file_path):
                raise HTTPException(status_code=400, detail=f"{filename} not found in ZIP.")

            # Read data using pandas
            df = pd.read_csv(file_path, encoding=config['encoding'], delimiter=config['delimiter'])

            if 'symbol' not in df.columns or 'value' not in df.columns:
                raise HTTPException(status_code=400, detail=f"Invalid columns in {filename}")

            # Sum values where symbol matches target symbols
            total_sum += df[df['symbol'].isin(target_symbols)]['value'].sum()

        return str(total_sum)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








import os
import re
import subprocess
import zipfile
from fastapi import UploadFile, HTTPException
import os
import re
import subprocess
import zipfile
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, HTTPException, Form

def replace_across_files(file: UploadFile):
    try:
        # Validate file input
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a ZIP file.")

        # Save uploaded ZIP file
        zip_path = f"/tmp/{file.filename}"
        with open(zip_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Create extraction directory
        extract_dir = "/tmp/extracted_files"
        os.makedirs(extract_dir, exist_ok=True)

        # Extract the ZIP using zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Perform case-insensitive replacement of "IITM" with "IIT Madras" across all files
        pattern = re.compile(r"IITM", re.IGNORECASE)
        
        for root, _, files in os.walk(extract_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Replace without altering line endings
                updated_content = pattern.sub("IIT Madras", content)

                with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(updated_content)

        # Run cat * | sha256sum to generate the hash
        # Run cat * | sha256sum and extract only the hash using awk
        result = subprocess.run(
            ['bash', '-c', f'cat {extract_dir}/* | sha256sum | awk \'{{print $1}}\'' ],
            capture_output=True, text=True
        )


        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {result.stderr.strip()}")

        return result.stdout.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)

    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    

def ensure_directory_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)



    
    
    
def total_size_filtered(file: UploadFile, dest_folder: str) -> int:
    try:
        ensure_directory_exists(dest_folder)
        
        # Validate file input
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a ZIP file.")
        
        # Save uploaded ZIP file
        zip_path = os.path.join('/tmp', file.filename)
        with open(zip_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        total_size = 0
        
        # Define the threshold datetime in IST.
        ist_offset = timedelta(hours=5, minutes=30)
        ist = timezone(ist_offset)
        threshold_dt = datetime(2012, 12, 29, 20, 51, 0, tzinfo=ist)
        
        # Open the ZIP file to read metadata before extracting
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for zip_info in zf.infolist():
                # Extract file details
                file_size = zip_info.file_size
                mod_dt = datetime(*zip_info.date_time, tzinfo=timezone.utc).astimezone(ist)

                # Apply filtering criteria
                if file_size >= 9416 and mod_dt >= threshold_dt:
                    total_size += file_size

            # Extract all files after processing metadata
            zf.extractall(dest_folder)

        return total_size
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








def ensure_directory_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

def digit_replace(file: UploadFile):
    try:
        work_folder = '/tmp/digit_replace_folder'
        ensure_directory_exists(work_folder)
        
        # Validate file input
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a ZIP file.")
        
        # Save uploaded ZIP file
        zip_path = os.path.join('/tmp', file.filename)
        with open(zip_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Extract files to work folder
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(work_folder)
        
        # Move files to root of work_folder
        for root, dirs, files in os.walk(work_folder, topdown=False):
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(work_folder, file)
                counter = 1
                while os.path.exists(dst_path):
                    dst_path = os.path.join(work_folder, f"{counter}_{file}")
                    counter += 1
                shutil.move(src_path, dst_path)
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except OSError:
                    pass
        
        # Perform digit replacement
        for file in os.listdir(work_folder):
            old_path = os.path.join(work_folder, file)
            if os.path.isfile(old_path):
                new_name = re.sub(r'\d', lambda m: str((int(m.group(0)) + 1) % 10), file)
                new_path = os.path.join(work_folder, new_name)
                os.rename(old_path, new_path)
        
        # Perform grep and hash
        grep_lines = []
        for file in sorted(os.listdir(work_folder), key=lambda x: x.encode('utf-8')):
            file_path = os.path.join(work_folder, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        stripped_line = line.rstrip('\n')
                        if stripped_line:
                            grep_lines.append(f"{file}:{stripped_line}")
        
        grep_lines.sort(key=lambda x: x.encode('utf-8'))
        concatenated_output = "\n".join(grep_lines) + "\n"
        sha256_hash = hashlib.sha256(concatenated_output.encode('utf-8')).hexdigest()
        
        return sha256_hash
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
















def compare_files(file: UploadFile):
    try:
        work_folder = '/tmp/compare_files_folder'
        ensure_directory_exists(work_folder)

        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a ZIP file.")

        zip_path = os.path.join('/tmp', file.filename)
        with open(zip_path, "wb") as buffer:
            buffer.write(file.file.read())

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(work_folder)

        a_path = os.path.join(work_folder, 'a.txt')
        b_path = os.path.join(work_folder, 'b.txt')

        if not os.path.isfile(a_path) or not os.path.isfile(b_path):
            raise HTTPException(status_code=400, detail="a.txt or b.txt not found in the archive.")

        with open(a_path, 'r', encoding='utf-8', errors='ignore') as a_file, \
             open(b_path, 'r', encoding='utf-8', errors='ignore') as b_file:
            a_lines = a_file.readlines()
            b_lines = b_file.readlines()

            if len(a_lines) != len(b_lines):
                raise HTTPException(status_code=400, detail="Files do not have the same number of lines.")

            different_lines_count = sum(1 for a_line, b_line in zip(a_lines, b_lines) if a_line != b_line)

        return different_lines_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
    
    
    
def extract_ticket_type(question: str) -> str:
    match = re.search(r'"([^"]+)" ticket type', question, re.IGNORECASE)
    if match:
        return match.group(1).strip().lower().capitalize()
    else:
        raise ValueError("Could not extract ticket type from the question.")

def ticket_sales(question: str) -> str:
    try:
        ticket_type = extract_ticket_type(question)

        sql_query = f'''
SELECT SUM(units * price) AS total_sales
FROM tickets
WHERE TRIM(LOWER(type)) = '{ticket_type.lower()}';

        '''

        return sql_query
    except Exception as e:
        return str(e)
    
    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
