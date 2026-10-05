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
    # 6B: Limits & Colimits of Presheaves

    > *Every presheaf is built from representables, and the recipe is written in the presheaf itself.*
    > — the density theorem, in one sentence

    Functor categories have been in the background since 1D, and since 4A one kind has mattered most: the category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ of presheaves on a small category $\mathcal{A}$, the home of the Yoneda embedding. This module asks two questions about such categories. *How do you compute a limit or colimit of functors?* And *how are arbitrary presheaves related to the representable ones?*

    The answer to the first is as simple as it could be: **pointwise**. To take a product of two functors, take the product of their values at each object. 5C stated this without proof; here you prove it, in four labelled stages, and you will see that every stage is one application of a universal property in the target category.

    The answer to the second is the **density theorem**: every presheaf $X$ is a colimit of representables, and the diagram of which it is the colimit is indexed by the *category of elements* of $X$. This is the categorical analogue of "every set is a union of its one-element subsets" and "every graph is glued from its vertices and edges". By the end you will be able to prove both theorems and to compute a category of elements by hand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Evaluation, and Diagrams of Functors

    Fix a small category $\mathcal{A}$ and a locally small category $\mathcal{S}$. Then $[\mathcal{A}, \mathcal{S}]$ is locally small: a natural transformation $X \Rightarrow Y$ is an element of the product $\prod_{A \in \mathcal{A}} \mathcal{S}(X(A), Y(A))$, a product of sets indexed by a set.

    > **Definition (evaluation).** For each object $A$ of $\mathcal{A}$, the **evaluation functor**
    > $$\mathrm{ev}_A \colon [\mathcal{A}, \mathcal{S}] \to \mathcal{S}$$
    > sends a functor $X$ to the object $X(A)$ and a natural transformation $\alpha \colon X \Rightarrow Y$ to its component $\alpha_A \colon X(A) \to Y(A)$.

    **Reading the definition.** $\mathrm{ev}_A$ is a functor because identities and composites of natural transformations are computed componentwise (1D): $(1_X)_A = 1_{X(A)}$ and $(\beta \circ \alpha)_A = \beta_A \circ \alpha_A$.

    Now let $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ be a diagram of functors, with $\mathbf{I}$ small. It has two inputs, so fix notation:

    - for $I \in \mathbf{I}$, $D(I)$ is a functor $\mathcal{A} \to \mathcal{S}$, with values $D(I)(A)$ and $D(I)(f)$;
    - for $u \colon I \to J$ in $\mathbf{I}$, $D(u) \colon D(I) \Rightarrow D(J)$ is a natural transformation with components $D(u)_A$;
    - for $A \in \mathcal{A}$, write $D_A = \mathrm{ev}_A \circ D \colon \mathbf{I} \to \mathcal{S}$. This is an ordinary diagram in $\mathcal{S}$, with $D_A(I) = D(I)(A)$ and $D_A(u) = D(u)_A$.

    **Examples.**

    - *Two functors.* If $\mathbf{I}$ is discrete with two objects, $D$ is a pair of functors $(X, Y)$ and $D_A$ is the pair of objects $(X(A), Y(A))$.
    - *Graphs.* Let $\mathcal{G}$ be the category with two objects $V, E$ and two non-identity maps $s, t \colon V \to E$. A presheaf $X \colon \mathcal{G}^{\mathrm{op}} \to \mathbf{Set}$ is a directed graph: a set $X(V)$ of vertices, a set $X(E)$ of edges, and functions $X(s), X(t) \colon X(E) \to X(V)$ giving each edge its source and target. A diagram in $[\mathcal{G}^{\mathrm{op}}, \mathbf{Set}]$ is a diagram of graphs; $D_V$ is the diagram of their vertex sets and $D_E$ the diagram of their edge sets.
    - *Monoid actions.* If $\mathcal{A}$ is a monoid $M$ regarded as a one-object category, there is only one evaluation functor, and it sends an $M$-set to its underlying set.

    **Non-example.** $\mathrm{ev}_A$ is not faithful in general: two different maps of graphs can agree on vertices and differ on edges. Knowing a natural transformation at one object does not determine it. All the evaluation functors *together* do: two natural transformations with the same components are equal.

    One fact from 5A will be used again and again, so it gets a name.

    > **Joint monicity of projections.** If $(p_I \colon L \to D(I))_I$ is a limit cone and $g, g' \colon B \to L$ satisfy $p_I g = p_I g'$ for all $I$, then $g = g'$.

    The reason: $(p_I g)_I$ is a cone with vertex $B$ (6A, Lemma 2), and $g$ and $g'$ are both maps that mediate it; the uniqueness clause of the universal property makes them equal.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Limits in Functor Categories Are Computed Pointwise

    Suppose you want the product of two graphs. A reasonable guess: vertices are pairs of vertices, edges are pairs of edges, and source and target are taken in each coordinate. The guess has two parts, and it is worth separating them. First, *each value* of the product is a product of values. Second, the *action on maps* (source and target) must be defined somehow, and must make the result a functor. The theorem says that the second part takes care of itself: the universal property of the pointwise limits forces a unique action on maps.

    > **Theorem 1 (pointwise limits).** Let $\mathcal{A}$ and $\mathbf{I}$ be small categories, $\mathcal{S}$ a locally small category and $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ a diagram. Suppose that for each $A \in \mathcal{A}$ the diagram $D_A = \mathrm{ev}_A \circ D \colon \mathbf{I} \to \mathcal{S}$ has a limit. Then:
    >
    > **(a)** there is a cone $(p_I \colon L \Rightarrow D(I))_{I}$ on $D$ such that, for each $A$, the cone $(p_{I,A} \colon L(A) \to D(I)(A))_I$ is a limit cone on $D_A$;
    >
    > **(b)** every cone on $D$ with that property is a limit cone on $D$.

    The proof is long only because there is a lot to name. Here it is in proof-anatomy form, with the proof itself in four stages.

    - **Goal.** (a) Construct a functor $L \colon \mathcal{A} \to \mathcal{S}$ and natural transformations $p_I \colon L \Rightarrow D(I)$ forming a cone on $D$, with each $(p_{I,A})_I$ a limit cone. (b) For any cone $(p_I \colon L \Rightarrow D(I))_I$ on $D$ whose components at each $A$ form a limit cone on $D_A$: for every functor $X$ and every cone $(q_I \colon X \Rightarrow D(I))_I$ on $D$ there is a unique natural transformation $h \colon X \Rightarrow L$ with $p_I \circ h = q_I$ for all $I$.
    - **Given.** For each $A$, a chosen limit cone $(p_{I,A} \colon L(A) \to D(I)(A))_I$ on $D_A$ in $\mathcal{S}$. Naturality of each $D(u)$. Joint monicity of projections.
    - **Plan.** Everything that has to be a map into some $L(A')$ is *defined* by the universal property of $L(A')$, and every equation between maps into $L(A')$ is *proved* by composing with the projections $p_{I,A'}$.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "LA": (0, 1.7, r"$L(A)$"),
            "LB": (3.2, 1.7, r"$L(A')$"),
            "DA": (0, 0, r"$D(I)(A)$"),
            "DB": (3.2, 0, r"$D(I)(A')$"),
        },
        [
            ("LA", "LB", r"$L(f)$", {"dashed": True, "color": "#b91c1c"}),
            ("LA", "DA", r"$p_{I,A}$", {"side": -1}),
            ("LB", "DB", r"$p_{I,A'}$"),
            ("DA", "DB", r"$D(I)(f)$", {"side": -1}),
        ],
        figsize=(5.8, 3.0),
        title="Stage 1: L(f) is the unique map making this commute for every I",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - **Proof.**

      **Stage 1: $L$ on maps.** Let $f \colon A \to A'$ in $\mathcal{A}$. Consider the family $\big(D(I)(f) \circ p_{I,A}\big)_I$ of maps out of $L(A)$. It is a cone on $D_{A'}$: for $u \colon I \to J$,
      $$D(u)_{A'} \circ D(I)(f) \circ p_{I,A} = D(J)(f) \circ D(u)_A \circ p_{I,A} = D(J)(f) \circ p_{J,A},$$
      the first step by naturality of $D(u)$ at $f$ and the second because $(p_{I,A})_I$ is a cone on $D_A$. By the universal property of $L(A')$ there is a unique map $L(f) \colon L(A) \to L(A')$ with
      $$p_{I,A'} \circ L(f) = D(I)(f) \circ p_{I,A} \quad\text{for all } I. \tag{$\star$}$$

      **Stage 2: $L$ is a functor.** *Identities.* $1_{L(A)}$ satisfies $(\star)$ for $f = 1_A$, because $D(I)(1_A) = 1$; by uniqueness $L(1_A) = 1_{L(A)}$. *Composition.* For $f \colon A \to A'$ and $f' \colon A' \to A''$,
      $$p_{I,A''} \circ L(f') \circ L(f) = D(I)(f') \circ p_{I,A'} \circ L(f) = D(I)(f') \circ D(I)(f) \circ p_{I,A} = D(I)(f'f) \circ p_{I,A},$$
      using $(\star)$ twice and functoriality of $D(I)$. So $L(f')L(f)$ satisfies the equation $(\star)$ that defines $L(f'f)$; by uniqueness they are equal.

      **Stage 3: the $p_I$ form a cone on $D$.** For fixed $I$, equation $(\star)$ is the naturality square of the family $p_I = (p_{I,A})_A$ at $f$. So $p_I \colon L \Rightarrow D(I)$ is a natural transformation. For $u \colon I \to J$ we need $D(u) \circ p_I = p_J$ in $[\mathcal{A}, \mathcal{S}]$; two natural transformations are equal when their components are, and at $A$ the equation reads $D(u)_A \circ p_{I,A} = p_{J,A}$, which holds because $(p_{I,A})_I$ is a cone on $D_A$. This proves (a).

      **Stage 4: any pointwise-limit cone is a limit cone.** Let $(p_I \colon L \Rightarrow D(I))_I$ be a cone on $D$ whose components at each $A$ form a limit cone on $D_A$, and let $(q_I \colon X \Rightarrow D(I))_I$ be any cone on $D$.

      *Components of $h$.* Applying the functor $\mathrm{ev}_A$ to the cone $q$ gives a cone $(q_{I,A})_I$ on $D_A$ with vertex $X(A)$. So there is a unique map $h_A \colon X(A) \to L(A)$ with $p_{I,A} \circ h_A = q_{I,A}$ for all $I$.

      *$h$ is natural.* Let $f \colon A \to A'$. The maps $L(f) \circ h_A$ and $h_{A'} \circ X(f)$ both go $X(A) \to L(A')$. Compose each with $p_{I,A'}$:
      $$p_{I,A'} \circ L(f) \circ h_A = D(I)(f) \circ p_{I,A} \circ h_A = D(I)(f) \circ q_{I,A},$$
      $$p_{I,A'} \circ h_{A'} \circ X(f) = q_{I,A'} \circ X(f) = D(I)(f) \circ q_{I,A},$$
      using naturality of $p_I$ in the first line and naturality of $q_I$ in the second. The two composites agree for every $I$, so by joint monicity of the projections of $L(A')$, $L(f) h_A = h_{A'} X(f)$.

      *$h$ mediates, uniquely.* $p_I \circ h = q_I$ holds because it holds in each component. If $h' \colon X \Rightarrow L$ also satisfies $p_I \circ h' = q_I$ for all $I$, then $p_{I,A} h'_A = q_{I,A}$ for all $I$, so $h'_A = h_A$ by the uniqueness of $h_A$; this for every $A$ gives $h' = h$. This proves (b). $\blacksquare$
    - **What made it work.** In all four stages the pattern was identical: to build a map into a limit, build a cone; to prove two maps into a limit equal, compose with every projection. No element of any object of $\mathcal{S}$ was ever mentioned, so the proof works for any $\mathcal{S}$.

    > **Corollary 1.** Let $\mathcal{A}, \mathbf{I}$ be small and $\mathcal{S}$ locally small. If $\mathcal{S}$ has all limits of shape $\mathbf{I}$, then so does $[\mathcal{A}, \mathcal{S}]$, and each evaluation functor $\mathrm{ev}_A$ preserves them.

    - **Goal.** (i) Every $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ has a limit. (ii) For *every* limit cone $(p'_I \colon L' \Rightarrow D(I))_I$ on $D$ and every $A$, the cone $(p'_{I,A})_I$ is a limit cone on $D_A$.
    - **Given.** Theorem 1; uniqueness of limits up to isomorphism (5A).
    - **Plan.** (i) is Theorem 1. For (ii), compare an arbitrary limit cone with the one Theorem 1 built.
    - **Proof.** (i) Each $D_A$ has a limit by hypothesis, so Theorem 1(a) and (b) give a limit cone $(p_I \colon L \Rightarrow D(I))_I$ on $D$ which is a limit cone at each $A$. (ii) Since $p'$ and $p$ are both limit cones on $D$, there is an isomorphism $j \colon L' \to L$ in $[\mathcal{A}, \mathcal{S}]$ with $p_I \circ j = p'_I$ for all $I$ (5A). Each component $j_A$ is an isomorphism in $\mathcal{S}$ (1D), and $p'_{I,A} = p_{I,A} \circ j_A$. A cone obtained from a limit cone by composing with an isomorphism of vertices is again a limit cone (5A), so $(p'_{I,A})_I$ is a limit cone on $D_A$. $\blacksquare$
    - **What made it work.** "Preserves limits" is a statement about every limit cone, not just the one you constructed. Uniqueness up to isomorphism is what transfers a property from one limit cone to all of them.

    **The dual.** Replacing $\mathcal{S}$ by $\mathcal{S}^{\mathrm{op}}$ (and noting $[\mathcal{A}, \mathcal{S}]^{\mathrm{op}} \cong [\mathcal{A}^{\mathrm{op}}, \mathcal{S}^{\mathrm{op}}]$) gives the same theorem for colimits. In particular:

    $$\boxed{\;\text{For small } \mathcal{A},\ [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}] \text{ has all small limits and colimits, and they are computed pointwise.}\;}$$

    **Examples in graphs** ($\mathcal{A} = \mathcal{G}$).

    - The product $X \times Y$ has vertices $X(V) \times Y(V)$ and edges $X(E) \times Y(E)$; the source of $(e, e')$ is forced by $(\star)$ to be $(\text{source of } e, \text{source of } e')$.
    - The sum $X + Y$ is the disjoint union on vertices and on edges.
    - The terminal graph has one vertex and one edge (necessarily a loop), since $1 \in \mathbf{Set}$ has one element.
    - The initial graph is empty.

    **A warning about the hypothesis.** Theorem 1 assumes the pointwise limits exist. If $\mathcal{S}$ lacks some limits of shape $\mathbf{I}$, the theorem says nothing about a diagram $D$ for which some $D_A$ has no limit, and Leinster §6.2 warns that $D$ may then still have a limit in $[\mathcal{A}, \mathcal{S}]$ which is not computed pointwise. "Pointwise" is a theorem about complete targets such as $\mathbf{Set}$, not a definition.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375) (limits in functor categories); [Riehl §3.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell
def _():
    def _run():
        # Two graphs as presheaves on G: vertex set, edge set, source and target functions.
        _X = {"V": ["a", "b", "c"], "E": ["p", "q"], "s": {"p": "a", "q": "b"}, "t": {"p": "b", "q": "c"}}
        _Y = {"V": ["v"], "E": ["l"], "s": {"l": "v"}, "t": {"l": "v"}}

        # The sum X + Y, pointwise: disjoint union at V and at E, source and target inherited.
        _sum_V = [("X", _v) for _v in _X["V"]] + [("Y", _v) for _v in _Y["V"]]
        _sum_E = [("X", _e) for _e in _X["E"]] + [("Y", _e) for _e in _Y["E"]]
        _src = {("X", _e): ("X", _X["s"][_e]) for _e in _X["E"]}
        _src.update({("Y", _e): ("Y", _Y["s"][_e]) for _e in _Y["E"]})
        _tgt = {("X", _e): ("X", _X["t"][_e]) for _e in _X["E"]}
        _tgt.update({("Y", _e): ("Y", _Y["t"][_e]) for _e in _Y["E"]})

        print("X = path a -> b -> c,   Y = one vertex with a loop")
        print("Pointwise sum X + Y:")
        print("  vertices:", _sum_V)
        for _e in _sum_E:
            print(f"  edge {_e}: {_src[_e]} -> {_tgt[_e]}")
        print()
        print("Terminal graph (pointwise terminal): 1 vertex, 1 edge, and that edge is a loop.")
        print("Initial graph (pointwise initial): 0 vertices, 0 edges.")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. The Yoneda Embedding Preserves Limits

    Theorem 1(b) is a tool for *recognising* limits of functors: to show a cone of functors is a limit cone, check it one object at a time. Here is the first use.

    Recall the Yoneda embedding $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$, $A \mapsto H_A = \mathcal{A}(-, A)$, which is full and faithful (4C).

    > **Theorem 2.** For a small category $\mathcal{A}$, the Yoneda embedding $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ preserves limits.

    - **Goal.** For every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every limit cone $(p_I \colon L \to D(I))_I$ in $\mathcal{A}$, the cone $(H_{p_I} \colon H_L \Rightarrow H_{D(I)})_I$ is a limit cone on $H_\bullet \circ D$ in $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$.
    - **Given.** Theorem 1(b) with $\mathcal{A}^{\mathrm{op}}$ in place of $\mathcal{A}$ and $\mathcal{S} = \mathbf{Set}$. Representables preserve limits (6A, Theorem 3).
    - **Plan.** Pointwise argument: evaluate at each object $B$ and recognise the result.
    - **Proof.** The family $(H_{p_I})_I$ is a cone on $H_\bullet \circ D$ because functors send cones to cones. Fix $B \in \mathcal{A}$. The component at $B$ of $H_{p_I}$ is the function $p_I \circ - \colon \mathcal{A}(B, L) \to \mathcal{A}(B, D(I))$. So evaluating the cone $(H_{p_I})_I$ at $B$ gives the cone $\big(p_I \circ -\big)_I$ on the diagram $\mathcal{A}(B, D(-))$ in $\mathbf{Set}$, which is the image of the limit cone $(p_I)$ under $\mathcal{A}(B, -)$. By 6A, Theorem 3, that image is a limit cone. So the cone $(H_{p_I})_I$ is a limit cone at each $B$, and by Theorem 1(b) it is a limit cone. $\blacksquare$
    - **What made it work.** The values of $H_\bullet$ at a fixed test object $B$ are the values of the representable $\mathcal{A}(B, -)$. "Pointwise" turned a statement about the embedding into a statement about hom-functors that was already proved.

    **Example.** If $\mathcal{A}$ has a product $A \times B$, then $H_{A \times B} \cong H_A \times H_B$, where the right-hand product is the pointwise one.

    **Non-example: colimits.** $H_\bullet$ does not preserve colimits. Let $\mathcal{A}$ be the poset $\{0 < 1\}$; its initial object is $0$. The presheaf $H_0$ has $H_0(0) = \{1_0\}$, a one-element set. But the initial object of $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is computed pointwise, so it is empty at every object. Hence $H_0$ is not initial. The Yoneda embedding keeps the limits $\mathcal{A}$ already has, and adds colimits freely rather than preserving the old ones.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Category of Elements

    A presheaf $X$ on $\mathcal{A}$ has a set of "elements" at each object. These sets are not independent: a map $f \colon A' \to A$ carries elements of $X(A)$ to elements of $X(A')$. The category of elements records all the elements and all these relationships in a single category.

    > **Definition (category of elements).** Let $\mathcal{A}$ be a category and $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ a presheaf. The **category of elements** $\mathbf{E}(X)$ has
    >
    > - *objects:* pairs $(A, x)$ with $A \in \mathcal{A}$ and $x \in X(A)$;
    > - *maps* $(A', x') \to (A, x)$: maps $f \colon A' \to A$ in $\mathcal{A}$ such that $(Xf)(x) = x'$;
    > - composition and identities as in $\mathcal{A}$.
    >
    > The **projection functor** $P \colon \mathbf{E}(X) \to \mathcal{A}$ sends $(A, x)$ to $A$ and $f$ to $f$.

    **Reading the definition.**

    - An object is an element *together with* the object it lives over. The same underlying thing appearing in $X(A)$ and $X(A')$ gives two different objects.
    - Mind the direction. $f$ goes $A' \to A$, but $Xf$ goes $X(A) \to X(A')$ because $X$ is contravariant. The condition takes the element of the *codomain* object, $x$, and requires that $Xf$ send it to the element of the *domain* object, $x'$.
    - That composites of such maps again satisfy the condition, and that identities do, has to be checked. This is brief P01.
    - If $\mathcal{A}$ is small then $\mathbf{E}(X)$ is small: its objects form the set $\coprod_{A} X(A)$.

    **Examples.**

    - *Graphs.* For a graph $X$ (a presheaf on $\mathcal{G}$), the objects of $\mathbf{E}(X)$ are the vertices and the edges of $X$. The non-identity maps are: for each edge $e$, one map labelled $s$ from the source vertex of $e$ to $e$, and one labelled $t$ from the target vertex of $e$ to $e$. The widget below draws this.
    - *Sets.* If $\mathcal{A} = \mathbf{1}$, a presheaf is a set $X$ and $\mathbf{E}(X)$ is the discrete category on the elements of $X$.
    - *Monoid actions.* If $\mathcal{A}$ is a monoid $M$, a presheaf is a set $X$ with a right action $x \cdot m = (Xm)(x)$. Then $\mathbf{E}(X)$ has the elements of $X$ as objects, and a map $x' \to x$ is an $m \in M$ with $x \cdot m = x'$.
    - *Representables.* $\mathbf{E}(H_B)$ has objects the maps $g \colon A \to B$ into $B$, and a map from $g' \colon A' \to B$ to $g \colon A \to B$ is an $f$ with $g f = g'$. This is the slice category $\mathcal{A}/B$ of 2C (brief P02).

    **Non-example.** For a graph, an edge $e$ from $a$ to $b$ does *not* give a map $(V, a) \to (V, b)$ in $\mathbf{E}(X)$. Maps in $\mathbf{E}(X)$ come only from maps of $\mathcal{A}$, and $\mathcal{G}$ has no non-identity map $V \to V$. The edge appears as an object, sitting above both its endpoints.

    **The Yoneda reading.** By the Yoneda lemma (4B), an element $x \in X(A)$ is the same as a natural transformation
    $$\tilde{x} \colon H_A \Rightarrow X, \qquad \tilde{x}_B(g) = (Xg)(x) \ \text{ for } g \colon B \to A,$$
    and $x$ is recovered as $\tilde{x}_A(1_A)$. So an object of $\mathbf{E}(X)$ is a representable *with a map to $X$*. The next section shows that a map $f \colon (A', x') \to (A, x)$ is then a commuting triangle $\tilde{x} \circ H_f = \tilde{x}'$.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375) (category of elements); [Riehl §2.4](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell
def _(mo):
    elements_pick = mo.ui.dropdown(
        options=[
            "path: a -> b -> c",
            "loop: one vertex with one loop",
            "H_E: a single edge with two distinct endpoints",
            "H_V: a single vertex and no edges",
            "two parallel edges a => b",
        ],
        value="path: a -> b -> c",
        label="Presheaf on G (a directed graph)",
    )
    elements_pick
    return (elements_pick,)


@app.cell
def _(elements_pick):
    def _run():
        _presets = {
            "path": (["a", "b", "c"], {"p": ("a", "b"), "q": ("b", "c")}),
            "loop": (["v"], {"l": ("v", "v")}),
            "H_E:": (["s", "t"], {"1_E": ("s", "t")}),
            "H_V:": (["1_V"], {}),
            "two ": (["a", "b"], {"p": ("a", "b"), "q": ("a", "b")}),
        }
        _verts, _edges = _presets[elements_pick.value[:4]]
        _width = 2.2 * max(len(_verts) - 1, len(_edges) - 1, 1)
        _nodes = {}
        for _i, _v in enumerate(_verts):
            _x = _width * (_i / (len(_verts) - 1)) if len(_verts) > 1 else _width / 2
            _nodes["V" + _v] = (_x, 0.0, r"$(V,\ " + _v + r")$")
        for _i, _e in enumerate(_edges):
            _x = _width * ((_i + 0.5) / len(_edges))
            _nodes["E" + _e] = (_x, 1.9, r"$(E,\ " + _e + r")$")
        _arrows = []
        for _e, (_src, _dst) in _edges.items():
            _same = _src == _dst
            _arrows.append(("V" + _src, "E" + _e, r"$s$", {"rad": 0.3 if _same else 0.0, "color": "#1d4ed8"}))
            _arrows.append(("V" + _dst, "E" + _e, r"$t$", {"rad": -0.3 if _same else 0.0, "color": "#b91c1c"}))
        _title = (
            f"E(X): {len(_verts) + len(_edges)} objects, {2 * len(_edges)} non-identity arrows "
            f"(identities not drawn)"
        )
        return draw_diagram(_nodes, _arrows, figsize=(7.0, 3.6), title=_title)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The picture is the graph with every edge *subdivided*: each edge has become an object, receiving one arrow from each of its endpoints. Look at the two representable presets. $\mathbf{E}(H_E)$ has an object, $(E, 1_E)$, that receives exactly one arrow from every object; $\mathbf{E}(H_V)$ is a single object. For the non-representable graphs there is no object with that property. Brief P04 turns this observation into a theorem.

    ---

    ## 5. The Density Theorem

    A graph is assembled from its vertices and edges by gluing: take one copy of "a bare vertex" for each vertex, one copy of "a bare edge" for each edge, and identify the endpoints of the edges with the right vertices. "A bare vertex" and "a bare edge" are the representables $H_V$ and $H_E$, and "identify" is a colimit. The density theorem says the same recipe works for every presheaf on every small category, and the gluing instructions are exactly $\mathbf{E}(X)$.

    > **Theorem 3 (density).** Let $\mathcal{A}$ be a small category and $X$ a presheaf on $\mathcal{A}$. Then $X$ is the colimit of the diagram
    > $$\mathbf{E}(X) \xrightarrow{\;P\;} \mathcal{A} \xrightarrow{\;H_\bullet\;} [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}].$$
    > Precisely: the family $\big(\tilde{x} \colon H_A \Rightarrow X\big)_{(A,x) \in \mathbf{E}(X)}$ is a colimit cocone on $H_\bullet \circ P$.

    The diagram sends an object $(A, x)$ to $H_A$ and a map $f \colon (A', x') \to (A, x)$ to $H_f \colon H_{A'} \Rightarrow H_A$. It is a small diagram because $\mathbf{E}(X)$ is small.

    - **Goal.** (1) The family $(\tilde{x})_{(A,x)}$ is a cocone: $\tilde{x} \circ H_f = \tilde{x}'$ for every map $f \colon (A', x') \to (A, x)$ of $\mathbf{E}(X)$. (2) For every presheaf $Y$ and every cocone $\big(\alpha_{(A,x)} \colon H_A \Rightarrow Y\big)_{(A,x)}$ on $H_\bullet \circ P$, there is a unique natural transformation $\theta \colon X \Rightarrow Y$ with $\theta \circ \tilde{x} = \alpha_{(A,x)}$ for all $(A, x)$.
    - **Given.** The Yoneda lemma (4B): for each presheaf $Z$ and object $A$, the assignments $z \mapsto \tilde{z}$ and $\beta \mapsto \beta_A(1_A)$ are mutually inverse bijections between $Z(A)$ and the set of natural transformations $H_A \Rightarrow Z$.
    - **Plan.** Translate every natural transformation out of a representable into an element, using Yoneda. A cocone then becomes a family of elements of $Y$, the cocone condition becomes naturality of $\theta$, and the rest is "follow the identity".
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "HA2": (0, 2.6, r"$H_{A'}$"),
            "HA": (3.2, 2.6, r"$H_A$"),
            "X": (1.6, 1.3, r"$X$"),
            "Y": (1.6, -0.4, r"$Y$"),
        },
        [
            ("HA2", "HA", r"$H_f$"),
            ("HA2", "X", r"$\tilde{x}'$"),
            ("HA", "X", r"$\tilde{x}$", {"side": -1}),
            ("X", "Y", r"$\exists!\,\theta$", {"dashed": True, "color": "#b91c1c"}),
            ("HA2", "Y", r"$\alpha_{(A',x')}$", {"rad": 0.3}),
            ("HA", "Y", r"$\alpha_{(A,x)}$", {"rad": -0.3}),
        ],
        figsize=(6.0, 4.6),
        title="Density: X is the universal cocone under the representables mapping to it",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - **Proof.**

      **Stage 0: one computation, used twice.** Let $Z$ be any presheaf, $f \colon A' \to A$ a map of $\mathcal{A}$ and $z \in Z(A)$. Then
      $$\tilde{z} \circ H_f = \widetilde{(Zf)(z)} \quad\text{as natural transformations } H_{A'} \Rightarrow Z. \tag{$\dagger$}$$
      *Check:* at an object $B$ and $g \in H_{A'}(B) = \mathcal{A}(B, A')$, the left side gives $\tilde{z}_B(f g) = Z(fg)(z)$, and the right side gives $(Zg)\big((Zf)(z)\big)$. These agree because $Z$ is a contravariant functor: $Z(fg) = Z(g) \circ Z(f)$.

      **Stage 1: the family $(\tilde{x})$ is a cocone.** Let $f \colon (A', x') \to (A, x)$ be a map of $\mathbf{E}(X)$, so $(Xf)(x) = x'$. By $(\dagger)$ with $Z = X$, $\tilde{x} \circ H_f = \widetilde{(Xf)(x)} = \tilde{x}'$.

      **Stage 2: translate a cocone into a family of elements.** Let $(\alpha_{(A,x)} \colon H_A \Rightarrow Y)$ be a cocone. For each object $(A, x)$ of $\mathbf{E}(X)$ let
      $$y_{(A,x)} = \big(\alpha_{(A,x)}\big)_A(1_A) \in Y(A),$$
      so that $\alpha_{(A,x)} = \widetilde{y_{(A,x)}}$ by Yoneda. The cocone condition at $f \colon (A', x') \to (A, x)$ says $\alpha_{(A,x)} \circ H_f = \alpha_{(A',x')}$. By $(\dagger)$ with $Z = Y$ the left side is $\widetilde{(Yf)(y_{(A,x)})}$, and the right side is $\widetilde{y_{(A',x')}}$. Since $z \mapsto \tilde{z}$ is injective, the cocone condition at $f$ is equivalent to
      $$(Yf)\big(y_{(A,x)}\big) = y_{(A',x')}. \tag{$\ddagger$}$$

      **Stage 3: define $\theta$ and prove it is natural.** For each $A \in \mathcal{A}$ define a function
      $$\theta_A \colon X(A) \to Y(A), \qquad \theta_A(x) = y_{(A,x)}.$$
      Let $f \colon A' \to A$ be any map of $\mathcal{A}$ and $x \in X(A)$. Then $f$ is a map $(A', (Xf)(x)) \to (A, x)$ in $\mathbf{E}(X)$, by the definition of $\mathbf{E}(X)$. Equation $(\ddagger)$ for this map reads $(Yf)(\theta_A(x)) = \theta_{A'}((Xf)(x))$. As $x$ was arbitrary, $Yf \circ \theta_A = \theta_{A'} \circ Xf$, which is the naturality square of $\theta$ at $f$.

      **Stage 4: $\theta$ mediates.** Fix $(A, x)$. The natural transformation $\theta \circ \tilde{x} \colon H_A \Rightarrow Y$ corresponds under Yoneda to the element $(\theta \circ \tilde{x})_A(1_A) = \theta_A(\tilde{x}_A(1_A)) = \theta_A(x) = y_{(A,x)}$. The natural transformation $\alpha_{(A,x)}$ corresponds to the same element. Since the Yoneda correspondence is a bijection, $\theta \circ \tilde{x} = \alpha_{(A,x)}$.

      **Stage 5: $\theta$ is unique.** Let $\theta' \colon X \Rightarrow Y$ satisfy $\theta' \circ \tilde{x} = \alpha_{(A,x)}$ for all $(A, x)$. Evaluate both sides at $A$ on $1_A$: the left side gives $\theta'_A(x)$ and the right gives $y_{(A,x)} = \theta_A(x)$. So $\theta'_A(x) = \theta_A(x)$ for every $A$ and every $x \in X(A)$, that is, $\theta' = \theta$. $\blacksquare$
    - **What made it work.** Yoneda turned maps out of representables into elements, and after that there were no choices left: $\theta_A(x)$ *had* to be $y_{(A,x)}$ (Stage 5), and the cocone condition was exactly what made that forced definition natural (Stage 3). When a universal property involves representables, translate with Yoneda first and look at what the conditions become.

    Notice where each hypothesis was used. Smallness of $\mathcal{A}$ makes $\mathbf{E}(X)$ a small category, so that the theorem is about a small colimit, and makes $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ locally small. The cocone condition for *every* map of $\mathbf{E}(X)$ was needed in Stage 3: dropping some maps would leave $\theta$ a family of functions that need not be natural.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375) (every presheaf is a colimit of representables); [Riehl §2.4](https://math.jhu.edu/~eriehl/context.pdf) for the category of elements it is built on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Reading the Density Theorem in Small Cases

    A theorem this general is best understood by specialising it until it says something you already believe.

    **Sets ($\mathcal{A} = \mathbf{1}$).** A presheaf is a set $X$. The only representable is the one-element set $1$. $\mathbf{E}(X)$ is discrete with one object per element of $X$, so the diagram is $|X|$ copies of $1$ with no maps between them, and its colimit is a sum. The theorem reads
    $$X \;\cong\; \coprod_{x \in X} 1 :$$
    every set is the disjoint union of its one-element subsets. The cocone map $\tilde{x} \colon 1 \to X$ picks out $x$.

    **Graphs ($\mathcal{A} = \mathcal{G}$).** The representables are $H_V$ (one vertex) and $H_E$ (one edge with two distinct endpoints). $\mathbf{E}(X)$ is the subdivided graph of the widget. The theorem says that $X$ is obtained from a disjoint union of copies of $H_V$ (one per vertex) and $H_E$ (one per edge) by gluing: each arrow $s \colon (V, a) \to (E, e)$ identifies the single vertex of that copy of $H_V$ with the source endpoint of that copy of $H_E$, and similarly for $t$. For the path $a \to b \to c$ the two edge-copies each bring two endpoints, four in all, and the gluing identifies the target endpoint of $p$ with the source endpoint of $q$ through the shared vertex $b$, leaving three vertices.

    **A representable ($X = H_B$).** $\mathbf{E}(H_B)$ has a terminal object $(B, 1_B)$. One can check that a colimit over a category with a terminal object is the value of the diagram at that object, so the theorem returns $H_B \cong H_B$. Nothing is learned, which is as it should be: a representable needs no assembling.

    **What density buys.** A natural transformation out of $X$ is the same thing as a cocone out of the diagram of representables over $X$. So any construction on presheaves that respects colimits is determined by what it does on representables, that is, on $\mathcal{A}$ itself. Brief P05 asks you to prove one precise form of this.

    **Non-example.** Density does not say that every presheaf is a *sum* of representables. The loop graph has one vertex and one edge; a sum of representables with one edge is $H_E$, possibly plus isolated vertices, and $H_E$ has two vertices. The gluing maps of $\mathbf{E}(X)$ are essential.

    > Reference: [Leinster §6.2](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Defining the limit functor on objects only.** Writing "let $L(A) = \lim D_A$" and then treating $L$ as a functor. *Diagnosis:* a functor needs an action on maps, and here that action exists only because a certain family is a cone (Stage 1). Until $(\star)$ is established there is nothing to be natural with respect to.
    2. **Proving naturality by chasing elements of $L(A)$.** *Diagnosis:* $\mathcal{S}$ is an arbitrary category, so $L(A)$ has no elements. The replacement for "two functions agree on every element" is "two maps into a limit agree after every projection".
    3. **Reversing the arrows of $\mathbf{E}(X)$.** Writing the condition as $(Xf)(x') = x$ for $f \colon A' \to A$. *Diagnosis:* $Xf$ has domain $X(A)$, so it cannot be applied to $x' \in X(A')$. Write down the domain and codomain of $Xf$ before writing the condition.
    4. **Defining $\theta$ and forgetting to prove it natural.** In the density theorem, $\theta_A(x) = y_{(A,x)}$ is a family of functions; it becomes a map of presheaves only after Stage 3. *Diagnosis:* a universal property in a functor category asks for a natural transformation, and naturality is where the cocone condition gets used. If your proof never uses the cocone condition, it is incomplete.
    5. **Assuming the Yoneda embedding preserves colimits.** *Diagnosis:* it preserves limits (Theorem 2) and, as the example of $H_0$ shows, not even initial objects among colimits.

    ---

    ## Why This Matters

    - **5C** used "limits in functor categories are pointwise" without proof; that debt is now paid, and with it the fact that $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is complete and cocomplete.
    - **6C** states that presheaf categories are cartesian closed. The construction of the exponential there is a density argument: decide what the answer must be on representables, then extend.
    - **6C**'s adjoint functor theorems need complete categories to work in; presheaf categories are the standard supply.
    - **6D** works in $[\mathcal{A}, \mathcal{A}]$, where the monad axioms are equations between natural transformations, checked one component at a time just as in Stage 3 of Theorem 1.
    - **7A** lists the density theorem as the reason presheaf categories are described as obtained from $\mathcal{A}$ by "freely adding colimits".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Each cell runs as shipped. Replace the `...` placeholders, then uncomment the `print` checks.

    A presheaf `X` on a finite category `cat` is encoded as `{"objects": {A: list of elements of X(A)}, "arrows": {f: dict}}`, where for `f : A' -> A` the dict `X["arrows"][f]` is the function $X(f) \colon X(A) \to X(A')$.

    ### Exercise 1: Build the category of elements, and look for a terminal object

    Fill in (a) the condition for `f` to be a map $(A', x') \to (A, x)$, and (b) the search for a terminal object of $\mathbf{E}(X)$: an object that receives exactly one arrow from every object.
    """)
    return


@app.cell
def _():
    def _run():
        cat = {
            "objects": ["V", "E"],
            "arrows": {"1V": ("V", "V"), "1E": ("E", "E"), "s": ("V", "E"), "t": ("V", "E")},
            "identity": {"V": "1V", "E": "1E"},
            "compose": {
                ("1V", "1V"): "1V", ("1E", "1E"): "1E",
                ("s", "1V"): "s", ("t", "1V"): "t", ("1E", "s"): "s", ("1E", "t"): "t",
            },
        }

        def graph_presheaf(vertices, edges):
            """edges: {name: (source, target)}"""
            return {
                "objects": {"V": list(vertices), "E": list(edges)},
                "arrows": {
                    "1V": {v: v for v in vertices},
                    "1E": {e: e for e in edges},
                    "s": {e: edges[e][0] for e in edges},
                    "t": {e: edges[e][1] for e in edges},
                },
            }

        path = graph_presheaf(["a", "b", "c"], {"p": ("a", "b"), "q": ("b", "c")})
        loop = graph_presheaf(["v"], {"l": ("v", "v")})
        H_E = graph_presheaf(["s", "t"], {"1E": ("s", "t")})

        def category_of_elements(cat, X):
            objects = [(A, x) for A in cat["objects"] for x in X["objects"][A]]
            arrows = []
            for f, (A2, A) in cat["arrows"].items():          # f : A2 -> A in cat
                for x in X["objects"][A]:
                    for x2 in X["objects"][A2]:
                        # TODO (a): is f a map (A2, x2) -> (A, x) of E(X)?
                        is_map = ...
                        if is_map is True:
                            arrows.append((f, (A2, x2), (A, x)))
            return objects, arrows

        def terminal_object(objects, arrows):
            # TODO (b): return an object receiving exactly one arrow from every object, or None.
            return ...

        # for X in (path, loop, H_E):
        #     objs, arrs = category_of_elements(cat, X)
        #     print(len(objs), len(arrs), terminal_object(objs, arrs))
        # expect:
        #   5 9 None
        #   2 4 None
        #   3 5 ('E', '1E')

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: A pointwise product of presheaves

    Build the product $X \times Y$ of two presheaves on the same finite category, following Theorem 1: the value at each object is the product of the values, and the action on arrows is the one forced by equation $(\star)$.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def graph_presheaf(vertices, edges):
            return {
                "objects": {"V": list(vertices), "E": list(edges)},
                "arrows": {
                    "1V": {v: v for v in vertices},
                    "1E": {e: e for e in edges},
                    "s": {e: edges[e][0] for e in edges},
                    "t": {e: edges[e][1] for e in edges},
                },
            }

        path = graph_presheaf(["a", "b", "c"], {"p": ("a", "b"), "q": ("b", "c")})
        loop = graph_presheaf(["v"], {"l": ("v", "v")})
        arrow_ends = {"1V": ("V", "V"), "1E": ("E", "E"), "s": ("V", "E"), "t": ("V", "E")}

        def product_presheaf(X, Y):
            objects = {A: list(itertools.product(X["objects"][A], Y["objects"][A])) for A in X["objects"]}
            arrows = {}
            for f, (A2, A) in arrow_ends.items():
                # TODO: the function (X x Y)(f) : (X x Y)(A) -> (X x Y)(A2), as a dict on pairs.
                arrows[f] = ...
            return {"objects": objects, "arrows": arrows}

        PP = product_presheaf(path, path)
        PL = product_presheaf(path, loop)
        # print(len(PP["objects"]["V"]), len(PP["objects"]["E"]))   # expect 9 4
        # print(len(PL["objects"]["V"]), len(PL["objects"]["E"]))   # expect 3 2
        # print(PP["arrows"]["s"][("p", "q")], PP["arrows"]["t"][("p", "q")])   # expect ('a', 'b') ('b', 'c')

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Check the density theorem by counting

    Since colimits of presheaves are pointwise, Theorem 3 says that for each object $B$ the set $X(B)$ is the colimit in $\mathbf{Set}$ of the sets $\mathcal{A}(B, A)$, one for each object $(A, x)$ of $\mathbf{E}(X)$. By the formula of 5B that colimit is the set of all triples $(A, x, g)$ with $g \colon B \to A$, modulo the equivalence relation generated by
    $$(A', x', g) \sim (A, x, f \circ g) \quad\text{for each map } f \colon (A', x') \to (A, x) \text{ of } \mathbf{E}(X).$$
    The category of elements of the path graph is written out for you. Fill in the merging step and count the classes.
    """)
    return


@app.cell
def _():
    def _run():
        hom = {("V", "V"): ["1V"], ("E", "E"): ["1E"], ("V", "E"): ["s", "t"], ("E", "V"): []}
        compose = {
            ("1V", "1V"): "1V", ("1E", "1E"): "1E",
            ("s", "1V"): "s", ("t", "1V"): "t", ("1E", "s"): "s", ("1E", "t"): "t",
        }
        X_sizes = {"V": 3, "E": 2}

        # E(X) for the path a -p-> b -q-> c: objects, and arrows as (f, domain, codomain)
        el_objects = [("V", "a"), ("V", "b"), ("V", "c"), ("E", "p"), ("E", "q")]
        el_arrows = [("1V", o, o) for o in el_objects[:3]] + [("1E", o, o) for o in el_objects[3:]] + [
            ("s", ("V", "a"), ("E", "p")), ("t", ("V", "b"), ("E", "p")),
            ("s", ("V", "b"), ("E", "q")), ("t", ("V", "c"), ("E", "q")),
        ]

        def colimit_size(B):
            triples = [(A, x, g) for (A, x) in el_objects for g in hom[(B, A)]]
            parent = {tr: tr for tr in triples}

            def find(tr):
                while parent[tr] != tr:
                    tr = parent[tr]
                return tr

            def union(tr1, tr2):
                parent[find(tr1)] = find(tr2)

            for f, (A2, x2), (A, x) in el_arrows:
                for g in hom[(B, A2)]:
                    # TODO: merge the class of (A2, x2, g) with the class of the triple it is related to.
                    pass
            return len({find(tr) for tr in triples})

        # print(colimit_size("V"), X_sizes["V"])   # expect 3 3
        # print(colimit_size("E"), X_sizes["E"])   # expect 2 2

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | `exercises/6b/p01_category_of_elements_is_a_category.md` | warm-up | verifying axioms |
    | 2 | `exercises/6b/p02_elements_of_a_representable.md` | warm-up | unpacking a definition |
    | 3 | `exercises/6b/p03_monics_of_presheaves_are_pointwise.md` | core | pointwise argument |
    | 4 | `exercises/6b/p04_representable_iff_terminal_element.md` | core | re-expressing a universal property |
    | 5 | `exercises/6b/p05_agreeing_on_representables.md` | core | using density |
    | 6 | `exercises/6b/p06_products_of_representables.md` | stretch | Yoneda-style proof |

    Write each proof in `proofs/6b/<same filename>`, using the Goal / Given / Plan / Proof / What made it work layout.
    Then ask Claude to review it; the review points at gaps and asks questions, it does not rewrite your proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [6A: Limits via Representables & Adjoints](../6a_limits_representables_adjoints/) | Next: [6C: Adjoints & Limits](../6c_adjoints_and_limits/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
