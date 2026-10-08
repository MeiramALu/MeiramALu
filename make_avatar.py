"""Генерирует аватар assets/avatar.png в стиле шапки профиля (монограмма MS)."""
import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 1000
NAVY, INDIGO, TEAL = (11, 17, 32), (49, 46, 129), (19, 78, 94)
SKY, VIOLET = (56, 189, 248), (167, 139, 250)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def background():
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S)
            px[x, y] = lerp(NAVY, INDIGO, t * 2) if t < .5 else lerp(INDIGO, TEAL, (t - .5) * 2)
    return img


def gradient_mask_fill(size, mask):
    grad = Image.new("RGB", size)
    d = ImageDraw.Draw(grad)
    for x in range(size[0]):
        d.line([(x, 0), (x, size[1])], fill=lerp(SKY, VIOLET, x / size[0]))
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(grad, mask=mask)
    return out


def main():
    img = background().convert("RGBA")
    c = S // 2

    rings = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(rings)
    r1, r2 = 360, 290
    for a in range(0, 360, 9):  # пунктирное внешнее кольцо
        d.arc([c - r1, c - r1, c + r1, c + r1], a, a + 5, fill=SKY + (180,), width=6)
    d.ellipse([c - r2, c - r2, c + r2, c + r2], outline=VIOLET + (110,), width=3)
    for r, ang, col, rad in [(r1, -35, VIOLET, 18), (r2, 140, SKY, 13)]:
        x, y = c + r * math.cos(math.radians(ang)), c + r * math.sin(math.radians(ang))
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col + (255,))
    glow = rings.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, rings)

    font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 300)
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.text((c, c + 10), "MS", font=font, fill=255, anchor="mm")
    letters = gradient_mask_fill((S, S), mask)
    img = Image.alpha_composite(img, letters.filter(ImageFilter.GaussianBlur(14)))
    img = Image.alpha_composite(img, letters)

    img.convert("RGB").save("assets/avatar.png", optimize=True)


if __name__ == "__main__":
    main()
