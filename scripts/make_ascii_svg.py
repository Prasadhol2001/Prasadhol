import os
import sys
import html
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (index 0 = space) -> Dark (dense glyphs)

def image_to_ascii_grid(image_path="source-prepped.png", cols=100, aspect_ratio=0.5):
    if not os.path.exists(image_path):
        if os.path.exists("source-photo.jpg"):
            image_path = "source-photo.jpg"
        else:
            raise FileNotFoundError(f"Neither 'source-prepped.png' nor 'source-photo.jpg' was found.")

    img = Image.open(image_path).convert("L")
    img_w, img_h = img.size
    rows = int((img_h / img_w) * cols * aspect_ratio)
    
    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
    
    grid = []
    ramp_len = len(RAMP)
    
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            val = img_resized.getpixel((c, r))
            idx = int((255 - val) / 255.0 * (ramp_len - 1))
            idx = max(0, min(ramp_len - 1, idx))
            char = RAMP[idx]
            row_chars.append(char)
        grid.append("".join(row_chars))
        
    return grid

def generate_ascii_svg(grid, output_svg="avi-ascii.svg"):
    cols = len(grid[0])
    rows = len(grid)
    
    # SVG canvas sizing
    font_size = 7
    char_width = 3.6
    line_height = 8.5
    
    padding_x = 12
    padding_y = 35
    
    svg_width = 370
    svg_height = 490
    
    # Typing animation durations
    total_duration = 3.5  # seconds for entire portrait print
    row_duration = total_duration / rows
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    
    # CSS Styles & SMIL Clip definitions
    svg_lines.append('<defs>')
    svg_lines.append('  <style>')
    svg_lines.append('    .bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #30363d; stroke-width: 1px; }')
    svg_lines.append('    .ascii-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 7px; fill: #8b949e; xml-space: preserve; }')
    svg_lines.append('    .header-dot { rx: 50%; ry: 50%; }')
    svg_lines.append('    .title-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('    .cursor { fill: #58a6ff; }')
    svg_lines.append('  </style>')
    
    # Clip paths for row-by-row typing
    for r in range(rows):
        clip_id = f"clip-row-{r}"
        svg_lines.append(f'  <clipPath id="{clip_id}">')
        svg_lines.append(f'    <rect x="0" y="0" width="0" height="{svg_height}">')
        begin_time = r * row_duration
        dur = max(0.04, row_duration * 0.9)
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{svg_width}" begin="{begin_time:.3f}s" dur="{dur:.3f}s" fill="freeze" />')
        svg_lines.append('    </rect>')
        svg_lines.append('  </clipPath>')
    svg_lines.append('</defs>')
    
    # Background card
    svg_lines.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" />')
    
    # Terminal Header Bar
    svg_lines.append('<circle class="header-dot" cx="20" cy="18" r="5" fill="#ff5f56" />')
    svg_lines.append('<circle class="header-dot" cx="35" cy="18" r="5" fill="#ffbd2e" />')
    svg_lines.append('<circle class="header-dot" cx="50" cy="18" r="5" fill="#27c93f" />')
    svg_lines.append(f'<text class="title-text" x="{svg_width // 2}" y="22" text-anchor="middle">portrait.ascii</text>')
    svg_lines.append('<line x1="0" y1="32" x2="370" y2="32" stroke="#21262d" stroke-width="1" />')
    
    # Render ASCII rows
    start_y = padding_y + 12
    
    for r, line_text in enumerate(grid):
        y_pos = start_y + (r * line_height)
        escaped_text = html.escape(line_text).replace(' ', '&#160;')
        clip_id = f"clip-row-{r}"
        
        # Row group with clip wipe
        svg_lines.append(f'<g clip-path="url(#{clip_id})">')
        svg_lines.append(f'  <text class="ascii-text" x="{padding_x}" y="{y_pos:.1f}" xml:space="preserve">{escaped_text}</text>')
        svg_lines.append('</g>')
        
    svg_lines.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Generated ASCII SVG '{output_svg}' with {rows} rows x {cols} cols.")

if __name__ == "__main__":
    img_file = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "avi-ascii.svg"
    grid = image_to_ascii_grid(img_file, cols=96, aspect_ratio=0.48)
    generate_ascii_svg(grid, out_file)
