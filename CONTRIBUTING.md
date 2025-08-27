# Contributing to HRules

thank you for considering contributing to HRules!  
I welcome contributions from everyone — whether you’re fixing a typo, adding a feature, or improving documentation.

---

## How to Contribute

### 1. Fork the Repository
Click the **Fork** button at the top right of the GitHub page to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/yourusername/hrules.git
cd hrules
```

### 3. Create a Branch
#### Use a descriptive branch name:
```bash
git checkout -b feature/add-new-check
```

### 4. Set Up Your Environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 5. Make Your Changes
- Follow the existing code style
- Add comments where necessary
- Keep functions small and focused

### 6. Test Your Changes
Run the scanner on sample files to ensure nothing breaks

### 7. Commit Your Changes
```bash
git add .
git commit -m "Add: new visibility check for XYZ"
```

### 8. Push and Open a Pull Request
```bash
git push origin feature/add-new-check
```
Then open a Pull Request (PR) on GitHub

** **
## Code Style
- Use PEP 8 for Python code formatting
- Use clear, descriptive variable and function names
- Keep lines under 100 characters where possible


## Pull Request Checklist
### Before submitting your PR:
- Code compiles without errors
- Documentation updated (if needed)
- No sensitive data or credentials included

** ** 

***Use GitHub Issues for bug reports and feature requests***

***Be respectful and constructive in all discussions***