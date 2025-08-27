# cli.py
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from hrules.scanner import scan_file, scan_directory
from hrules.report import format_block, write_txt_report

DEFAULT_REPORT = "hrules_report.txt"


def main():
    if len(sys.argv) < 2:
        print("Usage: hrules <file_or_directory> [--out report.txt]")
        sys.exit(1)

    target = Path(sys.argv[1])
    out = None
    if "--out" in sys.argv:
        try:
            out = Path(sys.argv[sys.argv.index("--out") + 1])
        except Exception:
            print("Invalid --out usage. Example: hrules ./docs --out report.txt")
            sys.exit(1)

    if not target.exists():
        print(f"[!] Path not found: {target}")
        sys.exit(1)

    pairs: List[Tuple[Path, Dict]] = []
    if target.is_dir():
        pairs = scan_directory(target)
        out_path = out or Path(DEFAULT_REPORT)
        write_txt_report(pairs, out_path)
        print(f"[+] Scan complete. Report saved to {out_path}")
        violations = sum(len(r["violations"]) for _, r in pairs)
        sys.exit(2 if violations > 0 else 0)
    else:
        res = scan_file(target)
        block = format_block(target, res)
        print(block)
        sys.exit(2 if res["violations"] else 0)


if __name__ == "__main__":
    main()
