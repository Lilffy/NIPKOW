# -*- coding: utf-8 -*-
"""
生成嘉立创EDA专业版可导入的 DXF：板框 + 4x M3 安装孔 + 禁布环 + 参考尺寸。

用法:
    python make_board_dxf.py
输出:
    docs/mech/board_100x90.dxf
    docs/mech/board_99x89.dxf
    docs/mech/preview_100x90.png
    docs/mech/preview_99x89.png

坐标原点 = 板左下角 (0,0)，单位 mm（DXF 头 $INSUNITS=4）。
图层:
    BOARD_OUTLINE  板框（闭合矩形，导入后再"转换为板框/板子形状"）
    MOUNTING_HOLE  安装孔 Ø3.2
    KEEPOUT        安装孔禁布环 Ø6.0（孔中心 6mm 内不放铜/走线）
    REF            中心十字、尺寸与文字（可整体删除）
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "docs", "mech")

HOLE_D = 3.2          # M3 螺钉通孔
PAD_D = 6.0           # 孔外禁布环直径（约等于 M3 垫片/铜柱外径）
EDGE_INSET = 5.08     # 孔中心到板边距离 (= 0.2 inch)


def esc(s):
    return s.replace("\n", " ")


class DXF:
    def __init__(self):
        self.entities = []
        self.layers = {}

    def layer(self, name, color=7):
        self.layers.setdefault(name, color)

    def line(self, layer, x1, y1, x2, y2):
        self.layer(layer)
        self.entities.append(
            "0\nLINE\n8\n%s\n10\n%.4f\n20\n%.4f\n11\n%.4f\n21\n%.4f\n"
            % (layer, x1, y1, x2, y2)
        )

    def circle(self, layer, cx, cy, r):
        self.layer(layer)
        self.entities.append(
            "0\nCIRCLE\n8\n%s\n10\n%.4f\n20\n%.4f\n40\n%.4f\n" % (layer, cx, cy, r)
        )

    def text(self, layer, x, y, h, s):
        self.layer(layer)
        self.entities.append(
            "0\nTEXT\n8\n%s\n10\n%.4f\n20\n%.4f\n40\n%.4f\n1\n%s\n"
            % (layer, x, y, h, esc(s))
        )

    def rect(self, layer, x0, y0, x1, y1):
        self.line(layer, x0, y0, x1, y0)
        self.line(layer, x1, y0, x1, y1)
        self.line(layer, x1, y1, x0, y1)
        self.line(layer, x0, y1, x0, y0)

    def dim_h(self, layer, x0, x1, y, text):
        self.line(layer, x0, y - 1, x0, y + 1)
        self.line(layer, x1, y - 1, x1, y + 1)
        self.line(layer, x0, y, x1, y)
        self.text(layer, (x0 + x1) / 2.0 - 4, y + 1.5, 2.5, text)

    def dim_v(self, layer, y0, y1, x, text):
        self.line(layer, x - 1, y0, x + 1, y0)
        self.line(layer, x - 1, y1, x + 1, y1)
        self.line(layer, x, y0, x, y1)
        self.text(layer, x + 1.5, (y0 + y1) / 2.0, 2.5, text)

    def render(self, extents=(0.0, 0.0, 0.0, 0.0)):
        xmin, ymin, xmax, ymax = extents
        out = []
        out.append("0\nSECTION\n2\nHEADER\n")
        out.append("9\n$ACADVER\n1\nAC1009\n")
        out.append("9\n$INSUNITS\n70\n4\n")          # 4 = millimeter
        out.append("9\n$MEASUREMENT\n70\n1\n")
        out.append("9\n$EXTMIN\n10\n%.4f\n20\n%.4f\n30\n0.0\n" % (xmin, ymin))
        out.append("9\n$EXTMAX\n10\n%.4f\n20\n%.4f\n30\n0.0\n" % (xmax, ymax))
        out.append("0\nENDSEC\n")

        # TABLES: 线型表 + 图层表（部分导入器要求 LTYPE 存在）
        out.append("0\nSECTION\n2\nTABLES\n")
        out.append("0\nTABLE\n2\nLTYPE\n70\n1\n")
        out.append("0\nLTYPE\n2\nCONTINUOUS\n70\n64\n3\nSolid line\n72\n65\n73\n0\n40\n0.0\n")
        out.append("0\nENDTAB\n")
        out.append("0\nTABLE\n2\nLAYER\n70\n%d\n" % len(self.layers))
        for name, color in self.layers.items():
            out.append(
                "0\nLAYER\n2\n%s\n70\n0\n62\n%d\n6\nCONTINUOUS\n" % (name, color)
            )
        out.append("0\nENDTAB\n0\nENDSEC\n")

        # BLOCKS（空表，保持结构完整）
        out.append("0\nSECTION\n2\nBLOCKS\n0\nENDSEC\n")

        out.append("0\nSECTION\n2\nENTITIES\n")
        out.extend(self.entities)
        out.append("0\nENDSEC\n0\nEOF\n")
        return "".join(out)


def build(w, h, title):
    d = DXF()
    holes = [
        (EDGE_INSET, EDGE_INSET),
        (round(w - EDGE_INSET, 4), EDGE_INSET),
        (EDGE_INSET, round(h - EDGE_INSET, 4)),
        (round(w - EDGE_INSET, 4), round(h - EDGE_INSET, 4)),
    ]

    # 板框（闭合矩形）
    d.rect("BOARD_OUTLINE", 0.0, 0.0, float(w), float(h))

    # 安装孔 + 禁布环
    for i, (cx, cy) in enumerate(holes, 1):
        d.circle("MOUNTING_HOLE", cx, cy, HOLE_D / 2.0)
        d.circle("KEEPOUT", cx, cy, PAD_D / 2.0)
        d.text("REF", cx + 2.6, cy + 2.6, 1.8, "H%d" % i)

    # 中心十字（对称参考）
    cx, cy = w / 2.0, h / 2.0
    d.line("REF", cx - 3, cy, cx + 3, cy)
    d.line("REF", cx, cy - 3, cx, cy + 3)

    # 参考尺寸
    d.dim_h("REF", 0, w, -5.0, "%.2f mm" % w)
    d.dim_v("REF", 0, h, -5.0, "%.2f mm" % h)
    d.text("REF", 2.0, h - 6.0, 3.0, title)

    return d, holes


def preview(holes, w, h, path, px_per_mm=9):
    from PIL import Image, ImageDraw, ImageFont

    def font(size):
        base = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        for cand in ("msyh.ttc", "msyhbd.ttc", "simhei.ttf", "simsun.ttc"):
            p = os.path.join(base, cand)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    f_title = font(15)
    f_small = font(12)

    top_mm, bottom_mm, side_mm = 16.0, 14.0, 14.0
    W = int(round((w + 2 * side_mm) * px_per_mm))
    H = int(round((h + top_mm + bottom_mm) * px_per_mm))
    img = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(img)

    def P(x, y):
        """DXF 坐标(y 向上，原点在板左下角) -> 图像像素"""
        return ((x + side_mm) * px_per_mm, H - (y + bottom_mm) * px_per_mm)

    def box(x0, y0, x1, y1):
        a, b = P(x0, y0), P(x1, y1)
        return [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]

    dr.rectangle(box(0, 0, w, h), fill=(233, 245, 234), outline=(20, 120, 40), width=3)

    for gx in range(10, int(w), 10):
        dr.line([P(gx, 0), P(gx, h)], fill=(208, 222, 208))
    for gy in range(10, int(h), 10):
        dr.line([P(0, gy), P(w, gy)], fill=(208, 222, 208))

    for cx, cy in holes:
        r = PAD_D / 2.0 * px_per_mm
        c = P(cx, cy)
        dr.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=(200, 60, 60), width=2)
        r2 = HOLE_D / 2.0 * px_per_mm
        dr.ellipse([c[0] - r2, c[1] - r2, c[0] + r2, c[1] + r2],
                   fill=(255, 255, 255), outline=(200, 60, 60), width=2)

    # 底部尺寸
    y0 = -3.0
    dr.line([P(0, y0), P(w, y0)], fill=(60, 60, 60))
    for xx in (0, w):
        dr.line([P(xx, y0 - 1.2), P(xx, y0 + 1.2)], fill=(60, 60, 60))
    dr.text(P(w / 2 - 8, y0 - 5.0), "%.0f mm" % w, fill=(60, 60, 60), font=f_small)

    # 左侧尺寸
    x0 = -5.0
    dr.line([P(x0, 0), P(x0, h)], fill=(60, 60, 60))
    for yy in (0, h):
        dr.line([P(x0 - 1.2, yy), P(x0 + 1.2, yy)], fill=(60, 60, 60))
    dr.text(P(x0 - 9.0, h / 2), "%.0f mm" % h, fill=(60, 60, 60), font=f_small)

    dr.text(P(0, h + 6.5), "Nipkow 扩展板  %.0f x %.0f mm  REV-A" % (w, h),
            fill=(20, 20, 20), font=f_title)
    dr.text(P(0, h + 2.0), "M3 x4  孔 Ø3.2  禁布环 Ø6.0  孔中心距板边 5.08 mm",
            fill=(90, 90, 90), font=f_small)

    for i, (cx, cy) in enumerate(holes, 1):
        tx = cx + 4.2 if cx < w / 2 else cx - 32.0
        ty = cy + 4.2 if cy < h / 2 else cy - 7.0
        dr.text(P(tx, ty), "H%d  %.2f, %.2f" % (i, cx, cy), fill=(120, 40, 40), font=f_small)

    dr.text(P(0, -9.5), "原点 (0,0) = 板左下角；导入 EDA 后请核对标注尺寸",
            fill=(110, 110, 110), font=f_small)

    img.save(path)
    print("preview ->", path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for (w, h, note) in ((100.0, 90.0, "100x90"), (99.0, 89.0, "99x89")):
        title = "YKB-NIPKOW  %.0fx%.0f  REV-A" % (w, h)
        d, holes = build(w, h, title)
        dxf_path = os.path.join(OUT_DIR, "board_%s.dxf" % note)
        with open(dxf_path, "w", encoding="ascii", newline="\n") as f:
            f.write(d.render(extents=(-10.0, -10.0, w + 10.0, h + 10.0)))
        print("dxf ->", dxf_path)
        preview(holes, w, h, os.path.join(OUT_DIR, "preview_%s.png" % note))
        for i, (cx, cy) in enumerate(holes, 1):
            print("   H%d  X=%.2f  Y=%.2f  (%.0f mil, %.0f mil)"
                  % (i, cx, cy, cx / 0.0254, cy / 0.0254))


if __name__ == "__main__":
    main()
