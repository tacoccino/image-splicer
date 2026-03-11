# Image Splicer

A lightweight desktop utility for cropping multiple regions out of an image and saving each one as a separate file. Built for speed — no save dialogs, no confirmations, just draw and export.

## Requirements

- Python 3.8+
- [Pillow](https://python-pillow.org/) — installed automatically on first run if missing

No other dependencies. Uses Python's built-in `tkinter` for the UI.

On **Windows**, drag-and-drop uses `ctypes` from the standard library — no extra packages needed.

## Running

```bash
python3 image_splicer.py
```

Pass `--debug` to print drag-and-drop diagnostics to the terminal:

```bash
python3 image_splicer.py --debug
```

## Usage

### Opening an image

- Click **⊞ Open Image** or press `Cmd+O` / `Ctrl+O`
- Drag and drop an image file onto the window (Windows and macOS)

### Drawing selections

Click and drag anywhere on the canvas to draw a rectangle selection. You can draw as many as you need. Each selection is numbered and listed in the panel on the right.

Selections are stored in image-space coordinates — they stay locked to the same region of the image regardless of zoom level or window size.

### Adjusting selections

- **Move** — click inside a selection and drag
- **Resize** — drag any edge or corner (the cursor changes to show the resize direction)
- **Delete one** — click a selection to activate it, then press `Delete` or `Backspace`, or click the ✕ next to it in the side panel
- **Undo last** — `Cmd+Z` / `Ctrl+Z`
- **Clear all** — click **✕ Clear All** in the toolbar

### Navigating the canvas

- **Zoom in** — scroll up, or `Cmd+=` / `Ctrl+=`
- **Zoom out** — scroll down, or `Cmd+−` / `Ctrl+−`
- **Fit to window** — click **⊡** or press `Cmd+0` / `Ctrl+0`
- **Pan** — hold `Shift` and drag anywhere on the canvas

### Saving crops

1. Click **⌂ Save Location** once to choose a folder. The current path is shown as a tooltip when hovering over the button. This setting is remembered between sessions.
2. Set a **filename prefix** and **format** (PNG, JPEG, WEBP, BMP, or TIFF) in the side panel. These are also remembered.
3. Click **✦ Save Crops** or press `Cmd+S` / `Ctrl+S`.

Files are saved as `<prefix>_01.png`, `<prefix>_02.png`, etc. If a file already exists, a number is appended to avoid overwriting. A brief toast notification appears on the canvas confirming how many crops were saved.

### Loading the next image

When **Keep selections** (toolbar checkbox) is ticked, loading a new image will carry over any selections that fit within the new image's bounds — useful when cropping the same regions across many similar images. Selections that fall outside the new image are removed automatically. Uncheck it to always start fresh.

## Keyboard Shortcuts

> On macOS, replace `Ctrl` with `Cmd`.

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Open image |
| `Ctrl+S` | Save all crops |
| `Ctrl+Z` | Delete last selection |
| `Ctrl+=` | Zoom in |
| `Ctrl+−` | Zoom out |
| `Ctrl+0` | Fit image to window |
| `Delete` / `Backspace` | Delete active selection |
| `Escape` | Cancel current draw |
| Scroll wheel | Zoom in / out |
| `Shift+drag` | Pan the canvas |

## Settings

Preferences are stored in `~/.image_splicer_config.json`:

| Key | Description |
|---|---|
| `save_dir` | Output folder path |
| `prefix` | Filename prefix for saved crops |
| `format` | Output image format |
| `keep_sels` | Whether to keep selections when loading a new image |
