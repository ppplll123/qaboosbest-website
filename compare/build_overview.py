#!/usr/bin/env python3
"""Generates compare/overview.svg (1200x630) from compare/data.json.
Re-run after data.json changes, then re-render PNG/JPG/PDF (see repo README or git log).
"""
import json, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'data.json')))
cs = d['companies']

def score(c):
    s = 0
    for cell in list(c['features'].values()) + list(c['services'].values()):
        v = cell.get('v')
        if v == 1: s += 1
        elif v == 0.5: s += 0.5
    return s

ranked = sorted(cs, key=score, reverse=True)
maxscore = 20  # 12 features + 8 services

# palette (matches the site's classic theme)
BLUE, TEAL, GOLD, INK, MUTED, LINE, BG2 = '#173f5f', '#14507e', '#b8860b', '#1c2b33', '#5a6a76', '#c9d4dd', '#edf3f8'

rows = []
y0, rowh, barx, barw = 150, 29, 300, 360
for i, c in enumerate(ranked):
    y = y0 + i * rowh
    s = score(c)
    us = c.get('us')
    w = max(6, s / maxscore * barw)
    name = html.escape(c['short'])
    star = ' ★' if us else ''
    fill = GOLD if us else TEAL
    weight = '700' if us else '500'
    rows.append(f'''  <text x="64" y="{y+15}" font-size="13.5" font-weight="{weight}" fill="{INK}">{i+1}.</text>
  <text x="88" y="{y+15}" font-size="13.5" font-weight="{weight}" fill="{GOLD if us else INK}">{name}{star}</text>
  <rect x="{barx}" y="{y+2}" width="{barw}" height="16" fill="{BG2}"/>
  <rect x="{barx}" y="{y+2}" width="{w:.0f}" height="16" fill="{fill}"/>
  <text x="{barx+barw+12}" y="{y+15}" font-size="13" font-weight="700" fill="{INK}">{s:g}</text>''')

stats = [
    ("0 / 10", "direct repair competitors have", "any Arabic website — we are fully bilingual"),
    ("1 / 15", "sites display a verifiable", "trade license. It's ours (DET 1475682)"),
    ("4 / 15", "sites have any FAQ section —", "ours is the only bilingual one"),
    ("10 / 15", "claim years-in-business;", "none show verifiable proof"),
]
statsvg = []
sy = 158
for big, l1, l2 in stats:
    statsvg.append(f'''  <rect x="760" y="{sy-26}" width="6" height="78" fill="{GOLD if big.startswith('1 /') else TEAL}"/>
  <text x="782" y="{sy}" font-size="34" font-weight="800" fill="{BLUE}">{big}</text>
  <text x="782" y="{sy+24}" font-size="13.5" fill="{MUTED}">{html.escape(l1)}</text>
  <text x="782" y="{sy+42}" font-size="13.5" fill="{MUTED}">{html.escape(l2)}</text>''')
    sy += 108

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" font-family="Arial,Helvetica,sans-serif">
  <rect width="1200" height="630" fill="#ffffff"/>
  <rect width="1200" height="92" fill="{BLUE}"/>
  <text x="40" y="40" font-size="27" font-weight="800" fill="#ffffff">UAE Medical Equipment Service Websites — At a Glance</text>
  <text x="40" y="68" font-size="13.5" fill="#cfe3ea">15 company websites compared on 20 criteria · compiled from publicly available data, June 2026 · full matrix: qaboosbest.com/compare</text>
  <text x="64" y="127" font-size="12" font-weight="700" fill="{MUTED}" letter-spacing="1">RANKED BY WEBSITE SCORE&#160;&#160;(present = 1 · partial = 0.5 · max {maxscore})</text>
  <text x="760" y="127" font-size="12" font-weight="700" fill="{MUTED}" letter-spacing="1">THE GAPS THAT MATTER</text>
{chr(10).join(rows)}
{chr(10).join(statsvg)}
  <rect x="0" y="596" width="1200" height="34" fill="{BG2}"/>
  <text x="40" y="617" font-size="11" fill="{MUTED}">Public website data only · competitor claims as stated, not independently verified · trademarks belong to their owners · © 2026 Qaboos Best Medical &amp; Laboratory Equipment Repairing Est.</text>
</svg>
'''
out = os.path.join(HERE, 'overview.svg')
open(out, 'w').write(svg)
print(f"wrote {out} ({len(svg)} bytes), {len(ranked)} companies, top: {ranked[0]['short']} ({score(ranked[0]):g})")
