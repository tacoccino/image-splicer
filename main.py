#!/usr/bin/env python3
"""
Image Splicer — entry point.

Run:  python main.py

Dependencies are auto-installed on first run if missing.
"""

import sys


def _install(pkg: str) -> None:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", pkg,
         "--break-system-packages", "-q"])


# ── ensure dependencies are available ────────────────────────────────────────

try:
    from PyQt6.QtWidgets import QApplication
except ImportError:
    _install("PyQt6")
    from PyQt6.QtWidgets import QApplication

try:
    from PIL import Image  # noqa: F401 — just checking it's installed
except ImportError:
    _install("Pillow")

# ── application entry point ───────────────────────────────────────────────────

from theme  import load_qss
from window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)

    # Fusion style ensures QPushButton colours are respected on all platforms.
    # macOS's native Aqua style ignores background/border on buttons.
    app.setStyle("Fusion")
    app.setStyleSheet(load_qss())

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
