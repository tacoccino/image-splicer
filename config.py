"""
config.py — load and save user configuration.

The config file lives at ~/.image_splicer_config.json.
All keys are optional; callers should use .get() with a default.
"""

import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".image_splicer_config.json"

# Defaults used throughout the app
DEFAULTS = {
    "save_dir":     "",
    "prefix":       "crop",
    "format":       "PNG",
    "jpeg_quality": 90,
    "theme":        "dark",
    "accent":       "#e94560",
    "keep_sels":      True,
    "overlay_color":   "#ff0000",
    "overlay_opacity": 30,
    "font_scale":      1.0,
    "zoom_speed":      1.0,
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
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
    except Exception:
        pass
