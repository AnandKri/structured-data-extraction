import fitz
import os

class Invoice:
    def __init__(self, rel_pdf_path):
        """
        Initialize using a relative PDF path.
        """
        self.pdf_path = os.path.abspath(rel_pdf_path)
        self.text_data = ""
        self.extract_structured_text()

    def extract_structured_text(self, pixel_threshold=10):
        """
        Extract structured text while preserving horizontal order.
        """
        structured_lines = ""

        doc = fitz.open(self.pdf_path)
        
        for page in doc:
            blocks = page.get_text("blocks")
            lines = {}

            for block in blocks:
                x0, y0, x1, y1, text, *_ = block
                if not text.strip():
                    continue
                y_key = round(y0 / pixel_threshold)
                lines.setdefault(y_key, []).append((x0, text))
            
            for y_key in sorted(lines.keys()):
                line_chunks = lines[y_key]
                line_chunks.sort(key=lambda x: x[0])
                structured_line = "\t".join(chunk[1].strip() for chunk in line_chunks)
                structured_lines += "\n" + structured_line

        self.text_data = structured_lines

def get_pdf_file_paths(relative_dir):
    script_dir = os.path.dirname(__file__)
    base_dir = os.path.join(script_dir, relative_dir)

    pdf_paths = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, script_dir)
                pdf_paths.append(rel_path)
    return pdf_paths

schema = {
        "title":"Test",
        "description":"Extract data from pdfs",
        "type":"object",
        "properties":{
            "customerName":{
                "type":"string",
                "description":"get customer name for whom the invoice was generated",
                "default":"customer name not found"
            },
            "address":{
                "type":"string",
                "description":"customer address as mentioned in the invoice",
                "default":""
            },
            "invoiceNumber":{
                "type":"integer",
                "description":"invoice number (unique ID) as mentioned in the invoice. Starts with hash",
                "default":""
            },
            "invoiceDate":{
                "type":"string",
                "description":"invoice date as mentioned in the invoice, extract in the format 'dd-mmm-yy'",
                "default":""
            },
            "amountDue":{
                "type":"integer",
                "description":"due amount which was paid or to be paid. Include decimal values as well if present.",
                "default":""
            }
        },
        "required":["customerName", "address", "invoiceNumber", "invoiceDate", "amountDue"]
    }