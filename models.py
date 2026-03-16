"""
models.py — pure-Python data model.  No Qt imports.

Keep this file free of UI concerns so it can be imported and tested
without a display or Qt installation.
"""


class Sel:
    """
    A rectangular selection stored in image-space pixel coordinates (floats).

    Coordinates are image-space so they remain stable across zoom changes
    and window resizes.  Canvas/screen coordinates are derived on demand.
    """

    def __init__(self, ix1: float, iy1: float, ix2: float, iy2: float,
                 name: str = ""):
        self.ix1 = min(ix1, ix2)
        self.iy1 = min(iy1, iy2)
        self.ix2 = max(ix1, ix2)
        self.iy2 = max(iy1, iy2)
        self.name = name  # user-defined label; empty → fall back to index

    # ── geometry ──────────────────────────────────────────────────────────────

    def rect(self) -> tuple[float, float, float, float]:
        """Return (ix1, iy1, ix2, iy2)."""
        return (self.ix1, self.iy1, self.ix2, self.iy2)

    def width(self) -> float:
        return self.ix2 - self.ix1

    def height(self) -> float:
        return self.iy2 - self.iy1

    def fits_in(self, img_w: float, img_h: float) -> bool:
        """True if this selection is fully inside an image of the given size."""
        return (self.ix1 >= 0 and self.iy1 >= 0
                and self.ix2 <= img_w and self.iy2 <= img_h)

    # ── filename slug ─────────────────────────────────────────────────────────

    def filename_slug(self, fallback_index: int) -> str:
        """
        Return a filesystem-safe slug for use in saved filenames.

        Uses self.name if set, otherwise falls back to a zero-padded index.
        Special characters are replaced with underscores.
        """
        raw = self.name.strip() if self.name.strip() else f"{fallback_index:02d}"
        return "".join(
            c if c.isalnum() or c in "-_ " else "_"
            for c in raw
        ).strip()

    def __repr__(self) -> str:
        name_part = f" name={self.name!r}" if self.name else ""
        return (f"Sel({self.ix1:.1f},{self.iy1:.1f} → "
                f"{self.ix2:.1f},{self.iy2:.1f}{name_part})")
