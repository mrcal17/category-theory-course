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
    # 6C: Adjoints & Limits

    > *Right adjoints preserve limits. And, when the sizes allow it, a functor that preserves limits is a right adjoint.*
    > — the two halves of this module

    6A showed that limits can be described by an adjunction. This module looks at how an *arbitrary* adjunction $F \dashv G$ interacts with limits, and the answer is the most frequently used theorem in category theory: **a right adjoint preserves every limit, and a left adjoint preserves every colimit.** The proof is three lines long once the right language is in place, and part of the work here is to see exactly why those three lines are a complete proof.

    The theorem is useful in both directions. Forwards, it tells you what limits in $\mathbf{Grp}$ or $\mathbf{Top}$ must look like before you construct them. Backwards, it is the quickest way to show that a functor has *no* adjoint: find one limit it fails to preserve.

    That raises the converse question. If $G$ preserves all limits, must it have a left adjoint? In a poset the answer is yes whenever the domain has all meets, and you will prove that in full: it is short, and it contains the whole idea. In general the answer is "yes, given a size condition", and the precise statements are the **general** and **special adjoint functor theorems**, which are stated here with every hypothesis and without proof. The module ends with **cartesian closed categories**, where the adjunction in question is between products and function objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Right Adjoints Preserve Limits: the Short Proof

    Fix an adjunction $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$, as always in this course. Write $\bar{g} \colon A \to G(B)$ for the transpose of $g \colon F(A) \to B$, and also $\bar{f} \colon F(A) \to B$ for the transpose of $f \colon A \to G(B)$, so that $\bar{\bar{f}} = f$.

    > **Theorem 1.** Let $F \dashv G$ be an adjunction between locally small categories, $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$. Then $G$ preserves limits: if $(p_I \colon L \to D(I))_{I}$ is a limit cone on a diagram $D \colon \mathbf{I} \to \mathcal{B}$, then $(G p_I \colon G(L) \to G D(I))_{I}$ is a limit cone on $G \circ D$. Dually, $F$ preserves colimits.

    The standing hypotheses are the ones inherited from 6A, Theorem 1, on which the proof rests: $\mathcal{A}$ and $\mathcal{B}$ are locally small and $\mathbf{I}$ is small, so that the hom-sets and sets of cones below really are sets. Nothing is assumed about which limits exist.

    Here is the argument as it is usually written. For each object $A$ of $\mathcal{A}$,

    $$\mathcal{A}(A, G(L)) \;\cong\; \mathcal{B}(F(A), L) \;\cong\; \mathrm{Cone}(F(A), D) \;\cong\; \mathrm{Cone}(A, G \circ D),$$

    naturally in $A$. The first step is the adjunction. The second is 6A, Theorem 1(a): $L$ represents the cone functor of $D$. The third is the adjunction again, applied to each component of a cone. So $G(L)$ represents $\mathrm{Cone}(-, G \circ D)$, and by 6A, Theorem 1(b), $G(L)$ is a limit of $G \circ D$.

    **Why is that a legitimate proof?** Three things have to be true for the chain to prove the theorem as stated, and none of them is automatic.

    1. *The third step must make sense.* Transposing each $f_I$ in a cone gives a family of maps; you must check that the result is again a cone.
    2. *The conclusion must be about the right cone.* 6A, Theorem 1(b) says the limit cone is the image of the identity $1_{G(L)}$ under the composite bijection. "Preserves limits" requires that image to be exactly $(G p_I)_I$, not merely some limit cone with vertex $G(L)$.
    3. *Nothing may be assumed to exist.* The chain never mentions $\lim (G \circ D)$. It shows that a certain functor is representable, and representability is what *produces* the limit. A version of the argument that began "$\mathcal{A}(A, \lim G D) \cong \ldots$" would be assuming the conclusion.

    Section 2 carries out checks 1 and 2 explicitly. Once you have seen them done, you are entitled to use chains like this one, provided you can say what each isomorphism does to an element.

    > Reference: [Leinster §6.3](https://arxiv.org/abs/1612.09375); [Riehl §4.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "A": (0, 1.8, r"$A$"),
            "GL": (0, 0, r"$G(L)$"),
            "GD": (2.2, 0, r"$GD(I)$"),
            "FA": (4.4, 1.8, r"$F(A)$"),
            "L": (4.4, 0, r"$L$"),
            "D": (6.6, 0, r"$D(I)$"),
        },
        [
            ("A", "GL", r"$f$", {"side": -1}),
            ("GL", "GD", r"$G p_I$", {"side": -1}),
            ("A", "GD", r"$f_I$"),
            ("FA", "L", r"$\bar{f}$", {"side": -1}),
            ("L", "D", r"$p_I$", {"side": -1}),
            ("FA", "D", r"$\bar{f}_I$"),
        ],
        figsize=(8.0, 3.2),
        title="A triangle in A (left) and its transpose in B (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Making the Short Proof Honest

    One fact from 2A does all the work: **naturality of transposition in $B$** (equation (N1) there). For $g \colon F(A) \to B$ and $q \colon B \to B'$,

    $$\overline{q \circ g} \;=\; G(q) \circ \bar{g}. \tag{N}$$

    In words: composing with $q$ after $g$ on the $\mathcal{B}$ side corresponds to composing with $G(q)$ after $\bar{g}$ on the $\mathcal{A}$ side.

    > **Lemma 1 (transposing cones).** Let $F \dashv G$ and let $D \colon \mathbf{I} \to \mathcal{B}$ be a diagram. A family $(f_I \colon A \to G D(I))_I$ is a cone on $G \circ D$ if and only if the family of transposes $(\bar{f}_I \colon F(A) \to D(I))_I$ is a cone on $D$. Consequently $(f_I)_I \mapsto (\bar{f}_I)_I$ is a bijection $\mathrm{Cone}(A, G \circ D) \to \mathrm{Cone}(F(A), D)$.

    - **Goal.** For every $u \colon I \to J$ in $\mathbf{I}$: $G(Du) \circ f_I = f_J$ if and only if $Du \circ \bar{f}_I = \bar{f}_J$.
    - **Given.** Transposition is a bijection $\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$ for each $B$; equation (N).
    - **Plan.** Direct: transpose one of the two equations and recognise the other.
    - **Proof.** Fix $u \colon I \to J$. Apply (N) with $g = \bar{f}_I$ and $q = Du$: $\overline{Du \circ \bar{f}_I} = G(Du) \circ \bar{\bar{f}}_I = G(Du) \circ f_I$. Also $\overline{\bar{f}_J} = f_J$. Because transposition is injective, $Du \circ \bar{f}_I = \bar{f}_J$ holds exactly when the transposes of the two sides are equal, that is, when $G(Du) \circ f_I = f_J$. For the last sentence of the lemma: transposition is a bijection on each component, and we have just shown it matches cones with cones in both directions. $\blacksquare$
    - **What made it work.** An equation between maps can be checked on either side of an adjunction, because transposition is a bijection, and (N) tells you what the equation looks like on the other side.

    **Proof of Theorem 1.**

    - **Goal.** For every object $A$ of $\mathcal{A}$ and every cone $(f_I \colon A \to G D(I))_I$ on $G \circ D$, there is a unique $f \colon A \to G(L)$ with $G p_I \circ f = f_I$ for all $I$. Equivalently (6A, Theorem 1): $(G p_I)_I$ is a cone, and for each $A$ the function $f \mapsto (G p_I \circ f)_I$ is a bijection $\mathcal{A}(A, G(L)) \to \mathrm{Cone}(A, G \circ D)$.
    - **Given.** $(p_I)$ is a limit cone on $D$, so $h \mapsto (p_I \circ h)_I$ is a bijection $\mathcal{B}(B, L) \to \mathrm{Cone}(B, D)$ for every $B$ (6A, Theorem 1(a)). Lemma 1. Equation (N).
    - **Plan.** Write the function $f \mapsto (G p_I \circ f)_I$ as a composite of three bijections. A composite of bijections is a bijection.
    - **Proof.** First, $(G p_I)_I$ is a cone on $G \circ D$ because functors send cones to cones: $G(Du) \circ G(p_I) = G(Du \circ p_I) = G(p_J)$.

      Fix $A$ and consider three functions:
      $$\mathcal{A}(A, G(L)) \xrightarrow{\;f \,\mapsto\, \bar{f}\;} \mathcal{B}(F(A), L) \xrightarrow{\;h \,\mapsto\, (p_I h)_I\;} \mathrm{Cone}(F(A), D) \xrightarrow{\;(k_I)_I \,\mapsto\, (\bar{k}_I)_I\;} \mathrm{Cone}(A, G \circ D).$$
      The first is a bijection because $F \dashv G$. The second is a bijection because $(p_I)$ is a limit cone. The third is a bijection by Lemma 1 (it is the inverse of the bijection there). So the composite is a bijection.

      Now compute the composite on $f \colon A \to G(L)$. It sends $f$ to the family with $I$-component $\overline{p_I \circ \bar{f}}$. By (N) with $g = \bar{f}$ and $q = p_I$, this is $G(p_I) \circ \bar{\bar{f}} = G(p_I) \circ f$. So the composite is the function $f \mapsto (G p_I \circ f)_I$, which is therefore a bijection. Surjectivity gives the existence of a mediating map for each cone and injectivity gives its uniqueness. $\blacksquare$
    - **What made it work.** The chain of isomorphisms of Section 1 was correct; what turns it into a proof is *following an element through it*. Following $f$ shows the composite is "compose with $G p_I$", and that settles which cone is the limit cone.

    The statement for colimits needs no new proof. $F \dashv G$ gives an adjunction $G^{\mathrm{op}} \dashv F^{\mathrm{op}}$ between the opposite categories, so $F^{\mathrm{op}}$ is a right adjoint and preserves limits, and a limit in $\mathcal{B}^{\mathrm{op}}$ is a colimit in $\mathcal{B}$.

    $$\boxed{\;\text{Right adjoints preserve limits;\quad left adjoints preserve colimits.}\;}$$

    > Reference: [Leinster §6.3](https://arxiv.org/abs/1612.09375); [Riehl §4.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Using the Theorem in Both Directions

    **Forwards: what limits must look like.**

    - *Forgetful functors.* $U \colon \mathbf{Grp} \to \mathbf{Set}$ has a left adjoint (the free group functor), so it preserves limits. Before you construct the product of two groups you already know its underlying set: it has to be the product of the underlying sets. The same holds for $\mathbf{Mon}$, $\mathbf{Ab}$, $\mathbf{Vect}_k$, and for equalizers and pullbacks.
    - *Topological spaces.* $U \colon \mathbf{Top} \to \mathbf{Set}$ has a left adjoint (discrete spaces) and a right adjoint (indiscrete spaces), by 2A. So $U$ preserves limits *and* colimits: the points of a product space are tuples of points, and the points of a sum or of a quotient space are what they are in $\mathbf{Set}$.
    - *Free functors.* $F \colon \mathbf{Set} \to \mathbf{Grp}$ is a left adjoint, so it preserves colimits: the free group on a disjoint union $X + Y$ is the sum in $\mathbf{Grp}$ (the free product) of the free groups on $X$ and on $Y$, and the free group on $\emptyset$ is the initial group, the one-element group.
    - *Products with a fixed set.* $- \times B \colon \mathbf{Set} \to \mathbf{Set}$ is left adjoint to $(-)^B$ (2A), so $(X + Y) \times B \cong (X \times B) + (Y \times B)$. The distributive law of arithmetic is an instance of "left adjoints preserve colimits".
    - *Images and preimages.* For a function $f \colon X \to Y$, direct image $f_* \colon \mathscr{P}(X) \to \mathscr{P}(Y)$ is left adjoint to inverse image $f^{-1} \colon \mathscr{P}(Y) \to \mathscr{P}(X)$, since $f_*(S) \subseteq T$ if and only if $S \subseteq f^{-1}(T)$. So $f_*$ preserves unions (joins) and $f^{-1}$ preserves intersections (meets). In fact $f^{-1}$ also has a right adjoint, so it preserves unions too.

    **Backwards: ruling out adjoints.** The contrapositive of Theorem 1 says: a functor that fails to preserve some limit has no left adjoint, and one that fails to preserve some colimit has no right adjoint.

    - *$U \colon \mathbf{Grp} \to \mathbf{Set}$ has no right adjoint.* The initial object of $\mathbf{Grp}$ is the one-element group, whose underlying set has one element; the initial object of $\mathbf{Set}$ is empty. $U$ does not preserve the initial object, which is the colimit of the empty diagram.
    - *Direct image has no left adjoint in general.* For $f \colon \{0, 1\} \to \{0\}$, $f_*(\{0\} \cap \{1\}) = \emptyset$ but $f_*\{0\} \cap f_*\{1\} = \{0\}$. So $f_*$ does not preserve binary meets and cannot be a right adjoint.
    - *The discrete-space functor $\mathbf{Set} \to \mathbf{Top}$ has no left adjoint.* An infinite product of two-point discrete spaces is not discrete, so this functor does not preserve infinite products.

    **Non-example of the method.** Preserving *some* limits proves nothing. The discrete-space functor preserves all finite products and still has no left adjoint. To conclude that an adjoint exists you need a theorem that runs the other way, which is the subject of the rest of this module.

    > Reference: [Leinster §6.3](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        # f : X -> Y a function between finite sets; direct image and inverse image on subsets.
        _X, _Y = [0, 1, 2], ["u", "v"]
        _f = {0: "u", 1: "u", 2: "v"}

        def _subsets(_xs):
            return [frozenset(_c) for _r in range(len(_xs) + 1) for _c in itertools.combinations(_xs, _r)]

        def _direct(_S):
            return frozenset(_f[_x] for _x in _S)

        def _inverse(_T):
            return frozenset(_x for _x in _X if _f[_x] in _T)

        _PX, _PY = _subsets(_X), _subsets(_Y)
        _adj = all((_direct(_S) <= _T) == (_S <= _inverse(_T)) for _S in _PX for _T in _PY)
        _direct_joins = all(_direct(_S | _S2) == _direct(_S) | _direct(_S2) for _S in _PX for _S2 in _PX)
        _direct_meets = all(_direct(_S & _S2) == _direct(_S) & _direct(_S2) for _S in _PX for _S2 in _PX)
        _inverse_meets = all(_inverse(_T & _T2) == _inverse(_T) & _inverse(_T2) for _T in _PY for _T2 in _PY)
        print("f : {0,1,2} -> {u,v},  f(0) = f(1) = u,  f(2) = v")
        print("direct image is left adjoint to inverse image:", _adj)
        print("direct image preserves binary joins (unions):  ", _direct_joins)
        print("inverse image preserves binary meets:          ", _inverse_meets)
        print("direct image preserves binary meets:           ", _direct_meets, " <- a left adjoint need not")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Converse in a Poset: an Adjoint Functor Theorem You Can Prove

    Does every limit-preserving functor have a left adjoint? Start where the question is cleanest. A poset is a category in which each hom-set has at most one element; a functor between posets is an order-preserving map; limits are meets (5A); and an adjunction $F \dashv G$ between posets $A$ and $B$ is a pair of order-preserving maps $F \colon A \to B$, $G \colon B \to A$ with

    $$F(a) \le b \iff a \le G(b) \qquad \text{for all } a \in A,\ b \in B$$

    (a Galois connection, 2A).

    > **Definition.** A poset $B$ is **complete** if every subset $S \subseteq B$ has a meet $\bigwedge S$. An order-preserving map $G \colon B \to A$ **preserves meets** if for every $S \subseteq B$ the element $G(\bigwedge S)$ is a meet of $\{G(s) : s \in S\}$ in $A$.

    **Reading the definition.**

    - "Every subset" includes the empty subset. Every element is a lower bound of $\emptyset$, so $\bigwedge \emptyset$ is the greatest element $\top$ of $B$. Preserving the empty meet means $G(\top_B)$ is the greatest element of $A$.
    - "Every subset" includes infinite subsets. A poset regarded as a category is small, so its small limits are meets of arbitrary subsets.
    - Preserving meets asks that $G(\bigwedge S)$ *be* a greatest lower bound in $A$; the existence of that meet in $A$ is part of the conclusion, not an assumption on $A$.

    **Examples.** The power set $\mathscr{P}(X)$ with $\bigwedge = \bigcap$; the divisors of $12$ with $\bigwedge = \gcd$; the closed interval $[0, 1]$ with $\bigwedge = \inf$. **Non-examples.** $\mathbb{N}$ with its usual order has no greatest element, so $\bigwedge \emptyset$ does not exist. $\mathbb{Q} \cap [0, 2]$ is not complete: $\{q : q^2 > 2\}$ has no greatest lower bound in it.

    > **Theorem 2 (adjoint functor theorem for posets).** Let $A$ be a poset, $B$ a complete poset and $G \colon B \to A$ an order-preserving map. Then
    > $$G \text{ has a left adjoint} \iff G \text{ preserves meets.}$$
    > When it exists, the left adjoint is given by $F(a) = \bigwedge \{ b \in B : a \le G(b) \}$.

    **Proof of "$\Rightarrow$".**

    - **Goal.** If $F \dashv G$ then for every $S \subseteq B$: (i) $G(\bigwedge S) \le G(s)$ for all $s \in S$; (ii) if $a \in A$ satisfies $a \le G(s)$ for all $s \in S$ then $a \le G(\bigwedge S)$.
    - **Given.** $F(a) \le b \iff a \le G(b)$; $G$ order-preserving; the definition of $\bigwedge S$.
    - **Plan.** This is Theorem 1 for posets. Run its proof directly: move the question across the adjunction, use the universal property of the meet in $B$, move back.
    - **Proof.** (i) $\bigwedge S \le s$ for each $s \in S$, and $G$ is order-preserving. (ii) Suppose $a \le G(s)$ for all $s \in S$. By the adjunction, $F(a) \le s$ for all $s \in S$. So $F(a)$ is a lower bound of $S$, hence $F(a) \le \bigwedge S$. By the adjunction again, $a \le G(\bigwedge S)$. $\blacksquare$
    - **What made it work.** The three steps "across, universal property, back" are the three isomorphisms of Section 1, with "is a bijection" replaced by "if and only if".

    **Proof of "$\Leftarrow$".**

    - **Goal.** Assuming $G$ preserves meets, define $F \colon A \to B$ and show (i) $F(a) \le b \iff a \le G(b)$ for all $a, b$, and (ii) $F$ is order-preserving.
    - **Given.** $B$ is complete; $G$ is order-preserving and preserves meets.
    - **Plan.** $F(a)$ should be the least $b$ with $a \le G(b)$. Take the meet of all such $b$, and use preservation of meets to show that this meet is itself one of them.
    - **Proof.** For $a \in A$ let $U_a = \{ b \in B : a \le G(b) \}$ and define $F(a) = \bigwedge U_a$, which exists because $B$ is complete.

      *Key step: $a \le G(F(a))$.* Since $G$ preserves meets, $G(F(a)) = G(\bigwedge U_a)$ is the greatest lower bound in $A$ of $\{G(b) : b \in U_a\}$. By the definition of $U_a$, $a$ is a lower bound of that set. So $a \le G(F(a))$.

      (i) "$\Leftarrow$": if $a \le G(b)$ then $b \in U_a$, so $F(a) = \bigwedge U_a \le b$. "$\Rightarrow$": if $F(a) \le b$ then $G(F(a)) \le G(b)$ because $G$ is order-preserving, and with the key step, $a \le G(F(a)) \le G(b)$.

      (ii) Let $a \le a'$. By the key step $a' \le G(F(a'))$, so $a \le G(F(a'))$, and by (i) "$\Leftarrow$", $F(a) \le F(a')$. $\blacksquare$
    - **What made it work.** $U_a$ is the comma category $(a \Rightarrow G)$ of 2C, and a left adjoint exists exactly when each such category has an initial object, here a least element. The least element of a subset of a complete poset is found by taking the meet of the whole subset and proving the meet lies in it. Preservation of meets is precisely what puts it there.

    The widget lets you watch the construction succeed and fail. Choose a map $G$; the table shows $U_a$, the candidate $F(a) = \bigwedge U_a$ and whether the key step $a \le G(F(a))$ holds.
    """)
    return


@app.cell
def _(mo):
    aft_pick = mo.ui.dropdown(
        options=[
            "1. chain 0..5 -> chain 0..3,  G = (0,1,1,2,2,3)",
            "2. subsets of {1,2,3} -> subsets of {1,2},  G(S) = S ∩ {1,2}",
            "3. subsets of {1,2} -> chain 0..2,  G(S) = |S|",
            "4. chain 0..3 -> chain 0..3,  G(b) = min(b, 2)",
        ],
        value="1. chain 0..5 -> chain 0..3,  G = (0,1,1,2,2,3)",
        label="Order-preserving map G : B -> A",
    )
    aft_pick
    return (aft_pick,)


@app.cell
def _(aft_pick, mo):
    def _run():
        import itertools

        def _subsets(_xs):
            return [frozenset(_c) for _r in range(len(_xs) + 1) for _c in itertools.combinations(_xs, _r)]

        def _show(_x):
            if isinstance(_x, frozenset):
                return "{" + ",".join(str(_i) for _i in sorted(_x)) + "}"
            return "none" if _x is None else str(_x)

        def _leq(_x, _y):
            return _x <= _y

        def _glb(_S, _elems):
            _lower = [_x for _x in _elems if all(_leq(_x, _s) for _s in _S)]
            _best = [_x for _x in _lower if all(_leq(_y, _x) for _y in _lower)]
            return _best[0] if _best else None

        _key = aft_pick.value[0]
        if _key == "1":
            _B, _A = list(range(6)), list(range(4))
            _G = dict(zip(_B, [0, 1, 1, 2, 2, 3]))
        elif _key == "2":
            _B, _A = _subsets([1, 2, 3]), _subsets([1, 2])
            _G = {_S: _S & frozenset([1, 2]) for _S in _B}
        elif _key == "3":
            _B, _A = _subsets([1, 2]), [0, 1, 2]
            _G = {_S: len(_S) for _S in _B}
        else:
            _B, _A = list(range(4)), list(range(4))
            _G = {_b: min(_b, 2) for _b in _B}

        _F = {}
        _rows = ["| $a$ | $U_a = \\{b : a \\le G(b)\\}$ | $F(a) = \\bigwedge U_a$ | $G(F(a))$ | key step $a \\le G(F(a))$ |", "|---|---|---|---|---|"]
        for _a in _A:
            _U = [_b for _b in _B if _leq(_a, _G[_b])]
            _F[_a] = _glb(_U, _B)
            _key_ok = _leq(_a, _G[_F[_a]])
            _rows.append(
                f"| {_show(_a)} | {', '.join(_show(_b) for _b in _U) or 'empty'} | {_show(_F[_a])} | {_show(_G[_F[_a]])} | {'yes' if _key_ok else '**no**'} |"
            )

        _bad_meets = [
            _S for _S in _subsets(_B)
            if _G[_glb(_S, _B)] != _glb([_G[_s] for _s in _S], _A)
        ]
        _pairs = [(_a, _b) for _a in _A for _b in _B]
        _fail = [(_a, _b) for (_a, _b) in _pairs if _leq(_F[_a], _b) != _leq(_a, _G[_b])]
        _rows.append("")
        if _bad_meets:
            _S = min(_bad_meets, key=len)
            _rows.append(
                f"**$G$ does not preserve meets.** For example let $S$ consist of: "
                f"{', '.join(_show(_s) for _s in sorted(_S, key=_show)) or 'nothing at all (the empty subset)'}. Then "
                f"$G(\\bigwedge S) = $ {_show(_G[_glb(_S, _B)])} but $\\bigwedge G(S) = $ {_show(_glb([_G[_s] for _s in _S], _A))}."
            )
        else:
            _rows.append(f"**$G$ preserves all meets** (checked on all {len(_subsets(_B))} subsets of $B$, including the empty one).")
        _rows.append("")
        if _fail:
            _a, _b = _fail[0]
            _rows.append(
                f"**$F$ is not a left adjoint:** $F(a) \\le b \\iff a \\le G(b)$ fails for {len(_fail)} of {len(_pairs)} pairs, "
                f"for example $a = $ {_show(_a)}, $b = $ {_show(_b)}."
            )
        else:
            _rows.append(f"**$F \\dashv G$:** $F(a) \\le b \\iff a \\le G(b)$ holds for all {len(_pairs)} pairs $(a, b)$.")
        return mo.md("\n".join(_rows))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In preset 3 the map $G(S) = |S|$ is order-preserving and sends the greatest element to the greatest element, but it does not preserve the meet of $\{1\}$ and $\{2\}$, and the key step fails at $a = 1$. In preset 4 every non-empty meet is preserved and the only failure is the empty meet, $G(\top) \ne \top$; that alone is enough to destroy the adjoint. The empty case is part of the hypothesis and it matters.

    > Reference: [Leinster §6.3](https://arxiv.org/abs/1612.09375) (adjoint functor theorems, beginning with ordered sets).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The General Adjoint Functor Theorem

    Try to repeat the proof of Theorem 2 for a functor $G \colon \mathcal{B} \to \mathcal{A}$ between arbitrary categories. By 2C, $G$ has a left adjoint if and only if, for each object $A$, the comma category $(A \Rightarrow G)$ has an initial object. Its objects are pairs $(B, f \colon A \to G(B))$; it is the analogue of $U_a$. The poset proof found the least element of $U_a$ as the meet of *all* of $U_a$. The analogue would be a limit, in $\mathcal{B}$, of a diagram indexed by *all* of $(A \Rightarrow G)$.

    That is where the argument breaks. "Complete" means having limits of all **small** diagrams (5A), and $(A \Rightarrow G)$ is usually not small: for the forgetful functor $\mathbf{Grp} \to \mathbf{Set}$ it contains every group equipped with a function from $A$. In a poset the problem cannot arise, because the poset is itself a set. In general an extra hypothesis is needed, one saying that a mere *set* of objects of $(A \Rightarrow G)$ is enough to reach all the others.

    > **Definition.** A **weakly initial set** in a category $\mathcal{C}$ is a set $\mathcal{S}$ of objects of $\mathcal{C}$ such that for every object $C$ of $\mathcal{C}$ there is at least one map $S \to C$ with $S \in \mathcal{S}$.

    **Reading the definition.**

    - $\mathcal{S}$ must be a *set*, not a proper class. Without that word the condition is empty: the class of all objects always qualifies.
    - "At least one map": no uniqueness is asked, and different $C$ may need different $S$. An initial object is the case where $\mathcal{S}$ has one member and the map is unique.
    - For $\mathcal{C} = (A \Rightarrow G)$ it unpacks to the **solution set condition**: there is a set of pairs $(B_i, f_i \colon A \to G(B_i))_{i \in X}$ such that every $f \colon A \to G(B)$ can be written as $f = G(q) \circ f_i$ for some $i \in X$ and some $q \colon B_i \to B$.

    > **Theorem 3 (General Adjoint Functor Theorem).** Let $\mathcal{A}$ be a category, $\mathcal{B}$ a category that is complete and locally small, and $G \colon \mathcal{B} \to \mathcal{A}$ a functor. Suppose that for each object $A$ of $\mathcal{A}$ the comma category $(A \Rightarrow G)$ has a weakly initial set. Then
    > $$G \text{ has a left adjoint} \iff G \text{ preserves limits.}$$

    Here "complete" means that $\mathcal{B}$ has limits of all small diagrams, and "preserves limits" refers to those same small limits. The direction "$\Rightarrow$" is Theorem 1 and uses none of the hypotheses. The direction "$\Leftarrow$" uses all of them, and is not proved in this course; the proof is in Leinster's Appendix A. Its outline is the poset proof with one extra step:

    1. because $\mathcal{B}$ is complete and $G$ preserves limits, each $(A \Rightarrow G)$ is complete;
    2. a complete, locally small category with a weakly initial set has an initial object (built from the product of the members of the set, cut down by an equalizer);
    3. initial objects of the categories $(A \Rightarrow G)$ assemble into a left adjoint (2C).

    **Example (free groups without words).** For $U \colon \mathbf{Grp} \to \mathbf{Set}$: $\mathbf{Grp}$ is complete and locally small and $U$ preserves limits. Given a set $A$, any function $f \colon A \to U(H)$ factors through the subgroup of $H$ generated by the image of $f$, and that subgroup has cardinality at most $\max(|A|, \aleph_0)$. Up to isomorphism there is only a set of groups of bounded cardinality, each with only a set of functions from $A$; these form a weakly initial set. Theorem 3 then gives the free group functor without ever mentioning reduced words.

    **Non-example (the size condition cannot be dropped).** Let $\mathcal{B}$ be the opposite of the ordered class of all ordinals. A small diagram in $\mathcal{B}$ involves a set of ordinals, and its limit in $\mathcal{B}$ is their supremum, which exists; so $\mathcal{B}$ is complete, and it is locally small. The unique functor $G \colon \mathcal{B} \to \mathbf{1}$ preserves limits. A left adjoint to $G$ would pick out an initial object of $\mathcal{B}$, that is, a greatest ordinal, and there is none. The hypothesis that fails is the weakly initial set: any set of ordinals has an ordinal above all its members.

    **Why the poset case needed no size condition.** In Theorem 2, $B$ is a set, so $U_a$ is a weakly initial set in itself. In fact this is the only kind of small example: a small category with all small limits is necessarily a preorder.

    > Reference: [Leinster §6.3 and Appendix A](https://arxiv.org/abs/1612.09375); [Riehl §4.6](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. The Special Adjoint Functor Theorem

    The solution set condition has to be checked separately for each functor $G$. The special adjoint functor theorem replaces it by conditions on the category $\mathcal{B}$ alone, which are checked once.

    > **Definition.** Let $\mathcal{B}$ be a category.
    >
    > - $\mathcal{B}$ is **well-powered** if for each object $B$ there is a *set* $\mathcal{M}_B$ of monics with codomain $B$ such that every monic $m \colon B' \to B$ is isomorphic to one in the set: there are $m_0 \colon B_0 \to B$ in $\mathcal{M}_B$ and an isomorphism $j \colon B' \to B_0$ with $m_0 \circ j = m$.
    > - A **coseparating set** (or cogenerating set) for $\mathcal{B}$ is a *set* $\mathcal{Q}$ of objects such that whenever $f, g \colon B \to B'$ are maps with $f \ne g$, there are $Q \in \mathcal{Q}$ and $h \colon B' \to Q$ with $h \circ f \ne h \circ g$.

    **Reading the definitions.**

    - Well-powered: "each object has only a set of subobjects". In $\mathbf{Set}$, $\mathbf{Grp}$, $\mathbf{Top}$ every monic into $B$ is isomorphic to the inclusion of a subset, subgroup, or subset with some topology, and there is only a set of those.
    - Coseparating: maps *into* the members of $\mathcal{Q}$ are enough to tell any two different parallel maps apart. Again $\mathcal{Q}$ must be a set.

    **Examples.** In $\mathbf{Set}$, the two-element set alone is coseparating: if $f(b) \ne g(b)$, a function to $2$ separating those two values does the job. In the category of compact Hausdorff spaces, the interval $[0, 1]$ alone is coseparating (this is Urysohn's lemma). **Non-example.** In $\mathbf{Set}$ the one-element set is not coseparating: all maps into it are equal after composing.

    > **Theorem 4 (Special Adjoint Functor Theorem).** Let $\mathcal{A}$ be a locally small category, and let $\mathcal{B}$ be a category that is complete, locally small and well-powered and has a coseparating set. Let $G \colon \mathcal{B} \to \mathcal{A}$ be a functor. Then
    > $$G \text{ has a left adjoint} \iff G \text{ preserves limits.}$$

    This too is stated without proof (see the references). The hypotheses on $\mathcal{B}$ are used to manufacture the weakly initial sets that Theorem 3 needs.

    **Example.** The category $\mathbf{CHaus}$ of compact Hausdorff spaces satisfies every hypothesis on $\mathcal{B}$, and the inclusion $\mathbf{CHaus} \to \mathbf{Top}$ preserves limits. Theorem 4 gives it a left adjoint, which sends a space to its Stone–Čech compactification.

    **The three theorems side by side.**

    | | hypotheses on $\mathcal{B}$ | extra hypothesis | conclusion |
    |---|---|---|---|
    | Poset (Thm 2) | complete poset | none | left adjoint $\iff$ preserves meets |
    | General (Thm 3) | complete, locally small | each $(A \Rightarrow G)$ has a weakly initial set | left adjoint $\iff$ preserves limits |
    | Special (Thm 4) | complete, locally small, well-powered, has a coseparating set | $\mathcal{A}$ locally small | left adjoint $\iff$ preserves limits |

    Each has a dual, obtained by reversing all arrows: a functor out of a *cocomplete* category has a *right* adjoint if and only if it preserves *colimits*, under the dual size conditions. For posets: an order-preserving map out of a poset with all joins has a right adjoint if and only if it preserves joins, and the right adjoint is $G(a) = \bigvee \{ b : F(b) \le a \}$.

    > Reference: [Leinster §6.3](https://arxiv.org/abs/1612.09375); [Riehl §4.6](https://math.jhu.edu/~eriehl/context.pdf) for the precise statement and proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Cartesian Closed Categories

    The adjunction $\mathbf{Set}(A \times B, C) \cong \mathbf{Set}(A, C^B)$ has been with you since 2A. A category in which this adjunction exists has "function objects", and the theorems of this module say a good deal about any such category.

    > **Definition.** A category $\mathcal{A}$ is **cartesian closed** if it has finite products and, for each object $B$, the functor $- \times B \colon \mathcal{A} \to \mathcal{A}$ has a right adjoint. The right adjoint is written $(-)^B$, and $C^B$ is called an **exponential**. So
    > $$\mathcal{A}(A \times B, C) \;\cong\; \mathcal{A}(A, C^B) \qquad\text{naturally in } A \text{ and } C.$$

    **Reading the definition.**

    - "Finite products" means binary products and a terminal object $1$ (the empty product).
    - One right adjoint is needed *for each* $B$.
    - The counit of the adjunction at $C$ is a map $\mathrm{ev} \colon C^B \times B \to C$, called evaluation. By 2B, every $g \colon A \times B \to C$ factors as $\mathrm{ev} \circ (\bar{g} \times 1_B)$ for a unique $\bar{g} \colon A \to C^B$.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "AB": (0, 1.8, r"$A \times B$"),
            "CB": (0, 0, r"$C^B \times B$"),
            "C": (3.0, 0, r"$C$"),
        },
        [
            ("AB", "CB", r"$\bar{g} \times 1_B$", {"dashed": True, "color": "#b91c1c", "side": -1}),
            ("CB", "C", r"$\mathrm{ev}$", {"side": -1}),
            ("AB", "C", r"$g$"),
        ],
        figsize=(5.2, 3.2),
        title="Every g factors through evaluation, for a unique transpose",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - $\mathbf{Set}$, with $C^B$ the set of functions $B \to C$ (3A).
    - A poset with finite meets is cartesian closed exactly when for all $b, c$ there is an element $b \Rightarrow c$ with $a \wedge b \le c \iff a \le (b \Rightarrow c)$. In a power set $\mathscr{P}(S)$, $B \Rightarrow C = (S \setminus B) \cup C$. In the poset of open sets of a topological space $S$, $U \Rightarrow W$ is the interior of $(S \setminus U) \cup W$.
    - $\mathbf{Cat}$, with $\mathcal{C}^{\mathcal{B}} = [\mathcal{B}, \mathcal{C}]$, and the presheaf category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ for any small $\mathcal{A}$ (both stated here without proof; see Leinster §6.3 for presheaves).

    To find non-examples, apply Theorem 1 to the left adjoint $- \times B$.

    > **Proposition 1.** Let $\mathcal{A}$ be cartesian closed and $B$ an object. Then $- \times B$ preserves colimits. In particular, if $\mathcal{A}$ has an initial object $0$ then $0 \times B$ is initial, so $0 \times B \cong 0$; and if a sum $X + Y$ exists then $(X + Y) \times B$, with the maps induced by the coprojections, is a sum of $X \times B$ and $Y \times B$.

    - **Goal.** For every colimit cocone in $\mathcal{A}$, its image under $- \times B$ is a colimit cocone; then read this off for the empty diagram and for a two-object discrete diagram.
    - **Given.** $- \times B \dashv (-)^B$ by the definition of cartesian closed; Theorem 1.
    - **Plan.** One line: quote Theorem 1 for the left adjoint, then specialise.
    - **Proof.** $- \times B$ is a left adjoint, so by Theorem 1 it preserves colimits. An initial object is a colimit of the empty diagram, so $0 \times B$ is a colimit of the empty diagram, that is, initial; any two initial objects are isomorphic. A sum is a colimit of a two-object discrete diagram, and the image of its cocone is the pair of maps $X \times B \to (X + Y) \times B \leftarrow Y \times B$ induced by the coprojections. $\blacksquare$
    - **What made it work.** The definition handed you a left adjoint. Whenever a definition does that, ask what the functor must therefore preserve.

    **Non-examples.**

    - *$\mathbf{Vect}_k$ is not cartesian closed.* The zero space $0$ is both initial and terminal, and the product of $0$ with $B$ is $B$ itself. If $\mathbf{Vect}_k$ were cartesian closed, Proposition 1 would give $B \cong 0 \times B \cong 0$ for every $B$, which is false for $B = k$.
    - *$\mathbf{Grp}$ is not cartesian closed*, by the same argument with the one-element group.
    - *$\mathbf{Top}$ is not cartesian closed* (stated without proof): for some spaces $B$ the functor $- \times B$ fails to preserve certain quotients.

    $\mathbf{Vect}_k$ does have a well-behaved adjunction $\mathbf{Vect}_k(A \otimes B, C) \cong \mathbf{Vect}_k(A, \mathrm{Hom}(B, C))$, but with the tensor product in place of the product. "Closed" structure is common; *cartesian* closed structure, where the product itself is the left adjoint, is special.

    > Reference: [Leinster §6.3](https://arxiv.org/abs/1612.09375) (cartesian closed categories); [Riehl §4.3](https://math.jhu.edu/~eriehl/context.pdf) for the parametrized adjunction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Assuming the limit you are trying to produce.** Starting a proof of Theorem 1 with "$\mathcal{A}(A, \lim G D) \cong \ldots$". *Diagnosis:* the theorem must show that $G \circ D$ *has* a limit, with a specific cone. Start from $\mathcal{A}(A, G(L))$ and end at $\mathrm{Cone}(A, G \circ D)$.
    2. **An isomorphism chain with no elements followed.** Concluding "so $G(L)$ is the limit" from a chain of bijections. *Diagnosis:* preservation is a statement about the cone $(G p_I)$. Follow $f$, or $1_{G(L)}$, through the chain and say where it lands.
    3. **Applying the theorem to the wrong adjoint.** "$U$ has a left adjoint, so $U$ preserves colimits." *Diagnosis:* the functor that *has a left adjoint* *is a right adjoint*, and preserves limits. Say out loud which of the two functors is on the right.
    4. **Forgetting the empty meet.** Checking that $G$ preserves binary meets and concluding it has a left adjoint. *Diagnosis:* the hypothesis is all meets, including $\bigwedge \emptyset = \top$ and infinite ones; preset 4 of the widget fails only at $\emptyset$.
    5. **Quoting an adjoint functor theorem without its size hypothesis.** "$\mathcal{B}$ is complete and $G$ preserves limits, so $G$ has a left adjoint." *Diagnosis:* the ordinals example shows this is false. You must supply a weakly initial set for each $(A \Rightarrow G)$, or verify the hypotheses of the special theorem.

    ---

    ## Why This Matters

    - **Everywhere after this:** "it is a right adjoint, so it preserves limits" is the standard first move when meeting a new functor, and "it does not preserve this colimit, so it has no right adjoint" is the standard way to stop looking.
    - **6D** studies the composite $GF$ of an adjunction. The closure operators there are exactly the composites arising from the poset adjunctions of Theorem 2, and the closed elements are found by the same "meet of everything above" formula.
    - **6A** showed $\lim$ is a right adjoint; Theorem 1 now explains why limits commute with limits (5C).
    - **6B** showed presheaf categories are complete and cocomplete; they are also cartesian closed, and Proposition 1 then says products of presheaves distribute over all colimits.
    - **7A** files the three adjoint functor theorems together with their hypotheses, since the hypotheses are what you will need to look up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Each cell runs as shipped. Replace the `...` placeholders, then uncomment the `print` checks.

    ### Exercise 1: Build a right adjoint from joins

    Dualize Theorem 2. $F \colon A \to B$ is an order-preserving map out of a finite poset $A$ with all joins. Here $A$ is the divisors of $12$ under divisibility and $B$ is the chain $0 < 1 < 2$; the least upper bound in $A$ is supplied. Implement (a) the candidate right adjoint $G(b) = \bigvee \{ a : F(a) \le b \}$, and (b) a census: `monotone_maps()` lists every order-preserving map $A \to B$, and you count how many of them have a right adjoint. By the dual of Theorem 2 that is the number of join-preserving maps, so the count tells you how rare preserving *all* joins is.
    """)
    return


@app.cell
def _():
    def _run():
        A = [1, 2, 3, 4, 6, 12]
        B = [0, 1, 2]

        def leq_A(x, y):
            return y % x == 0

        def leq_B(x, y):
            return x <= y

        F_good = {1: 0, 2: 1, 3: 0, 4: 2, 6: 1, 12: 2}   # exponent of 2 in d
        F_bad = {1: 0, 2: 1, 3: 1, 4: 2, 6: 2, 12: 2}    # number of prime factors, capped at 2

        def lub_A(S):
            upper = [x for x in A if all(leq_A(s, x) for s in S)]
            return [x for x in upper if all(leq_A(x, y) for y in upper)][0]

        def right_adjoint(F):
            # TODO (a): G[b] = join in A of all a with F[a] <= b.
            return {b: ... for b in B}

        def is_adjunction(F, G):
            return all(leq_B(F[a], b) == leq_A(a, G[b]) for a in A for b in B)

        def monotone_maps():
            import itertools

            maps = [dict(zip(A, values)) for values in itertools.product(B, repeat=len(A))]
            return [F for F in maps if all(leq_B(F[x], F[y]) for x in A for y in A if leq_A(x, y))]

        def count_left_adjoints():
            # TODO (b): how many F in monotone_maps() have a right adjoint?
            return ...

        # G = right_adjoint(F_good)
        # print(G, is_adjunction(F_good, G))                # expect {0: 3, 1: 6, 2: 12} True
        # G2 = right_adjoint(F_bad)
        # print(G2, is_adjunction(F_bad, G2))               # expect {0: 1, 1: 6, 2: 12} False
        # print(len(monotone_maps()), count_left_adjoints())   # expect 50 18

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Is this lattice cartesian closed?

    A finite lattice is cartesian closed when each $- \wedge b$ has a right adjoint $b \Rightarrow -$. By the dual of Theorem 2 the only candidate is $b \Rightarrow c = \bigvee \{ a : a \wedge b \le c \}$. Implement it and test the adjunction $a \wedge b \le c \iff a \le (b \Rightarrow c)$ on two lattices: the divisors of $12$, and the five-element lattice $M_3$ with bottom `0`, top `1` and three incomparable elements `x`, `y`, `z`.
    """)
    return


@app.cell
def _():
    def _run():
        def make_lattice(elems, leq):
            def glb(S):
                lower = [x for x in elems if all(leq(x, s) for s in S)]
                return [x for x in lower if all(leq(y, x) for y in lower)][0]

            def lub(S):
                upper = [x for x in elems if all(leq(s, x) for s in S)]
                return [x for x in upper if all(leq(x, y) for y in upper)][0]

            return {"elems": elems, "leq": leq, "glb": glb, "lub": lub}

        div12 = make_lattice([1, 2, 3, 4, 6, 12], lambda x, y: y % x == 0)
        M3 = make_lattice(["0", "x", "y", "z", "1"], lambda x, y: x == y or x == "0" or y == "1")

        def implies(lat, b, c):
            # TODO: the join of all a with (a meet b) <= c.
            return ...

        def is_cartesian_closed(lat):
            # TODO: test  leq(glb([a, b]), c) == leq(a, implies(lat, b, c))  for all a, b, c.
            return ...

        # print(implies(div12, 4, 6), implies(div12, 6, 4), implies(div12, 2, 3))   # expect 6 4 3
        # print(is_cartesian_closed(div12))                                         # expect True
        # print(implies(M3, "x", "0"), is_cartesian_closed(M3))                     # expect 1 False

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: A left adjoint preserves sums, and need not preserve products

    In finite sets, $- \times B$ is a left adjoint. Build the canonical map $(X \times B) + (Y \times B) \to (X + Y) \times B$ induced by the coprojections and check that it is a bijection, as Proposition 1 predicts. Sums are encoded with tags: an element of $X + Y$ is `("L", x)` or `("R", y)`.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        X, Y, B = ["x1", "x2"], ["y1", "y2", "y3"], ["b1", "b2"]

        def times(S, T):
            return list(itertools.product(S, T))

        def plus(S, T):
            return [("L", s) for s in S] + [("R", t) for t in T]

        domain = plus(times(X, B), times(Y, B))
        codomain = times(plus(X, Y), B)

        def canonical(element):
            tag, (v, b) = element
            # TODO: the image of ("L", (x, b)) or ("R", (y, b)) in (X + Y) x B.
            return ...

        # images = [canonical(e) for e in domain]
        # print(len(domain), len(codomain))                                        # expect 10 10
        # print(sorted(images) == sorted(codomain))                                # expect True
        # print(canonical(("R", ("y2", "b1"))))                                    # expect (('R', 'y2'), 'b1')
        # print(len(times(times(X, Y), B)), len(times(times(X, B), times(Y, B))))  # expect 12 24

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | `exercises/6c/p01_right_adjoints_preserve_monics.md` | warm-up | moving an equation across an adjunction |
    | 2 | `exercises/6c/p02_no_adjoint_by_limits.md` | warm-up | counterexample via a preservation theorem |
    | 3 | `exercises/6c/p03_distributive_complete_lattices.md` | core | applying the poset adjoint functor theorem |
    | 4 | `exercises/6c/p04_exponential_laws.md` | core | one-line Yoneda proof, made honest |
    | 5 | `exercises/6c/p05_set_op_not_cartesian_closed.md` | core | dualizing, then a preservation argument |
    | 6 | `exercises/6c/p06_limit_of_identity_is_initial.md` | stretch | uniqueness argument with a large cone |

    Write each proof in `proofs/6c/<same filename>`, using the Goal / Given / Plan / Proof / What made it work layout.
    Then ask Claude to review it; the review points at gaps and asks questions, it does not rewrite your proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [6B: Limits & Colimits of Presheaves](../6b_presheaf_limits/) | Next: [6D: Monads](../6d_monads/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
