"""
theme.py — stylesheet loading and theme application.

HOW THEMING WORKS
-----------------
style.qss uses a small set of named token hex values (see DARK_TOKENS below).
apply_theme() builds a token→value mapping for the current theme and accent
colour, then does a single-pass substitution on the raw QSS text before
passing it to Qt.  This means:

  • All colours in style.qss should use the canonical dark-theme hex values.
  • To add a new themeable colour, add it to DARK_TOKENS and a corresponding
    entry in _light_tokens().
  • Accent colour replaces #e94560 everywhere in the sheet.

ADDING A NEW THEME VARIANT
--------------------------
Define a new function alongside _light_tokens() that returns a dict with the
same keys as DARK_TOKENS, then wire it into apply_theme().
"""

from pathlib import Path
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication

# ── canonical dark-theme tokens ───────────────────────────────────────────────
# These exact hex strings must appear in style.qss.
# The mapping is: token_name → hex_value_in_qss
DARK_TOKENS = {
    "btn_top":   "#1a4070",   # top of button gradient
    "btn_base":  "#0f3460",   # base/bottom of button gradient, inputs
    "panel":     "#16213e",   # toolbar, side panel, list backgrounds
    "bg":        "#1a1a2e",   # window / dialog background
    "canvas":    "#0d0d1a",   # graphics view background
    "text":      "#eaeaea",   # primary text
    "text_white": "#ffffff",  # white text on green buttons
    "textdim":   "#8888aa",   # secondary / placeholder text, borders
    "accent":    "#e94560",   # accent — replaced by user-chosen colour
}


def _light_tokens(accent: str) -> dict:
    """Return token→value mapping for light theme."""
    return {
        "btn_top":    "#cad4e8",
        "btn_base":   "#b8c4d8",
        "panel":      "#dde1ea",
        "bg":         "#f0f2f5",
        "canvas":     "#c0c4d0",
        "text":       "#1a1a2e",
        "text_white": "#1a1a2e",
        "textdim":    "#555577",
        "accent":     accent,
    }


def _dark_tokens(accent: str) -> dict:
    """Return token→value mapping for dark theme."""
    return {**DARK_TOKENS, "accent": accent}


def load_qss(qss_dir: Path | None = None) -> str:
    """
    Load style.qss from qss_dir (defaults to this file's directory).
    Returns empty string if the file is missing — the app still runs, just unstyled.
    """
    search = qss_dir or Path(__file__).parent
    qss_path = search / "style.qss"
    if qss_path.exists():
        return qss_path.read_text()
    return ""


def apply_theme(cfg: dict, canvas_sel_items: list | None = None,
                qss_dir: Path | None = None) -> None:
    """
    Apply the current theme from cfg to the running QApplication.

    cfg keys used:
        theme  — "dark" | "light"
        accent — hex colour string, e.g. "#e94560"

    canvas_sel_items: optional list of SelItem instances to redraw after
        the colour globals are updated.
    """
    accent = cfg.get("accent", DARK_TOKENS["accent"])
    dark   = cfg.get("theme", "dark") == "dark"

    tokens = _dark_tokens(accent) if dark else _light_tokens(accent)
    global CURRENT_TOKENS
    CURRENT_TOKENS = tokens
    qss    = load_qss(qss_dir)

    # Substitute tokens — longest values first to avoid partial matches.
    # We iterate DARK_TOKENS so the substitution order is always consistent.
    for key in DARK_TOKENS:
        qss = qss.replace(DARK_TOKENS[key], tokens[key])

    app = QApplication.instance()
    if app:
        app.setStyleSheet(qss)

    # Update the runtime colour globals used by canvas drawing code
    _update_colour_globals(accent, cfg)

    # Redraw any existing selection items with the new colours
    if canvas_sel_items:
        for item in canvas_sel_items:
            item.set_active(item._active)
            item._sync()


# ── runtime colour globals ────────────────────────────────────────────────────
# These are used directly by SelItem for drawing; kept here so theme.py
# is the single source of truth for all colour decisions.

C_BG      = QColor(DARK_TOKENS["bg"])
C_PANEL   = QColor(DARK_TOKENS["panel"])

# Overlay fill — updated from config by apply_theme()
C_OVERLAY    = "#ff0000"   # overlay fill colour (hex string)
OVERLAY_ALPHA = 80          # 0–255 opacity
C_ACCENT  = QColor(DARK_TOKENS["accent"])
C_GREEN   = QColor("#27ae60")
C_TEXT    = QColor(DARK_TOKENS["text"])
C_TEXTDIM = QColor(DARK_TOKENS["textdim"])
C_HANDLE  = QColor("#ffd700")
C_SEL     = QColor(DARK_TOKENS["accent"])
C_SEL_ACT = QColor(DARK_TOKENS["accent"]).lighter(130)


# Current resolved token values — updated by apply_theme() on every call.
# Use these anywhere you need the live theme colour in Python code.
CURRENT_TOKENS: dict = dict(DARK_TOKENS)


def _update_colour_globals(accent: str, cfg: dict | None = None) -> None:
    """Update the module-level colour globals when the accent or cfg changes."""
    global C_ACCENT, C_SEL, C_SEL_ACT, C_OVERLAY, OVERLAY_ALPHA
    C_ACCENT  = QColor(accent)
    C_SEL     = QColor(accent)
    C_SEL_ACT = QColor(accent).lighter(130)
    if cfg:
        C_OVERLAY    = cfg.get("overlay_color",   "#ff0000")
        OVERLAY_ALPHA = cfg.get("overlay_opacity",  80)
