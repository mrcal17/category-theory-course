import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.function(hide_code=True)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6A: Limits via Representables & Adjoints

    > *Adjoints, representables and limits are three ways of saying one thing.*
    > — the theme of Leinster, Chapter 6

    You now own three large ideas. An **adjunction** (Part 2) is a natural bijection between two hom-sets. A **representable** (Part 4) is a set-valued functor that is secretly a hom-functor. A **limit** (Part 5) is a universal cone. Each was defined on its own terms, and each came with its own style of proof. This module shows that the third idea can be rewritten, word for word, in the language of each of the other two.

    The question this module answers is: *what kind of thing is the universal property of a limit?* There are two answers. First, a limit of a diagram $D$ is a **representation** of the functor that sends an object $A$ to the set of cones on $D$ with vertex $A$. Second, when every diagram of a given shape has a limit, "take the limit" is a functor, and it is **right adjoint** to the functor that sends an object to a constant diagram. A third result then drops out: every representable functor $\mathcal{A}(A, -)$ **preserves limits**.

    By the end you will be able to prove all three statements, and, more usefully, you will be able to move a problem about limits into whichever language makes it shortest. Nothing here is a new construction. The whole module is practice in one skill: **re-expressing one universal property as another**, and checking that nothing was lost in translation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Diagonal Functor, and Cones as Natural Transformations

    In 5A a diagram was a functor $D \colon \mathbf{I} \to \mathcal{A}$ from a small category $\mathbf{I}$, and a **cone** on $D$ was an object $A$ (the vertex) with a family of maps $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ such that $Du \circ f_I = f_J$ for every map $u \colon I \to J$ of $\mathbf{I}$. The family looks a lot like a natural transformation: one map for each object of $\mathbf{I}$, with a compatibility condition for each map of $\mathbf{I}$. It *is* one, as soon as you find the functor it starts from.

    > **Definition (diagonal functor).** Let $\mathbf{I}$ be a small category and $\mathcal{A}$ a category. For an object $A$ of $\mathcal{A}$, the **constant functor** $\Delta A \colon \mathbf{I} \to \mathcal{A}$ sends every object $I$ to $A$ and every map $u$ to $1_A$. For a map $g \colon A' \to A$ of $\mathcal{A}$, the natural transformation $\Delta g \colon \Delta A' \Rightarrow \Delta A$ has every component equal to $g$. This defines the **diagonal functor**
    > $$\Delta \colon \mathcal{A} \to [\mathbf{I}, \mathcal{A}].$$

    **Reading the definition.** To accept it you must check:

    - $\Delta A$ is a functor: it sends identities to $1_A$ and composites $v \circ u$ to $1_A = 1_A \circ 1_A$.
    - $\Delta g$ is natural: its naturality square at $u$ has $1_{A'}$ and $1_A$ on two sides and $g$ on the other two.
    - $\Delta$ respects identities and composition in $\mathcal{A}$.

    The first bullet is done in the line above; the other two are brief P01.

    **Examples.**

    - If $\mathbf{I}$ is the discrete category with two objects, then $[\mathbf{I}, \mathcal{A}]$ is $\mathcal{A} \times \mathcal{A}$ and $\Delta A = (A, A)$. This is where the name "diagonal" comes from.
    - If $\mathbf{I}$ is the empty category, then $[\mathbf{I}, \mathcal{A}]$ has exactly one object (the empty functor) and one map, and $\Delta$ is the unique functor $\mathcal{A} \to \mathbf{1}$.
    - If $\mathbf{I}$ is a group $G$ seen as a one-object category and $\mathcal{A} = \mathbf{Set}$, then $[G, \mathbf{Set}]$ is the category of $G$-sets and $\Delta A$ is the set $A$ with the action in which every group element does nothing.

    **Non-example.** Sending $A$ to the functor $I \mapsto A$, $u \mapsto e$ for some fixed non-identity endomorphism $e \colon A \to A$ is not allowed: a functor must send $1_I$ to $1_A$, and $e \neq 1_A$.

    Here is the lemma that turns cones into something Parts 1–4 already know how to handle.

    > **Lemma 1.** Let $D \colon \mathbf{I} \to \mathcal{A}$ be a diagram and $A$ an object of $\mathcal{A}$. A family $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ is a cone on $D$ if and only if it is a natural transformation $\Delta A \Rightarrow D$.

    - **Goal.** For every family $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$: the cone condition holds for all maps $u$ of $\mathbf{I}$ if and only if the naturality condition for a transformation $\Delta A \Rightarrow D$ holds for all maps $u$ of $\mathbf{I}$.
    - **Given.** The definition of a cone (5A), of a natural transformation (1D), and of $\Delta A$.
    - **Plan.** Direct: write out the naturality square at one map $u$ and simplify it using the definition of $\Delta A$.
    - **Proof.** Fix $u \colon I \to J$ in $\mathbf{I}$. A family $(f_I)$ is natural at $u$ exactly when $D(u) \circ f_I = f_J \circ (\Delta A)(u)$. By the definition of $\Delta A$, $(\Delta A)(u) = 1_A$, and by the identity axiom $f_J \circ 1_A = f_J$. So naturality at $u$ says $D(u) \circ f_I = f_J$, which is the cone condition at $u$. Since $u$ was arbitrary, the two conditions agree for all $u$. $\blacksquare$
    - **What made it work.** A triangle is a square with one side an identity. Whenever a compatible family of maps out of a single object appears, ask whether it is a natural transformation out of a constant functor.

    The picture below is the naturality square; its top edge is an identity, so it collapses to the cone triangle.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "A1": (0, 1.6, r"$A$"),
            "A2": (2.4, 1.6, r"$A$"),
            "DI": (0, 0, r"$D(I)$"),
            "DJ": (2.4, 0, r"$D(J)$"),
        },
        [
            ("A1", "A2", r"$(\Delta A)(u) = 1_A$"),
            ("A1", "DI", r"$f_I$", {"side": -1}),
            ("A2", "DJ", r"$f_J$"),
            ("DI", "DJ", r"$Du$", {"side": -1}),
        ],
        figsize=(5.2, 3.0),
        title="Naturality of a cone at u : I -> J",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lemma 1 lets you write the set of cones as a hom-set of a functor category:

    $$\mathrm{Cone}(A, D) \;=\; [\mathbf{I}, \mathcal{A}](\Delta A, D).$$

    **A word on size.** Throughout this module $\mathbf{I}$ is small and $\mathcal{A}$ is locally small. Then $\mathrm{Cone}(A, D)$ really is a set: a cone is an element of the product $\prod_{I \in \mathbf{I}} \mathcal{A}(A, D(I))$, which is a product of sets indexed by a set (3A).

    > Reference: [Leinster §6.1](https://arxiv.org/abs/1612.09375) (the diagonal functor and the description of cones); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf) for cones as natural transformations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. The Cone Functor

    A set that depends on an object $A$ is asking to be a functor of $A$. To make $\mathrm{Cone}(A, D)$ into one you need to say what a map $g \colon A' \to A$ does to cones. The only thing it can do is go in front: a cone out of $A$ becomes a cone out of $A'$ by first travelling along $g$. Because the vertex moves from $A$ back to $A'$, the functor is contravariant.

    > **Definition (cone functor).** Let $\mathcal{A}$ be locally small, $\mathbf{I}$ small and $D \colon \mathbf{I} \to \mathcal{A}$ a diagram. The **cone functor** is
    > $$\mathrm{Cone}(-, D) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set},$$
    > sending an object $A$ to the set $\mathrm{Cone}(A, D)$ of cones on $D$ with vertex $A$, and a map $g \colon A' \to A$ to the function
    > $$\mathrm{Cone}(g, D) \colon \mathrm{Cone}(A, D) \to \mathrm{Cone}(A', D), \qquad (f_I)_{I} \mapsto (f_I \circ g)_{I}.$$

    **Reading the definition.** Three things must be verified before this is a functor:

    - *Well defined:* $(f_I \circ g)_I$ is again a cone.
    - *Identities:* $\mathrm{Cone}(1_A, D)$ is the identity function.
    - *Composition, in the contravariant order:* $\mathrm{Cone}(g \circ g', D) = \mathrm{Cone}(g', D) \circ \mathrm{Cone}(g, D)$.

    > **Lemma 2.** $\mathrm{Cone}(-, D)$ is a functor $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$.

    - **Goal.** For all $g \colon A' \to A$ and $g' \colon A'' \to A'$ in $\mathcal{A}$ and every cone $(f_I)$ on $D$ with vertex $A$: (i) $(f_I g)_I$ is a cone with vertex $A'$; (ii) $(f_I 1_A)_I = (f_I)_I$; (iii) $(f_I (g g'))_I = ((f_I g) g')_I$.
    - **Given.** The cone condition $Du \circ f_I = f_J$ for all $u \colon I \to J$; the axioms of the category $\mathcal{A}$.
    - **Plan.** Direct verification of each clause, one axiom per clause.
    - **Proof.** (i) Let $u \colon I \to J$. Then $Du \circ (f_I \circ g) = (Du \circ f_I) \circ g$ by associativity, and this equals $f_J \circ g$ because $(f_I)$ is a cone. So $(f_I g)_I$ satisfies the cone condition at every $u$. (ii) $f_I \circ 1_A = f_I$ for each $I$ by the identity axiom, so the two families are equal. (iii) $f_I \circ (g \circ g') = (f_I \circ g) \circ g'$ for each $I$ by associativity; the left side is the $I$-component of $\mathrm{Cone}(g g', D)(f)$ and the right side is the $I$-component of $\mathrm{Cone}(g', D)\big(\mathrm{Cone}(g, D)(f)\big)$. $\blacksquare$
    - **What made it work.** "Compose in front" is the same operation that makes $H_A = \mathcal{A}(-, A)$ a functor in 4A, done one component at a time. Functoriality of a "precompose" rule is always associativity plus the identity axiom.

    **Examples of cone functors.**

    - *Two objects, no maps between them.* A diagram is a pair $(X, Y)$ and a cone with vertex $A$ is a pair of maps, so $\mathrm{Cone}(A, D) = \mathcal{A}(A, X) \times \mathcal{A}(A, Y)$.
    - *A parallel pair $s, t \colon X \rightrightarrows Y$.* A cone is determined by its component $f \colon A \to X$ (the other component is forced to be $s f$), and the condition is $s f = t f$. So $\mathrm{Cone}(A, D) \cong \{ f \in \mathcal{A}(A, X) : s f = t f \}$.
    - *In a poset.* There is at most one map between two objects, so $\mathrm{Cone}(a, D)$ has one element if $a \le D(I)$ for every $I$ (that is, $a$ is a lower bound of the diagram) and is empty otherwise.
    - *The empty diagram.* There are no components to choose and no conditions, so $\mathrm{Cone}(A, D)$ has exactly one element for every $A$.

    **Non-example.** In $\mathbf{Set}$ take the parallel pair $s = \mathrm{id}$ and $t = $ the swap on $\{0, 1\}$. The family with $f_X = \mathrm{id}$ and $f_Y = \mathrm{id}$ out of the vertex $\{0, 1\}$ is not a cone: $t \circ f_X$ is the swap, which is not $f_Y$. A family of maps to every object of the diagram is not yet a cone; the triangles must commute.

    The cell below lists $\mathrm{Cone}(a, D)$ in the poset of divisors of $12$ for the two-object diagram $\{4, 6\}$. Compare the last two columns.

    > Reference: [Leinster §6.1](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell
def _():
    def _run():
        _divs = [1, 2, 3, 4, 6, 12]
        _diagram = [4, 6]
        print("Divisors of 12 ordered by divisibility; diagram D = {4, 6} (no maps between them)")
        print(f"{'a':>3} | cone on D with vertex a? | a divides gcd(4, 6) = 2?")
        for _a in _divs:
            _cone = all(_d % _a == 0 for _d in _diagram)
            _maps_to_limit = 2 % _a == 0
            print(f"{_a:>3} | {str(_cone):<24} | {_maps_to_limit}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. A Limit Is a Representation of the Cone Functor

    The table above shows the two columns agreeing: there is a cone from $a$ exactly when there is a map from $a$ to the limit. That is the theorem of this section, and in a poset it is the whole theorem. In a general category "there is a cone" becomes "the *set* of cones", "there is a map" becomes "the *set* of maps", and "exactly when" becomes "in natural bijection".

    Two facts from Part 4 are needed.

    - (4A) A **representation** of a functor $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ is an object $L$ together with a natural isomorphism $\alpha \colon H_L \to X$, where $H_L = \mathcal{A}(-, L)$.
    - (4B, the Yoneda lemma) Every natural transformation $\alpha \colon H_L \to X$ is determined by the single element $u = \alpha_L(1_L) \in X(L)$, through the formula $\alpha_A(g) = (Xg)(u)$ for $g \colon A \to L$.

    > **Theorem 1 (limits are representations).** Let $\mathcal{A}$ be locally small, $\mathbf{I}$ small and $D \colon \mathbf{I} \to \mathcal{A}$ a diagram.
    >
    > **(a)** If $(p_I \colon L \to D(I))_{I}$ is a limit cone, then the functions
    > $$\alpha_A \colon \mathcal{A}(A, L) \to \mathrm{Cone}(A, D), \qquad g \mapsto (p_I \circ g)_{I}$$
    > are the components of a natural isomorphism $H_L \cong \mathrm{Cone}(-, D)$.
    >
    > **(b)** Conversely, if $\alpha \colon H_L \to \mathrm{Cone}(-, D)$ is a natural isomorphism, then the cone $p = \alpha_L(1_L)$ is a limit cone on $D$, and $\alpha_A(g) = (p_I \circ g)_I$ for every $g \colon A \to L$.

    **Proof of (a).**

    - **Goal.** (i) Each $\alpha_A$ is a well-defined function into $\mathrm{Cone}(A, D)$. (ii) For every $h \colon A' \to A$, the square $\mathrm{Cone}(h, D) \circ \alpha_A = \alpha_{A'} \circ H_L(h)$ commutes. (iii) Each $\alpha_A$ is a bijection.
    - **Given.** $(p_I)$ is a limit cone: for every object $A$ and every cone $(f_I)$ on $D$ with vertex $A$ there is a unique $g \colon A \to L$ with $p_I \circ g = f_I$ for all $I$.
    - **Plan.** (i) and (ii) are bookkeeping with Lemma 2. (iii) is the universal property read as two separate statements: "there is" gives surjectivity, "unique" gives injectivity.
    - **Proof.** (i) $\alpha_A(g) = \mathrm{Cone}(g, D)(p)$, which is a cone by Lemma 2(i). (ii) Take $g \in \mathcal{A}(A, L)$. Going one way, $\mathrm{Cone}(h, D)(\alpha_A(g)) = ((p_I g) h)_I$. Going the other way, $H_L(h)(g) = g h$ and $\alpha_{A'}(g h) = (p_I (g h))_I$. These agree by associativity. (iii) *Surjective:* given a cone $f \in \mathrm{Cone}(A, D)$, the universal property provides $g$ with $p_I g = f_I$ for all $I$, that is, $\alpha_A(g) = f$. *Injective:* if $\alpha_A(g) = \alpha_A(g') = f$, then $g$ and $g'$ are both maps with $p_I g = f_I = p_I g'$ for all $I$, so $g = g'$ by the uniqueness clause. A natural transformation whose components are all bijections is a natural isomorphism (1D). $\blacksquare$
    - **What made it work.** "There exists a unique $g$ such that ..." is the statement that a certain function is a bijection. Each time you meet a universal property, name that function.

    **Proof of (b).**

    - **Goal.** For every object $A$ and every cone $f$ on $D$ with vertex $A$, there is a unique $g \colon A \to L$ with $p_I \circ g = f_I$ for all $I$, where $p = \alpha_L(1_L)$.
    - **Given.** $\alpha$ is natural and every $\alpha_A$ is a bijection; the Yoneda lemma.
    - **Plan.** "Follow the identity": Yoneda says what $\alpha_A$ must be in terms of $p$; then bijectivity of $\alpha_A$ *is* the goal.
    - **Proof.** By the Yoneda lemma applied to $X = \mathrm{Cone}(-, D)$, for every $g \colon A \to L$ we have $\alpha_A(g) = \mathrm{Cone}(g, D)(p) = (p_I \circ g)_I$. Now fix a cone $f \in \mathrm{Cone}(A, D)$. Because $\alpha_A$ is surjective there is a $g$ with $\alpha_A(g) = f$, which says $p_I g = f_I$ for all $I$. Because $\alpha_A$ is injective that $g$ is the only one. $\blacksquare$
    - **What made it work.** A representation always comes with a distinguished element, the image of the identity (4C called it the universal element). For the cone functor that element *is* the limit cone.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "A": (1.3, 3.0, r"$A$"),
            "L": (1.3, 1.5, r"$L$"),
            "DI": (0, 0, r"$D(I)$"),
            "DJ": (2.6, 0, r"$D(J)$"),
        },
        [
            ("A", "L", r"$\exists!\, g$", {"dashed": True, "color": "#b91c1c"}),
            ("L", "DI", r"$p_I$", {"side": -1}),
            ("L", "DJ", r"$p_J$"),
            ("A", "DI", r"$f_I$", {"rad": 0.35}),
            ("A", "DJ", r"$f_J$", {"rad": -0.35}),
            ("DI", "DJ", r"$Du$", {"side": -1}),
        ],
        figsize=(5.4, 4.4),
        title="Cones from A  <->  maps A -> L",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Putting Lemma 1 and Theorem 1 together gives the formula to remember:

    $$\boxed{\;\mathcal{A}(A, \lim D) \;\cong\; \mathrm{Cone}(A, D) \;=\; [\mathbf{I}, \mathcal{A}](\Delta A, D) \quad \text{naturally in } A\;}$$

    **What you gain.**

    - *Uniqueness for free.* 4C proved that a representation of a functor is unique up to a unique isomorphism compatible with the universal elements. Applied to $\mathrm{Cone}(-, D)$, that is the statement from 5A that limit cones are unique up to unique isomorphism. You do not need a second proof.
    - *A test for "is this a limit?"* To show $L$ with a cone $p$ is a limit, show that $g \mapsto (p_I g)_I$ is a bijection for each $A$. In $\mathbf{Set}$, and in any finite category, that is a counting problem, which is the widget below.

    **Non-example.** In the poset of divisors of $12$ the object $1$ has a cone to the diagram $\{4, 6\}$, but $H_1$ is not a representation of $\mathrm{Cone}(-, D)$: at $a = 2$ the set $\mathrm{Cone}(2, D)$ has one element while there is no map $2 \to 1$. Having *a* cone is far weaker than representing *all* cones.

    > Reference: [Leinster §6.1](https://arxiv.org/abs/1612.09375); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf) takes this statement as the definition of a limit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Counting Cones

    In $\mathbf{Set}$ with finite sets, Theorem 1 predicts a number. If $L$ is the limit of $D$ and $A$ has $n$ elements, there are $|L|^n$ functions $A \to L$, so there must be exactly $|L|^n$ cones on $D$ with vertex $A$.

    The widget checks this honestly. It builds $L$ by the explicit formula of 5A (compatible families of elements), and separately enumerates every family of functions $(f_I \colon A \to D(I))$ and keeps those for which all the triangles commute. The sets are $X = \{0,1,2\}$, $Y = \{0,1\}$, $Z = \{0,1\}$.
    """)
    return


@app.cell
def _(mo):
    cone_shape = mo.ui.dropdown(
        options=["product: X, Y", "equalizer: s, t : X -> Y", "pullback: X -> Z <- Y"],
        value="product: X, Y",
        label="Diagram",
    )
    cone_n = mo.ui.slider(start=0, stop=3, step=1, value=2, label="Number of elements of the test set A")
    mo.vstack([cone_shape, cone_n])
    return cone_n, cone_shape


@app.cell
def _(cone_n, cone_shape, mo):
    def _run():
        import itertools

        _n = cone_n.value
        if cone_shape.value.startswith("product"):
            _sets = {"X": [0, 1, 2], "Y": [0, 1]}
            _maps = {}
        elif cone_shape.value.startswith("equalizer"):
            _sets = {"X": [0, 1, 2], "Y": [0, 1]}
            _maps = {"s": ("X", "Y", {0: 0, 1: 1, 2: 0}), "t": ("X", "Y", {0: 0, 1: 0, 2: 0})}
        else:
            _sets = {"X": [0, 1, 2], "Y": [0, 1], "Z": [0, 1]}
            _maps = {"s": ("X", "Z", {0: 0, 1: 1, 2: 1}), "t": ("Y", "Z", {0: 0, 1: 1})}
        _names = list(_sets)
        _idx = {_k: _i for _i, _k in enumerate(_names)}

        # The limit, by the explicit formula of 5A: compatible families of elements.
        _limit = [
            _fam for _fam in itertools.product(*[_sets[_k] for _k in _names])
            if all(_m[_fam[_idx[_s]]] == _fam[_idx[_d]] for (_s, _d, _m) in _maps.values())
        ]

        # Cones with vertex A = {0, ..., n-1}, by brute force over families of functions.
        _funcs = {_k: list(itertools.product(_sets[_k], repeat=_n)) for _k in _names}
        _families = 0
        _cones = 0
        for _fam in itertools.product(*[_funcs[_k] for _k in _names]):
            _families += 1
            if all(
                all(_m[_fam[_idx[_s]][_a]] == _fam[_idx[_d]][_a] for _a in range(_n))
                for (_s, _d, _m) in _maps.values()
            ):
                _cones += 1

        _lines = [
            "| Quantity | Value |",
            "|---|---|",
            f"| families of functions $(f_I \\colon A \\to D(I))$ tried | {_families} |",
            f"| of those, cones on $D$ with vertex $A$ | **{_cones}** |",
            f"| elements of the limit $L$ | {len(_limit)} |",
            f"| functions $A \\to L$, that is $\\lvert L \\rvert^{{{_n}}}$ | **{len(_limit) ** _n}** |",
            "",
            "The two bold numbers agree: " + ("yes" if _cones == len(_limit) ** _n else "NO"),
        ]
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try $n = 0$: there is exactly one cone from the empty set, whatever the diagram, and exactly one function $\emptyset \to L$. Try $n = 1$: a cone from a one-element set is a compatible family of *elements*, which is how 5A described the elements of a limit in $\mathbf{Set}$. That special case is Theorem 1 with $A = 1$.

    A count is not a proof. Equal cardinalities show that *some* bijection exists for each $A$; Theorem 1 says a specific one, $g \mapsto (p_I g)_I$, is a bijection, and that it is natural in $A$. Mistake 1 at the end of the module is about exactly this gap.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Taking Limits Is a Functor

    So far the diagram $D$ has been fixed. Now let it vary. If $\alpha \colon D \Rightarrow D'$ is a map of diagrams (a natural transformation), is there an induced map $\lim D \to \lim D'$? For products you know the answer: maps $\alpha_1 \colon X \to X'$ and $\alpha_2 \colon Y \to Y'$ induce $\alpha_1 \times \alpha_2 \colon X \times Y \to X' \times Y'$. The general case is the same argument.

    > **Definition.** A category $\mathcal{A}$ **has limits of shape $\mathbf{I}$** if every diagram $D \colon \mathbf{I} \to \mathcal{A}$ has a limit. In that case, *choose* for each $D$ a limit cone
    > $$\big(p^D_I \colon \lim D \to D(I)\big)_{I \in \mathbf{I}}.$$
    > For a natural transformation $\alpha \colon D \Rightarrow D'$, define $\lim \alpha \colon \lim D \to \lim D'$ to be the unique map such that
    > $$p^{D'}_I \circ \lim \alpha \;=\; \alpha_I \circ p^D_I \qquad \text{for all } I \in \mathbf{I}. \tag{$\ast$}$$

    **Reading the definition.**

    - A choice is being made. Limits are unique only up to isomorphism, so "$\lim D$" names the chosen one.
    - "The unique map such that" is only meaningful if the family $(\alpha_I \circ p^D_I)_I$ is a cone on $D'$ with vertex $\lim D$. That needs checking.
    - Then $\lim$ must be shown to respect identities and composition.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "L": (0, 1.6, r"$\lim\, D$"),
            "L2": (2.8, 1.6, r"$\lim\, D'$"),
            "DI": (0, 0, r"$D(I)$"),
            "DI2": (2.8, 0, r"$D'(I)$"),
        },
        [
            ("L", "L2", r"$\lim\, \alpha$", {"dashed": True, "color": "#b91c1c"}),
            ("L", "DI", r"$p^{D}_I$", {"side": -1}),
            ("L2", "DI2", r"$p^{D'}_I$"),
            ("DI", "DI2", r"$\alpha_I$", {"side": -1}),
        ],
        figsize=(5.4, 3.0),
        title="The defining square of lim(alpha), one for each I",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Lemma 3.** If $\mathcal{A}$ has limits of shape $\mathbf{I}$, then (for any choice of limit cones) $\lim \colon [\mathbf{I}, \mathcal{A}] \to \mathcal{A}$ is a functor.

    - **Goal.** (i) For every $\alpha \colon D \Rightarrow D'$, the family $(\alpha_I p^D_I)_I$ is a cone on $D'$, so $\lim \alpha$ exists and is unique. (ii) $\lim 1_D = 1_{\lim D}$. (iii) $\lim(\beta \circ \alpha) = \lim \beta \circ \lim \alpha$ for all $\alpha \colon D \Rightarrow D'$ and $\beta \colon D' \Rightarrow D''$.
    - **Given.** The chosen limit cones and their universal properties; Lemma 1.
    - **Plan.** (i) by Lemma 1. (ii) and (iii) are uniqueness arguments: exhibit a map satisfying the defining equation $(\ast)$ of the thing you want, then quote uniqueness.
    - **Proof.** (i) By Lemma 1 the cone $p^D$ is a natural transformation $\Delta(\lim D) \Rightarrow D$. The composite $\alpha \circ p^D \colon \Delta(\lim D) \Rightarrow D'$ is a natural transformation because vertical composites of natural transformations are natural (1D). Its components are $\alpha_I p^D_I$, so by Lemma 1 again they form a cone on $D'$ with vertex $\lim D$. The universal property of $p^{D'}$ gives a unique map satisfying $(\ast)$.

      (ii) The defining equation of $\lim 1_D$ is $p^D_I \circ m = 1_{D(I)} \circ p^D_I$ for all $I$. The map $m = 1_{\lim D}$ satisfies it, by the identity axioms. By uniqueness, $\lim 1_D = 1_{\lim D}$.

      (iii) The defining equation of $\lim (\beta\alpha)$ is $p^{D''}_I \circ m = \beta_I \alpha_I p^D_I$ for all $I$. Test $m = \lim \beta \circ \lim \alpha$:
      $$p^{D''}_I \circ \lim\beta \circ \lim\alpha = \beta_I \circ p^{D'}_I \circ \lim\alpha = \beta_I \circ \alpha_I \circ p^D_I,$$
      using $(\ast)$ for $\beta$ and then $(\ast)$ for $\alpha$. So $\lim\beta \circ \lim\alpha$ satisfies the defining equation, and by uniqueness it equals $\lim(\beta\alpha)$. $\blacksquare$
    - **What made it work.** A map defined by a universal property is pinned down by its composites with the projections. To prove two such maps equal, never chase elements: compose with every $p_I$ and compare.

    **Examples.**

    - *Products.* For the two-object discrete shape, $\lim$ is the functor $\times \colon \mathcal{A} \times \mathcal{A} \to \mathcal{A}$ and $\lim(\alpha_1, \alpha_2) = \alpha_1 \times \alpha_2$.
    - *Posets.* A natural transformation between diagrams in a poset is just the statement $D(I) \le D'(I)$ for all $I$. Lemma 3 says: if $x_i \le x'_i$ for all $i$ then $\bigwedge x_i \le \bigwedge x'_i$. Meets are monotone.

    **Non-example.** The category of fields has no product of $\mathbb{F}_2$ and $\mathbb{F}_3$: a field mapping to both would have characteristic $2$ and characteristic $3$ at once. So there is no functor $\lim$ of this shape on fields, and nothing in this section applies there.

    > Reference: [Leinster §6.1](https://arxiv.org/abs/1612.09375); [Riehl §3.4](https://math.jhu.edu/~eriehl/context.pdf) (functoriality of limits).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Limits Are Right Adjoint to the Diagonal

    Look again at the boxed formula of Section 3, now with $\lim$ a functor:

    $$\mathcal{A}(A, \lim D) \;\cong\; [\mathbf{I}, \mathcal{A}](\Delta A, D).$$

    On the right is a hom-set of $[\mathbf{I}, \mathcal{A}]$ with $\Delta$ applied in the first slot. On the left is a hom-set of $\mathcal{A}$ with $\lim$ applied in the second slot. That is the shape of an adjunction $F \dashv G$ from 2A, $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$, with $F = \Delta$ and $G = \lim$. The only thing missing is naturality in $D$.

    > **Theorem 2 (limits as an adjoint).** Let $\mathbf{I}$ be a small category and $\mathcal{A}$ a locally small category with limits of shape $\mathbf{I}$. Then the functor $\lim \colon [\mathbf{I}, \mathcal{A}] \to \mathcal{A}$ of Lemma 3 is right adjoint to the diagonal functor:
    > $$\Delta \dashv \lim, \qquad [\mathbf{I}, \mathcal{A}](\Delta A, D) \;\cong\; \mathcal{A}(A, \lim D) \quad\text{naturally in } A \in \mathcal{A} \text{ and } D \in [\mathbf{I}, \mathcal{A}].$$

    - **Goal.** Produce, for all $A$ and $D$, a bijection $\varphi_{A, D} \colon \mathcal{A}(A, \lim D) \to [\mathbf{I}, \mathcal{A}](\Delta A, D)$ such that (i) for every $h \colon A' \to A$ and $g \colon A \to \lim D$, $\varphi_{A', D}(g \circ h) = \varphi_{A, D}(g) \circ \Delta h$; and (ii) for every $\alpha \colon D \Rightarrow D'$ and $g \colon A \to \lim D$, $\varphi_{A, D'}(\lim \alpha \circ g) = \alpha \circ \varphi_{A, D}(g)$.
    - **Given.** Theorem 1(a) for each $D$; the defining equation $(\ast)$ of $\lim \alpha$; Lemma 1.
    - **Plan.** Take $\varphi_{A,D}(g) = (p^D_I \circ g)_I$. Bijectivity and naturality in $A$ are Theorem 1(a). Naturality in $D$ is one line from $(\ast)$.
    - **Proof.** Define $\varphi_{A,D}(g) = (p^D_I g)_I$, regarded by Lemma 1 as a natural transformation $\Delta A \Rightarrow D$. It is a bijection by Theorem 1(a)(iii).

      (i) The $I$-component of $\varphi_{A',D}(g h)$ is $p^D_I g h$. The $I$-component of $\varphi_{A,D}(g) \circ \Delta h$ is $(p^D_I g) \circ h$, since every component of $\Delta h$ is $h$. These agree by associativity.

      (ii) The $I$-component of $\varphi_{A,D'}(\lim\alpha \circ g)$ is $p^{D'}_I \circ \lim \alpha \circ g$, which by $(\ast)$ equals $\alpha_I \circ p^D_I \circ g$. That is the $I$-component of $\alpha \circ \varphi_{A,D}(g)$. $\blacksquare$
    - **What made it work.** The definition of $\lim$ on maps, equation $(\ast)$, *is* naturality in $D$. When a functor is defined on maps by a universal property, the defining equation usually turns out to be the naturality you need later.

    **Unit and counit.** Following the identity as in 2B: the counit $\varepsilon_D \colon \Delta(\lim D) \Rightarrow D$ is $\varphi(1_{\lim D}) = (p^D_I)_I$. *The counit of $\Delta \dashv \lim$ is the limit cone.* The unit $\eta_A \colon A \to \lim \Delta A$ is the map induced by the cone whose every component is $1_A$.

    **The dual.** Running everything in $\mathcal{A}^{\mathrm{op}}$: if $\mathcal{A}$ has colimits of shape $\mathbf{I}$ then $\mathrm{colim} \colon [\mathbf{I}, \mathcal{A}] \to \mathcal{A}$ is *left* adjoint to $\Delta$, with $\mathcal{A}(\mathrm{colim}\, D, A) \cong [\mathbf{I}, \mathcal{A}](D, \Delta A)$. When both exist,

    $$\mathrm{colim} \;\dashv\; \Delta \;\dashv\; \lim.$$

    **Examples.**

    - *Two-object discrete shape.* $\Delta \colon \mathcal{A} \to \mathcal{A} \times \mathcal{A}$ has right adjoint $\times$ and left adjoint $+$: maps *into* a product are pairs of maps, $\mathcal{A}(A, X \times Y) \cong \mathcal{A}(A, X) \times \mathcal{A}(A, Y)$, and maps *out of* a sum are pairs of maps.
    - *Empty shape.* $\Delta \colon \mathcal{A} \to \mathbf{1}$; a right adjoint picks out a terminal object and a left adjoint an initial object, as in 2A.
    - *Posets.* In a poset with binary meets, $a \le x \wedge y$ if and only if ($a \le x$ and $a \le y$). That one line is $\Delta \dashv \wedge$.

    **Which way round?** If you forget which side $\lim$ is on, test with products: a cone goes *into* the diagram, and $\lim$ sits in the *second* slot of the hom-set, which is where right adjoints sit.

    > Reference: [Leinster §6.1](https://arxiv.org/abs/1612.09375); [Riehl §4.5](https://math.jhu.edu/~eriehl/context.pdf) for the same adjunction seen from the adjoint side.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Representables Preserve Limits

    Recall from 5C: a functor $F \colon \mathcal{A} \to \mathcal{B}$ **preserves limits** if whenever $(p_I \colon L \to D(I))_I$ is a limit cone on a diagram $D$ in $\mathcal{A}$, the cone $(F p_I \colon F(L) \to F D(I))_I$ is a limit cone on $F \circ D$ in $\mathcal{B}$.

    The most important functors out of a locally small category are the representables $H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$. Do they preserve limits? For a product the answer is the definition of a product: a map $A \to X \times Y$ is a pair of maps. The general statement has the same flavour.

    > **Theorem 3.** Let $\mathcal{A}$ be a locally small category and $A$ an object. Then $\mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$ preserves limits.

    Write $E = \mathcal{A}(A, D(-)) \colon \mathbf{I} \to \mathbf{Set}$ for the composite diagram, so $E(I) = \mathcal{A}(A, D(I))$ and $E(u) = Du \circ -$.

    - **Goal.** Given a limit cone $(p_I \colon L \to D(I))_I$ in $\mathcal{A}$: for every set $S$ and every cone $(q_I \colon S \to \mathcal{A}(A, D(I)))_I$ on $E$ in $\mathbf{Set}$, there is a unique function $h \colon S \to \mathcal{A}(A, L)$ with $(p_I \circ -) \circ h = q_I$ for all $I$.
    - **Given.** The universal property of $(p_I)$ in $\mathcal{A}$. That functors send cones to cones, so $(p_I \circ -)_I$ is a cone on $E$ (5C).
    - **Plan.** Work one element $s \in S$ at a time. Each $s$ gives a cone on $D$ in $\mathcal{A}$ with vertex $A$; the universal property of $L$ turns that cone into a map $A \to L$, which is the value $h(s)$.
    - **Proof.** *One element gives one cone.* Fix $s \in S$ and put $f_I = q_I(s) \in \mathcal{A}(A, D(I))$. For $u \colon I \to J$ in $\mathbf{I}$, the cone condition on $(q_I)$ in $\mathbf{Set}$ says $E(u) \circ q_I = q_J$; evaluating at $s$ gives $Du \circ f_I = f_J$. So $(f_I)_I$ is a cone on $D$ with vertex $A$.

      *Existence.* By the universal property of $(p_I)$ there is a unique map $A \to L$, call it $h(s)$, with $p_I \circ h(s) = q_I(s)$ for all $I$. Doing this for each $s$ defines a function $h \colon S \to \mathcal{A}(A, L)$, and the equation $p_I \circ h(s) = q_I(s)$ for all $s$ says $(p_I \circ -) \circ h = q_I$.

      *Uniqueness.* Let $h' \colon S \to \mathcal{A}(A, L)$ also satisfy $(p_I \circ -) \circ h' = q_I$ for all $I$. Then for each $s$, the map $h'(s) \colon A \to L$ satisfies $p_I \circ h'(s) = q_I(s)$ for all $I$. By the uniqueness clause of the universal property of $(p_I)$, $h'(s) = h(s)$. Two functions that agree at every $s$ are equal (0B). $\blacksquare$
    - **What made it work.** A cone in $\mathbf{Set}$ over hom-sets is a family of cones in $\mathcal{A}$, one per element. Universal properties in $\mathbf{Set}$ that involve hom-sets can be checked pointwise in $S$.

    The statement is often written as an isomorphism, with the understanding that the right-hand limit is taken in $\mathbf{Set}$:

    $$\boxed{\;\mathcal{A}(A, \lim_I D(I)) \;\cong\; \lim_I \mathcal{A}(A, D(I))\;}$$

    Compare with the explicit formula of 5A: the limit in $\mathbf{Set}$ of the sets $\mathcal{A}(A, D(I))$ is the set of compatible families $(f_I)$ with $Du \circ f_I = f_J$, which is $\mathrm{Cone}(A, D)$. So Theorem 3 and Theorem 1 are the same fact, viewed from $\mathbf{Set}$ and from $\mathcal{A}$.

    **Examples.**

    - $\mathbf{Set}(A, X \times Y) \cong \mathbf{Set}(A, X) \times \mathbf{Set}(A, Y)$; for finite sets this is the law of exponents $(xy)^a = x^a y^a$.
    - Any representable functor preserves limits. The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ is isomorphic to $\mathbf{Grp}(\mathbb{Z}, -)$ (4A), and a functor naturally isomorphic to a limit-preserving one preserves limits. So the underlying set of a product of groups is the product of the underlying sets, and similarly for equalizers and pullbacks.
    - In a poset, $\mathcal{A}(a, -)$ takes the value "one point" or "empty", and Theorem 3 says: $a \le \bigwedge x_i$ if and only if $a \le x_i$ for all $i$.

    **Non-example: colimits are not preserved.** $\mathbf{Set}(2, -)$ does not preserve sums. $\mathbf{Set}(2, 1 + 1)$ has $2^2 = 4$ elements, while $\mathbf{Set}(2, 1) + \mathbf{Set}(2, 1)$ has $1 + 1 = 2$. The cell below counts a few more cases.

    **The contravariant version.** $\mathcal{A}(-, A)$ is a functor on $\mathcal{A}^{\mathrm{op}}$, and limits in $\mathcal{A}^{\mathrm{op}}$ are colimits in $\mathcal{A}$. So the dual statement is that $\mathcal{A}(-, A)$ turns *colimits* in $\mathcal{A}$ into limits in $\mathbf{Set}$: $\mathcal{A}(\mathrm{colim}\, D, A) \cong \lim \mathcal{A}(D(-), A)$. Making this precise is brief P04.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375) (representables preserve limits); [Riehl §3.4](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell
def _():
    def _run():
        print("Counting functions between finite sets: |Set(A, B)| = |B| ** |A|")
        print()
        print(f"{'|A|':>4} {'|X|':>4} {'|Y|':>4} | {'Set(A, X x Y)':>14} {'Set(A,X) x Set(A,Y)':>20} | {'Set(A, X + Y)':>14} {'Set(A,X) + Set(A,Y)':>20}")
        for _a, _x, _y in [(1, 2, 3), (2, 1, 1), (2, 2, 3), (3, 2, 2)]:
            _into_product = (_x * _y) ** _a
            _product_of_homs = (_x ** _a) * (_y ** _a)
            _into_sum = (_x + _y) ** _a
            _sum_of_homs = (_x ** _a) + (_y ** _a)
            print(f"{_a:>4} {_x:>4} {_y:>4} | {_into_product:>14} {_product_of_homs:>20} | {_into_sum:>14} {_sum_of_homs:>20}")
        print()
        print("Product columns always agree (Theorem 3). In this table the sum columns agree only in the row with |A| = 1.")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **A bijection for each $A$, with no naturality.** Showing that $\mathcal{A}(A, L)$ and $\mathrm{Cone}(A, D)$ have the same number of elements for every $A$ does not make $L$ a limit. *Diagnosis:* a representation is a *natural* isomorphism; without naturality you cannot apply Yoneda to recover the limit cone.
    2. **Treating the limit as an object.** Writing "$L$ is the limit" and never mentioning the projections. *Diagnosis:* the universal element $p = \alpha_L(1_L)$ is part of the data; two different cones on the same vertex can have different universal properties, and only one of them need be a limit cone.
    3. **Using $\lim \alpha$ before it exists.** Invoking the universal property of $\lim D'$ on the family $(\alpha_I p^D_I)$ without first proving that the family is a cone. *Diagnosis:* the universal property takes cones as input, not arbitrary families; Lemma 3(i) is not optional.
    4. **Putting the adjoint on the wrong side.** Writing $\lim \dashv \Delta$. *Diagnosis:* in $F \dashv G$ the left adjoint appears in the first slot of a hom-set. Maps into a limit are cones, so $\lim$ is in the second slot: $\Delta \dashv \lim$ and $\mathrm{colim} \dashv \Delta$.
    5. **Proving preservation by an abstract isomorphism.** Showing $F(\lim D) \cong \lim (F D)$ by some isomorphism and stopping. *Diagnosis:* preservation says the specific cone $(F p_I)$ is a limit cone. An isomorphism of vertices that is not compatible with the projections proves nothing about that cone.

    ---

    ## Why This Matters

    - **6B** proves that limits of presheaves are computed pointwise and that the Yoneda embedding preserves limits. The first is built from universal properties in the target category, in the style of Lemma 3; the second reduces, one object at a time, to Theorem 3.
    - **6C** proves that right adjoints preserve limits. The short proof is a chain of natural isomorphisms that ends at $\mathrm{Cone}(A, G \circ D)$, and Theorem 1(b) is what converts that chain into a statement about a limit cone.
    - **6C** also needs Theorem 2 read backwards: the adjoint functor theorems build an adjoint out of limits, which is only thinkable once you know that limits and adjoints are the same kind of object.
    - **5C** stated that limits commute with limits. With Theorem 2 in hand, one reason is structural: $\lim$ is a right adjoint, and 6C shows right adjoints preserve limits.
    - **7A** records the three boxed formulas of this module as the standard dictionary between the three languages.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Each cell runs as shipped. Replace the `...` placeholders, then uncomment the `print` checks and compare with the expected values.

    ### Exercise 1: Cones, and the limit test of Theorem 1

    The category below has objects `E`, `X`, `Y` and non-identity arrows `e : E -> X`, `f, g : X -> Y`, `k : E -> Y` with `f∘e = g∘e = k`. The diagram is the parallel pair `f, g`.

    Fill in (a) the cone condition in `cones`, and (b) the test in `is_limit_cone`: by Theorem 1, a cone `p` with vertex `L` is a limit cone exactly when, for every object `A`, the function $g \mapsto (p_I \circ g)_I$ from arrows `A -> L` to cones with vertex `A` is a bijection.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        _objects = ["E", "X", "Y"]
        _arrows = {
            "1E": ("E", "E"), "1X": ("X", "X"), "1Y": ("Y", "Y"),
            "e": ("E", "X"), "f": ("X", "Y"), "g": ("X", "Y"), "k": ("E", "Y"),
        }
        _identity = {"E": "1E", "X": "1X", "Y": "1Y"}
        _compose = {("f", "e"): "k", ("g", "e"): "k"}
        for _name, (_dom, _cod) in _arrows.items():
            _compose[(_name, _identity[_dom])] = _name
            _compose[(_identity[_cod], _name)] = _name
        cat = {"objects": _objects, "arrows": _arrows, "identity": _identity, "compose": _compose}

        shape = {"objects": ["X", "Y"], "arrows": {"f": ("X", "Y"), "g": ("X", "Y")}}
        D = {"objects": {"X": "X", "Y": "Y"}, "arrows": {"f": "f", "g": "g"}}

        def hom(cat, A, B):
            return [name for name, (dom, cod) in cat["arrows"].items() if dom == A and cod == B]

        def cones(cat, shape, D, A):
            """All cones on D with vertex A, each as a dict {I: arrow A -> D(I)}."""
            choices = [hom(cat, A, D["objects"][I]) for I in shape["objects"]]
            found = []
            for choice in itertools.product(*choices):
                fam = dict(zip(shape["objects"], choice))
                # TODO (a): fam is a cone when, for every shape arrow u : I -> J,
                #           D(u) composed after fam[I] equals fam[J].
                is_cone = ...
                if is_cone is True:
                    found.append(fam)
            return found

        def is_limit_cone(cat, shape, D, L, p):
            for A in cat["objects"]:
                # TODO (b): send each arrow g : A -> L to the cone (p_I ∘ g)_I and
                #           decide whether this assignment is a bijection onto cones(cat, shape, D, A).
                bijection = ...
                if bijection is not True:
                    return False
            return True

        # print([len(cones(cat, shape, D, A)) for A in ["E", "X", "Y"]])       # expect [1, 0, 0]
        # print(is_limit_cone(cat, shape, D, "E", {"X": "e", "Y": "k"}))        # expect True
        # print(cones(cat, shape, D, "E"))                                      # expect [{'X': 'e', 'Y': 'k'}]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: The meet is right adjoint to the diagonal

    In the poset of divisors of $12$ under divisibility, compute the meet of two elements *from the definition* (the greatest lower bound, found by search, with no use of `math.gcd`), and then check the adjunction $\Delta \dashv \wedge$ of Section 6 on every triple $(a, x, y)$.
    """)
    return


@app.cell
def _():
    def _run():
        elems = [1, 2, 3, 4, 6, 12]

        def leq(a, b):
            return b % a == 0

        def meet(x, y):
            lower = [a for a in elems if leq(a, x) and leq(a, y)]
            # TODO: return the element of `lower` that every element of `lower` is <= to.
            return ...

        def adjunction_holds():
            # TODO: for all a, x, y in elems compare  leq(a, meet(x, y))  with  (leq(a, x) and leq(a, y)).
            return ...

        # print(meet(4, 6), meet(4, 12), meet(3, 4))   # expect 2 4 1
        # print(adjunction_holds())                    # expect True
        # print(sum(1 for a in elems for x in elems for y in elems if leq(a, meet(x, y))))   # expect 70

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: $\lim$ on a map of diagrams

    Two pullback-shaped diagrams of finite sets, `D1` and `D2`, and a natural transformation `alpha` between them are given. `limit` computes the limit by the formula of 5A, as a list of compatible triples $(x, y, z)$. Implement `lim_on_arrows`, the function $\lim \alpha \colon \lim D_1 \to \lim D_2$ determined by equation $(\ast)$ of Section 5, and confirm that every value lands in $\lim D_2$.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        D1 = {
            "sets": {"X": [0, 1, 2], "Y": [0, 1], "Z": [0, 1]},
            "maps": {"s": ("X", "Z", {0: 0, 1: 1, 2: 1}), "t": ("Y", "Z", {0: 0, 1: 1})},
        }
        D2 = {
            "sets": {"X": ["a", "b"], "Y": ["c", "d"], "Z": ["z"]},
            "maps": {"s": ("X", "Z", {"a": "z", "b": "z"}), "t": ("Y", "Z", {"c": "z", "d": "z"})},
        }
        alpha = {"X": {0: "a", 1: "b", 2: "b"}, "Y": {0: "c", 1: "d"}, "Z": {0: "z", 1: "z"}}
        names = ["X", "Y", "Z"]

        def limit(D):
            pos = {k: i for i, k in enumerate(names)}
            return [
                fam for fam in itertools.product(*[D["sets"][k] for k in names])
                if all(m[fam[pos[src]]] == fam[pos[dst]] for (src, dst, m) in D["maps"].values())
            ]

        def lim_on_arrows(alpha, L1):
            """Return a dict sending each element of lim D1 to an element of lim D2."""
            result = {}
            for fam in L1:
                # TODO: the projections of the image are alpha applied to the projections of fam.
                result[fam] = ...
            return result

        L1, L2 = limit(D1), limit(D2)
        lim_alpha = lim_on_arrows(alpha, L1)
        # print(len(L1), len(L2))                          # expect 3 4
        # print([lim_alpha[fam] for fam in L1])            # expect [('a', 'c', 'z'), ('b', 'd', 'z'), ('b', 'd', 'z')]
        # print(all(lim_alpha[fam] in L2 for fam in L1))   # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | `exercises/6a/p01_diagonal_is_a_functor.md` | warm-up | verifying functoriality |
    | 2 | `exercises/6a/p02_colimit_represents_cocones.md` | warm-up | dualizing a proof |
    | 3 | `exercises/6a/p03_right_adjoint_to_diagonal_gives_limits.md` | core | re-expressing a universal property |
    | 4 | `exercises/6a/p04_hom_turns_colimits_into_limits.md` | core | pointwise argument in $\mathbf{Set}$ |
    | 5 | `exercises/6a/p05_representables_detect_limits.md` | core | testing a universal property against all representables |
    | 6 | `exercises/6a/p06_constant_diagrams_on_connected_shapes.md` | stretch | induction along a zigzag |

    Write each proof in `proofs/6a/<same filename>`, using the Goal / Given / Plan / Proof / What made it work layout.
    Then ask Claude to review it; the review points at gaps and asks questions, it does not rewrite your proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [5C: Functors & Limits](../5c_functors_and_limits/) | Next: [6B: Limits & Colimits of Presheaves](../6b_presheaf_limits/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
