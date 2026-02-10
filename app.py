# -*- coding: utf-8 -*-

"""

Created on Thu Feb  5 10:11:32 2026

 

@author: Sydney

"""

#!{sys.executable} -m pip install fastapi uvicorn python-multipart

 

 

from fastapi import FastAPI, UploadFile, File, Form, Request

from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

import os

import uuid

 

app = FastAPI()

 

# Get the directory where app.py is located

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

 

# Create directories if they don't exist

os.makedirs(TEMPLATES_DIR, exist_ok=True)

os.makedirs(UPLOAD_DIR, exist_ok=True)

 

# Initialize templates

templates = Jinja2Templates(directory=TEMPLATES_DIR)

 

# Maximum file size: 10MB

MAX_BYTES = 10 * 1024 * 1024

 

 

@app.get("/", response_class=HTMLResponse)

async def home(request: Request):

    """Serve the main upload page"""

    return templates.TemplateResponse("index.html", {"request": request})

 

 

@app.post("/api/upload")

async def upload_file(

    document_type: str = Form(...),

    file: UploadFile = File(...),

):

    """Handle file upload"""

    try:

        # Read file content

        contents = await file.read()

       

        # Check file size

        if len(contents) > MAX_BYTES:

            return JSONResponse(

                {"ok": False, "error": "File exceeds 10MB limit"},

                status_code=400

            )

       

        # Generate unique file ID

        file_id = str(uuid.uuid4())

       

        # Sanitize filename

        safe_name = (file.filename or "upload").replace("/", "_").replace("\\", "_")

        file_path = os.path.join(UPLOAD_DIR, f"{file_id}__{safe_name}")

       

        # Save file

        with open(file_path, "wb") as f:

            f.write(contents)

       

        return {

            "ok": True,

            "fileId": file_id,

            "filename": file.filename,

            "documentType": document_type,

        }

   

    except Exception as e:

        return JSONResponse(

            {"ok": False, "error": str(e)},

            status_code=500

        )

 

 

@app.post("/api/remove")

async def remove_file(file_id: str = Form(...)):

    """Remove an uploaded file"""

    try:

        removed = False

       

        # Find and remove file with matching ID

        for filename in os.listdir(UPLOAD_DIR):

            if filename.startswith(file_id + "__"):

                try:

                    os.remove(os.path.join(UPLOAD_DIR, filename))

                    removed = True

                except Exception:

                    pass

       

        return {"ok": True, "removed": removed}

   

    except Exception as e:

        return JSONResponse(

            {"ok": False, "error": str(e)},

            status_code=500

        )

 

 

@app.post("/api/submit")

async def submit(file_ids: str = Form(...)):

    """Handle final submission of documents"""

    try:

        # Parse file IDs

        ids = [x.strip() for x in file_ids.split(",") if x.strip()]

       

        if not ids:

            return JSONResponse(

                {"ok": False, "error": "No files submitted"},

                status_code=400

            )

       

        # In a real application, you would:

        # - Validate file ownership

        # - Trigger OCR pipeline

        # - Store results in database

        # - Send confirmation emails

        # etc.

       

        return {"ok": True, "submittedCount": len(ids)}

   

    except Exception as e:

        return JSONResponse(

            {"ok": False, "error": str(e)},

            status_code=500

        )

 

 

#if __name__ == "__main__":

#   import uvicorn

  #  uvicorn.run(app, host="0.0.0.0", port=8000)