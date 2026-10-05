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
    # 5B: Colimits

    > *A limit is carved out of a product by equations. A colimit is glued together from a sum by identifications.*
    > — the theme of this module

    Every definition in 5A was a statement about arrows, so every definition has a mirror image obtained by reversing all the arrows. The mirror image of a limit is a **colimit**. The mirror images of products, equalizers and pullbacks are **sums** (coproducts), **coequalizers** and **pushouts**.

    Formally nothing new happens: a colimit in $\mathcal{A}$ is a limit in $\mathcal{A}^{\mathrm{op}}$, and by the principle of duality (1B) each theorem of 5A gives a theorem here with no further proof. Concretely a great deal changes. Limits in $\mathbf{Set}$ were *subsets of products*: tuples satisfying equations. Colimits in $\mathbf{Set}$ are *quotients of disjoint unions*: elements glued together along an equivalence relation. So the question of this module is: *what does a universal property look like when the universal object receives maps instead of emitting them, and how do you prove one when the object is a quotient?*

    By the end you will be able to: dualize a definition and a proof correctly; prove that a disjoint union is a sum and that a quotient set is a coequalizer, including the well-definedness check that quotients always demand; state and use the explicit formula for any colimit in $\mathbf{Set}$; and recognise sums, coequalizers and pushouts in $\mathbf{Ab}$, $\mathbf{Grp}$, $\mathbf{Top}$ and posets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Cocones, Colimits and Duality

    In 5A a cone was an object mapping *into* every object of a diagram. Reverse the arrows: a cocone is an object that every object of the diagram maps *into*.

    > **Definition (cocone, colimit).** Let $\mathbf{I}$ be a small category and $D \colon \mathbf{I} \to \mathcal{A}$ a diagram.
    >
    > A **cocone on $D$** consists of an object $A$ of $\mathcal{A}$ (the **vertex**) and a family of maps $\big(f_I \colon D(I) \to A\big)_{I \in \mathbf{I}}$ such that for every arrow $u \colon I \to J$ in $\mathbf{I}$
    > $$f_J \circ D(u) = f_I .$$
    >
    > A **colimit of $D$** is a cocone $\big(q_I \colon D(I) \to C\big)_{I \in \mathbf{I}}$ with the following property: for every cocone $\big(f_I \colon D(I) \to A\big)_{I \in \mathbf{I}}$ on $D$ there exists a unique map $\bar{f} \colon C \to A$ such that
    > $$\bar{f} \circ q_I = f_I \quad\text{for all } I \in \mathbf{I} .$$
    > The maps $q_I$ are the **coprojections**, and we write $C = \operatorname{colim} D$.

    **Reading the definition.** To show that $(C, (q_I))$ is a colimit of $D$:

    - **It is a cocone.** One leg $q_I$ *into* $C$ for each object $I$, and one equation $q_J \circ D(u) = q_I$ for each arrow $u \colon I \to J$. Note which side the diagram map is on: it is composed *before* the leg.
    - **Fix an arbitrary cocone** $(A, (f_I))$; its equations $f_J D(u) = f_I$ are your hypotheses.
    - **Existence.** Produce $\bar{f} \colon C \to A$, a map *out of* $C$, and verify $\bar{f} q_I = f_I$ for every $I$.
    - **Uniqueness.** Any $g \colon C \to A$ with $g q_I = f_I$ for all $I$ equals $\bar{f}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "DI": (-1.6, 2.6, r"$D(I)$"), "DJ": (1.6, 2.6, r"$D(J)$"),
            "C": (0, 1.3, r"$C$"), "A": (0, 0, r"$A$"),
        },
        [
            ("DI", "DJ", r"$D(u)$"),
            ("DI", "C", r"$q_I$"),
            ("DJ", "C", r"$q_J$", {"side": -1}),
            ("C", "A", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
            ("DI", "A", r"$f_I$", {"rad": 0.3}),
            ("DJ", "A", r"$f_J$", {"rad": -0.3}),
        ],
        figsize=(6.0, 4.0),
        title="A colimit cocone (q_I) and the mediating map to a cocone (f_I)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Colimits are limits in the opposite category.** A diagram $D \colon \mathbf{I} \to \mathcal{A}$ gives a diagram $D^{\mathrm{op}} \colon \mathbf{I}^{\mathrm{op}} \to \mathcal{A}^{\mathrm{op}}$ with the same effect on objects and arrows. Let us check that a cocone on $D$ is the same thing as a cone on $D^{\mathrm{op}}$. A map $f_I \colon D(I) \to A$ in $\mathcal{A}$ is a map $A \to D(I)$ in $\mathcal{A}^{\mathrm{op}}$: a leg of a cone. An arrow $u \colon I \to J$ of $\mathbf{I}$ is an arrow $J \to I$ of $\mathbf{I}^{\mathrm{op}}$, and the cone equation for it reads "$D^{\mathrm{op}}(u)$ after $f_J$ equals $f_I$", the composite being taken in $\mathcal{A}^{\mathrm{op}}$. Composition in $\mathcal{A}^{\mathrm{op}}$ is composition in $\mathcal{A}$ in the other order, so in $\mathcal{A}$ this is $f_J \circ D(u) = f_I$: the cocone equation. In the same way a mediating map $A \to C$ in $\mathcal{A}^{\mathrm{op}}$ is a map $C \to A$ in $\mathcal{A}$. Hence:

    $$\boxed{\;\text{a colimit of } D \text{ in } \mathcal{A} \;=\; \text{a limit of } D^{\mathrm{op}} \text{ in } \mathcal{A}^{\mathrm{op}}\;}$$

    | In 5A | Dual notion here |
    |---|---|
    | cone, limit, projection $p_I \colon L \to D(I)$ | cocone, colimit, coprojection $q_I \colon D(I) \to C$ |
    | mediating map *into* the limit | mediating map *out of* the colimit |
    | terminal object $1$ | initial object $0$ |
    | product $X \times Y$ | sum (coproduct) $X + Y$ |
    | equalizer | coequalizer |
    | pullback | pushout |
    | monic | epic |

    Because every theorem of 5A holds in every category, each holds in $\mathcal{A}^{\mathrm{op}}$; translating back gives a theorem about colimits in $\mathcal{A}$. In particular, with no further proof:

    - **Uniqueness.** If $(q_I \colon D(I) \to C)$ and $(q'_I \colon D(I) \to C')$ are colimit cocones on $D$, there is a unique map $j \colon C \to C'$ with $j q_I = q'_I$ for all $I$, and $j$ is an isomorphism. A cocone isomorphic to a colimit cocone is a colimit cocone.
    - **Construction.** A category with all small sums and all coequalizers has all small colimits.

    Dualizing is a skill, and it is worth doing once by hand. The next proof does it both ways.

    ### Proof 1: maps out of a colimit are determined by their composites with the coprojections

    - **Goal.** Let $(q_I \colon D(I) \to C)_{I \in \mathbf{I}}$ be a colimit cocone on $D \colon \mathbf{I} \to \mathcal{A}$. For every object $A$ and all maps $h, h' \colon C \to A$: if $h \circ q_I = h' \circ q_I$ for all $I$, then $h = h'$.
    - **Given.** The Lemma of 5A §5 (Proof 4), which holds in every category: if $(p_I \colon L \to E(I))$ is a limit cone on a diagram $E$ and $k, k' \colon A \to L$ satisfy $p_I k = p_I k'$ for all $I$, then $k = k'$.
    - **Plan.** Dualize: apply the Lemma in $\mathcal{A}^{\mathrm{op}}$ and translate. Then, to see that nothing mysterious happened, repeat the argument directly.
    - **Proof.** *By duality.* In $\mathcal{A}^{\mathrm{op}}$, $(q_I)$ is a limit cone on $D^{\mathrm{op}}$ with vertex $C$, and $h, h'$ are maps $A \to C$. The hypothesis $h q_I = h' q_I$ in $\mathcal{A}$ says that in $\mathcal{A}^{\mathrm{op}}$ the composites "$q_I$ after $h$" and "$q_I$ after $h'$" agree for all $I$. By the Lemma applied in the category $\mathcal{A}^{\mathrm{op}}$, $h = h'$.

        *Directly.* Put $f_I = h \circ q_I \colon D(I) \to A$. This is a cocone: for $u \colon I \to J$, $f_J \circ D(u) = h \circ q_J \circ D(u) = h \circ q_I = f_I$, since $(q_I)$ is a cocone. Both $h$ and $h'$ satisfy $(-) \circ q_I = f_I$ for all $I$: the first by definition, the second by hypothesis. By the uniqueness clause of the colimit, $h = h'$. $\qquad\blacksquare$
    - **What made it work.** The direct proof is the proof from 5A with every composite written in the opposite order. To prove two maps *out of* a colimit equal, compose each with every coprojection.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf). Duality: [Leinster §1.1](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Sums

    The dual of a product is a sum, also called a coproduct. A map *out of* a sum $X + Y$ is the same thing as one map out of $X$ and one map out of $Y$: a definition by cases.

    > **Definition (sum).** Let $X, Y$ be objects of a category $\mathcal{A}$. A **sum** (or **coproduct**) of $X$ and $Y$ consists of an object $S$ and maps
    > $$X \xrightarrow{\;i_1\;} S \xleftarrow{\;i_2\;} Y$$
    > such that for every object $A$ and every pair of maps $f_1 \colon X \to A$, $f_2 \colon Y \to A$ there exists a unique map $\bar{f} \colon S \to A$ with $\bar{f} \circ i_1 = f_1$ and $\bar{f} \circ i_2 = f_2$. We write $S = X + Y$. The sum $\sum_{i \in I} X_i$ of a family is defined in the same way, with one coprojection $i_k \colon X_k \to S$ for each index $k$.

    **Reading the definition.** The data are an object and *two maps into it*. Test data are two maps *out of* $X$ and $Y$ to a common object $A$. Existence: produce $\bar{f} \colon S \to A$ and check two equations. Uniqueness: any $g \colon S \to A$ with $g i_1 = f_1$, $g i_2 = f_2$ equals $\bar{f}$.

    A sum of the empty family is an object $S$ such that every object $A$ receives exactly one map $S \to A$: an **initial object** $0$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"X": (-0.4, 2.3, r"$X$"), "Y": (2.8, 2.3, r"$Y$"), "S": (1.2, 1.3, r"$X + Y$"), "A": (1.2, 0, r"$A$")},
        [
            ("X", "S", r"$i_1$"),
            ("Y", "S", r"$i_2$", {"side": -1}),
            ("S", "A", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
            ("X", "A", r"$f_1$", {"rad": 0.25}),
            ("Y", "A", r"$f_2$", {"rad": -0.25}),
        ],
        figsize=(5.2, 3.6),
        title="A sum: every pair (f1, f2) factors uniquely through X + Y",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proof 2: the disjoint union is a sum in $\mathbf{Set}$

    For sets $X$ and $Y$ recall from 3A the **disjoint union**
    $$X + Y = (X \times \{1\}) \cup (Y \times \{2\}), \qquad i_1(x) = (x, 1), \quad i_2(y) = (y, 2).$$
    The tags $1$ and $2$ make the two pieces disjoint even when $X$ and $Y$ overlap. In 3A·P03 you proved that for every set $A$ the function
    $$\Theta \colon \mathbf{Set}(X + Y, A) \to \mathbf{Set}(X, A) \times \mathbf{Set}(Y, A), \qquad \Theta(h) = (h \circ i_1,\ h \circ i_2),$$
    is a bijection. We do not repeat that proof. What we do here is translate it into the language of this module, because the translation is a pattern you will meet again.

    - **Goal.** For every set $A$ and all functions $f_1 \colon X \to A$, $f_2 \colon Y \to A$ there exists a unique function $\bar{f} \colon X + Y \to A$ with $\bar{f} \circ i_1 = f_1$ and $\bar{f} \circ i_2 = f_2$.
    - **Given.** For every set $A$, the function $\Theta$ above is a bijection (3A·P03).
    - **Plan.** Read "surjective" as existence and "injective" as uniqueness.
    - **Proof.** Fix $A$, $f_1$, $f_2$. The pair $(f_1, f_2)$ is an element of the codomain of $\Theta$.

        *Existence.* Since $\Theta$ is surjective there is a function $\bar{f} \colon X + Y \to A$ with $\Theta(\bar{f}) = (f_1, f_2)$. By the definition of $\Theta$ this says $\bar{f} i_1 = f_1$ and $\bar{f} i_2 = f_2$.

        *Uniqueness.* Let $g \colon X + Y \to A$ satisfy $g i_1 = f_1$ and $g i_2 = f_2$. Then $\Theta(g) = (f_1, f_2) = \Theta(\bar{f})$. Since $\Theta$ is injective, $g = \bar{f}$. $\qquad\blacksquare$
    - **What made it work.** "For every test datum there exists a unique mediating map" says exactly that a certain function, from mediating maps to test data, is a bijection. Module 6A turns this observation into a description of limits and colimits by representability.

    Looking back at your proof of 3A·P03, notice which property of $X + Y$ each half used: defining a function by cases needs the two pieces to be *disjoint*, and its uniqueness needs them to *cover* $X + Y$. In a colimit, uniqueness of the mediating map always comes from the coprojections jointly covering the object.

    **More examples.**

    - **$\mathbf{Top}$.** The disjoint union of the underlying sets, where a subset is open exactly when its intersections with both pieces are open.
    - **A poset.** A sum of $x$ and $y$ is a least upper bound, a **join** $x \vee y$. In the natural numbers ordered by divisibility it is the least common multiple. (This is the dual of 5A·P01.)
    - **$\mathbf{Ab}$ and $\mathbf{Vect}_k$.** The direct sum $G \oplus H$, whose underlying set is the *product* $G \times H$, with $i_1(g) = (g, 0)$ and $i_2(h) = (0, h)$. See Proof 3.
    - **$\mathbf{Grp}$.** The **free product** $G * H$, whose elements are the words alternating between non-identity elements of $G$ and non-identity elements of $H$, multiplied by concatenating and then reducing. It is much bigger than $G \times H$: the sum $\mathbb{Z} + \mathbb{Z}$ in $\mathbf{Grp}$ is the free group on two generators, which is not abelian.
    - **Initial objects.** $\varnothing$ in $\mathbf{Set}$ and in $\mathbf{Top}$; the one-element group in $\mathbf{Grp}$ and $\mathbf{Ab}$; the zero space in $\mathbf{Vect}_k$; a least element in a poset.

    **Non-examples.**

    - *The plain union is not a sum.* In $\mathbf{Set}$ take $X = Y = \{0\}$, so $X \cup Y = \{0\}$ with both "inclusions" the identity. For $A = \{a, b\}$, $f_1(0) = a$, $f_2(0) = b$, a mediating map $g$ would need $g(0) = a$ and $g(0) = b$. Existence fails.
    - *The direct product is not a sum in $\mathbf{Grp}$.* Let $G = H = \mathbb{Z}/2$ and try $S = G \times H$ with $i_1(g) = (g, 0)$, $i_2(h) = (0, h)$. Let $A = S_3$ and let $f_1, f_2 \colon \mathbb{Z}/2 \to S_3$ send $1$ to the transpositions $(1\,2)$ and $(1\,3)$. If a homomorphism $k \colon G \times H \to S_3$ had $k i_1 = f_1$ and $k i_2 = f_2$, then since $(1, 0) + (0, 1) = (0, 1) + (1, 0)$ in $G \times H$ we would get $(1\,2)(1\,3) = (1\,3)(1\,2)$ in $S_3$. But those two products are the two different 3-cycles. Existence fails.

    The last non-example shows that the *same* object with the *same* maps can be a sum in one category and not in another. In $\mathbf{Ab}$ it is one:

    ### Proof 3: in $\mathbf{Ab}$, the direct sum is a sum

    Let $G, H$ be abelian groups written additively, $G \oplus H$ the set $G \times H$ with coordinatewise addition, $i_1(g) = (g, 0)$, $i_2(h) = (0, h)$. Both $i_1$ and $i_2$ are homomorphisms.

    - **Goal.** For every abelian group $A$ and all homomorphisms $f_1 \colon G \to A$, $f_2 \colon H \to A$ there exists a unique homomorphism $\bar{f} \colon G \oplus H \to A$ with $\bar{f} i_1 = f_1$ and $\bar{f} i_2 = f_2$.
    - **Given.** $f_1, f_2$ are homomorphisms; addition in $A$ is commutative and associative.
    - **Plan.** Universal-property proof. Uniqueness will tell us what the formula for $\bar{f}$ must be, so we do it first; then we check that the forced formula really is a homomorphism.
    - **Proof.** *Uniqueness.* Let $k \colon G \oplus H \to A$ be a homomorphism with $k i_1 = f_1$ and $k i_2 = f_2$. Every element satisfies $(g, h) = (g, 0) + (0, h) = i_1(g) + i_2(h)$. Since $k$ is a homomorphism, $k(g, h) = k(i_1(g)) + k(i_2(h)) = f_1(g) + f_2(h)$. So $k$ is determined: there is at most one such homomorphism.

        *Existence.* Define $\bar{f}(g, h) = f_1(g) + f_2(h)$. It is a homomorphism:
        $$\bar{f}\big((g, h) + (g', h')\big) = f_1(g + g') + f_2(h + h') = f_1(g) + f_1(g') + f_2(h) + f_2(h') = \big(f_1(g) + f_2(h)\big) + \big(f_1(g') + f_2(h')\big),$$
        where the second equality uses that $f_1, f_2$ are homomorphisms and the third **rearranges the middle two terms, using commutativity of $A$**. The right-hand side is $\bar{f}(g, h) + \bar{f}(g', h')$. Finally $\bar{f}(i_1(g)) = f_1(g) + f_2(0) = f_1(g)$ and $\bar{f}(i_2(h)) = f_1(0) + f_2(h) = f_2(h)$, because homomorphisms send $0$ to $0$. $\qquad\blacksquare$
    - **What made it work.** Every element of $G \oplus H$ is a sum of an element from each coprojection, which forces the formula; commutativity of the *target* makes the formula a homomorphism. In $\mathbf{Grp}$ the target need not be commutative, and that is exactly where the non-example above broke.

    Since $G \times H$ is also the product of $G$ and $H$ in $\mathbf{Ab}$, binary sums and binary products in $\mathbf{Ab}$ have the same underlying object. This fails for infinite families: the sum $\bigoplus_i G_i$ consists of the families with only finitely many non-zero entries, a proper subgroup of the product $\prod_i G_i$ when infinitely many $G_i$ are non-zero.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375) (sums); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Coequalizers and Quotients

    An equalizer of $s, t \colon X \to Y$ is the best map *into* $X$ that makes $s$ and $t$ agree. A coequalizer is the best map *out of* $Y$ that makes them agree: it forces $s(x)$ and $t(x)$ to become equal for every $x$, and identifies nothing more than it has to.

    > **Definition (coequalizer).** Let $s, t \colon X \to Y$ be maps in a category $\mathcal{A}$. A **coequalizer** of $s$ and $t$ is a map $q \colon Y \to C$ such that $q \circ s = q \circ t$, with the following property: for every object $A$ and every map $f \colon Y \to A$ with $f \circ s = f \circ t$ there exists a unique map $\bar{f} \colon C \to A$ such that $\bar{f} \circ q = f$.

    **Reading the definition.** (1) Check $q s = q t$. (2) Fix an arbitrary $f \colon Y \to A$ with $f s = f t$. (3) Existence: produce $\bar{f} \colon C \to A$ with $\bar{f} q = f$. (4) Uniqueness: any $g \colon C \to A$ with $g q = f$ equals $\bar{f}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"X": (0, 1.5, r"$X$"), "Y": (1.9, 1.5, r"$Y$"), "C": (3.6, 1.5, r"$C$"), "A": (3.6, 0, r"$A$")},
        [
            ("X", "Y", r"$s$", {"rad": -0.25}),
            ("X", "Y", r"$t$", {"rad": 0.25}),
            ("Y", "C", r"$q$"),
            ("Y", "A", r"$f$", {"side": -1}),
            ("C", "A", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
        ],
        figsize=(6.2, 2.8),
        title="A coequalizer: every f with fs = ft factors uniquely through q",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In $\mathbf{Set}$, "forcing $s(x) = t(x)$" means passing to a quotient of $Y$. The relation $\{(s(x), t(x)) : x \in X\}$ is usually not an equivalence relation, so we need the smallest equivalence relation containing it.

    > **Definition (generated equivalence relation; recalled from 3A).** Let $S$ be a set and $R \subseteq S \times S$ any relation on $S$. The **equivalence relation generated by $R$** is the smallest equivalence relation $\sim$ on $S$ containing $R$: it is an equivalence relation, it contains $R$, and every equivalence relation on $S$ that contains $R$ also contains $\sim$. (It exists: it is the intersection of all equivalence relations on $S$ containing $R$.)

    **Reading the definition.** The definition tells you how to *use* $\sim$ but not what it looks like. Both are worth having.

    - *How to use it.* To prove that $a \sim b$ implies some property $\Phi(a, b)$, show that "$\Phi(a, b)$" is an equivalence relation containing $R$. Minimality of $\sim$ does the rest.
    - *What it looks like.* $a \sim b$ if and only if there is a **zigzag** from $a$ to $b$: a list $c_0, c_1, \dots, c_n$ in $S$ with $n \ge 0$, $c_0 = a$, $c_n = b$, and for each $k < n$ either $(c_k, c_{k+1}) \in R$ or $(c_{k+1}, c_k) \in R$.

    The zigzag description is justified as follows. Write $a \approx b$ when a zigzag from $a$ to $b$ exists. Then $\approx$ is reflexive (take $n = 0$), symmetric (reverse the list; each step is allowed in either direction) and transitive (put two zigzags end to end), and it contains $R$ (a pair in $R$ is a zigzag with $n = 1$). So $\approx$ is an equivalence relation containing $R$, and therefore contains $\sim$. Conversely each step of a zigzag is a pair related by $\sim$ (because $\sim$ contains $R$ and is symmetric), so its two ends are related by $\sim$ (because $\sim$ is reflexive and transitive). Hence the two relations are equal.

    We write $S/{\sim}$ for the set of equivalence classes, $[a]$ for the class of $a$, and $\pi \colon S \to S/{\sim}$, $\pi(a) = [a]$, for the quotient map. Every proof about colimits in $\mathbf{Set}$ rests on the next lemma. It sharpens the universal property of a quotient set that you proved in 3A·P04: there the hypothesis was about all pairs related by $\sim$; here it is only about the generating pairs.

    ### Proof 4 (Lemma): maps out of a quotient by a generated relation

    - **Goal.** Let $\sim$ be the equivalence relation on $S$ generated by $R$. For every set $B$ and every function $g \colon S \to B$ such that $g(a) = g(b)$ for all $(a, b) \in R$, there exists a unique function $\bar{g} \colon S/{\sim} \to B$ with $\bar{g} \circ \pi = g$.
    - **Given.** $\sim$ is the smallest equivalence relation containing $R$. The universal property of the quotient set (3A §5, your 3A·P04): if $g(a) = g(b)$ whenever $a \sim b$, then there is exactly one $\bar{g}$ with $\bar{g} \circ \pi = g$.
    - **Plan.** Upgrade the hypothesis from pairs in $R$ to pairs related by $\sim$, using the "how to use it" recipe. Then quote 3A.
    - **Proof.** Define a relation on $S$ by: $a \equiv b$ if and only if $g(a) = g(b)$. It is reflexive, symmetric and transitive, because equality in $B$ is. It contains $R$, by the hypothesis on $g$. So $\equiv$ is an equivalence relation containing $R$, and since $\sim$ is the smallest such, $a \sim b$ implies $a \equiv b$, that is, $g(a) = g(b)$.

        Now $g$ satisfies the hypothesis of the universal property of the quotient set, which gives both the existence and the uniqueness of $\bar{g}$ with $\bar{g} \circ \pi = g$. $\qquad\blacksquare$
    - **What made it work.** The relation "$g$ cannot tell $a$ and $b$ apart" is an equivalence relation for any function $g$. So to check that $g$ is constant on the classes of a *generated* relation it is enough to check the generators, and we never needed to know what the classes look like. Remember from 3A·P04 what the quoted property hides: $\bar{g}([a]) = g(a)$ is defined on a representative, and independence of the representative is the whole issue.

    **Coequalizers in $\mathbf{Set}$.** Let $s, t \colon X \to Y$ be functions, let $\sim$ be the equivalence relation on $Y$ generated by $R = \{(s(x), t(x)) : x \in X\}$, and let $q = \pi \colon Y \to Y/{\sim}$. Then $q$ is a coequalizer of $s$ and $t$. Indeed $q(s(x)) = [s(x)] = [t(x)] = q(t(x))$ because $\sim$ contains $R$. And a function $f \colon Y \to A$ satisfies $f s = f t$ exactly when $f(a) = f(b)$ for all $(a, b) \in R$; for such $f$, the Lemma gives a unique $\bar{f}$ with $\bar{f} q = f$, which is both halves of the universal property.

    **Examples.**

    - **$\mathbf{Set}$.** Let $X = Y = \mathbb{Z}$, $s = 1_{\mathbb{Z}}$ and $t(x) = x + n$ for a fixed $n \ge 1$. The generating pairs are $(x, x + n)$; a zigzag changes an integer by $\pm n$ at each step; so $a \sim b$ exactly when $n$ divides $a - b$. The coequalizer is the set of residue classes modulo $n$.
    - **$\mathbf{Ab}$, $\mathbf{Vect}_k$.** The coequalizer of homomorphisms $s, t \colon G \to H$ is the quotient $H \to H / \operatorname{im}(s - t)$. With $t = 0$ this is the **cokernel** $H / \operatorname{im}(s)$, dual to the kernel in 5A. You verify this in `p02_cokernel_coequalizer.md`.
    - **$\mathbf{Grp}$.** The quotient $H \to H/N$, where $N$ is the smallest normal subgroup of $H$ containing all the elements $s(x)\, t(x)^{-1}$.
    - **$\mathbf{Top}$.** The quotient set of $\mathbf{Set}$ with the quotient topology. Let $X$ be a one-point space, $Y = [0, 1]$, and let $s, t$ pick out $0$ and $1$. The coequalizer glues the two endpoints of the interval together and is homeomorphic to a circle.

    **Non-examples.** In $\mathbf{Set}$ let $X = \{\ast\}$, $Y = \{0, 1, 2\}$, $s(\ast) = 0$, $t(\ast) = 1$. The coequalizer is $Y \to \{\{0, 1\}, \{2\}\}$.

    - The identity $1_Y$ is not a coequalizer; it is not even a map with $q s = q t$.
    - The map $q' \colon Y \to \{\ast\}$ satisfies $q' s = q' t$ but is not a coequalizer: the function $f \colon Y \to \{a, b\}$ with $f(0) = f(1) = a$ and $f(2) = b$ satisfies $f s = f t$ and does not factor through $q'$. It identifies *too much*, and existence fails.
    - The map $q'' \colon Y \to \{u, v, w\}$ with $q''(0) = q''(1) = u$, $q''(2) = v$ satisfies $q'' s = q'' t$ but is not a coequalizer: a mediating map may send $w$ anywhere, so uniqueness fails. It is not surjective. In fact every coequalizer is epic: this is the dual of the corresponding fact about equalizers in 5A §2, or Proof 1 of this module read for a parallel pair.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375) (coequalizers, generated equivalence relations); quotient sets: [Leinster §3.1](https://arxiv.org/abs/1612.09375); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Pushouts

    The dual of a pullback glues two objects together along a common part.

    > **Definition (pushout).** Let $s \colon Z \to X$ and $t \colon Z \to Y$ be maps in a category $\mathcal{A}$ with the same domain. A **pushout** of $(s, t)$ consists of an object $Q$ and maps $j_1 \colon X \to Q$, $j_2 \colon Y \to Q$ such that
    > $$j_1 \circ s = j_2 \circ t,$$
    > with the following property: for every object $A$ and every pair of maps $f_1 \colon X \to A$, $f_2 \colon Y \to A$ satisfying $f_1 \circ s = f_2 \circ t$, there exists a unique map $\bar{f} \colon Q \to A$ such that $\bar{f} \circ j_1 = f_1$ and $\bar{f} \circ j_2 = f_2$.

    **Reading the definition.** (1) The square commutes. (2) Fix arbitrary $f_1, f_2$ with $f_1 s = f_2 t$. (3) Existence of $\bar{f} \colon Q \to A$ with two equations. (4) Uniqueness.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "Z": (0, 2.7, r"$Z$"), "Y": (1.8, 2.7, r"$Y$"),
            "X": (0, 1.2, r"$X$"), "Q": (1.8, 1.2, r"$Q$"), "A": (3.1, 0, r"$A$"),
        },
        [
            ("Z", "Y", r"$t$", {"side": -1}),
            ("Z", "X", r"$s$", {"side": -1}),
            ("X", "Q", r"$j_1$", {"side": -1}),
            ("Y", "Q", r"$j_2$"),
            ("Q", "A", r"$\bar{f}$", {"dashed": True, "color": "#b91c1c"}),
            ("X", "A", r"$f_1$", {"rad": 0.3}),
            ("Y", "A", r"$f_2$", {"rad": -0.3}),
        ],
        figsize=(5.0, 4.4),
        title="A pushout square and its universal property",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - **$\mathbf{Set}$.** $Q = (X + Y)/{\sim}$, where $\sim$ is generated by $(s(z), 1) \sim (t(z), 2)$ for $z \in Z$, and $j_1(x) = [(x, 1)]$, $j_2(y) = [(y, 2)]$. This agrees with the formula of Section 5 up to a bijection compatible with the coprojections (there the elements of $Z$ are also present in the disjoint union, but each is glued to its image in $X$). In words: take a copy of $X$ and a copy of $Y$ and glue $s(z)$ to $t(z)$ for every $z$.
    - **Unions.** If $A, B$ are subsets of a set, then $A \cup B$ is a pushout of the inclusions $A \hookleftarrow A \cap B \hookrightarrow B$. You prove this in `p01_union_is_pushout.md`.
    - **A poset.** For $z \le x$ and $z \le y$, the square commutes automatically and a pushout is a join $x \vee y$.
    - **$\mathbf{Top}$.** The same set as in $\mathbf{Set}$ with the quotient topology of the disjoint union. Gluing two closed discs along their boundary circles gives a sphere.
    - **$\mathbf{Grp}$.** The pushout is called an *amalgamated free product*: the free product $G * H$ modulo the smallest normal subgroup that identifies the image of $s(z)$ with the image of $t(z)$ for each $z$.
    - **$Z$ initial.** If $Z = 0$ is an initial object, a pushout of $X \leftarrow 0 \to Y$ is a sum $X + Y$. This is the dual of Proof 3 of 5A, so it needs no new argument: apply that proof in $\mathcal{A}^{\mathrm{op}}$, where $0$ is terminal.

    **Non-example, and a warning about zigzags.** In $\mathbf{Set}$ let $Z = \{a, b\}$, $X = \{0, 1\}$ with $s(a) = 0$, $s(b) = 1$, and $Y = \{\ast\}$. The generating identifications are $0 \sim \ast$ and $1 \sim \ast$. No generator relates $0$ to $1$ directly, but the zigzag $0, \ast, 1$ does: the pushout has one element. The set $X$ with $j_1 = 1_X$ and $j_2(\ast) = 0$ is *not* a pushout: its square does not commute, since $j_1(s(b)) = 1 \ne 0 = j_2(t(b))$. Gluing can collapse elements of $X$ that no single identification mentions.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375) (pushouts); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Colimits in $\mathbf{Set}$: the Explicit Formula

    The limit of a diagram of sets was a subset of the product. Dually, the colimit is a quotient of the sum. The statement needs care, because the relation we quotient by has to be *generated*.

    > **Theorem (colimits in $\mathbf{Set}$).** Let $\mathbf{I}$ be a small category and $D \colon \mathbf{I} \to \mathbf{Set}$ a diagram. Let
    > $$S = \sum_{I \in \mathbf{I}} D(I) = \{(I, x) : I \text{ an object of } \mathbf{I},\ x \in D(I)\}$$
    > be the disjoint union of the sets of the diagram. Let $\sim$ be the equivalence relation on $S$ **generated by** the relation
    > $$R = \big\{ \big((I, x),\ (J, (Du)(x))\big) \;:\; u \colon I \to J \text{ an arrow of } \mathbf{I},\ x \in D(I) \big\}.$$
    > Put
    > $$\boxed{\;\operatorname{colim} D = S/{\sim}, \qquad q_I \colon D(I) \to S/{\sim}, \quad q_I(x) = [(I, x)]\;}$$
    > Then $(q_I \colon D(I) \to S/{\sim})_{I \in \mathbf{I}}$ is a colimit cocone on $D$.

    **Reading the formula.**

    - Elements of the colimit are *classes* of tagged elements $(I, x)$. Every element of every set of the diagram contributes.
    - The generating identifications are: each element is glued to its image under each map of the diagram.
    - Two tagged elements $(I, x)$ and $(J, y)$ give the same element of the colimit if and only if they are joined by a **zigzag**: a finite list of tagged elements starting at $(I, x)$ and ending at $(J, y)$ in which each consecutive pair is $(K, w)$ and $(K', (Dv)(w))$ for some arrow $v \colon K \to K'$, in one order or the other.
    - It is **not** true in general that $(I, x) \sim (J, y)$ only when some map of the diagram sends one to the other. The warning example of Section 4 shows two elements of the same set $X$ becoming equal.

    As in 5A, if the arrows of $\mathbf{I}$ are composites of a few generating arrows, the pairs coming from the generating arrows already generate $\sim$: a pair coming from a composite $v u$ is joined by the two-step zigzag $(I, x)$, $(J, (Du)(x))$, $(K, (Dv)((Du)(x)))$, and a pair coming from an identity is of the form $(a, a)$.

    ### Proof 5: the formula gives a colimit

    - **Goal.** $(q_I)$ is a cocone on $D$; and for every set $B$ and every cocone $(g_I \colon D(I) \to B)_{I \in \mathbf{I}}$ there exists a unique function $\bar{g} \colon S/{\sim} \to B$ with $\bar{g} \circ q_I = g_I$ for all $I$.
    - **Given.** The Lemma on maps out of a quotient (Proof 4); the fact that every element of $S$ is $(I, x)$ for exactly one object $I$ and one $x \in D(I)$.
    - **Plan.** Assemble the legs $g_I$ into one function $g \colon S \to B$ (the sum), check that $g$ respects the generating relation $R$ (this is where the cocone equations are used), and apply the Lemma (the quotient). Two stages in each half, dual to Proof 8 of 5A.
    - **Proof.** *Cocone.* Let $u \colon I \to J$ and $x \in D(I)$. Then $q_J((Du)(x)) = [(J, (Du)(x))] = [(I, x)] = q_I(x)$, the middle equality because the two tagged elements form a pair in $R$ and $\sim$ contains $R$. So $q_J \circ D(u) = q_I$.

        *Existence.* Let $(g_I)$ be a cocone with vertex $B$. Define $g \colon S \to B$ by $g(I, x) = g_I(x)$; this is a function because each element of $S$ has exactly one tag. It respects $R$: for a generating pair,
        $$g\big(J, (Du)(x)\big) = g_J\big((Du)(x)\big) = g_I(x) = g(I, x),$$
        the middle equality being the cocone equation $g_J \circ D(u) = g_I$. By the Lemma there is a function $\bar{g} \colon S/{\sim} \to B$ with $\bar{g} \circ \pi = g$. Then for every $I$ and $x \in D(I)$, $\bar{g}(q_I(x)) = \bar{g}(\pi(I, x)) = g(I, x) = g_I(x)$. So $\bar{g} q_I = g_I$.

        *Uniqueness.* Let $h \colon S/{\sim} \to B$ satisfy $h q_I = g_I$ for all $I$. Then for every $(I, x) \in S$, $h(\pi(I, x)) = h(q_I(x)) = g_I(x) = g(I, x)$, so $h \pi = g$. By the uniqueness clause of the Lemma, $h = \bar{g}$. $\qquad\blacksquare$
    - **What made it work.** A cocone is a family of maps out of the pieces (handled by the sum) that agree along the diagram (handled by the quotient). The cocone equations are exactly the statement that $g$ respects the generating pairs.

    **Examples of the formula.**

    - *Two objects, no arrows:* $R$ is empty, $\sim$ is equality, and the colimit is the disjoint union.
    - *Parallel pair $s, t \colon X \to Y$:* every $(X, x)$ is glued to $(Y, s(x))$, so every class contains an element of $Y$; and $(Y, s(x)) \sim (Y, t(x))$. The classes correspond to the classes of $Y$ under the relation of Section 3.
    - *A chain of inclusions* $X_0 \subseteq X_1 \subseteq X_2 \subseteq \cdots$, with shape the poset $0 \le 1 \le 2 \le \cdots$: $(m, x) \sim (n, y)$ exactly when $x = y$, and the colimit is in bijection with the union $\bigcup_n X_n$.
    - *A group action.* For a group $G$ acting on a set $X$, viewed as a functor $G \to \mathbf{Set}$: the generating pairs are $(x, g \cdot x)$ and the colimit is the set of **orbits**. Compare with 5A, where the limit of the same diagram was the set of fixed points.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375) (colimits in $\mathbf{Set}$); [Riehl §3.1](https://math.jhu.edu/~eriehl/context.pdf) and [§3.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Interactive: colimit calculator

    Choose a diagram and two parameters. The calculator forms the disjoint union, glues each element to its images under the generating maps, and lists the classes of the generated equivalence relation. Elements are written `X:3` for the element $3$ of the set $X$. Predict the number of classes before you look.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    colimit_shape = mo.ui.dropdown(
        options=[
            "sum: X, Y",
            "coequalizer: s, t : X -> Y",
            "pushout: X <- Z -> Y",
            "chain: X0 -> X1 -> X2",
            "orbits: r : X -> X",
        ],
        value="pushout: X <- Z -> Y",
        label="Diagram",
    )
    colimit_n = mo.ui.slider(start=2, stop=12, step=1, value=6, label="n")
    colimit_k = mo.ui.slider(start=1, stop=6, step=1, value=4, label="k")
    mo.vstack([colimit_shape, colimit_n, colimit_k])
    return colimit_k, colimit_n, colimit_shape


@app.cell(hide_code=True)
def _(colimit_k, colimit_n, colimit_shape, mo):
    def _run():
        _n = colimit_n.value
        _k = colimit_k.value
        _kind = colimit_shape.value.split(":")[0]
        if _kind == "sum":
            _sets = {"X": list(range(_n)), "Y": list(range(_k))}
            _maps = {}
            _desc = {}
            _note = "No arrows, so nothing is glued: the colimit has n + k elements."
        elif _kind == "coequalizer":
            _sets = {"X": list(range(_n)), "Y": list(range(_n))}
            _maps = {
                "s": ("X", "Y", {x: x for x in range(_n)}),
                "t": ("X", "Y", {x: (x + _k) % _n for x in range(_n)}),
            }
            _desc = {"s": "x", "t": "x + k mod n"}
            _note = "Each class contains elements of Y that differ by multiples of k modulo n. How is the number of classes related to n and k?"
        elif _kind == "pushout":
            _m = min(_k, _n)
            _sets = {"X": list(range(_n)), "Y": [0, 1, 2], "Z": list(range(_m))}
            _maps = {
                "s": ("Z", "X", {z: z for z in range(_m)}),
                "t": ("Z", "Y", {z: z % 2 for z in range(_m)}),
            }
            _desc = {"s": "z (inclusion of the first min(k, n) elements)", "t": "z mod 2"}
            _note = "Look for elements of X that end up in the same class although no single map relates them: that is a zigzag through Y."
        elif _kind == "chain":
            _sets = {"X0": list(range(_k)), "X1": list(range(_k + 2)), "X2": list(range(_k + 2 + _n))}
            _maps = {
                "a": ("X0", "X1", {x: x for x in range(_k)}),
                "b": ("X1", "X2", {x: x for x in range(_k + 2)}),
            }
            _desc = {"a": "x (inclusion)", "b": "x (inclusion)"}
            _note = "Every class contains exactly one element of X2. Compare the count with the size of X2."
        else:
            _sets = {"X": list(range(_n))}
            _maps = {"r": ("X", "X", {x: (_k * x) % _n for x in range(_n)})}
            _desc = {"r": "k * x mod n"}
            _note = "One object and one generating arrow: the colimit glues each x to r(x). When r is a bijection the classes are its orbits."

        _elements = [(_name, _x) for _name in _sets for _x in _sets[_name]]
        _parent = {_e: _e for _e in _elements}

        def _find(e):
            while _parent[e] != e:
                e = _parent[e]
            return e

        _pairs = 0
        for (_dom, _cod, _fn) in _maps.values():
            for _x in _sets[_dom]:
                _pairs += 1
                _a, _b = _find((_dom, _x)), _find((_cod, _fn[_x]))
                if _a != _b:
                    _parent[_a] = _b
        _classes = {}
        for _e in _elements:
            _classes.setdefault(_find(_e), []).append(_e)

        _lines = ["| Set | Elements |", "|---|---|"]
        for _name in _sets:
            _lines.append("| $" + _name.replace("X0", "X_0").replace("X1", "X_1").replace("X2", "X_2") + "$ | "
                          + ", ".join(str(_e) for _e in _sets[_name]) + " |")
        _lines.append("")
        if _maps:
            _lines += ["| Generating map | Rule |", "|---|---|"]
            for _m2, (_dom, _cod, _fn) in _maps.items():
                _lines.append("| `" + _m2 + " : " + _dom + " -> " + _cod + "` | " + _desc[_m2] + " |")
            _lines.append("")
        _lines.append("**Elements of the disjoint union:** " + str(len(_elements))
                      + " &nbsp; **Generating pairs:** " + str(_pairs)
                      + " &nbsp; **Classes (elements of the colimit):** " + str(len(_classes)))
        _lines.append("")
        for _members in _classes.values():
            _lines.append("- `{ " + ", ".join(_name + ":" + str(_x) for (_name, _x) in _members) + " }`")
        _lines.append("")
        _lines.append(_note)
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Epics and Pushouts

    Recall from 1B: a map $e \colon X \to Y$ is **epic** if for every object $A$ and all maps $h, k \colon Y \to A$, $h e = k e$ implies $h = k$. It is the dual of monic: $e$ is epic in $\mathcal{A}$ exactly when it is monic in $\mathcal{A}^{\mathrm{op}}$. In $\mathbf{Set}$ the epics are the surjections.

    Section 8 of 5A proved that the pullback of a monic is monic. Its dual is a theorem about pushouts. We prove it twice, to practise dualizing a *proof* and not only a statement.

    ### Proof 6: the pushout of an epic is epic

    - **Goal.** Let the square below be a pushout in $\mathcal{A}$: $j_1 s = j_2 t$ and the universal property holds. If $t \colon Z \to Y$ is epic, then $j_1 \colon X \to Q$ is epic: for every object $A$ and all $h, k \colon Q \to A$, if $h j_1 = k j_1$ then $h = k$.
    - **Given.** The pushout property; $t$ is epic; Proof 9 of 5A (in a pullback square with $s p_1 = t p_2$, if $t$ is monic then $p_1$ is monic), valid in every category.
    - **Plan.** Dualize Proof 9 of 5A. Then write the dual argument out in $\mathcal{A}$, reversing each composite.
    - **Proof.** *By duality.* In $\mathcal{A}^{\mathrm{op}}$ the square is a pullback of $(s, t)$ with projections $j_1, j_2$, and $t$ is monic there. By Proof 9 of 5A applied in $\mathcal{A}^{\mathrm{op}}$, $j_1$ is monic in $\mathcal{A}^{\mathrm{op}}$, that is, epic in $\mathcal{A}$.

        *Directly.* Let $h, k \colon Q \to A$ with $h j_1 = k j_1$. Then
        $$(h j_2) \circ t = h (j_2 t) = h (j_1 s) = (h j_1) s = (k j_1) s = k (j_1 s) = k (j_2 t) = (k j_2) \circ t,$$
        using associativity, the commuting square, the hypothesis, and the commuting square again. Since $t$ is epic, $h j_2 = k j_2$.

        Put $f_1 = h j_1$ and $f_2 = h j_2$. They satisfy $f_1 s = h j_1 s = h j_2 t = f_2 t$, so they are valid test data for the pushout. Both $h$ and $k$ are mediating maps for them: $h j_1 = f_1$, $h j_2 = f_2$ by definition, and $k j_1 = h j_1 = f_1$, $k j_2 = h j_2 = f_2$ by the above. By the uniqueness clause of the pushout, $h = k$. $\qquad\blacksquare$
    - **What made it work.** The direct proof is Proof 9 of 5A read in a mirror: "compose after" became "compose before", monic became epic, and the uniqueness clause of the pullback became that of the pushout. When you dualize, change *every* arrow, including the ones hidden inside words like "monic".
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "Z": (0, 1.5, r"$Z$"), "Y": (1.8, 1.5, r"$Y$"),
            "X": (0, 0, r"$X$"), "Q": (1.8, 0, r"$Q$"), "A": (3.7, 0, r"$A$"),
        },
        [
            ("Z", "Y", r"$t$", {"side": -1, "color": "#1d4ed8"}),
            ("Z", "X", r"$s$", {"side": -1}),
            ("X", "Q", r"$j_1$", {"color": "#1d4ed8"}),
            ("Y", "Q", r"$j_2$", {"side": -1}),
            ("Q", "A", r"$h$", {"rad": -0.25}),
            ("Q", "A", r"$k$", {"rad": 0.25}),
        ],
        figsize=(5.4, 3.3),
        title="If t is epic then j1 is epic",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The second fact of 5A §8 also dualizes. For any map $f \colon X \to Y$, the square with $f$ along the top and down the left side, and $1_Y$ along the bottom and down the right side, commutes. The statement is:

    > $f$ is epic **if and only if** that square is a pushout.

    You are asked to prove this in `p04_epic_iff_pushout.md`, by a direct argument in $\mathcal{A}$.

    **Example in $\mathbf{Set}$.** Let $t \colon Z \to Y$ be surjective. In the pushout $(X + Y)/{\sim}$, every $(y, 2)$ equals $(t(z), 2)$ for some $z$ and is therefore glued to $(s(z), 1)$. So every class contains an element coming from $X$, which says that $j_1$ is surjective, in agreement with Proof 6.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375) (epics and pushouts); epics: [Riehl §1.2](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Colimits Across Categories

    Collecting the examples of this module and of 5A side by side:

    | Category | Product $X \times Y$ | Sum $X + Y$ | Equalizer of $s, t$ | Coequalizer of $s, t \colon X \to Y$ |
    |---|---|---|---|---|
    | $\mathbf{Set}$ | cartesian product | disjoint union | $\{x : s(x) = t(x)\}$ | $Y/{\sim}$, generated by $s(x) \sim t(x)$ |
    | $\mathbf{Top}$ | product topology | disjoint union topology | subspace | quotient space |
    | $\mathbf{Ab}$, $\mathbf{Vect}_k$ | cartesian product | direct sum (same object as the product) | $\ker(s - t)$ | $Y / \operatorname{im}(s - t)$ |
    | $\mathbf{Grp}$ | cartesian product | free product | $\{x : s(x) = t(x)\}$ | $Y/N$, with $N$ the normal subgroup generated by the $s(x)t(x)^{-1}$ |
    | a poset | meet $x \wedge y$ | join $x \vee y$ | identity | identity |

    Three observations.

    - **Posets.** In a poset, a cocone on any diagram $D$ with vertex $a$ is the statement "$D(I) \le a$ for all $I$" (the equations hold automatically, because there is at most one arrow between two objects). So a colimit of $D$ is a least upper bound of the set $\{D(I)\}$, and dually a limit of $D$ is a greatest lower bound. The proof is the argument you give in 5A·P01, with a family in place of a pair and, for colimits, with the order reversed.
    - **Limits are computed on underlying sets; colimits often are not.** In every row above, the product and the equalizer have the same underlying set as in $\mathbf{Set}$. For sums this is true in $\mathbf{Top}$ but false in $\mathbf{Ab}$ and $\mathbf{Grp}$: the underlying set of $\mathbb{Z} \oplus \mathbb{Z}$ is not the disjoint union of two copies of $\mathbb{Z}$. Module 5C makes this precise by asking which functors *preserve* limits and colimits.
    - **Completeness of the list.** By the dual of the theorem of 5A §7, each of these categories has all small colimits as soon as it has sums of arbitrary families and coequalizers. $\mathbf{Set}$, $\mathbf{Top}$, $\mathbf{Ab}$, $\mathbf{Vect}_k$ and $\mathbf{Grp}$ all do.

    > **References.** [Leinster §5.2](https://arxiv.org/abs/1612.09375); [Riehl §3.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Using a map out of a quotient before showing it is well defined.** "Define $\bar{g}([a]) = g(a)$; then $\bar{g} \pi = g$." *Diagnosis:* the formula mentions the representative $a$. Until you prove $a \sim b \Rightarrow g(a) = g(b)$ there is no function.
    2. **Treating the generating relation as if it were the equivalence relation.** "$[x] = [x']$, so $x' = (Du)(x)$ for some $u$." *Diagnosis:* classes are joined by zigzags of any length, in both directions. Use the Lemma of Section 3, which only asks you to check the generating pairs.
    3. **Dualizing only half of a statement.** Turning "pullback" into "pushout" but leaving "monic", or leaving a composite in its old order. *Diagnosis:* in $\mathcal{A}^{\mathrm{op}}$ every arrow turns round, so $g \circ f$ becomes $f \circ g$, "into" becomes "out of", and monic becomes epic.
    4. **Using the union for the sum.** *Diagnosis:* if $X$ and $Y$ share an element, the two clauses defining $\bar{f}$ may disagree on it. The tags in $X + Y$ are what make the definition by cases legitimate.
    5. **Assuming a colimit in $\mathbf{Grp}$ or $\mathbf{Ab}$ has the underlying set of the colimit in $\mathbf{Set}$.** *Diagnosis:* the universal property is tested against homomorphisms only. The sum of two abelian groups has underlying set $G \times H$, not the disjoint union.

    ---

    ## Why This Matters

    - **5C** asks which functors preserve limits and colimits. The contrast noticed in Section 7 (forgetful functors behave well with limits and badly with colimits) is its starting point.
    - **6A** re-expresses limits, and dually colimits, as adjoints to the diagonal functor.
    - **6B** proves that every presheaf is a colimit of representables. The explicit formula of Section 5, with its generated equivalence relation, is what makes that theorem computable.
    - **6C** proves that left adjoints preserve colimits. This explains at a stroke why free functors turn disjoint unions into free products and direct sums.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Diagrams of finite sets are encoded as in 5A:

    ```python
    diagram = {
        "sets": {"X": [0, 1, 2], "Y": [0, 1]},
        "maps": {"s": ("X", "Y", {0: 0, 1: 1, 2: 0})},   # name -> (domain, codomain, function as a dict)
    }
    ```

    An element of the disjoint union is a pair `(name, x)`. A cocone with vertex a finite set `B` is a dict `legs = {"X": {x: b, ...}, "Y": {...}}`. Fill in each `# TODO`, then un-comment the `print` checks.

    ### Exercise 1: The mediating map out of a colimit, with its well-definedness check

    The scaffolding computes the classes of the colimit. Write `induced(classes, legs)`. For each class it must collect the values `legs[name][x]` over all members `(name, x)` of the class. If some class yields more than one value, the family is not constant on classes and no mediating map exists: return `None`. Otherwise return the list of values, one per class, in the order of `classes`. This is the well-definedness check of 3A·P04, as a computation.
    """)
    return


@app.cell
def _():
    def _run():
        diagram = {
            "sets": {"X": [0, 1, 2, 3], "Y": [0, 1, 2], "Z": [0, 1]},
            "maps": {
                "s": ("Z", "X", {0: 0, 1: 1}),
                "t": ("Z", "Y", {0: 0, 1: 0}),
            },
        }

        def colimit_classes(diagram):
            _elements = [(_name, _x) for _name in diagram["sets"] for _x in diagram["sets"][_name]]
            _parent = {_e: _e for _e in _elements}

            def _find(e):
                while _parent[e] != e:
                    e = _parent[e]
                return e

            for (_dom, _cod, _fn) in diagram["maps"].values():
                for _x in diagram["sets"][_dom]:
                    _a, _b = _find((_dom, _x)), _find((_cod, _fn[_x]))
                    if _a != _b:
                        _parent[_a] = _b
            _classes = {}
            for _e in _elements:
                _classes.setdefault(_find(_e), []).append(_e)
            return sorted(sorted(_c) for _c in _classes.values())

        classes = colimit_classes(diagram)

        legs_good = {
            "X": {0: "p", 1: "p", 2: "q", 3: "r"},
            "Y": {0: "p", 1: "q", 2: "q"},
            "Z": {0: "p", 1: "p"},
        }
        legs_bad = {
            "X": {0: "p", 1: "q", 2: "q", 3: "r"},
            "Y": {0: "p", 1: "q", 2: "q"},
            "Z": {0: "p", 1: "q"},
        }

        def induced(classes, legs):
            # TODO: for each class, build the set of values legs[name][x] over its members;
            #       return None if any class has more than one value,
            #       otherwise the list of values in the order of `classes`
            _result = ...
            return _result

        # print(len(classes))                 # expected: 5
        # print(classes[0])                   # expected: [('X', 0), ('X', 1), ('Y', 0), ('Z', 0), ('Z', 1)]
        # print(induced(classes, legs_good))  # expected: ['p', 'q', 'r', 'q', 'q']
        # print(induced(classes, legs_bad))   # expected: None

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Find the zigzag

    Two tagged elements are equal in the colimit exactly when a zigzag joins them. The scaffolding builds, for each tagged element, the list of elements one generating step away (in either direction). Write `zigzag(start, end)`: a **shortest** zigzag from `start` to `end` as a list of tagged elements (including both ends), or `None` if there is none. A breadth-first search does it.
    """)
    return


@app.cell
def _():
    def _run():
        diagram = {
            "sets": {"X": [0, 1, 2, 3], "Y": [0, 1, 2], "Z": [0, 1]},
            "maps": {
                "s": ("Z", "X", {0: 0, 1: 1}),
                "t": ("Z", "Y", {0: 0, 1: 0}),
            },
        }
        neighbours = {(_name, _x): [] for _name in diagram["sets"] for _x in diagram["sets"][_name]}
        for (_dom, _cod, _fn) in diagram["maps"].values():
            for _x in diagram["sets"][_dom]:
                neighbours[(_dom, _x)].append((_cod, _fn[_x]))
                neighbours[(_cod, _fn[_x])].append((_dom, _x))

        def zigzag(start, end):
            # TODO: breadth-first search from `start` through `neighbours`,
            #       remembering for each visited element the element it was reached from;
            #       when `end` is reached, rebuild the path; return None if it is never reached
            _path = ...
            return _path

        # print(zigzag(("X", 0), ("X", 1)))   # expected: [('X', 0), ('Z', 0), ('Y', 0), ('Z', 1), ('X', 1)]
        # print(zigzag(("X", 2), ("X", 2)))   # expected: [('X', 2)]
        # print(zigzag(("X", 2), ("Y", 1)))   # expected: None

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: A coequalizer and its quotient map

    Given functions $s, t \colon X \to Y$ between finite sets (as dicts), write `coequalizer(X, Y, s, t)` returning a dict `q` that sends each $y \in Y$ to a label for its class; use the smallest element of the class as the label. Use the provided `classes_generated_by`. Then check the coequalizer equation $q \circ s = q \circ t$ and count the classes.
    """)
    return


@app.cell
def _():
    def _run():
        def classes_generated_by(elements, pairs):
            _parent = {_e: _e for _e in elements}

            def _find(e):
                while _parent[e] != e:
                    e = _parent[e]
                return e

            for (_a, _b) in pairs:
                _ra, _rb = _find(_a), _find(_b)
                if _ra != _rb:
                    _parent[_ra] = _rb
            _classes = {}
            for _e in elements:
                _classes.setdefault(_find(_e), []).append(_e)
            return sorted(sorted(_c) for _c in _classes.values())

        def coequalizer(X, Y, s, t):
            # TODO: the generating pairs are (s[x], t[x]) for x in X;
            #       get the classes, then send each y to the smallest element of its class
            _q = ...
            return _q

        n = 12
        X = list(range(n))
        Y = list(range(n))
        s = {x: x for x in X}
        t_shift = {x: (x + 8) % n for x in X}
        t_times = {x: (5 * x) % n for x in X}
        t_square = {x: (x * x) % n for x in X}

        # q = coequalizer(X, Y, s, t_shift)
        # print(all(q[s[x]] == q[t_shift[x]] for x in X))              # expected: True
        # print(len(set(q.values())))                                  # expected: 4
        # print(len(set(coequalizer(X, Y, s, t_times).values())))      # expected: 8
        # print(len(set(coequalizer(X, Y, s, t_square).values())))     # expected: 4

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | A union is a pushout — `exercises/5b/p01_union_is_pushout.md` | warm-up | universal-property proof in $\mathbf{Set}$ |
    | 2 | The cokernel is a coequalizer — `exercises/5b/p02_cokernel_coequalizer.md` | warm-up | maps out of a quotient |
    | 3 | A sum of epics is epic — `exercises/5b/p03_sum_of_epics.md` | core | dualizing a proof |
    | 4 | Epic if and only if a square is a pushout — `exercises/5b/p04_epic_iff_pushout.md` | core | translating between two definitions |
    | 5 | A monic coequalizer is an isomorphism — `exercises/5b/p05_monic_coequalizer_is_iso.md` | core | building an inverse from a universal property |
    | 6 | Pushouts of injections in Set — `exercises/5b/p06_pushout_of_injection.md` | stretch | choosing a test cocone |

    Write each proof in `proofs/5b/` under the same filename as its brief, using the five-step proof anatomy of this lecture.
    Then ask Claude to review it: the review points at gaps and asks questions; it does not hand you a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [5A: Limits](../5a_limits/) &nbsp;|&nbsp; Next: [5C: Functors & Limits](../5c_functors_and_limits/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
