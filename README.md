# HRules

**HRules** is an open‑source, HR‑friendly document visibility compliance scanner.  
It helps HR teams, compliance officers, and document managers ensure that **all incoming and outgoing documents** — from job postings to contracts — are **clear, visible, and compliant**.  
No hidden clauses, no low‑contrast fine print, no invisible metadata.

> 💡 **Want to help improve HRules?** See [Contributing Guidelines](CONTRIBUTING.md).

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

### **Linux / macOS**
```bash
# Get the latest HRules
git clone https://github.com/<your-username>/HRules.git
cd HRules

# First time only: ensure launchers are executable
chmod +x hrules hrules-gui

# Launch the GUI
./hrules-gui

# Or run CLI mode
./hrules path/to/file.pdf
```
**On first run, HRules will create a local .venv in the project folder and install all dependencies automatically**


## Windows (batch or PowerShell)

# Get the latest HRules
```bash
git clone https://github.com/<your-username>/HRules.git
cd HRules

# Launch the GUI
.\hrules-gui.bat   # or: .\hrules-gui.ps1

# Or run CLI mode
.\hrules.bat path\to\file.pdf

```

## Project Structure
```bash
HRules/
├── hrules               # CLI launcher (Linux/macOS)
├── hrules-gui           # GUI launcher (Linux/macOS)
├── hrules.bat           # CLI launcher (Windows)
├── hrules-gui.bat       # GUI launcher (Windows)
├── hrules.ps1           # CLI launcher (Windows PowerShell)
├── hrules-gui.ps1       # GUI launcher (Windows PowerShell)
├── pyproject.toml       # Packaging and entry points
└── src/
    └── hrules/          # Main Python package
        ├── __init__.py
        ├── cli.py
        ├── gui.py
        └── ...
```
