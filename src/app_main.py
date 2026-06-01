"""Minimal PyQt entry point for the portfolio version of the GUI.

The original GUI lives in ``financial/qt_design`` and ``22_hf352-master/week16``.
Those files include generated UI loading and historical experiment logic.  This
module provides a small, readable entry point that can be used as the public
starting place while the original UI files remain available for reference.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from .config import PROJECT_ROOT


DEFAULT_UI_PATH = PROJECT_ROOT / "financial" / "qt_design" / "main_window.ui"


class PortfolioMainWindow(QMainWindow):
    """Load the historical Qt Designer screen when the UI file is present."""

    def __init__(self, ui_path: Path = DEFAULT_UI_PATH):
        super().__init__()
        if not ui_path.exists():
            raise FileNotFoundError(f"UI file not found: {ui_path}")
        uic.loadUi(str(ui_path), self)
        self.setWindowTitle("ICT 멘토링 금융 상품 가격 예측 시스템")


def main() -> int:
    app = QApplication(sys.argv)
    window = PortfolioMainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
