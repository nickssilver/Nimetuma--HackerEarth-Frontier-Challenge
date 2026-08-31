"""Build the HackerEarth source-code zip."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
OUT_DIR = WORKSPACE / "submission"
ZIP_PATH = OUT_DIR / "Nimetuma-micro1-Frontier-Engineering-2026.zip"
SKIP_DIRS = {".venv", "__pycache__", ".pytest_cache", ".git", "nimetuma.egg-info"}
SKIP_SUFFIX = {".pyc"}


def keep(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return False
    if path.suffix in SKIP_SUFFIX:
        return False
    return True


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    count = 0
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in ROOT.rglob("*"):
            if not path.is_file() or not keep(path.relative_to(ROOT)):
                continue
            zf.write(path, Path("nimetuma") / path.relative_to(ROOT))
            count += 1
        form = OUT_DIR / "HACKEREARTH_FORM.md"
        if form.exists():
            zf.write(form, "HACKEREARTH_FORM.md")
            count += 1
    size = ZIP_PATH.stat().st_size
    print(f"wrote {ZIP_PATH}  ({count} files, {size // 1024} KB)")


if __name__ == "__main__":
    main()
