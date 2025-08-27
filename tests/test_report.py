# test_report.py
from pathlib import Path
from hrules import report


def test_format_block():
    dummy_path = Path("dummy.txt")
    dummy_results = {
        "violations": ["Hidden text found "],
        "notes": ["Excerpt:\nHello⟦ZW⟧World"]
    }
    output = report.format_block(dummy_path, dummy_results)
    assert "[dummy.txt]" in output
    assert "Hidden text found" in output
    assert "Excerpt" in output


def test_write_txt_report(tmp_path):
    dummy_path = tmp_path / "file.txt"
    dummy_results = {
        "violations": ["Low contrast text "],
        "notes": ["Snippet: <<<HIGHLIGHT>>>...<<<END>>>"]
    }
    pairs = [(dummy_path, dummy_results)]
    out_file = tmp_path / "report.txt"
    report.write_txt_report(pairs, out_file)
    content = out_file.read_text()
    assert "Low contrast text" in content


def test_write_pdf_report(tmp_path):
    dummy_path = tmp_path / "file.txt"
    dummy_results = {
        "violations": ["Transparency detected "],
        "notes": ["Note: Example"]
    }
    pairs = [(dummy_path, dummy_results)]
    out_file = tmp_path / "report.pdf"
    report.write_pdf_report(pairs, out_file)
    assert out_file.exists()
    assert out_file.stat().st_size > 0
