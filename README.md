# Loan Application Document Upload

A FastAPI application for handling document uploads for loan applications.

## Setup Instructions

1. Install dependencies:
```bash
pip install fastapi uvicorn jinja2 python-multipart
```

2. Run the application:
```bash
uvicorn app:app --reload
```

3. Open your browser to: http://localhost:8000

## Project Structure

```
your_project/
├── app.py                 # FastAPI backend
├── templates/
│   └── index.html        # Frontend interface
└── uploads/              # Uploaded files (auto-created)
```

## Features

- Document type selection (W-2, Pay Stubs, Bank Statements, Government ID)
- Drag & drop file upload
- Upload progress tracking
- File validation (10MB limit)
- Upload queue management
- Success confirmation page
