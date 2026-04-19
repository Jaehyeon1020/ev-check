import json, urllib.request, sys
from datetime import datetime, timezone, timedelta

SERVICE_KEY = "70d9d335578e9fceb09425f85cc40a1976989c3fd59fe61962a4775daba7b7cf"

STATIONS = [
    {"stat_id": "PW801329", "location": ""},
    {"stat_id": "PW801037", "location": "지하주차장"},
]

CHARGER_TAGS = {
    "PW801329-01": "105동 지상 후문 쪽",
    "PW801329-02": "105동 지상 후문 쪽",
    "PW801329-03": "105동 지상 후문 쪽",
    "PW801329-04": "105동 지상 후문 쪽",
    "PW801329-05": "105동 지상 후문 쪽",
    "PW801329-06": "105동 지상 후문 쪽",
    "PW801329-07": "105동 지상 후문 쪽",
    "PW801329-08": "105동 지상 후문 쪽",
    "PW801329-09": "105동 지상 후문 쪽",
    "PW801329-10": "109동 지상",
    "PW801329-11": "109동 지상",
    "PW801329-12": "109동 지상",
    "PW801329-13": "109동 지상",
    "PW801329-14": "109동 지상",
    "PW801037-01": "107동 후문 쪽",
    "PW801037-02": "107동 후문 쪽",
    "PW801037-03": "107동 후문 쪽",
    "PW801037-04": "107동 후문 쪽",
    "PW801037-05": "102동 지하 1층",
    "PW801037-06": "102동 지하 1층",
    "PW801037-07": "102동 지하 1층",
    "PW801037-08": "102동 지하 1층",
    "PW801037-09": "102동 지하 1층",
}

STAT_MAP = {
    "0": ("알수없음", "#aaa"),
    "1": ("통신이상", "#e74c3c"),
    "2": ("사용가능", "#2ecc71"),
    "3": ("충전중",   "#3498db"),
    "4": ("운영중지", "#e67e22"),
    "5": ("점검중",   "#e67e22"),
}

def fetch(stat_id):
    url = (f"http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
           f"?serviceKey={SERVICE_KEY}&numOfRows=9999&pageNo=1&dataType=JSON&statId={stat_id}")
    with urllib.request.urlopen(url) as r:
        return json.load(r)["items"]["item"]

def render_station(stat_id, location, items):
    label = f" [{location}]" if location else ""
    stat_name = items[0].get("statNm", stat_id)

    rows = ""
    for x in items:
        chger_id = x.get("chgerId")
        stat_code = x.get("stat", "0")
        stat_text, color = STAT_MAP.get(stat_code, ("알수없음", "#aaa"))
        tag = CHARGER_TAGS.get(f"{stat_id}-{chger_id}", "")
        tag_html = f'<span class="tag">{tag}</span>' if tag else ""
        rows += f"""
        <tr>
          <td>충전기 {chger_id}</td>
          <td>{tag_html}</td>
          <td><span class="badge" style="background:{color}">{stat_text}</span></td>
          <td>{x.get("output")}kW</td>
        </tr>"""

    available = sum(1 for x in items if x.get("stat") == "2")
    total = len(items)

    return f"""
    <div class="station">
      <h2>{stat_name}{label} <small>({stat_id})</small></h2>
      <p class="summary">사용가능 <strong>{available}</strong> / 전체 {total}기</p>
      <table>
        <thead><tr><th>충전기</th><th>위치</th><th>상태</th><th>용량</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""

kst = datetime.now(timezone(timedelta(hours=9)))
updated = kst.strftime("%Y-%m-%d %H:%M KST")

stations_html = ""
for s in STATIONS:
    items = fetch(s["stat_id"])
    stations_html += render_station(s["stat_id"], s["location"], items)

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>동탄파크푸르지오 충전기 현황</title>
  <style>
    body {{ font-family: -apple-system, sans-serif; max-width: 700px; margin: 0 auto; padding: 16px; background: #f5f5f5; }}
    h1 {{ font-size: 1.3rem; margin-bottom: 4px; }}
    .updated {{ color: #888; font-size: 0.85rem; margin-bottom: 24px; }}
    .station {{ background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
    h2 {{ font-size: 1rem; margin: 0 0 4px; }}
    h2 small {{ color: #999; font-weight: normal; font-size: 0.8rem; }}
    .summary {{ margin: 0 0 12px; font-size: 0.9rem; color: #555; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    th {{ text-align: left; padding: 6px 8px; border-bottom: 2px solid #eee; color: #888; font-weight: 500; }}
    td {{ padding: 6px 8px; border-bottom: 1px solid #f0f0f0; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 20px; color: #fff; font-size: 0.8rem; }}
    .tag {{ display: inline-block; padding: 1px 6px; border-radius: 4px; background: #eef; color: #558; font-size: 0.78rem; }}
  </style>
</head>
<body>
  <h1>동탄파크푸르지오 충전기 현황</h1>
  <p class="updated">마지막 업데이트: {updated}</p>
  {stations_html}
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 생성 완료")
