#!/usr/bin/env python3
"""Extract the original SYSU artwork. Build does not depend on this script."""

import argparse
import hashlib
import io
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from PIL import Image

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
ROOT = Path(__file__).resolve().parents[1]


def extract(source: Path) -> None:
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    with ZipFile(source) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        size = presentation.find("p:sldSz", NS)
        width, height = int(size.get("cx")), int(size.get("cy"))
        if (width, height) != (9144000, 6858000):
            raise ValueError("Expected the original SYSU 4:3 template canvas")

        original_images = {}
        for member, target in (
            ("ppt/media/image1.png", "sysu-logo-green.png"),
            ("ppt/media/image3.png", "sysu-logo-white.png"),
        ):
            data = archive.read(member)
            (assets / target).write_bytes(data)
            original_images[target] = {
                "member": member,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        # Original cover srcRect right crop: 71.25% of the 1053 px logo.
        with Image.open(io.BytesIO(archive.read("ppt/media/image1.png"))) as logo:
            seal_width = round(logo.width * (1 - 0.7125))
            logo.crop((0, 0, seal_width, logo.height)).save(assets / "sysu-seal.png")

        layout = ET.fromstring(archive.read("ppt/slideLayouts/slideLayout1.xml"))
        group = layout.find("p:cSld/p:spTree/p:grpSp", NS)
        transform = group.find("p:grpSpPr/a:xfrm", NS)
        off = transform.find("a:off", NS)
        ext = transform.find("a:ext", NS)
        child_off = transform.find("a:chOff", NS)
        child_ext = transform.find("a:chExt", NS)
        gx, gy = int(off.get("x")), int(off.get("y"))
        gw, gh = int(ext.get("cx")), int(ext.get("cy"))
        cx, cy = int(child_off.get("x")), int(child_off.get("y"))
        cw, ch = int(child_ext.get("cx")), int(child_ext.get("cy"))

        output = [
            "% Extracted from ppt/slideLayouts/slideLayout1.xml, Group 433.",
            "% Native paths in normalized slide coordinates; edit SYSUMap for color.",
        ]
        path_count = 0
        for shape in group.findall("p:sp", NS):
            xf = shape.find("p:spPr/a:xfrm", NS)
            so, se = xf.find("a:off", NS), xf.find("a:ext", NS)
            sx, sy = int(so.get("x")), int(so.get("y"))
            sw, sh = int(se.get("cx")), int(se.get("cy"))
            for path in shape.findall("p:spPr/a:custGeom/a:pathLst/a:path", NS):
                # Several tiny horizontal paths omit h because it is zero.
                # They enclose no area and have no stroke in the original.
                pw, ph = float(path.get("w", 0)), float(path.get("h", 0))
                if pw == 0 or ph == 0:
                    continue
                parts = [r"\path[fill=SYSUMap,draw=none]"]
                for command in path:
                    tag = command.tag.rsplit("}", 1)[-1]
                    if tag == "close":
                        parts.append("-- cycle")
                        continue
                    if tag not in ("moveTo", "lnTo"):
                        raise ValueError(f"Unsupported source path command: {tag}")
                    point = command.find("a:pt", NS)
                    px, py = float(point.get("x")), float(point.get("y"))
                    x = (gx + (sx + px * sw / pw - cx) * gw / cw) / width
                    y = (gy + (sy + py * sh / ph - cy) * gh / ch) / height
                    prefix = "" if tag == "moveTo" else "-- "
                    parts.append(f"{prefix}({x:.8f},{y:.8f})")
                output.append("\n  ".join(parts) + ";")
                path_count += 1
        (assets / "world-map.tikz").write_text("\n".join(output) + "\n", encoding="utf-8")

        provenance = {
            "source": source.name,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "slide_size_emu": [width, height],
            "source_slide_count": len(presentation.find("p:sldIdLst", NS)),
            "used_layouts": [1, 3, 4, 5, 8, 10, 11],
            "images": original_images,
            "seal_crop_right_percent": 71.25,
            "map_path_count": path_count,
            "colors": {"green": "005825", "accent": "008E3D", "map": "F2F2F2"},
        }
        (assets / "provenance.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Extracted {path_count} map paths and original logos to {assets}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to the original SYSU PPT template")
    extract(parser.parse_args().source)
