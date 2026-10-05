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
    # 1D: Natural Transformations

    > *"... 'functor' has been defined in order to be able to define 'natural transformation'."*
    > — Saunders Mac Lane, *Categories for the Working Mathematician*

    You now have two layers of the language: **categories** (1A, 1B) and **functors**, the maps between categories (1C). This module adds the third and last layer: maps between *functors*. Given two functors $F, G \colon \mathcal{A} \to \mathcal{B}$ with the same domain and the same codomain, a **natural transformation** $\alpha \colon F \Rightarrow G$ is a way of comparing them, one object of $\mathcal{A}$ at a time, that is compatible with every arrow of $\mathcal{A}$.

    The word "natural" was in use in mathematics long before it had a definition. People said that a finite-dimensional vector space is "naturally" isomorphic to its double dual but not to its dual, or that the determinant is defined "in the same way for every ring". Category theory was invented to turn that feeling into a statement that can be proved or refuted. The statement is a single equation between two composite arrows, and it has a shape: a commuting square.

    **What you will be able to prove by the end.** Given a family of arrows, you will be able to decide whether it is a natural transformation by writing down the naturality square and checking it. You will prove that natural transformations compose in two different ways (vertically and horizontally), that functors $\mathcal{A} \to \mathcal{B}$ and natural transformations between them form a category $[\mathcal{A}, \mathcal{B}]$, and you will know what "naturally isomorphic" means precisely. The proof technique of this module is always the same: **draw the square, name the arrow at which you use naturality, and paste squares together.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Definition and the Naturality Square

    Suppose $F$ and $G$ are two functors from $\mathcal{A}$ to $\mathcal{B}$. For each object $A$ of $\mathcal{A}$ they give two objects $F(A)$ and $G(A)$ of $\mathcal{B}$. To compare $F$ with $G$ we should at least choose, for every $A$, an arrow $F(A) \to G(A)$. But a functor is more than what it does on objects: it also acts on arrows. So the chosen arrows should respect what $F$ and $G$ do to each arrow $f$ of $\mathcal{A}$. That requirement is the whole definition.

    > **Definition (natural transformation).** Let $\mathcal{A}$ and $\mathcal{B}$ be categories and let $F, G \colon \mathcal{A} \to \mathcal{B}$ be functors. A **natural transformation** $\alpha \colon F \Rightarrow G$ is a family
    > $$\big(\alpha_A \colon F(A) \to G(A)\big)_{A \in \mathcal{A}}$$
    > of arrows of $\mathcal{B}$, one for each object $A$ of $\mathcal{A}$, such that **for every arrow** $f \colon A \to A'$ of $\mathcal{A}$,
    > $$\boxed{\,G(f) \circ \alpha_A \;=\; \alpha_{A'} \circ F(f)\,}$$
    > The arrow $\alpha_A$ is called the **component of $\alpha$ at $A$**. The equation is called **naturality of $\alpha$ at $f$**, and it says that the square below commutes.

    **Reading the definition.** To show that something is a natural transformation $F \Rightarrow G$ you must check, in this order:

    1. $F$ and $G$ are functors with the **same** domain $\mathcal{A}$ and the **same** codomain $\mathcal{B}$, and of the same variance. (If one is covariant and the other contravariant, the definition does not apply.)
    2. For **each** object $A$ of $\mathcal{A}$ you have **one** arrow $\alpha_A$, and it is an arrow of $\mathcal{B}$ with domain $F(A)$ and codomain $G(A)$. If $\mathcal{B}$ is $\mathbf{Grp}$ or $\mathbf{Vect}_k$, this includes checking that $\alpha_A$ is a homomorphism or a linear map.
    3. For **every** arrow $f \colon A \to A'$ of $\mathcal{A}$, the two arrows $G(f) \circ \alpha_A$ and $\alpha_{A'} \circ F(f)$, both of which go from $F(A)$ to $G(A')$, are equal.

    Notice the quantifiers in step 3: one family $\alpha$, fixed in advance, must work for all $f$ at once. You are not allowed to choose the components after seeing $f$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "tl": (0.0, 1.7, r"$F(A)$"),
            "tr": (3.0, 1.7, r"$F(A')$"),
            "bl": (0.0, 0.0, r"$G(A)$"),
            "br": (3.0, 0.0, r"$G(A')$"),
            # unlabelled anchor points, so that horizontal arrows clear the wide node labels
            "tl+": (0.3, 1.7, ""),
            "tr-": (2.7, 1.7, ""),
            "bl+": (0.3, 0.0, ""),
            "br-": (2.7, 0.0, ""),
        },
        [
            ("tl+", "tr-", r"$F(f)$", {"side": -1}),
            ("tl", "bl", r"$\quad\alpha_A$"),
            ("tr", "br", r"$\quad\alpha_{A'}$"),
            ("bl+", "br-", r"$G(f)$"),
        ],
        figsize=(5.0, 3.2),
        title=r"Naturality of $\alpha$ at $f$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example 1 (identity).** For any functor $F \colon \mathcal{A} \to \mathcal{B}$ the family $(1_{F(A)})_{A \in \mathcal{A}}$ is a natural transformation $1_F \colon F \Rightarrow F$. Check: for $f \colon A \to A'$ the two sides of the naturality equation are $F(f) \circ 1_{F(A)}$ and $1_{F(A')} \circ F(f)$, and both equal $F(f)$ by the identity axioms of $\mathcal{B}$.

    **Example 2 (the determinant).** Let $\mathbf{CRing}$ be the category of commutative rings and ring homomorphisms (which preserve $0$, $1$, $+$ and $\times$), and let $\mathbf{Mon}$ be the category of monoids. Fix $n \geq 1$. There are two functors $\mathbf{CRing} \to \mathbf{Mon}$:

    - $M_n$ sends a ring $R$ to the monoid $M_n(R)$ of $n \times n$ matrices over $R$ under matrix multiplication, and a ring homomorphism $\varphi \colon R \to S$ to the map $M_n(\varphi)$ that applies $\varphi$ to every entry;
    - $U$ sends $R$ to the monoid $(R, \times, 1)$, forgetting addition, and $\varphi$ to itself.

    For each ring $R$ the determinant is a function $\det_R \colon M_n(R) \to U(R)$, and it is a monoid homomorphism because $\det(XY) = \det(X)\det(Y)$ and $\det(I) = 1$. So we have a family of arrows of $\mathbf{Mon}$ of the right kind (step 2 of the checklist). Step 3 is the proposition below.

    **Non-example (a family that is not natural).** Take $F = G = 1_{\mathbf{Set}}$, the identity functor on $\mathbf{Set}$. Define a family by: $\alpha_X$ is the function swapping $0$ and $1$ when $X = \{0, 1\}$, and $\alpha_X = 1_X$ for every other set $X$. Each $\alpha_X$ is an arrow $X \to X$, so step 2 is satisfied. But naturality fails at the function $f \colon \{\ast\} \to \{0, 1\}$ with $f(\ast) = 0$:
    $$\big(G(f) \circ \alpha_{\{\ast\}}\big)(\ast) = f(\ast) = 0, \qquad \big(\alpha_{\{0,1\}} \circ F(f)\big)(\ast) = \alpha_{\{0,1\}}(0) = 1.$$
    One failing square is enough: this family is **not** a natural transformation, even though every component is a perfectly good bijection. Naturality is a property of the whole family, not of its members.

    ### The determinant is natural

    **Proposition 1.** The family $(\det_R)_{R \in \mathbf{CRing}}$ is a natural transformation $\det \colon M_n \Rightarrow U$.

    - **Goal.** For every ring homomorphism $\varphi \colon R \to S$ between commutative rings and every matrix $X \in M_n(R)$,
      $$\varphi(\det\nolimits_R X) = \det\nolimits_S\big(M_n(\varphi)(X)\big).$$
      This is the equation $U(\varphi) \circ \det_R = \det_S \circ M_n(\varphi)$ evaluated at $X$; two functions with the same domain and codomain are equal exactly when they agree at every element (0B).
    - **Given.** The Leibniz formula $\det X = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, x_{1\sigma(1)} x_{2\sigma(2)} \cdots x_{n\sigma(n)}$, valid over any commutative ring, where $\operatorname{sgn}(\sigma) \in \{1, -1\}$. The definition of a ring homomorphism: $\varphi(a + b) = \varphi(a) + \varphi(b)$, $\varphi(ab) = \varphi(a)\varphi(b)$, $\varphi(1) = 1$.
    - **Plan.** Direct computation: push $\varphi$ through the Leibniz formula one operation at a time.
    - **Proof.** Write $X = (x_{ij})$, so $M_n(\varphi)(X)$ has entries $\varphi(x_{ij})$. From $\varphi(a+b) = \varphi(a)+\varphi(b)$ we get $\varphi(0) = 0$ and hence $\varphi(-a) = -\varphi(a)$; together with $\varphi(1) = 1$ this gives $\varphi(\operatorname{sgn}(\sigma) \cdot a) = \operatorname{sgn}(\sigma) \cdot \varphi(a)$ for every $a \in R$. Then
      $$\varphi(\det\nolimits_R X) = \varphi\Big(\sum_{\sigma} \operatorname{sgn}(\sigma) \prod_{i} x_{i\sigma(i)}\Big) = \sum_{\sigma} \operatorname{sgn}(\sigma)\, \varphi\Big(\prod_{i} x_{i\sigma(i)}\Big) = \sum_{\sigma} \operatorname{sgn}(\sigma) \prod_{i} \varphi(x_{i\sigma(i)}),$$
      where the second equality uses that $\varphi$ preserves sums and signs, and the third that $\varphi$ preserves products. The right-hand side is the Leibniz formula for the matrix with entries $\varphi(x_{ij})$, that is, $\det_S(M_n(\varphi)(X))$. $\blacksquare$
    - **What made it work.** The determinant is given by *one formula built only from ring operations*, and ring homomorphisms preserve ring operations. Whenever a family of maps is "given by the same formula for every object", this is the argument to reach for.

    The cell below checks one naturality square numerically, for the reduction homomorphism $\varphi \colon \mathbb{Z} \to \mathbb{Z}/5$.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (definition and the determinant example); [Riehl §1.4](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell
def _():
    def _run():
        import itertools
        import random

        def _sign(perm):
            _s = 1
            for _i in range(len(perm)):
                for _j in range(_i + 1, len(perm)):
                    if perm[_i] > perm[_j]:
                        _s = -_s
            return _s

        def _det(matrix):
            # Leibniz formula: uses only +, -, x, so it makes sense over any commutative ring
            _n = len(matrix)
            _total = 0
            for _perm in itertools.permutations(range(_n)):
                _term = _sign(_perm)
                for _i in range(_n):
                    _term *= matrix[_i][_perm[_i]]
                _total += _term
            return _total

        _rng = random.Random(0)
        print("Naturality of det at the ring homomorphism  phi: Z -> Z/5,  phi(a) = a mod 5")
        print("  route 1: det over Z, then phi          route 2: phi on every entry, then det over Z/5")
        for _ in range(4):
            _X = [[_rng.randint(-9, 9) for _c in range(3)] for _r in range(3)]
            _route1 = _det(_X) % 5
            _route2 = _det([[_a % 5 for _a in _row] for _row in _X]) % 5
            print(f"  X = {_X}   route 1 = {_route1}   route 2 = {_route2}   equal: {_route1 == _route2}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Explore: One Naturality Square

    The smallest situation in which naturality says something is when the domain category has a single non-identity arrow. Let $\mathbf{2}$ be the category with two objects $0, 1$ and one non-identity arrow $u \colon 0 \to 1$. For the codomain take the category $\mathcal{T}$ with a single object, the set $\{0, 1\}$, and all four functions $\{0,1\} \to \{0,1\}$ as arrows:

    | name | $0 \mapsto$ | $1 \mapsto$ |
    |---|---|---|
    | `id` | 0 | 1 |
    | `swap` | 1 | 0 |
    | `c0` | 0 | 0 |
    | `c1` | 1 | 1 |

    A functor $F \colon \mathbf{2} \to \mathcal{T}$ must send both objects to $\{0,1\}$ and both identities to `id`, so it is determined by the single arrow $F(u)$. Any of the four functions will do, because $\mathbf{2}$ has no composable pair of non-identity arrows for functoriality to constrain.

    A natural transformation $\alpha \colon F \Rightarrow G$ is then a pair of functions $(\alpha_0, \alpha_1)$ such that
    $$G(u) \circ \alpha_0 = \alpha_1 \circ F(u).$$
    (The squares at the two identity arrows commute automatically: there both horizontal arrows are identities.) Pick $F(u)$, $G(u)$, $\alpha_0$ and $\alpha_1$ below and see whether the square commutes. Before you look at the verdict, compute both routes by hand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sq_Fu = mo.ui.dropdown(options=["id", "swap", "c0", "c1"], value="c0", label="F(u)")
    sq_Gu = mo.ui.dropdown(options=["id", "swap", "c0", "c1"], value="c1", label="G(u)")
    sq_a0 = mo.ui.dropdown(options=["id", "swap", "c0", "c1"], value="id", label="component at 0")
    sq_a1 = mo.ui.dropdown(options=["id", "swap", "c0", "c1"], value="swap", label="component at 1")
    mo.vstack([
        mo.md("**The two functors** (each is determined by where it sends $u$)"),
        mo.hstack([sq_Fu, sq_Gu], justify="start"),
        mo.md("**The candidate transformation**"),
        mo.hstack([sq_a0, sq_a1], justify="start"),
    ])
    return sq_Fu, sq_Gu, sq_a0, sq_a1


@app.cell(hide_code=True)
def _(draw_diagram, mo, sq_Fu, sq_Gu, sq_a0, sq_a1):
    def _run():
        import itertools

        _table = {"id": (0, 1), "swap": (1, 0), "c0": (0, 0), "c1": (1, 1)}

        def _after(g, f):
            # the function "g after f" on the set {0, 1}, as a pair of values
            return tuple(_table[g][_table[f][_x]] for _x in (0, 1))

        _route_down_right = _after(sq_Gu.value, sq_a0.value)
        _route_right_down = _after(sq_a1.value, sq_Fu.value)
        _ok = _route_down_right == _route_right_down
        _count = sum(
            1 for _p, _q in itertools.product(_table, repeat=2)
            if _after(sq_Gu.value, _p) == _after(_q, sq_Fu.value)
        )
        _color = "#15803d" if _ok else "#b91c1c"
        _fig = draw_diagram(
            {
                "F0": (0.0, 1.7, r"$F(0)$"),
                "F1": (3.2, 1.7, r"$F(1)$"),
                "F0+": (0.3, 1.7, ""),
                "F1-": (2.9, 1.7, ""),
                "G0+": (0.3, 0.0, ""),
                "G1-": (2.9, 0.0, ""),
                "G0": (0.0, 0.0, r"$G(0)$"),
                "G1": (3.2, 0.0, r"$G(1)$"),
            },
            [
                ("F0+", "F1-", r"$F(u)=\mathrm{" + sq_Fu.value + "}$", {"side": -1, "color": _color}),
                ("F0", "G0", r"$\quad\alpha_0$", {"color": _color}),
                ("F1", "G1", r"$\quad\alpha_1$", {"color": _color}),
                ("G0+", "G1-", r"$G(u)=\mathrm{" + sq_Gu.value + "}$", {"color": _color}),
            ],
            figsize=(5.4, 3.2),
            title=(
                r"$\alpha_0=\mathrm{" + sq_a0.value + r"}$,  $\alpha_1=\mathrm{" + sq_a1.value + r"}$:  "
                + ("commutes" if _ok else "does NOT commute")
            ),
        )
        _lines = [
            "| route | value at 0 | value at 1 |",
            "|---|---|---|",
            "| down then right: $G(u) \\circ \\alpha_0$ | "
            + str(_route_down_right[0]) + " | " + str(_route_down_right[1]) + " |",
            "| right then down: $\\alpha_1 \\circ F(u)$ | "
            + str(_route_right_down[0]) + " | " + str(_route_right_down[1]) + " |",
            "",
        ]
        if _ok:
            _lines.append("**Verdict:** the two routes are the same function, so $(\\alpha_0, \\alpha_1)$ is a natural transformation $F \\Rightarrow G$.")
        else:
            _lines.append("**Verdict:** the two routes differ, so $(\\alpha_0, \\alpha_1)$ is **not** a natural transformation $F \\Rightarrow G$.")
        _lines.append("")
        _lines.append(
            "For this choice of $F$ and $G$, exactly **" + str(_count)
            + "** of the 16 possible pairs $(\\alpha_0, \\alpha_1)$ are natural."
        )
        return mo.vstack([_fig, mo.md("\n".join(_lines))])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Things to try.**

    - Set $F(u) = G(u) = $ `id`. Which pairs are natural? Explain the count you see by simplifying the naturality equation by hand.
    - Set $F(u) = $ `c0` and $G(u) = $ `c1`. The component $\alpha_0$ can be anything, but $\alpha_1$ is constrained. Why? What does the equation say about $\alpha_1(0)$, and why does it say nothing about $\alpha_1(1)$?
    - Find $F$, $G$ and a pair $(\alpha_0, \alpha_1)$ of *bijections* that is not natural. Being an isomorphism componentwise does not make a family natural.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Naturality in Familiar Clothing: Group Actions and Posets

    In 1A you saw that a monoid or a group is a category with one object, and that a poset is a category with at most one arrow between any two objects. In 1C you saw what functors out of these categories are. A good way to get a feel for a new definition is to ask what it says in those two special cases.

    **Functors from a group to $\mathbf{Set}$.** Let $G$ be a group, regarded as a category with one object $\star$. A functor $X \colon G \to \mathbf{Set}$ consists of a set $S = X(\star)$ and, for each $g \in G$, a function $X(g) \colon S \to S$, with $X(gh) = X(g) \circ X(h)$ and $X(e) = 1_S$. Writing $g \cdot s$ for $X(g)(s)$, this is exactly a **left $G$-set** (1C).

    Now let $X, Y \colon G \to \mathbf{Set}$ be two such functors, with underlying sets $S$ and $T$. Walk through the checklist:

    1. $G$ has one object, so a family of components is a single function $\alpha_\star \colon S \to T$. Call it $\alpha$.
    2. The arrows of $G$ are the elements $g \in G$, each an arrow $\star \to \star$. Naturality at $g$ says $Y(g) \circ \alpha = \alpha \circ X(g)$, that is,
       $$g \cdot \alpha(s) = \alpha(g \cdot s) \qquad \text{for all } g \in G,\ s \in S.$$

    So a natural transformation $X \Rightarrow Y$ is the same thing as a function $S \to T$ that commutes with the action. Such functions are called **$G$-equivariant maps**, and they are what an algebraist would call the homomorphisms of $G$-sets. The general definition, specialised, has produced the correct notion of map without being told about it.

    **Non-example.** Let $G = \mathbb{Z}/2 = \{e, t\}$. Let $X$ be the set $\{a, b\}$ with the action in which $t$ fixes both points, and $Y$ the set $\{a, b\}$ with the action in which $t$ swaps them. Is there any natural transformation $\alpha \colon X \Rightarrow Y$? Naturality at $t$ would give $t \cdot \alpha(s) = \alpha(t \cdot s) = \alpha(s)$, so $\alpha(s)$ would be a point of $Y$ fixed by $t$. There is no such point. So there is **no** natural transformation $X \Rightarrow Y$ at all, although the underlying sets $X(\star)$ and $Y(\star)$ are equal.

    **Functors between posets.** Let $P$ and $Q$ be posets, regarded as categories: there is an arrow $p \to p'$ exactly when $p \leq p'$, and then only one. A functor $P \to Q$ is an order-preserving map (1C).

    ### Natural transformations between order-preserving maps

    **Proposition 2.** Let $F, G \colon P \to Q$ be order-preserving maps between posets. There is a natural transformation $F \Rightarrow G$ if and only if $F(p) \leq G(p)$ for every $p \in P$, and in that case there is exactly one.

    - **Goal.** Two things: (i) if a natural transformation $F \Rightarrow G$ exists then $F(p) \leq G(p)$ for all $p \in P$; (ii) if $F(p) \leq G(p)$ for all $p \in P$ then there exists exactly one natural transformation $F \Rightarrow G$.
    - **Given.** In the category $Q$ there is an arrow $q \to q'$ if and only if $q \leq q'$, and any two arrows with the same domain and the same codomain are equal. The definition of a natural transformation.
    - **Plan.** Unpack the definition. Existence of components is the inequality; the naturality equation is an equation between two parallel arrows of $Q$, and in a poset parallel arrows are always equal.
    - **Proof.** (i) Suppose $\alpha \colon F \Rightarrow G$ is a natural transformation. For each $p \in P$ its component $\alpha_p$ is an arrow $F(p) \to G(p)$ in $Q$. An arrow $F(p) \to G(p)$ exists in $Q$ only if $F(p) \leq G(p)$. So $F(p) \leq G(p)$ for all $p$.

      (ii) Suppose $F(p) \leq G(p)$ for all $p \in P$. *Existence.* For each $p$ let $\alpha_p$ be the unique arrow $F(p) \to G(p)$ of $Q$. To check naturality, let $p \leq p'$ in $P$, and write $f$ for the corresponding arrow $p \to p'$. Both $G(f) \circ \alpha_p$ and $\alpha_{p'} \circ F(f)$ are arrows $F(p) \to G(p')$ in $Q$. Since any two arrows of $Q$ with the same domain and codomain are equal, $G(f) \circ \alpha_p = \alpha_{p'} \circ F(f)$. So $\alpha$ is natural. *Uniqueness.* If $\beta \colon F \Rightarrow G$ is another natural transformation, then for each $p$ both $\alpha_p$ and $\beta_p$ are arrows $F(p) \to G(p)$ of $Q$, hence equal. So $\beta = \alpha$. $\blacksquare$
    - **What made it work.** In a poset every diagram commutes, so the naturality condition costs nothing; all the content is in whether the components exist. In a general category it is the other way round: components are easy to write down and the square is the work.

    **Example.** On $(\mathbb{Z}, \leq)$ let $F(n) = n$ and $G(n) = n + 1$. Both are order-preserving, and $F(n) \leq G(n)$ for all $n$, so there is exactly one natural transformation $F \Rightarrow G$. There is none in the direction $G \Rightarrow F$, since $G(0) = 1 \not\leq 0 = F(0)$.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (functors out of a monoid or group, and between ordered sets); [Riehl §1.4](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Two Classic Examples: the Double Dual and Reversal

    ### The double dual

    Fix a field $k$. For a vector space $V$ over $k$, the **dual space** is $V^* = \mathbf{Vect}_k(V, k)$, the vector space of linear maps $V \to k$. A linear map $f \colon V \to W$ induces a linear map in the *opposite* direction,
    $$f^* \colon W^* \to V^*, \qquad f^*(\theta) = \theta \circ f,$$
    which makes $(-)^*$ a contravariant functor (1C). Applying it twice gives a **covariant** functor $(-)^{**} \colon \mathbf{Vect}_k \to \mathbf{Vect}_k$, the *double dual*: on objects $V \mapsto V^{**} = (V^*)^*$, and on a linear map $f \colon V \to W$,
    $$f^{**} \colon V^{**} \to W^{**}, \qquad f^{**}(\Phi) = \Phi \circ f^*, \quad\text{so}\quad \big(f^{**}(\Phi)\big)(\theta) = \Phi(\theta \circ f) \ \text{ for } \theta \in W^*.$$

    For each $V$ there is a map from $V$ to its double dual, "evaluate at $v$":
    $$\mathrm{ev}_V \colon V \to V^{**}, \qquad \mathrm{ev}_V(v)(\theta) = \theta(v) \ \text{ for } \theta \in V^*.$$
    Step 2 of the checklist asks that each $\mathrm{ev}_V$ be an arrow of $\mathbf{Vect}_k$ from $V$ to $V^{**}$. First, $\mathrm{ev}_V(v)$ really is an element of $V^{**}$: it is linear in $\theta$ because $(\theta + \theta')(v) = \theta(v) + \theta'(v)$ and $(c\theta)(v) = c\,\theta(v)$, by the definition of the vector space structure on $V^*$. Second, $\mathrm{ev}_V$ is linear in $v$ because each $\theta$ is linear: $\theta(v + v') = \theta(v) + \theta(v')$ and $\theta(cv) = c\,\theta(v)$.

    **Proposition 3.** The family $(\mathrm{ev}_V)_{V \in \mathbf{Vect}_k}$ is a natural transformation $\mathrm{ev} \colon 1_{\mathbf{Vect}_k} \Rightarrow (-)^{**}$.

    - **Goal.** For every linear map $f \colon V \to W$: $\;f^{**} \circ \mathrm{ev}_V = \mathrm{ev}_W \circ f$ as maps $V \to W^{**}$.
    - **Given.** The definitions of $\mathrm{ev}$ and of $f^{**}$ displayed above.
    - **Plan.** Both sides are functions $V \to W^{**}$, and an element of $W^{**}$ is itself a function $W^* \to k$. So "equal" means: for every $v \in V$ and every $\theta \in W^*$, both sides give the same scalar. Evaluate twice and compare.
    - **Proof.** Let $v \in V$ and $\theta \in W^*$. On one side,
      $$\big(f^{**}(\mathrm{ev}_V(v))\big)(\theta) = \mathrm{ev}_V(v)(\theta \circ f) = (\theta \circ f)(v) = \theta(f(v)),$$
      using the definition of $f^{**}$ and then the definition of $\mathrm{ev}_V$ applied to the functional $\theta \circ f \in V^*$. On the other side,
      $$\big(\mathrm{ev}_W(f(v))\big)(\theta) = \theta(f(v)),$$
      by the definition of $\mathrm{ev}_W$. The two agree for all $\theta$, so $f^{**}(\mathrm{ev}_V(v)) = \mathrm{ev}_W(f(v))$ in $W^{**}$; this holds for all $v$, so $f^{**} \circ \mathrm{ev}_V = \mathrm{ev}_W \circ f$. $\blacksquare$
    - **What made it work.** Nothing was chosen. The map $\mathrm{ev}_V$ is defined without a basis, by a formula that makes sense for every $V$, and the proof is "unfold both sides until they are the same expression". When the objects are sets of functions, expect to apply the equation to an argument more than once.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "tl": (0.0, 1.7, r"$V$"),
            "tr": (3.0, 1.7, r"$W$"),
            "bl": (0.0, 0.0, r"$V^{**}$"),
            "br": (3.0, 0.0, r"$W^{**}$"),
            # unlabelled anchor points, so that horizontal arrows clear the wide node labels
            "tl+": (0.15, 1.7, ""),
            "tr-": (2.85, 1.7, ""),
            "bl+": (0.15, 0.0, ""),
            "br-": (2.85, 0.0, ""),
        },
        [
            ("tl+", "tr-", r"$f$", {"side": -1}),
            ("tl", "bl", r"$\qquad\mathrm{ev}_V$"),
            ("tr", "br", r"$\qquad\mathrm{ev}_W$"),
            ("bl+", "br-", r"$f^{**}$"),
        ],
        figsize=(5.0, 3.2),
        title=r"Naturality of ev at $f$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What about the single dual?** If $V$ is finite-dimensional then $V$ and $V^*$ have the same dimension, so they are isomorphic. But every isomorphism $V \to V^*$ you can write down uses a choice (of a basis, or of an inner product). And the definition of natural transformation cannot even be applied to compare $1_{\mathbf{Vect}_k}$ with $(-)^*$, because the first is covariant and the second contravariant (step 1 of the checklist fails). That is the precise content of the old slogan "$V$ is naturally isomorphic to $V^{**}$ but not to $V^*$". We return to the isomorphism part in Section 6.

    ### Reversal of finite sequences

    For a set $X$, let $L(X)$ be the set of all finite sequences $(x_1, \dots, x_n)$ of elements of $X$, for all $n \geq 0$ (the case $n = 0$ is the empty sequence). A function $f \colon X \to Y$ gives a function
    $$L(f) \colon L(X) \to L(Y), \qquad L(f)(x_1, \dots, x_n) = (f(x_1), \dots, f(x_n)).$$
    Then $L(1_X) = 1_{L(X)}$ and $L(g \circ f) = L(g) \circ L(f)$, both by applying each side to a sequence, so $L$ is a functor $\mathbf{Set} \to \mathbf{Set}$.

    **Example (reversal).** Define $\mathrm{rev}_X \colon L(X) \to L(X)$ by $\mathrm{rev}_X(x_1, \dots, x_n) = (x_n, \dots, x_1)$. This is a natural transformation $\mathrm{rev} \colon L \Rightarrow L$. Check naturality at $f \colon X \to Y$ on a sequence $(x_1, \dots, x_n)$:
    $$L(f)\big(\mathrm{rev}_X(x_1, \dots, x_n)\big) = L(f)(x_n, \dots, x_1) = (f(x_n), \dots, f(x_1)),$$
    $$\mathrm{rev}_Y\big(L(f)(x_1, \dots, x_n)\big) = \mathrm{rev}_Y(f(x_1), \dots, f(x_n)) = (f(x_n), \dots, f(x_1)).$$
    Reversal only moves positions around; it never looks at what the entries are, so it does not matter whether you rename the entries by $f$ before or after.

    **Example (length).** Let $\Delta\mathbb{N} \colon \mathbf{Set} \to \mathbf{Set}$ be the constant functor sending every set to $\mathbb{N}$ and every function to $1_{\mathbb{N}}$. The maps $\mathrm{len}_X \colon L(X) \to \mathbb{N}$ form a natural transformation $L \Rightarrow \Delta\mathbb{N}$: naturality at $f$ says that $L(f)$ does not change the length of a sequence.

    **Non-example (deleting repeats).** Define $d_X \colon L(X) \to L(X)$ by deleting from a sequence every entry that has already occurred earlier in it, so $d_X(a, b, a) = (a, b)$. Each $d_X$ is a function $L(X) \to L(X)$, but the family is **not** natural. Take $X = \{a, b\}$ with $a \neq b$, $Y = \{c\}$, and $f$ the only function $X \to Y$. Then
    $$L(f)\big(d_X(a, b)\big) = L(f)(a, b) = (c, c), \qquad d_Y\big(L(f)(a, b)\big) = d_Y(c, c) = (c).$$
    The operation $d$ has to ask whether two entries are *equal*, and a non-injective $f$ changes the answer.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (the double dual); [Riehl §1.4](https://math.jhu.edu/~eriehl/context.pdf) (the double dual, and why the single dual is not natural).
    """)
    return


@app.cell
def _():
    def _run():
        def _L(f):
            # the function L(f): apply f to every entry of a finite sequence
            return lambda seq: tuple(f[_x] for _x in seq)

        def _rev(seq):
            return tuple(reversed(seq))

        def _delete_repeats(seq):
            _out = []
            for _x in seq:
                if _x not in _out:
                    _out.append(_x)
            return tuple(_out)

        _f = {"a": "c", "b": "c", "e": "d"}          # a function X = {a, b, e} -> Y = {c, d}
        _seqs = [(), ("a",), ("a", "b"), ("a", "e", "b"), ("e", "a", "a", "b")]

        print("reversal: L(f) after rev_X   vs   rev_Y after L(f)")
        for _s in _seqs:
            _one, _two = _L(_f)(_rev(_s)), _rev(_L(_f)(_s))
            print(f"  {str(_s):24s} {str(_one):22s} {str(_two):22s} equal: {_one == _two}")

        print("\ndeleting repeats: L(f) after d_X   vs   d_Y after L(f)")
        for _s in _seqs:
            _one, _two = _L(_f)(_delete_repeats(_s)), _delete_repeats(_L(_f)(_s))
            print(f"  {str(_s):24s} {str(_one):22s} {str(_two):22s} equal: {_one == _two}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Vertical Composition and the Functor Category

    Natural transformations are maps between functors, so we should be able to compose them. Given three functors $F, G, H \colon \mathcal{A} \to \mathcal{B}$ and natural transformations $\alpha \colon F \Rightarrow G$ and $\beta \colon G \Rightarrow H$, there is only one sensible thing to try: compose the components.

    > **Definition (vertical composite).** Let $F, G, H \colon \mathcal{A} \to \mathcal{B}$ be functors and $\alpha \colon F \Rightarrow G$, $\beta \colon G \Rightarrow H$ natural transformations. Their **vertical composite** $\beta \circ \alpha \colon F \Rightarrow H$ is the family with components
    > $$(\beta \circ \alpha)_A = \beta_A \circ \alpha_A \colon F(A) \to H(A) \qquad \text{for each object } A \text{ of } \mathcal{A}.$$

    **Reading the definition.** A definition that produces a new object of a given kind carries a proof obligation:

    1. Each $(\beta\circ\alpha)_A$ is an arrow $F(A) \to H(A)$. It is: $\alpha_A \colon F(A) \to G(A)$ and $\beta_A \colon G(A) \to H(A)$ are composable in $\mathcal{B}$.
    2. The family $\beta \circ \alpha$ is natural. This is not automatic; it is Proposition 4.

    ### The vertical composite is natural

    **Proposition 4.** With notation as in the definition, $\beta \circ \alpha$ is a natural transformation $F \Rightarrow H$.

    - **Goal.** For every arrow $f \colon A \to A'$ of $\mathcal{A}$: $\;H(f) \circ (\beta_A \circ \alpha_A) = (\beta_{A'} \circ \alpha_{A'}) \circ F(f)$.
    - **Given.** Naturality of $\alpha$ at $f$: $\;G(f) \circ \alpha_A = \alpha_{A'} \circ F(f)$. Naturality of $\beta$ at $f$: $\;H(f) \circ \beta_A = \beta_{A'} \circ G(f)$. Associativity in $\mathcal{B}$.
    - **Plan.** Paste two squares. The outer rectangle of the diagram below is what we want; it is made of the naturality square of $\alpha$ on top of the naturality square of $\beta$. Move $f$ past $\beta$, then past $\alpha$.
    - **Proof.** Let $f \colon A \to A'$ be an arrow of $\mathcal{A}$. Then
      $$\begin{aligned}
      H(f) \circ (\beta_A \circ \alpha_A) &= (H(f) \circ \beta_A) \circ \alpha_A && \text{by associativity} \\
      &= (\beta_{A'} \circ G(f)) \circ \alpha_A && \text{by naturality of } \beta \text{ at } f \\
      &= \beta_{A'} \circ (G(f) \circ \alpha_A) && \text{by associativity} \\
      &= \beta_{A'} \circ (\alpha_{A'} \circ F(f)) && \text{by naturality of } \alpha \text{ at } f \\
      &= (\beta_{A'} \circ \alpha_{A'}) \circ F(f) && \text{by associativity.} \qquad \blacksquare
      \end{aligned}$$
    - **What made it work.** If two small squares that share an edge both commute, the rectangle they form commutes. This is called **pasting**, and it is the standard way to prove that a large diagram commutes: cut it into pieces each of which commutes for a reason you can name.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "FA": (0.0, 3.0, r"$F(A)$"),
            "FB": (2.6, 3.0, r"$F(A')$"),
            "GA": (0.0, 1.5, r"$G(A)$"),
            "GB": (2.6, 1.5, r"$G(A')$"),
            "HA": (0.0, 0.0, r"$H(A)$"),
            "HB": (2.6, 0.0, r"$H(A')$"),
        },
        [
            ("FA", "FB", r"$F(f)$", {"side": -1}),
            ("GA", "GB", r"$G(f)$", {"side": -1}),
            ("HA", "HB", r"$H(f)$"),
            ("FA", "GA", r"$\alpha_A$"),
            ("FB", "GB", r"$\alpha_{A'}$", {"side": -1}),
            ("GA", "HA", r"$\beta_A$"),
            ("GB", "HB", r"$\beta_{A'}$", {"side": -1}),
        ],
        figsize=(4.6, 4.6),
        title="Pasting two commuting squares",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vertical composition is associative and the identity transformations $1_F$ of Example 1 are identities for it. Both facts are inherited from $\mathcal{B}$ one component at a time: for instance $(\gamma \circ (\beta \circ \alpha))_A = \gamma_A \circ (\beta_A \circ \alpha_A) = (\gamma_A \circ \beta_A) \circ \alpha_A = ((\gamma \circ \beta) \circ \alpha)_A$ by associativity in $\mathcal{B}$, and two natural transformations with the same components are equal. So we have all the data and axioms of a category.

    > **Definition (functor category).** Let $\mathcal{A}$ and $\mathcal{B}$ be categories. The **functor category** $[\mathcal{A}, \mathcal{B}]$ has
    > - as objects, the functors $\mathcal{A} \to \mathcal{B}$;
    > - as arrows $F \to G$, the natural transformations $F \Rightarrow G$;
    > - as composition, vertical composition; and as identities, the transformations $1_F$.

    **Reading the definition.** To work in $[\mathcal{A}, \mathcal{B}]$ you need to remember that (1) an equation between arrows of $[\mathcal{A}, \mathcal{B}]$ means an equation between components for **every** object $A$ of $\mathcal{A}$; and (2) composition is computed componentwise, in $\mathcal{B}$.

    **Example ($G$-sets).** For a group $G$, Section 3 shows that $[G, \mathbf{Set}]$ is the category of left $G$-sets and $G$-equivariant maps.

    **Example (posets).** For posets $P$ and $Q$, Proposition 2 shows that $[P, Q]$ has at most one arrow between any two objects, and an arrow $F \to G$ exactly when $F(p) \leq G(p)$ for all $p$. So $[P, Q]$ is the set of order-preserving maps $P \to Q$ with the *pointwise* order, regarded as a category.

    **Example (arrows and squares).** A functor $\mathbf{2} \to \mathcal{B}$ picks out one arrow of $\mathcal{B}$, as in Section 2. So the objects of $[\mathbf{2}, \mathcal{B}]$ are the arrows of $\mathcal{B}$, and an arrow of $[\mathbf{2}, \mathcal{B}]$ from $h \colon B_0 \to B_1$ to $h' \colon B_0' \to B_1'$ is a pair $(\alpha_0 \colon B_0 \to B_0',\ \alpha_1 \colon B_1 \to B_1')$ with $h' \circ \alpha_0 = \alpha_1 \circ h$: a commutative square in $\mathcal{B}$.

    **Non-example.** Functors with different domains or codomains do not live in a common functor category. There is no such thing as a natural transformation from a functor $\mathcal{A} \to \mathcal{B}$ to a functor $\mathcal{A}' \to \mathcal{B}$ with $\mathcal{A} \neq \mathcal{A}'$; the naturality square cannot be drawn.

    A caution about size, to be made precise in 3A: when $\mathcal{A}$ is very large, the natural transformations between two given functors need not form a set. For now, read $[\mathcal{A}, \mathcal{B}]$ with a small $\mathcal{A}$ in mind, such as a group, a poset or $\mathbf{2}$.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (composition of natural transformations, functor categories); [Riehl §1.7](https://math.jhu.edu/~eriehl/context.pdf) treats the two compositions together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Natural Isomorphism

    In 1B an isomorphism in a category was an arrow with a two-sided inverse. The functor category is a category, so the definition applies there with no further work.

    > **Definition (natural isomorphism).** Let $F, G \colon \mathcal{A} \to \mathcal{B}$ be functors. A **natural isomorphism** $F \Rightarrow G$ is an isomorphism in $[\mathcal{A}, \mathcal{B}]$: a natural transformation $\alpha \colon F \Rightarrow G$ for which there exists a natural transformation $\beta \colon G \Rightarrow F$ with
    > $$\beta \circ \alpha = 1_F \qquad \text{and} \qquad \alpha \circ \beta = 1_G.$$
    > If a natural isomorphism $F \Rightarrow G$ exists, $F$ and $G$ are **naturally isomorphic**, written $F \cong G$.

    **Reading the definition.** Unpacked into components, you must produce:

    1. a natural transformation $\alpha \colon F \Rightarrow G$;
    2. a family $(\beta_A \colon G(A) \to F(A))_{A \in \mathcal{A}}$ that is itself **natural**;
    3. with $\beta_A \circ \alpha_A = 1_{F(A)}$ and $\alpha_A \circ \beta_A = 1_{G(A)}$ for every object $A$.

    Item 3 says that every component $\alpha_A$ is an isomorphism in $\mathcal{B}$ with inverse $\beta_A$. Item 2 looks like extra work, but it is not:

    > **Lemma 5 (stated; the proof is exercise P03).** A natural transformation $\alpha \colon F \Rightarrow G$ is a natural isomorphism if and only if every component $\alpha_A \colon F(A) \to G(A)$ is an isomorphism in $\mathcal{B}$.

    So in practice you prove that something is a natural isomorphism in two steps: show it is natural, then show each component is an isomorphism. The order matters; a family of isomorphisms that is not natural (as in the non-example of Section 1) is not a natural isomorphism.

    **Terminology.** When $F \cong G$ one also says
    $$F(A) \cong G(A) \quad \textbf{naturally in } A.$$
    This phrase claims more than "for each $A$ there is some isomorphism $F(A) \cong G(A)$". It claims that the isomorphisms can be chosen, for all $A$ simultaneously, so that they form a natural transformation.

    **Example (double dual, finite dimensions).** Let $\mathbf{FDVect}_k$ be the category of finite-dimensional vector spaces over $k$. The double dual restricts to a functor $\mathbf{FDVect}_k \to \mathbf{FDVect}_k$ and, by Proposition 3, $\mathrm{ev}$ is a natural transformation $1 \Rightarrow (-)^{**}$ there. Each $\mathrm{ev}_V$ is injective: if $v \neq 0$, extend $v$ to a basis of $V$ and let $\theta$ be the functional that reads off the coefficient of $v$; then $\mathrm{ev}_V(v)(\theta) = \theta(v) = 1 \neq 0$, so $\mathrm{ev}_V(v) \neq 0$. And $\dim V^{**} = \dim V^* = \dim V$ when $V$ is finite-dimensional, so the injective linear map $\mathrm{ev}_V$ is an isomorphism. By Lemma 5, $\mathrm{ev}$ is a natural isomorphism:
    $$V \cong V^{**} \quad \text{naturally in } V \in \mathbf{FDVect}_k.$$

    **Example (reversal).** $\mathrm{rev} \colon L \Rightarrow L$ from Section 4 is a natural isomorphism, with inverse $\mathrm{rev}$ itself, since reversing twice returns the original sequence.

    **Example (swapping factors).** Fix a set $B$. The functors $(-) \times B$ and $B \times (-)$ from $\mathbf{Set}$ to $\mathbf{Set}$ send a function $f \colon A \to A'$ to $(a, b) \mapsto (f(a), b)$ and $(b, a) \mapsto (b, f(a))$ respectively. The maps $\sigma_A \colon A \times B \to B \times A$, $\sigma_A(a, b) = (b, a)$, are natural in $A$ (both routes send $(a, b)$ to $(b, f(a))$) and each is a bijection. So $A \times B \cong B \times A$ naturally in $A$.

    **Non-example (isomorphic at every object, not naturally isomorphic).** Return to the two $\mathbb{Z}/2$-sets $X$ and $Y$ of Section 3, viewed as functors $\mathbb{Z}/2 \to \mathbf{Set}$. At the only object $\star$ we have $X(\star) = \{a, b\} = Y(\star)$, so $X(\star) \cong Y(\star)$ in $\mathbf{Set}$. But there is no natural transformation $X \Rightarrow Y$ whatsoever, so $X \not\cong Y$. "$F(A) \cong G(A)$ for every $A$" does not imply "$F \cong G$".

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (natural isomorphism, "naturally in $A$"); [Riehl §1.4](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Whiskering and Horizontal Composition

    Vertical composition stacks two transformations between functors that all go from $\mathcal{A}$ to $\mathcal{B}$. There is a second way to combine natural transformations, which arises when *functors* are composed:
    $$\mathcal{A} \xrightarrow{\;F,\ F'\;} \mathcal{B} \xrightarrow{\;G,\ G'\;} \mathcal{C}, \qquad \alpha \colon F \Rightarrow F', \quad \beta \colon G \Rightarrow G'.$$
    Out of this we would like a natural transformation $GF \Rightarrow G'F'$. We build it in two steps.

    > **Definition (whiskering).** With notation as above:
    > - $G\alpha \colon GF \Rightarrow GF'$ is the family with components $(G\alpha)_A = G(\alpha_A) \colon GF(A) \to GF'(A)$;
    > - $\beta F \colon GF \Rightarrow G'F$ is the family with components $(\beta F)_A = \beta_{F(A)} \colon GF(A) \to G'F(A)$.

    **Reading the definition.** $G\alpha$ means "apply the functor $G$ to each component of $\alpha$". $\beta F$ means "use only the components of $\beta$ at objects of the form $F(A)$". In both cases there is a naturality claim to prove.

    **Proposition 6.** $G\alpha$ and $\beta F$ are natural transformations.

    - **Goal.** For every arrow $f \colon A \to A'$ of $\mathcal{A}$: (i) $GF'(f) \circ G(\alpha_A) = G(\alpha_{A'}) \circ GF(f)$; (ii) $G'F(f) \circ \beta_{F(A)} = \beta_{F(A')} \circ GF(f)$.
    - **Given.** Naturality of $\alpha$ at every arrow of $\mathcal{A}$; naturality of $\beta$ at every arrow of $\mathcal{B}$; functoriality of $G$, i.e. $G(h \circ k) = G(h) \circ G(k)$.
    - **Plan.** For (i), apply $G$ to the naturality square of $\alpha$: functors send commutative squares to commutative squares. For (ii), use naturality of $\beta$ at a well-chosen arrow of $\mathcal{B}$.
    - **Proof.** (i) Let $f \colon A \to A'$. Then
      $$GF'(f) \circ G(\alpha_A) = G\big(F'(f) \circ \alpha_A\big) = G\big(\alpha_{A'} \circ F(f)\big) = G(\alpha_{A'}) \circ GF(f),$$
      by functoriality of $G$, then naturality of $\alpha$ at $f$, then functoriality of $G$ again.

      (ii) The arrow $F(f) \colon F(A) \to F(A')$ is an arrow of $\mathcal{B}$. Naturality of $\beta$ at the arrow $F(f)$ reads $G'(F(f)) \circ \beta_{F(A)} = \beta_{F(A')} \circ G(F(f))$, which is the required equation. $\blacksquare$
    - **What made it work.** In (ii) the key step was to **name the arrow** at which naturality is used. Naturality of $\beta$ is a statement about *every* arrow of $\mathcal{B}$; the art is in choosing which one to feed it.

    Now there are two candidate transformations $GF \Rightarrow G'F'$: go $GF \Rightarrow GF' \Rightarrow G'F'$, or go $GF \Rightarrow G'F \Rightarrow G'F'$.

    **Proposition 7.** For every object $A$ of $\mathcal{A}$,
    $$\beta_{F'(A)} \circ G(\alpha_A) \;=\; G'(\alpha_A) \circ \beta_{F(A)}.$$
    In other words $\beta F' \circ G\alpha = G'\alpha \circ \beta F$ as natural transformations $GF \Rightarrow G'F'$.

    - **Goal.** For each object $A$ of $\mathcal{A}$, the two arrows $GF(A) \to G'F'(A)$ displayed above are equal.
    - **Given.** Naturality of $\beta \colon G \Rightarrow G'$ at every arrow of $\mathcal{B}$.
    - **Plan.** The equation has the shape of a naturality square for $\beta$. Find the arrow of $\mathcal{B}$ it belongs to.
    - **Proof.** Fix $A$. The component $\alpha_A \colon F(A) \to F'(A)$ is an arrow of $\mathcal{B}$. Naturality of $\beta$ at the arrow $\alpha_A$ says $G'(\alpha_A) \circ \beta_{F(A)} = \beta_{F'(A)} \circ G(\alpha_A)$. $\blacksquare$
    - **What made it work.** A component of one natural transformation is just an arrow, and so another natural transformation can be natural *at it*. This trick, "use naturality of $\beta$ at a component of $\alpha$", comes back in 2C, where the proof of Theorem 3 uses naturality of the unit $\eta$ at its own component $\eta_A$; and the proof of the Yoneda lemma in 4B turns on the same kind of choice, of the arrow at which to use naturality.

    > **Definition (horizontal composite).** The **horizontal composite** $\beta * \alpha \colon GF \Rightarrow G'F'$ is the natural transformation with components
    > $$(\beta * \alpha)_A = \beta_{F'(A)} \circ G(\alpha_A) = G'(\alpha_A) \circ \beta_{F(A)}.$$

    It is natural because it is the vertical composite $\beta F' \circ G\alpha$ of two natural transformations (Propositions 6 and 4). The whiskerings are special cases: $G\alpha = 1_G * \alpha$ and $\beta F = \beta * 1_F$, where for the second you use $G(1_{F(A)}) = 1_{GF(A)}$.

    **Example.** Take $\mathcal{A} = \mathcal{B} = \mathcal{C} = \mathbf{Set}$ and $F = F' = G = G' = L$, the finite-sequence functor, with $\alpha = \beta = \mathrm{rev}$. An element of $LL(X)$ is a sequence of sequences. The whiskering $L\,\mathrm{rev}$ reverses each inner sequence, and $\mathrm{rev}\,L$ reverses the outer sequence:
    $$(L\,\mathrm{rev})_X\big((1,2),(3)\big) = \big((2,1),(3)\big), \qquad (\mathrm{rev}\,L)_X\big((1,2),(3)\big) = \big((3),(1,2)\big).$$
    Proposition 7 says these two operations can be done in either order, and $\mathrm{rev} * \mathrm{rev}$ sends $\big((1,2),(3)\big)$ to $\big((3),(2,1)\big)$.

    **Non-example.** The expression $\alpha G$ makes no sense here: $\alpha$ has components indexed by objects of $\mathcal{A}$, while $G$ takes values in $\mathcal{C}$. Before whiskering, check that the functor and the transformation are composable in the order written.

    Vertical and horizontal composition are compatible with each other; the precise statement is the **interchange law**, which is exercise P06.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (horizontal composition); [Riehl §1.7](https://math.jhu.edu/~eriehl/context.pdf) (whiskering, horizontal composition and interchange).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "tl": (0.0, 1.7, r"$GF(A)$"),
            "tr": (3.4, 1.7, r"$GF'(A)$"),
            "bl": (0.0, 0.0, r"$G'F(A)$"),
            "br": (3.4, 0.0, r"$G'F'(A)$"),
            # unlabelled anchor points, so that horizontal arrows clear the wide node labels
            "tl+": (0.45, 1.7, ""),
            "tr-": (2.9499999999999997, 1.7, ""),
            "bl+": (0.45, 0.0, ""),
            "br-": (2.9499999999999997, 0.0, ""),
        },
        [
            ("tl+", "tr-", r"$G(\alpha_A)$", {"side": -1}),
            ("tl", "bl", r"$\qquad\ \beta_{F(A)}$"),
            ("tr", "br", r"$\qquad\ \beta_{F'(A)}$"),
            ("bl+", "br-", r"$G'(\alpha_A)$"),
        ],
        figsize=(5.6, 3.2),
        title=r"Naturality of $\beta$ at the arrow $\alpha_A$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Checking naturality only at identity arrows, or only at one convenient arrow.** The definition quantifies over *every* arrow $f$ of $\mathcal{A}$. A proof of naturality starts "Let $f \colon A \to A'$ be an arbitrary arrow of $\mathcal{A}$".
    2. **Choosing the components after seeing $f$.** The family $(\alpha_A)$ must be fixed first. "Pick a basis of $V$ adapted to $f$" produces a different map for each $f$, which is not one transformation.
    3. **Forgetting that a component must be an arrow of $\mathcal{B}$.** In $\mathbf{Grp}$ or $\mathbf{Vect}_k$, a function between underlying sets is not yet a component; show it is a homomorphism or linear before discussing squares.
    4. **Concluding $F \cong G$ from $F(A) \cong G(A)$ for each $A$.** Objectwise isomorphism gives no natural transformation at all (the two $\mathbb{Z}/2$-sets). You need a single natural $\alpha$ whose components are isomorphisms.
    5. **Using naturality without saying at which arrow.** Every use of naturality in a proof should read "by naturality of $\alpha$ at $f$", with $f$ an arrow of the *domain category of the functors that $\alpha$ goes between*. If you cannot name the arrow, the step is not justified yet.
    6. **Comparing functors of different variance.** A covariant and a contravariant functor are never the two ends of a natural transformation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why This Matters

    Natural transformations are the notion of "sameness" and "comparison" that the rest of the course is written in.

    - **1E (equivalence).** Two categories are equivalent when there are functors each way whose composites are *naturally isomorphic* to identity functors. The definition of Section 6 and Lemma 5 are used on the first page.
    - **2A–2C (adjunctions).** An adjunction is a bijection $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$ that is *natural in $A$ and $B$*; its unit and counit are natural transformations, and the triangle identities are equations between whiskered transformations (Section 7).
    - **4A–4C (representables and Yoneda).** The Yoneda lemma is a statement about the set of natural transformations out of a hom-functor: the arrows of the functor category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$.
    - **5A–6B (limits).** A cone over a diagram is a natural transformation from a constant functor, and limits in functor categories are computed in $[\mathcal{A}, \mathcal{B}]$.

    In every one of these, the proofs consist of naturality squares pasted together, exactly as in Propositions 4, 6 and 7.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    These exercises use the shared finite-category encoding. A category is a dictionary with keys `objects`, `arrows` (name $\mapsto$ (domain, codomain)), `identity` and `compose`, where `compose[(g, f)]` is $g \circ f$. A functor is `{"objects": {...}, "arrows": {...}}`. A natural transformation is a dictionary sending each object of the domain category to the *name* of its component arrow.

    Each skeleton builds the same two categories: $\mathbf{2}$ (objects `"0"`, `"1"`, arrows `id0`, `id1`, `u`) and the one-object category $\mathcal{T}$ of Section 2 (object `"*"`, arrows `id`, `swap`, `c0`, `c1`). The cells run as shipped; fill in each `# TODO`, then uncomment the `print` checks and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: A General Naturality Checker

    Write `is_natural(A, B, F, G, alpha)`, which returns `True` exactly when the family `alpha` satisfies the naturality equation at **every** arrow of `A`. You may assume `F` and `G` are functors `A -> B` and that each `alpha[X]` is an arrow of `B` from `F(X)` to `G(X)`.
    """)
    return


@app.cell
def _():
    def _run():
        _table = {"id": (0, 1), "swap": (1, 0), "c0": (0, 0), "c1": (1, 1)}
        _name = {_v: _k for _k, _v in _table.items()}
        T = {
            "objects": ["*"],
            "arrows": {_a: ("*", "*") for _a in _table},
            "identity": {"*": "id"},
            "compose": {
                (_g, _f): _name[tuple(_table[_g][_table[_f][_x]] for _x in (0, 1))]
                for _g in _table for _f in _table
            },
        }
        two = {
            "objects": ["0", "1"],
            "arrows": {"id0": ("0", "0"), "id1": ("1", "1"), "u": ("0", "1")},
            "identity": {"0": "id0", "1": "id1"},
            "compose": {("id0", "id0"): "id0", ("id1", "id1"): "id1", ("u", "id0"): "u", ("id1", "u"): "u"},
        }

        def functor_picking(arrow):
            # the functor 2 -> T that sends u to the given arrow
            return {"objects": {"0": "*", "1": "*"}, "arrows": {"id0": "id", "id1": "id", "u": arrow}}

        def is_natural(A, B, F, G, alpha):
            # TODO: for every arrow f: X -> Y of A, compare the two composites in B
            #       (use A["arrows"], F["arrows"], G["arrows"] and B["compose"])
            _result = ...
            return _result

        F = functor_picking("c0")
        G = functor_picking("c0")

        # print(is_natural(two, T, F, G, {"0": "swap", "1": "id"}))     # expect True
        # print(is_natural(two, T, F, G, {"0": "id", "1": "swap"}))     # expect False
        # print(is_natural(two, T, functor_picking("swap"), functor_picking("id"), {"0": "swap", "1": "id"}))  # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Count All Natural Transformations

    Write `all_natural(A, B, F, G)`, which returns the list of **all** natural transformations `F => G`. Enumerate every family of components (for each object `X` of `A`, any arrow of `B` from `F(X)` to `G(X)`; `itertools.product` is the right tool) and keep the natural ones. Paste your `is_natural` from Exercise 1 into the stub.

    The last check uses the symmetric group $S_3$ as a one-object category and asks for the natural transformations from its identity functor to itself. Compare the number you get with what you know about the centre of $S_3$; exercise P04 explains the connection.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        _table = {"id": (0, 1), "swap": (1, 0), "c0": (0, 0), "c1": (1, 1)}
        _name = {_v: _k for _k, _v in _table.items()}
        T = {
            "objects": ["*"],
            "arrows": {_a: ("*", "*") for _a in _table},
            "identity": {"*": "id"},
            "compose": {
                (_g, _f): _name[tuple(_table[_g][_table[_f][_x]] for _x in (0, 1))]
                for _g in _table for _f in _table
            },
        }
        two = {
            "objects": ["0", "1"],
            "arrows": {"id0": ("0", "0"), "id1": ("1", "1"), "u": ("0", "1")},
            "identity": {"0": "id0", "1": "id1"},
            "compose": {("id0", "id0"): "id0", ("id1", "id1"): "id1", ("u", "id0"): "u", ("id1", "u"): "u"},
        }

        def functor_picking(arrow):
            return {"objects": {"0": "*", "1": "*"}, "arrows": {"id0": "id", "id1": "id", "u": arrow}}

        # S3 as a one-object category: arrows are the 6 permutations of (0, 1, 2), named "p012", "p102", ...
        _perms = list(itertools.permutations(range(3)))
        _pname = {_p: "p" + "".join(str(_i) for _i in _p) for _p in _perms}
        S3 = {
            "objects": ["*"],
            "arrows": {_pname[_p]: ("*", "*") for _p in _perms},
            "identity": {"*": "p012"},
            "compose": {
                (_pname[_g], _pname[_f]): _pname[tuple(_g[_f[_i]] for _i in range(3))]
                for _g in _perms for _f in _perms
            },
        }
        identity_on_S3 = {"objects": {"*": "*"}, "arrows": {_a: _a for _a in S3["arrows"]}}

        def is_natural(A, B, F, G, alpha):
            # TODO: paste your solution to Exercise 1 here
            _result = ...
            return _result

        def all_natural(A, B, F, G):
            # TODO: list, for each object X of A, the arrows of B from F(X) to G(X);
            #       run through every combination; keep those that pass is_natural
            _result = ...
            return _result

        # print(len(all_natural(two, T, functor_picking("id"), functor_picking("id"))))     # expect 4
        # print(len(all_natural(two, T, functor_picking("c0"), functor_picking("c1"))))     # expect 8
        # print(all_natural(two, T, functor_picking("swap"), functor_picking("c1")))
        # expect the four families {"0": x, "1": "c1"} for x in id, swap, c0, c1
        # print(all_natural(S3, S3, identity_on_S3, identity_on_S3))                        # expect [{'*': 'p012'}]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Vertical Composition

    Write `vertical(B, beta, alpha)`, which returns the vertical composite $\beta \circ \alpha$ as a dictionary of component names. Then use your `is_natural` to confirm Proposition 4 on the example: here $\alpha \colon F \Rightarrow G$ and $\beta \colon G \Rightarrow H$ where $F$, $G$, $H$ pick out `swap`, `id`, `c0`.
    """)
    return


@app.cell
def _():
    def _run():
        _table = {"id": (0, 1), "swap": (1, 0), "c0": (0, 0), "c1": (1, 1)}
        _name = {_v: _k for _k, _v in _table.items()}
        T = {
            "objects": ["*"],
            "arrows": {_a: ("*", "*") for _a in _table},
            "identity": {"*": "id"},
            "compose": {
                (_g, _f): _name[tuple(_table[_g][_table[_f][_x]] for _x in (0, 1))]
                for _g in _table for _f in _table
            },
        }
        two = {
            "objects": ["0", "1"],
            "arrows": {"id0": ("0", "0"), "id1": ("1", "1"), "u": ("0", "1")},
            "identity": {"0": "id0", "1": "id1"},
            "compose": {("id0", "id0"): "id0", ("id1", "id1"): "id1", ("u", "id0"): "u", ("id1", "u"): "u"},
        }

        def functor_picking(arrow):
            return {"objects": {"0": "*", "1": "*"}, "arrows": {"id0": "id", "id1": "id", "u": arrow}}

        def is_natural(A, B, F, G, alpha):
            # TODO: paste your solution to Exercise 1 here
            _result = ...
            return _result

        def vertical(B, beta, alpha):
            # TODO: the component of (beta after alpha) at X is a composite in B
            _result = ...
            return _result

        F, G, H = functor_picking("swap"), functor_picking("id"), functor_picking("c0")
        alpha = {"0": "swap", "1": "id"}      # F => G
        beta = {"0": "swap", "1": "c0"}       # G => H

        # print(is_natural(two, T, F, G, alpha), is_natural(two, T, G, H, beta))   # expect True True
        # print(vertical(T, beta, alpha))                                          # expect {'0': 'id', '1': 'c0'}
        # print(is_natural(two, T, F, H, vertical(T, beta, alpha)))                # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six proof briefs, in `exercises/1d/`. Each has the statement, what you may assume, what a complete proof must contain, and hints that open one at a time. There are no solutions anywhere in the course.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | Over a discrete category, every family is natural — `exercises/1d/p01_discrete_families_natural.md` | warm-up | unpacking the definition |
    | P02 | The singleton map into the power set is natural — `exercises/1d/p02_singleton_natural.md` | warm-up | checking a naturality square on elements |
    | P03 | A natural transformation with invertible components is a natural isomorphism — `exercises/1d/p03_natural_iso_componentwise.md` | core | manipulating a naturality square with inverses |
    | P04 | Natural transformations between group homomorphisms — `exercises/1d/p04_conjugate_homomorphisms.md` | core | translating a definition into algebra |
    | P05 | The identity functor on Set has only one natural endomorphism — `exercises/1d/p05_identity_functor_on_set.md` | core | naturality at a well-chosen arrow |
    | P06 | The interchange law — `exercises/1d/p06_interchange_law.md` | stretch | pasting squares, naming every use of naturality |

    **How to submit a proof.** Write your proof in `proofs/1d/pNN_<slug>.md` (the same file name as the brief), then ask Claude to review it.
    The review points at gaps and asks questions; it does not supply a model proof, so the proof stays yours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [1C: Functors](../1c_functors/) | Next: [1E: Equivalence of Categories](../1e_equivalence/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
