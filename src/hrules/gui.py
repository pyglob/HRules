# gui.py
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Tuple, Dict

from hrules.scanner import scan_file, scan_directory
from hrules.report import format_block, write_txt_report, write_pdf_report

APP_TITLE = "HRules — Document Visibility Scanner"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x620")
        self._build_ui()
        self.target: Path | None = None
        self.results: List[Tuple[Path, Dict]] = []

    def _build_ui(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)

        self.path_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(top, text="Choose File/Folder", command=self.choose_target).pack(side=tk.LEFT)
        ttk.Button(top, text="Scan", command=self.run_scan).pack(side=tk.LEFT, padx=(8, 0))

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=10)

        nb = ttk.Notebook(frame)
        nb.pack(fill=tk.BOTH, expand=True)

        self.txt_output = tk.Text(nb, wrap="word")
        self.txt_output.configure(font=("Consolas", 10))
        nb.add(self.txt_output, text="Results")

        btns = ttk.Frame(frame)
        btns.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btns, text="Save TXT Report", command=self.save_txt).pack(side=tk.LEFT)
        ttk.Button(btns, text="Save PDF Report", command=self.save_pdf).pack(side=tk.LEFT, padx=(8, 0))

        # Drag & drop (basic): clicking area behaves like choose dialog; true DnD requires extra packages
        hint = ttk.Label(frame, text="Tip: Drag files/folders onto this window title bar on Windows, or use 'Choose File/Folder'.")
        hint.pack(anchor="w", pady=(6, 0))

    def choose_target(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.target = Path(file_path)
            self.path_var.set(str(self.target))
            return
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.target = Path(dir_path)
            self.path_var.set(str(self.target))

    def run_scan(self):
        if not self.path_var.get():
            messagebox.showwarning("HRules", "Please choose a file or folder to scan.")
            return
        self.target = Path(self.path_var.get())
        if not self.target.exists():
            messagebox.showerror("HRules", "Selected path does not exist.")
            return
        self._start_background(self._scan)

    def _scan(self):
        self._set_busy(True)
        self.txt_output.delete("1.0", tk.END)
        try:
            if self.target.is_dir():
                self.results = scan_directory(self.target)
            else:
                self.results = [(self.target, scan_file(self.target))]
            for p, r in self.results:
                self.txt_output.insert(tk.END, format_block(p, r))
            self.txt_output.see(tk.END)
            messagebox.showinfo("HRules", "Scan complete.")
        except Exception as e:
            messagebox.showerror("HRules", f"Scan failed: {e}")
        finally:
            self._set_busy(False)

    def save_txt(self):
        if not self.results:
            messagebox.showwarning("HRules", "No results to save.")
            return
        out = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")], initialfile="hrules_report.txt")
        if not out:
            return
        write_txt_report(self.results, Path(out))
        messagebox.showinfo("HRules", f"Saved: {out}")

    def save_pdf(self):
        if not self.results:
            messagebox.showwarning("HRules", "No results to save.")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile="hrules_report.pdf")
        if not out:
            return
        write_pdf_report(self.results, Path(out))
        messagebox.showinfo("HRules", f"Saved: {out}")


    def _start_background(self, func):
        t = threading.Thread(target=func, daemon=True)
        t.start()

    def _set_busy(self, busy: bool):
        if busy:
            self.progress.start(60)
        else:
            self.progress.stop()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
