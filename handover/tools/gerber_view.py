# -*- coding: utf-8 -*-
"""
最小 Gerber / Excellon 解析器 + 预览渲染（够用版）

用途：打板前"看一眼"——确认板框尺寸、层有没有缺、孔位对不对。
不是 CAM 工具，不做 DRC。

用法: python gerber_view.py <gerber目录> <输出png>
"""

import os
import re
import sys


def _num(s, scale):
    return float(s) / scale


class GerberLayer:
    """解析 RS-274X 的常用子集：G01 直线、D01/D02/D03、圆形/矩形光圈。"""

    def __init__(self, path):
        self.path = path
        self.segments = []   # (x1,y1,x2,y2)
        self.flashes = []    # (x,y,r)
        self.unit = 'mm'
        self.fmt_int, self.fmt_dec = 3, 5
        self._parse()

    def _parse(self):
        txt = open(self.path, 'r', errors='replace').read()
        m = re.search(r'%FSLAX(\d)(\d)Y\d\d\*%', txt)
        if m:
            self.fmt_int, self.fmt_dec = int(m.group(1)), int(m.group(2))
        if '%MOIN*%' in txt:
            self.unit = 'inch'
        # 单位换算成 mm
        self.k = 25.4 if self.unit == 'inch' else 1.0
        self.scale = 10 ** self.fmt_dec

        apertures = {}
        for am in re.finditer(r'%ADD(\d+)([A-Za-z_.$][\w.$]*),([\d.Xx]+)\*%', txt):
            dcode = int(am.group(1))
            shape = am.group(2)
            params = am.group(3).split('X')
            try:
                vals = [float(p) for p in params if p not in ('', 'X')]
            except ValueError:
                vals = []
            if shape.startswith('C') and vals:
                apertures[dcode] = ('C', vals[0])
            elif shape.startswith('R') and len(vals) >= 2:
                apertures[dcode] = ('R', max(vals[0], vals[1]))
            elif shape.startswith('O') and len(vals) >= 2:
                apertures[dcode] = ('O', max(vals[0], vals[1]))
            else:
                apertures[dcode] = ('C', 0.1)

        cur = (0.0, 0.0)
        cur_ap = None
        for raw in txt.splitlines():
            line = raw.strip()
            if not line or line.startswith('%') or line.startswith('G04'):
                continue
            # 光圈选择
            for d in re.finditer(r'(?:^|G54)?D(\d+)\*', line):
                code = int(d.group(1))
                if code >= 10:
                    cur_ap = apertures.get(code, ('C', 0.1))
            # 坐标 + 操作
            for cmd in re.finditer(r'(?:G0?([123]))?'
                                   r'(?:X(-?\d+))?(?:Y(-?\d+))?'
                                   r'(?:I(-?\d+))?(?:J(-?\d+))?'
                                   r'D0?([123])\*', line):
                g, x, y, i, j, op = cmd.groups()
                nx = _num(x, self.scale) * self.k if x is not None else cur[0]
                ny = _num(y, self.scale) * self.k if y is not None else cur[1]
                if op == '1':
                    self.segments.append((cur[0], cur[1], nx, ny))
                elif op == '3':
                    r = (cur_ap[1] if cur_ap else 0.2) / 2.0
                    self.flashes.append((nx, ny, r))
                cur = (nx, ny)

    def bbox(self):
        pts = []
        for x1, y1, x2, y2 in self.segments:
            pts += [(x1, y1), (x2, y2)]
        pts += [(x, y) for x, y, _ in self.flashes]
        if not pts:
            return None
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return min(xs), min(ys), max(xs), max(ys)


class DrillFile:
    def __init__(self, path):
        self.path = path
        self.holes = []   # (x,y,dia)
        self._parse()

    def _parse(self):
        txt = open(self.path, 'r', errors='replace').read()
        unit = 'inch' if re.search(r'(?i)(METRIC|M71)', txt) is None else 'mm'
        k = 25.4 if unit == 'inch' else 1.0
        # 坐标格式：EasyEDA 用 2.4 / 3.3，取 FILE_FORMAT 或默认 6 位
        fmt = re.search(r';FILE_FORMAT=(\d):(\d)', txt)
        if fmt:
            scale = 10 ** int(fmt.group(2))
        else:
            m2 = re.search(r'METRIC\s*,\w+\s*,\s*(\d+)\.(\d+)', txt)
            if m2:
                scale = 10 ** len(m2.group(2))
            else:
                scale = 1000.0
        tools = {}
        cur = None
        for raw in txt.splitlines():
            line = raw.strip()
            m = re.match(r'T(\d+)C([\d.]+)', line)
            if m:
                tools[int(m.group(1))] = float(m.group(2))
                continue
            if re.match(r'T\d+$', line):
                cur = int(line[1:])
                continue
            if line.startswith('X') or line.startswith('Y'):
                m = re.match(r'X(-?[\d.]+)?Y(-?[\d.]+)?', line)
                if m and cur:
                    x = float(m.group(1)) / scale * k if m.group(1) else 0.0
                    y = float(m.group(2)) / scale * k if m.group(2) else 0.0
                    self.holes.append((x, y, tools.get(cur, 0.0)))


def render(layers, drills, out_png, scale=6.0):
    from PIL import Image, ImageDraw, ImageFont
    allbb = [l.bbox() for l in layers.values() if l.bbox()]
    xs0 = min(b[0] for b in allbb); ys0 = min(b[1] for b in allbb)
    xs1 = max(b[2] for b in allbb); ys1 = max(b[3] for b in allbb)
    margin = 6.0
    W = int((xs1 - xs0 + 2 * margin) * scale)
    H = int((ys1 - ys0 + 2 * margin) * scale)

    def P(x, y):
        return ((x - xs0 + margin) * scale, H - (y - ys0 + margin) * scale)

    img = Image.new('RGB', (W, H), (18, 20, 24))
    dr = ImageDraw.Draw(img, 'RGBA')

    colors = {
        'GKO': ((90, 200, 120), 3),
        'GTL': ((220, 90, 90), 1),
        'GBL': ((90, 140, 230), 1),
        'GTO': ((235, 235, 235), 1),
        'GBO': ((150, 150, 150), 1),
    }
    order = ['GBL', 'GTL', 'GTO', 'GBO', 'GKO']
    for key in order:
        layer = layers.get(key)
        if not layer:
            continue
        col, w = colors[key]
        for x1, y1, x2, y2 in layer.segments:
            dr.line([P(x1, y1), P(x2, y2)], fill=col + (235,), width=w)
        for x, y, r in layer.flashes:
            c = P(x, y)
            rr = max(1.0, r * scale)
            dr.ellipse([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], fill=col + (235,))

    for x, y, d in drills:
        c = P(x, y)
        rr = max(1.0, d / 2 * scale)
        dr.ellipse([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], fill=(250, 230, 120, 220))

    try:
        font = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 16)
    except Exception:
        font = ImageFont.load_default()
    dr.text((10, 8), 'NIPKOW 扩展开板  %.2f x %.2f mm   (红=顶层铜 蓝=底层铜 灰=丝印 绿=板框 黄=钻孔)'
            % (xs1 - xs0, ys1 - ys0), fill=(230, 230, 230), font=font)
    img.save(out_png)
    return (xs1 - xs0, ys1 - ys0)


def main():
    gdir = sys.argv[1]
    out = sys.argv[2]
    names = {'GKO': 'Gerber_BoardOutlineLayer.GKO', 'GTL': 'Gerber_TopLayer.GTL',
             'GBL': 'Gerber_BottomLayer.GBL', 'GTO': 'Gerber_TopSilkscreenLayer.GTO',
             'GBO': 'Gerber_BottomSilkscreenLayer.GBO'}
    layers = {}
    for k, fn in names.items():
        p = os.path.join(gdir, fn)
        if os.path.exists(p):
            layers[k] = GerberLayer(p)
            bb = layers[k].bbox()
            print('%-4s seg=%-5d flash=%-5d bbox=%s' % (k, len(layers[k].segments),
                                                        len(layers[k].flashes),
                                                        None if not bb else tuple(round(v, 2) for v in bb)))
    drills = []
    for fn in ('Drill_PTH_Through.DRL', 'Drill_NPTH_Through.DRL', 'Drill_PTH_Through_Via.DRL'):
        p = os.path.join(gdir, fn)
        if os.path.exists(p):
            d = DrillFile(p)
            sizes = {}
            for _, _, dia in d.holes:
                sizes[dia] = sizes.get(dia, 0) + 1
            print('%-32s holes=%-4d sizes=%s' % (fn, len(d.holes),
                  {round(k, 2): v for k, v in sorted(sizes.items())}))
            drills += d.holes
    w, h = render(layers, drills, out)
    print('preview -> %s  (%.2f x %.2f mm)' % (out, w, h))


if __name__ == '__main__':
    main()
