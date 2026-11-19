# Renders the launch-curve chart as two SVGs (light + dark) from data/gta6_viewers_hourly.csv.
# No third-party libraries: the SVG is written directly so the repo stays reproducible.
import csv, os
from datetime import datetime, timezone

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
rows = list(csv.DictReader(open(os.path.join(D, 'gta6_viewers_hourly.csv'), encoding='utf-8')))

def t(s): return datetime.strptime(s, '%Y-%m-%dT%H:%MZ').replace(tzinfo=timezone.utc)
# Only the on-the-hour scheduled snapshots are charted, so the series is evenly
# spaced and its first point is the one the headline quotes. The 07:48 manual run
# that set the schedule up stays in the CSV.
pts = [(t(r['snapshot_utc']), int(r['gta6_viewers']), int(r['just_chatting_viewers']),
        int(r['gta5_viewers']), int(r['gta6_rank'])) for r in rows
       if t(r['snapshot_utc']).minute == 30]

W, H = 940, 470
L, R, T, B = 74, 148, 66, 58
PW, PH = W - L - R, H - T - B
x0, x1 = pts[0][0], pts[-1][0]
span = (x1 - x0).total_seconds()
YMAX = 1_400_000

def X(d): return L + PW * ((d - x0).total_seconds() / span)
def Y(v): return T + PH * (1 - v / YMAX)

SERIES = [('GTA 6', 1, 0), ('Just Chatting', 2, 1), ('GTA V', 3, 2)]  # label, slot, column offset
PEAK = max(pts, key=lambda p: p[1])
# The steepest two-hour climb. Labelled as a measurement, not a cause: the
# snapshots show when viewers arrived, not when any server opened.
CLIMB_TO = next(p for p in pts if p[1] > 500_000)
CLIMB_FROM = pts[pts.index(CLIMB_TO) - 2]
CLIMB_MARK = pts[pts.index(CLIMB_TO) - 1]

THEMES = {
    'light': dict(surface='#ffffff', ink='#0b0b0b', ink2='#52514e', ink3='#75736c',
                  grid='#e6e5e1', s1='#2a78d6', s2='#eb6834', s3='#1baf7a'),
    'dark':  dict(surface='#0d1117', ink='#f0efec', ink2='#c3c2b7', ink3='#9a988d',
                  grid='#272c33', s1='#3987e5', s2='#d95926', s3='#199e70'),
}

def fmt(v):
    if v >= 1_000_000: return f'{v/1_000_000:.2f}M'
    if v >= 1_000: return f'{v//1000}k'
    return str(v)

def build(mode):
    c = THEMES[mode]
    col = {1: c['s1'], 2: c['s2'], 3: c['s3']}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
         f'role="img" aria-label="Hourly concurrent viewers on Kick.com for GTA 6, Just Chatting and GTA V '
         f'from 18 to 19 November 2026. GTA 6 rises from 6,724 to a peak of 1,353,198.">']
    o.append(f'<rect width="{W}" height="{H}" fill="{c["surface"]}"/>')
    # title
    o.append(f'<text x="{L}" y="30" fill="{c["ink"]}" font-size="19" font-weight="650">'
             f'GTA 6 launch night on Kick.com</text>')
    o.append(f'<text x="{L}" y="50" fill="{c["ink2"]}" font-size="13">'
             f'Concurrent viewers by category &#183; 18&#8211;19 November 2026 (UTC)</text>')
    # y grid + labels
    for v in range(0, YMAX + 1, 200_000):
        y = Y(v)
        o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+PW}" y2="{y:.1f}" stroke="{c["grid"]}" stroke-width="1"/>')
        o.append(f'<text x="{L-10}" y="{y+4:.1f}" fill="{c["ink3"]}" font-size="11.5" text-anchor="end">{fmt(v)}</text>')
    # x ticks every 3h
    for d, *_ in pts:
        if d.hour % 3 == 0 and d.minute == 30:
            o.append(f'<text x="{X(d):.1f}" y="{T+PH+20:.1f}" fill="{c["ink3"]}" font-size="11.5" '
                     f'text-anchor="middle">{d:%H:%M}</text>')
    midnight = next((d for d, *_ in pts if d.hour == 0), None)
    if midnight:
        mx = X(midnight)
        o.append(f'<line x1="{mx:.1f}" y1="{T}" x2="{mx:.1f}" y2="{T+PH}" stroke="{c["grid"]}" stroke-width="1.5"/>')
        o.append(f'<text x="{mx+6:.1f}" y="{T+13}" fill="{c["ink3"]}" font-size="11">19 Nov</text>')
    # steepest-climb annotation
    ux = X(CLIMB_MARK[0])
    o.append(f'<line x1="{ux:.1f}" y1="{T}" x2="{ux:.1f}" y2="{T+PH}" stroke="{c["ink3"]}" '
             f'stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<text x="{ux+7:.1f}" y="{T+16}" fill="{c["ink2"]}" font-size="11.5" font-weight="600">'
             f'+{CLIMB_TO[1]-CLIMB_FROM[1]:,} in two hours</text>')
    o.append(f'<text x="{ux+7:.1f}" y="{T+31}" fill="{c["ink3"]}" font-size="11">'
             f'{CLIMB_FROM[0]:%H:%M} &#8594; {CLIMB_TO[0]:%H:%M} UTC</text>')
    # lines
    for label, slot, idx in SERIES:
        pth = ' '.join(f'{X(p[0]):.1f},{Y(p[1+idx]):.1f}' for p in pts)
        o.append(f'<polyline points="{pth}" fill="none" stroke="{col[slot]}" stroke-width="2" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
    # peak marker
    px, py = X(PEAK[0]), Y(PEAK[1])
    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{col[1]}" stroke="{c["surface"]}" stroke-width="2"/>')
    o.append(f'<text x="{px:.1f}" y="{py-14:.1f}" fill="{c["ink"]}" font-size="12.5" font-weight="650" '
             f'text-anchor="middle">{PEAK[1]:,}</text>')
    o.append(f'<text x="{px:.1f}" y="{py-29:.1f}" fill="{c["ink2"]}" font-size="11" '
             f'text-anchor="middle">peak &#183; rank #1</text>')
    # first point marker
    fx, fy = X(pts[0][0]), Y(pts[0][1])
    o.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="4" fill="{col[1]}" stroke="{c["surface"]}" stroke-width="2"/>')
    o.append(f'<path d="M {fx+11:.1f} 312 L {fx+11:.1f} {fy-24:.1f} L {fx+2:.1f} {fy-7:.1f}" '
             f'fill="none" stroke="{c["ink3"]}" stroke-width="1"/>')
    o.append(f'<text x="{fx+6:.1f}" y="298" fill="{c["ink2"]}" font-size="11.5" font-weight="600">'
             f'{pts[0][1]:,}</text>')
    o.append(f'<text x="{fx+6:.1f}" y="283" fill="{c["ink3"]}" font-size="11">'
             f'rank #{pts[0][4]} at {pts[0][0]:%H:%M}</text>')
    # direct labels, nudged apart
    lab = sorted(((Y(pts[-1][1 + idx]), label, slot, pts[-1][1 + idx]) for label, slot, idx in SERIES),
                 key=lambda z: z[0])
    GAP, LO, HI = 34.0, T + 6, T + PH - 18      # two text lines per label need ~34px
    ys = [z[0] for z in lab]
    for i in range(1, len(ys)):                  # push down, then clamp the whole stack up
        ys[i] = max(ys[i], ys[i - 1] + GAP)
    overflow = ys[-1] - HI
    if overflow > 0:
        ys = [max(LO, y - overflow) for y in ys]
        for i in range(1, len(ys)):
            ys[i] = max(ys[i], ys[i - 1] + GAP)
    for (anchor, label, slot, val), y in zip(lab, ys):
        o.append(f'<line x1="{L+PW:.1f}" y1="{anchor:.1f}" x2="{L+PW+10:.1f}" y2="{y:.1f}" '
                 f'stroke="{col[slot]}" stroke-width="1"/>')
        o.append(f'<text x="{L+PW+15:.1f}" y="{y:.1f}" fill="{c["ink"]}" font-size="12.5" '
                 f'font-weight="600">{label}</text>')
        o.append(f'<text x="{L+PW+15:.1f}" y="{y+15:.1f}" fill="{c["ink2"]}" font-size="11.5">{val:,}</text>')
    # legend
    lx = L + 2
    o.append(f'<g>')
    for i, (label, slot, _) in enumerate(SERIES):
        gx = lx + i * 132
        o.append(f'<rect x="{gx}" y="{H-24}" width="18" height="3" rx="1.5" fill="{col[slot]}"/>')
        o.append(f'<text x="{gx+25}" y="{H-18}" fill="{c["ink2"]}" font-size="11.5">{label}</text>')
    o.append('</g>')
    o.append(f'<text x="{W-14}" y="{H-18}" fill="{c["ink3"]}" font-size="10.5" text-anchor="end">'
             f'Source: Kick.com, collected hourly with the Kick Scraper on Apify</text>')
    o.append('</svg>')
    return '\n'.join(o)

for mode in ('light', 'dark'):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'chart-{mode}.svg')
    open(p, 'w', encoding='utf-8').write(build(mode))
    print('wrote', p)
print(f'{len(pts)} points | first {pts[0][1]:,} | peak {PEAK[1]:,} at {PEAK[0]:%H:%M} | steepest climb {CLIMB_FROM[0]:%H:%M}-{CLIMB_TO[0]:%H:%M}')
