# Structured Data Extraction

A Python project for extracting structured data (like invoice fields) from unstructured PDF documents using LLM-based parsing. This repository includes sample PDFs, and processing-pipeline for exporting extracted data to Excel.

---

## Features

- Extracts structured fields (customer name, address, invoice number, date, amount due) from PDFs.
- LLM-based workflow (LLaMa) for high-quality parsing.
- Used locally hosted open-source LLM to mitigate data privacy concerns associated with cloud-based APIs.
- Saves extracted results into an Excel file (`extracted_invoice_data.xlsx`).
- Easily extensible for other document types or models..

---

## Project Structure

.
├── Sample PDFs/                     
├── PDFdataExtraction_ollama.py      
├── util.py                          
├── extracted_invoice_data.xlsx      
├── requirements.txt                 
├── .gitignore  
└── README.md  


---

## Installation

Clone the repository:

```bash
git clone https://github.com/AnandKri/structured-data-extraction.git
cd structured-data-extraction
```

Ensure Ollama is installed and the required model is pulled:

```bash
ollama pull llama3.2:1b-instruct-q8_0
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the extraction script:

```bash
python PDFdataExtraction_ollama.py
```