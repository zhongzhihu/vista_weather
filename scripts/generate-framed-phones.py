#!/usr/bin/env python3
"""Build website-only phone composites from the original screenshots and frame."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops

root = Path(__file__).resolve().parents[1]
slugs = ['eden-prairie-minute-by-minute-rain-forecast', 'eden-prairie-minute-by-minute-rain-forecast-fahrenheit', 'united-states-live-rain-radar-lightning', 'europe-live-rain-radar-lightning', '30-day-weather-forecast-celsius', '30-day-weather-forecast-fahrenheit', 'paris-possible-temperature-outcomes-en-gb', 'paris-possible-temperature-outcomes-en-us', 'forecast-comparison-celsius', 'forecast-comparison-fahrenheit', 'aurora-forecast-europe', 'aurora-forecast-anz', 'aurora-forecast-north-america', 'aurora-basic-advanced-space-weather-conditions', 'storm-tracking-map-with-fires']
w, h = 1245, 2520
frame = Image.open(root / 'src/assets/postspark-phone-frame.png').convert('RGBA').resize((w, h), Image.Resampling.LANCZOS)
fade = Image.new('L', (w, 1))
for x in range(w):
    pos = (x + .5) / w * 100
    fade.putpixel((x, 0), round(255 * min(1, max(0, (pos - .8) / 1.1), max(0, (98.959 - pos) / 1.1))))
frame.putalpha(ImageChops.multiply(frame.getchannel('A'), fade.resize((w, h))))
for slug in slugs:
    src = root / 'public/images' / f'vista-weather-{slug}.webp'
    image = Image.open(src).convert('RGBA')
    sw, sh = round(w * .8939759), round(h * .9547619)
    image = image.resize((sw, sh), Image.Resampling.LANCZOS)
    mask = Image.new('L', (sw, sh))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw-1, sh-1), radius=round(sw * .1455526), fill=255)
    out = Image.new('RGBA', (w, h))
    out.paste(image, (round(w*.0506024), round(h*.0214286)), mask)
    out.alpha_composite(frame)
    out.save(root / 'public/images' / f'vista-weather-{slug}-framed.webp', 'WEBP', quality=92, method=6)
    out.save(root / 'public/press' / f'vista-weather-{slug}-framed.png', optimize=True)
