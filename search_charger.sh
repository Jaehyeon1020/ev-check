#!/bin/bash

SERVICE_KEY="__SERVICE_KEY__"

# 충전소 목록: "statId 위치설명" 형식
STATIONS=(
    "PW801329 "
    "PW801037 지하주차장"
)

# 충전기별 태그: "statId-chgerId 태그" 형식
CHARGER_TAGS=(
    "PW801329-01 105동 지상 후문 쪽"
    "PW801329-02 105동 지상 후문 쪽"
    "PW801329-03 105동 지상 후문 쪽"
    "PW801329-04 105동 지상 후문 쪽"
    "PW801329-05 105동 지상 후문 쪽"
    "PW801329-06 105동 지상 후문 쪽"
    "PW801329-07 105동 지상 후문 쪽"
    "PW801329-08 105동 지상 후문 쪽"
    "PW801329-09 105동 지상 후문 쪽"
    "PW801329-10 109동 지상"
    "PW801329-11 109동 지상"
    "PW801329-12 109동 지상"
    "PW801329-13 109동 지상"
    "PW801329-14 109동 지상"
    "PW801037-01 107동 후문 쪽"
    "PW801037-02 107동 후문 쪽"
    "PW801037-03 107동 후문 쪽"
    "PW801037-04 107동 후문 쪽"
    "PW801037-05 102동 지하 1층"
    "PW801037-06 102동 지하 1층"
    "PW801037-07 102동 지하 1층"
    "PW801037-08 102동 지하 1층"
    "PW801037-09 102동 지하 1층"
)

python3 -c "
import json, urllib.request, sys

service_key = sys.argv[1]
n = int(sys.argv[2])
stations = [sys.argv[3+i].split(' ', 1) for i in range(n)]
tags = {}
for entry in sys.argv[3+n:]:
    key, label = entry.split(' ', 1)
    tags[key] = label

stat_map = {'0':'알수없음','1':'통신이상','2':'사용가능','3':'충전중','4':'운영중지','5':'점검중'}

for stat_id, location in stations:
    url = (f'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
           f'?serviceKey={service_key}&numOfRows=9999&pageNo=1&dataType=JSON&statId={stat_id}')
    with urllib.request.urlopen(url) as r:
        data = json.load(r)
    items = data['items']['item']
    label = f' [{location}]' if location.strip() else ''
    print(f'=== {items[0].get(\"statNm\")}{label} ({stat_id}) / 총 {len(items)}기 ===')
    for x in items:
        stat = x.get('stat', '0')
        chger_id = x.get('chgerId')
        tag = tags.get(f'{stat_id}-{chger_id}', '')
        tag_str = f' [{tag}]' if tag else ''
        print(f'  충전기 {chger_id}{tag_str} | {stat_map.get(stat, stat)} | {x.get(\"output\")}kW | 타입: {x.get(\"chgerType\")}')
    print()
" "$SERVICE_KEY" "${#STATIONS[@]}" "${STATIONS[@]}" "${CHARGER_TAGS[@]}"
