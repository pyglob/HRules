# HRules

**HRules** is an open‑source, HR‑friendly document visibility compliance scanner.  
It helps HR teams, compliance officers, and document managers ensure that **all incoming and outgoing documents** — from job postings to contracts — are **clear, visible, and compliant**.  
No hidden clauses, no low‑contrast fine print, no invisible metadata.

---

## Features

- **Hidden text detection** - zero‑width characters, hidden Word runs, invisible HTML/CSS.
- **Low‑contrast text check** - flags text that fails WCAG readability standards.
- **Transparency scan** - finds semi‑transparent or hidden elements in images.
- **OCR on images** - detects text baked into graphics or embedded in PDFs/DOCX.
- **Metadata inspection** - flags EXIF data, PSD hidden layers, and more.
- **Multi‑format support** - DOCX, PDF, HTML, TXT, PNG, JPG, PSD, CSS.
- **HR‑friendly reports** - plain‑language results with severity icons.

---

## Installation
   Steps to install HRules

### Install Dependencies

#### macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate

#### Windows (PowerShell)
    python -m venv .venv
    .venv\Scripts\Activate.ps1

Once your virtual environment is active:

```bash 
pip install -r requirements.txt
```

#### This will install all required libraries, including:
```bash
Pillow
python-docx
PyMuPDF
pytesseract
BeautifulSoup4
cssutils
psd-tools
reportlab
```

### Usage
```bash
hrules path/to/file_or_folder
```

### GUI
How to run the graphical interface
```bash
hrules-gui
```

## Project Structure
```bash
src/hrules/
    __init__.py    # Marks this as a Python package
    scanner.py     # Core scanning logic
    report.py      # Report formatting and export
    cli.py         # Command-line interface
    gui.py         # HR-friendly GUI
requirements.txt   # Python dependencies
pyproject.toml     # Project metadata and build config
README.md          # Project documentation
```
