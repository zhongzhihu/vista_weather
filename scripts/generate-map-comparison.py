#!/usr/bin/env python3
"""Generate the website map comparison from VistaScreenshots exports."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path.home() / 'VistaScreenshots'
EXPORT = SOURCE / 'Export/Map Resolution Screenshots No Annotations'
RESOURCES = SOURCE / 'Sources/VistaScreenshots/Resources'
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W, H = 1740, 1110

def load_heic(name):
    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
        subprocess.run(['sips', '-s', 'format', 'png', str(RESOURCES / name), '--out', tmp.name], stdout=subprocess.DEVNULL, check=True)
        return Image.open(tmp.name).convert('RGBA')

def rounded_paste(canvas, image, box, radius):
    x, y, w, h = box
    image = image.resize((w, h), Image.Resampling.LANCZOS)
    mask = Image.new('L', (w, h)); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w-1, h-1), radius, fill=255)
    canvas.paste(image, (x, y), mask)

def phone(canvas, image, x):
    # Match the feature mockups: the same photographed frame, screen inset,
    # rounded corners, and edge fade used by .phone-case-feature.
    y, h = 5, 1074
    w = round(h * 415 / 840)
    x = round(x + (494 - w) / 2)
    shadow = Image.new('RGBA', (W, H))
    ImageDraw.Draw(shadow).rounded_rectangle((x + 12, y + 12, x + w - 12, y + h + 12), 65, fill=(22, 32, 42, 75))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))
    rounded_paste(canvas, image, (x + round(w * .0506024), y + round(h * .0214286), round(w * .8939759), round(h * .9547619)), round(w * .8939759 * .1455526))
    frame = Image.open(ROOT / 'src/assets/postspark-phone-frame.png').convert('RGBA').resize((w, h), Image.Resampling.LANCZOS)
    alpha = frame.getchannel('A')
    fade = Image.new('L', (w, 1))
    for px in range(w):
        pos = (px + .5) / w * 100
        opacity = min(1, max(0, (pos - .8) / 1.1), max(0, (98.959 - pos) / 1.1))
        fade.putpixel((px, 0), round(opacity * 255))
    from PIL import ImageChops
    frame.putalpha(ImageChops.multiply(alpha, fade.resize((w, h))))
    canvas.alpha_composite(frame, (x, y))

def lens(canvas, source, x, y, coarse, fahrenheit):
    size = 360
    # The native zoom covers about 8% less map than the coarse source.
    # Align the two captures using their shared Elko and temperature landmarks.
    if coarse:
        source = source.crop((49, 51, 782, 779))
    crop = source.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new('L', (size, size)); md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, size-1, size-1), fill=255)
    shadow = Image.new('RGBA', (W, H)); shadow.paste((30, 38, 45, 80), (x, y+9, x+size, y+size+9), mask)
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    canvas.paste(crop, (x, y), mask)
    d = ImageDraw.Draw(canvas)
    d.ellipse((x, y, x+size, y+size), outline='white', width=5)
    # Match the orientation label used in the onboarding map.
    city_font = ImageFont.truetype(str(ROOT / 'scripts/fonts/NotoSans.ttf'), 15)
    city_font.set_variation_by_name('Bold')
    city_position = (x + int(.692 * size), y + int(.116 * size))
    city_shadow = Image.new('RGBA', (W, H))
    ImageDraw.Draw(city_shadow).text(city_position, 'Elko', font=city_font, fill=(0, 0, 0, 220), stroke_width=1, anchor='mm')
    canvas.alpha_composite(city_shadow.filter(ImageFilter.GaussianBlur(0.6)))
    d = ImageDraw.Draw(canvas)
    d.text(city_position, 'Elko', font=city_font, fill='#f7f7f7', anchor='mm')
    # The three values are from VistaWeather's MapsOnboardingView.
    vals = [24, 39.1, 38] if coarse else [9, 48.6, 40.6]
    # Tips mark the same locations as the onboarding view. Sierra Nevada and
    # Las Vegas sit above their points; Death Valley sits below its point.
    spots = [(0.423, 0.547, False, -25), (0.594, 0.651, True, 0),
             (0.767, 0.667, False, -4)]
    for (name, value), (px, py, below, shift) in zip(zip(['Sierra Nevada', 'Death Valley', 'Las Vegas'], vals), spots):
        value = value * 9 / 5 + 32 if fahrenheit else value
        temp = f'{value:.0f}°' + ('F' if fahrenheit else 'C')
        small = ImageFont.truetype(FONT, 18); large = ImageFont.truetype(FONT, 29)
        width = max(d.textbbox((0,0), name, font=small)[2], d.textbbox((0,0), temp, font=large)[2]) + 22
        point_x, point_y = x + int(px*size), y + int(py*size)
        cx = point_x + shift
        left = int(cx-width/2)
        top = point_y + 9 if below else point_y - 71
        fill = (63, 19, 21, 235)
        if below:
            d.polygon([(point_x, point_y), (point_x-9, top+1), (point_x+9, top+1)], fill=fill)
        else:
            d.polygon([(point_x, point_y), (point_x-9, top+61), (point_x+9, top+61)], fill=fill)
        d.rounded_rectangle((left, top, left+width, top+62), 10, fill=fill)
        d.text((cx, top+7), name, font=small, fill='#f5e9e6', anchor='mt')
        d.text((cx, top+27), temp, font=large, fill='white', anchor='mt')

native = Image.open(EXPORT / 'maps_onboarding_with_island_native.png').convert('RGBA')
coarse = Image.open(EXPORT / 'maps_onboarding_with_island_75km.png').convert('RGBA')
zoom = load_heic('maps_onboarding_zoom.heic'); coarse_zoom = load_heic('maps_onboarding_coarse.heic')
for fahrenheit in (False, True):
    canvas = Image.new('RGBA', (W, H))
    phone(canvas, native, 339); phone(canvas, coarse, 907)
    lens(canvas, zoom, 20, 455, False, fahrenheit); lens(canvas, coarse_zoom, 1360, 455, True, fahrenheit)
    unit = 'fahrenheit' if fahrenheit else 'celsius'
    name = f'vista-weather-map-screen-comparison-{unit}'
    canvas.save(ROOT / 'public/press' / (name + '.png'), optimize=True)
    canvas.save(ROOT / 'public/images' / (name + '.webp'), 'WEBP', quality=90, method=6)

# Export independent transparent layers so each phone and detail can be saved.
def export_part(name, draw, bounds):
    layer = Image.new('RGBA', (W, H))
    draw(layer)
    part = layer.crop(bounds)
    part.save(ROOT / 'public/press' / f'vista-weather-{name}.png', optimize=True)
    part.save(ROOT / 'public/images' / f'vista-weather-{name}.webp', 'WEBP', quality=90, method=6)

export_part('map-native-phone', lambda c: phone(c, native, 339), (300, 0, 875, 1110))
export_part('map-75km-phone', lambda c: phone(c, coarse, 907), (868, 0, 1443, 1110))
for fahrenheit in (False, True):
    unit = 'fahrenheit' if fahrenheit else 'celsius'
    export_part(f'map-native-detail-{unit}', lambda c: lens(c, zoom, 20, 455, False, fahrenheit), (0, 430, 405, 850))
    export_part(f'map-75km-detail-{unit}', lambda c: lens(c, coarse_zoom, 1360, 455, True, fahrenheit), (1340, 430, 1740, 850))
