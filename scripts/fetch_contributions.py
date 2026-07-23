import os
import sys
import json
import re
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="Prasadhol2001", output_json="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml"
    }
    
    print(f"Fetching contribution data for user '{username}' from {url}...")
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP error {resp.status_code} while fetching {url}")
        
    soup = BeautifulSoup(resp.text, "html.parser")
    
    days_data = []
    
    # Extract calendar cells (both <td> and <rect> elements are supported by GitHub HTML)
    cells = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)
    
    # Also find tooltips to match dates to contribution counts accurately
    tooltips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip") if t.get("for")}
    
    for cell in cells:
        cell_id = cell.get("id")
        date_str = cell.get("data-date")
        level_str = cell.get("data-level", "0")
        count_str = cell.get("data-count")
        
        if not date_str:
            continue
            
        try:
            level = int(level_str)
        except ValueError:
            level = 0
            
        count = 0
        if count_str is not None:
            try:
                count = int(count_str)
            except ValueError:
                count = 0
        else:
            # Fallback: check tooltip content or cell text
            tooltip_text = tooltips.get(cell_id, "")
            if tooltip_text:
                match = re.search(r"(\d+)\s+contribution", tooltip_text)
                if match:
                    count = int(match.group(1))
                    
        days_data.append({
            "date": date_str,
            "level": level,
            "count": count
        })
        
    # Sort days chronologically
    days_data.sort(key=lambda d: d["date"])
    
    # Calculate statistics
    total_contributions = sum(d["count"] for d in days_data)
    
    # Streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    best_day_count = 0
    best_day_date = ""
    
    for d in days_data:
        cnt = d["count"]
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
            if cnt > best_day_count:
                best_day_count = cnt
                best_day_date = d["date"]
        else:
            temp_streak = 0
            
    # Calculate current streak ending today or yesterday
    for d in reversed(days_data):
        if d["count"] > 0:
            current_streak += 1
        else:
            break
            
    result = {
        "username": username,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {
            "date": best_day_date,
            "count": best_day_count
        },
        "days_count": len(days_data),
        "days": days_data
    }
    
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"Successfully scraped {len(days_data)} days! Total contributions: {total_contributions}. Saved to '{output_json}'.")

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "Prasadhol2001"
    fetch_contributions(user)
