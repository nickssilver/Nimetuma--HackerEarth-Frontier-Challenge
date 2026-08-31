"""Build the 16:9 cover and a short PDF for the HackerEarth form."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W, H = 1280, 720
BG = (18, 18, 18)
INK = (245, 243, 238)
MUTED = (168, 166, 160)
ACCENT = (214, 122, 62)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    bold_names = (
        "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    )
    for path in bold_names if bold else names:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def slide(lines: list[tuple[str, int, bool, tuple[int, int, int]]]) -> Image.Image:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 8, H), fill=ACCENT)
    y = 88
    for text, size, bold, color in lines:
        draw.text((72, y), text, font=font(size, bold=bold), fill=color)
        y += size + 18
    return image


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    cover = slide(
        [
            ("NIMETUMA", 64, True, INK),
            ("Did the money actually land?", 36, False, MUTED),
            ("Baseline 3/10  ·  Final 10/10  ·  False paid 0", 28, False, ACCENT),
            ("Till-first agent for Kenyan sellers. Amina still decides.", 24, False, MUTED),
        ]
    )
    cover.save(ASSETS / "cover.png", "PNG")

    pages = [
        slide(
            [
                ("NIMETUMA", 56, True, INK),
                ("Did the money actually land?", 32, False, MUTED),
                ("micro1 Frontier Engineering Challenge 2026", 24, False, MUTED),
                ("Synthetic M-Pesa. No keys. No live money.", 24, False, ACCENT),
            ]
        ),
        slide(
            [
                ("The user", 28, True, ACCENT),
                ("Amina. WhatsApp shop. Till 892341.", 36, True, INK),
                ("Customer: Bro nimetuma + screenshot.", 28, False, MUTED),
                ("Rider is downstairs. She has ten seconds.", 28, False, MUTED),
            ]
        ),
        slide(
            [
                ("The agent", 28, True, ACCENT),
                ("Screenshot is never evidence.", 36, True, INK),
                ("Only a matching till row is paid.", 28, False, MUTED),
                ("Reply in Sheng / Kiswahili / English.", 28, False, MUTED),
                ("Human checkpoint before release.", 28, False, MUTED),
            ]
        ),
        slide(
            [
                ("Measured improvement", 28, True, ACCENT),
                ("Same 10 cases every stage.", 32, True, INK),
                ("Baseline          3/10 correct   7 false paid", 28, False, MUTED),
                ("Screenshot trust  7/10           3 false paid", 28, False, MUTED),
                ("Fluent trust      9/10           1 false paid  (removed)", 28, False, MUTED),
                ("Final agent      10/10           0 false paid", 28, False, ACCENT),
            ]
        ),
        slide(
            [
                ("Hot take", 28, True, ACCENT),
                ("Sheng made the agent easier to con.", 36, True, INK),
                ("Language comfort is a risk until the till moves.", 26, False, MUTED),
                ("python -m nimetuma eval     10/10 in under 2s", 26, False, INK),
            ]
        ),
    ]
    pages[0].save(
        ASSETS / "Nimetuma-presentation.pdf",
        save_all=True,
        append_images=pages[1:],
    )
    print(f"wrote {ASSETS / 'cover.png'}")
    print(f"wrote {ASSETS / 'Nimetuma-presentation.pdf'}")


if __name__ == "__main__":
    main()
