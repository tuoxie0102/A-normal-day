#!/usr/bin/env python3
"""
Round 8 · Character PNG batch cleanup

Goals (from user requirements):
- Strip residual white fringe / halo
- Soften aliasing on alpha edge
- Gentle alpha feather (1-2px max)
- Remove white-fringe color contamination
- KEEP transparent PNG (RGBA)
- DO NOT change aspect ratio
- DO NOT downgrade clarity / resolution

Pipeline per file:
  1. Load as RGBA
  2. Alpha noise floor — pixels with alpha < 6 become fully transparent
  3. White Fringe decontamination — only on semi-transparent + bright pixels,
     reverse the over-white compositing equation:
       rendered = C * a + 255 * (1 - a)   =>   C = (rendered - 255*(1-a)) / a
     This recovers the original (uncomposited) color, which removes the
     telltale white halo seen around AI-generated cutout PNGs.
  4. Alpha edge softening — gaussian blur (radius 0.55) on alpha channel only
     and a gentle s-curve to tighten the result, so we get clean anti-aliased
     edges without softening the interior of the figure.
  5. Save as optimized PNG.

What we DO NOT do:
- Resample / resize (preserves all original pixels)
- Crop or pad (preserves bbox)
- Touch RGB of fully-opaque interior pixels (preserves art)
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def clean_png(path_in: Path, path_out: Path):
    img = Image.open(path_in)
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    arr = np.array(img).astype(np.float32)
    rgb = arr[..., :3].copy()
    a = arr[..., 3].copy()
    h, w = a.shape
    orig_w, orig_h = img.size

    # 1) Alpha noise floor — kill near-transparent ghost pixels
    near_zero = a < 6
    a[near_zero] = 0
    # zero out their RGB too so they can't bleed during scaling
    rgb[near_zero] = 0

    # 2) White-fringe decontamination
    # Only on edge pixels: partial alpha AND visibly bright (likely white-composited)
    a_f = a / 255.0
    semi = (a > 0) & (a < 230)
    bright = (rgb[..., 0] > 215) & (rgb[..., 1] > 215) & (rgb[..., 2] > 215)
    fringe_mask = semi & bright

    fringe_count = int(fringe_mask.sum())
    if fringe_mask.any():
        # Unpremul against white background
        a_f_safe = np.maximum(a_f[fringe_mask], 0.04)  # avoid div by ~0
        rendered = rgb[fringe_mask]
        bg = 255.0 * (1.0 - a_f_safe[..., None])
        recovered = (rendered - bg) / a_f_safe[..., None]
        rgb[fringe_mask] = np.clip(recovered, 0, 255)

    # 3) Alpha edge softening + tightening curve
    a_uint8 = np.clip(a, 0, 255).astype(np.uint8)
    a_img = Image.fromarray(a_uint8, "L")
    a_img = a_img.filter(ImageFilter.GaussianBlur(radius=0.55))
    a_np = np.array(a_img).astype(np.float32)
    # Gentle s-curve to tighten alpha: push <8 to 0, lift 8-255 by 1.06x then clamp
    # Effect: anti-aliased edges stay smooth, half-transparent "veil" pixels
    # along the contour either commit to opaque or vanish.
    a_np = np.where(a_np < 8, 0, a_np * 1.06 - 4)
    a_final = np.clip(a_np, 0, 255).astype(np.uint8)

    # 4) Recompose
    rgb_final = np.clip(rgb, 0, 255).astype(np.uint8)
    out_arr = np.dstack([rgb_final, a_final])
    out_img = Image.fromarray(out_arr, "RGBA")
    out_img.save(path_out, "PNG", optimize=True)

    # Sanity check: dimensions preserved
    assert out_img.size == (orig_w, orig_h), (
        f"DIMENSION CHANGED for {path_in.name}: {(orig_w,orig_h)} -> {out_img.size}"
    )

    return {
        "name": path_in.name,
        "size": (orig_w, orig_h),
        "fringe_pixels_decontaminated": fringe_count,
        "bytes_before": path_in.stat().st_size,
        "bytes_after": path_out.stat().st_size,
    }


def main():
    project = Path(
        "D:/01_Projects_项目/2026 个人知识库 飞书录音/糕糕知识库/像男人一样相亲"
    )
    gen = project / "generated_characters"
    assets = project / "assets" / "characters"

    files = sorted(gen.glob("*.png"))
    assert files, "No PNG files found"

    print(f"Found {len(files)} PNGs in generated_characters/")
    print(f"Will mirror to assets/characters/ after processing\n")

    results = []
    for f in files:
        bak = f.with_suffix(".png.bak")
        if not bak.exists():
            # Make a one-time .bak preserving the original
            bak.write_bytes(f.read_bytes())

        # Process in-place: read from .bak, write to .png
        result = clean_png(bak, f)
        results.append(result)
        delta = result["bytes_after"] - result["bytes_before"]
        sign = "+" if delta >= 0 else ""
        print(
            f"  ✓ {result['name']:<32} "
            f"{result['size'][0]:>5}×{result['size'][1]:<5}  "
            f"fringe={result['fringe_pixels_decontaminated']:>7}  "
            f"size {result['bytes_before']:>8}→{result['bytes_after']:<8} ({sign}{delta})"
        )

    print(f"\nSyncing to assets/characters/ ...")
    for f in files:
        target = assets / f.name
        target.write_bytes(f.read_bytes())
        print(f"  ✓ assets/characters/{f.name}")

    print(f"\n✅ Done. {len(files)} files processed. Originals preserved as *.png.bak in generated_characters/")


if __name__ == "__main__":
    main()
