import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
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

    return (draw_diagram,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5C: Functors & Limits

    > *The product of two groups is built on the product of their underlying sets. The sum of two groups is not built on the sum of their underlying sets. Why the difference?*
    > — the question of this module

    Modules 5A and 5B computed limits and colimits inside one category at a time. But the examples kept inviting a comparison *between* categories: the product of two groups, of two vector spaces, of two topological spaces all had the cartesian product as underlying set, whereas the sum of two groups looked nothing like a disjoint union. A comparison between categories is made by a functor, here the forgetful functor to $\mathbf{Set}$. So we ask: *what can a functor do to a limit?*

    There are three precise answers. A functor may **preserve** limits (it sends limit cones to limit cones), **reflect** them (a cone that becomes a limit cone was one already), or **create** them (a limit downstairs lifts uniquely to a limit upstairs). The module defines the three notions, proves a model result for each, records how the standard forgetful functors behave, and then treats two situations where the functor is itself a limit construction: limits in functor categories, and limits of limits.

    By the end you will be able to prove that a given functor preserves or creates a given kind of limit, to refute preservation with a counterexample (and to say exactly what a counterexample must exhibit), and to prove that limits commute with limits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Functors Send Cones to Cones

    Before asking whether a functor respects limits we should check that it respects cones at all. Throughout, $\mathbf{I}$ is a small category, $D \colon \mathbf{I} \to \mathcal{A}$ is a diagram and $F \colon \mathcal{A} \to \mathcal{B}$ is a functor. The composite $F \circ D \colon \mathbf{I} \to \mathcal{B}$ is a diagram of the same shape in $\mathcal{B}$.

    ### Proof 1: the image of a cone is a cone

    - **Goal.** For every cone $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$, the family $(F f_I \colon F A \to F D(I))_{I \in \mathbf{I}}$ is a cone on $F \circ D$.
    - **Given.** The cone equations $D(u) \circ f_I = f_J$ for all $u \colon I \to J$ in $\mathbf{I}$; functoriality of $F$.
    - **Plan.** Direct: apply $F$ to each cone equation.
    - **Proof.** Let $u \colon I \to J$ be an arrow of $\mathbf{I}$. Then
      $$(F \circ D)(u) \circ F f_I = F(D(u)) \circ F(f_I) = F\big(D(u) \circ f_I\big) = F(f_J),$$
      using the definition of the composite functor, then that $F$ preserves composition, then the cone equation. This is the cone equation for $(F f_I)$ at $u$. $\qquad\blacksquare$
    - **What made it work.** Functors preserve every equation between composites, and a cone is defined by such equations. The same argument shows that $F$ sends cocones to cocones.

    Being a *limit* cone is not an equation between composites. It is a statement of the form "for every cone there exists a unique map", quantified over all objects of $\mathcal{A}$. A functor has no reason to respect that: $\mathcal{B}$ may contain test cones that do not come from $\mathcal{A}$, and maps that do not come from $\mathcal{A}$.

    **The comparison map.** Suppose $D$ has a limit cone $(p_I \colon L \to D(I))$ in $\mathcal{A}$ and $F \circ D$ has a limit cone $(m_I \colon M \to F D(I))$ in $\mathcal{B}$. By Proof 1, $(F p_I)$ is a cone on $F \circ D$ with vertex $F L$. So the universal property of $M$ gives a unique map
    $$c \colon F L \to M \qquad\text{with}\qquad m_I \circ c = F p_I \ \text{ for all } I,$$
    called the **comparison map**. For a product it is a map $F(X \times Y) \to F X \times F Y$. It always exists and always points in this direction. The question of this module is when it is an isomorphism.

    > **References.** [Leinster §5.3](https://arxiv.org/abs/1612.09375); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "FL": (1.4, 2.5, r"$F(X \times Y)$"), "M": (1.4, 1.1, r"$FX \times FY$"),
            "FX": (-0.6, 0, r"$FX$"), "FY": (3.4, 0, r"$FY$"),
        },
        [
            ("FL", "M", r"$c$", {"dashed": True, "color": "#b91c1c"}),
            ("M", "FX", r"$m_1$", {"side": -1}),
            ("M", "FY", r"$m_2$"),
            ("FL", "FX", r"$Fp_1$", {"rad": 0.3}),
            ("FL", "FY", r"$Fp_2$", {"rad": -0.3}),
        ],
        figsize=(5.8, 3.8),
        title="The comparison map for a binary product",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Preserving Limits

    > **Definition (preserves).** Let $\mathbf{I}$ be a small category. A functor $F \colon \mathcal{A} \to \mathcal{B}$ **preserves limits of shape $\mathbf{I}$** if for every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every cone $(p_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$:
    > $$(p_I \colon A \to D(I))_{I} \text{ is a limit cone on } D \quad\Longrightarrow\quad (F p_I \colon F A \to F D(I))_{I} \text{ is a limit cone on } F \circ D .$$
    > $F$ **preserves limits** if it preserves limits of shape $\mathbf{I}$ for all small $\mathbf{I}$. Preservation of colimits is defined dually, with cocones.

    **Reading the definition.**

    - **The conclusion is about a specific cone.** It is not enough that $F A$ be isomorphic, somehow, to the vertex of a limit of $F \circ D$. The cone $(F p_I)$ itself must be universal.
    - **To prove preservation:** take an arbitrary limit cone in $\mathcal{A}$, then run a universal-property proof in $\mathcal{B}$ for its image. The test cones are *arbitrary cones in $\mathcal{B}$* on $F \circ D$; their vertices need not be of the form $F A'$.
    - **To refute preservation:** exhibit one diagram $D$ that *has* a limit cone in $\mathcal{A}$ whose image is not a limit cone in $\mathcal{B}$.
    - **Vacuous cases.** If $D$ has no limit in $\mathcal{A}$, the definition demands nothing for that $D$.

    One limit cone per diagram is enough, which saves work in every example:

    ### Proof 2: it suffices to test one limit cone

    - **Goal.** Let $D \colon \mathbf{I} \to \mathcal{A}$ and suppose *some* limit cone $(p_I \colon L \to D(I))$ on $D$ has the property that $(F p_I)$ is a limit cone on $F \circ D$. Then for *every* limit cone $(p'_I \colon L' \to D(I))$ on $D$, $(F p'_I)$ is a limit cone on $F \circ D$.
    - **Given.** From 5A §5: Proof 5 (two limit cones differ by a unique isomorphism) and Proof 6 (a cone obtained from a limit cone by composing with an isomorphism is a limit cone). From 1C: functors preserve isomorphisms.
    - **Plan.** Move from $L'$ to $L$ by the isomorphism of 5A, apply $F$, and use Proof 6 in $\mathcal{B}$.
    - **Proof.** By Proof 5 of 5A there is an isomorphism $j \colon L' \to L$ with $p_I \circ j = p'_I$ for all $I$. Applying $F$ and using functoriality, $F p'_I = F p_I \circ F j$ for all $I$, and $F j \colon F L' \to F L$ is an isomorphism because functors preserve isomorphisms. By hypothesis $(F p_I)$ is a limit cone on $F \circ D$. By Proof 6 of 5A, applied in $\mathcal{B}$ to the limit cone $(F p_I)$ and the isomorphism $F j$, the cone $(F p_I \circ F j) = (F p'_I)$ is a limit cone. $\qquad\blacksquare$
    - **What made it work.** Limits are unique up to an isomorphism compatible with the projections, and functors preserve both isomorphisms and that compatibility.

    When $F \circ D$ is known to have a limit, there is a convenient test: *the image cone $(F p_I)$ is a limit cone if and only if the comparison map $c$ of Section 1 is an isomorphism.* For products this is `p04_comparison_map.md`.

    **Examples.**

    - **The inclusion $\mathbf{Ab} \to \mathbf{Grp}$ preserves binary products.** The product of abelian groups $G, H$ in $\mathbf{Ab}$ is $G \times H$ with its projections. The same group with the same projections is the product in $\mathbf{Grp}$ (5A §1). By Proof 2 that is enough.
    - **Order-preserving maps.** A functor between posets is an order-preserving map $f \colon P \to Q$ (1C). Products in a poset are meets (5A·P01), and any two cones with the same vertex are equal, so $f$ preserves binary products exactly when: whenever $x \wedge y$ exists in $P$, $f(x \wedge y)$ is a meet of $f(x)$ and $f(y)$ in $Q$. The map $x \mapsto \gcd(x, 6)$ on the divisors of $12$, ordered by divisibility, has this property.
    - **Forgetful functors** $\mathbf{Grp} \to \mathbf{Set}$, $\mathbf{Vect}_k \to \mathbf{Set}$, $\mathbf{Top} \to \mathbf{Set}$ preserve all limits (Sections 4 and 5).

    **Non-examples.**

    - **The inclusion $\mathbf{Ab} \to \mathbf{Grp}$ does not preserve binary sums.** In $\mathbf{Ab}$, the sum of $\mathbb{Z}/2$ and $\mathbb{Z}/2$ is $\mathbb{Z}/2 \oplus \mathbb{Z}/2$ with $i_1(g) = (g, 0)$, $i_2(h) = (0, h)$ (5B, Proof 3). Its image in $\mathbf{Grp}$ is that same cocone, and 5B §2 showed it is not a sum in $\mathbf{Grp}$: the test maps into $S_3$ sending the generators to two transpositions have no mediating homomorphism.
    - **The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ does not preserve initial objects** (colimits of the empty diagram). The one-element group is initial in $\mathbf{Grp}$. Its underlying set has one element, and a one-element set is not initial in $\mathbf{Set}$: it has two different maps to a two-element set.
    - **An order-preserving map that does not preserve meets.** Let $P$ be the subsets of $\{1, 2\}$ ordered by inclusion, $Q = \{0 < 1\}$, and $f(S) = 1$ if $S$ is non-empty, $f(\varnothing) = 0$. Then $\{1\} \wedge \{2\} = \varnothing$ and $f(\varnothing) = 0$, but $f(\{1\}) \wedge f(\{2\}) = 1 \wedge 1 = 1$.

    > **References.** [Leinster §5.3](https://arxiv.org/abs/1612.09375) (preservation); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Interactive: does this functor preserve this product?

    Each preset is a functor between two finite posets, regarded as categories and stored in the finite-category encoding of the course. Pick the functor, then two objects $X$ and $Y$ of the source. The widget finds every product cone of $X$ and $Y$ in the source by brute force over the universal property, applies $F$, and tests whether the image cone is a product cone in the target, again by brute force. The picture shows the two posets (an arrow $a \to b$ means $a \le b$; only covering relations are drawn).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pres_functor = mo.ui.dropdown(
        options=[
            "gcd(-, 6) : divisors of 12 -> divisors of 12",
            "nonempty? : subsets of {1,2} -> {0 < 1}",
            "inclusion : {1, 4, 6, 12} -> divisors of 12",
            "collapse : {a, b < t} -> {0 < 1}",
        ],
        value="inclusion : {1, 4, 6, 12} -> divisors of 12",
        label="Functor F",
    )
    pres_functor
    return (pres_functor,)


@app.cell(hide_code=True)
def _(mo, pres_functor):
    _objects = {
        "gcd(-, 6)": ["1", "2", "3", "4", "6", "12"],
        "nonempty?": ["{}", "{1}", "{2}", "{1,2}"],
        "inclusion": ["1", "4", "6", "12"],
        "collapse": ["a", "b", "t"],
    }[pres_functor.value.split(" :")[0]]
    pres_x = mo.ui.dropdown(options=_objects, value=_objects[1], label="X")
    pres_y = mo.ui.dropdown(options=_objects, value=_objects[2], label="Y")
    mo.hstack([pres_x, pres_y], justify="start")
    return pres_x, pres_y


@app.cell(hide_code=True)
def _(draw_diagram, mo, pres_functor, pres_x, pres_y):
    def _run():
        import math

        def poset_cat(elements, leq):
            arrows = {a + "<=" + b: (a, b) for a in elements for b in elements if leq(a, b)}
            identity = {a: a + "<=" + a for a in elements}
            compose = {
                (g, f): arrows[f][0] + "<=" + arrows[g][1]
                for f in arrows for g in arrows if arrows[f][1] == arrows[g][0]
            }
            return {"objects": list(elements), "arrows": arrows, "identity": identity, "compose": compose}

        def hom(cat, a, b):
            return [name for name, (dom, cod) in cat["arrows"].items() if dom == a and cod == b]

        def is_product(cat, P, p1, p2, X, Y):
            for A in cat["objects"]:
                for f1 in hom(cat, A, X):
                    for f2 in hom(cat, A, Y):
                        mediating = [
                            h for h in hom(cat, A, P)
                            if cat["compose"][(p1, h)] == f1 and cat["compose"][(p2, h)] == f2
                        ]
                        if len(mediating) != 1:
                            return False
            return True

        def products(cat, X, Y):
            return [
                (P, p1, p2)
                for P in cat["objects"] for p1 in hom(cat, P, X) for p2 in hom(cat, P, Y)
                if is_product(cat, P, p1, p2, X, Y)
            ]

        def divides(a, b):
            return int(b) % int(a) == 0

        _d12 = ["1", "2", "3", "4", "6", "12"]
        _d12_xy = {"1": (1, 0), "2": (0, 1), "3": (2, 1), "4": (0, 2), "6": (2, 2), "12": (1, 3)}
        _two = ["0", "1"]
        _two_xy = {"0": (0.5, 0.5), "1": (0.5, 2)}
        _sub = {"{}": set(), "{1}": {1}, "{2}": {2}, "{1,2}": {1, 2}}
        _name = pres_functor.value.split(" :")[0]
        if _name == "gcd(-, 6)":
            _src, _src_leq, _src_xy = _d12, divides, _d12_xy
            _tgt, _tgt_leq, _tgt_xy = _d12, divides, _d12_xy
            _on_objects = {x: str(math.gcd(int(x), 6)) for x in _d12}
        elif _name == "nonempty?":
            _src, _src_leq = list(_sub), (lambda a, b: _sub[a] <= _sub[b])
            _src_xy = {"{}": (1, 0), "{1}": (0, 1.3), "{2}": (2, 1.3), "{1,2}": (1, 2.6)}
            _tgt, _tgt_leq, _tgt_xy = _two, (lambda a, b: int(a) <= int(b)), _two_xy
            _on_objects = {"{}": "0", "{1}": "1", "{2}": "1", "{1,2}": "1"}
        elif _name == "inclusion":
            _src, _src_leq = ["1", "4", "6", "12"], divides
            _src_xy = {"1": (1, 0), "4": (0, 1.5), "6": (2, 1.5), "12": (1, 3)}
            _tgt, _tgt_leq, _tgt_xy = _d12, divides, _d12_xy
            _on_objects = {x: x for x in _src}
        else:
            _src = ["a", "b", "t"]
            _src_leq = lambda a, b: a == b or b == "t"
            _src_xy = {"a": (0, 0.5), "b": (2, 0.5), "t": (1, 2)}
            _tgt, _tgt_leq, _tgt_xy = _two, (lambda a, b: int(a) <= int(b)), _two_xy
            _on_objects = {"a": "0", "b": "0", "t": "1"}

        _A = poset_cat(_src, _src_leq)
        _B = poset_cat(_tgt, _tgt_leq)
        _F = {
            "objects": _on_objects,
            "arrows": {f: _on_objects[d] + "<=" + _on_objects[c] for f, (d, c) in _A["arrows"].items()},
        }

        def verdict(X, Y):
            found = products(_A, X, Y)
            if not found:
                return None, []
            image = [(_F["objects"][P], _F["arrows"][p1], _F["arrows"][p2]) for (P, p1, p2) in found]
            ok = all(is_product(_B, Q, q1, q2, _F["objects"][X], _F["objects"][Y]) for (Q, q1, q2) in image)
            return ok, found

        _X, _Y = pres_x.value, pres_y.value
        _ok, _found = verdict(_X, _Y)
        _FX, _FY = _F["objects"][_X], _F["objects"][_Y]
        _target_products = products(_B, _FX, _FY)

        _lines = ["**On objects:** " + ", &nbsp; ".join(x + " ↦ " + _on_objects[x] for x in _src), ""]
        if _ok is None:
            _lines.append("$X$ = `" + _X + "` and $Y$ = `" + _Y + "` have **no product** in the source. "
                          "The definition of preservation asks nothing of this pair.")
        else:
            _P = _found[0][0]
            _lines.append("Product of `" + _X + "` and `" + _Y + "` in the source: vertex `" + _P
                          + "` with projections `" + _found[0][1] + "`, `" + _found[0][2] + "`.")
            _lines.append("")
            _lines.append("Image cone in the target: vertex `" + _F["objects"][_P] + "` over `" + _FX + "` and `" + _FY + "`.")
            _lines.append("")
            if _target_products:
                _lines.append("Product of `" + _FX + "` and `" + _FY + "` in the target has vertex `" + _target_products[0][0] + "`.")
            else:
                _lines.append("`" + _FX + "` and `" + _FY + "` have no product in the target.")
            _lines.append("")
            _lines.append("**Is the image cone a product cone?** " + ("Yes: $F$ preserves this product." if _ok else "No: $F$ does not preserve this product."))
        _bad = []
        for _i, _a in enumerate(_src):
            for _b in _src[_i:]:
                if verdict(_a, _b)[0] is False:
                    _bad.append("(" + _a + ", " + _b + ")")
        _lines.append("")
        _lines.append("**All pairs whose product is not preserved:** " + (", ".join(_bad) if _bad else "none. $F$ preserves binary products."))

        def covers(elements, leq):
            return [
                (a, b) for a in elements for b in elements
                if a != b and leq(a, b) and not any(c not in (a, b) and leq(a, c) and leq(c, b) for c in elements)
            ]

        _shift = max(x for (x, _y) in _src_xy.values()) + 2.6
        _nodes = {"s:" + k: (x, y, k) for k, (x, y) in _src_xy.items()}
        _nodes.update({"t:" + k: (x + _shift, y, k) for k, (x, y) in _tgt_xy.items()})
        _arrows = [("s:" + a, "s:" + b, "") for (a, b) in covers(_src, _src_leq)]
        _arrows += [("t:" + a, "t:" + b, "") for (a, b) in covers(_tgt, _tgt_leq)]
        _fig = draw_diagram(_nodes, _arrows, figsize=(6.4, 3.6), title="source poset (left) and target poset (right)")
        return mo.vstack([_fig, mo.md("\n".join(_lines))])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try. With **inclusion**, take $X = 4$, $Y = 6$: inside $\{1, 4, 6, 12\}$ their meet is $1$, but among all divisors of $12$ the meet is $2$, which the subposet does not contain. With **gcd(-, 6)** every binary product is preserved, and yet the terminal object $12$ is sent to $6$, which is not terminal: preserving one shape of limit says nothing about another shape. With **collapse**, the pair $(a, b)$ has no product in the source, so there is nothing to preserve.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Reflecting Limits

    Reflection is the converse implication. It lets you *detect* a limit in $\mathcal{A}$ by looking at its image in $\mathcal{B}$.

    > **Definition (reflects).** A functor $F \colon \mathcal{A} \to \mathcal{B}$ **reflects limits of shape $\mathbf{I}$** if for every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every cone $(p_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$:
    > $$(F p_I \colon F A \to F D(I))_{I} \text{ is a limit cone on } F \circ D \quad\Longrightarrow\quad (p_I \colon A \to D(I))_{I} \text{ is a limit cone on } D .$$

    **Reading the definition.** You start with a cone that already lives in $\mathcal{A}$. The hypothesis is a universal property in $\mathcal{B}$; the conclusion is a universal property in $\mathcal{A}$. To prove reflection, take a test cone in $\mathcal{A}$, push it to $\mathcal{B}$, use the universal property there, and bring the mediating map back. Bringing it back is where hypotheses on $F$ are needed.

    ### Proof 3: a full and faithful functor reflects limits

    - **Goal.** Let $F \colon \mathcal{A} \to \mathcal{B}$ be full and faithful, $D \colon \mathbf{I} \to \mathcal{A}$ a diagram and $(p_I \colon A \to D(I))$ a cone on $D$ such that $(F p_I)$ is a limit cone on $F \circ D$. Then for every cone $(f_I \colon A' \to D(I))$ on $D$ there exists a unique map $h \colon A' \to A$ with $p_I h = f_I$ for all $I$.
    - **Given.** *Full:* every map $F A' \to F A$ in $\mathcal{B}$ is $F h$ for some $h \colon A' \to A$. *Faithful:* if $F h = F h'$ for $h, h' \colon A' \to A$ then $h = h'$ (1C). The universal property of $(F p_I)$. Proof 1.
    - **Plan.** Universal-property proof in $\mathcal{A}$. Existence uses fullness to pull the mediating map back, and faithfulness to pull its equations back. Uniqueness uses faithfulness.
    - **Proof.** Fix a cone $(f_I \colon A' \to D(I))$ on $D$.

        *Existence.* By Proof 1, $(F f_I \colon F A' \to F D(I))$ is a cone on $F \circ D$. Since $(F p_I)$ is a limit cone, there is a unique map $g \colon F A' \to F A$ in $\mathcal{B}$ with $F p_I \circ g = F f_I$ for all $I$. Since $F$ is full, $g = F h$ for some $h \colon A' \to A$. Then for each $I$,
        $$F(p_I \circ h) = F p_I \circ F h = F p_I \circ g = F f_I .$$
        The maps $p_I h$ and $f_I$ are both maps $A' \to D(I)$ with the same image under $F$; since $F$ is faithful, $p_I h = f_I$.

        *Uniqueness.* Let $h' \colon A' \to A$ also satisfy $p_I h' = f_I$ for all $I$. Applying $F$, $F p_I \circ F h' = F f_I$ for all $I$. So $F h'$ is a mediating map in $\mathcal{B}$ for the cone $(F f_I)$, and by the uniqueness of $g$, $F h' = g = F h$. Since $F$ is faithful, $h' = h$. $\qquad\blacksquare$
    - **What made it work.** Full and faithful means "$F$ is a bijection on each hom-set", so both the mediating map and the equations it satisfies can be transported back. Notice that the proof only needed test cones in $\mathcal{B}$ of the form $(F f_I)$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A2": (0, 2.6, r"$A'$"), "A": (0, 1.3, r"$A$"), "D": (0, 0, r"$D(I)$"),
            "FA2": (3.6, 2.6, r"$FA'$"), "FA": (3.6, 1.3, r"$FA$"), "FD": (3.6, 0, r"$FD(I)$"),
        },
        [
            ("A2", "A", r"$h$", {"dashed": True, "color": "#b91c1c"}),
            ("A", "D", r"$p_I$"),
            ("A2", "D", r"$f_I$", {"rad": 0.45}),
            ("FA2", "FA", r"$g$", {"dashed": True, "color": "#b91c1c"}),
            ("FA", "FD", r"$Fp_I$"),
            ("FA2", "FD", r"$Ff_I$", {"rad": 0.45}),
        ],
        figsize=(6.4, 3.8),
        title="Reflecting: solve in B (right), pull the solution g = Fh back to A (left)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - The inclusion $\mathbf{Ab} \to \mathbf{Grp}$ is full and faithful, so it reflects limits: a cone of abelian groups that is a limit cone in $\mathbf{Grp}$ is a limit cone in $\mathbf{Ab}$. Dualizing Proof 3, it reflects colimits too.
    - The inclusion of a subposet $P' \subseteq P$ (with the induced order) is full and faithful. So if $m \in P'$ is the meet of $x, y \in P'$ computed in $P$, it is their meet in $P'$. The interactive preset "inclusion" shows that this functor does not *preserve* meets. Reflecting and preserving are independent properties.

    **Non-examples.**

    - Let $\mathbf{1}$ be the category with one object and only its identity arrow, and $F \colon \mathbf{Set} \to \mathbf{1}$ the unique functor. Every cone in $\mathbf{1}$ is a limit cone (there is exactly one map between any two objects, and every equation holds). So the image of *every* cone in $\mathbf{Set}$ is a limit cone. If $F$ reflected limits, every cone in $\mathbf{Set}$ would be a limit cone, and 5A §4 gave a cone that is not.
    - The forgetful functor $U \colon \mathbf{Top} \to \mathbf{Set}$ does not reflect products. Give the set $\mathbb{R} \times \mathbb{R}$ the discrete topology and call the resulting space $T$. The two projections $T \to \mathbb{R}$ are continuous (every function out of a discrete space is), so $(T, \mathrm{pr}_1, \mathrm{pr}_2)$ is a cone in $\mathbf{Top}$ on the pair $(\mathbb{R}, \mathbb{R})$, and its image in $\mathbf{Set}$ is the product cone. But it is not a product in $\mathbf{Top}$: for the test cone $(\mathbb{R}^2, \mathrm{pr}_1, \mathrm{pr}_2)$ with the usual topology, the only function commuting with the projections is the identity function $\mathbb{R}^2 \to T$, which is not continuous.

    > **References.** [Leinster §5.3](https://arxiv.org/abs/1612.09375) (reflection); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Creating Limits

    For forgetful functors something stronger than preservation happens. Given groups $G$ and $H$, you compute the product of the underlying *sets*, and then discover that this set carries exactly one group structure for which the projections are homomorphisms, and that the result is the product in $\mathbf{Grp}$. The limit in $\mathbf{Set}$ *creates* the limit in $\mathbf{Grp}$.

    > **Definition (creates).** A functor $F \colon \mathcal{A} \to \mathcal{B}$ **creates limits of shape $\mathbf{I}$** if for every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every limit cone $(q_I \colon B \to F D(I))_{I \in \mathbf{I}}$ on $F \circ D$ in $\mathcal{B}$:
    >
    > 1. there exists a unique cone $(p_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$ in $\mathcal{A}$ such that $F(A) = B$ and $F(p_I) = q_I$ for all $I$; and
    > 2. this cone $(p_I)$ is a limit cone on $D$.

    **Reading the definition.** Starting from a limit cone *downstairs* (in $\mathcal{B}$), there are three things to prove: (a) **existence of a lift**, a cone upstairs lying exactly over it; (b) **uniqueness of the lift**; (c) **the lift is a limit cone** upstairs, which is itself a universal-property proof with an existence half and a uniqueness half. The equalities $F(A) = B$ and $F(p_I) = q_I$ are equalities on the nose, not isomorphisms.

    The picture: the bottom row is given, the top row is what creation provides.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 1.7, r"$A$"), "D": (2.4, 1.7, r"$D(I)$"),
            "B": (0, 0, r"$B$"), "FD": (2.4, 0, r"$FD(I)$"),
            "la": (-1.5, 1.7, r"in $\mathcal{A}$:"), "lb": (-1.5, 0, r"in $\mathcal{B}$:"),
        },
        [
            ("A", "D", r"$p_I$", {"dashed": True, "color": "#b91c1c"}),
            ("B", "FD", r"$q_I$"),
        ],
        figsize=(6.4, 2.8),
        title="Creation: (q_I) lifts uniquely to (p_I), and (p_I) is a limit cone",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proof 4: the forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ creates binary products

    - **Goal.** Let $G, H$ be groups and let $(B, q_1 \colon B \to U G, q_2 \colon B \to U H)$ be any product cone in $\mathbf{Set}$ on the underlying sets. Then (1) there is exactly one group structure on the set $B$ for which $q_1$ and $q_2$ are homomorphisms; and (2) $B$ with that structure, together with $q_1, q_2$, is a product of $G$ and $H$ in $\mathbf{Grp}$.

      This is the definition of creation for this shape: a cone $(P, p_1, p_2)$ in $\mathbf{Grp}$ with $U P = B$ and $U p_i = q_i$ is the same thing as a group structure on $B$ making $q_1, q_2$ homomorphisms.
    - **Given.** The universal property of $(B, q_1, q_2)$ in $\mathbf{Set}$, in two forms. *(E)* For every $x \in G$ and $y \in H$ there is an element $b \in B$ with $q_1(b) = x$ and $q_2(b) = y$ (apply existence to the one-element set $\{\ast\}$ and the functions $\ast \mapsto x$, $\ast \mapsto y$). *(U)* If $b, b' \in B$ satisfy $q_1(b) = q_1(b')$ and $q_2(b) = q_2(b')$ then $b = b'$ (apply the Lemma of 5A §5 to the two functions $\{\ast\} \to B$ picking out $b$ and $b'$).
    - **Plan.** Uniqueness of the group structure first, because it tells us what the structure must be. Then existence: define the forced operations and verify the group axioms, each time by comparing images under $q_1$ and $q_2$ and using (U). Finally a universal-property proof in $\mathbf{Grp}$, in which the only new thing to check is that the mediating *function* is a *homomorphism*.
    - **Proof.** *Uniqueness of the lift.* Suppose $\cdot$ is a group structure on $B$ making $q_1, q_2$ homomorphisms. Then for $b, b' \in B$ and $i = 1, 2$ we have $q_i(b \cdot b') = q_i(b)\, q_i(b')$. By (U), $b \cdot b'$ is the only element of $B$ with these two images. So the multiplication is determined by $q_1, q_2$ and the multiplications of $G$ and $H$: there is at most one such structure.

        *Existence of the lift.* For $b, b' \in B$ define $b \cdot b'$ to be the element of $B$ with
        $$q_1(b \cdot b') = q_1(b)\, q_1(b'), \qquad q_2(b \cdot b') = q_2(b)\, q_2(b');$$
        it exists by (E) and is unique by (U), so $\cdot$ is a well-defined operation on $B$. We check the group axioms.

        Associativity: for $i = 1, 2$, $q_i((b \cdot b') \cdot b'') = (q_i(b)\, q_i(b'))\, q_i(b'')$ and $q_i(b \cdot (b' \cdot b'')) = q_i(b)\, (q_i(b')\, q_i(b''))$. These are equal by associativity in $G$ and in $H$. By (U), $(b \cdot b') \cdot b'' = b \cdot (b' \cdot b'')$.

        Identity: let $e \in B$ be the element with $q_1(e) = e_G$ and $q_2(e) = e_H$. Then $q_i(e \cdot b) = q_i(e)\, q_i(b) = q_i(b)$ for $i = 1, 2$, so $e \cdot b = b$ by (U); likewise $b \cdot e = b$.

        Inverses: given $b$, let $b^{\ast} \in B$ be the element with $q_1(b^{\ast}) = q_1(b)^{-1}$ and $q_2(b^{\ast}) = q_2(b)^{-1}$. Then $q_i(b \cdot b^{\ast}) = q_i(b)\, q_i(b)^{-1}$, which is the identity of $G$ or $H$, and so equals $q_i(e)$; by (U), $b \cdot b^{\ast} = e$. Likewise $b^{\ast} \cdot b = e$.

        So $(B, \cdot)$ is a group; call it $P$. By the defining equations of $\cdot$, $q_1$ and $q_2$ preserve multiplication, so they are homomorphisms $p_1 \colon P \to G$, $p_2 \colon P \to H$ with $U p_i = q_i$.

        *The lift is a product in $\mathbf{Grp}$: existence.* Let $A$ be a group and $f_1 \colon A \to G$, $f_2 \colon A \to H$ homomorphisms. Their underlying functions form a cone in $\mathbf{Set}$, so there is a unique *function* $\bar{f} \colon U A \to B$ with $q_i \bar{f} = f_i$. We show $\bar{f}$ is a homomorphism. For $a, a' \in A$ and $i = 1, 2$:
        $$q_i\big(\bar{f}(a a')\big) = f_i(a a') = f_i(a)\, f_i(a') = q_i(\bar{f}(a))\, q_i(\bar{f}(a')) = q_i\big(\bar{f}(a) \cdot \bar{f}(a')\big),$$
        using $q_i \bar{f} = f_i$, that $f_i$ is a homomorphism, $q_i \bar{f} = f_i$ again, and the definition of $\cdot$. By (U), $\bar{f}(a a') = \bar{f}(a) \cdot \bar{f}(a')$. So $\bar{f}$ is a homomorphism $A \to P$ with $p_i \bar{f} = f_i$.

        *The lift is a product in $\mathbf{Grp}$: uniqueness.* A homomorphism $g \colon A \to P$ with $p_i g = f_i$ is in particular a function $U A \to B$ with $q_i g = f_i$. There is only one such function, namely $\bar{f}$. So $g = \bar{f}$. $\qquad\blacksquare$
    - **What made it work.** The projections of a limit in $\mathbf{Set}$ are jointly injective (U). So an equation in $B$ can be checked after applying $q_1$ and $q_2$, where it becomes an equation in $G$ and one in $H$, and those hold because $G$ and $H$ are groups. Every axiom and every homomorphism condition was verified this way. The same idea works whenever the structure is given by operations satisfying equations.

    The argument used nothing special about two factors: with one projection per object of a diagram and the same properties (E) and (U) of limits in $\mathbf{Set}$ (for a general diagram, (E) has to be restated with care, and finding the right statement is part of the exercise below), it shows that $U \colon \mathbf{Grp} \to \mathbf{Set}$ creates all limits. You carry this out for equalizers in `p05_forgetful_creates_equalizers.md`.

    **What creation buys.**

    > **Lemma.** Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor and $\mathbf{I}$ a small category. If $\mathcal{B}$ has limits of shape $\mathbf{I}$ and $F$ creates limits of shape $\mathbf{I}$, then $\mathcal{A}$ has limits of shape $\mathbf{I}$ and $F$ preserves them.

    Its proof is `p06_creation_lemma.md`, where you also show that a functor creating limits reflects them. With it, Proof 4 and its generalisation say: $\mathbf{Grp}$ has all limits, and they are computed on underlying sets.

    **Non-example.** $U \colon \mathbf{Top} \to \mathbf{Set}$ does not create products. A lift of the product cone $(\mathbb{R} \times \mathbb{R}, \mathrm{pr}_1, \mathrm{pr}_2)$ is a topology on $\mathbb{R} \times \mathbb{R}$ making both projections continuous. The product topology is one and the discrete topology is another, so the lift is not unique, and (by Section 3) one of the lifts is not a limit cone.

    **A remark on terminology.** The definition above is Leinster's. Riehl organises her definition of "creates" differently (in particular it does not require the lift to be unique) and calls the notion above *strict* creation. When reading other sources, check which is meant.

    > **References.** [Leinster §5.3](https://arxiv.org/abs/1612.09375) (creation of limits); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Forgetful Functors: the Scorecard

    We can now answer the question in the epigraph, at least descriptively.

    | Functor | Limits | Colimits |
    |---|---|---|
    | $U \colon \mathbf{Grp} \to \mathbf{Set}$ | creates them, hence preserves them | does not preserve sums or the initial object |
    | $U \colon \mathbf{Ab} \to \mathbf{Set}$, $U \colon \mathbf{Vect}_k \to \mathbf{Set}$ | creates them, hence preserves them | does not preserve sums or the initial object |
    | $U \colon \mathbf{Top} \to \mathbf{Set}$ | preserves them; does not reflect or create them | preserves them; does not reflect them |
    | inclusion $\mathbf{Ab} \to \mathbf{Grp}$ | preserves binary products; reflects all limits | reflects them; does not preserve sums |

    **Justifications.**

    - *Algebraic rows, limits.* Proof 4 and the remark after it for groups. The proof used only that the structure consists of operations satisfying equations, and it goes through in the same way for abelian groups and vector spaces. "Hence preserves" is the Lemma of Section 4, since $\mathbf{Set}$ has all limits (5A §6).
    - *Algebraic rows, colimits.* The initial object of $\mathbf{Grp}$, $\mathbf{Ab}$ and $\mathbf{Vect}_k$ has a one-element underlying set, which is not initial in $\mathbf{Set}$. For sums: in each of these categories the two coprojections $i_1, i_2$ of a sum are homomorphisms, so both send the identity element to the identity element of the sum, and their images overlap. In $\mathbf{Set}$ the two coprojections of a sum have disjoint images (this holds for the disjoint union, and every sum is isomorphic to it compatibly with the coprojections). So the underlying cocone of a sum of groups is never a sum of sets. For instance the sum of $\mathbb{Z}$ and $\mathbb{Z}$ in $\mathbf{Ab}$ has underlying set $\mathbb{Z} \times \mathbb{Z}$ with coprojections $x \mapsto (x, 0)$ and $y \mapsto (0, y)$.
    - *$\mathbf{Top}$.* Products, equalizers, sums and coequalizers in $\mathbf{Top}$ are the corresponding constructions on underlying sets, equipped with a suitable topology (5A and 5B), so $U$ preserves these four kinds. Every limit is isomorphic to one built from products and an equalizer as in 5A §7, and $U$ carries that construction in $\mathbf{Top}$ to the same construction in $\mathbf{Set}$; with Proof 2 this gives preservation of all limits, and dually of all colimits. The failures of reflection and creation for limits are the non-examples of Sections 3 and 4. For colimits: the two-point set with the indiscrete topology is the vertex of a cocone over two one-point spaces whose image in $\mathbf{Set}$ is a sum, but it is not a sum in $\mathbf{Top}$, because the mediating function to the discrete two-point space is not continuous.
    - *$\mathbf{Ab} \to \mathbf{Grp}$.* Section 2 and Proof 3.

    The pattern (forgetful functors from algebra respect limits and not colimits) is not a coincidence. Each forgetful functor from $\mathbf{Grp}$, $\mathbf{Ab}$ or $\mathbf{Vect}_k$ to $\mathbf{Set}$ has a left adjoint, the free functor (2A), and 6C proves that every functor with a left adjoint preserves limits. $U \colon \mathbf{Top} \to \mathbf{Set}$ has adjoints on both sides (2A), which is why it respects both.

    > **References.** [Leinster §5.3](https://arxiv.org/abs/1612.09375); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf), [§3.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Limits in Functor Categories Are Computed Pointwise

    Functor categories $[\mathcal{A}, \mathcal{S}]$ (1D) are where the rest of the course lives: presheaves are objects of $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$. How do you take the product of two functors $X, Y \colon \mathcal{A} \to \mathbf{Set}$? The natural guess is: one object at a time,
    $$(X \times Y)(A) = X(A) \times Y(A).$$
    The guess is right, and it is an instance of a preservation statement about the evaluation functors.

    > **Definition (evaluation).** For an object $A$ of $\mathcal{A}$, the **evaluation functor** $\mathrm{ev}_A \colon [\mathcal{A}, \mathcal{S}] \to \mathcal{S}$ sends a functor $X$ to the object $X(A)$ and a natural transformation $\alpha \colon X \Rightarrow Y$ to its component $\alpha_A \colon X(A) \to Y(A)$.

    **Reading the definition.** $\mathrm{ev}_A$ is a functor because identities and composites of natural transformations are computed componentwise (1D). A diagram $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ therefore gives, for each $A$, a diagram $\mathrm{ev}_A \circ D \colon \mathbf{I} \to \mathcal{S}$, written $D(-)(A)$: it sends $I$ to the object $D(I)(A)$.

    > **Theorem (limits in functor categories are pointwise).** Let $\mathcal{A}$ and $\mathbf{I}$ be small categories and $\mathcal{S}$ a locally small category. Let $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ be a diagram, and suppose that for each object $A$ of $\mathcal{A}$ the diagram $D(-)(A) \colon \mathbf{I} \to \mathcal{S}$ has a limit. Then:
    >
    > 1. there is a cone on $D$ whose image under $\mathrm{ev}_A$ is a limit cone on $D(-)(A)$ for every object $A$ of $\mathcal{A}$;
    > 2. any cone on $D$ with that property is a limit cone on $D$.
    >
    > Consequently, if $\mathcal{S}$ has all limits of shape $\mathbf{I}$, then so does $[\mathcal{A}, \mathcal{S}]$, and every evaluation functor $\mathrm{ev}_A$ preserves them. The dual statements hold for colimits.

    **The proof is in 6B.** It needs one idea beyond this module: the pointwise limits $L(A) = \lim D(-)(A)$ must be assembled into a *functor* $L \colon \mathcal{A} \to \mathcal{S}$, and the maps $L(a) \colon L(A) \to L(A')$ come from the universal property. (You will see the same manoeuvre in Proof 5 below, in a simpler setting.) Here we only use the statement.

    **Examples.**

    - **Pairs.** If $\mathcal{A}$ is the discrete category with two objects, $[\mathcal{A}, \mathbf{Set}]$ is the category of pairs of sets, and the theorem says limits of pairs are computed in each coordinate.
    - **Functions.** If $\mathcal{A}$ has two objects and one non-identity arrow $0 \to 1$, an object of $[\mathcal{A}, \mathbf{Set}]$ is a function $X_0 \to X_1$. The product of $f \colon X_0 \to X_1$ and $g \colon Y_0 \to Y_1$ is the function $X_0 \times Y_0 \to X_1 \times Y_1$, $(x, y) \mapsto (f(x), g(y))$.
    - **Group actions.** For a group $G$ regarded as a one-object category, $[G, \mathbf{Set}]$ is the category of $G$-sets (a functor $G \to \mathbf{Set}$ is a set with a $G$-action, as in 5A §4, and a natural transformation is a function commuting with the action). The product of $G$-sets $X$ and $Y$ has underlying set $X \times Y$; the theorem also dictates the action, $g \cdot (x, y) = (g \cdot x, g \cdot y)$. Sums are disjoint unions, with $G$ acting on each piece.
    - **Terminal presheaf.** The terminal object of $[\mathcal{A}, \mathbf{Set}]$ is the functor sending every object to a one-element set.

    **A caution (non-example of the reasoning).** The theorem needs the pointwise limits to exist. When $\mathcal{S}$ lacks some limits of shape $\mathbf{I}$, the theorem does not say that every limit that happens to exist in $[\mathcal{A}, \mathcal{S}]$ is computed pointwise. Statement 2 is about cones that are *known* to be pointwise limits.

    > **References.** [Leinster §6.2](https://arxiv.org/abs/1612.09375) (statement and proof; treated in module 6B); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Limits Commute with Limits

    The set $(A \times B) \times (C \times D)$ and the set $(A \times C) \times (B \times D)$ are in bijection: both are "all four coordinates". Taking an equalizer of a product of maps gives the product of the equalizers. These are instances of one theorem: when a diagram depends on two indices, you may take the limit over one index and then the other, in either order.

    **Setting.** Let $\mathbf{I}$ and $\mathbf{J}$ be small categories and $D \colon \mathbf{I} \times \mathbf{J} \to \mathcal{A}$ a functor (product categories are from 1B). Write $D(u, J)$ for $D(u, 1_J)$ and $D(I, v)$ for $D(1_I, v)$. Every arrow of $\mathbf{I} \times \mathbf{J}$ factors as $(u, v) = (u, 1_{J'}) \circ (1_I, v)$ for $u \colon I \to I'$, $v \colon J \to J'$, so by functoriality
    $$D(u, v) = D(u, J') \circ D(I, v). \tag{$\ast$}$$
    Also $(u, 1_{J'}) \circ (1_I, v) = (1_{I'}, v) \circ (u, 1_J)$, so
    $$D(u, J') \circ D(I, v) = D(I', v) \circ D(u, J). \tag{$\ast\ast$}$$
    For each fixed $I$, $D(I, -) \colon \mathbf{J} \to \mathcal{A}$ is a diagram of shape $\mathbf{J}$.

    > **Theorem.** Suppose that for each object $I$ of $\mathbf{I}$ the diagram $D(I, -)$ has a limit, and choose a limit cone $(\pi_{I,J} \colon L_I \to D(I, J))_{J \in \mathbf{J}}$ for each $I$. Then:
    >
    > 1. the objects $L_I$ are the values of a functor $L \colon \mathbf{I} \to \mathcal{A}$, whose value on $u \colon I \to I'$ is the unique map $L_u \colon L_I \to L_{I'}$ with $\pi_{I',J} \circ L_u = D(u, J) \circ \pi_{I,J}$ for all $J$;
    > 2. if $(\mu_I \colon M \to L_I)_{I \in \mathbf{I}}$ is a limit cone on $L$, then $(\pi_{I,J} \circ \mu_I \colon M \to D(I, J))_{(I,J) \in \mathbf{I} \times \mathbf{J}}$ is a limit cone on $D$.
    >
    > In symbols: $\ \lim_{\mathbf{I}} \lim_{\mathbf{J}} D(I, J)$ is a limit of $D$ over $\mathbf{I} \times \mathbf{J}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (-2.2, 2.7, r"$A$"), "M": (-2.2, 0.85, r"$M$"),
            "LI": (0, 1.7, r"$L_I$"), "LI2": (0, 0, r"$L_{I'}$"),
            "DIJ": (2.6, 1.7, r"$D(I,J)$"), "DI2J": (2.6, 0, r"$D(I',J)$"),
        },
        [
            ("LI", "DIJ", r"$\pi_{I,J}$"),
            ("LI2", "DI2J", r"$\pi_{I',J}$", {"side": -1}),
            ("LI", "LI2", r"$L_u$", {"dashed": True, "side": -1, "color": "#b91c1c"}),
            ("DIJ", "DI2J", r"$D(u,J)$"),
            ("M", "LI", r"$\mu_I$"),
            ("M", "LI2", r"$\mu_{I'}$", {"side": -1}),
            ("A", "M", r"$h$", {"dashed": True, "side": -1, "color": "#b91c1c"}),
            ("A", "LI", r"$g_I$", {"dashed": True, "color": "#b91c1c"}),
        ],
        figsize=(8.0, 4.4),
        title="Limits over J first (the L's), then over I (the object M)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proof 5: an iterated limit is a limit over the product category

    - **Goal.** Statements 1 and 2 of the theorem. For 2: for every cone $(f_{I,J} \colon A \to D(I, J))$ on $D$ there exists a unique $h \colon A \to M$ with $\pi_{I,J}\, \mu_I\, h = f_{I,J}$ for all $I, J$.
    - **Given.** The universal property of each $(L_I, (\pi_{I,J})_J)$ and of $(M, (\mu_I)_I)$; the Lemma of 5A §5 for each of them (maps into a limit are equal if their composites with all projections are equal); equations $(\ast)$ and $(\ast\ast)$.
    - **Plan.** Every map into some $L_I$ will be produced by the universal property of $L_I$ and every equation between maps into $L_I$ will be proved by the Lemma. Then the universal property of $M$ is used once. Existence and uniqueness for $D$ are each done in two layers: first the $\mathbf{J}$-direction, then the $\mathbf{I}$-direction.
    - **Proof.** *Statement 1: $L_u$ exists.* Let $u \colon I \to I'$. The maps $D(u, J) \circ \pi_{I,J} \colon L_I \to D(I', J)$ form a cone on $D(I', -)$: for $v \colon J \to J'$,
      $$D(I', v) \circ D(u, J) \circ \pi_{I,J} = D(u, J') \circ D(I, v) \circ \pi_{I,J} = D(u, J') \circ \pi_{I,J'},$$
      by $(\ast\ast)$ and then the cone equation of $(\pi_{I,J})_J$. So the universal property of $L_{I'}$ gives a unique $L_u$ with $\pi_{I',J} L_u = D(u, J)\, \pi_{I,J}$ for all $J$.

        *Statement 1: functoriality.* For $u = 1_I$: the map $1_{L_I}$ satisfies $\pi_{I,J} 1_{L_I} = D(1_I, 1_J)\, \pi_{I,J}$, since $D(1_I, 1_J)$ is an identity; by uniqueness $L_{1_I} = 1_{L_I}$. For $u \colon I \to I'$ and $u' \colon I' \to I''$:
        $$\pi_{I'',J}\, L_{u'} L_u = D(u', J)\, \pi_{I',J}\, L_u = D(u', J)\, D(u, J)\, \pi_{I,J} = D(u' u, J)\, \pi_{I,J},$$
        using the defining property of $L_{u'}$, then of $L_u$, then functoriality of $D$. So $L_{u'} L_u$ has the property that characterises $L_{u' u}$; by uniqueness $L_{u'} L_u = L_{u' u}$.

        *Statement 2: the family is a cone on $D$.* Put $r_{I,J} = \pi_{I,J}\, \mu_I$. For an arrow $(u, v) \colon (I, J) \to (I', J')$:
        $$D(u, v)\, r_{I,J} = D(u, J')\, D(I, v)\, \pi_{I,J}\, \mu_I = D(u, J')\, \pi_{I,J'}\, \mu_I = \pi_{I',J'}\, L_u\, \mu_I = \pi_{I',J'}\, \mu_{I'} = r_{I',J'},$$
        using $(\ast)$; the cone equation of $(\pi_{I,J})_J$; the defining property of $L_u$; and the cone equation $L_u \mu_I = \mu_{I'}$ of $(\mu_I)$.

        *Statement 2: existence of the mediating map.* Let $(f_{I,J} \colon A \to D(I, J))$ be a cone on $D$.

        Layer 1 ($\mathbf{J}$-direction). Fix $I$. The cone equations of $(f_{I,J})$ for the arrows $(1_I, v)$ say $D(I, v) f_{I,J} = f_{I,J'}$, so $(f_{I,J})_J$ is a cone on $D(I, -)$. Hence there is a unique $g_I \colon A \to L_I$ with $\pi_{I,J}\, g_I = f_{I,J}$ for all $J$.

        Layer 2 ($\mathbf{I}$-direction). We claim $(g_I)_I$ is a cone on $L$, that is, $L_u g_I = g_{I'}$ for $u \colon I \to I'$. Both sides are maps $A \to L_{I'}$, so by the Lemma it suffices to compare them after each $\pi_{I',J}$:
        $$\pi_{I',J}\, L_u\, g_I = D(u, J)\, \pi_{I,J}\, g_I = D(u, J)\, f_{I,J} = f_{I',J} = \pi_{I',J}\, g_{I'},$$
        where the third equality is the cone equation of $(f_{I,J})$ for the arrow $(u, 1_J)$. So $(g_I)$ is a cone on $L$, and there is a unique $h \colon A \to M$ with $\mu_I h = g_I$ for all $I$. Then $r_{I,J}\, h = \pi_{I,J}\, \mu_I\, h = \pi_{I,J}\, g_I = f_{I,J}$.

        *Statement 2: uniqueness of the mediating map.* Let $h' \colon A \to M$ satisfy $\pi_{I,J}\, \mu_I\, h' = f_{I,J}$ for all $I, J$.

        Layer 1. Fix $I$. The map $\mu_I h' \colon A \to L_I$ satisfies $\pi_{I,J} (\mu_I h') = f_{I,J}$ for all $J$; so does $g_I$, uniquely. Hence $\mu_I h' = g_I$.

        Layer 2. So $h'$ satisfies $\mu_I h' = g_I$ for all $I$; so does $h$, uniquely. Hence $h' = h$. $\qquad\blacksquare$
    - **What made it work.** The universal property of a limit was used in two roles: to *construct* maps into it ($L_u$, $g_I$, $h$) and, through the Lemma, to *compare* maps into it. A cone over $\mathbf{I} \times \mathbf{J}$ was split into its $\mathbf{J}$-part and its $\mathbf{I}$-part, exactly as the cone in Proof 8 of 5A was split into a product part and an equalizer part.

    **Corollary (interchange).** Exchanging the roles of $\mathbf{I}$ and $\mathbf{J}$ in the theorem, $\lim_{\mathbf{J}} \lim_{\mathbf{I}} D(I, J)$ is also a limit of $D$, whenever those limits exist. By the uniqueness of limits (5A, Proof 5), when both iterated limits exist there is a unique isomorphism
    $$\boxed{\;\lim_{\mathbf{I}} \lim_{\mathbf{J}} D(I, J) \;\cong\; \lim_{\mathbf{J}} \lim_{\mathbf{I}} D(I, J)\;}$$
    compatible with the projections to every $D(I, J)$. By duality, colimits commute with colimits.

    **Examples.**

    - $\mathbf{I}$ and $\mathbf{J}$ both discrete with two objects: $(A \times B) \times (C \times D) \cong (A \times C) \times (B \times D)$ in any category with binary products.
    - $\mathbf{I}$ discrete with two objects, $\mathbf{J}$ a parallel pair: for $s, t \colon X \to Y$ and $s', t' \colon X' \to Y'$, the equalizer of $s \times s'$ and $t \times t'$ is the product of the equalizer of $(s, t)$ with the equalizer of $(s', t')$. In $\mathbf{Set}$: $(x, x')$ satisfies both equations exactly when $x$ satisfies the first and $x'$ the second.
    - In a poset with all meets: $\bigwedge_i \bigwedge_j x_{ij} = \bigwedge_j \bigwedge_i x_{ij}$.

    **Non-example: limits do not commute with colimits in general.** In $\mathbf{Set}$, take four sets $A, B, C, D$. "Sum of products" and "product of sums" are
    $$(A \times C) + (B \times D) \qquad\text{and}\qquad (A + B) \times (C + D),$$
    with $ac + bd$ and $(a + b)(c + d)$ elements respectively when the sets are finite of sizes $a, b, c, d$. For one-element sets these numbers are $2$ and $4$. There is a comparison map from the first to the second, and it is not a bijection. Which limits commute with which colimits is a delicate question; one positive result, proved in Riehl §3.8, is that in $\mathbf{Set}$ finite limits commute with *filtered* colimits.

    > **References.** [Leinster §6.2](https://arxiv.org/abs/1612.09375) (limits commute with limits); [Riehl §3.8](https://math.jhu.edu/~eriehl/context.pdf) (interchange of limits and colimits).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **"$F(X \times Y) \cong F X \times F Y$, so $F$ preserves the product."** *Diagnosis:* preservation is about the specific cone $(F p_1, F p_2)$, equivalently about the comparison map. An unrelated isomorphism, or an equality of cardinalities, proves nothing. Compute It, Exercise 1 gives a functor where the two sides have the same number of elements and the product is not preserved.
    2. **Testing the image cone only against cones that come from $\mathcal{A}$.** *Diagnosis:* to show $(F p_I)$ is a limit cone in $\mathcal{B}$ you must handle every cone in $\mathcal{B}$ on $F \circ D$, including those whose vertex is not of the form $F A'$. (For *reflection* the test cones do come from $\mathcal{A}$; do not mix the two up.)
    3. **Mixing up the directions of preserve and reflect.** *Diagnosis:* write the implication out. Preserve: limit cone in $\mathcal{A}$ $\Rightarrow$ image is a limit cone in $\mathcal{B}$. Reflect: image is a limit cone in $\mathcal{B}$ $\Rightarrow$ limit cone in $\mathcal{A}$. Neither implies the other.
    4. **In a creation proof, forgetting that the mediating function must be a morphism upstairs.** "The function $\bar{f}$ exists by the universal property in $\mathbf{Set}$, done." *Diagnosis:* the universal property in $\mathbf{Grp}$ asks for a *homomorphism*. Showing $\bar{f}$ is one is the real content.
    5. **Refuting preservation with a diagram that has no limit.** *Diagnosis:* the definition is an implication whose hypothesis is "this cone is a limit cone in $\mathcal{A}$". A counterexample must exhibit an actual limit cone in $\mathcal{A}$ whose image fails.

    ---

    ## Why This Matters

    - **6A** proves that representable functors $\mathcal{A}(A, -)$ preserve limits, and in fact that this is a restatement of the definition of limit. The vocabulary of Section 2 is what makes the statement possible.
    - **6B** proves the pointwise theorem of Section 6 and uses it to show that every presheaf is a colimit of representables. Proof 5 is a rehearsal for its main construction.
    - **6C** proves that right adjoints preserve limits and left adjoints preserve colimits. That single theorem explains the whole scorecard of Section 5, and its converse direction (the adjoint functor theorems) asks when a limit-preserving functor has a left adjoint.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    ### Exercise 1: Same size, still not preserved

    The covariant power-set functor $\mathcal{P} \colon \mathbf{Set} \to \mathbf{Set}$ sends a set to the set of its subsets and a function $f$ to the direct-image function $S \mapsto f(S) = \{f(x) : x \in S\}$. For $X = Y = \{0, 1\}$ the comparison map of Section 1 is
    $$c \colon \mathcal{P}(X \times Y) \to \mathcal{P}(X) \times \mathcal{P}(Y), \qquad c(S) = \big(\mathrm{pr}_1(S),\ \mathrm{pr}_2(S)\big).$$
    Compute $c$ on every subset $S$ and decide whether it is injective and whether it is surjective. Both sides have $16$ elements.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        X = [0, 1]
        Y = [0, 1]
        product = list(itertools.product(X, Y))

        def subsets(elements):
            return [
                frozenset(_c)
                for _r in range(len(elements) + 1)
                for _c in itertools.combinations(elements, _r)
            ]

        domain = subsets(product)                                              # P(X x Y)
        codomain = [(_s, _t) for _s in subsets(X) for _t in subsets(Y)]        # P(X) x P(Y)

        def comparison(S):
            # TODO: return the pair (direct image of S under pr1, direct image of S under pr2),
            #       each as a frozenset
            _pair = ...
            return _pair

        # TODO: the set of all values of `comparison` on `domain`
        image = ...

        # print(len(domain), len(codomain))        # expected: 16 16
        # print(len(image))                        # expected: 10
        # print(len(image) == len(domain))         # injective?  expected: False
        # print(len(image) == len(codomain))       # surjective? expected: False

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Sums of products versus products of sums

    For finite sets $A, B, C, D$, build the comparison function of Section 7,
    $$k \colon (A \times C) + (B \times D) \to (A + B) \times (C + D),$$
    which sends $((a, c), 1)$ to $((a, 1), (c, 1))$ and $((b, d), 2)$ to $((b, 2), (d, 2))$. Elements of a sum are tagged pairs `(element, tag)`. Decide whether $k$ is injective and whether it is surjective.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        A, B, C, D = ["a1", "a2"], ["b1", "b2", "b3"], ["c1", "c2"], ["d1"]

        def tagged_sum(S, T):
            return [(_x, 1) for _x in S] + [(_y, 2) for _y in T]

        sum_of_products = tagged_sum(list(itertools.product(A, C)), list(itertools.product(B, D)))
        product_of_sums = list(itertools.product(tagged_sum(A, B), tagged_sum(C, D)))

        def k(element):
            (_first, _second), _tag = element
            # TODO: return the corresponding element of product_of_sums
            return ...

        # TODO: the list of values of k on sum_of_products
        values = ...

        # print(len(sum_of_products), len(product_of_sums))     # expected: 7 15
        # print(all(v in product_of_sums for v in values))      # expected: True
        # print(len(set(values)) == len(sum_of_products))       # injective?  expected: True
        # print(len(set(values)) == len(product_of_sums))       # surjective? expected: False

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Does this functor preserve the terminal object?

    A terminal object is the limit of the empty diagram, so "preserves terminal objects" is a preservation statement that the product widget above does not test. Using the finite-category encoding, write

    - `terminal_objects(cat)`: the list of objects $T$ such that every object $A$ has exactly one arrow $A \to T$;
    - `preserves_terminal(F, cat1, cat2)`: `True` when $F$ sends every terminal object of `cat1` to a terminal object of `cat2`.

    The scaffolding builds the divisors of $12$ as a category, two functors from it to itself, and the two-element group as a one-object category.
    """)
    return


@app.cell
def _():
    def _run():
        import math

        def poset_cat(elements, leq):
            arrows = {a + "<=" + b: (a, b) for a in elements for b in elements if leq(a, b)}
            identity = {a: a + "<=" + a for a in elements}
            compose = {
                (g, f): arrows[f][0] + "<=" + arrows[g][1]
                for f in arrows for g in arrows if arrows[f][1] == arrows[g][0]
            }
            return {"objects": list(elements), "arrows": arrows, "identity": identity, "compose": compose}

        def functor_from_map(cat, on_objects):
            return {
                "objects": dict(on_objects),
                "arrows": {f: on_objects[d] + "<=" + on_objects[c] for f, (d, c) in cat["arrows"].items()},
            }

        d12 = poset_cat(["1", "2", "3", "4", "6", "12"], lambda a, b: int(b) % int(a) == 0)
        F_gcd6 = functor_from_map(d12, {x: str(math.gcd(int(x), 6)) for x in d12["objects"]})
        F_lcm2 = functor_from_map(d12, {x: str(math.lcm(int(x), 2)) for x in d12["objects"]})

        z2 = {
            "objects": ["*"],
            "arrows": {"e": ("*", "*"), "g": ("*", "*")},
            "identity": {"*": "e"},
            "compose": {("e", "e"): "e", ("e", "g"): "g", ("g", "e"): "g", ("g", "g"): "e"},
        }

        def terminal_objects(cat):
            # TODO: objects T such that for every object A, exactly one arrow has (domain, codomain) == (A, T)
            _result = ...
            return _result

        def preserves_terminal(F, cat1, cat2):
            # TODO: every terminal object T of cat1 has F["objects"][T] terminal in cat2
            _result = ...
            return _result

        # print(terminal_objects(d12))                    # expected: ['12']
        # print(terminal_objects(z2))                     # expected: []
        # print(preserves_terminal(F_gcd6, d12, d12))     # expected: False
        # print(preserves_terminal(F_lcm2, d12, d12))     # expected: True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | Composites of limit-preserving functors — `exercises/5c/p01_composite_preserves.md` | warm-up | unpacking a definition twice |
    | 2 | A functor that does not preserve products — `exercises/5c/p02_product_with_c_fails.md` | warm-up | counterexample to preservation |
    | 3 | Pullback-preserving functors preserve monics — `exercises/5c/p03_preserves_monics.md` | core | converting a property into a limit |
    | 4 | The comparison map — `exercises/5c/p04_comparison_map.md` | core | uniqueness of limits, in both directions |
    | 5 | The forgetful functor creates equalizers — `exercises/5c/p05_forgetful_creates_equalizers.md` | core | creation proof, imitating a model |
    | 6 | Creation gives existence, preservation and reflection — `exercises/5c/p06_creation_lemma.md` | stretch | chaining universal properties |

    Write each proof in `proofs/5c/` under the same filename as its brief, using the five-step proof anatomy of this lecture.
    Then ask Claude to review it: the review points at gaps and asks questions; it does not hand you a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [5B: Colimits](../5b_colimits/) &nbsp;|&nbsp; Next: [6A: Limits via Representables & Adjoints](../6a_limits_representables_adjoints/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
