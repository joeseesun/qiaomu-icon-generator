#!/usr/bin/env python3
"""Export a selected square icon candidate to web and iOS app-icon sizes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


DEFAULT_WEB_SIZES = (32, 64, 180, 192, 512, 1024)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Selected source PNG.")
    parser.add_argument("--web-out", type=Path, help="Directory for web icon PNGs.")
    parser.add_argument("--web-prefix", default="app-icon", help="Web output filename prefix.")
    parser.add_argument(
        "--web-sizes",
        default=",".join(str(size) for size in DEFAULT_WEB_SIZES),
        help="Comma-separated square web sizes, default: 32,64,180,192,512,1024.",
    )
    parser.add_argument("--appiconset", type=Path, help="Existing Xcode AppIcon.appiconset directory.")
    return parser.parse_args()


def load_square_rgb(source: Path) -> Image.Image:
    img = Image.open(source).convert("RGB")
    width, height = img.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return img.crop((left, top, left + side, top + side))


def save_png(img: Image.Image, path: Path, size: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.resize((size, size), Image.Resampling.LANCZOS).save(path, optimize=True)


def export_web(img: Image.Image, out_dir: Path, prefix: str, sizes_text: str) -> list[Path]:
    sizes = [int(part) for part in re.split(r"[, ]+", sizes_text.strip()) if part]
    outputs: list[Path] = []
    for size in sizes:
        path = out_dir / f"{prefix}-{size}.png"
        save_png(img, path, size)
        outputs.append(path)
    return outputs


def pixels_from_appicon_entry(entry: dict) -> int | None:
    size_text = entry.get("size")
    scale_text = entry.get("scale", "1x")
    if not size_text:
        return None
    try:
        point_size = float(str(size_text).split("x", 1)[0])
        scale = int(str(scale_text).rstrip("x"))
    except ValueError:
        return None
    return int(round(point_size * scale))


def export_appiconset(img: Image.Image, appiconset: Path) -> list[Path]:
    contents_path = appiconset / "Contents.json"
    if not contents_path.exists():
        raise FileNotFoundError(f"Missing {contents_path}")
    contents = json.loads(contents_path.read_text(encoding="utf-8"))
    outputs: list[Path] = []
    for entry in contents.get("images", []):
        filename = entry.get("filename")
        pixels = pixels_from_appicon_entry(entry)
        if not filename or not pixels:
            continue
        path = appiconset / filename
        save_png(img, path, pixels)
        outputs.append(path)
    return outputs


def main() -> int:
    args = parse_args()
    img = load_square_rgb(args.source)
    outputs: list[Path] = []
    if args.web_out:
        outputs.extend(export_web(img, args.web_out, args.web_prefix, args.web_sizes))
    if args.appiconset:
        outputs.extend(export_appiconset(img, args.appiconset))
    for path in outputs:
        print(path)
    print(f"Exported {len(outputs)} files from {args.source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
