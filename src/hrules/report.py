from pathlib import Path
from typing import Dict, List, Tuple
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

H_START = "<<<HIGHLIGHT>>>"
H_END = "<<<END>>>"

def format_block(path: Path, res: Dict[str, List[str]]) -> str:
    lines = [f"[{path}]"]
    for v in res.get("violations", []):
        lines.append(f"  - {v}")
    for n in res.get("notes", []):
        if "\n" in n:
            lines.append("  - Note:")
            for ln in n.splitlines():
                lines.append(f"      {ln}")
        else:
            lines.append(f"  - Note: {n}")
    lines.append("")
    return "\n".join(lines)

def write_txt_report(pairs: List[Tuple[Path, Dict[str, List[str]]]], out_path: Path) -> None:
    out_lines = []
    for p, r in pairs:
        out_lines.append(format_block(p, r))
    out_path.write_text("\n".join(out_lines), encoding="utf-8")

def write_pdf_report(pairs: List[Tuple[Path, Dict[str, List[str]]]], out_path: Path) -> None:
    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4
    x, y = 40, height - 40
    def draw_line(text):
        nonlocal y
        if y < 60:
            c.showPage()
            y = height - 40
        c.drawString(x, y, text[:120])
        y -= 14
    for p, r in pairs:
        draw_line(f"[{p}]")
        for v in r.get("violations", []):
            draw_line(f"  - {v}")
        for n in r.get("notes", []):
            if "\n" in n:
                draw_line("  - Note:")
                for ln in n.splitlines():
                    draw_line(f"      {ln}")
            else:
                draw_line(f"  - Note: {n}")
        draw_line("")
    c.save()
