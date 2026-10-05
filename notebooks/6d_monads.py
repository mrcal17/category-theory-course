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
    # 6D: Monads *(advanced)*

    > *A monad is what an adjunction looks like from one side.*
    > — the idea behind Riehl, Chapter 5

    This module is marked advanced. It uses 2B (units, counits and the triangle identities) and the closure operators met there, and nothing from 6A–6C. Leinster's book stops before monads, so the source here is Riehl, Chapter 5.

    Start with an adjunction $F \dashv G$, with $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$, and suppose you can only see the category $\mathcal{A}$. The category $\mathcal{B}$ is out of sight, but the adjunction leaves a trace on $\mathcal{A}$: the composite functor $T = GF \colon \mathcal{A} \to \mathcal{A}$, the unit $\eta \colon 1 \Rightarrow T$, and a map $\mu \colon TT \Rightarrow T$ built from the counit. For free monoids, $T$ sends a set to the set of words in it, $\eta$ makes a letter into a one-letter word, and $\mu$ concatenates a word of words. For a Galois connection between posets, $T$ is a closure operator. A **monad** is this trace, axiomatised.

    The question this module answers is: *how much of the adjunction can be recovered from its monad?* The answer has two parts. Every monad comes from an adjunction; in fact from two canonical ones, built on the **Eilenberg–Moore category** of algebras and the **Kleisli category**. And for the adjunctions of algebra (monoids, groups, and so on) the original category $\mathcal{B}$ is recovered exactly as the category of algebras; such functors $G$ are called **monadic**. By the end you will be able to prove that an adjunction gives a monad, that each of the two constructions gives back the monad you started with, and to work out the whole story by hand for a closure operator on a poset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Monads

    Take the free monoid adjunction $F \dashv U$ between $\mathbf{Set}$ and $\mathbf{Mon}$. The set $UF(X)$ is the set $X^*$ of finite words $x_1 x_2 \cdots x_n$ ($n \ge 0$) in the elements of $X$. Three pieces of structure on $X^*$ make sense without mentioning monoids at all:

    - a function $f \colon X \to Y$ gives a function $X^* \to Y^*$, applying $f$ to each letter;
    - each $x \in X$ is a one-letter word, giving a function $X \to X^*$;
    - a word whose letters are themselves words can be flattened by concatenation, giving a function $(X^*)^* \to X^*$.

    The definition of a monad abstracts exactly these three things, and the laws they obey.

    > **Definition (monad).** A **monad** on a category $\mathcal{A}$ is a triple $(T, \eta, \mu)$ consisting of a functor $T \colon \mathcal{A} \to \mathcal{A}$ and natural transformations
    > $$\eta \colon 1_{\mathcal{A}} \Rightarrow T \quad\text{(the unit)}, \qquad \mu \colon T \circ T \Rightarrow T \quad\text{(the multiplication)},$$
    > such that for every object $A$ of $\mathcal{A}$:
    > $$\mu_A \circ T(\mu_A) = \mu_A \circ \mu_{TA} \quad\text{(associativity, two maps } T^3A \to TA\text{)},$$
    > $$\mu_A \circ \eta_{TA} = 1_{TA} = \mu_A \circ T(\eta_A) \quad\text{(unit laws, maps } TA \to TA\text{)}.$$

    **Reading the definition.** To show $(T, \eta, \mu)$ is a monad you must check, in order:

    - $T$ is a functor from $\mathcal{A}$ to *itself*;
    - $\eta$ is natural: $T(f) \circ \eta_A = \eta_B \circ f$ for every $f \colon A \to B$;
    - $\mu$ is natural: $T(f) \circ \mu_A = \mu_B \circ T(T(f))$ for every $f \colon A \to B$;
    - associativity: from $T^3 A$ there are two ways to multiply down to $TA$, the inner two layers first ($T\mu_A$) or the outer two first ($\mu_{TA}$), and they agree;
    - the two unit laws: inserting a unit on the outside ($\eta_{TA}$) or on the inside ($T\eta_A$) and then multiplying does nothing.

    The two diagrams below are the associativity square and the unit triangles.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "T3": (0, 1.8, r"$T^3A$"),
            "T2a": (2.6, 1.8, r"$T^2A$"),
            "T2b": (0, 0, r"$T^2A$"),
            "T1": (2.6, 0, r"$TA$"),
            "L": (4.6, 1.8, r"$TA$"),
            "M": (6.8, 1.8, r"$T^2A$"),
            "R": (9.0, 1.8, r"$TA$"),
            "Bm": (6.8, 0, r"$TA$"),
        },
        [
            ("T3", "T2a", r"$T\mu_A$"),
            ("T3", "T2b", r"$\mu_{TA}$", {"side": -1}),
            ("T2a", "T1", r"$\mu_A$"),
            ("T2b", "T1", r"$\mu_A$", {"side": -1}),
            ("L", "M", r"$\eta_{TA}$"),
            ("R", "M", r"$T\eta_A$", {"side": -1}),
            ("M", "Bm", r"$\mu_A$"),
            ("L", "Bm", r"$1$", {"side": -1}),
            ("R", "Bm", r"$1$"),
        ],
        figsize=(9.6, 3.0),
        title="Monad axioms: associativity (left) and the two unit laws (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.** These four monads are the running examples of the module.

    - **The free monoid monad** on $\mathbf{Set}$. $T X = X^*$; $T f$ applies $f$ letter by letter; $\eta_X(x)$ is the one-letter word $x$; $\mu_X$ concatenates a word of words. Associativity says that a word of words of words can be flattened in either order. The unit laws say that flattening the one-letter word $(w)$, or flattening $w = x_1 \cdots x_n$ rewritten as the word of one-letter words $(x_1) \cdots (x_n)$, gives back $w$.
    - **The free group monad** on $\mathbf{Set}$. $T X$ is the set of reduced words in the letters $x$ and $x^{-1}$ for $x \in X$; $\eta_X(x)$ is the word $x$; $\mu_X$ takes a reduced word whose letters are themselves reduced words (or formal inverses of them), substitutes, and reduces.
    - **The power set monad** on $\mathbf{Set}$. $T X = \mathscr{P}(X)$, the set of subsets; $T f$ is direct image, $S \mapsto \{ f(x) : x \in S \}$; $\eta_X(x) = \{x\}$; $\mu_X \colon \mathscr{P}(\mathscr{P}(X)) \to \mathscr{P}(X)$ is union, $\mathcal{S} \mapsto \bigcup \mathcal{S}$. The axioms are brief P01. Note that this $\mathscr{P}$ is covariant; it is not the contravariant power set functor of 4A, which uses inverse images.
    - **A closure operator** on a poset $P$: an order-preserving map $T \colon P \to P$ with $p \le T(p)$ and $T(T(p)) \le T(p)$ for all $p$. Section 7 shows that this is precisely a monad on $P$ regarded as a category. Examples: the subgroup generated by a subset of a group; the closure of a subset of a topological space; the linear span of a subset of a vector space.

    There is also the **identity monad** on any category: $T = 1_{\mathcal{A}}$ with $\eta$ and $\mu$ identities.

    **Non-examples.**

    - Keep $T = \mathscr{P}$ and $\mu = \bigcup$ but put $\eta_X(x) = \emptyset$. This $\eta$ is natural, but the unit law fails: $\mu_X(\eta_{\mathscr{P}X}(S)) = \bigcup \emptyset = \emptyset$, which is not $S$ unless $S$ is empty.
    - The *interior* of a subset of a topological space is order-preserving and idempotent, but $\mathrm{int}(S) \subseteq S$, the wrong way round for a unit $S \subseteq T(S)$. Interior is not a monad on the poset of subsets.
    - A functor $F \colon \mathcal{A} \to \mathcal{B}$ between different categories cannot be a monad: $T \circ T$ would make no sense.

    > Reference: [Riehl §5.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Every Adjunction Gives a Monad

    The free monoid monad was read off an adjunction. That works for every adjunction.

    Recall from 2B: an adjunction $F \dashv G$, $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$, has a unit $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and a counit $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ satisfying the **triangle identities**
    $$\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}, \qquad G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}.$$

    > **Theorem 1.** Let $F \dashv G$ be an adjunction with unit $\eta$ and counit $\varepsilon$. Then
    > $$T = GF, \qquad \eta, \qquad \mu_A = G(\varepsilon_{F(A)}) \colon GFGF(A) \to GF(A)$$
    > is a monad on $\mathcal{A}$.

    - **Goal.** (i) $\mu$ is a natural transformation $TT \Rightarrow T$. (ii) For every $A$: $\mu_A \circ T(\mu_A) = \mu_A \circ \mu_{TA}$. (iii) For every $A$: $\mu_A \circ \eta_{TA} = 1_{TA}$ and $\mu_A \circ T(\eta_A) = 1_{TA}$.
    - **Given.** $F$, $G$ are functors; $\eta$, $\varepsilon$ are natural; the two triangle identities.
    - **Plan.** Each unit law is one triangle identity. Associativity is naturality of $\varepsilon$ at one well-chosen map, with $G$ applied.
    - **Proof.** (i) For $f \colon A \to A'$, naturality of $\varepsilon$ at $F(f)$ gives $F(f) \circ \varepsilon_{F(A)} = \varepsilon_{F(A')} \circ FGF(f)$. Applying $G$ gives $T(f) \circ \mu_A = \mu_{A'} \circ TT(f)$.

      (iii) *First unit law.* $\mu_A \circ \eta_{TA} = G(\varepsilon_{F(A)}) \circ \eta_{GF(A)}$. This is the second triangle identity at the object $B = F(A)$, so it equals $1_{GF(A)}$. *Second unit law.* $\mu_A \circ T(\eta_A) = G(\varepsilon_{F(A)}) \circ GF(\eta_A) = G\big(\varepsilon_{F(A)} \circ F(\eta_A)\big)$ because $G$ is a functor, and the first triangle identity makes this $G(1_{F(A)}) = 1_{GF(A)}$.

      (ii) Write $k = \varepsilon_{F(A)} \colon FGF(A) \to F(A)$. Naturality of $\varepsilon \colon FG \Rightarrow 1$ at the map $k$ says
      $$k \circ \varepsilon_{FGF(A)} = \varepsilon_{F(A)} \circ FG(k), \quad\text{that is,}\quad \varepsilon_{F(A)} \circ \varepsilon_{FGF(A)} = \varepsilon_{F(A)} \circ FG(\varepsilon_{F(A)}).$$
      Apply $G$ and use functoriality: $G(\varepsilon_{F(A)}) \circ G(\varepsilon_{FGF(A)}) = G(\varepsilon_{F(A)}) \circ GFG(\varepsilon_{F(A)})$. The left side is $\mu_A \circ \mu_{TA}$, since $\mu_{TA} = G(\varepsilon_{F(GF(A))})$. The right side is $\mu_A \circ T(\mu_A)$, since $T(\mu_A) = GF(G(\varepsilon_{F(A)}))$. $\blacksquare$
    - **What made it work.** Naturality of a transformation can be applied at *any* map, including a component of the transformation itself. "Naturality of $\varepsilon$ at $\varepsilon$" is the standard source of associativity-type laws.

    **Checking the examples.**

    - *Free monoids.* $\varepsilon_M \colon F U(M) \to M$ multiplies out a word of elements of $M$. So $\mu_X = U(\varepsilon_{F(X)})$ multiplies out a word of elements of the free monoid $X^*$, and multiplication in $X^*$ is concatenation. This is the $\mu$ of Section 1.
    - *Posets.* For a Galois connection, $\eta$ is the inequality $p \le GF(p)$ and $\mu$ is $GFGF(p) \le GF(p)$: 2B's proof that $GF$ is a closure operator is Theorem 1 in a poset.
    - *Discrete spaces.* For $D \dashv U$ between $\mathbf{Set}$ and $\mathbf{Top}$ ($D$ the discrete-space functor), $UD$ is the identity functor and the monad is the identity monad. Remember this one: a great deal of $\mathbf{Top}$ has left no trace.

    > Reference: [Riehl §5.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Algebras and the Eilenberg–Moore Category

    Does every monad come from an adjunction? To build one you need a second category $\mathcal{B}$, and the monad must supply it. Think about what a monoid $M$ gives you in terms of the free monoid monad: a way to *multiply out* any word of elements of $M$ to a single element, that is, a function $M^* \to M$. That is the idea of an algebra.

    > **Definition (algebra).** Let $(T, \eta, \mu)$ be a monad on $\mathcal{A}$. A **$T$-algebra** is a pair $(A, a)$ of an object $A$ of $\mathcal{A}$ and a map $a \colon TA \to A$ such that
    > $$a \circ \eta_A = 1_A \quad\text{(unit axiom)}, \qquad a \circ \mu_A = a \circ T(a) \quad\text{(associativity axiom, two maps } T^2A \to A\text{)}.$$
    > A **map of $T$-algebras** $(A, a) \to (B, b)$ is a map $f \colon A \to B$ of $\mathcal{A}$ with $f \circ a = b \circ T(f)$. The $T$-algebras and their maps form the **Eilenberg–Moore category** $\mathcal{A}^T$, with composition and identities as in $\mathcal{A}$.

    **Reading the definition.**

    - An algebra is an object *with extra structure*; the same object may carry many algebra structures or none.
    - Unit axiom: evaluating a "one-letter" expression returns the letter.
    - Associativity axiom: an expression of expressions can be evaluated in two ways, flatten first ($\mu_A$) or evaluate the inner expressions first ($T(a)$), with the same result.
    - A map of algebras commutes with evaluation.
    - That composites and identities of algebra maps are algebra maps, so that $\mathcal{A}^T$ is a category, is brief P02.
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "T2": (0, 1.8, r"$T^2A$"),
            "Ta": (2.6, 1.8, r"$TA$"),
            "Tb": (0, 0, r"$TA$"),
            "A": (2.6, 0, r"$A$"),
            "A1": (4.8, 1.8, r"$A$"),
            "TA": (7.2, 1.8, r"$TA$"),
            "A2": (7.2, 0, r"$A$"),
        },
        [
            ("T2", "Ta", r"$T(a)$"),
            ("T2", "Tb", r"$\mu_A$", {"side": -1}),
            ("Ta", "A", r"$a$"),
            ("Tb", "A", r"$a$", {"side": -1}),
            ("A1", "TA", r"$\eta_A$"),
            ("TA", "A2", r"$a$"),
            ("A1", "A2", r"$1_A$", {"side": -1}),
        ],
        figsize=(8.0, 3.0),
        title="Algebra axioms: associativity (left) and unit (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - *Free monoid monad.* A monoid $M$ gives an algebra $a \colon M^* \to M$, $a(m_1 \cdots m_n) = m_1 m_2 \cdots m_n$ (the empty word goes to the identity element). In fact every algebra arises this way from exactly one monoid structure, and algebra maps are monoid homomorphisms; that is the stretch brief P06.
    - *Power set monad.* An algebra is a function $a \colon \mathscr{P}(A) \to A$ choosing an element for every subset. If $A$ is a poset in which every subset has a join, $a(S) = \bigvee S$ is an algebra. It is a fact (stated, not proved here) that every algebra is of this form for a unique such order.
    - *Closure operator.* An algebra is an element $p$ with $T(p) \le p$; see Section 7.
    - *Identity monad.* The unit axiom forces $a = 1_A$, so every object is an algebra in exactly one way and $\mathcal{A}^T \cong \mathcal{A}$.

    **Non-example.** For the free monoid monad on $A = \mathbb{N}$, the function $a(n_1 \cdots n_k) = k$ (the length of the word) is not an algebra: the unit axiom would require $a$ of the one-letter word $n$ to be $n$, and it is $1$. The function $a(n_1 \cdots n_k) = n_1 + \cdots + n_k$ is an algebra, the one coming from the monoid $(\mathbb{N}, +, 0)$.

    The most important algebras are built from $T$ itself.

    > **Lemma 1 (free algebras).** For every object $A$, the pair $(TA, \mu_A)$ is a $T$-algebra. For every map $f \colon A \to B$ of $\mathcal{A}$, $T(f)$ is a map of algebras $(TA, \mu_A) \to (TB, \mu_B)$.

    - **Goal.** (i) $\mu_A \circ \eta_{TA} = 1_{TA}$. (ii) $\mu_A \circ \mu_{TA} = \mu_A \circ T(\mu_A)$. (iii) $T(f) \circ \mu_A = \mu_B \circ T(T(f))$.
    - **Given.** The monad axioms and naturality of $\mu$.
    - **Plan.** Match each clause of the definition of an algebra, with the object $TA$ and structure map $\mu_A$, against a monad axiom.
    - **Proof.** (i) is the first unit law of the monad. (ii) is the associativity law of the monad. (iii) is naturality of $\mu$ at $f$. $\blacksquare$
    - **What made it work.** The algebra axioms were designed to be the monad axioms with the outermost $T$ removed. Putting it back gives a free supply of algebras.

    > Reference: [Riehl §5.2](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Eilenberg–Moore Adjunction

    Lemma 1 defines a functor $F^T \colon \mathcal{A} \to \mathcal{A}^T$, $F^T(A) = (TA, \mu_A)$ and $F^T(f) = T(f)$; it is a functor because $T$ is. In the other direction there is the forgetful functor $U^T \colon \mathcal{A}^T \to \mathcal{A}$, $U^T(A, a) = A$ and $U^T(f) = f$.

    > **Theorem 2.** Let $(T, \eta, \mu)$ be a monad on $\mathcal{A}$. Then $F^T \dashv U^T$, with unit $\eta$ and counit $\varepsilon_{(A,a)} = a \colon (TA, \mu_A) \to (A, a)$. The monad induced by this adjunction (Theorem 1) is $(T, \eta, \mu)$.

    - **Goal.** (i) Each $\varepsilon_{(A,a)} = a$ is a map of algebras $F^T U^T(A, a) \to (A, a)$, and $\varepsilon$ is natural. (ii) $\eta$ is a natural transformation $1_{\mathcal{A}} \Rightarrow U^T F^T$. (iii) The triangle identities hold. (iv) $U^T F^T = T$ and $U^T(\varepsilon_{F^T(A)}) = \mu_A$.
    - **Given.** The monad axioms; the algebra axioms for each $(A, a)$; from 2B, that functors $F$, $G$ with natural transformations $\eta$, $\varepsilon$ satisfying the triangle identities form an adjunction $F \dashv G$.
    - **Plan.** Use the unit–counit description of an adjunction. Every item to be checked turns out to be one axiom, of the monad or of an algebra.
    - **Proof.** (i) $F^T U^T(A, a) = (TA, \mu_A)$. For $a$ to be an algebra map $(TA, \mu_A) \to (A, a)$ we need $a \circ \mu_A = a \circ T(a)$, which is the associativity axiom of the algebra $(A, a)$. Naturality of $\varepsilon$ at an algebra map $f \colon (A, a) \to (B, b)$ reads $f \circ a = b \circ T(f)$, which is the definition of an algebra map.

      (ii) $U^T F^T(A) = TA$ and $U^T F^T(f) = T(f)$, so $U^T F^T = T$ and $\eta \colon 1 \Rightarrow T$ is natural as part of the monad.

      (iii) *First triangle identity*, at $A \in \mathcal{A}$: $\varepsilon_{F^T(A)} \circ F^T(\eta_A) = \mu_A \circ T(\eta_A) = 1_{TA}$ by the second unit law of the monad. *Second triangle identity*, at $(A, a) \in \mathcal{A}^T$: $U^T(\varepsilon_{(A,a)}) \circ \eta_{U^T(A,a)} = a \circ \eta_A = 1_A$ by the unit axiom of the algebra.

      (iv) $U^T F^T = T$ was shown in (ii). The induced multiplication at $A$ is $U^T(\varepsilon_{F^T(A)}) = \varepsilon_{(TA, \mu_A)} = \mu_A$. The unit of the adjunction is $\eta$ by construction. $\blacksquare$
    - **What made it work.** The definition of an algebra is exactly the list of what a counit $a$ must satisfy. The Eilenberg–Moore category is the answer to "what is the most general thing a counit could act on?"

    So every monad comes from an adjunction. For the free monoid monad, Theorem 2 together with P06 says that $\mathbf{Set}^T$ is the category of monoids and $F^T \dashv U^T$ is the free–forgetful adjunction you started from.

    > Reference: [Riehl §5.2](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The Kleisli Category

    There is a second, more economical way to get an adjunction from a monad. Instead of adding *all* possible algebras, keep the objects of $\mathcal{A}$ and change what a map is.

    > **Definition (Kleisli category).** Let $(T, \eta, \mu)$ be a monad on $\mathcal{A}$. The **Kleisli category** $\mathcal{A}_T$ has
    >
    > - the same objects as $\mathcal{A}$;
    > - as maps $A \rightsquigarrow B$, the maps $A \to TB$ of $\mathcal{A}$;
    > - as identity on $A$, the unit $\eta_A \colon A \to TA$;
    > - as composite of $f \colon A \to TB$ and $g \colon B \to TC$, the map
    > $$g \bullet f \;=\; \mu_C \circ T(g) \circ f \;\colon\; A \to TC.$$

    **Reading the definition.**

    - A Kleisli map from $A$ to $B$ does not land in $B$; it lands in $TB$. The symbol $\rightsquigarrow$ is a reminder.
    - Two such maps cannot be composed directly, since the codomain $TB$ of $f$ is not the domain $B$ of $g$. Apply $T$ to $g$ to get $TB \to T^2C$, then use $\mu$ to come back down to $TC$.
    - That this is a category (identity laws and associativity) must be proved.

    **Examples.**

    - *Free monoid monad.* A Kleisli map $X \rightsquigarrow Y$ assigns to each $x \in X$ a word in $Y$. The composite substitutes words for letters and concatenates. A function $X \to Y^*$ is the same as a monoid homomorphism $X^* \to Y^*$ (the adjunction), so $\mathbf{Set}_T$ looks like the category of *free* monoids and all homomorphisms between them.
    - *Power set monad.* A Kleisli map $X \rightsquigarrow Y$ is a function $X \to \mathscr{P}(Y)$, which is the same information as a relation between $X$ and $Y$. Brief P04 identifies $\mathbf{Set}_{\mathscr{P}}$ with the category of sets and relations.
    - *Closure operator.* $p \rightsquigarrow q$ exactly when $p \le T(q)$; see Section 7.

    **Non-example.** Composing $f \colon A \to TB$ and $g \colon B \to TC$ as $T(g) \circ f \colon A \to T^2 C$ and stopping there does not define a category on these maps: the composite has the wrong codomain to be a map $A \rightsquigarrow C$. The multiplication $\mu$ is not optional.

    > **Theorem 3.** $\mathcal{A}_T$ is a category. The assignments
    > $$F_T \colon \mathcal{A} \to \mathcal{A}_T, \quad F_T(A) = A, \quad F_T(f \colon A \to B) = \eta_B \circ f,$$
    > $$U_T \colon \mathcal{A}_T \to \mathcal{A}, \quad U_T(A) = TA, \quad U_T(g \colon A \rightsquigarrow B) = \mu_B \circ T(g)$$
    > are functors, $F_T \dashv U_T$, and the monad induced by this adjunction is $(T, \eta, \mu)$.

    The proof is in three parts. Two computations recur, so name them: for any map $f \colon A \to B$ of $\mathcal{A}$ and any map $h \colon C \to TD$ of $\mathcal{A}$,
    $$\text{(K1)}\quad T(f) \circ \eta_A = \eta_B \circ f \ \ (\text{naturality of } \eta), \qquad \text{(K2)}\quad \mu_{TD} \circ T^2(h) = T(h) \circ \mu_C \ \ (\text{naturality of } \mu \text{ at } h).$$

    **Part 1: $\mathcal{A}_T$ is a category.**

    - **Goal.** For all $f \colon A \to TB$, $g \colon B \to TC$, $h \colon C \to TD$: $\eta_B \bullet f = f$, $f \bullet \eta_A = f$, and $(h \bullet g) \bullet f = h \bullet (g \bullet f)$.
    - **Given.** The monad axioms, (K1), (K2), functoriality of $T$.
    - **Plan.** Expand each side with the definition of $\bullet$ and rewrite with one axiom at a time.
    - **Proof.** *Left identity.* $\eta_B \bullet f = \mu_B \circ T(\eta_B) \circ f = f$ by the second unit law.

      *Right identity.* $f \bullet \eta_A = \mu_B \circ T(f) \circ \eta_A = \mu_B \circ \eta_{TB} \circ f$ by (K1) applied to $f \colon A \to TB$, and this is $f$ by the first unit law.

      *Associativity.* Using functoriality of $T$,
      $$(h \bullet g) \bullet f = \mu_D \circ T(\mu_D \circ T(h) \circ g) \circ f = \mu_D \circ T(\mu_D) \circ T^2(h) \circ T(g) \circ f.$$
      On the other side,
      $$h \bullet (g \bullet f) = \mu_D \circ T(h) \circ \mu_C \circ T(g) \circ f = \mu_D \circ \mu_{TD} \circ T^2(h) \circ T(g) \circ f$$
      by (K2). The two right-hand sides agree by the associativity law $\mu_D \circ T(\mu_D) = \mu_D \circ \mu_{TD}$. $\blacksquare$
    - **What made it work.** Each category axiom for $\mathcal{A}_T$ consumed exactly one monad axiom, plus naturality to move maps past $\eta$ and $\mu$. The monad axioms are what is needed for "maps into $TB$" to compose.

    **Part 2: $F_T$ and $U_T$ are functors.**

    - **Goal.** $F_T(1_A) = \eta_A$ and $F_T(g) \bullet F_T(f) = F_T(g f)$; $U_T(\eta_A) = 1_{TA}$ and $U_T(h \bullet g) = U_T(h) \circ U_T(g)$.
    - **Given.** As in Part 1.
    - **Plan.** Expand and rewrite, as before.
    - **Proof.** $F_T(1_A) = \eta_A \circ 1_A = \eta_A$, the identity of $\mathcal{A}_T$. For $f \colon A \to B$ and $g \colon B \to C$ in $\mathcal{A}$:
      $$F_T(g) \bullet F_T(f) = \mu_C \circ T(\eta_C) \circ T(g) \circ \eta_B \circ f = T(g) \circ \eta_B \circ f = \eta_C \circ g \circ f = F_T(gf),$$
      by the second unit law and then (K1). Next, $U_T(\eta_A) = \mu_A \circ T(\eta_A) = 1_{TA}$. For $g \colon B \rightsquigarrow C$ and $h \colon C \rightsquigarrow D$:
      $$U_T(h \bullet g) = \mu_D \circ T(\mu_D) \circ T^2(h) \circ T(g) = \mu_D \circ \mu_{TD} \circ T^2(h) \circ T(g) = \mu_D \circ T(h) \circ \mu_C \circ T(g) = U_T(h) \circ U_T(g),$$
      by associativity and then (K2). $\blacksquare$
    - **What made it work.** The same two moves as Part 1; $U_T$ is "compose on the Kleisli side" with the first map removed.

    **Part 3: the adjunction and its monad.**

    - **Goal.** A bijection $\mathcal{A}_T(F_T(A), B) \to \mathcal{A}(A, U_T(B))$, natural in $A \in \mathcal{A}$ and $B \in \mathcal{A}_T$, whose induced monad is $(T, \eta, \mu)$.
    - **Given.** The definitions; Parts 1 and 2; from 2B, that the unit is the transpose of an identity of $\mathcal{B}$ and the counit the transpose of an identity of $\mathcal{A}$.
    - **Plan.** The two hom-sets are literally the same set, so take the identity function; then check naturality and follow identities.
    - **Proof.** $\mathcal{A}_T(F_T(A), B) = \mathcal{A}_T(A, B) = \mathcal{A}(A, TB) = \mathcal{A}(A, U_T(B))$. Take the bijection to be the identity, $g \mapsto g$.

      *Natural in $A$.* For $p \colon A' \to A$ in $\mathcal{A}$ and $g \colon A \rightsquigarrow B$: $g \bullet F_T(p) = \mu_B \circ T(g) \circ \eta_A \circ p = \mu_B \circ \eta_{TB} \circ g \circ p = g \circ p$, by (K1) and the first unit law. So precomposing with $F_T(p)$ in $\mathcal{A}_T$ matches precomposing with $p$ in $\mathcal{A}$.

      *Natural in $B$.* For $k \colon B \rightsquigarrow B'$ and $g \colon A \rightsquigarrow B$: $k \bullet g = \mu_{B'} \circ T(k) \circ g = U_T(k) \circ g$. So postcomposing with $k$ in $\mathcal{A}_T$ matches postcomposing with $U_T(k)$ in $\mathcal{A}$.

      *The induced monad.* On objects $U_T F_T(A) = TA$; on maps $U_T F_T(f) = \mu_B \circ T(\eta_B) \circ T(f) = T(f)$. The unit at $A$ is the transpose of the identity of $F_T(A)$ in $\mathcal{A}_T$, which is $\eta_A$. The counit at $B$ is the Kleisli map $TB \rightsquigarrow B$ whose transpose is $1_{TB}$, namely $1_{TB}$ itself regarded as a map $TB \to TB$. So the induced multiplication at $A$ is $U_T(1_{TA} \colon TA \rightsquigarrow A) = \mu_A \circ T(1_{TA}) = \mu_A$. $\blacksquare$
    - **What made it work.** The Kleisli category is built so that the adjunction bijection is the identity: it is the smallest category in which "a map $A \to TB$" *is* "a map out of the free object on $A$".

    > Reference: [Riehl §5.2](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Comparing Adjunctions: Monadic Functors

    One monad, two adjunctions (at least). How does an arbitrary adjunction $F \dashv G$ with $GF = T$ sit relative to these two? The Kleisli and Eilenberg–Moore adjunctions are the two extremes: there are canonical functors $\mathcal{A}_T \to \mathcal{B} \to \mathcal{A}^T$ compatible with all the free and forgetful functors. The second one is the important one.

    > **Definition (comparison functor; monadic).** Let $F \dashv G$, $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$, with counit $\varepsilon$ and induced monad $T = GF$ on $\mathcal{A}$. The **comparison functor** is
    > $$K \colon \mathcal{B} \to \mathcal{A}^T, \qquad K(B) = \big(G(B),\ G(\varepsilon_B)\big), \qquad K(q) = G(q).$$
    > It satisfies $U^T \circ K = G$ and $K \circ F = F^T$. The adjunction, and the functor $G$, are called **monadic** if $K$ is an equivalence of categories.

    **Reading the definition.**

    - $K$ equips the object $G(B)$ of $\mathcal{A}$ with the algebra structure $G(\varepsilon_B) \colon GFG(B) \to G(B)$.
    - That $K(B)$ really is an algebra, that $G(q)$ is an algebra map, and the two displayed equations, are brief P03.
    - "Monadic" says: $\mathcal{B}$ can be reconstructed, up to equivalence, from the monad on $\mathcal{A}$ alone. Everything in $\mathcal{B}$ is "an object of $\mathcal{A}$ with operations".
    """)
    return


@app.cell(hide_code=True)
def _():
    draw_diagram(
        {
            "B": (0, 1.9, r"$\mathcal{B}$"),
            "AT": (3.2, 1.9, r"$\mathcal{A}^T$"),
            "A": (1.6, 0, r"$\mathcal{A}$"),
        },
        [
            ("B", "AT", r"$K$", {"dashed": True, "color": "#b91c1c"}),
            ("B", "A", r"$G$", {"side": -1}),
            ("AT", "A", r"$U^T$"),
        ],
        figsize=(4.8, 3.2),
        title="The comparison functor: G factors through the algebras",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    - The forgetful functors $\mathbf{Mon} \to \mathbf{Set}$ and $\mathbf{Grp} \to \mathbf{Set}$ are monadic: a monoid *is* an algebra for the free monoid monad (P06 proves the essential point for monoids), and similarly for groups.
    - $U^T \colon \mathcal{A}^T \to \mathcal{A}$ is monadic for every monad $T$: its comparison functor is the identity.

    **Non-example.** $U \colon \mathbf{Top} \to \mathbf{Set}$ is not monadic. Its left adjoint is the discrete-space functor and the monad is the identity monad (Section 2), whose category of algebras is $\mathbf{Set}$ itself (Section 3). The comparison functor is $U \colon \mathbf{Top} \to \mathbf{Set}$, which is not full (a non-continuous function is a map of underlying sets that does not come from $\mathbf{Top}$), so it is not an equivalence. A topology is not algebraic structure in this sense.

    How do you recognise a monadic functor without computing the category of algebras? The answer is a theorem of Beck. It is stated here with all its hypotheses and **not proved**.

    > **Definition (split coequalizer).** In a category $\mathcal{A}$, a **split coequalizer** of a parallel pair $u, v \colon X \rightrightarrows Y$ is a map $h \colon Y \to Z$ together with maps $s \colon Z \to Y$ and $t \colon Y \to X$ such that
    > $$h u = h v, \qquad h s = 1_Z, \qquad u t = 1_Y, \qquad v t = s h.$$

    These equations imply that $h$ is a coequalizer of $u$ and $v$, and, being equations, they are preserved by every functor.

    > **Theorem 4 (Beck's monadicity theorem, strict form; statement only).** Let $G \colon \mathcal{B} \to \mathcal{A}$ be a functor with a left adjoint $F$, and let $K \colon \mathcal{B} \to \mathcal{A}^T$ be the comparison functor for $T = GF$. The following are equivalent:
    >
    > **(i)** $K$ is an isomorphism of categories;
    >
    > **(ii)** for every parallel pair $f, g \colon B \rightrightarrows B'$ in $\mathcal{B}$ and every split coequalizer $h \colon G(B') \to C$ of $G(f), G(g)$ in $\mathcal{A}$, there is exactly one pair consisting of an object $E$ of $\mathcal{B}$ and a map $e \colon B' \to E$ with $G(E) = C$ and $G(e) = h$, and this $e$ is a coequalizer of $f$ and $g$ in $\mathcal{B}$.

    Condition (ii) is expressed by saying that $G$ *creates coequalizers of $G$-split pairs*, with "creates" in the strict sense: equalities $G(E) = C$ and $G(e) = h$, not isomorphisms. There is a parallel version for monadic functors as defined above: $K$ is an *equivalence* if and only if $G$ creates such coequalizers in the corresponding up-to-isomorphism sense. That is the form given in Riehl §5.5, which also contains the proof.

    What the theorem says informally: $\mathcal{B}$ is a category of algebras exactly when quotients in $\mathcal{B}$ of a certain special kind can be computed in $\mathcal{A}$ and then lifted uniquely. Groups pass this test, because a quotient of the right kind of the underlying set carries exactly one compatible group structure. Topological spaces fail it.

    > Reference: [Riehl §5.3](https://math.jhu.edu/~eriehl/context.pdf) (monadic functors) and [Riehl §5.5](https://math.jhu.edu/~eriehl/context.pdf) (the monadicity theorem).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. The Poset Case, Worked in Full: Closure Operators

    In a poset every construction of this module can be carried out completely, and every theorem above becomes a statement you can check by inspection. Throughout, $P$ is a poset regarded as a category: there is a map $p \to q$ exactly when $p \le q$, and any two maps with the same domain and codomain are equal. That last fact means **every diagram in a poset commutes**, so every *equation* between maps holds automatically; only the *existence* of maps needs attention.

    > **Definition.** A **closure operator** on a poset $P$ is a function $T \colon P \to P$ that is
    >
    > - *order-preserving:* $p \le q \Rightarrow T(p) \le T(q)$;
    > - *extensive:* $p \le T(p)$;
    > - *idempotent:* $T(T(p)) \le T(p)$ (and hence $T(T(p)) = T(p)$, using extensivity at $T(p)$ and antisymmetry).
    >
    > An element $p$ is **closed** if $T(p) = p$. Write $\mathrm{Cl}(T)$ for the set of closed elements, ordered as in $P$.

    > **Theorem 5 (monads on a poset).** Let $P$ be a poset.
    >
    > **(a)** A monad on $P$ is the same thing as a closure operator on $P$.
    >
    > **(b)** For a closure operator $T$, the Eilenberg–Moore category $P^T$ is isomorphic to the poset $\mathrm{Cl}(T)$, and the Eilenberg–Moore adjunction is: $T \colon P \to \mathrm{Cl}(T)$ is left adjoint to the inclusion $\mathrm{Cl}(T) \to P$.
    >
    > **(c)** The Kleisli category $P_T$ is the preorder on the elements of $P$ with $p \rightsquigarrow q$ if and only if $p \le T(q)$, and $p \mapsto T(p)$ is an equivalence of categories $P_T \to \mathrm{Cl}(T)$.
    >
    > **(d)** Let $F \dashv G$ be a Galois connection, $F \colon P \to Q$, $G \colon Q \to P$, and $T = GF$. The comparison functor is $K \colon Q \to \mathrm{Cl}(T)$, $K(q) = G(q)$. It is always order-preserving and surjective, and it is an isomorphism of posets if and only if $G$ reflects the order: $G(q) \le G(q') \Rightarrow q \le q'$.

    **Proof of (a).**

    - **Goal.** The data and axioms of a monad on the category $P$ correspond exactly to the three conditions on a closure operator.
    - **Given.** The definition of a monad; in $P$ there is at most one map between two objects.
    - **Plan.** Unpack each piece of monad data as an inequality; observe that naturality and the axioms are automatic.
    - **Proof.** A functor $T \colon P \to P$ is an order-preserving function. A natural transformation $\eta \colon 1 \Rightarrow T$ is a map $p \to T(p)$ for each $p$, that is, $p \le T(p)$; the naturality squares commute because all diagrams in $P$ do. Likewise $\mu \colon TT \Rightarrow T$ is $T(T(p)) \le T(p)$ for each $p$. The associativity and unit laws are equations between parallel maps in $P$, so they hold. Since components are unique when they exist, a closure operator has exactly one monad structure. $\blacksquare$
    - **What made it work.** In a poset, data are inequalities and axioms are free.

    **Proof of (b).**

    - **Goal.** (i) An element $p$ has an algebra structure if and only if it is closed, and then exactly one. (ii) Every inequality between closed elements is an algebra map. (iii) For $p \in P$ and $c \in \mathrm{Cl}(T)$: $T(p) \le c \iff p \le c$.
    - **Given.** The definition of an algebra; $T$ is a closure operator.
    - **Plan.** Unpack; then prove (iii) directly, although it also follows from Theorem 2.
    - **Proof.** (i) An algebra structure on $p$ is a map $T(p) \to p$, that is, the inequality $T(p) \le p$; the two algebra axioms are equations in $P$ and hold automatically. With extensivity $p \le T(p)$ and antisymmetry, $T(p) \le p$ is equivalent to $T(p) = p$. There is at most one map $T(p) \to p$, so the structure is unique. (ii) A map of algebras $c \to c'$ is a map $c \le c'$ satisfying an equation in $P$, which holds automatically. So $P^T$ has the closed elements as objects and their inequalities as maps: it is $\mathrm{Cl}(T)$. Under this identification $F^T(p) = (T(p), \mu_p)$ is the closed element $T(p)$ and $U^T$ is the inclusion. (iii) If $T(p) \le c$ then $p \le T(p) \le c$ by extensivity. If $p \le c$ then $T(p) \le T(c) = c$ because $T$ is order-preserving and $c$ is closed. $\blacksquare$
    - **What made it work.** "Algebra" collapsed to "fixed point" because a poset has no room for more than one structure map.

    **Proof of (c).**

    - **Goal.** (i) $p \le T(q) \iff T(p) \le T(q)$ for all $p, q \in P$. (ii) The functor $J \colon P_T \to \mathrm{Cl}(T)$, $J(p) = T(p)$, is full, faithful and essentially surjective on objects.
    - **Given.** The definition of $P_T$; $T$ is a closure operator; from 1E, a functor that is full, faithful and essentially surjective on objects is an equivalence.
    - **Plan.** (i) is two one-line inequalities. (ii) reads off the three properties from (i).
    - **Proof.** (i) If $p \le T(q)$ then $T(p) \le T(T(q)) = T(q)$. If $T(p) \le T(q)$ then $p \le T(p) \le T(q)$. (ii) A map $p \rightsquigarrow q$ in $P_T$ is a map $p \to T(q)$ in $P$, so there is one exactly when $p \le T(q)$, and at most one. By (i), $J$ is well defined on maps, and there is a map $J(p) \to J(q)$ exactly when there is a map $p \rightsquigarrow q$. Both hom-sets have at most one element, so $J$ is a bijection on each hom-set: full and faithful. Every closed $c$ equals $T(c) = J(c)$, so $J$ is surjective on objects. $\blacksquare$
    - **What made it work.** The Kleisli category has "too many" objects: $p$ and $T(p)$ are different objects of $P_T$ but isomorphic there. An equivalence, not an isomorphism, is the right notion of sameness (1E).

    **Proof of (d).**

    - **Goal.** (i) $G(q)$ is closed for every $q \in Q$. (ii) $K$ is surjective onto $\mathrm{Cl}(T)$. (iii) $K$ is an isomorphism of posets $\iff$ $G$ reflects the order.
    - **Given.** $F(p) \le q \iff p \le G(q)$; hence $p \le GF(p)$ and $FG(q) \le q$ (take $q = F(p)$, respectively $p = G(q)$); $F$, $G$ order-preserving.
    - **Plan.** Direct, using the unit and counit inequalities; for (iii), recall that an isomorphism of posets is a bijection that preserves and reflects the order.
    - **Proof.** (i) $G(q) \le GF(G(q))$ by the unit inequality at $p = G(q)$. Also $FG(q) \le q$, so $GFG(q) \le G(q)$ because $G$ is order-preserving. By antisymmetry $T(G(q)) = G(q)$. (ii) If $c$ is closed then $c = GF(c) = K(F(c))$. (iii) $K$ and $G$ are the same function with different codomains, so $K$ reflects the order exactly when $G$ does. If $K$ is an isomorphism it reflects the order. Conversely, suppose $G$ reflects the order. If $K(q) = K(q')$ then $q \le q'$ and $q' \le q$, so $q = q'$: $K$ is injective. With (ii), $K$ is a bijection; it preserves the order because $G$ does, and its inverse preserves the order because $K$ reflects it. $\blacksquare$
    - **What made it work.** In a poset, "monadic" means "$G$ is an order-embedding": $Q$ is, up to isomorphism, a set of closed elements of $P$. Compare the non-example of Section 6: there $U$ failed to be full; here $G$ fails to reflect the order.

    **The round trip.** Parts (b) and (d) together describe both directions. *Closure operator $\to$ Galois connection $\to$ closure operator:* from $T$ form $P \rightleftarrows \mathrm{Cl}(T)$; its composite is $T$ again (Theorem 2). *Galois connection $\to$ closure operator $\to$ Galois connection:* from $F \dashv G$ form $T = GF$ and then $P \rightleftarrows \mathrm{Cl}(T)$; you get back $Q$ only up to the comparison map $K$, and only when $G$ reflects the order.

    The widget runs both trips. Preset 1 is "subgroup generated by a subset" for the cyclic group $\mathbb{Z}_4$; preset 2 is a Galois connection between chains in which $G$ is not injective; preset 3 adjoins the element $1$ to a subset of $\{1, 2, 3\}$.

    > Reference: [Riehl §5.1–5.3](https://math.jhu.edu/~eriehl/context.pdf); closure operators appear there as the monads on a poset.
    """)
    return


@app.cell
def _(mo):
    closure_pick = mo.ui.dropdown(
        options=[
            "1. P = subsets of Z_4,  Q = subgroups of Z_4,  F = generated subgroup,  G = inclusion",
            "2. P = chain 0..2,  Q = chain 0..3,  F = (0,1,3),  G = (0,1,1,2)",
            "3. P = subsets of {1,2,3},  Q = subsets of {2,3},  F(S) = S - {1},  G(R) = R + {1}",
        ],
        value="1. P = subsets of Z_4,  Q = subgroups of Z_4,  F = generated subgroup,  G = inclusion",
        label="Galois connection F : P -> Q, G : Q -> P",
    )
    closure_pick
    return (closure_pick,)


@app.cell
def _(closure_pick, mo):
    def _run():
        import itertools

        def _subsets(_xs):
            return [frozenset(_c) for _r in range(len(_xs) + 1) for _c in itertools.combinations(_xs, _r)]

        def _show(_x):
            if isinstance(_x, frozenset):
                return "{" + ",".join(str(_i) for _i in sorted(_x)) + "}"
            return str(_x)

        def _leq(_x, _y):
            return _x <= _y

        _key = closure_pick.value[0]
        if _key == "1":
            _P = _subsets([0, 1, 2, 3])
            _Q = [frozenset([0]), frozenset([0, 2]), frozenset([0, 1, 2, 3])]
            _F = {_S: min((_H for _H in _Q if _S <= _H), key=len) for _S in _P}
            _G = {_H: _H for _H in _Q}
        elif _key == "2":
            _P, _Q = [0, 1, 2], [0, 1, 2, 3]
            _F = {0: 0, 1: 1, 2: 3}
            _G = {0: 0, 1: 1, 2: 1, 3: 2}
        else:
            _P, _Q = _subsets([1, 2, 3]), _subsets([2, 3])
            _F = {_S: _S - frozenset([1]) for _S in _P}
            _G = {_R: _R | frozenset([1]) for _R in _Q}

        _galois = all(_leq(_F[_p], _q) == _leq(_p, _G[_q]) for _p in _P for _q in _Q)
        _T = {_p: _G[_F[_p]] for _p in _P}
        _closed = [_p for _p in _P if _T[_p] == _p]
        _extensive = all(_leq(_p, _T[_p]) for _p in _P)
        _monotone = all(_leq(_T[_p], _T[_p2]) for _p in _P for _p2 in _P if _leq(_p, _p2))
        _idempotent = all(_T[_T[_p]] == _T[_p] for _p in _P)

        # Trip 1: closure operator -> Eilenberg-Moore adjunction -> closure operator.
        # The left adjoint of the inclusion Cl(T) -> P, found by search: the least closed element above p.
        def _least_closed_above(_p):
            _above = [_c for _c in _closed if _leq(_p, _c)]
            return [_c for _c in _above if all(_leq(_c, _d) for _d in _above)][0]

        _trip1 = all(_least_closed_above(_p) == _T[_p] for _p in _P)

        # Trip 2: the comparison map K : Q -> Cl(T), q |-> G(q).
        _K = {_q: _G[_q] for _q in _Q}
        _K_lands = all(_K[_q] in _closed for _q in _Q)
        _K_bijective = _K_lands and len(set(_K.values())) == len(_Q) and set(_K.values()) == set(_closed)
        _G_reflects = all(_leq(_q, _q2) for _q in _Q for _q2 in _Q if _leq(_G[_q], _G[_q2]))

        _yes = lambda _b: "yes" if _b else "**no**"
        _rows = [
            f"**Galois connection** ($F(p) \\le q \\iff p \\le G(q)$ on all {len(_P) * len(_Q)} pairs): {_yes(_galois)}",
            "",
            "| $p$ | $F(p)$ | $T(p) = GF(p)$ | closed? |",
            "|---|---|---|---|",
        ]
        for _p in _P:
            _rows.append(f"| {_show(_p)} | {_show(_F[_p])} | {_show(_T[_p])} | {'closed' if _T[_p] == _p else ''} |")
        _rows += [
            "",
            f"**$T$ is a closure operator:** extensive {_yes(_extensive)}, order-preserving {_yes(_monotone)}, idempotent {_yes(_idempotent)}.",
            "",
            f"**Closed elements** $\\mathrm{{Cl}}(T)$ ({len(_closed)} of {len(_P)}): " + ", ".join(_show(_c) for _c in _closed),
            "",
            f"**Trip 1** (closure operator $\\to$ adjunction $P \\rightleftarrows \\mathrm{{Cl}}(T)$ $\\to$ closure operator): "
            f"the least closed element above $p$ equals $T(p)$ for every $p$: {_yes(_trip1)}",
            "",
            "**Trip 2** (comparison map $K \\colon Q \\to \\mathrm{Cl}(T)$): "
            + ", ".join(f"{_show(_q)} $\\mapsto$ {_show(_K[_q])}" for _q in _Q),
            "",
            f"$K$ lands in closed elements: {_yes(_K_lands)}. $G$ reflects the order: {_yes(_G_reflects)}. "
            f"$K$ is an isomorphism of posets: {_yes(_K_bijective and _G_reflects)}.",
        ]
        return mo.md("\n".join(_rows))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In preset 1 the sixteen subsets of $\mathbb{Z}_4$ collapse onto three closed ones, the subgroups, and $K$ is an isomorphism: the poset of subgroups is recovered from the closure operator alone. This is the poset shadow of "$\mathbf{Grp} \to \mathbf{Set}$ is monadic". In preset 2 the monad is the identity, every element of $P$ is closed, and $Q$ has four elements where $\mathrm{Cl}(T)$ has three: the Galois connection contains information that the closure operator has forgotten, exactly as $\mathbf{Top}$ did in Section 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Mixing up $T\mu$ and $\mu T$.** Treating $T(\mu_A)$ and $\mu_{TA}$ as the same map $T^3A \to T^2A$. *Diagnosis:* one multiplies the inner two layers, the other the outer two. For words: one concatenates inside each letter of the outer word, the other concatenates the outer word. The associativity law says they agree *after* a further $\mu_A$, not before.
    2. **Checking an algebra's unit axiom only.** Showing $a \circ \eta_A = 1_A$ and declaring $(A, a)$ an algebra. *Diagnosis:* there are two axioms, and the associativity axiom is the one with content: it is where, for monoids, associativity of the multiplication comes from.
    3. **Composing Kleisli maps as if they were maps of $\mathcal{A}$.** Writing $g \circ f$ for $f \colon A \to TB$ and $g \colon B \to TC$. *Diagnosis:* the domain of $g$ is $B$, not $TB$; write out the types and the missing $T(g)$ and $\mu_C$ become visible.
    4. **Using naturality at the wrong map.** In Theorem 1(ii), applying naturality of $\varepsilon$ at $\eta_A$ or at $F(\eta_A)$. *Diagnosis:* look at the two composites you want to compare; the map that appears "with a functor applied" on one side and "bare" on the other is the one to be natural at. Here that map is $\varepsilon_{F(A)}$.
    5. **Concluding that an adjunction is determined by its monad.** *Diagnosis:* Theorems 2 and 3 already give two different adjunctions with the same monad, and preset 2 of the widget gives a third. Only *monadic* adjunctions are recovered, and that is a hypothesis to be checked.

    ---

    ## Why This Matters

    - **Universal algebra.** Monoids, groups, rings, modules and vector spaces are all categories of algebras for monads on $\mathbf{Set}$. Statements proved once for $\mathcal{A}^T$ (for example, that $U^T$ creates limits) then hold for all of them at once.
    - **2B revisited.** Closure operators from Galois connections were the first monads you met; Theorem 5 explains why the closed elements kept appearing there.
    - **6C revisited.** $U^T$ is a right adjoint, so by 6C it preserves limits: limits of algebras are computed on underlying objects. That is the general reason products of groups have the product set underneath.
    - **Beyond this course.** The monadicity theorem is the main tool for proving that a category is "algebraic" over another, and the dual notion, comonads and coalgebras, is where interior operators belong.
    - **7A** lists the two canonical adjunctions of a monad side by side with the poset dictionary of Theorem 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Each cell runs as shipped. Replace the `...` placeholders, then uncomment the `print` checks.

    ### Exercise 1: A closure operator from a relation, and its Kleisli preorder

    Let $X = \mathbb{Z}_4 = \{0,1,2,3\}$ and let $Y$ be its set of subgroups. The relation "$x \in H$" gives two order-reversing maps: `up(S)` is the set of subgroups containing every element of $S$, and `down(Hs)` is the set of elements lying in every subgroup in `Hs`. Their composite is a closure operator on subsets of $X$ (the supplied check confirms the three axioms once you have written it). Fill in (a) the closure $T$; (b) the Kleisli relation of Theorem 5(c), $S \rightsquigarrow S'$; and (c) for a closed set $C$, the number of subsets whose closure is $C$, which is the size of the isomorphism class of $C$ in the Kleisli preorder.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        X = [0, 1, 2, 3]
        subgroups = [frozenset([0]), frozenset([0, 2]), frozenset([0, 1, 2, 3])]
        subsets = [frozenset(c) for r in range(len(X) + 1) for c in itertools.combinations(X, r)]

        def up(S):
            return [H for H in subgroups if all(x in H for x in S)]

        def down(Hs):
            return frozenset(x for x in X if all(x in H for H in Hs))

        def T(S):
            # TODO (a): the closure of S, in terms of up and down.
            return ...

        def is_closure_operator():
            extensive = all(S <= T(S) for S in subsets)
            monotone = all(T(S) <= T(S2) for S in subsets for S2 in subsets if S <= S2)
            idempotent = all(T(T(S)) == T(S) for S in subsets)
            return extensive and monotone and idempotent

        def kleisli(S, S2):
            # TODO (b): is there a Kleisli map S ~> S2 ?  (Theorem 5(c))
            return ...

        def class_size(C):
            # TODO (c): the number of S in `subsets` whose closure is C.
            return ...

        # print(sorted(T(frozenset([1]))), sorted(T(frozenset([2]))), sorted(T(frozenset())))
        #   expect [0, 1, 2, 3] [0, 2] [0]
        # print(is_closure_operator())                 # expect True
        # print(kleisli(frozenset([0]), frozenset([2])), kleisli(frozenset([2]), frozenset([0])))   # expect True False
        # print(sum(1 for S in subsets for S2 in subsets if kleisli(S, S2)))                      # expect 204
        # print(all(kleisli(S, S2) == (T(S) <= T(S2)) for S in subsets for S2 in subsets))        # expect True
        # print([class_size(H) for H in subgroups])                                               # expect [2, 2, 12]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Kleisli composition for the power set monad

    A Kleisli map $A \rightsquigarrow B$ for $\mathscr{P}$ is a dict sending each element of $A$ to a frozenset of elements of $B$. Implement $g \bullet f = \mu \circ \mathscr{P}(g) \circ f$ from the definition, then check the identity and associativity laws of Theorem 3 on the three maps given (all on the divisors of $12$).
    """)
    return


@app.cell
def _():
    def _run():
        D = [1, 2, 3, 4, 6, 12]
        f = {n: frozenset(p for p in (2, 3) if n % p == 0) for n in D}       # prime divisors of n
        g = {n: frozenset(m for m in D if m % n == 0 and m != n) for n in D}  # proper multiples of n in D
        h = {n: frozenset(d for d in D if n % d == 0) for n in D}            # divisors of n
        eta = {n: frozenset([n]) for n in D}

        def kleisli(g, f):
            # TODO: for each a, apply g to every element of f[a] (direct image), then take the union.
            return {a: ... for a in f}

        # print(sorted(kleisli(g, f)[12]), sorted(kleisli(g, f)[4]), sorted(kleisli(g, f)[1]))
        #   expect [4, 6, 12] [4, 6, 12] []
        # print(kleisli(f, eta) == f, kleisli(eta, f) == f)                          # expect True True
        # print(kleisli(h, kleisli(g, f)) == kleisli(kleisli(h, g), f))              # expect True
        # print(sorted(kleisli(h, kleisli(g, f))[6]))                                # expect [1, 2, 3, 4, 6, 12]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Count the algebras of the power set monad on a small set

    An algebra on $X$ is a function $a \colon \mathscr{P}(X) \to X$ with $a(\{x\}) = x$ (unit axiom) and $a \circ \mu_X = a \circ \mathscr{P}(a)$ (associativity axiom), where both sides are functions on $\mathscr{P}(\mathscr{P}(X))$. The skeleton enumerates every function satisfying the unit axiom; you supply the associativity test. Count the algebras on a 2-element set and on a 3-element set.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def powerset(xs):
            xs = list(xs)
            return [frozenset(c) for r in range(len(xs) + 1) for c in itertools.combinations(xs, r)]

        def count_algebras(X):
            PX = powerset(X)
            PPX = powerset(PX)
            free = [S for S in PX if len(S) != 1]          # subsets whose value the unit axiom does not fix
            count = 0
            for values in itertools.product(X, repeat=len(free)):
                a = {frozenset([x]): x for x in X}
                a.update(dict(zip(free, values)))
                # TODO: associativity. For every family SS in PPX compare
                #       a[union of the members of SS]   with   a[{a[S] for S in SS}].
                associative = ...
                if associative is True:
                    count += 1
            return count

        # print(count_algebras([0, 1]))        # expect 2
        # print(count_algebras([0, 1, 2]))     # expect 6

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | 1 | `exercises/6d/p01_powerset_monad_axioms.md` | warm-up | verifying axioms with elements |
    | 2 | `exercises/6d/p02_algebra_maps_compose.md` | warm-up | pasting commuting squares |
    | 3 | `exercises/6d/p03_comparison_functor.md` | core | checking algebra axioms |
    | 4 | `exercises/6d/p04_kleisli_of_powerset_is_rel.md` | core | building an isomorphism of categories |
    | 5 | `exercises/6d/p05_kleisli_embeds_in_eilenberg_moore.md` | core | building a comparison functor |
    | 6 | `exercises/6d/p06_algebras_for_free_monoid_monad.md` | stretch | translating between two definitions |

    Write each proof in `proofs/6d/<same filename>`, using the Goal / Given / Plan / Proof / What made it work layout.
    Then ask Claude to review it; the review points at gaps and asks questions, it does not rewrite your proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [6C: Adjoints & Limits](../6c_adjoints_and_limits/) | Next: [7A: Definition & Theorem Study Guide](../7a_study_guide/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
