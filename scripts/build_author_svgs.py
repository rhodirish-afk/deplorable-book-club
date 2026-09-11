#!/usr/bin/env python3
import base64, pathlib, io
from PIL import Image
for stem in ("kevin-myers", "william-matchett"):
    base = pathlib.Path(f"assets/authors/{stem}.jpg.b64")
    extras = sorted(pathlib.Path("assets/authors").glob(f"{stem}.jpg.b64.part*"))
    if not base.exists() and not extras:
        print("skip", stem)
        continue
    chunks = []
    if base.exists():
        chunks.append(base.read_text().strip())
    for p in extras:
        chunks.append(p.read_text().strip())
        print(" +", p.name, len(chunks[-1]))
    b64 = "".join(chunks)
    if not b64:
        continue
    base.write_text(b64 + "\n")
    print("assembled", base, len(b64))
    raw = base64.b64decode(b64)
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = im.size
    enc = base64.b64encode(raw).decode()
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f'  <image width="{w}" height="{h}" xlink:href="data:image/jpeg;base64,{enc}"/>\n'
        '</svg>\n'
    )
    out = pathlib.Path(f"assets/authors/{stem}.svg")
    out.write_text(svg)
    print("wrote", out, out.stat().st_size)
