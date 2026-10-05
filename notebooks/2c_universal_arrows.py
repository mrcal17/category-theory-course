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
    # 2C: Adjunctions via Initial Objects

    > *An adjunction is a family of universal properties, one for each object.*
    > — the idea behind this module

    You already know a sentence of the following kind from algebra: *every function from a set $S$ to a vector space $V$ extends uniquely to a linear map from the free vector space on $S$.* There are two claims in it, "extends" and "uniquely", and both are quantified over every $V$ and every function. A statement of this shape is called a **universal property**. This module shows that it is exactly what an adjunction is, seen one object $A$ at a time.

    The route is as follows. First we build, from a functor $G \colon \mathcal{B} \to \mathcal{A}$ and an object $A$, a new category $(A \Rightarrow G)$ whose objects are the arrows $A \to G(B)$. This is an instance of a general construction, the **comma category**, which also produces the slice and coslice categories. Then the universal property of the free vector space becomes a single phrase: *the unit $\eta_A$ is an initial object of $(A \Rightarrow G)$*. And everything known about initial objects from 2A, above all their uniqueness up to unique isomorphism, transfers to adjoints.

    By the end you will be able to describe the objects and arrows of a comma category in any example; to prove that the unit of an adjunction is initial; to prove that an adjunction between $F$ and $G$ is the same as a natural $\eta$ whose components are all initial; to prove that $G$ has a left adjoint exactly when every $(A \Rightarrow G)$ has an initial object; and to prove that left adjoints are unique up to isomorphism. Every one of these proofs is an *initial-object argument*: to show two arrows are equal, show they are both arrows out of an initial object to the same target.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Comma Categories

    We want to treat *arrows* as objects of a new category. The general recipe takes two functors with a common codomain and looks at the arrows of that codomain that go from an image of the first functor to an image of the second.

    > **Definition (comma category).** Let $P \colon \mathcal{A} \to \mathcal{C}$ and $Q \colon \mathcal{B} \to \mathcal{C}$ be functors with the same codomain. The **comma category** $(P \Rightarrow Q)$ is defined as follows.
    >
    > - An **object** is a triple $(A, h, B)$ where $A$ is an object of $\mathcal{A}$, $B$ is an object of $\mathcal{B}$, and $h \colon P(A) \to Q(B)$ is an arrow of $\mathcal{C}$.
    > - An **arrow** $(A, h, B) \to (A', h', B')$ is a pair $(f, g)$ where $f \colon A \to A'$ is an arrow of $\mathcal{A}$ and $g \colon B \to B'$ is an arrow of $\mathcal{B}$, such that
    >   $$Q(g) \circ h \;=\; h' \circ P(f) \qquad \text{in } \mathcal{C}.$$
    > - **Composition** and **identities** are componentwise: $(f', g') \circ (f, g) = (f' \circ f, g' \circ g)$ and $1_{(A, h, B)} = (1_A, 1_B)$.

    **Reading the definition.**

    1. An object is not just the pair $(A, B)$: the arrow $h$ is part of it. Two different arrows $h_1 \ne h_2 \colon P(A) \to Q(B)$ give two different objects.
    2. An arrow of the comma category is a pair of arrows *satisfying a condition*, and the condition says a square in $\mathcal{C}$ commutes (drawn below).
    3. To know this is a category one must check: the composite of two arrows again satisfies the square condition; $(1_A, 1_B)$ satisfies it; associativity and the identity laws hold. That verification is brief P01.

    Riehl writes $P \downarrow Q$ for the same category.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "PA": (0, 2, r"$P(A)$"), "PA2": (3.4, 2, r"$P(A')$"), "PA2_w": (3.0, 2, ""),
            "QB": (0, 0, r"$Q(B)$"), "QB2": (3.4, 0, r"$Q(B')$"), "QB2_w": (3.0, 0, ""), "QB_e": (0.4, 0, ""),
        },
        [
            ("PA", "PA2_w", r"$P(f)$"),
            ("QB_e", "QB2_w", r"$Q(g)$", {"side": -1}),
            ("PA", "QB", r"$h$", {"side": -1}),
            ("PA2", "QB2", r"$h'$"),
        ],
        figsize=(5.4, 3.6),
        title=r"An arrow $(f, g) : (A, h, B) \rightarrow (A', h', B')$ of $(P \Rightarrow Q)$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example (the arrow category).** Take $\mathcal{A} = \mathcal{B} = \mathcal{C}$ and $P = Q = 1_{\mathcal{C}}$. An object of $(1_{\mathcal{C}} \Rightarrow 1_{\mathcal{C}})$ is an arrow $h \colon A \to B$ of $\mathcal{C}$ (together with its domain and codomain), and an arrow from $h$ to $h'$ is a commutative square. For $\mathcal{C} = \mathbf{Set}$ the objects are all functions.

    **Example (posets).** Let $\mathcal{A}$, $\mathcal{B}$, $\mathcal{C}$ be posets and let $P \colon \mathcal{A} \to \mathcal{C}$ and $Q \colon \mathcal{B} \to \mathcal{C}$ be order-preserving maps. An object of $(P \Rightarrow Q)$ is a pair $(a, b)$ with $P(a) \le Q(b)$; the arrow $h$ is the inequality itself, and there is at most one. The square condition holds automatically. So $(P \Rightarrow Q)$ is the set $\{(a, b) : P(a) \le Q(b)\}$ ordered componentwise.

    **Non-example.** For functors $P \colon \mathcal{A} \to \mathcal{C}$ and $Q \colon \mathcal{B} \to \mathcal{D}$ with $\mathcal{C} \ne \mathcal{D}$ there is no comma category: an "arrow $P(A) \to Q(B)$" has nowhere to live. The common codomain is essential. Also, $(P \Rightarrow Q)$ and $(Q \Rightarrow P)$ are different categories: in the first, the arrows $h$ start at an image of $P$; in the second they end at one.

    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) (comma categories); [Riehl §2.4](https://math.jhu.edu/~eriehl/context.pdf) (the category of elements, a comma category in disguise) and [Riehl §4.6](https://math.jhu.edu/~eriehl/context.pdf) (comma categories in the adjoint functor theorem).

    ---

    ## 2. Slice and Coslice Categories

    The most used comma categories have one of the two functors as simple as possible. Recall from 2A that $\mathbf{1}$ is the category with one object $\star$ and one arrow, and that a functor $\mathbf{1} \to \mathcal{A}$ is the same thing as an object of $\mathcal{A}$. Write $A \colon \mathbf{1} \to \mathcal{A}$ for the functor that picks out the object $A$.

    > **Definition (slice and coslice).** Let $A$ be an object of a category $\mathcal{A}$.
    >
    > The **slice category** $\mathcal{A}/A$ is the comma category $(1_{\mathcal{A}} \Rightarrow A)$. Dropping the component $\star$, which carries no information: an object is a pair $(X, h)$ with $h \colon X \to A$; an arrow $(X, h) \to (X', h')$ is an arrow $f \colon X \to X'$ of $\mathcal{A}$ with $h' \circ f = h$.
    >
    > The **coslice category** $A/\mathcal{A}$ is the comma category $(A \Rightarrow 1_{\mathcal{A}})$: an object is a pair $(X, h)$ with $h \colon A \to X$; an arrow $(X, h) \to (X', h')$ is an arrow $f \colon X \to X'$ of $\mathcal{A}$ with $f \circ h = h'$.

    **Reading the definition.** In the slice, objects are arrows *into* $A$ and the arrows are commutative triangles over $A$. In the coslice, objects are arrows *out of* $A$ and the arrows are commutative triangles under $A$. In both, check the general square condition against the triangle: one side of the square is an identity ($A(1_\star) = 1_A$), so the square degenerates to a triangle.

    **Examples.**

    - *$\mathbf{Set}/I$.* An object is a function $h \colon X \to I$, which is the same information as the family of sets $X_i = h^{-1}(i)$, one for each $i \in I$. An arrow $f$ with $h' \circ f = h$ is a function sending $X_i$ into $X'_i$ for every $i$. So $\mathbf{Set}/I$ is the category of $I$-indexed families of sets.
    - *$\{\ast\}/\mathbf{Set}$.* An object is a set $X$ with a function $\{\ast\} \to X$, that is, a set with a chosen element $x_0$. An arrow is a function preserving the chosen elements. This is the category of *pointed sets*.
    - *A poset.* For $a$ in a poset $P$, the slice $P/a$ is the down-set $\{x : x \le a\}$ and the coslice $a/P$ is the up-set $\{x : a \le x\}$, each with the order inherited from $P$.

    **Proposition 1.** For every object $A$ of a category $\mathcal{A}$, the object $(A, 1_A)$ is terminal in the slice category $\mathcal{A}/A$.

    - **Goal.** For every object $(X, h)$ of $\mathcal{A}/A$ there is exactly one arrow $(X, h) \to (A, 1_A)$ in $\mathcal{A}/A$.
    - **Given.** An arrow $(X, h) \to (A, 1_A)$ of $\mathcal{A}/A$ is an arrow $f \colon X \to A$ of $\mathcal{A}$ with $1_A \circ f = h$. The identity axiom in $\mathcal{A}$.
    - **Plan.** Unpack what an arrow into $(A, 1_A)$ is. The condition will pin $f$ down completely.
    - **Proof.** Let $(X, h)$ be an object of $\mathcal{A}/A$, so $h \colon X \to A$. By the identity axiom, $1_A \circ f = f$ for any $f \colon X \to A$. So the condition "$1_A \circ f = h$" is the same as "$f = h$". *Existence:* $f = h$ is an arrow $X \to A$ satisfying the condition, so it is an arrow $(X, h) \to (A, 1_A)$. *Uniqueness:* any arrow $(X, h) \to (A, 1_A)$ is an $f$ with $f = h$. Hence there is exactly one. $\blacksquare$
    - **What made it work.** *In a comma category, "exactly one arrow" is a statement about solutions of an equation in the original category.* Here the equation $1_A \circ f = h$ has exactly one solution. Every initial-object or terminal-object argument in this module starts by writing down that equation.

    **Non-example.** $(A, 1_A)$ is usually *not* initial in $\mathcal{A}/A$. An arrow $(A, 1_A) \to (X, h)$ is an $f \colon A \to X$ with $h \circ f = 1_A$. In $\mathbf{Set}/\{0, 1\}$, take $X = \emptyset$ with its unique function to $\{0,1\}$: there is no function $\{0,1\} \to \emptyset$ at all, so existence fails.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram, mo):
    mo.hstack(
        [
            draw_diagram(
                {"X": (0, 1.8, r"$X$"), "X2": (3, 1.8, r"$X'$"), "A": (1.5, 0, r"$A$")},
                [
                    ("X", "X2", r"$f$"),
                    ("X", "A", r"$h$", {"side": -1}),
                    ("X2", "A", r"$h'$"),
                ],
                figsize=(4.2, 3.2),
                title=r"Arrow of the slice $\mathcal{A}/A$:  $h' \circ f = h$",
            ),
            draw_diagram(
                {"A": (1.5, 1.8, r"$A$"), "X": (0, 0, r"$X$"), "X2": (3, 0, r"$X'$")},
                [
                    ("A", "X", r"$h$", {"side": -1}),
                    ("A", "X2", r"$h'$"),
                    ("X", "X2", r"$f$", {"side": -1}),
                ],
                figsize=(4.2, 3.2),
                title=r"Arrow of the coslice $A/\mathcal{A}$:  $f \circ h = h'$",
            ),
        ],
        justify="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) (slice and coslice categories as comma categories).

    ---

    ## 3. The Category $(A \Rightarrow G)$ and Universal Arrows

    Now the comma category that this module is really about. Fix a functor $G \colon \mathcal{B} \to \mathcal{A}$ and an object $A$ of $\mathcal{A}$, regarded as a functor $A \colon \mathbf{1} \to \mathcal{A}$. Both functors land in $\mathcal{A}$, so $(A \Rightarrow G)$ is defined.

    > **Definition (the category $(A \Rightarrow G)$; universal arrow).** Let $G \colon \mathcal{B} \to \mathcal{A}$ be a functor and $A$ an object of $\mathcal{A}$. In the comma category $(A \Rightarrow G)$:
    >
    > - an object is a pair $(B, f)$ with $B$ an object of $\mathcal{B}$ and $f \colon A \to G(B)$ an arrow of $\mathcal{A}$;
    > - an arrow $(B, f) \to (B', f')$ is an arrow $q \colon B \to B'$ of $\mathcal{B}$ such that $G(q) \circ f = f'$.
    >
    > An initial object $(B_0, u)$ of $(A \Rightarrow G)$ is called a **universal arrow from $A$ to $G$**. Written out: for every object $B$ of $\mathcal{B}$ and every arrow $f \colon A \to G(B)$ of $\mathcal{A}$, there is exactly one arrow $q \colon B_0 \to B$ of $\mathcal{B}$ such that $G(q) \circ u = f$.

    **Reading the definition.**

    1. The objects are "all the ways of mapping $A$ into something of the form $G(B)$". The same $B$ can appear many times, once for each $f$.
    2. The arrows $q$ live in $\mathcal{B}$, but the condition on them, $G(q) \circ f = f'$, is an equation in $\mathcal{A}$.
    3. $(B_0, u)$ universal means: every $f \colon A \to G(B)$ **factors through $u$**, as $f = G(q) \circ u$, and the $q$ doing so is **unique**. To prove universality you must prove existence and uniqueness of $q$, for every $(B, f)$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram, mo):
    mo.hstack(
        [
            draw_diagram(
                {"A": (1.6, 1.9, r"$A$"), "GB0": (0, 0, r"$G(B_0)$"), "GB": (3.2, 0, r"$G(B)$"),
                 "GB0_e": (0.45, 0, ""), "GB_w": (2.8, 0, "")},
                [
                    ("A", "GB0", r"$u$", {"side": -1}),
                    ("A", "GB", r"$f$"),
                    ("GB0_e", "GB_w", r"$G(q)$", {"side": -1, "dashed": True}),
                ],
                figsize=(4.6, 3.3),
                title=r"in $\mathcal{A}$:  $G(q) \circ u = f$",
            ),
            draw_diagram(
                {"B0": (0, 0.9, r"$B_0$"), "B": (3.0, 0.9, r"$B$"), "pad1": (1.5, 1.9, ""), "pad2": (1.5, -0.1, "")},
                [("B0", "B", r"exactly one $q$", {"dashed": True})],
                figsize=(4.2, 3.3),
                title=r"in $\mathcal{B}$",
            ),
        ],
        justify="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - *Free monoids.* Let $U \colon \mathbf{Mon} \to \mathbf{Set}$ be the forgetful functor and $S$ a set. An object of $(S \Rightarrow U)$ is a monoid $M$ with a function $f \colon S \to U(M)$. The pair $(F(S), \eta_S)$, the monoid of words with the insertion of letters $\eta_S(s) = (s)$, is initial: for every monoid $M$ and function $f \colon S \to U(M)$ there is exactly one homomorphism $q \colon F(S) \to M$ with $q((s)) = f(s)$ for all $s$. This is the sentence "a homomorphism out of a free monoid is determined by, and can be freely prescribed on, the generators" from 2A. Lemma 2 below proves it for every adjunction at once.
    - *Bases.* For $U \colon \mathbf{Vect}_k \to \mathbf{Set}$, a universal arrow from $S$ is a vector space $V_0$ with a function $u \colon S \to U(V_0)$ such that every function from $S$ to a vector space extends uniquely along $u$ to a linear map. That is the defining property of a vector space with basis $S$.
    - *Posets.* For an order-preserving map $g \colon Q \to P$ and $a \in P$, the category $(a \Rightarrow g)$ is the set $\{b \in Q : a \le g(b)\}$ with the order of $Q$. A universal arrow from $a$ to $g$ is a least element of that set.
    - *Coslices.* When $G = 1_{\mathcal{A}}$, $(A \Rightarrow 1_{\mathcal{A}})$ is the coslice $A/\mathcal{A}$.

    **Non-examples.**

    - For the inclusion $g \colon \mathbb{Q} \to \mathbb{R}$ and $a = \sqrt{2}$, the category $(\sqrt{2} \Rightarrow g)$ is the set of rationals $q \ge \sqrt{2}$, which has no least element. There is no universal arrow from $\sqrt{2}$ to $g$.
    - For the functor $! \colon \mathbb{Z}/3 \to \mathbf{1}$ (the group $\mathbb{Z}/3$ as a one-object category), $(\star \Rightarrow\, !)$ has one object and three arrows from it to itself. An initial object would have exactly one arrow to itself, so there is none. Existence of the factorisation holds here; uniqueness is what fails.

    Build some yourself. Choose a functor $G$ between finite categories, an object $A$ of its codomain, and which comma category to form. The builder lists the objects and arrows and reports the initial and terminal objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    comma_functor = mo.ui.dropdown(
        options=[
            "identity on the divisors of 12",
            "identity on the parallel pair X => Y",
            "g(b) = 2b + 1 : chain {0,1,2} -> chain {0,...,5}",
            "constant at 1 : antichain {p, q} -> chain {0, 1}",
            "! : Z/3 -> 1",
        ],
        value="g(b) = 2b + 1 : chain {0,1,2} -> chain {0,...,5}",
        label="Functor G : B -> A",
    )
    comma_kind = mo.ui.radio(
        options=["(A => G): arrows from A to G(B)", "(G => A): arrows from G(B) to A"],
        value="(A => G): arrows from A to G(B)",
        label="Which comma category?",
    )
    mo.vstack([mo.md("**Comma-category builder**"), comma_functor, comma_kind])
    return comma_functor, comma_kind


@app.cell(hide_code=True)
def _(comma_functor, mo):
    _objects = {
        "identity on the divisors of 12": [1, 2, 3, 4, 6, 12],
        "identity on the parallel pair X => Y": ["X", "Y"],
        "g(b) = 2b + 1 : chain {0,1,2} -> chain {0,...,5}": [0, 1, 2, 3, 4, 5],
        "constant at 1 : antichain {p, q} -> chain {0, 1}": [0, 1],
        "! : Z/3 -> 1": ["*"],
    }[comma_functor.value]
    _opts = {str(_o): _o for _o in _objects}
    comma_object = mo.ui.dropdown(options=_opts, value=list(_opts)[len(_opts) // 2],
                                  label="Object A of the codomain of G")
    comma_object
    return (comma_object,)


@app.cell(hide_code=True)
def _(comma_functor, comma_kind, comma_object, draw_diagram):
    def _run():
        import math

        def _poset(elements, leq):
            _arr = {f"{_a}<={_b}": (_a, _b) for _a in elements for _b in elements if leq(_a, _b)}
            return {
                "objects": list(elements),
                "arrows": _arr,
                "identity": {_a: f"{_a}<={_a}" for _a in elements},
                "compose": {(_g, _f): f"{_arr[_f][0]}<={_arr[_g][1]}"
                            for _g in _arr for _f in _arr if _arr[_f][1] == _arr[_g][0]},
            }

        def _ident(cat):
            return {"objects": {_x: _x for _x in cat["objects"]}, "arrows": {_x: _x for _x in cat["arrows"]}}

        def _setup(name):
            """Returns (B, A, G) with G : B -> A."""
            if name == "identity on the divisors of 12":
                _c = _poset([1, 2, 3, 4, 6, 12], lambda _a, _b: _b % _a == 0)
                return _c, _c, _ident(_c)
            if name == "identity on the parallel pair X => Y":
                _c = {
                    "objects": ["X", "Y"],
                    "arrows": {"1X": ("X", "X"), "1Y": ("Y", "Y"), "s": ("X", "Y"), "t": ("X", "Y")},
                    "identity": {"X": "1X", "Y": "1Y"},
                    "compose": {("1X", "1X"): "1X", ("1Y", "1Y"): "1Y", ("s", "1X"): "s", ("t", "1X"): "t",
                                ("1Y", "s"): "s", ("1Y", "t"): "t"},
                }
                return _c, _c, _ident(_c)
            if name == "g(b) = 2b + 1 : chain {0,1,2} -> chain {0,...,5}":
                _b, _a = _poset(range(3), lambda _x, _y: _x <= _y), _poset(range(6), lambda _x, _y: _x <= _y)
                _go = {_x: 2 * _x + 1 for _x in range(3)}
                return _b, _a, {"objects": _go,
                                "arrows": {_n: f"{_go[_x]}<={_go[_y]}" for _n, (_x, _y) in _b["arrows"].items()}}
            if name == "constant at 1 : antichain {p, q} -> chain {0, 1}":
                _b, _a = _poset(["p", "q"], lambda _x, _y: _x == _y), _poset(range(2), lambda _x, _y: _x <= _y)
                return _b, _a, {"objects": {"p": 1, "q": 1}, "arrows": {_n: "1<=1" for _n in _b["arrows"]}}
            _z3 = {
                "objects": ["*"],
                "arrows": {_n: ("*", "*") for _n in "012"},
                "identity": {"*": "0"},
                "compose": {(_g, _f): str((int(_g) + int(_f)) % 3) for _g in "012" for _f in "012"},
            }
            _one = {"objects": ["*"], "arrows": {"1*": ("*", "*")}, "identity": {"*": "1*"},
                    "compose": {("1*", "1*"): "1*"}}
            return _z3, _one, {"objects": {"*": "*"}, "arrows": {_n: "1*" for _n in "012"}}

        _B, _A, _G = _setup(comma_functor.value)
        _a0 = comma_object.value
        if _a0 not in _A["objects"]:
            print("Pick the object A again for the new functor.")
            return None
        _from_a = comma_kind.value.startswith("(A => G)")

        # objects: (b, f) with f : a0 -> G(b)   [or f : G(b) -> a0]
        _objs = []
        for _b in _B["objects"]:
            for _n, (_d, _c) in _A["arrows"].items():
                if (_from_a and _d == _a0 and _c == _G["objects"][_b]) or \
                        (not _from_a and _d == _G["objects"][_b] and _c == _a0):
                    _objs.append((_b, _n))
        # arrows: q : b -> b' in B with G(q) o f = f'   [or f' o G(q) = f]
        _arrs = []
        for (_b1, _f1) in _objs:
            for (_b2, _f2) in _objs:
                for _q, (_d, _c) in _B["arrows"].items():
                    if _d == _b1 and _c == _b2:
                        _Gq = _G["arrows"][_q]
                        if (_from_a and _A["compose"][(_Gq, _f1)] == _f2) or \
                                (not _from_a and _A["compose"][(_f2, _Gq)] == _f1):
                            _arrs.append((_q, (_b1, _f1), (_b2, _f2)))

        def _count(src, dst):
            return sum(1 for (_q, _s, _t) in _arrs if _s == src and _t == dst)

        _initial = [_o for _o in _objs if all(_count(_o, _p) == 1 for _p in _objs)]
        _terminal = [_o for _o in _objs if all(_count(_p, _o) == 1 for _p in _objs)]

        def _show(o):
            return f"({o[0]}, {o[1]})"

        _name = f"({_a0} => G)" if _from_a else f"(G => {_a0})"
        print(f"{_name} for G = {comma_functor.value}")
        print(f"\n{len(_objs)} objects (b, f) with f : " + ("A -> G(b):" if _from_a else "G(b) -> A:"))
        print("   " + (",  ".join(_show(_o) for _o in _objs) if _objs else "(none: the category is empty)"))
        print(f"\n{len(_arrs)} arrows (including {len(_objs)} identities). The non-identity arrows:")
        _non_id = [(_q, _s, _t) for (_q, _s, _t) in _arrs if not (_s == _t and _q == _B["identity"][_s[0]])]
        for (_q, _s, _t) in _non_id:
            print(f"   {_q} : {_show(_s)} -> {_show(_t)}")
        if not _non_id:
            print("   (none)")
        print("\ninitial objects: ", ",  ".join(_show(_o) for _o in _initial) if _initial else "none")
        print("terminal objects:", ",  ".join(_show(_o) for _o in _terminal) if _terminal else "none")

        if not _objs:
            return None
        # picture: objects on a circle, non-identity arrows between them
        _n = len(_objs)
        _r = 1.6 + 0.4 * _n
        _nodes = {}
        for _i, _o in enumerate(_objs):
            _ang = math.pi / 2 - 2 * math.pi * _i / _n
            _mark = " [initial]" if _o in _initial else ""
            _mark += " [terminal]" if _o in _terminal else ""
            _nodes[_o] = (_r * math.cos(_ang) if _n > 1 else 0.0, _r * math.sin(_ang) if _n > 1 else 0.0,
                          _show(_o) + _mark)
        _nodes["pad_a"] = (-_r - 1.4, -_r - 0.3, "")
        _nodes["pad_b"] = (_r + 1.4, _r + 0.3, "")
        _edges, _seen = [], {}
        for (_q, _s, _t) in _non_id:
            if _s == _t:
                _k = _seen.get((_s, _t), 0)
                _edges.append((_s, _t, _q, {"loop": ["up", "down", "left", "right"][_k % 4]}))
            else:
                _k = _seen.get((_s, _t), 0)
                _edges.append((_s, _t, _q if len(_non_id) <= 8 else "", {"rad": 0.12 + 0.3 * _k}))
            _seen[(_s, _t)] = _k + 1
        return draw_diagram(_nodes, _edges, figsize=(8.0, 5.6), title=f"{_name}: objects and non-identity arrows")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try. With $g(b) = 2b + 1$ and "(A ⇒ G)", step $A$ through $0, \ldots, 5$ and record the initial object each time: you are computing the left adjoint $a \mapsto \lfloor a/2 \rfloor$ of 2A, one object at a time. Switch to "(G ⇒ A)" with $A = 0$: the category is empty, so it has no terminal object. (Indeed $g$ has no right adjoint: a right adjoint $r$ would satisfy $g(b) \le 0 \iff b \le r(0)$, and taking $b = r(0)$ would give $g(r(0)) \le 0$, but every value of $g$ is at least $1$.) With the identity on the parallel pair, compare the slice over $Y$ with the coslice under $X$, and check Proposition 1. With the constant map on the antichain and $A = 0$, see two objects with no arrow between them: a category with no initial object for want of *existence*, where $\mathbb{Z}/3$ fails for want of *uniqueness*.

    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) (the comma category $(A \Rightarrow G)$ and its initial objects); [Riehl §2.4](https://math.jhu.edu/~eriehl/context.pdf) (universal properties as initial or terminal objects of a category of elements).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Unit Is an Initial Object

    The free monoid example was not special.

    **Lemma 2.** Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be functors with $F \dashv G$ and unit $\eta$. Then for every object $A$ of $\mathcal{A}$, the pair $(F(A), \eta_A)$ is an initial object of $(A \Rightarrow G)$.

    - **Goal.** For every object $A$ of $\mathcal{A}$, every object $B$ of $\mathcal{B}$ and every arrow $f \colon A \to G(B)$: there is exactly one arrow $q \colon F(A) \to B$ of $\mathcal{B}$ such that $G(q) \circ \eta_A = f$.
    - **Given.** The adjunction, in particular that transposition $q \mapsto \bar{q}$ is a bijection $\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$; and Lemma 2(a) of 2B: $\bar{q} = G(q) \circ \eta_A$ for every $q \colon F(A) \to B$.
    - **Plan.** Rewrite the condition on $q$ using Lemma 2(a) of 2B. It becomes "$\bar{q} = f$", and a bijection takes each value exactly once.
    - **Proof.** Fix $A$, and let $(B, f)$ be an object of $(A \Rightarrow G)$. An arrow $(F(A), \eta_A) \to (B, f)$ is an arrow $q \colon F(A) \to B$ with $G(q) \circ \eta_A = f$. By Lemma 2(a) of 2B, $G(q) \circ \eta_A = \bar{q}$. So the arrows $(F(A), \eta_A) \to (B, f)$ are exactly the $q \in \mathcal{B}(F(A), B)$ with $\bar{q} = f$. Since $q \mapsto \bar{q}$ is a bijection onto $\mathcal{A}(A, G(B))$ and $f$ is an element of $\mathcal{A}(A, G(B))$, there is exactly one such $q$ (namely $q = \bar{f}$). $\blacksquare$
    - **What made it work.** *"Bijection" and "exactly one" are the same statement.* The hom-set bijection says each $f$ has exactly one preimage; initiality says each $(B, f)$ receives exactly one arrow. Lemma 2(a) of 2B is the dictionary between them.

    So an adjunction produces a universal arrow from every object $A$. In the free monoid example, Lemma 2 is the sentence "every function $S \to U(M)$ extends uniquely to a homomorphism $F(S) \to M$". For a Galois connection $f \dashv g$ it says: $f(a)$ is the least $b$ with $a \le g(b)$, which is the mirror image of Proposition 5 of 2A.

    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) (the unit as an initial object of the comma category).

    ---

    ## 5. An Adjunction Is a Family of Initial Objects

    Lemma 2 extracts universal arrows from an adjunction. The main theorem of this module says that nothing is lost: the unit, with its universal property, *is* the adjunction.

    **Theorem 3.** Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be functors. There is a one-to-one correspondence between

    - **(a)** adjunctions between $F$ and $G$ with $F$ on the left; and
    - **(b)** natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ such that, for every object $A$ of $\mathcal{A}$, the pair $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$.

    The correspondence sends an adjunction to its unit.

    - **Goal.** The map "adjunction $\mapsto$ its unit" is well defined from (a) to (b), and is a bijection.
    - **Given.** Theorem 4 of 2B: adjunctions correspond one-to-one to pairs $(\eta, \varepsilon)$ of natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$, $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ satisfying the triangle identities, the adjunction being sent to its unit and counit. Lemma 1 of 2B (the unit is natural) and Lemma 2 above.
    - **Plan.** By Lemma 1 of 2B and Lemma 2, the unit of an adjunction is as in (b). In view of Theorem 4 of 2B, it remains to prove the following **Claim**: *for each $\eta$ as in (b), there is exactly one natural transformation $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ such that $(\eta, \varepsilon)$ satisfies both triangle identities.* Existence in the Claim makes the map (a) → (b) surjective; uniqueness makes it injective. Each part of the Claim is an initial-object argument.
    - **Proof.** Let $\eta$ be as in (b).

      **Uniqueness of $\varepsilon$.** Suppose $\varepsilon$ is natural and $(\eta, \varepsilon)$ satisfies the triangle identities. Fix an object $B$ of $\mathcal{B}$. The second triangle identity reads $G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}$. Read this in the comma category $(G(B) \Rightarrow G)$: it has objects $(FG(B), \eta_{G(B)})$ and $(B, 1_{G(B)})$, and the equation says exactly that $\varepsilon_B \colon FG(B) \to B$ is an arrow
      $$\varepsilon_B \colon (FG(B), \eta_{G(B)}) \longrightarrow (B, 1_{G(B)}) \qquad \text{in } (G(B) \Rightarrow G).$$
      By hypothesis (b), applied to the object $G(B)$ of $\mathcal{A}$, the object $(FG(B), \eta_{G(B)})$ is initial. So there is exactly one arrow from it to $(B, 1_{G(B)})$, and $\varepsilon_B$ must be that arrow. Hence $\varepsilon$ is determined by $\eta$.

      **Existence of $\varepsilon$.** For each object $B$ of $\mathcal{B}$, *define* $\varepsilon_B \colon FG(B) \to B$ to be the unique arrow $(FG(B), \eta_{G(B)}) \to (B, 1_{G(B)})$ in $(G(B) \Rightarrow G)$. By definition of arrows in that category,
      $$G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)} \qquad (\ast)$$
      which is the second triangle identity. Two things remain: naturality of $\varepsilon$, and the first triangle identity.

      *Naturality.* Let $q \colon B \to B'$ be an arrow of $\mathcal{B}$. We must show $q \circ \varepsilon_B = \varepsilon_{B'} \circ FG(q)$. Both are arrows $FG(B) \to B'$ of $\mathcal{B}$. Consider the object $(B', G(q))$ of $(G(B) \Rightarrow G)$; it is an object because $G(q) \colon G(B) \to G(B')$. We show that both arrows are arrows $(FG(B), \eta_{G(B)}) \to (B', G(q))$ in $(G(B) \Rightarrow G)$, by checking the defining condition for each.
      For the first: $G(q \circ \varepsilon_B) \circ \eta_{G(B)} = G(q) \circ G(\varepsilon_B) \circ \eta_{G(B)} = G(q) \circ 1_{G(B)} = G(q)$, using functoriality of $G$, then $(\ast)$, then the identity axiom.
      For the second: $G(\varepsilon_{B'} \circ FG(q)) \circ \eta_{G(B)} = G(\varepsilon_{B'}) \circ GF(G(q)) \circ \eta_{G(B)} = G(\varepsilon_{B'}) \circ \eta_{G(B')} \circ G(q) = 1_{G(B')} \circ G(q) = G(q)$, using functoriality of $G$; then naturality of $\eta$ at the arrow $G(q) \colon G(B) \to G(B')$, which reads $GF(G(q)) \circ \eta_{G(B)} = \eta_{G(B')} \circ G(q)$; then $(\ast)$ for $B'$; then the identity axiom.
      So both are arrows out of the initial object $(FG(B), \eta_{G(B)})$ to the same object $(B', G(q))$. There is exactly one such arrow, so they are equal.

      *First triangle identity.* Fix an object $A$ of $\mathcal{A}$. We must show $\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}$. Both are arrows $F(A) \to F(A)$ of $\mathcal{B}$. We show both are arrows $(F(A), \eta_A) \to (F(A), \eta_A)$ in $(A \Rightarrow G)$.
      For the identity: $G(1_{F(A)}) \circ \eta_A = 1_{GF(A)} \circ \eta_A = \eta_A$.
      For the composite: $G(\varepsilon_{F(A)} \circ F(\eta_A)) \circ \eta_A = G(\varepsilon_{F(A)}) \circ GF(\eta_A) \circ \eta_A = G(\varepsilon_{F(A)}) \circ \eta_{GF(A)} \circ \eta_A = 1_{GF(A)} \circ \eta_A = \eta_A$, using functoriality of $G$; then naturality of $\eta$ at the arrow $\eta_A \colon A \to GF(A)$, which reads $GF(\eta_A) \circ \eta_A = \eta_{GF(A)} \circ \eta_A$; then $(\ast)$ for the object $B = F(A)$; then the identity axiom.
      Since $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$, there is exactly one arrow from it to itself. So $\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}$.

      This proves the Claim.

      **Conclusion.** By Theorem 4 of 2B we may identify adjunctions with pairs $(\eta, \varepsilon)$ of natural transformations satisfying the triangle identities; under this identification the map in the theorem is $(\eta, \varepsilon) \mapsto \eta$. It lands in (b) by Lemma 2. It is surjective, since for each $\eta$ in (b) the existence part of the Claim supplies an $\varepsilon$. It is injective, since if $(\eta, \varepsilon)$ and $(\eta, \varepsilon')$ are two such pairs with the same $\eta$, the uniqueness part of the Claim gives $\varepsilon = \varepsilon'$. $\blacksquare$
    - **What made it work.** *To prove two arrows of $\mathcal{B}$ equal, exhibit both as arrows out of an initial object of a comma category, to the same object.* The work in each case was choosing the right target object ($(B', G(q))$ for naturality, $(F(A), \eta_A)$ for the triangle identity) and then verifying one equation in $\mathcal{A}$ for each arrow. No arrow of $\mathcal{B}$ was ever manipulated directly.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram, mo):
    mo.hstack(
        [
            draw_diagram(
                {"GB": (1.7, 1.9, r"$G(B)$"), "GFGB": (0, 0, r"$GFG(B)$"), "GB2": (3.4, 0, r"$G(B)$"),
                 "GFGB_e": (0.55, 0, ""), "GB2_w": (3.0, 0, "")},
                [
                    ("GB", "GFGB", r"$\eta_{G(B)}$", {"side": -1}),
                    ("GB", "GB2", r"$1_{G(B)}$"),
                    ("GFGB_e", "GB2_w", r"$G(\varepsilon_B)$", {"side": -1, "dashed": True}),
                ],
                figsize=(4.8, 3.3),
                title=r"$\varepsilon_B$ is defined by initiality of $\eta_{G(B)}$",
            ),
            draw_diagram(
                {"GB": (1.7, 1.9, r"$G(B)$"), "GFGB": (0, 0, r"$GFG(B)$"), "GB2": (3.4, 0, r"$G(B')$"),
                 "GFGB_e": (0.55, 0, ""), "GB2_w": (3.0, 0, "")},
                [
                    ("GB", "GFGB", r"$\eta_{G(B)}$", {"side": -1}),
                    ("GB", "GB2", r"$G(q)$"),
                    ("GFGB_e", "GB2_w", r"$G(\,?\,)$", {"side": -1, "dashed": True}),
                ],
                figsize=(4.8, 3.3),
                title=r"Naturality: $q \circ \varepsilon_B$ and $\varepsilon_{B'} \circ FG(q)$ both fit at $?$",
            ),
        ],
        justify="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** For the free monoid, Theorem 3 says the whole adjunction $F \dashv U$ is recovered from the insertions $\eta_S \colon S \to UF(S)$ and their universal property. The counit is forced: $\varepsilon_M$ must be the unique homomorphism $FU(M) \to M$ whose restriction to one-letter words is the identity of $U(M)$, and that is "multiply out", as found in 2B.

    **Non-example.** Naturality of $\eta$ is a genuine part of (b). Initiality of each $(F(A), \eta_A)$ separately does not mention how $F$ acts on arrows at all; (b) requires in addition that the given functor $F$ and the family $\eta$ fit together. The next section shows that when only $G$ is given, a functor $F$ can always be *constructed* to fit.

    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) (adjunctions as natural transformations whose components are initial objects); [Riehl §4.6](https://math.jhu.edu/~eriehl/context.pdf) (the same characterisation, as the starting point of the adjoint functor theorems).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. When Does $G$ Have a Left Adjoint?

    In Theorem 3 both functors were given. Usually only one is: we have a forgetful functor $G$ and ask whether a "free" functor exists. The answer is a condition on $G$ alone, to be checked one object at a time.

    **Corollary 4.** A functor $G \colon \mathcal{B} \to \mathcal{A}$ has a left adjoint if and only if, for every object $A$ of $\mathcal{A}$, the category $(A \Rightarrow G)$ has an initial object.

    - **Goal.** (⇒) If some functor $F$ satisfies $F \dashv G$, then every $(A \Rightarrow G)$ has an initial object. (⇐) If every $(A \Rightarrow G)$ has an initial object, then there exist a functor $F \colon \mathcal{A} \to \mathcal{B}$ and an adjunction $F \dashv G$.
    - **Given.** Lemma 2 and Theorem 3.
    - **Plan.** (⇒) is Lemma 2. For (⇐), choose an initial object for each $A$ and call it $(F(A), \eta_A)$. This defines $F$ on objects only. Define $F$ on arrows by initiality, in the only way that makes $\eta$ natural; prove functoriality by the uniqueness half of initiality; then quote Theorem 3.
    - **Proof.**
      (⇒) If $F \dashv G$ with unit $\eta$, then $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$ by Lemma 2.

      (⇐) For each object $A$ of $\mathcal{A}$, choose an initial object of $(A \Rightarrow G)$ and write it $(F(A), \eta_A)$. So $F(A)$ is an object of $\mathcal{B}$, $\eta_A \colon A \to G(F(A))$, and:
      $$\text{for every } f \colon A \to G(B) \text{ there is exactly one } q \colon F(A) \to B \text{ with } G(q) \circ \eta_A = f. \qquad (\dagger)$$

      *$F$ on arrows.* Let $p \colon A' \to A$ be an arrow of $\mathcal{A}$. Then $\eta_A \circ p \colon A' \to G(F(A))$, so $(F(A), \eta_A \circ p)$ is an object of $(A' \Rightarrow G)$. Define $F(p) \colon F(A') \to F(A)$ to be the unique arrow $(F(A'), \eta_{A'}) \to (F(A), \eta_A \circ p)$ given by $(\dagger)$ for $A'$. That is, $F(p)$ is the unique arrow of $\mathcal{B}$ with
      $$G(F(p)) \circ \eta_{A'} = \eta_A \circ p. \qquad (\ddagger)$$

      *$F$ preserves identities.* Take $p = 1_A$. The arrow $1_{F(A)}$ satisfies $G(1_{F(A)}) \circ \eta_A = 1_{GF(A)} \circ \eta_A = \eta_A = \eta_A \circ 1_A$. So $1_{F(A)}$ satisfies the equation $(\ddagger)$ that characterises $F(1_A)$; by uniqueness, $F(1_A) = 1_{F(A)}$.

      *$F$ preserves composition.* Let $p' \colon A'' \to A'$ and $p \colon A' \to A$. Then
      $$G(F(p) \circ F(p')) \circ \eta_{A''} = G(F(p)) \circ G(F(p')) \circ \eta_{A''} = G(F(p)) \circ \eta_{A'} \circ p' = \eta_A \circ p \circ p',$$
      using functoriality of $G$, then $(\ddagger)$ for $p'$, then $(\ddagger)$ for $p$. So $F(p) \circ F(p')$ satisfies the equation $(\ddagger)$ that characterises $F(p \circ p')$; by uniqueness, $F(p \circ p') = F(p) \circ F(p')$.

      *$\eta$ is natural.* Equation $(\ddagger)$ is the naturality square of $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ at $p$.

      So $F$ is a functor and $\eta$ is a natural transformation $1_{\mathcal{A}} \Rightarrow GF$ each of whose components is initial in the relevant comma category. By Theorem 3, $\eta$ is the unit of an adjunction $F \dashv G$. $\blacksquare$
    - **What made it work.** *Define by existence, verify by uniqueness.* $F(p)$ was defined as "the unique arrow such that…"; each property of $F$ was then proved by showing that some other arrow satisfies the same defining equation.

    A remark on the word "choose". The initial object of $(A \Rightarrow G)$ is not unique, only unique up to isomorphism, so the proof makes a choice for every $A$ at once. You met the same step in 1E, when building an inverse to a full, faithful, essentially surjective functor.

    **Examples.**

    - *Constructing free objects.* To show $U \colon \mathbf{Mon} \to \mathbf{Set}$ has a left adjoint it is enough, for each set $S$, to produce one monoid $F(S)$ and one function $S \to U(F(S))$ with the universal property. No functor needs to be defined by hand; Corollary 4 manufactures it.
    - *Posets.* An order-preserving $g \colon Q \to P$ has a left adjoint if and only if, for every $a \in P$, the set $\{b \in Q : a \le g(b)\}$ has a least element. The left adjoint sends $a$ to that least element. Compare Proposition 5 of 2A, which is the dual statement.
    - *Initial objects.* For $G = \,! \colon \mathcal{B} \to \mathbf{1}$, the category $(\star \Rightarrow\, !)$ has the objects of $\mathcal{B}$ as objects and all arrows of $\mathcal{B}$ as arrows; it is a copy of $\mathcal{B}$. So $!$ has a left adjoint if and only if $\mathcal{B}$ has an initial object, which is Proposition 4 of 2A again.

    **Non-examples.**

    - The inclusion $\mathbb{Q} \to \mathbb{R}$ has no left adjoint, because $(\sqrt{2} \Rightarrow g)$ has no initial object (Section 3).
    - $! \colon \mathbb{Z}/3 \to \mathbf{1}$ has no left adjoint, because $(\star \Rightarrow\, !)$ has no initial object.
    - The forgetful functor $U \colon \mathbf{Field} \to \mathbf{Set}$ has no left adjoint. An object of $(\emptyset \Rightarrow U)$ is a field $K$ with a function $\emptyset \to U(K)$, and there is exactly one such function, so $(\emptyset \Rightarrow U)$ is a copy of $\mathbf{Field}$, which has no initial object (2A, Section 4).

    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) (existence of a left adjoint in terms of initial objects of comma categories); [Riehl §4.6](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Adjoints Are Unique

    In 2A we saw that a right adjoint between posets is unique when it exists. In general categories the correct statement is uniqueness *up to isomorphism*, and the proof is now a direct application of the uniqueness of initial objects (Lemma 3 of 2A).

    First, a small observation about isomorphisms in $(A \Rightarrow G)$. Composition and identities there are those of $\mathcal{B}$. So if $q \colon (B, f) \to (B', f')$ is an isomorphism in $(A \Rightarrow G)$, with inverse $r \colon (B', f') \to (B, f)$, then $r \circ q = 1_B$ and $q \circ r = 1_{B'}$ in $\mathcal{B}$: the arrow $q$ is an isomorphism of $\mathcal{B}$.

    **Theorem 5 (uniqueness of left adjoints).** Let $G \colon \mathcal{B} \to \mathcal{A}$ be a functor, and suppose $F \dashv G$ with unit $\eta$ and $F' \dashv G$ with unit $\eta'$. Then there is exactly one natural transformation $\alpha \colon F \Rightarrow F'$ such that $G(\alpha_A) \circ \eta_A = \eta'_A$ for every object $A$ of $\mathcal{A}$, and it is a natural isomorphism. In particular $F \cong F'$.

    - **Goal.** (i) For each $A$ there is exactly one arrow $\alpha_A \colon F(A) \to F'(A)$ with $G(\alpha_A) \circ \eta_A = \eta'_A$, and it is an isomorphism. (ii) These arrows are natural: for every $p \colon A' \to A$, $F'(p) \circ \alpha_{A'} = \alpha_A \circ F(p)$.
    - **Given.** Lemma 2 for each adjunction: $(F(A), \eta_A)$ and $(F'(A), \eta'_A)$ are both initial in $(A \Rightarrow G)$. Lemma 3 of 2A: between two initial objects there is exactly one isomorphism. Naturality of $\eta$ and of $\eta'$.
    - **Plan.** (i) is uniqueness of initial objects, read in $(A \Rightarrow G)$. (ii) is an initial-object argument: show both sides are arrows out of the initial object $(F(A'), \eta_{A'})$ to the same object of $(A' \Rightarrow G)$.
    - **Proof.**
      (i) Fix $A$. An arrow $\alpha_A \colon F(A) \to F'(A)$ with $G(\alpha_A) \circ \eta_A = \eta'_A$ is precisely an arrow $(F(A), \eta_A) \to (F'(A), \eta'_A)$ in $(A \Rightarrow G)$. Since $(F(A), \eta_A)$ is initial, there is exactly one. Since $(F'(A), \eta'_A)$ is also initial, Lemma 3 of 2A says there is an isomorphism between them in $(A \Rightarrow G)$; being an arrow $(F(A), \eta_A) \to (F'(A), \eta'_A)$, it must be $\alpha_A$. By the observation above, $\alpha_A$ is then an isomorphism of $\mathcal{B}$.

      (ii) Let $p \colon A' \to A$. Consider the object $(F'(A), \eta'_A \circ p)$ of $(A' \Rightarrow G)$. We check that $F'(p) \circ \alpha_{A'}$ and $\alpha_A \circ F(p)$ are both arrows $(F(A'), \eta_{A'}) \to (F'(A), \eta'_A \circ p)$.
      For the first: $G(F'(p) \circ \alpha_{A'}) \circ \eta_{A'} = GF'(p) \circ G(\alpha_{A'}) \circ \eta_{A'} = GF'(p) \circ \eta'_{A'} = \eta'_A \circ p$, using functoriality of $G$, the defining property of $\alpha_{A'}$, and naturality of $\eta'$ at $p$.
      For the second: $G(\alpha_A \circ F(p)) \circ \eta_{A'} = G(\alpha_A) \circ GF(p) \circ \eta_{A'} = G(\alpha_A) \circ \eta_A \circ p = \eta'_A \circ p$, using functoriality of $G$, naturality of $\eta$ at $p$, and the defining property of $\alpha_A$.
      Since $(F(A'), \eta_{A'})$ is initial in $(A' \Rightarrow G)$, the two arrows are equal.

      So $\alpha$ is a natural transformation all of whose components are isomorphisms, that is, a natural isomorphism (1D). It is the only natural transformation with the stated property, because each component is determined by (i). $\blacksquare$
    - **What made it work.** *Two solutions to the same universal problem are isomorphic, by the one isomorphism that respects the universal arrows.* The isomorphism $F(A) \cong F'(A)$ is not found by inspecting $F$ and $F'$; it is handed to us by initiality, and naturality comes from the same source.

    **Dually,** if $F \dashv G$ and $F \dashv G'$ then $G \cong G'$: right adjoints are unique up to isomorphism too. The proof replaces "unit, initial, $(A \Rightarrow G)$" by "counit, terminal, $(F \Rightarrow B)$"; brief P03 supplies the first step.

    **Examples.**

    - Any two constructions of "the free group on $S$" (reduced words, or any other) give isomorphic groups, by an isomorphism that is the identity on the generators. That is Theorem 5 for $G = U \colon \mathbf{Grp} \to \mathbf{Set}$.
    - In a poset the only isomorphisms are identities, so Theorem 5 says a left adjoint of an order-preserving map is unique on the nose.

    **Non-example.** Uniqueness is of the *adjoint of a given functor*. A functor may well have a left adjoint and a right adjoint that are not isomorphic to each other: $D$ and $I$ are both adjoint to $U \colon \mathbf{Top} \to \mathbf{Set}$, on different sides, and $D(S) \not\cong I(S)$ as soon as $S$ has two elements.

    > Reference: [Leinster §2.3](https://arxiv.org/abs/1612.09375) for initial objects of comma categories; [Riehl §4.4](https://math.jhu.edu/~eriehl/context.pdf) for uniqueness of adjoints.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Forgetting that the arrow is part of the object.** *Diagnosis:* writing "the object $B$ of $(A \Rightarrow G)$". An object is a pair $(B, f)$, and "arrows out of an initial object to the same object" requires the same $B$ **and** the same $f$. In Theorem 3 the targets were $(B', G(q))$ and $(F(A), \eta_A)$, each named in full.
    2. **Proving existence of the factorisation and stopping.** *Diagnosis:* initial means *exactly one* arrow. In $(\star \Rightarrow\, !)$ for $\mathbb{Z}/3$ every factorisation exists and none is unique. A universal-property proof has an existence paragraph and a uniqueness paragraph.
    3. **Invoking initiality before checking membership.** *Diagnosis:* "both are arrows out of an initial object, so they are equal" is valid only after you have verified, for *each* of the two, the equation $G(q) \circ u = f$ that makes it an arrow of the comma category.
    4. **Checking the condition in the wrong category.** *Diagnosis:* the arrow $q$ lives in $\mathcal{B}$, the condition $G(q) \circ \eta_A = f$ lives in $\mathcal{A}$. Writing $q \circ \eta_A$ is a type error.
    5. **Claiming two left adjoints are equal.** *Diagnosis:* Theorem 5 gives a natural isomorphism $F \cong F'$, not $F = F'$. Outside posets, "unique" for adjoints always means "unique up to isomorphism".

    ---

    ## Why This Matters

    - **3A** takes stock of the set theory behind "choose an initial object for each $A$" and behind the size of categories such as $(A \Rightarrow G)$.
    - **4A–4C.** A universal arrow from $A$ to $G$ is the same as a *representation* of the functor $\mathcal{A}(A, G(-))$; Theorem 5 becomes "representations are unique up to unique isomorphism": 4C uses the Yoneda lemma to prove that two representing objects are isomorphic, and you will prove the uniqueness of the isomorphism yourself in an exercise there.
    - **5A–5B.** A limit is a terminal object in a category of cones, and a colimit an initial object in a category of cocones; both are comma categories. Proposition 1 and the initial-object arguments of this module are the template for every proof about limits.
    - **6A.** "Limits are right adjoint to the diagonal functor" is Corollary 4, in its dual form, applied to the diagonal.
    - **6B.** The category of elements of a presheaf is a comma category.
    - **6C.** The adjoint functor theorems are theorems about when the categories $(A \Rightarrow G)$ have initial objects. Corollary 4 is where their proofs begin.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Fill in each `# TODO`, then un-comment the `print` checks and compare with the expected values. Categories and functors use the shared encoding: `cat["arrows"][name] = (domain, codomain)`, `cat["compose"][(g, f)]` is $g \circ f$, and a functor is `{"objects": ..., "arrows": ...}`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Build the left adjoint on arrows (Corollary 4)

    You are given a functor `G` from `B` to `A` and, for every object `a` of `A`, a candidate universal arrow: an object `F_ob[a]` of `B` and an arrow `eta[a]` of `A` from `a` to `G(F_ob[a])`.

    First write `unique_factor(A, B, G, b0, u, b, f)`: for `u` an arrow of `A` into `G(b0)` and `f` an arrow of `A` with the same domain into `G(b)`, return the arrow `q` from `b0` to `b` in `B` with $G(q) \circ u = f$ if there is **exactly one**, and `None` otherwise.

    Then carry out the construction in the proof of Corollary 4: `left_adjoint_on_arrows(A, B, G, F_ob, eta)` returns the dict sending each arrow $p \colon a' \to a$ of `A` to the arrow $F(p)$ characterised by equation $(\ddagger)$ of that proof, or to `None` if there is not exactly one such arrow.
    """)
    return


@app.cell
def _():
    def _run():
        def unique_factor(A, B, G, b0, u, b, f):
            # TODO: collect the arrows q : b0 -> b of B with  G(q) o u == f  in A;
            #       return the arrow if there is exactly one, otherwise None
            return ...

        def left_adjoint_on_arrows(A, B, G, F_ob, eta):
            F_arr = {}
            for p, (a2, a) in A["arrows"].items():      # p : a2 -> a
                # TODO: F(p) is the unique arrow out of (F_ob[a2], eta[a2]); into which object of (a2 => G)?
                F_arr[p] = ...
            return F_arr

        def chain(n):
            arrows = {f"{i}<={j}": (i, j) for i in range(n) for j in range(i, n)}
            compose = {(f"{j}<={k}", f"{i}<={j}"): f"{i}<={k}"
                       for i in range(n) for j in range(i, n) for k in range(j, n)}
            return {"objects": list(range(n)), "arrows": arrows,
                    "identity": {i: f"{i}<={i}" for i in range(n)}, "compose": compose}

        # g(b) = 2b + 1 : chain {0,1,2} -> chain {0,...,5}, with candidate universal arrows  a <= g(a // 2)
        C6, C3 = chain(6), chain(3)
        g = {"objects": {b: 2 * b + 1 for b in range(3)},
             "arrows": {f"{i}<={j}": f"{2 * i + 1}<={2 * j + 1}" for i in range(3) for j in range(i, 3)}}
        F_half = {a: a // 2 for a in range(6)}
        eta_half = {a: f"{a}<={2 * (a // 2) + 1}" for a in range(6)}

        # negation on the group Z/3 (one object, composition = addition mod 3)
        Z3 = {"objects": ["*"], "arrows": {n: ("*", "*") for n in "012"}, "identity": {"*": "0"},
              "compose": {(a, b): str((int(a) + int(b)) % 3) for a in "012" for b in "012"}}
        neg = {"objects": {"*": "*"}, "arrows": {"0": "0", "1": "2", "2": "1"}}

        ONE = {"objects": ["*"], "arrows": {"1*": ("*", "*")}, "identity": {"*": "1*"},
               "compose": {("1*", "1*"): "1*"}}
        bang_Z3 = {"objects": {"*": "*"}, "arrows": {"0": "1*", "1": "1*", "2": "1*"}}

        ISO = {   # two objects with mutually inverse arrows u : P -> Q, v : Q -> P
            "objects": ["P", "Q"],
            "arrows": {"1P": ("P", "P"), "1Q": ("Q", "Q"), "u": ("P", "Q"), "v": ("Q", "P")},
            "identity": {"P": "1P", "Q": "1Q"},
            "compose": {("1P", "1P"): "1P", ("1Q", "1Q"): "1Q", ("u", "1P"): "u", ("1Q", "u"): "u",
                        ("v", "1Q"): "v", ("1P", "v"): "v", ("v", "u"): "1P", ("u", "v"): "1Q"},
        }
        bang_ISO = {"objects": {"P": "*", "Q": "*"}, "arrows": {n: "1*" for n in ISO["arrows"]}}

        # print(unique_factor(C6, C3, g, 1, "2<=3", 2, "2<=5"))     # expect 1<=2
        # print(unique_factor(C6, C3, g, 1, "2<=3", 0, "2<=3"))     # expect None   (there is no arrow 1 -> 0)
        # F_arr = left_adjoint_on_arrows(C6, C3, g, F_half, eta_half)
        # print(len(F_arr), F_arr["2<=5"], F_arr["0<=1"], F_arr["4<=4"])               # expect 21 1<=2 0<=0 2<=2
        # print(left_adjoint_on_arrows(Z3, Z3, neg, {"*": "*"}, {"*": "1"}))           # expect {'0': '0', '1': '2', '2': '1'}
        # print(left_adjoint_on_arrows(ONE, ISO, bang_ISO, {"*": "Q"}, {"*": "1*"}))   # expect {'1*': '1Q'}
        # print(left_adjoint_on_arrows(ONE, Z3, bang_Z3, {"*": "*"}, {"*": "1*"}))     # expect {'1*': None}

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Recover the counit from the unit (Theorem 3)

    With the same data, write `counit_from_unit(A, B, G, F_ob, eta)` returning the dict sending each object `b` of `B` to the arrow $\varepsilon_b \colon F(G(b)) \to b$ defined in the existence part of the proof of Theorem 3, by equation $(\ast)$ there. Paste your `unique_factor` from Exercise 1 into the stub.

    In the $\mathbb{Z}/3$ example the unit is changed from `"1"` to `"2"` between two of the checks; watch the counit change with it.
    """)
    return


@app.cell
def _():
    def _run():
        def unique_factor(A, B, G, b0, u, b, f):
            # TODO: paste your solution to Exercise 1 here
            return ...

        def counit_from_unit(A, B, G, F_ob, eta):
            eps = {}
            for b in B["objects"]:
                # TODO: eps[b] is the unique arrow out of the initial object of (G(b) => G); into which object?
                eps[b] = ...
            return eps

        def chain(n):
            arrows = {f"{i}<={j}": (i, j) for i in range(n) for j in range(i, n)}
            compose = {(f"{j}<={k}", f"{i}<={j}"): f"{i}<={k}"
                       for i in range(n) for j in range(i, n) for k in range(j, n)}
            return {"objects": list(range(n)), "arrows": arrows,
                    "identity": {i: f"{i}<={i}" for i in range(n)}, "compose": compose}

        # g(b) = 2b + 1 : chain {0,1,2} -> chain {0,...,5}, with candidate universal arrows  a <= g(a // 2)
        C6, C3 = chain(6), chain(3)
        g = {"objects": {b: 2 * b + 1 for b in range(3)},
             "arrows": {f"{i}<={j}": f"{2 * i + 1}<={2 * j + 1}" for i in range(3) for j in range(i, 3)}}
        F_half = {a: a // 2 for a in range(6)}
        eta_half = {a: f"{a}<={2 * (a // 2) + 1}" for a in range(6)}

        # negation on the group Z/3 (one object, composition = addition mod 3)
        Z3 = {"objects": ["*"], "arrows": {n: ("*", "*") for n in "012"}, "identity": {"*": "0"},
              "compose": {(a, b): str((int(a) + int(b)) % 3) for a in "012" for b in "012"}}
        neg = {"objects": {"*": "*"}, "arrows": {"0": "0", "1": "2", "2": "1"}}

        ONE = {"objects": ["*"], "arrows": {"1*": ("*", "*")}, "identity": {"*": "1*"},
               "compose": {("1*", "1*"): "1*"}}
        bang_Z3 = {"objects": {"*": "*"}, "arrows": {"0": "1*", "1": "1*", "2": "1*"}}

        ISO = {   # two objects with mutually inverse arrows u : P -> Q, v : Q -> P
            "objects": ["P", "Q"],
            "arrows": {"1P": ("P", "P"), "1Q": ("Q", "Q"), "u": ("P", "Q"), "v": ("Q", "P")},
            "identity": {"P": "1P", "Q": "1Q"},
            "compose": {("1P", "1P"): "1P", ("1Q", "1Q"): "1Q", ("u", "1P"): "u", ("1Q", "u"): "u",
                        ("v", "1Q"): "v", ("1P", "v"): "v", ("v", "u"): "1P", ("u", "v"): "1Q"},
        }
        bang_ISO = {"objects": {"P": "*", "Q": "*"}, "arrows": {n: "1*" for n in ISO["arrows"]}}

        # print(counit_from_unit(C6, C3, g, F_half, eta_half))                   # expect {0: '0<=0', 1: '1<=1', 2: '2<=2'}
        # print(counit_from_unit(Z3, Z3, neg, {"*": "*"}, {"*": "1"}))           # expect {'*': '1'}
        # print(counit_from_unit(Z3, Z3, neg, {"*": "*"}, {"*": "2"}))           # expect {'*': '2'}
        # print(counit_from_unit(ONE, ISO, bang_ISO, {"*": "Q"}, {"*": "1*"}))   # expect {'P': 'v', 'Q': '1Q'}

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six briefs, each with a statement, what you may assume, what a complete proof must contain, and hints that open one at a time. There are no solutions anywhere; the proofs are yours to write.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | The comma category is a category — `exercises/2c/p01_comma_is_a_category.md` | warm-up | verifying axioms |
    | P02 | The identity is initial in the coslice — `exercises/2c/p02_coslice_initial_object.md` | warm-up | dualizing a lecture proof |
    | P03 | The counit is a terminal object — `exercises/2c/p03_counit_is_terminal.md` | core | terminal-object argument |
    | P04 | Abelianization as a universal arrow — `exercises/2c/p04_abelianization_universal_arrow.md` | core | existence and uniqueness of a factorisation |
    | P05 | Universal arrows compose — `exercises/2c/p05_universal_arrows_compose.md` | core | initial-object argument |
    | P06 | An adjunction is an isomorphism of comma categories — `exercises/2c/p06_comma_categories_isomorphic.md` | stretch | building mutually inverse functors |

    **How to submit.** Write each proof in `proofs/2c/<same file name>.md`, in the five-step proof anatomy (Goal / Given / Plan / Proof / What made it work).
    Then ask Claude to review it: the review points at gaps and asks questions, and never supplies a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [2B: Units & Counits](../2b_units_counits/) &nbsp;|&nbsp; Next: [3A: Sets & Size](../3a_sets_and_size/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
