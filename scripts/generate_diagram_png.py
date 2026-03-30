from __future__ import annotations

from pathlib import Path


def main() -> None:
    out_path = Path(__file__).resolve().parents[1] / "diagram.png"

    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch
    except Exception:
        plt = None
        FancyBboxPatch = None

    # Simple diagram generator.
    # Prefer matplotlib for nicer layout, but fall back to Pillow so it always works.
    if plt is None:
        _render_with_pillow(out_path)
        print(f"Wrote {out_path}")
        return

    fig_w, fig_h = 14, 3.4
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_axis_off()

    labels = [
        "Data Sources",
        "Knowledge Base",
        "Retrieval (RAG)",
        "Domain-Adapted Model",
        "AI Agent (Tools)",
        "Snowflake",
        "Streamlit App",
        "Evaluation + Logs",
    ]

    x_positions = [0.02, 0.15, 0.28, 0.43, 0.58, 0.70, 0.82, 0.93]
    y = 0.55
    box_w, box_h = 0.12, 0.22

    for x, label in zip(x_positions, labels):
        box = FancyBboxPatch(
            (x - box_w / 2, y - box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            linewidth=1.5,
            edgecolor="#2b2b2b",
            facecolor="#f5f7ff",
        )
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=10, wrap=True)

    # Arrows
    for i in range(len(x_positions) - 1):
        ax.annotate(
            "",
            xy=(x_positions[i + 1] - box_w / 2, y),
            xytext=(x_positions[i] + box_w / 2, y),
            arrowprops=dict(arrowstyle="->", lw=1.8, color="#2b2b2b"),
        )

    ax.text(
        0.5,
        0.15,
        "Integrated end-to-end pipeline (Project 3)",
        ha="center",
        va="center",
        fontsize=11,
        color="#2b2b2b",
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

    print(f"Wrote {out_path}")


def _render_with_pillow(out_path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    width, height = 2200, 520
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Try a default font; pillow will fall back if not available.
    try:
        font = ImageFont.truetype("Arial.ttf", 26)
        small_font = ImageFont.truetype("Arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    labels = [
        "Data Sources",
        "Knowledge Base",
        "Retrieval (RAG)",
        "Domain-Adapted Model",
        "AI Agent (Tools)",
        "Snowflake",
        "Streamlit App",
        "Evaluation + Logs",
    ]

    margin_x = 70
    box_w = 240
    box_h = 120
    gap = 40
    y = 180
    x = margin_x

    def draw_box(x0: int, y0: int, text: str) -> None:
        x1, y1 = x0 + box_w, y0 + box_h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=18, outline=(40, 40, 40), width=3, fill=(245, 247, 255))
        # Center text
        text_w, text_h = draw.textbbox((0, 0), text, font=small_font)[2:]
        draw.text((x0 + (box_w - text_w) / 2, y0 + (box_h - text_h) / 2), text, fill=(30, 30, 30), font=small_font)

    # Draw boxes + arrows
    centers = []
    for label in labels:
        draw_box(x, y, label)
        centers.append((x + box_w // 2, y + box_h // 2))
        x += box_w + gap

    for (x0, y0), (x1, y1) in zip(centers, centers[1:]):
        start = (x0 + box_w // 2, y0)
        end = (x1 - box_w // 2, y1)
        draw.line([start, end], fill=(40, 40, 40), width=4)
        # Arrow head
        arrow_size = 12
        draw.polygon(
            [
                (end[0], end[1]),
                (end[0] - arrow_size, end[1] - arrow_size // 2),
                (end[0] - arrow_size, end[1] + arrow_size // 2),
            ],
            fill=(40, 40, 40),
        )

    title = "Integrated end-to-end pipeline (Project 3)"
    title_w, title_h = draw.textbbox((0, 0), title, font=font)[2:]
    draw.text(((width - title_w) / 2, 60), title, fill=(20, 20, 20), font=font)

    img.save(out_path)


if __name__ == "__main__":
    main()
