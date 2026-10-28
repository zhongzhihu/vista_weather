#!/usr/bin/env python3
"""Encode the existing satellite/cloud composite as WebP; retain its original colors.

The source JPEG already resembles the app's onboarding image. Requires Pillow.
"""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / 'public/satellite-hero-20261009.jpg'
target = root / 'public/satellite-hero-20261009.webp'
with Image.open(source) as image:
    image.convert('RGB').save(target, 'WEBP', quality=80, method=6)
print(f'{source.name}: {source.stat().st_size:,} bytes -> {target.name}: {target.stat().st_size:,} bytes')
