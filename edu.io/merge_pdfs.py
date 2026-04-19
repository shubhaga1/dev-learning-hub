"""
merge_pdfs.py — merge all PDFs in each course subfolder into one file.

Output per folder:  _MERGED_<FolderName>.pdf  (inside the same folder)
Originals:          untouched
Safe to re-run:     skips folders that already have a _MERGED_ file

Usage:
    python3 merge_pdfs.py
"""

import os
import re
import sys
import time
import subprocess
from pathlib import Path

# Auto-install pypdf inside a venv if missing (Homebrew Python blocks system pip)
try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    import venv, subprocess, sys
    from pathlib import Path
    venv_dir = Path(__file__).parent / ".venv"
    if not venv_dir.exists():
        print("pypdf not found — creating venv and installing...")
        venv.create(str(venv_dir), with_pip=True)
    venv_python = venv_dir / "bin" / "python"
    subprocess.check_call([str(venv_python), "-m", "pip", "install", "--quiet", "pypdf"])
    # Re-exec this script inside the venv so imports work
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)


ROOT = Path(__file__).parent


def numeric_sort_key(filename: str) -> tuple:
    """Sort '10_Foo.pdf' after '2_Bar.pdf' — by leading number, not alphabetically."""
    match = re.match(r'^(\d+)', filename)
    return (int(match.group(1)) if match else float('inf'), filename)


def merge_course(folder: Path) -> dict:
    """
    Merge all PDFs in folder into _MERGED_<name>.pdf.
    Returns a result dict with status and details.
    """
    name        = folder.name
    output_path = folder / f"_MERGED_{name}.pdf"

    # Skip if already merged
    if output_path.exists():
        return {"folder": name, "status": "skipped", "files": 0, "note": "already merged"}

    # Collect PDFs — exclude any _MERGED_ files
    pdfs = sorted(
        [f for f in folder.iterdir() if f.suffix.lower() == ".pdf" and not f.name.startswith("_MERGED_")],
        key=lambda f: numeric_sort_key(f.name),
    )

    if not pdfs:
        return {"folder": name, "status": "skipped", "files": 0, "note": "no PDFs found"}

    writer  = PdfWriter()
    failed  = []

    for pdf_path in pdfs:
        try:
            reader = PdfReader(str(pdf_path))
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            failed.append(f"{pdf_path.name}: {e}")

    if not writer.pages:
        return {"folder": name, "status": "failed", "files": len(pdfs), "note": "no pages merged — all files failed"}

    try:
        with open(output_path, "wb") as f:
            writer.write(f)
        size_mb = output_path.stat().st_size / (1024 * 1024)
    except Exception as e:
        return {"folder": name, "status": "failed", "files": len(pdfs), "note": str(e)}

    return {
        "folder":   name,
        "status":   "ok" if not failed else "partial",
        "files":    len(pdfs),
        "pages":    len(writer.pages),
        "size_mb":  round(size_mb, 1),
        "skipped":  failed,
        "note":     f"{len(failed)} file(s) had errors" if failed else "",
    }


def main():
    folders = sorted([
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

    total    = len(folders)
    ok       = 0
    partial  = 0
    failed   = 0
    skipped  = 0
    start    = time.time()

    print(f"Merging PDFs in {total} course folders...\n")

    for i, folder in enumerate(folders, 1):
        result = merge_course(folder)
        status = result["status"]

        # Progress line
        symbol = {"ok": "✓", "partial": "~", "failed": "✗", "skipped": "–"}.get(status, "?")
        detail = (
            f"{result.get('files', 0)} files → {result.get('pages', 0)} pages, {result.get('size_mb', 0)} MB"
            if status in ("ok", "partial") else result.get("note", "")
        )
        print(f"[{i:3}/{total}] {symbol}  {folder.name[:55]:<55}  {detail}")

        if result.get("skipped"):
            for err in result["skipped"]:
                print(f"            ↳ WARN: {err}")

        if status == "ok":       ok      += 1
        elif status == "partial": partial += 1
        elif status == "failed":  failed  += 1
        elif status == "skipped": skipped += 1

    elapsed = time.time() - start
    print(f"""
{'='*65}
DONE in {elapsed:.0f}s

  ✓ merged   : {ok}
  ~ partial  : {partial}
  ✗ failed   : {failed}
  – skipped  : {skipped}
  total      : {total}
{'='*65}
    """)


if __name__ == "__main__":
    main()
