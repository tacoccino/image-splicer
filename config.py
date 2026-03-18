"""
config.py — load and save user configuration.

All user data lives in ~/.imagesplicer/:
  config.json   — app settings
  themes/       — user-created theme JSON files

This directory is created on first use if it doesn't exist.
"""

import json
from pathlib import Path

# ── user directory ────────────────────────────────────────────────────────────

def user_dir() -> Path:
    """Return ~/.imagesplicer/, creating it if necessary."""
    d = Path.home() / ".imagesplicer"
    d.mkdir(exist_ok=True)
    return d


def user_themes_dir() -> Path:
    """Return ~/.imagesplicer/themes/, creating it if necessary."""
    d = user_dir() / "themes"
    d.mkdir(exist_ok=True)
    return d


CONFIG_FILE = user_dir() / "config.json"

# ── migrate old config if present ────────────────────────────────────────────
_OLD_CONFIG = Path.home() / ".image_splicer_config.json"


def _migrate():
    """Move the old flat config file into the new user dir, once."""
    if _OLD_CONFIG.exists() and not CONFIG_FILE.exists():
        try:
            CONFIG_FILE.write_text(_OLD_CONFIG.read_text())
            _OLD_CONFIG.unlink()
        except Exception:
            pass

_migrate()

# ── defaults ──────────────────────────────────────────────────────────────────

DEFAULTS = {
    "save_dir":        "",
    "prefix":          "",
    "format":          "PNG",
    "jpeg_quality":    90,
    "theme":           "Dark",
    "accent":          "#e94560",
    "keep_sels":       True,
    "overlay_color":   "#ff0000",
    "overlay_opacity": 30,
    "font_scale":      1.0,
    "zoom_speed":      1.0,
    "filename_pattern": "",
}


def load_cfg() -> dict:
    """Return config dict, merged with defaults so all keys are always present."""
    cfg = dict(DEFAULTS)
    try:
        if CONFIG_FILE.exists():
            stored = json.loads(CONFIG_FILE.read_text())
            cfg.update(stored)
    except Exception:
        pass
    return cfg


def save_cfg(cfg: dict) -> None:
    """Persist config to disk. Silently swallows errors."""
    try:
        user_dir()  # ensure dir exists
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
    except Exception:
        pass
