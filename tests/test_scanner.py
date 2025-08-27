# test_scanner.py
import io
from pathlib import Path
from PIL import Image
import pytest # for future tests
from hrules import scanner


def test_hidden_char_detection():
    text = "Hello\u200BWorld"  # contains a zero-width space
    count, highlighted = scanner.detect_hidden_chars(text)
    assert count == 1
    assert "⟦ZW⟧" in highlighted


def test_transparency_detection(tmp_path):
    img_path = tmp_path / "transparent.png"
    img = Image.new("RGBA", (2, 2), (255, 0, 0, 128))  # semi-transparent red
    img.save(img_path)
    has_trans, ratio = scanner.detect_transparency(img_path)
    assert has_trans
    assert ratio > 0


def test_low_contrast_detection():
    html = '<p style="color:#000000; background-color:#000000;">Test</p>'
    findings = scanner.detect_low_contrast_in_text_blob(html)
    assert any(f["ratio"] < scanner.CONTRAST_THRESHOLD for f in findings)


def test_scan_image_with_exif(tmp_path):
    img_path = tmp_path / "test.jpg"
    img = Image.new("RGB", (1, 1), (255, 255, 255))
    img.save(img_path)
    result = scanner.scan_image(img_path)
    assert "violations" in result
    assert "notes" in result


def test_scan_text_or_css(tmp_path):
    css_path = tmp_path / "style.css"
    css_path.write_text("body { color:#000; background-color:#000; }")
    result = scanner.scan_text_or_css(css_path)
    assert any("Low-contrast" in v for v in result["violations"])
