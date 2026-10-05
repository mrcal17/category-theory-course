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
    # 5A: Limits

    > *Products, equalizers and pullbacks are one idea.*
    > — the theme of Part 5

    You have met universal properties twice already: as initial objects of comma categories (2C) and as representations of functors (4A–4C). This module gives the third and most hands-on way of saying the same kind of thing. A **limit** of a diagram is an object that maps to every object of the diagram, compatibly, and does so in the best possible way: every other object that maps compatibly into the diagram factors through it, by exactly one map.

    The question this module answers is: *what do the cartesian product of two sets, the kernel of a group homomorphism, the inverse image of a subset, the greatest common divisor of two numbers and the set of fixed points of a group action have in common?* They are all limits. We meet the three classic shapes one at a time (products, equalizers, pullbacks), then give the general definition with cones, and then prove two structural theorems about all limits at once.

    The proof technique of this Part is the **universal-property proof**. Every such proof has two halves that must be kept apart: **existence** of a mediating map and **uniqueness** of that map. By the end of the module you will be able to prove that a given object is a product, equalizer or pullback; that any two limits of the same diagram are isomorphic by exactly one isomorphism compatible with the projections; and that a category with all products and all equalizers has every limit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Products

    Given two sets $X$ and $Y$ you can form the set $X \times Y$ of ordered pairs. What makes it useful is the following fact, which never mentions pairs: to give a function from any set $A$ into $X \times Y$ is exactly the same as giving one function $A \to X$ and one function $A \to Y$. That fact can be stated in any category, and it is the definition of a product.

    > **Definition (binary product).** Let $\mathcal{A}$ be a category and let $X, Y$ be objects of $\mathcal{A}$. A **product** of $X$ and $Y$ consists of an object $P$ and two maps
    > $$X \xleftarrow{\;p_1\;} P \xrightarrow{\;p_2\;} Y$$
    > with the following property: for every object $A$ and every pair of maps $f_1 \colon A \to X$, $f_2 \colon A \to Y$, there exists a unique map $\bar{f} \colon A \to P$ such that
    > $$p_1 \circ \bar{f} = f_1 \qquad\text{and}\qquad p_2 \circ \bar{f} = f_2 .$$
    > The maps $p_1, p_2$ are called **projections**, and $\bar{f}$ is often written $(f_1, f_2)$.

    **Reading the definition.** To show that $(P, p_1, p_2)$ is a product of $X$ and $Y$ you must do the following.

    - **Name the data.** A product is an object *together with two maps*. An object alone is never a product.
    - **Fix arbitrary test data.** Take an arbitrary object $A$ and arbitrary maps $f_1 \colon A \to X$ and $f_2 \colon A \to Y$. You may assume nothing else about them.
    - **Existence.** Produce a map $\bar{f} \colon A \to P$ and verify the two equations $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$.
    - **Uniqueness.** Take any map $g \colon A \to P$ with $p_1 g = f_1$ and $p_2 g = f_2$, and prove $g = \bar{f}$.

    The picture is below. Solid arrows are given; the dashed arrow is the one whose existence and uniqueness is being asserted. We keep that drawing convention for the whole of Part 5.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (1.2, 2.3, r"$A$"), "P": (1.2, 1.0, r"$P$"), "X": (-0.4, 0, r"$X$"), "Y": (2.8, 0, r"$Y$")},
        [
            ("A", "P", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
            ("P", "X", r"$p_1$", {"side": -1}),
            ("P", "Y", r"$p_2$"),
            ("A", "X", r"$f_1$", {"rad": 0.25}),
            ("A", "Y", r"$f_2$", {"rad": -0.25}),
        ],
        figsize=(5.2, 3.6),
        title="A product: every pair (f1, f2) factors uniquely through P",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - **$\mathbf{Set}$.** The cartesian product $X \times Y = \{(x, y) : x \in X,\ y \in Y\}$ with $p_1(x, y) = x$ and $p_2(x, y) = y$. This is proved in full below.
    - **$\mathbf{Grp}$, $\mathbf{Vect}_k$.** The cartesian product of the underlying sets, with the operations defined coordinate by coordinate, and the same two projections. The mediating map is the same function as in $\mathbf{Set}$; the extra check is that it is a homomorphism (a linear map), which holds because the operations of $P$ are coordinatewise.
    - **$\mathbf{Top}$.** The set $X \times Y$ with the product topology. The product topology is designed so that a function $A \to X \times Y$ is continuous exactly when its two coordinate functions are continuous, and that sentence is the universal property.
    - **A poset.** In a poset regarded as a category, a product of $x$ and $y$ is a greatest lower bound (a **meet**) $x \wedge y$. In the natural numbers ordered by divisibility it is the greatest common divisor. You prove this yourself in `p01_meets_are_products.md`.

    **Non-examples.** Each of the two halves of the universal property can fail on its own.

    - *Existence fails.* In $\mathbf{Set}$ take $X = Y = \{0, 1\}$ and try $P = \{0, 1\}$ with $p_1 = p_2 = 1_{\{0,1\}}$. Let $A = \{\ast\}$, $f_1(\ast) = 0$, $f_2(\ast) = 1$. A mediating map $g$ would need $g(\ast) = p_1(g(\ast)) = 0$ and $g(\ast) = p_2(g(\ast)) = 1$. There is none.
    - *Uniqueness fails.* Take the same $X$ and $Y$ and $P = X \times Y \times \{0, 1\}$ with $p_1(x, y, c) = x$, $p_2(x, y, c) = y$. For any $f_1, f_2$ both $a \mapsto (f_1(a), f_2(a), 0)$ and $a \mapsto (f_1(a), f_2(a), 1)$ are mediating maps, and they are different as soon as $A$ is non-empty.
    - *No product at all.* In the category of fields and ring homomorphisms, $\mathbb{F}_2$ and $\mathbb{F}_3$ have no product. A product would be a field $P$ with homomorphisms $P \to \mathbb{F}_2$ and $P \to \mathbb{F}_3$. A homomorphism of fields sends $1$ to $1$ and is injective, so the first forces $1 + 1 = 0$ in $P$ and the second forces $1 + 1 + 1 = 0$ in $P$; subtracting gives $1 = 0$ in $P$, which is impossible in a field.

    ### Proof 1: the cartesian product is a product in $\mathbf{Set}$

    - **Goal.** For all sets $X, Y$: for every set $A$ and all functions $f_1 \colon A \to X$, $f_2 \colon A \to Y$, there exists a unique function $\bar{f} \colon A \to X \times Y$ with $p_1 \circ \bar{f} = f_1$ and $p_2 \circ \bar{f} = f_2$.
    - **Given.** The definition of $X \times Y$ as a set of ordered pairs; the projections $p_1(x, y) = x$, $p_2(x, y) = y$; the fact that two ordered pairs are equal exactly when their first entries agree and their second entries agree; and the fact (0B) that two functions with the same domain and codomain are equal exactly when they agree at every element.
    - **Plan.** A universal-property proof: write down a candidate for $\bar{f}$ and check the two equations (existence); then take any other map satisfying the two equations and show it equals the candidate (uniqueness).
    - **Proof.** Fix $A$, $f_1$, $f_2$.

        *Existence.* Define $\bar{f} \colon A \to X \times Y$ by $\bar{f}(a) = (f_1(a), f_2(a))$. This is a function into $X \times Y$ because $f_1(a) \in X$ and $f_2(a) \in Y$. For every $a \in A$ we have $p_1(\bar{f}(a)) = p_1(f_1(a), f_2(a)) = f_1(a)$ by the definition of $p_1$, so $p_1 \circ \bar{f} = f_1$. In the same way $p_2 \circ \bar{f} = f_2$.

        *Uniqueness.* Let $g \colon A \to X \times Y$ be any function with $p_1 \circ g = f_1$ and $p_2 \circ g = f_2$. Fix $a \in A$. The element $g(a)$ is an ordered pair; its first entry is $p_1(g(a)) = f_1(a)$ and its second entry is $p_2(g(a)) = f_2(a)$. So $g(a) = (f_1(a), f_2(a)) = \bar{f}(a)$. Since $a$ was arbitrary, $g = \bar{f}$. $\qquad\blacksquare$
    - **What made it work.** The two equations $p_i \circ g = f_i$ pin down both coordinates of $g(a)$, and a pair has nothing else. In every uniqueness half of this module, the question to ask is the same: *do the projections see everything about a map into this object?*

    ### Products of families, and the terminal object

    > **Definition (product of a family).** Let $I$ be a set and $(X_i)_{i \in I}$ a family of objects of $\mathcal{A}$. A **product** of the family consists of an object $P$ and maps $p_i \colon P \to X_i$, one for each $i \in I$, such that for every object $A$ and every family of maps $(f_i \colon A \to X_i)_{i \in I}$ there exists a unique map $\bar{f} \colon A \to P$ with $p_i \circ \bar{f} = f_i$ for all $i \in I$. We write $P = \prod_{i \in I} X_i$.

    Take $I = \varnothing$ and read the definition literally. A product of the empty family is an object $P$ (with no projections) such that for every object $A$ (with no maps to give) there exists a unique map $A \to P$. That is the definition of a **terminal object** $1$. So a terminal object is a product of no objects.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (products); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Equalizers

    Solving an equation means finding the inputs at which two expressions agree. Given two functions $s, t \colon X \to Y$, the solution set is $\{x \in X : s(x) = t(x)\}$. The categorical version of "the solution set of $s = t$" is the equalizer.

    > **Definition (fork, equalizer).** Let $s, t \colon X \to Y$ be two maps in a category $\mathcal{A}$ with the same domain and the same codomain. A **fork** on $(s, t)$ is an object $A$ with a map $f \colon A \to X$ such that $s \circ f = t \circ f$. An **equalizer** of $s$ and $t$ is a fork $i \colon E \to X$ with the following property: for every fork $f \colon A \to X$ there exists a unique map $\bar{f} \colon A \to E$ such that $i \circ \bar{f} = f$.

    **Reading the definition.** To show that $i \colon E \to X$ is an equalizer of $s$ and $t$:

    - **It is a fork.** Check $s \circ i = t \circ i$. This step is often forgotten.
    - **Fix an arbitrary fork.** Take an object $A$ and a map $f \colon A \to X$, and assume $s f = t f$. That equation is the only thing you know about $f$.
    - **Existence.** Produce $\bar{f} \colon A \to E$ and check $i \bar{f} = f$. You will have to use $s f = t f$ here; if you did not, something is wrong.
    - **Uniqueness.** Take any $g \colon A \to E$ with $i g = f$ and prove $g = \bar{f}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"E": (0, 0, r"$E$"), "X": (1.7, 0, r"$X$"), "Y": (3.6, 0, r"$Y$"), "A": (0, 1.5, r"$A$")},
        [
            ("E", "X", r"$i$", {"side": -1}),
            ("X", "Y", r"$s$", {"rad": -0.25}),
            ("X", "Y", r"$t$", {"rad": 0.25}),
            ("A", "X", r"$f$"),
            ("A", "E", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
        ],
        figsize=(5.6, 2.8),
        title="An equalizer: every fork f (with sf = tf) factors uniquely through i",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proof 2: equalizers in $\mathbf{Set}$

    Let $s, t \colon X \to Y$ be functions, let $E = \{x \in X : s(x) = t(x)\}$ and let $i \colon E \to X$ be the inclusion, $i(x) = x$.

    - **Goal.** $i$ is a fork on $(s, t)$, and for every set $A$ and every function $f \colon A \to X$ with $s \circ f = t \circ f$ there exists a unique function $\bar{f} \colon A \to E$ with $i \circ \bar{f} = f$.
    - **Given.** The definition of $E$ as a subset of $X$; the inclusion $i$, which is injective.
    - **Plan.** Universal-property proof. The mediating map has to be "$f$ with a smaller codomain", so the content of existence is checking that $f$ lands inside $E$.
    - **Proof.** *Fork.* For $x \in E$ we have $s(i(x)) = s(x) = t(x) = t(i(x))$, the middle equality by the definition of $E$. So $s i = t i$.

        *Existence.* Let $f \colon A \to X$ satisfy $s f = t f$. For each $a \in A$ this says $s(f(a)) = t(f(a))$, so $f(a) \in E$ by the definition of $E$. Hence $\bar{f}(a) = f(a)$ defines a function $\bar{f} \colon A \to E$, and $i(\bar{f}(a)) = f(a)$ for all $a$, that is, $i \bar{f} = f$.

        *Uniqueness.* Let $g \colon A \to E$ satisfy $i g = f$. Then for each $a$, $i(g(a)) = f(a) = i(\bar{f}(a))$. Since $i$ is injective, $g(a) = \bar{f}(a)$. So $g = \bar{f}$. $\qquad\blacksquare$
    - **What made it work.** Existence used the fork hypothesis (it is what puts $f(a)$ inside $E$); uniqueness used injectivity of $i$. When an existence half does not use the hypothesis on the test data, re-read it.

    **More examples.**

    - **$\mathbf{Grp}$.** For homomorphisms $s, t \colon G \to H$ the subset $\{x \in G : s(x) = t(x)\}$ is a subgroup of $G$ (it contains the identity and is closed under products and inverses because $s$ and $t$ are homomorphisms), and its inclusion is an equalizer in $\mathbf{Grp}$. Taking $t$ to be the homomorphism sending everything to the identity of $H$, the equalizer is the **kernel** of $s$.
    - **$\mathbf{Vect}_k$.** The equalizer of linear maps $s, t$ is the inclusion of the subspace $\ker(s - t)$.
    - **$\mathbf{Top}$.** The same subset as in $\mathbf{Set}$, with the subspace topology.
    - **A poset.** Two maps with the same domain and codomain are always equal, so the only equalizers to compute are of pairs $(s, s)$. The identity $1_X$ is an equalizer of $(s, s)$: any $f \colon A \to X$ is a fork, and $f$ itself is the one map with $1_X \circ f = f$.

    **Non-examples.** In $\mathbf{Set}$ let $X = \{0, 1, 2\}$, $Y = \{0, 1\}$, $s(0) = s(1) = s(2) = 0$ and $t(0) = t(1) = 0$, $t(2) = 1$, so that $s$ and $t$ agree exactly on $\{0, 1\}$.

    - The inclusion $\{0\} \hookrightarrow X$ is a fork but not an equalizer: the fork $f \colon \{\ast\} \to X$, $f(\ast) = 1$, does not factor through it. *Existence fails.*
    - The map $j \colon \{0, 1\} \times \{a, b\} \to X$, $j(x, c) = x$, is a fork but not an equalizer: the fork $f(\ast) = 1$ factors as $\ast \mapsto (1, a)$ and as $\ast \mapsto (1, b)$. *Uniqueness fails.*
    - The identity $1_X$ is not even a fork, because $s(2) \neq t(2)$.

    The second non-example fails because $j$ is not injective. That is no accident: in any category an equalizer is a monic. It is a special case of the Lemma of Section 5: a cone on a parallel pair is determined by its leg to $X$, so two maps into $E$ with the same composite with $i$ have the same composite with every projection.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (equalizers); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Pullbacks

    A product pairs up *all* elements of $X$ with all elements of $Y$. Often you only want the pairs that agree after being sent to some third object $Z$: pairs $(x, y)$ with $s(x) = t(y)$. That is a pullback.

    > **Definition (pullback).** Let $s \colon X \to Z$ and $t \colon Y \to Z$ be maps in a category $\mathcal{A}$ with the same codomain. A **pullback** of $(s, t)$ consists of an object $P$ and maps $p_1 \colon P \to X$, $p_2 \colon P \to Y$ such that
    > $$s \circ p_1 = t \circ p_2,$$
    > with the following property: for every object $A$ and every pair of maps $f_1 \colon A \to X$, $f_2 \colon A \to Y$ satisfying $s \circ f_1 = t \circ f_2$, there exists a unique map $\bar{f} \colon A \to P$ such that $p_1 \circ \bar{f} = f_1$ and $p_2 \circ \bar{f} = f_2$. The square formed by $p_1, p_2, s, t$ is then called a **pullback square**.

    **Reading the definition.** To show that a square is a pullback:

    - **The square commutes.** Check $s p_1 = t p_2$.
    - **Fix an arbitrary commuting "outer square".** Take $A$, $f_1$, $f_2$ and assume $s f_1 = t f_2$.
    - **Existence.** Produce $\bar{f} \colon A \to P$ with $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$ (two equations).
    - **Uniqueness.** Any $g \colon A \to P$ satisfying the same two equations equals $\bar{f}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (-1.3, 2.7, r"$A$"), "P": (0, 1.5, r"$P$"), "Y": (1.8, 1.5, r"$Y$"),
            "X": (0, 0, r"$X$"), "Z": (1.8, 0, r"$Z$"),
        },
        [
            ("P", "Y", r"$p_2$", {"side": -1}),
            ("P", "X", r"$p_1$", {"side": -1}),
            ("X", "Z", r"$s$"),
            ("Y", "Z", r"$t$", {"side": -1}),
            ("A", "P", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
            ("A", "Y", r"$f_2$", {"rad": -0.3}),
            ("A", "X", r"$f_1$", {"rad": 0.3}),
        ],
        figsize=(5.0, 4.4),
        title="A pullback square and its universal property",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - **$\mathbf{Set}$.** The set $P = \{(x, y) \in X \times Y : s(x) = t(y)\}$ with $p_1(x, y) = x$ and $p_2(x, y) = y$ is a pullback. It is a special case of the formula proved in Section 6.
    - **Inverse images.** If $t$ is the inclusion of a subset $U \subseteq Z$, the pullback is the inverse image $s^{-1}(U)$, included in $X$. You prove this in `p02_inverse_image_pullback.md`.
    - **Intersections.** If $X$ and $Y$ are both subsets of $Z$ and $s, t$ are the inclusions, the pullback set is $\{(x, y) : x = y\}$, which is in bijection with $X \cap Y$ by $(x, x) \mapsto x$.
    - **A poset.** For $x \le z$ and $y \le z$ the equation $s p_1 = t p_2$ holds automatically (both sides are the one arrow $P \to z$), so a pullback of $x \to z \leftarrow y$ is again a meet $x \wedge y$.
    - **Kernel pairs.** Taking $X = Y$ and $s = t = f$ gives the pullback of $f$ along itself. In $\mathbf{Set}$ it is $\{(x, x') : f(x) = f(x')\}$, the equivalence relation "$f$ cannot tell these apart".

    **Non-example.** In $\mathbf{Set}$ let $X = Y = Z = \{\ast\}$ and $P = \{0, 1\}$, with the only possible maps. The square commutes, because every map into $\{\ast\}$ is the same. But for $A = \{\ast\}$ there are two maps $A \to P$ and both satisfy the two equations. Uniqueness fails, so a commuting square need not be a pullback.

    ### Proof 3: a pullback over a terminal object is a product

    - **Goal.** Let $\mathcal{A}$ have a terminal object $1$, let $X, Y$ be objects, and let $s \colon X \to 1$ and $t \colon Y \to 1$ be the unique maps. For every object $P$ and maps $p_1 \colon P \to X$, $p_2 \colon P \to Y$: $(P, p_1, p_2)$ is a pullback of $(s, t)$ if and only if $(P, p_1, p_2)$ is a product of $X$ and $Y$.
    - **Given.** The definitions of product and pullback; the defining property of $1$: for every object $A$ there is exactly one map $A \to 1$.
    - **Plan.** Compare the two definitions clause by clause. They differ only in the equations $s p_1 = t p_2$ and $s f_1 = t f_2$, so it is enough to show that those equations always hold.
    - **Proof.** Let $A$ be any object and $f_1 \colon A \to X$, $f_2 \colon A \to Y$ any maps. Both $s \circ f_1$ and $t \circ f_2$ are maps $A \to 1$. There is exactly one map $A \to 1$, so $s f_1 = t f_2$. In particular (taking $A = P$) $s p_1 = t p_2$ for any $p_1, p_2$.

        Therefore the condition "the square commutes" in the definition of pullback holds for every $(P, p_1, p_2)$, and the test data "$A, f_1, f_2$ with $s f_1 = t f_2$" are exactly the test data "$A, f_1, f_2$" of the definition of product. The conclusion demanded of each test datum (there exists a unique $\bar{f}$ with $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$) is word for word the same in both definitions. Hence $(P, p_1, p_2)$ satisfies one definition if and only if it satisfies the other. $\qquad\blacksquare$
    - **What made it work.** Maps into a terminal object carry no information, so a condition about them is automatic. When two universal properties look alike, line up their definitions clause by clause and prove only the clauses that differ.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (pullbacks); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Cones and the General Definition

    Products, equalizers and pullbacks follow one pattern. In each there is a small configuration of objects and maps (two objects; a parallel pair; two maps into a common object), and the construction is the best object that maps into every part of the configuration compatibly. To state the pattern once and for all we need a precise meaning for "configuration", and functors provide it.

    > **Definition (diagram).** Let $\mathcal{A}$ be a category and $\mathbf{I}$ a small category. A **diagram of shape $\mathbf{I}$ in $\mathcal{A}$** is a functor $D \colon \mathbf{I} \to \mathcal{A}$.

    The category $\mathbf{I}$ is only a template. Its objects say how many objects the configuration has, its arrows say which maps must be present, and functoriality of $D$ says which composites must agree.

    > **Definition (cone, limit).** Let $D \colon \mathbf{I} \to \mathcal{A}$ be a diagram.
    >
    > A **cone on $D$** consists of an object $A$ of $\mathcal{A}$ (the **vertex**) and a family of maps $\big(f_I \colon A \to D(I)\big)_{I \in \mathbf{I}}$, one for each object $I$ of $\mathbf{I}$, such that for every arrow $u \colon I \to J$ in $\mathbf{I}$
    > $$D(u) \circ f_I = f_J .$$
    >
    > A **limit of $D$** is a cone $\big(p_I \colon L \to D(I)\big)_{I \in \mathbf{I}}$ with the following property: for every cone $\big(f_I \colon A \to D(I)\big)_{I \in \mathbf{I}}$ on $D$ there exists a unique map $\bar{f} \colon A \to L$ such that
    > $$p_I \circ \bar{f} = f_I \quad \text{for all } I \in \mathbf{I}.$$
    > The maps $p_I$ are the **projections** of the limit, the cone $(p_I)$ is a **limit cone**, and we write $L = \lim D$.

    **Reading the definition.** To show that $(L, (p_I))$ is a limit of $D$:

    - **It is a cone.** One leg $p_I$ for *each object* of $\mathbf{I}$, and one equation $D(u) p_I = p_J$ for *each arrow* $u \colon I \to J$ of $\mathbf{I}$.
    - **Fix an arbitrary cone** $(A, (f_I))$. Its cone equations $D(u) f_I = f_J$ are your hypotheses.
    - **Existence.** Produce $\bar{f} \colon A \to L$ and verify $p_I \bar{f} = f_I$ for every $I$.
    - **Uniqueness.** Any $g \colon A \to L$ with $p_I g = f_I$ for every $I$ equals $\bar{f}$.

    The picture shows the part of a cone over a single arrow $u \colon I \to J$ of the shape category. The two triangles on the right commute because $(p_I)$ is a cone; the triangles through the dashed arrow commute by the choice of $\bar{f}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 2.6, r"$A$"), "L": (0, 1.3, r"$L$"),
            "DI": (-1.6, 0, r"$D(I)$"), "DJ": (1.6, 0, r"$D(J)$"),
        },
        [
            ("A", "L", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
            ("L", "DI", r"$p_I$", {"side": -1}),
            ("L", "DJ", r"$p_J$"),
            ("DI", "DJ", r"$D(u)$", {"side": -1}),
            ("A", "DI", r"$f_I$", {"rad": 0.3}),
            ("A", "DJ", r"$f_J$", {"rad": -0.3}),
        ],
        figsize=(5.4, 4.0),
        title="A limit cone (p_I) and the mediating map from another cone (f_I)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The three classics as limits.** The three shape categories are drawn below (identity arrows omitted).

    | Shape $\mathbf{I}$ | A diagram $D$ is | A cone is | A limit is |
    |---|---|---|---|
    | two objects, only identities | a pair of objects $X, Y$ | $A$ with $f_1 \colon A \to X$, $f_2 \colon A \to Y$, no equations | a product |
    | two objects, two parallel arrows | a pair $s, t \colon X \to Y$ | $f_X \colon A \to X$, $f_Y \colon A \to Y$ with $s f_X = f_Y$ and $t f_X = f_Y$ | an equalizer |
    | three objects, two arrows into one of them | $s \colon X \to Z$, $t \colon Y \to Z$ | $f_X, f_Y, f_Z$ with $s f_X = f_Z$ and $t f_Y = f_Z$ | a pullback |
    | no objects | nothing | an object $A$ | a terminal object |

    In the equalizer row the leg $f_Y$ is forced: it must equal $s f_X$. So a cone is determined by $f_X$ alone, and the remaining condition is $s f_X = t f_X$. That is a fork. In the pullback row the leg $f_Z$ is forced in the same way and the remaining condition is $s f_X = t f_Y$. This is why the earlier definitions mention fewer legs than the cone definition does: the omitted legs are determined by the others.

    **Two more examples.**

    - **A tower.** Let $\mathbf{I}$ have objects $0, 1, 2, \dots$ and exactly one arrow $n \to m$ whenever $n \ge m$. A diagram is a sequence $\cdots \to X_2 \to X_1 \to X_0$. In $\mathbf{Set}$ a limit is the set of sequences $(x_0, x_1, x_2, \dots)$ with $x_n \in X_n$ and each $x_{n+1}$ mapping to $x_n$ (this follows from Section 6). For $X_n = \mathbb{Z}/p^n\mathbb{Z}$ with the reduction maps this is how the $p$-adic integers are defined.
    - **Fixed points.** A group $G$ is a category with one object $\star$ (1A), and a functor $D \colon G \to \mathbf{Set}$ is a set $X = D(\star)$ with an action of $G$. A cone on $D$ with vertex $A$ is a function $f \colon A \to X$ with $g \cdot f(a) = f(a)$ for all $g \in G$ and $a \in A$, that is, a function into the set $X^G$ of fixed points. The inclusion $X^G \hookrightarrow X$ is a limit of $D$.

    **Non-example.** A cone is not automatically a limit cone. In $\mathbf{Set}$, on the pair $X = \{0, 1\}$, $Y = \{0, 1\}$, the one-element set $\{\ast\}$ with $f_1(\ast) = 0$, $f_2(\ast) = 0$ is a cone. It is not a limit: the cone with vertex $\{\ast\}$ and legs $\ast \mapsto 1$, $\ast \mapsto 1$ does not factor through it.

    **Vocabulary.** A category **has limits of shape $\mathbf{I}$** if every diagram of shape $\mathbf{I}$ in it has a limit. It **has all limits** (is **complete**) if it has limits of shape $\mathbf{I}$ for every *small* category $\mathbf{I}$. A **finite limit** is a limit of a diagram whose shape has finitely many objects and arrows. The restriction to small shapes is the reason 3A was needed: a product indexed by a proper class is too much to ask even of $\mathbf{Set}$.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (the definition of limit); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "a1": (0, 1.2, r"$\bullet$"), "a2": (1.6, 1.2, r"$\bullet$"),
            "b1": (3.6, 1.2, r"$\bullet$"), "b2": (5.6, 1.2, r"$\bullet$"),
            "c1": (7.6, 0.3, r"$\bullet$"), "c2": (9.4, 2.1, r"$\bullet$"), "c3": (9.4, 0.3, r"$\bullet$"),
            "la": (0.8, -0.6, "product"), "lb": (4.6, -0.6, "equalizer"), "lc": (8.5, -0.6, "pullback"),
        },
        [
            ("b1", "b2", "", {"rad": 0.3}),
            ("b1", "b2", "", {"rad": -0.3}),
            ("c1", "c3", ""),
            ("c2", "c3", ""),
        ],
        figsize=(8.6, 3.2),
        title="The three classic shape categories (identities not drawn)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Limits Are Unique up to Unique Isomorphism

    The definition says "*a* limit", not "*the* limit". In $\mathbf{Set}$ the sets $X \times Y$ and $Y \times X$ are different sets, and each is a product of $X$ and $Y$ with suitable projections. This section proves that the ambiguity is harmless: two limits of the same diagram are isomorphic, and there is exactly one isomorphism that respects the projections. This is the pattern "unique up to unique isomorphism" from 0C and 2C, now for cones.

    We need one lemma first. It is the uniqueness half of the universal property, repackaged as a tool, and it gets used constantly from here on.

    ### Proof 4 (Lemma): maps into a limit are determined by their composites with the projections

    - **Goal.** Let $(p_I \colon L \to D(I))_{I \in \mathbf{I}}$ be a limit cone on $D \colon \mathbf{I} \to \mathcal{A}$. For every object $A$ and all maps $h, h' \colon A \to L$: if $p_I \circ h = p_I \circ h'$ for all $I \in \mathbf{I}$, then $h = h'$.
    - **Given.** The definition of limit, in particular its uniqueness clause.
    - **Plan.** Uniqueness clauses talk about mediating maps for a cone. So build a cone for which both $h$ and $h'$ are mediating maps.
    - **Proof.** Define $f_I = p_I \circ h$ for each $I$. We check that $(f_I)$ is a cone on $D$ with vertex $A$: for $u \colon I \to J$,
      $$D(u) \circ f_I = D(u) \circ p_I \circ h = p_J \circ h = f_J,$$
      where the middle equality holds because $(p_I)$ is a cone. Now $h$ satisfies $p_I h = f_I$ for all $I$ by the definition of $f_I$, and $h'$ satisfies $p_I h' = p_I h = f_I$ for all $I$ by hypothesis. By the uniqueness clause of the definition of limit, applied to the cone $(f_I)$, there is only one map with this property. So $h = h'$. $\qquad\blacksquare$
    - **What made it work.** To prove two maps *into* a limit are equal, compose each with every projection and compare. For a product this says: a map into $X \times Y$ is determined by its two components.

    ### Proof 5 (Theorem): uniqueness of limits

    - **Goal.** Let $D \colon \mathbf{I} \to \mathcal{A}$ be a diagram and let $(p_I \colon L \to D(I))$ and $(p'_I \colon L' \to D(I))$ both be limit cones on $D$. Then there exists a unique map $j \colon L \to L'$ such that $p'_I \circ j = p_I$ for all $I$, and this $j$ is an isomorphism.
    - **Given.** The universal property of $(L, (p_I))$; the universal property of $(L', (p'_I))$; the Lemma (Proof 4) for each of them.
    - **Plan.** Use each limit as a test cone for the other, which produces maps $j \colon L \to L'$ and $k \colon L' \to L$. Then show $k j = 1_L$ and $j k = 1_{L'}$ by the Lemma.
    - **Proof.** *Existence and uniqueness of $j$.* The cone $(p_I)$ is a cone on $D$ with vertex $L$. Since $(p'_I)$ is a limit cone, there exists a unique map $j \colon L \to L'$ with $p'_I j = p_I$ for all $I$. That is the first claim.

        *A map the other way.* Exchanging the roles: $(p'_I)$ is a cone with vertex $L'$ and $(p_I)$ is a limit cone, so there exists a unique map $k \colon L' \to L$ with $p_I k = p'_I$ for all $I$.

        *$k j = 1_L$.* Both $k j$ and $1_L$ are maps $L \to L$. For every $I$,
        $$p_I \circ (k j) = (p_I k) j = p'_I j = p_I = p_I \circ 1_L,$$
        using associativity, then the defining property of $k$, then that of $j$, then the identity axiom. By the Lemma applied to the limit cone $(p_I)$, $k j = 1_L$.

        *$j k = 1_{L'}$.* For every $I$, $p'_I \circ (j k) = (p'_I j) k = p_I k = p'_I = p'_I \circ 1_{L'}$. By the Lemma applied to the limit cone $(p'_I)$, $j k = 1_{L'}$.

        So $j$ has the two-sided inverse $k$, and is an isomorphism. $\qquad\blacksquare$
    - **What made it work.** The only map $L \to L$ that commutes with all the projections is the identity. Any round trip $L \to L' \to L$ built from mediating maps commutes with the projections, so it is forced to be the identity. Reach for this whenever two objects have the same universal property.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "L": (-1.3, 1.6, r"$L$"), "Lp": (1.3, 1.6, r"$L'$"), "DI": (0, 0, r"$D(I)$"),
        },
        [
            ("L", "Lp", r"$j$", {"rad": -0.25, "dashed": True, "color": "#b91c1c"}),
            ("Lp", "L", r"$k$", {"rad": -0.25, "dashed": True, "color": "#b91c1c"}),
            ("L", "DI", r"$p_I$", {"side": -1}),
            ("Lp", "DI", r"$p'_I$"),
        ],
        figsize=(5.8, 3.3),
        title="Two limit cones on one diagram: j and k are inverse",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The theorem has a converse, which lets you recognise limits by comparing with a known one.

    ### Proof 6 (Proposition): a cone isomorphic to a limit cone is a limit cone

    - **Goal.** Let $(p_I \colon L \to D(I))$ be a limit cone on $D$ and let $j \colon L'' \to L$ be an isomorphism. Then $(p_I \circ j \colon L'' \to D(I))_{I \in \mathbf{I}}$ is a limit cone on $D$.
    - **Given.** The universal property of $(p_I)$; the inverse $j^{-1} \colon L \to L''$.
    - **Plan.** Universal-property proof, transporting everything along $j$.
    - **Proof.** *Cone.* For $u \colon I \to J$, $D(u) \circ (p_I j) = (D(u) p_I) j = p_J j$.

        *Existence.* Let $(f_I \colon A \to D(I))$ be a cone. Let $\bar{f} \colon A \to L$ be the map with $p_I \bar{f} = f_I$ for all $I$, and put $g = j^{-1} \bar{f} \colon A \to L''$. Then $(p_I j) g = p_I j j^{-1} \bar{f} = p_I \bar{f} = f_I$.

        *Uniqueness.* Let $g' \colon A \to L''$ satisfy $(p_I j) g' = f_I$ for all $I$. Then $j g' \colon A \to L$ satisfies $p_I (j g') = f_I$ for all $I$, so $j g' = \bar{f}$ by the uniqueness clause for $(p_I)$. Composing with $j^{-1}$ on the left, $g' = j^{-1} \bar{f} = g$. $\qquad\blacksquare$
    - **What made it work.** An isomorphism lets you translate each clause of a universal property back and forth without loss.

    Together, Proofs 5 and 6 say: once you know one limit of $D$, the limits of $D$ are exactly the cones obtained from it by composing with an isomorphism. This justifies speaking of "the" limit, and it explains why $X \times Y$ and $Y \times X$ are both products.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375); the pattern is the one of [Leinster §2.3](https://arxiv.org/abs/1612.09375) (uniqueness of initial objects). See also [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Limits in $\mathbf{Set}$: the Explicit Formula

    In $\mathbf{Set}$ every limit can be written down. The recipe combines the two ideas you have seen: take *tuples* (as for products) and keep only those satisfying *equations* (as for equalizers).

    > **Theorem (limits in $\mathbf{Set}$).** Let $\mathbf{I}$ be a small category and $D \colon \mathbf{I} \to \mathbf{Set}$ a diagram. Put
    > $$\boxed{\;L = \Big\{ (x_I)_{I \in \mathbf{I}} \in \prod_{I \in \mathbf{I}} D(I) \;:\; (Du)(x_I) = x_J \text{ for every arrow } u \colon I \to J \text{ in } \mathbf{I} \Big\}\;}$$
    > and let $p_I \colon L \to D(I)$ send a tuple to its $I$-th entry. Then $(p_I \colon L \to D(I))_{I \in \mathbf{I}}$ is a limit cone on $D$.

    **Reading the formula.** An element of $L$ is a choice of one element $x_I$ from *each* set of the diagram, such that *every* map of the diagram carries the chosen element of its domain to the chosen element of its codomain.

    - For the two-object discrete shape there are no non-identity arrows and no conditions: $L = X \times Y$.
    - For a parallel pair $s, t \colon X \to Y$: $L = \{(x, y) : s(x) = y,\ t(x) = y\}$, which is in bijection with $\{x : s(x) = t(x)\}$ by $(x, y) \mapsto x$.
    - For $X \xrightarrow{s} Z \xleftarrow{t} Y$: $L = \{(x, y, z) : s(x) = z = t(y)\}$, in bijection with $\{(x, y) : s(x) = t(y)\}$.

    By Proof 6, those bijections turn the limit given by the formula into the more economical descriptions of Sections 1–3.

    ### Proof 7: the formula gives a limit

    - **Goal.** $(p_I)$ is a cone on $D$; and for every set $A$ and every cone $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$ there exists a unique function $\bar{f} \colon A \to L$ with $p_I \circ \bar{f} = f_I$ for all $I$.
    - **Given.** The definition of $L$ and of $p_I$; two tuples are equal exactly when all their entries are equal.
    - **Plan.** The same two-step proof as for $X \times Y$ (Proof 1), with one extra check in the existence half: the tuple we write down must satisfy the equations defining $L$.
    - **Proof.** *Cone.* Let $u \colon I \to J$ be an arrow and $x = (x_K)_{K \in \mathbf{I}} \in L$. Then $(Du)(p_I(x)) = (Du)(x_I) = x_J = p_J(x)$, the middle equality by the definition of $L$. So $D(u) \circ p_I = p_J$.

        *Existence.* Let $(f_I)$ be a cone with vertex $A$. For $a \in A$ define $\bar{f}(a) = (f_I(a))_{I \in \mathbf{I}}$. We must check $\bar{f}(a) \in L$: for $u \colon I \to J$, $(Du)(f_I(a)) = f_J(a)$ because $(f_I)$ is a cone. So $\bar{f}$ is a function $A \to L$, and $p_I(\bar{f}(a)) = f_I(a)$ by the definition of $p_I$. Hence $p_I \bar{f} = f_I$ for all $I$.

        *Uniqueness.* Let $g \colon A \to L$ satisfy $p_I g = f_I$ for all $I$. For $a \in A$, the $I$-th entry of the tuple $g(a)$ is $p_I(g(a)) = f_I(a)$, which is the $I$-th entry of $\bar{f}(a)$. All entries agree, so $g(a) = \bar{f}(a)$; hence $g = \bar{f}$. $\qquad\blacksquare$
    - **What made it work.** The cone equations on $(f_I)$ are exactly the equations defining $L$, read at a single element $a$. Consequently $\mathbf{Set}$ has all limits.

    **A practical remark.** If the arrows of $\mathbf{I}$ are all composites of a few **generating** arrows, it is enough to impose the equations for the generators. Indeed if $(Du)(x_I) = x_J$ and $(Dv)(x_J) = x_K$ then $D(v u)(x_I) = (Dv)((Du)(x_I)) = x_K$ by functoriality of $D$; and $D(1_I)(x_I) = x_I$ always. The calculator below uses this: you give it only the generating maps.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (limits in $\mathbf{Set}$); [Riehl §3.2](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Interactive: limit calculator for finite diagrams of finite sets

    Choose a diagram shape and the size parameter $n$. The calculator builds the diagram, enumerates the product of all its sets, keeps the tuples satisfying the equations, and lists them. Before moving the slider, predict the number of elements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    limit_shape = mo.ui.dropdown(
        options=[
            "product: X, Y",
            "equalizer: s, t : X -> Y",
            "pullback: X -> Z <- Y",
            "tower: X2 -> X1 -> X0",
            "fixed points: r : X -> X",
        ],
        value="pullback: X -> Z <- Y",
        label="Diagram",
    )
    limit_n = mo.ui.slider(start=2, stop=9, step=1, value=6, label="n (size of X or X2)")
    mo.vstack([limit_shape, limit_n])
    return limit_n, limit_shape


@app.cell(hide_code=True)
def _(limit_n, limit_shape, mo):
    def _run():
        import itertools

        _n = limit_n.value
        _kind = limit_shape.value.split(":")[0]
        if _kind == "product":
            _sets = {"X": list(range(_n)), "Y": [0, 1, 2]}
            _maps = {}
            _desc = {}
            _note = "No arrows, so no equations: every pair survives."
        elif _kind == "equalizer":
            _sets = {"X": list(range(_n)), "Y": [0, 1, 2]}
            _maps = {
                "s": ("X", "Y", {x: x % 3 for x in range(_n)}),
                "t": ("X", "Y", {x: (x * x) % 3 for x in range(_n)}),
            }
            _desc = {"s": "x mod 3", "t": "x*x mod 3"}
            _note = "The Y-entry is forced by the X-entry, so the limit is in bijection with {x : s(x) = t(x)}."
        elif _kind == "pullback":
            _sets = {"X": list(range(_n)), "Y": [0, 1, 2, 3], "Z": [0, 1, 2]}
            _maps = {
                "s": ("X", "Z", {x: x % 3 for x in range(_n)}),
                "t": ("Y", "Z", {y: y % 3 for y in range(4)}),
            }
            _desc = {"s": "x mod 3", "t": "y mod 3"}
            _note = "The Z-entry is forced, so the limit is in bijection with {(x, y) : s(x) = t(y)}."
        elif _kind == "tower":
            _sets = {"X2": list(range(_n)), "X1": [0, 1, 2, 3], "X0": [0, 1]}
            _maps = {
                "a": ("X2", "X1", {x: x % 4 for x in range(_n)}),
                "b": ("X1", "X0", {x: x % 2 for x in range(4)}),
            }
            _desc = {"a": "x mod 4", "b": "x mod 2"}
            _note = "Compare the count with the size of X2. Which entries of a tuple are forced by which?"
        else:
            _sets = {"X": list(range(_n))}
            _maps = {"r": ("X", "X", {x: (-x) % _n for x in range(_n)})}
            _desc = {"r": "-x mod n"}
            _note = "One object and one generating arrow r with r(r(x)) = x: an action of the two-element group. The limit is the set of fixed points."

        _names = list(_sets)
        _limit = []
        for _tuple in itertools.product(*[_sets[_k] for _k in _names]):
            _x = dict(zip(_names, _tuple))
            if all(_fn[_x[_dom]] == _x[_cod] for (_dom, _cod, _fn) in _maps.values()):
                _limit.append(_tuple)

        _total = 1
        for _k in _names:
            _total *= len(_sets[_k])
        _lines = ["| Set | Elements |", "|---|---|"]
        for _k in _names:
            _lines.append("| $" + _k + "$ | " + ", ".join(str(_e) for _e in _sets[_k]) + " |")
        _lines.append("")
        if _maps:
            _lines += ["| Generating map | Rule | Equation imposed on a tuple |", "|---|---|---|"]
            for _m, (_dom, _cod, _fn) in _maps.items():
                _lines.append("| $" + _m + " \\colon " + _dom + " \\to " + _cod + "$ | " + _desc[_m]
                              + " | $" + _m + "(x_{" + _dom + "}) = x_{" + _cod + "}$ |")
            _lines.append("")
        _lines.append("**Tuples in the product:** " + str(_total) + " &nbsp; **Tuples in the limit:** " + str(len(_limit)))
        _lines.append("")
        _lines.append("Order of entries: (" + ", ".join(_names) + ")")
        _lines.append("")
        _lines.append("`" + "  ".join(str(_t) for _t in _limit) + "`" if _limit else "*The limit is the empty set.*")
        _lines.append("")
        _lines.append(_note)
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. All Limits from Products and Equalizers

    The formula for limits in $\mathbf{Set}$ has two stages: form a product, then cut out the solutions of some equations. The next theorem says that the same two-stage construction works in *any* category that has products and equalizers. It is the reason those two shapes get so much attention: once you have them, you have everything.

    > **Theorem.** Let $\mathcal{A}$ be a category that has all small products (a product for every family of objects indexed by a set) and all equalizers. Then $\mathcal{A}$ has all small limits.

    **The idea.** In $\mathbf{Set}$, an element of the limit is a tuple $(x_I)$ in $\prod_I D(I)$ satisfying one equation $(Du)(x_I) = x_J$ per arrow $u \colon I \to J$. We bundle all those equations into a single one. An equation per arrow $u$, each taking place in $D(\operatorname{cod} u)$, is one equation in the product $\prod_u D(\operatorname{cod} u)$. So we want two maps
    $$s, t \colon \prod_{I} D(I) \;\rightrightarrows\; \prod_{u} D(\operatorname{cod} u),$$
    where $s$ records, for each $u \colon I \to J$, the entry $x_J$, and $t$ records $(Du)(x_I)$. The limit is their equalizer. In the picture, $P$ is the first product and $Q$ the second.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 1.6, r"$A$"), "L": (0, 0, r"$L$"),
            "P": (1.8, 0, r"$P$"), "Q": (3.8, 0, r"$Q$"),
        },
        [
            ("L", "P", r"$e$", {"side": -1}),
            ("P", "Q", r"$s$", {"rad": -0.25}),
            ("P", "Q", r"$t$", {"rad": 0.25}),
            ("A", "P", r"$f$"),
            ("A", "L", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
        ],
        figsize=(6.2, 2.9),
        title="L is an equalizer of s, t : P -> Q, where P and Q are products",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proof 8: products and equalizers give all limits

    - **Goal.** For every small category $\mathbf{I}$ and every diagram $D \colon \mathbf{I} \to \mathcal{A}$ there exists a cone $(p_I \colon L \to D(I))_{I \in \mathbf{I}}$ such that for every cone $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ there is a unique $\bar{f} \colon A \to L$ with $p_I \bar{f} = f_I$ for all $I$.
    - **Given.** $\mathcal{A}$ has a product of every set-indexed family and an equalizer of every parallel pair. Because $\mathbf{I}$ is small, its objects form a set and its arrows form a set. We also have the Lemma (Proof 4) for products: two maps into a product are equal if they have the same composite with every projection.
    - **Plan.** Construct $L$ as an equalizer of two maps between two products. Then run a universal-property proof in which each half is done in two stages: first use the product, then use the equalizer.
    - **Proof.** *Construction.* Let
      $$P = \prod_{I \in \mathrm{ob}\,\mathbf{I}} D(I) \quad\text{with projections } \pi_I \colon P \to D(I),$$
      $$Q = \prod_{u \in \mathrm{arr}\,\mathbf{I}} D(\operatorname{cod} u) \quad\text{with projections } \rho_u \colon Q \to D(\operatorname{cod} u).$$
      Here $Q$ has one factor for each arrow $u \colon I \to J$ of $\mathbf{I}$, and that factor is $D(J)$. A map into $Q$ is determined by, and can be specified by, its composites with the $\rho_u$ (the universal property of the product $Q$). So we may define $s, t \colon P \to Q$ by requiring, for every arrow $u \colon I \to J$,
      $$\rho_u \circ s = \pi_J, \qquad \rho_u \circ t = D(u) \circ \pi_I .$$
      Let $e \colon L \to P$ be an equalizer of $s$ and $t$, and define $p_I = \pi_I \circ e \colon L \to D(I)$.

        *$(p_I)$ is a cone.* Let $u \colon I \to J$ be an arrow of $\mathbf{I}$. Then
        $$D(u) \circ p_I = D(u) \circ \pi_I \circ e = \rho_u \circ t \circ e = \rho_u \circ s \circ e = \pi_J \circ e = p_J,$$
        using in turn: the definition of $p_I$; the defining equation of $t$; that $e$ is a fork, $s e = t e$; the defining equation of $s$; the definition of $p_J$.

        *Existence of the mediating map.* Let $(f_I \colon A \to D(I))$ be a cone on $D$.

        Stage 1 (product). By the universal property of $P$ there is a unique map $f \colon A \to P$ with $\pi_I f = f_I$ for all objects $I$.

        Stage 2 (equalizer). We claim $s f = t f$. Both are maps $A \to Q$, and $Q$ is a product, so by the Lemma it is enough to show $\rho_u s f = \rho_u t f$ for every arrow $u \colon I \to J$. We compute
        $$\rho_u s f = \pi_J f = f_J, \qquad \rho_u t f = D(u)\, \pi_I f = D(u)\, f_I = f_J,$$
        the last equality being the cone equation for $(f_I)$ at $u$. So $s f = t f$, that is, $f$ is a fork on $(s, t)$. By the universal property of the equalizer $e$ there is a unique map $\bar{f} \colon A \to L$ with $e \bar{f} = f$. Then for every $I$,
        $$p_I \bar{f} = \pi_I e \bar{f} = \pi_I f = f_I .$$

        *Uniqueness of the mediating map.* Let $g \colon A \to L$ satisfy $p_I g = f_I$ for all $I$.

        Stage 1 (product). The map $e g \colon A \to P$ satisfies $\pi_I (e g) = p_I g = f_I$ for all $I$. The map $f$ is the unique map with that property. So $e g = f$.

        Stage 2 (equalizer). Now $g$ and $\bar{f}$ are both maps $A \to L$ whose composite with $e$ is $f$. By the uniqueness clause of the equalizer, $g = \bar{f}$. $\qquad\blacksquare$
    - **What made it work.** A cone is a family of maps (handled by a product) satisfying equations (handled by an equalizer). The cone equations for $(f_I)$ became the single equation $s f = t f$. Each half of the proof peeled off the two layers in order: product first, equalizer second.

    **Reading the proof in $\mathbf{Set}$.** There $P$ is the set of all tuples $(x_I)$, $s$ sends a tuple to the family $(x_{\operatorname{cod} u})_u$, and $t$ sends it to $((Du)(x_{\operatorname{dom} u}))_u$. The equalizer is the set of tuples with $x_J = (Du)(x_I)$ for all $u \colon I \to J$, which is the formula of Section 6.

    **Finite version.** If $\mathbf{I}$ has finitely many objects and arrows, both products in the construction are finite. So the same proof shows: *a category with all finite products and all equalizers has all finite limits.* (A category has all finite products as soon as it has a terminal object and binary products; we do not prove that here.)

    **Consequences.** $\mathbf{Grp}$, $\mathbf{Ab}$, $\mathbf{Vect}_k$ and $\mathbf{Top}$ all have products of arbitrary families (cartesian products with coordinatewise structure, respectively the product topology) and equalizers (Section 2), so each has all limits. A poset has all limits if and only if every subset has a meet, because equalizers in a poset always exist (Section 2) and products are meets.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (limits from products and equalizers).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8. Monics and Pullbacks

    Recall from 1B: a map $m \colon X \to Y$ is **monic** if for every object $A$ and all maps $h, k \colon A \to X$, $m h = m k$ implies $h = k$. In $\mathbf{Set}$ the monics are the injections. Pullbacks interact with monics in two ways.

    First, monics are *stable under pullback*: if you pull a monic back along any map you get a monic. In $\mathbf{Set}$ this generalises the fact that the inverse image of a subset is a subset.

    ### Proof 9: the pullback of a monic is monic

    - **Goal.** Let the square below be a pullback in a category $\mathcal{A}$, so $s p_1 = t p_2$ and the universal property holds. If $t \colon Y \to Z$ is monic, then $p_1 \colon P \to X$ is monic: for every object $A$ and all $h, k \colon A \to P$, if $p_1 h = p_1 k$ then $h = k$.
    - **Given.** The pullback property of the square; $t$ is monic.
    - **Plan.** To prove two maps into a pullback equal, show they have the same composite with *both* projections (the Lemma, Proof 4, for a pullback). We are told about $p_1$; we get $p_2$ from the monic $t$.
    - **Proof.** Let $h, k \colon A \to P$ with $p_1 h = p_1 k$. Then
      $$t \circ (p_2 h) = (t p_2) h = (s p_1) h = s (p_1 h) = s (p_1 k) = (s p_1) k = (t p_2) k = t \circ (p_2 k),$$
      using associativity, the commuting square $t p_2 = s p_1$, the hypothesis $p_1 h = p_1 k$, and the commuting square again. Since $t$ is monic, $p_2 h = p_2 k$.

        Now put $f_1 = p_1 h$ and $f_2 = p_2 h$. They satisfy $s f_1 = s p_1 h = t p_2 h = t f_2$, so they are valid test data for the pullback. The map $h$ satisfies $p_1 h = f_1$ and $p_2 h = f_2$ by definition, and the map $k$ satisfies $p_1 k = p_1 h = f_1$ and $p_2 k = p_2 h = f_2$ by what we have shown. By the uniqueness clause of the pullback, $h = k$. $\qquad\blacksquare$
    - **What made it work.** The projections of a pullback are jointly "injective"; monicity of $t$ lets you recover the missing projection from the one you were given.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (-1.9, 1.5, r"$A$"), "P": (0, 1.5, r"$P$"), "Y": (1.8, 1.5, r"$Y$"),
            "X": (0, 0, r"$X$"), "Z": (1.8, 0, r"$Z$"),
        },
        [
            ("A", "P", r"$h$", {"rad": -0.25}),
            ("A", "P", r"$k$", {"rad": 0.25}),
            ("P", "Y", r"$p_2$", {"side": -1}),
            ("P", "X", r"$p_1$", {"side": -1, "color": "#1d4ed8"}),
            ("X", "Z", r"$s$"),
            ("Y", "Z", r"$t$", {"side": -1, "color": "#1d4ed8"}),
        ],
        figsize=(5.4, 3.3),
        title="If t is monic then p1 is monic",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Second, monicity itself can be *expressed* as a statement about a pullback. For any map $f \colon X \to Y$, the square with $1_X$ along the top and down the left side, and $f$ along the bottom and down the right side, commutes (it is drawn below). The statement is:

    > $f$ is monic **if and only if** this square is a pullback.

    This matters because it converts a property of a map (being monic) into a property of a limit, and limits are something functors can preserve (5C). The proof is yours: `p04_monic_iff_pullback.md`.

    **Example.** In $\mathbf{Set}$ the pullback of $f$ along itself is $\{(x, x') : f(x) = f(x')\}$. The square above being a pullback says that this set is no bigger than the diagonal $\{(x, x)\}$, which is injectivity of $f$.

    **Non-example.** The converse of Proof 9 fails: $p_1$ can be monic without $t$ being monic. In $\mathbf{Set}$ take $X = \varnothing$. Then $P = \varnothing$ whatever $t$ is, and $p_1 \colon \varnothing \to \varnothing$ is injective, even if $t$ is not.

    > **References.** [Leinster §5.1](https://arxiv.org/abs/1612.09375) (monics and pullbacks); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"P": (0, 1.5, r"$X$"), "Y": (1.8, 1.5, r"$X$"), "X": (0, 0, r"$X$"), "Z": (1.8, 0, r"$Y$")},
        [
            ("P", "Y", r"$1_X$", {"side": -1}),
            ("P", "X", r"$1_X$", {"side": -1}),
            ("X", "Z", r"$f$"),
            ("Y", "Z", r"$f$", {"side": -1}),
        ],
        figsize=(4.6, 3.2),
        title="f is monic iff this square is a pullback",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Proving existence and calling it a day.** "Define $\bar{f}(a) = (f_1(a), f_2(a))$; it commutes with the projections; done." *Diagnosis:* half a proof. The object $X \times Y \times \{0, 1\}$ also admits a mediating map for every cone. Uniqueness is what rules it out.
    2. **Proving uniqueness by exhibiting one map.** "The mediating map is $j^{-1} \bar{f}$, so it is unique." *Diagnosis:* writing down a formula shows there is *at least* one. Uniqueness starts with "let $g$ be any map satisfying the equations" and ends with "$g = \bar{f}$".
    3. **Forgetting that a limit is a cone, not an object.** "The limit of $X \to Z \leftarrow Y$ is the set $P$." *Diagnosis:* without the projections there is nothing to be universal. The same object with different projections can fail to be a limit (the first non-example of Section 1).
    4. **Not using the cone condition.** If the existence half never uses $s f = t f$ (or $D(u) f_I = f_J$), the argument would work for a non-cone, and for a non-cone no mediating map exists. *Diagnosis:* find the step where you checked that your map lands in $L$; that is where the hypothesis belongs.
    5. **Arguing with elements in a general category.** "Take $x \in P$ with $p_1(x) = \dots$". *Diagnosis:* objects of an arbitrary category have no elements. In a general category the substitute for "these two elements are equal" is the Lemma of Section 5: compose with every projection.

    ---

    ## Why This Matters

    - **5B** turns every arrow of this module around: sums, coequalizers, pushouts, colimits. Each theorem here has a dual there, with no new proof needed.
    - **5C** asks which functors carry limit cones to limit cones. The Lemma (Proof 4) and Proofs 5–6 are the tools used there; the pullback characterisation of monics is what makes "a functor that preserves pullbacks preserves monics" a short argument.
    - **6A** shows that the definition of limit is a representability statement (cones with vertex $A$ correspond to maps $A \to \lim D$) and also an adjunction. The uniqueness theorem of Section 5 is then a special case of the uniqueness of representations from 4C.
    - **6B** computes limits of presheaves one object at a time, using the $\mathbf{Set}$ formula of Section 6 at each object.
    - **6C** proves that right adjoints preserve limits. The theorem of Section 7 is the standard labour-saving device around such results: to show that a category has all limits it is enough to handle products and equalizers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    These exercises work with finite diagrams of finite sets. A diagram is encoded by its sets and its **generating** maps only:

    ```python
    diagram = {
        "sets": {"X": [0, 1, 2], "Y": [0, 1]},
        "maps": {"s": ("X", "Y", {0: 0, 1: 1, 2: 0})},   # name -> (domain, codomain, function as a dict)
    }
    ```

    A cone with vertex a finite set `A` is a dict `legs = {"X": {a: ..., ...}, "Y": {a: ..., ...}}` giving one function out of `A` per set of the diagram. Fill in each `# TODO`, then un-comment the `print` checks and compare with the expected values.

    ### Exercise 1: Is this family of maps a cone?

    Write `is_cone(A, legs, diagram)`: it returns `True` exactly when, for every generating map $u \colon I \to J$ of the diagram and every $a \in A$, $(Du)(f_I(a)) = f_J(a)$.
    """)
    return


@app.cell
def _():
    def _run():
        diagram = {
            "sets": {"X": [0, 1, 2, 3], "Y": [0, 1, 2], "Z": [0, 1]},
            "maps": {
                "s": ("X", "Z", {0: 0, 1: 1, 2: 0, 3: 1}),
                "t": ("Y", "Z", {0: 0, 1: 1, 2: 1}),
            },
        }
        A = ["a", "b"]
        legs_good = {"X": {"a": 1, "b": 2}, "Y": {"a": 2, "b": 0}, "Z": {"a": 1, "b": 0}}
        legs_bad = {"X": {"a": 1, "b": 2}, "Y": {"a": 0, "b": 0}, "Z": {"a": 1, "b": 0}}

        def is_cone(A, legs, diagram):
            # TODO: for every generating map (dom, cod, fn) and every a in A,
            #       compare fn[legs[dom][a]] with legs[cod][a]
            _result = ...
            return _result

        # print(is_cone(A, legs_good, diagram))   # expected: True
        # print(is_cone(A, legs_bad, diagram))    # expected: False

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: The mediating map, and a brute-force uniqueness check

    The scaffolding computes the limit $L$ of a diagram by the formula of Section 6, as a list of tuples (entries in the order of `diagram["sets"]`). Given a cone, write

    - `mediating(A, legs, diagram)`: the function $\bar{f} \colon A \to L$ as a dict `{a: tuple}`;
    - `count_mediating(A, legs, diagram)`: the number of functions $g \colon A \to L$, among **all** $|L|^{|A|}$ of them, that satisfy $p_I \circ g = f_I$ for every $I$. The universal property predicts the answer.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        diagram = {
            "sets": {"X": [0, 1, 2, 3], "Y": [0, 1, 2], "Z": [0, 1]},
            "maps": {
                "s": ("X", "Z", {0: 0, 1: 1, 2: 0, 3: 1}),
                "t": ("Y", "Z", {0: 0, 1: 1, 2: 1}),
            },
        }
        names = list(diagram["sets"])

        def limit_of(diagram):
            _out = []
            for _tuple in itertools.product(*[diagram["sets"][_k] for _k in names]):
                _x = dict(zip(names, _tuple))
                if all(_fn[_x[_d]] == _x[_c] for (_d, _c, _fn) in diagram["maps"].values()):
                    _out.append(_tuple)
            return _out

        L = limit_of(diagram)
        A = ["a", "b"]
        legs = {"X": {"a": 1, "b": 2}, "Y": {"a": 2, "b": 0}, "Z": {"a": 1, "b": 0}}

        def mediating(A, legs, diagram):
            # TODO: the tuple at a has entry legs[I][a] in position I (for I in names)
            _fbar = ...
            return _fbar

        def count_mediating(A, legs, diagram):
            _count = 0
            for _values in itertools.product(L, repeat=len(A)):
                _g = dict(zip(A, _values))
                # TODO: add 1 to _count if, for every position i and every a in A,
                #       entry i of _g[a] equals legs[names[i]][a]
                ...
            return _count

        # print(len(L))                              # expected: 6
        # print(mediating(A, legs, diagram))         # expected: {'a': (1, 2, 1), 'b': (2, 0, 0)}
        # print(len(L) ** len(A))                    # expected: 36   (functions A -> L to search)
        # print(count_mediating(A, legs, diagram))   # expected: 1

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: A pullback built from a product and an equalizer

    Section 7 says a pullback of $X \xrightarrow{s} Z \xleftarrow{t} Y$ can be built in two stages. For this shape the construction simplifies: form the product $X \times Y$, then take the equalizer of the two functions $s \circ \mathrm{pr}_1,\ t \circ \mathrm{pr}_2 \colon X \times Y \to Z$. Do exactly that, and compare with the direct description $\{(x, y) : s(x) = t(y)\}$.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        X = list(range(7))
        Y = list(range(5))
        s = {x: (x * x) % 4 for x in X}      # s : X -> Z
        t = {y: y % 4 for y in Y}            # t : Y -> Z

        product = list(itertools.product(X, Y))

        # TODO: the two composites X x Y -> Z, each as a dict keyed by the pairs in `product`
        s_pr1 = ...
        t_pr2 = ...

        def equalizer(domain, u, v):
            # TODO: the list of elements of `domain` on which the dicts u and v agree
            _result = ...
            return _result

        direct = [(x, y) for x in X for y in Y if s[x] == t[y]]

        # print(len(product))                                    # expected: 35
        # print(len(equalizer(product, s_pr1, t_pr2)))           # expected: 11
        # print(equalizer(product, s_pr1, t_pr2) == direct)      # expected: True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | Meets are products — `exercises/5a/p01_meets_are_products.md` | warm-up | unpacking a universal property in a poset |
    | 2 | The inverse image is a pullback — `exercises/5a/p02_inverse_image_pullback.md` | warm-up | universal-property proof in $\mathbf{Set}$ |
    | 3 | A product of monics is monic — `exercises/5a/p03_product_of_monics.md` | core | comparing maps into a product through its projections |
    | 4 | Monic if and only if a square is a pullback — `exercises/5a/p04_monic_iff_pullback.md` | core | translating between two definitions |
    | 5 | The pullback pasting lemma — `exercises/5a/p05_pullback_pasting.md` | core | existence and uniqueness, twice |
    | 6 | Finite limits from pullbacks and a terminal object — `exercises/5a/p06_finite_limits_from_pullbacks.md` | stretch | building one universal property from another |

    Write each proof in `proofs/5a/` under the same filename as its brief, using the five-step proof anatomy of this lecture.
    Then ask Claude to review it: the review points at gaps and asks questions; it does not hand you a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [4C: Consequences of Yoneda](../4c_yoneda_consequences/) &nbsp;|&nbsp; Next: [5B: Colimits](../5b_colimits/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
