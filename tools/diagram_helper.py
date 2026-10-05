"""Canonical source of `draw_diagram`, the commutative-diagram helper.

Notebooks must be self-contained (they are exported to WASM one at a time), so
this file is NOT imported. Each notebook that draws diagrams pastes the function
below, verbatim, into its second cell:

    @app.cell(hide_code=True)
    def _():
        def draw_diagram(nodes, arrows, figsize=(5.0, 3.2), title=None):
            ...
        return (draw_diagram,)

and later cells take `draw_diagram` as a cell argument. If you change the
function here, re-paste it into every notebook that uses it.
"""


def draw_diagram(nodes, arrows, figsize=(5.0, 3.2), title=None):
    """Draw a diagram in a category.

    nodes:  {key: (x, y)} or {key: (x, y, label)}  -- label defaults to key, mathtext allowed
    arrows: [(src, dst, label)] or [(src, dst, label, opts)]
            opts: rad    curvature (default 0; use +/-0.3 for parallel or bypassing arrows)
                  dashed True for an arrow whose existence is being asserted ("exists unique")
                  side   -1 to put the label on the other side of the arrow
                  color  matplotlib color
                  loop   "up" | "down" | "left" | "right" when src == dst (identities, endomorphisms)
    Returns the matplotlib figure; make it the last expression of the cell.
    """
    import math

    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch

    _fig, _ax = plt.subplots(figsize=figsize)
    _pos = {}
    for _key, _val in nodes.items():
        _label = _val[2] if len(_val) > 2 else _key
        _pos[_key] = (_val[0], _val[1])
        _ax.text(_val[0], _val[1], _label, ha="center", va="center", fontsize=15, zorder=3)
    for _arrow in arrows:
        _src, _dst, _label = _arrow[0], _arrow[1], _arrow[2]
        _opts = _arrow[3] if len(_arrow) > 3 else {}
        _color = _opts.get("color", "#1f2937")
        _ls = "--" if _opts.get("dashed") else "-"
        _side = _opts.get("side", 1)
        _x1, _y1 = _pos[_src]
        _x2, _y2 = _pos[_dst]
        if _src == _dst:
            _ux, _uy = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}[_opts.get("loop", "up")]
            _tx, _ty = _uy, -_ux
            _ax.add_patch(FancyArrowPatch(
                (_x1 + 0.20 * _ux - 0.13 * _tx, _y1 + 0.20 * _uy - 0.13 * _ty),
                (_x1 + 0.20 * _ux + 0.13 * _tx, _y1 + 0.20 * _uy + 0.13 * _ty),
                connectionstyle="arc3,rad=-2.2", arrowstyle="-|>", mutation_scale=11,
                shrinkA=0, shrinkB=0, lw=1.3, color=_color, linestyle=_ls, zorder=2,
            ))
            _ax.text(_x1 + 0.66 * _ux, _y1 + 0.66 * _uy, _label, ha="center", va="center", fontsize=12, color=_color)
            continue
        _rad = _opts.get("rad", 0.0)
        _ax.add_patch(FancyArrowPatch(
            (_x1, _y1), (_x2, _y2),
            connectionstyle=f"arc3,rad={_rad}", arrowstyle="-|>", mutation_scale=13,
            shrinkA=17, shrinkB=17, lw=1.3, color=_color, linestyle=_ls, zorder=2,
        ))
        _dx, _dy = _x2 - _x1, _y2 - _y1
        _len = math.hypot(_dx, _dy) or 1.0
        _px, _py = _dy / _len, -_dx / _len
        _out = (1 if _rad > 0 else -1) * _side
        _off = 0.5 * _rad * _len + _out * 0.14
        _ax.text(
            (_x1 + _x2) / 2 + _off * _px, (_y1 + _y2) / 2 + _off * _py, _label,
            ha="center", va="center", fontsize=12, color=_color,
        )
    _xs = [_p[0] for _p in _pos.values()]
    _ys = [_p[1] for _p in _pos.values()]
    _ax.set_xlim(min(_xs) - 0.8, max(_xs) + 0.8)
    _ax.set_ylim(min(_ys) - 0.8, max(_ys) + 0.8)
    _ax.set_aspect("equal")
    _ax.axis("off")
    if title:
        _ax.set_title(title, fontsize=12)
    _fig.tight_layout()
    return _fig
