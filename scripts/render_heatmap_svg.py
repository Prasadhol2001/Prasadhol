import os
import sys
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap_svg(input_json="data/contributions.json", output_svg="contrib-heatmap.svg"):
    if not os.path.exists(input_json):
        raise FileNotFoundError(f"Input JSON '{input_json}' not found. Run fetch_contributions.py first.")
        
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    username = data.get("username", "Prasadhol2001")
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    days = data.get("days", [])
    
    # SVG Dimensions
    width = 860
    height = 230
    
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    lines.append('<defs>')
    lines.append('  <style>')
    lines.append('    .card-bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #30363d; stroke-width: 1px; }')
    lines.append('    .header-dot { rx: 50%; ry: 50%; }')
    lines.append('    .title-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    lines.append('    .label-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; fill: #7d8590; }')
    lines.append('    .stat-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #c9d1d9; }')
    lines.append('    .stat-bold { font-weight: bold; fill: #39d353; }')
    lines.append('    .day-rect { rx: 2.5px; ry: 2.5px; opacity: 0; transform: translateY(-6px); animation: slideIn 0.3s ease-out forwards; }')
    lines.append('    @keyframes slideIn { to { opacity: 1; transform: translateY(0); } }')
    lines.append('  </style>')
    lines.append('</defs>')
    
    # Background
    lines.append(f'<rect class="card-bg" width="{width}" height="{height}" />')
    
    # Header Bar
    lines.append('<circle class="header-dot" cx="20" cy="18" r="5" fill="#ff5f56" />')
    lines.append('<circle class="header-dot" cx="35" cy="18" r="5" fill="#ffbd2e" />')
    lines.append('<circle class="header-dot" cx="50" cy="18" r="5" fill="#27c93f" />')
    lines.append(f'<text class="title-text" x="{width // 2}" y="22" text-anchor="middle">{username}@github ~ $ ./contributions.sh</text>')
    lines.append(f'<line x1="0" y1="32" x2="{width}" y2="32" stroke="#21262d" stroke-width="1" />')
    
    # Calendar Grid Positioning
    box_size = 11
    box_gap = 3
    box_step = box_size + box_gap
    
    grid_start_x = 42
    grid_start_y = 65
    
    # Render Day Labels on Left (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for d_name, d_idx in day_labels:
        ly = grid_start_y + (d_idx * box_step) + 9
        lines.append(f'<text class="label-text" x="{grid_start_x - 8}" y="{ly}" text-anchor="end">{d_name}</text>')
        
    # Group days into 53 weeks
    weeks = [[] for _ in range(54)]
    last_month = -1
    month_headers = []
    
    if days:
        first_date_str = days[0]["date"]
        first_dt = datetime.strptime(first_date_str, "%Y-%m-%d")
        start_wday = (first_dt.weekday() + 1) % 7 # Sunday = 0
        
        current_w = 0
        current_d = start_wday
        
        for d in days:
            if current_d >= 7:
                current_d = 0
                current_w += 1
                
            if current_w < 54:
                weeks[current_w].append((current_d, d))
                
                # Check for month transition
                dt = datetime.strptime(d["date"], "%Y-%m-%d")
                if dt.month != last_month:
                    last_month = dt.month
                    month_headers.append((current_w, MONTH_NAMES[dt.month - 1]))
                    
            current_d += 1
            
    # Render Month Labels along top
    for w_idx, m_name in month_headers:
        mx = grid_start_x + (w_idx * box_step)
        lines.append(f'<text class="label-text" x="{mx}" y="{grid_start_y - 8}">{m_name}</text>')
        
    # Render Heatmap Rectangles
    for w_idx in range(min(53, len(weeks))):
        for d_idx, day_obj in weeks[w_idx]:
            x_pos = grid_start_x + (w_idx * box_step)
            y_pos = grid_start_y + (d_idx * box_step)
            
            level = day_obj.get("level", 0)
            count = day_obj.get("count", 0)
            
            if count > 0 and level == 0:
                level = 1
            level = max(0, min(len(PALETTE) - 1, level))
            color = PALETTE[level]
            
            # Staggered diagonal animation delay
            delay = 0.05 + (w_idx * 0.012) + (d_idx * 0.015)
            
            tooltip_str = f"{count} contribution{'s' if count != 1 else ''} on {day_obj['date']}"
            
            lines.append(
                f'<rect class="day-rect" x="{x_pos}" y="{y_pos}" width="{box_size}" height="{box_size}" '
                f'fill="{color}" style="animation-delay: {delay:.3f}s;">'
                f'<title>{tooltip_str}</title></rect>'
            )
            
    # Render Summary Footer Stats
    footer_y = grid_start_y + (7 * box_step) + 26
    
    # Left stats
    lines.append(f'<text class="stat-text" x="{grid_start_x}" y="{footer_y}">')
    lines.append(f'  <tspan class="stat-bold">{total_contribs:,}</tspan> contributions in the last year | ')
    lines.append(f'  Current streak: <tspan class="stat-bold">{current_streak} days</tspan> | ')
    lines.append(f'  Longest streak: <tspan class="stat-bold">{longest_streak} days</tspan>')
    lines.append('</text>')
    
    # Right Legend (Less -> More)
    legend_start_x = width - 160
    lines.append(f'<text class="label-text" x="{legend_start_x - 8}" y="{footer_y}">Less</text>')
    
    for l_idx, l_color in enumerate(PALETTE):
        lx = legend_start_x + (l_idx * 14)
        lines.append(f'<rect x="{lx}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{l_color}" />')
        
    lines.append(f'<text class="label-text" x="{legend_start_x + (len(PALETTE) * 14) + 4}" y="{footer_y}">More</text>')
    
    lines.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Rendered contribution heatmap SVG '{output_svg}'.")

if __name__ == "__main__":
    json_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    svg_path = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap_svg(json_path, svg_path)
