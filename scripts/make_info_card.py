import os
import sys

def generate_info_card(output_svg="info-card.svg", username="Prasadhol2001"):
    is_static = os.environ.get("STATIC") == "1"
    
    width = 490
    height = 490
    
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Styles & Animations
    lines.append('<defs>')
    lines.append('  <style>')
    lines.append('    .card-bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #30363d; stroke-width: 1px; }')
    lines.append('    .header-dot { rx: 50%; ry: 50%; }')
    lines.append('    .title-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    lines.append('    .term-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; }')
    lines.append('    .user-title { fill: #58a6ff; font-weight: bold; font-size: 15px; }')
    lines.append('    .host-title { fill: #bc8cff; font-weight: bold; font-size: 15px; }')
    lines.append('    .separator { stroke: #30363d; stroke-width: 1px; }')
    lines.append('    .key { fill: #79c0ff; font-weight: 600; }')
    lines.append('    .val { fill: #c9d1d9; }')
    lines.append('    .val-highlight { fill: #7ee787; font-weight: 500; }')
    lines.append('    .prompt { fill: #d2a8ff; font-weight: bold; }')
    
    if not is_static:
        lines.append('    .fade-line { opacity: 0; transform: translateY(6px); animation: fadeIn 0.4s ease-out forwards; }')
        lines.append('    @keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }')
        
    lines.append('  </style>')
    lines.append('</defs>')
    
    # Card Backdrop
    lines.append(f'<rect class="card-bg" width="{width}" height="{height}" />')
    
    # Window Header
    lines.append('<circle class="header-dot" cx="20" cy="18" r="5" fill="#ff5f56" />')
    lines.append('<circle class="header-dot" cx="35" cy="18" r="5" fill="#ffbd2e" />')
    svg_header_dot = '<circle class="header-dot" cx="50" cy="18" r="5" fill="#27c93f" />'
    lines.append(svg_header_dot)
    lines.append(f'<text class="title-text" x="{width // 2}" y="22" text-anchor="middle">neofetch --user {username}</text>')
    lines.append(f'<line x1="0" y1="32" x2="{width}" y2="32" stroke="#21262d" stroke-width="1" />')
    
    # Info Data Rows
    info_rows = [
        ("HEADER", f'<tspan class="user-title">{username}</tspan><tspan class="val">@</tspan><tspan class="host-title">github</tspan>'),
        ("SEP", "------------------------------------------"),
        ("KEYVAL", "OS", "GitHub Profile Linux x86_64"),
        ("KEYVAL", "Host", "Cloud Engine v2.4"),
        ("KEYVAL", "Kernel", "5.15.0-profile-generic"),
        ("KEYVAL", "Uptime", "365 days, 24 mins"),
        ("KEYVAL", "Shell", "zsh 5.9 (x86_64-apple-darwin22.0)"),
        ("KEYVAL", "Role", "Full-Stack Software Engineer"),
        ("KEYVAL", "Focus", "Web Architecture, APIs, DevTools"),
        ("KEYVAL", "Stack", "Python, TypeScript, React, Node.js, C++"),
        ("KEYVAL", "Editor", "VS Code / Antigravity IDE"),
        ("KEYVAL", "Terminal", "Kitty / iTerm2 / Windows Terminal"),
        ("KEYVAL", "Status", "Building awesome open-source software 🚀"),
        ("COLORS", None)
    ]
    
    start_x = 24
    start_y = 62
    row_height = 24
    
    for i, row in enumerate(info_rows):
        y_pos = start_y + (i * row_height)
        delay = 0.1 + (i * 0.08)
        anim_attr = f' class="fade-line" style="animation-delay: {delay:.2f}s;"' if not is_static else ''
        
        row_type = row[0]
        if row_type == "HEADER":
            lines.append(f'<g{anim_attr}>')
            lines.append(f'  <text class="term-text" x="{start_x}" y="{y_pos}">{row[1]}</text>')
            lines.append('</g>')
        elif row_type == "SEP":
            lines.append(f'<g{anim_attr}>')
            lines.append(f'  <line x1="{start_x}" y1="{y_pos - 6}" x2="{width - start_x}" y2="{y_pos - 6}" class="separator" />')
            lines.append('</g>')
        elif row_type == "KEYVAL":
            key, val = row[1], row[2]
            lines.append(f'<g{anim_attr}>')
            lines.append(f'  <text class="term-text" x="{start_x}" y="{y_pos}">')
            lines.append(f'    <tspan class="key">{key}:</tspan>&#160;&#160;<tspan class="val">{val}</tspan>')
            lines.append('  </text>')
            lines.append('</g>')
        elif row_type == "COLORS":
            # Color block palette
            colors = ["#484f58", "#ff7b72", "#7ee787", "#f2cc60", "#79c0ff", "#d2a8ff", "#a5d6ff", "#f0f6fc"]
            lines.append(f'<g{anim_attr}>')
            block_y = y_pos - 8
            for c_idx, color in enumerate(colors):
                bx = start_x + (c_idx * 24)
                lines.append(f'  <rect x="{bx}" y="{block_y}" width="20" height="14" rx="3" fill="{color}" />')
            lines.append('</g>')
            
    lines.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Generated Info Card SVG '{output_svg}'.")

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "Prasadhol2001"
    generate_info_card("info-card.svg", user)
