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
    # 2A: Adjunctions: Definition & Examples

    > *"Adjoint functors arise everywhere."*
    > — Saunders Mac Lane, *Categories for the Working Mathematician*

    In Part 1 you met functors that go in opposite directions without being inverse to each other. The forgetful functor $U \colon \mathbf{Mon} \to \mathbf{Set}$ throws away the multiplication of a monoid; the free functor $F \colon \mathbf{Set} \to \mathbf{Mon}$ builds the monoid of words on a set. Neither undoes the other: $UF(S)$ is far bigger than $S$. Yet the two are tightly linked, and this module gives the link a name. The functors $F$ and $U$ are **adjoint**: a homomorphism *out of* the free monoid $F(S)$ is the same thing as a function *out of* $S$.

    That one sentence, made precise, is the definition of an adjunction: a bijection between two hom-sets, $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$, that is *natural* in both $A$ and $B$. The bijection is the easy half to state. Naturality is the half that carries the content, and it is the half that people skip in proofs. We will write both naturality conditions out in full and use them as tools.

    By the end of this module you will be able to state the definition with every quantifier in place; to prove that a given pair of functors is adjoint by building the bijection and checking the two naturality equations; to compute with transposes; to prove that initial objects are unique up to unique isomorphism and that an initial object is the same thing as a left adjoint to the functor $\mathcal{A} \to \mathbf{1}$; and to recognise an adjunction between posets (a Galois connection) by one line of inequalities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Definition: a Natural Bijection of Hom-Sets

    Start with something you know from linear algebra. Let $S$ be a set and let $F(S)$ be the vector space with basis $S$. To define a linear map $F(S) \to V$ you choose where each basis vector goes, and any choice works. So linear maps $F(S) \to V$ correspond exactly to plain functions $S \to U(V)$, where $U(V)$ is the underlying set of $V$. Two different categories are involved ($\mathbf{Vect}_k$ on one side, $\mathbf{Set}$ on the other), two functors pointing in opposite directions, and a bijection between a hom-set of one category and a hom-set of the other. That is the pattern.

    > **Definition (adjunction).** Let $\mathcal{A}$ and $\mathcal{B}$ be categories and let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be functors. An **adjunction** between $F$ and $G$ consists of, for every object $A$ of $\mathcal{A}$ and every object $B$ of $\mathcal{B}$, a bijection
    > $$\mathcal{B}(F(A), B) \;\longrightarrow\; \mathcal{A}(A, G(B)), \qquad g \longmapsto \bar{g},$$
    > whose inverse is also written with a bar, $f \mapsto \bar{f}$ (so $\bar{\bar{g}} = g$ and $\bar{\bar{f}} = f$), such that the following two **naturality** equations hold.
    >
    > **(N1) Naturality in $B$.** For all arrows $g \colon F(A) \to B$ and $q \colon B \to B'$ in $\mathcal{B}$,
    > $$\overline{q \circ g} \;=\; G(q) \circ \bar{g}.$$
    >
    > **(N2) Naturality in $A$.** For all arrows $p \colon A' \to A$ and $f \colon A \to G(B)$ in $\mathcal{A}$,
    > $$\overline{f \circ p} \;=\; \bar{f} \circ F(p).$$
    >
    > When such bijections exist we say $F$ is **left adjoint** to $G$ and $G$ is **right adjoint** to $F$, and write $F \dashv G$. The arrow $\bar{g}$ is called the **transpose** of $g$, and likewise $\bar{f}$ is the transpose of $f$.

    **Reading the definition.** To show $F \dashv G$ you must do all of the following.

    1. For every pair $(A, B)$, say what $\bar{g} \colon A \to G(B)$ is for each $g \colon F(A) \to B$. Check that $\bar{g}$ really is an arrow of $\mathcal{A}$ with that domain and codomain.
    2. For every pair $(A, B)$, say what $\bar{f} \colon F(A) \to B$ is for each $f \colon A \to G(B)$, and check it is an arrow of $\mathcal{B}$.
    3. Check the two round trips: $\bar{\bar{g}} = g$ and $\bar{\bar{f}} = f$. This is what "bijection" means.
    4. Check (N1): transposing after composing with $q$ on the $\mathcal{B}$ side equals composing with $G(q)$ after transposing.
    5. Check (N2): transposing after composing with $p$ on the $\mathcal{A}$ side equals composing with $F(p)$ after transposing.

    Two things to notice about the shape. In (N1) the bar goes from $\mathcal{B}$ to $\mathcal{A}$, and in (N2) it goes from $\mathcal{A}$ to $\mathcal{B}$. And the name "left adjoint" records where the functor sits in the hom-set: $F$ appears in the *left* slot of $\mathcal{B}(F(A), B)$, $G$ in the *right* slot of $\mathcal{A}(A, G(B))$.

    **Why this is called naturality.** For fixed $A$, (N1) says exactly that the bijections form a natural transformation between the two functors $\mathcal{B}(F(A), -)$ and $\mathcal{A}(A, G(-))$ from $\mathcal{B}$ to $\mathbf{Set}$: the naturality square at $q$ (from 1D), evaluated at an element $g$, is equation (N1). Similarly (N2) is naturality in the contravariant variable $A$. You do not need this reformulation to work with adjunctions. The two equations are what you check and what you use.

    The picture for (N1): a composable pair in $\mathcal{B}$ on top, and its image under transposition in $\mathcal{A}$ underneath.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "FA": (0, 1.6, r"$F(A)$"), "B": (2.6, 1.6, r"$B$"), "B2": (5.2, 1.6, r"$B'$"),
            "A": (0, 0, r"$A$"), "GB": (2.6, 0, r"$G(B)$"), "GB2": (5.2, 0, r"$G(B')$"),
            "pad_top": (2.6, 2.3, ""), "pad_bottom": (2.6, -0.7, ""),
        },
        [
            ("FA", "B", r"$g$"), ("B", "B2", r"$q$"),
            ("A", "GB", r"$\bar{g}$"), ("GB", "GB2", r"$G(q)$"),
            ("FA", "B2", r"$q \circ g$", {"rad": -0.35, "color": "#1d4ed8"}),
            ("A", "GB2", r"$\overline{q \circ g}$", {"rad": 0.35, "color": "#1d4ed8"}),
        ],
        figsize=(7.2, 5.0),
        title=r"(N1): top row lives in $\mathcal{B}$, bottom row in $\mathcal{A}$; the bottom triangle commutes",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example 1 (the identity).** For any category $\mathcal{A}$, the identity functor is left adjoint to itself: take $\bar{g} = g$. Both round trips are immediate, (N1) reads $q \circ g = q \circ g$ and (N2) reads $f \circ p = f \circ p$.

    **Example 2 (rounding up).** Regard the ordered sets $(\mathbb{R}, \le)$ and $(\mathbb{Z}, \le)$ as categories (1A). Let $G \colon \mathbb{Z} \to \mathbb{R}$ be the inclusion and $F \colon \mathbb{R} \to \mathbb{Z}$ the ceiling function $x \mapsto \lceil x \rceil$. For a real $x$ and an integer $n$,
    $$\lceil x \rceil \le n \iff x \le n.$$
    The left side says $\mathbb{Z}(F(x), n)$ is non-empty, the right side says $\mathbb{R}(x, G(n))$ is non-empty. Each hom-set has at most one element, so "both empty or both non-empty" is a bijection. Section 5 explains why naturality needs no checking in a poset. So $\lceil - \rceil \dashv G$.

    **Non-example (a bijection that is not natural).** Take $\mathcal{A} = \mathcal{B} = \mathbf{Set}$ and $F = G = 1_{\mathbf{Set}}$. Define a bijection $\mathbf{Set}(A, B) \to \mathbf{Set}(A, B)$ for every $A, B$ as follows: it is the identity except when $A = \{\ast\}$ and $B = \{0, 1\}$, where it swaps the two functions $\{\ast\} \to \{0, 1\}$. Every one of these maps is a bijection. But (N1) fails. Let $g$ be the function picking out $0$, so $\bar{g}$ picks out $1$, and let $q \colon \{0,1\} \to \{0,1\}$ be constant at $0$. Then $q \circ g$ picks out $0$, so $\overline{q \circ g}$ picks out $1$; but $G(q) \circ \bar{g} = q \circ \bar{g}$ picks out $q(1) = 0$. A family of bijections is not an adjunction until both naturality equations have been checked.

    ### First proof: naturality runs in both directions

    (N1) describes how $g \mapsto \bar{g}$ interacts with composition in $\mathcal{B}$. The inverse map $f \mapsto \bar{f}$ interacts with it too, and you will need this constantly.

    **Lemma 1.** Let $F \dashv G$. For all arrows $f \colon A \to G(B)$ in $\mathcal{A}$ and $q \colon B \to B'$ in $\mathcal{B}$,
    $$\textbf{(N1')} \qquad \overline{G(q) \circ f} \;=\; q \circ \bar{f}.$$

    - **Goal.** For every $A$ in $\mathcal{A}$, every $B, B'$ in $\mathcal{B}$, every $f \colon A \to G(B)$ and every $q \colon B \to B'$: the two arrows $\overline{G(q) \circ f}$ and $q \circ \bar{f}$ from $F(A)$ to $B'$ are equal.
    - **Given.** The bijections of the adjunction, with $\bar{\bar{h}} = h$ for every arrow $h$ on either side, and equation (N1).
    - **Plan.** Two arrows are equal if their transposes are equal, because transposition is a bijection. So name the arrow $\bar{f}$, apply (N1) to it, and transpose back.
    - **Proof.** Put $g = \bar{f} \colon F(A) \to B$. By (N1) applied to $g$ and $q$,
      $$\overline{q \circ g} = G(q) \circ \bar{g}.$$
      Since $g = \bar{f}$, we have $\bar{g} = \bar{\bar{f}} = f$ (the two bars are mutually inverse). So the equation reads $\overline{q \circ \bar{f}} = G(q) \circ f$. Now apply the bar to both sides. On the left, $\overline{\overline{q \circ \bar{f}}} = q \circ \bar{f}$, again because the bars are mutually inverse. On the right we get $\overline{G(q) \circ f}$. Hence $q \circ \bar{f} = \overline{G(q) \circ f}$. $\blacksquare$
    - **What made it work.** *To prove an equation between arrows on one side of an adjunction, transpose it to the other side, where a known naturality equation applies.* Reach for this whenever an expression has a bar over a composite.

    The companion statement **(N2')**, $\overline{g \circ F(p)} = \bar{g} \circ p$ for $g \colon F(A) \to B$ and $p \colon A' \to A$, is proof brief P02.

    > Reference: [Leinster §2.1](https://arxiv.org/abs/1612.09375) for the definition and the two naturality equations; [Riehl §4.1](https://math.jhu.edu/~eriehl/context.pdf) for the same definition phrased as a natural isomorphism of functors $\mathcal{A}^{\mathrm{op}} \times \mathcal{B} \to \mathbf{Set}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Free $\dashv$ Forgetful

    The most common source of adjunctions is algebra. Whenever you "forget structure" there is a functor $U$ to a simpler category, and "the free thing on" is its left adjoint. We prove one case completely, so that you see every item of the checklist discharged, and then list the others.

    **The free monoid.** For a set $S$, let $F(S)$ be the set of all finite sequences $(s_1, \ldots, s_n)$ of elements of $S$, with $n \ge 0$. These are called **words**; we write them $s_1 s_2 \cdots s_n$, and write $e$ for the empty word ($n = 0$). Multiplication is concatenation, and $e$ is the identity element, so $F(S)$ is a monoid. For a function $p \colon S' \to S$, define $F(p) \colon F(S') \to F(S)$ by $F(p)(s'_1 \cdots s'_n) = p(s'_1) \cdots p(s'_n)$. This is a monoid homomorphism, and $F$ is a functor $\mathbf{Set} \to \mathbf{Mon}$ (1C). Write $U \colon \mathbf{Mon} \to \mathbf{Set}$ for the forgetful functor, and $(s)$ for the one-letter word.

    **Theorem 2.** $F \dashv U$. Precisely: for every set $S$ and monoid $M$, the map
    $$\mathbf{Mon}(F(S), M) \to \mathbf{Set}(S, U(M)), \qquad g \mapsto \bar{g}, \quad \bar{g}(s) = g((s)),$$
    is a bijection, and these bijections satisfy (N1) and (N2).

    - **Goal.** For all sets $S$ and monoids $M$: the map $g \mapsto \bar{g}$ has a two-sided inverse; and for all homomorphisms $q \colon M \to M'$ and functions $p \colon S' \to S$, equations (N1) and (N2) hold.
    - **Given.** The definitions of $F$ on objects and arrows, the definition of a monoid homomorphism (preserves products and the identity), and the fact that every word is a product of one-letter words: $s_1 \cdots s_n = (s_1)(s_2) \cdots (s_n)$.
    - **Plan.** Follow the checklist of Section 1. Define the inverse $f \mapsto \bar{f}$ by "multiply out the word", check that $\bar f$ is a homomorphism, check both round trips, then check (N1) and (N2) by evaluating both sides on a general element.
    - **Proof.**
      *The inverse.* Given a function $f \colon S \to U(M)$, define $\bar{f} \colon F(S) \to M$ by
      $$\bar{f}(s_1 \cdots s_n) = f(s_1) \cdot f(s_2) \cdots f(s_n),$$
      the product taken in $M$, with the empty product ($n = 0$) equal to the identity $1_M$.
      *$\bar{f}$ is a homomorphism.* It sends $e$ to $1_M$ by definition. For words $v = s_1 \cdots s_n$ and $w = t_1 \cdots t_m$, $\bar{f}(vw) = f(s_1) \cdots f(s_n) f(t_1) \cdots f(t_m) = \bar{f}(v)\,\bar{f}(w)$, where regrouping the product uses associativity in $M$.
      *Round trip starting from $f$.* For $s \in S$, $\bar{\bar{f}}(s) = \bar{f}((s)) = f(s)$. So $\bar{\bar{f}} = f$, since two functions that agree on every element are equal.
      *Round trip starting from $g$.* Let $g \colon F(S) \to M$ be a homomorphism. For a word $s_1 \cdots s_n$,
      $$\bar{\bar{g}}(s_1 \cdots s_n) = \bar{g}(s_1) \cdots \bar{g}(s_n) = g((s_1)) \cdots g((s_n)) = g((s_1) \cdots (s_n)) = g(s_1 \cdots s_n).$$
      The first equality is the definition of the bar on functions, the second the definition of $\bar{g}$, the third holds because $g$ preserves products (and, when $n = 0$, because $g$ preserves the identity), and the fourth because a word is the product of its letters. So $\bar{\bar{g}} = g$.
      *(N1).* Let $g \colon F(S) \to M$ and $q \colon M \to M'$ be homomorphisms. For $s \in S$: $\overline{q \circ g}(s) = (q \circ g)((s)) = q(g((s))) = q(\bar{g}(s)) = (U(q) \circ \bar{g})(s)$, where the last step uses that $U(q)$ is the same function as $q$.
      *(N2).* Let $p \colon S' \to S$ and $f \colon S \to U(M)$ be functions. Both $\overline{f \circ p}$ and $\bar{f} \circ F(p)$ are homomorphisms $F(S') \to M$. On a word $s'_1 \cdots s'_n$ the first gives $f(p(s'_1)) \cdots f(p(s'_n))$. The second gives $\bar{f}(p(s'_1) \cdots p(s'_n)) = f(p(s'_1)) \cdots f(p(s'_n))$. They agree on every word, so they are equal. $\blacksquare$
    - **What made it work.** *A homomorphism out of a free object is determined by, and can be freely prescribed on, the generators.* The round trip $\bar{\bar{g}} = g$ is the "determined by" half, and the fact that $\bar{f}$ is a homomorphism is the "freely prescribed" half. Every free $\dashv$ forgetful proof has this shape.

    **More examples of the same kind** (stated; each is verified by the same five checks).

    | Forgetful functor $U$ | Left adjoint $F$ | The bijection says |
    |---|---|---|
    | $\mathbf{Vect}_k \to \mathbf{Set}$ | $F(S)$ = formal finite linear combinations of elements of $S$ | a linear map out of $F(S)$ is a function on the basis $S$ |
    | $\mathbf{Grp} \to \mathbf{Set}$ | $F(S)$ = the free group on $S$ (reduced words in the letters $s$ and $s^{-1}$) | a homomorphism out of $F(S)$ is a function on the generators |
    | $\mathbf{Ab} \to \mathbf{Grp}$ (inclusion) | $G \mapsto G/[G,G]$, the abelianization | a homomorphism from $G$ to an abelian group factors uniquely through $G/[G,G]$ |

    The last row shows that "forgetful" need not mean "forget down to sets": the inclusion $\mathbf{Ab} \to \mathbf{Grp}$ forgets only the *property* of being abelian.

    **Non-example.** The forgetful functor $U \colon \mathbf{Field} \to \mathbf{Set}$ has no left adjoint: there is no "free field on a set". You will be able to prove this at the end of Section 4, by combining proof brief P03 with the fact that there is no homomorphism between fields of different characteristic.

    > Reference: [Leinster §2.1](https://arxiv.org/abs/1612.09375) (algebraic examples of adjunctions); [Riehl §4.1](https://math.jhu.edu/~eriehl/context.pdf) (free $\dashv$ forgetful examples).
    """)
    return


@app.cell
def _():
    def _run():
        # Transposes for the free monoid on S = {a, b} and the monoid M = (Z/4, multiplication).
        _S = ["a", "b"]

        def _mult(x, y):
            return (x * y) % 4

        def _bar_of_function(f):
            """f : S -> U(M), as a dict.  Returns the homomorphism F(S) -> M, as a function on words."""
            def _hom(word):
                _acc = 1  # the identity of M: the empty product
                for _letter in word:
                    _acc = _mult(_acc, f[_letter])
                return _acc
            return _hom

        def _bar_of_hom(g):
            """g : F(S) -> M, a function on words.  Returns the function S -> U(M), as a dict."""
            return {_s: g((_s,)) for _s in _S}

        _f = {"a": 3, "b": 2}
        _fbar = _bar_of_function(_f)
        print("f =", _f, "  (a function S -> U(M), M = Z/4 under multiplication)")
        for _word in [(), ("a",), ("a", "a"), ("a", "b"), ("b", "b"), ("a", "b", "a")]:
            print(f"  f-bar({''.join(_word) or 'e'}) = {_fbar(_word)}")
        print("round trip: bar(bar(f)) =", _bar_of_hom(_fbar), "  (equal to f)")

        # f-bar is a homomorphism: check f-bar(vw) = f-bar(v) f-bar(w) on all words of length <= 3
        import itertools
        _words = [_w for _n in range(4) for _w in itertools.product(_S, repeat=_n)]
        _ok = all(_fbar(_v + _w) == _mult(_fbar(_v), _fbar(_w)) for _v in _words for _w in _words)
        print("f-bar(vw) = f-bar(v) f-bar(w) for all words v, w of length <= 3:", _ok)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. A Functor Can Have Adjoints on Both Sides: $D \dashv U \dashv I$

    Left and right adjoints are different jobs, and one functor can have both. The forgetful functor $U \colon \mathbf{Top} \to \mathbf{Set}$ sends a topological space to its set of points. Going back, there are two extreme ways to put a topology on a set $S$:

    - $D(S)$: the **discrete** space, in which every subset is open;
    - $I(S)$: the **indiscrete** space, in which only $\emptyset$ and $S$ are open.

    Both are functors $\mathbf{Set} \to \mathbf{Top}$ that send a function to itself. For that to make sense you must check that every function $D(S') \to D(S)$ and every function $I(S') \to I(S)$ is continuous; this is contained in the two facts used below.

    **Example ($D \dashv U$).** For a set $S$ and a space $X$, *every* function $S \to U(X)$ is continuous as a map $D(S) \to X$, because the preimage of an open set is a subset of $S$ and every subset of $D(S)$ is open. So
    $$\mathbf{Top}(D(S), X) = \mathbf{Set}(S, U(X))$$
    as sets, and the bijection $g \mapsto \bar{g}$ is "regard the continuous map as a function". Both (N1) and (N2) then say that a composite of functions is the same whether or not you remember that the functions are continuous.

    **Example ($U \dashv I$).** For a space $X$ and a set $S$, every function $U(X) \to S$ is continuous as a map $X \to I(S)$: the only open sets of $I(S)$ are $\emptyset$ and $S$, whose preimages $\emptyset$ and $X$ are open. So $\mathbf{Set}(U(X), S) = \mathbf{Top}(X, I(S))$, and $U \dashv I$. Here $U$ plays the role of the *left* adjoint.

    So we have a chain of adjunctions $D \dashv U \dashv I$: the functor in the middle is right adjoint to the one above it and left adjoint to the one below it.

    **Non-example ($U$ is not left adjoint to $D$).** The order matters. If $U \dashv D$ held, there would be a bijection $\mathbf{Set}(U(X), S) \cong \mathbf{Top}(X, D(S))$ for all $X$ and $S$. Take $X = \mathbb{R}$ with its usual topology and $S = \{0, 1\}$. A continuous map $\mathbb{R} \to D(\{0,1\})$ is constant, because $\mathbb{R}$ is connected; so the right side has exactly two elements. The left side is the set of all functions $\mathbb{R} \to \{0,1\}$, which is infinite. No bijection exists, so $U$ is not left adjoint to $D$.

    **Another chain.** The inclusion $U \colon \mathbf{Grp} \to \mathbf{Mon}$ (every group is a monoid) also has adjoints on both sides. Its right adjoint sends a monoid $M$ to its group $M^{\times}$ of invertible elements; that is proof brief P05. Its left adjoint sends $M$ to a group obtained by formally adjoining inverses; we only record its existence here.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "Top": (0, 0, r"$\mathbf{Top}$"), "Set": (4.2, 0, r"$\mathbf{Set}$"),
            "pad_top": (2.1, 1.0, ""), "pad_bottom": (2.1, -1.0, ""),
        },
        [
            ("Set", "Top", r"$D$  (discrete)", {"rad": 0.45}),
            ("Top", "Set", r"$U$", {}),
            ("Set", "Top", r"$I$  (indiscrete)", {"rad": -0.45}),
        ],
        figsize=(6.2, 4.0),
        title=r"$D \dashv U \dashv I$: left adjoint drawn above, right adjoint below",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Reference: [Leinster §2.1](https://arxiv.org/abs/1612.09375) (the adjunctions between $\mathbf{Top}$ and $\mathbf{Set}$, and between $\mathbf{Grp}$ and $\mathbf{Mon}$).

    ---

    ## 4. Initial and Terminal Objects

    Here is the smallest possible adjunction, and at the same time the first *universal property* stated in the language of this course. In $\mathbf{Set}$ the empty set has a peculiar feature: for every set $X$ there is exactly one function $\emptyset \to X$. The one-element set has the mirror-image feature: exactly one function $X \to \{\ast\}$.

    > **Definition (initial and terminal objects).** Let $\mathcal{A}$ be a category.
    > An object $I$ of $\mathcal{A}$ is **initial** if for every object $A$ of $\mathcal{A}$ there is exactly one arrow $I \to A$.
    > An object $T$ of $\mathcal{A}$ is **terminal** if for every object $A$ of $\mathcal{A}$ there is exactly one arrow $A \to T$.
    > An initial object is often written $0$ and a terminal object $1$.

    **Reading the definition.** To show $I$ is initial you must do two things *for every* object $A$:

    1. **Existence:** produce an arrow $I \to A$.
    2. **Uniqueness:** show that any two arrows $I \to A$ are equal.

    Note that $A$ ranges over all objects, including $I$ itself: there is exactly one arrow $I \to I$, and since $1_I$ is one, it is the only one. A terminal object of $\mathcal{A}$ is the same thing as an initial object of $\mathcal{A}^{\mathrm{op}}$, so every statement about initial objects has a dual about terminal objects (1B).

    **Examples.**

    - In $\mathbf{Set}$: $\emptyset$ is initial; every one-element set is terminal.
    - In $\mathbf{Grp}$: the one-element group is both initial and terminal. A homomorphism out of it must send the identity to the identity, and a map into it has no choice at all.
    - In the category of rings with identity (homomorphisms preserve $1$): $\mathbb{Z}$ is initial, since a homomorphism $\mathbb{Z} \to R$ must send $n$ to $n \cdot 1_R$.
    - In a poset regarded as a category: an initial object is a least element, a terminal object is a greatest element.

    **Non-examples.**

    - The poset $(\mathbb{Z}, \le)$ has no least and no greatest element, so it has neither an initial nor a terminal object.
    - In $\mathbf{Set}$ a two-element set $\{0,1\}$ is not terminal: there are two functions $\{\ast\} \to \{0,1\}$, so uniqueness fails. It is not initial either: there is no function $\{0,1\} \to \emptyset$, so existence fails.
    - $\mathbf{Field}$ has no initial object. An initial field $K$ would have a homomorphism to $\mathbb{Q}$ and one to $\mathbb{Z}/2$. Field homomorphisms preserve $1$ and are injective, so they preserve whether $1 + 1 = 0$; that equation is false in $\mathbb{Q}$ and true in $\mathbb{Z}/2$, so it would be both false and true in $K$.

    A category can have many terminal objects (every one-element set is terminal in $\mathbf{Set}$), and in the same way many initial objects, but they cannot be told apart by the category:

    **Lemma 3 (initial objects are unique up to unique isomorphism).** Let $I$ and $I'$ be initial objects of a category $\mathcal{A}$. Then there is exactly one isomorphism $I \to I'$.

    - **Goal.** There exists an arrow $f \colon I \to I'$ that is an isomorphism, and any isomorphism $I \to I'$ is equal to $f$.
    - **Given.** For every object $A$: exactly one arrow $I \to A$, and exactly one arrow $I' \to A$.
    - **Plan.** A uniqueness argument of the kind in 0C. Initiality hands us an arrow each way. The composites are arrows $I \to I$ and $I' \to I'$, and initiality says there is only one such arrow each, which must be the identity.
    - **Proof.** Since $I$ is initial, there is an arrow $f \colon I \to I'$. Since $I'$ is initial, there is an arrow $f' \colon I' \to I$. The composite $f' \circ f$ is an arrow $I \to I$. So is $1_I$. Since $I$ is initial there is exactly one arrow $I \to I$; hence $f' \circ f = 1_I$. In the same way, $f \circ f'$ and $1_{I'}$ are both arrows $I' \to I'$, and $I'$ is initial, so $f \circ f' = 1_{I'}$. Thus $f$ is an isomorphism with inverse $f'$. For uniqueness: any isomorphism $I \to I'$ is in particular an arrow $I \to I'$, and there is exactly one such arrow because $I$ is initial. $\blacksquare$
    - **What made it work.** *Uniqueness of arrows out of $I$ was used three times, each time to conclude that two arrows with the same domain $I$ and the same codomain are equal.* This is the template for every "unique up to unique isomorphism" proof in the course.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"I": (0, 0, r"$I$"), "J": (3, 0, r"$I'$")},
        [
            ("I", "J", r"$f$", {"rad": -0.3, "dashed": True}),
            ("J", "I", r"$f'$", {"rad": -0.3, "dashed": True}),
            ("I", "I", r"$1_I$", {"loop": "left"}),
            ("J", "J", r"$1_{I'}$", {"loop": "right"}),
        ],
        figsize=(6.6, 3.0),
        title=r"Only one arrow $I \rightarrow I$ and only one $I' \rightarrow I'$, so $f' \circ f = 1_I$ and $f \circ f' = 1_{I'}$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Initial objects are left adjoints

    Let $\mathbf{1}$ be the category with one object $\star$ and one arrow $1_\star$. Every category $\mathcal{A}$ has exactly one functor $! \colon \mathcal{A} \to \mathbf{1}$. A functor $F \colon \mathbf{1} \to \mathcal{A}$ is the same thing as a choice of an object $F(\star)$ of $\mathcal{A}$ (it must send $1_\star$ to the identity).

    **Proposition 4.** Let $F \colon \mathbf{1} \to \mathcal{A}$ be a functor and put $I = F(\star)$. Then $F \dashv\, !$ if and only if $I$ is an initial object of $\mathcal{A}$.

    - **Goal.** Two implications. (⇒) If there are bijections $\mathcal{A}(F(\star), A) \to \mathbf{1}(\star, !(A))$ satisfying (N1) and (N2), then for every $A$ there is exactly one arrow $I \to A$. (⇐) If $I$ is initial, then such bijections exist and satisfy (N1) and (N2).
    - **Given.** $!(A) = \star$ for every $A$, so $\mathbf{1}(\star, !(A)) = \mathbf{1}(\star, \star) = \{1_\star\}$, a one-element set. The only arrow of $\mathbf{1}$ is $1_\star$, and $F(1_\star) = 1_I$ because functors preserve identities.
    - **Plan.** Unpack the definition of adjunction for these particular functors. One of the two hom-sets always has exactly one element, so the bijection says the other one does too.
    - **Proof.**
      (⇒) Fix an object $A$. The adjunction gives a bijection between $\mathcal{A}(I, A)$ and the one-element set $\{1_\star\}$. A set in bijection with a one-element set has exactly one element. So there is exactly one arrow $I \to A$. As $A$ was arbitrary, $I$ is initial.
      (⇐) Suppose $I$ is initial. For each $A$, the set $\mathcal{A}(I, A)$ has exactly one element, and so does $\mathbf{1}(\star, \star)$; the only function between them, $g \mapsto \bar{g} = 1_\star$, is a bijection. *(N1):* for $g \colon I \to A$ and $q \colon A \to A'$, both $\overline{q \circ g}$ and $!(q) \circ \bar{g}$ are arrows $\star \to \star$ in $\mathbf{1}$, and there is only one such arrow, so they are equal. *(N2):* the arrow $p$ in (N2) is an arrow of $\mathbf{1}$, so $p = 1_\star$. For $f \colon \star \to\, !(A)$ we get $\overline{f \circ 1_\star} = \bar{f}$ by the identity axiom in $\mathbf{1}$, and $\bar{f} \circ F(1_\star) = \bar{f} \circ 1_I = \bar{f}$ by the identity axiom in $\mathcal{A}$. So both sides of (N2) equal $\bar{f}$. $\blacksquare$
    - **What made it work.** *Equations between arrows in a hom-set with one element hold automatically.* When a hom-set has at most one element, naturality costs nothing. The same observation powers the next section.

    **Dually,** a functor $\mathbf{1} \to \mathcal{A}$ is *right* adjoint to $!$ if and only if the object it picks out is terminal. The proof is the mirror image: the bijection is now $\mathbf{1}(!(A), \star) \cong \mathcal{A}(A, T)$.

    > Reference: [Leinster §2.1](https://arxiv.org/abs/1612.09375) (initial and terminal objects; their uniqueness; their description as adjoints).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Galois Connections: Adjunctions Between Posets

    A poset $(P, \le)$ is a category with one arrow $a \to a'$ when $a \le a'$ and none otherwise (1A). A functor between posets is an order-preserving map (1C). What is an adjunction between two such functors? Every hom-set has zero or one elements, so nearly everything in the definition collapses, and what remains is a single condition on inequalities. These are the adjunctions you can compute completely by hand, and the ones the Compute It exercises use.

    > **Definition (Galois connection).** Let $P$ and $Q$ be posets and let $f \colon P \to Q$ and $g \colon Q \to P$ be order-preserving maps. The pair $(f, g)$ is a **Galois connection**, with $f$ the left adjoint and $g$ the right adjoint, if for all $a \in P$ and all $b \in Q$,
    > $$f(a) \le b \iff a \le g(b).$$

    **Reading the definition.**

    1. $f$ and $g$ must each be order-preserving. That is part of the data, not a consequence you may assume silently.
    2. The condition is an "if and only if" for *every* pair $(a, b)$: two implications to prove.
    3. $f$ sits on the *small* side of its inequality, $g$ on the *large* side. This is the same "left slot, right slot" as in $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$.

    **Why this is exactly an adjunction $f \dashv g$.** The hom-set $Q(f(a), b)$ has one element if $f(a) \le b$ and is empty otherwise; likewise $P(a, g(b))$. A bijection between two sets with at most one element each exists precisely when both are empty or both are non-empty, which is the displayed "iff"; and when it exists it is the only function between them. Naturality is automatic: (N1) and (N2) are equations between two arrows of a poset with the same domain and codomain, and a poset has at most one arrow between any two objects. So the two notions coincide.

    **Example (direct and inverse image).** Let $h \colon K \to L$ be a function between sets. The power sets $\mathscr{P}(K)$ and $\mathscr{P}(L)$ are posets under $\subseteq$. Direct image $h_* \colon \mathscr{P}(K) \to \mathscr{P}(L)$, $S \mapsto \{h(s) : s \in S\}$, and inverse image $h^{*} \colon \mathscr{P}(L) \to \mathscr{P}(K)$, $T \mapsto \{k \in K : h(k) \in T\}$, are both order-preserving. For $S \subseteq K$ and $T \subseteq L$:
    $$h_*(S) \subseteq T \iff \text{for all } s \in S,\ h(s) \in T \iff S \subseteq h^{*}(T).$$
    So $h_* \dashv h^{*}$.

    **Example (floor and ceiling).** With $G \colon \mathbb{Z} \to \mathbb{R}$ the inclusion, $\lceil x \rceil \le n \iff x \le n$ gives $\lceil - \rceil \dashv G$, and $n \le x \iff n \le \lfloor x \rfloor$ gives $G \dashv \lfloor - \rfloor$. Another chain of three.

    **Example (halving).** Let $f \colon \mathbb{N} \to \mathbb{N}$ be $f(a) = \lfloor a/2 \rfloor$ and $g(b) = 2b + 1$. Then $\lfloor a/2 \rfloor \le b \iff a \le 2b + 1$, so $f \dashv g$.

    **Non-example.** The inclusion $g \colon \mathbb{Q} \to \mathbb{R}$ has no left adjoint. A left adjoint $f$ would satisfy $f(x) \le q \iff x \le q$ for all real $x$ and rational $q$. Taking $q = f(x)$, the left side holds, so $x \le f(x)$; and every rational $q \ge x$ satisfies $f(x) \le q$. So $f(x)$ would be the least rational number that is $\ge x$. For $x = \sqrt{2}$ there is no such rational: $\sqrt{2}$ is irrational, and between $\sqrt{2}$ and any larger rational there is a smaller rational.

    The last non-example is an instance of a general fact: in a Galois connection each map is determined by the other, by an explicit formula. We prove the version for the right adjoint; the version for the left adjoint ("$f(a)$ is the least $b$ with $a \le g(b)$") is its mirror image, and is what the non-example derived by hand.

    **Proposition 5.** Let $f \colon P \to Q$ and $g \colon Q \to P$ be order-preserving maps of posets with $f \dashv g$. Then for every $b \in Q$, the element $g(b)$ is the greatest element of the set $D_b = \{a \in P : f(a) \le b\}$.

    - **Goal.** For every $b \in Q$: (i) $g(b) \in D_b$, that is, $f(g(b)) \le b$; and (ii) every $a \in D_b$ satisfies $a \le g(b)$.
    - **Given.** For all $a, b$: $f(a) \le b \iff a \le g(b)$. Reflexivity of $\le$ in $P$.
    - **Plan.** Direct proof. Each of (i) and (ii) is one direction of the "iff", applied to a well-chosen $a$.
    - **Proof.** Fix $b \in Q$.
      (i) By reflexivity, $g(b) \le g(b)$. Apply the "iff" with $a = g(b)$, reading it from right to left: $f(g(b)) \le b$. So $g(b) \in D_b$.
      (ii) Let $a \in D_b$, so $f(a) \le b$. Reading the "iff" from left to right gives $a \le g(b)$.
      Hence $g(b)$ belongs to $D_b$ and is $\ge$ every element of $D_b$: it is the greatest element. $\blacksquare$
    - **What made it work.** *Feed the trivial inequality $g(b) \le g(b)$ into the adjunction.* Applying an adjunction to an identity arrow is the single most productive move in this subject; in 2B it produces the unit and counit.

    A set has at most one greatest element (antisymmetry), so Proposition 5 shows that $f$ has **at most one** right adjoint. In a general category the statement becomes "unique up to isomorphism", proved in 2C.

    Explore it. Choose two finite posets and an order-preserving map $f \colon P \to Q$. The picture shows $f$ in blue, and its right adjoint $g$ in red if one exists. When there is none, the title names an element $b$ for which $D_b$ has no greatest element.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _names = [
        "chain 0 < 1 < 2",
        "chain 0 < 1 < 2 < 3",
        "diamond: divisors of 6",
        "wedge: x, y below t",
        "antichain: p, q",
    ]
    poset_p = mo.ui.dropdown(options=_names, value="chain 0 < 1 < 2 < 3", label="Poset P (domain of f)")
    poset_q = mo.ui.dropdown(options=_names, value="chain 0 < 1 < 2", label="Poset Q (codomain of f)")
    mo.vstack([mo.md("**Galois-connection explorer**"), poset_p, poset_q])
    return poset_p, poset_q


@app.cell(hide_code=True)
def _(mo, poset_p, poset_q):
    def _options():
        import itertools

        def _poset(name):
            _data = {
                "chain 0 < 1 < 2": ([0, 1, 2], [(0, 1), (1, 2)]),
                "chain 0 < 1 < 2 < 3": ([0, 1, 2, 3], [(0, 1), (1, 2), (2, 3)]),
                "diamond: divisors of 6": ([1, 2, 3, 6], [(1, 2), (1, 3), (2, 6), (3, 6)]),
                "wedge: x, y below t": (["x", "y", "t"], [("x", "t"), ("y", "t")]),
                "antichain: p, q": (["p", "q"], []),
            }
            _els, _covers = _data[name]
            _leq = {(_a, _a) for _a in _els} | set(_covers)
            for _k in _els:
                for _i in _els:
                    for _j in _els:
                        if (_i, _k) in _leq and (_k, _j) in _leq:
                            _leq.add((_i, _j))
            return _els, _leq

        _pe, _pleq = _poset(poset_p.value)
        _qe, _qleq = _poset(poset_q.value)
        _out = {}
        for _vals in itertools.product(_qe, repeat=len(_pe)):
            _f = dict(zip(_pe, _vals))
            if all((_f[_a], _f[_b]) in _qleq for (_a, _b) in _pleq):
                _label = ",  ".join(f"{_a} -> {_f[_a]}" for _a in _pe)
                _out[_label] = tuple(_vals)
        return _out

    _opts = _options()
    f_choice = mo.ui.dropdown(
        options=_opts, value=list(_opts)[0],
        label=f"order-preserving map f : P -> Q   ({len(_opts)} of them)",
    )
    f_choice
    return (f_choice,)


@app.cell(hide_code=True)
def _(f_choice, poset_p, poset_q):
    def _run():
        import logging
        logging.getLogger("matplotlib").setLevel(logging.ERROR)
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch

        def _poset(name):
            _data = {
                "chain 0 < 1 < 2": ([0, 1, 2], [(0, 1), (1, 2)], {0: (0, 0), 1: (0, 1), 2: (0, 2)}),
                "chain 0 < 1 < 2 < 3": ([0, 1, 2, 3], [(0, 1), (1, 2), (2, 3)],
                                        {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3)}),
                "diamond: divisors of 6": ([1, 2, 3, 6], [(1, 2), (1, 3), (2, 6), (3, 6)],
                                           {1: (0, 0), 2: (-0.7, 1), 3: (0.7, 1), 6: (0, 2)}),
                "wedge: x, y below t": (["x", "y", "t"], [("x", "t"), ("y", "t")],
                                        {"x": (-0.7, 0), "y": (0.7, 0), "t": (0, 1)}),
                "antichain: p, q": (["p", "q"], [], {"p": (-0.7, 0), "q": (0.7, 0)}),
            }
            _els, _covers, _pos = _data[name]
            _leq = {(_a, _a) for _a in _els} | set(_covers)
            for _k in _els:
                for _i in _els:
                    for _j in _els:
                        if (_i, _k) in _leq and (_k, _j) in _leq:
                            _leq.add((_i, _j))
            return _els, _covers, _pos, _leq

        def _extreme(subset, leq, greatest):
            for _c in subset:
                if all(((_x, _c) in leq) if greatest else ((_c, _x) in leq) for _x in subset):
                    return _c
            return None

        _pe, _pc, _ppos, _pleq = _poset(poset_p.value)
        _qe, _qc, _qpos, _qleq = _poset(poset_q.value)
        _f = dict(zip(_pe, f_choice.value))

        # right adjoint: g(b) = greatest a with f(a) <= b
        _g, _g_fail = {}, None
        for _b in _qe:
            _m = _extreme([_a for _a in _pe if (_f[_a], _b) in _qleq], _pleq, True)
            if _m is None:
                _g_fail = _b
                break
            _g[_b] = _m
        # left adjoint: l(b) = least a with b <= f(a)
        _l, _l_fail = {}, None
        for _b in _qe:
            _m = _extreme([_a for _a in _pe if (_b, _f[_a]) in _qleq], _pleq, False)
            if _m is None:
                _l_fail = _b
                break
            _l[_b] = _m

        _fig, _ax = plt.subplots(figsize=(7.4, 4.6))
        _shift = 3.6
        _P = {_a: _ppos[_a] for _a in _pe}
        _Q = {_b: (_qpos[_b][0] + _shift, _qpos[_b][1]) for _b in _qe}
        for (_u, _v) in _pc:
            _ax.plot([_P[_u][0], _P[_v][0]], [_P[_u][1], _P[_v][1]], color="#9ca3af", lw=1.5, zorder=1)
        for (_u, _v) in _qc:
            _ax.plot([_Q[_u][0], _Q[_v][0]], [_Q[_u][1], _Q[_v][1]], color="#9ca3af", lw=1.5, zorder=1)
        for _a in _pe:
            _ax.text(*_P[_a], str(_a), ha="center", va="center", fontsize=13, zorder=4,
                     bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec="#1f2937"))
        for _b in _qe:
            _ax.text(*_Q[_b], str(_b), ha="center", va="center", fontsize=13, zorder=4,
                     bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec="#1f2937"))
        for _a in _pe:
            _ax.add_patch(FancyArrowPatch(_P[_a], _Q[_f[_a]], connectionstyle="arc3,rad=0.12",
                                          arrowstyle="-|>", mutation_scale=12, shrinkA=13, shrinkB=13,
                                          color="#1d4ed8", lw=1.2, zorder=2))
        if _g_fail is None:
            for _b in _qe:
                _ax.add_patch(FancyArrowPatch(_Q[_b], _P[_g[_b]], connectionstyle="arc3,rad=0.12",
                                              arrowstyle="-|>", mutation_scale=12, shrinkA=13, shrinkB=13,
                                              color="#dc2626", lw=1.2, linestyle="--", zorder=2))
            _right = "right adjoint g (red):  " + ",  ".join(f"{_b} -> {_g[_b]}" for _b in _qe)
        else:
            _right = f"no right adjoint: {{a : f(a) <= {_g_fail}}} has no greatest element"
        if _l_fail is None:
            _left = "left adjoint of f:  " + ",  ".join(f"{_b} -> {_l[_b]}" for _b in _qe)
        else:
            _left = f"no left adjoint: {{a : {_l_fail} <= f(a)}} has no least element"
        _ys = [_p[1] for _p in list(_P.values()) + list(_Q.values())]
        _ax.text(0, max(_ys) + 0.75, "P", ha="center", fontsize=13, weight="bold")
        _ax.text(_shift, max(_ys) + 0.75, "Q", ha="center", fontsize=13, weight="bold")
        _ax.set_xlim(-1.5, _shift + 1.5)
        _ax.set_ylim(min(_ys) - 0.6, max(_ys) + 1.2)
        _ax.set_aspect("equal")
        _ax.axis("off")
        _ax.set_title("f in blue.  " + _right + "\n" + _left, fontsize=10)
        _fig.tight_layout()
        return _fig

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try. With $P$ the 4-chain and $Q$ the 3-chain, find a map with a right adjoint but no left adjoint. Then take $P$ to be the wedge and find a map into a chain with no right adjoint; look at which set $D_b$ fails to have a greatest element. Finally take $Q$ to be the antichain: which order-preserving maps into it have adjoints at all?

    The next cell converts a Galois connection to the course's finite-category encoding and checks the definition of Section 1 literally: for every pair of objects, the two hom-sets have the same number of elements.

    > Reference: [Leinster §2.1](https://arxiv.org/abs/1612.09375) (adjunctions between ordered sets appear among the examples and are developed further in §2.2); [Riehl §4.1](https://math.jhu.edu/~eriehl/context.pdf) (Galois connections as adjunctions between posets).
    """)
    return


@app.cell
def _():
    def _run():
        def _poset_cat(elements, leq):
            """The poset (elements, leq) in the finite-category encoding."""
            _arrows = {f"{_a}<={_b}": (_a, _b) for _a in elements for _b in elements if leq(_a, _b)}
            _compose = {}
            for _gname, (_b1, _c) in _arrows.items():
                for _fname, (_a, _b2) in _arrows.items():
                    if _b1 == _b2:
                        _compose[(_gname, _fname)] = f"{_a}<={_c}"
            return {
                "objects": list(elements),
                "arrows": _arrows,
                "identity": {_a: f"{_a}<={_a}" for _a in elements},
                "compose": _compose,
            }

        def _hom(cat, x, y):
            return [_n for _n, (_d, _c) in cat["arrows"].items() if _d == x and _c == y]

        _catP = _poset_cat(range(6), lambda _a, _b: _a <= _b)      # the chain 0 < 1 < ... < 5
        _catQ = _poset_cat(range(3), lambda _a, _b: _a <= _b)      # the chain 0 < 1 < 2
        _F = {"objects": {_a: _a // 2 for _a in range(6)}}          # f(a) = floor(a / 2)
        _G = {"objects": {_b: 2 * _b + 1 for _b in range(3)}}       # g(b) = 2b + 1
        _F["arrows"] = {_n: f"{_F['objects'][_a]}<={_F['objects'][_b]}" for _n, (_a, _b) in _catP["arrows"].items()}
        _G["arrows"] = {_n: f"{_G['objects'][_a]}<={_G['objects'][_b]}" for _n, (_a, _b) in _catQ["arrows"].items()}

        print("P has", len(_catP["arrows"]), "arrows;  Q has", len(_catQ["arrows"]), "arrows")
        print("\n|Q(f(a), b)| and |P(a, g(b))| for every pair (a, b):")
        print("   a  b   |Q(f a, b)|  |P(a, g b)|")
        _all_match = True
        for _a in _catP["objects"]:
            for _b in _catQ["objects"]:
                _left = len(_hom(_catQ, _F["objects"][_a], _b))
                _right = len(_hom(_catP, _a, _G["objects"][_b]))
                _all_match = _all_match and (_left == _right)
                print(f"   {_a}  {_b}        {_left}            {_right}")
        print("hom-sets match for every pair:", _all_match)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Products and Function Sets: Two Adjunctions Inside $\mathbf{Set}$

    Adjunctions also describe constructions *within* a single category. Two of the most familiar constructions on sets, the product $X \times Y$ and the set $C^B$ of all functions $B \to C$, are each one half of an adjunction.

    ### 6.1 The diagonal functor and products

    Let $\Delta \colon \mathbf{Set} \to \mathbf{Set} \times \mathbf{Set}$ be the **diagonal functor**, $\Delta(A) = (A, A)$ and $\Delta(p) = (p, p)$; the product category is from 1B. Let $\Pi \colon \mathbf{Set} \times \mathbf{Set} \to \mathbf{Set}$ be the product functor, $\Pi(X, Y) = X \times Y$ and $\Pi(q_1, q_2) = q_1 \times q_2$, the function $(x, y) \mapsto (q_1(x), q_2(y))$.

    **Example ($\Delta \dashv \Pi$).** An arrow $\Delta(A) \to (X, Y)$ in $\mathbf{Set} \times \mathbf{Set}$ is a pair $(g_1, g_2)$ of functions $g_1 \colon A \to X$, $g_2 \colon A \to Y$. Its transpose is the single function
    $$\overline{(g_1, g_2)} \colon A \to X \times Y, \qquad a \mapsto (g_1(a), g_2(a)).$$
    In the other direction, a function $f \colon A \to X \times Y$ transposes to the pair $(\pi_1 \circ f, \pi_2 \circ f)$, where $\pi_1, \pi_2$ are the projections. The round trips are the statements "a point of $X \times Y$ is determined by its two coordinates" and "the coordinates of $(g_1(a), g_2(a))$ are $g_1(a)$ and $g_2(a)$". For (N1), take $(q_1, q_2) \colon (X, Y) \to (X', Y')$: both sides send $a$ to $(q_1 g_1(a), q_2 g_2(a))$. For (N2), take $p \colon A' \to A$: both sides are the pair $(\pi_1 f p, \pi_2 f p)$. So the product is right adjoint to the diagonal.

    On the other side, the disjoint union $X + Y$ gives a *left* adjoint to $\Delta$: a function out of $X + Y$ is a pair of functions, one out of $X$ and one out of $Y$. So again we have a chain of three, $+ \dashv \Delta \dashv \times$. Products and sums in general categories are the subject of Part 5.

    ### 6.2 Functions of two variables

    Fix a set $B$. There are functors $- \times B \colon \mathbf{Set} \to \mathbf{Set}$, sending $A$ to $A \times B$ and $p \colon A' \to A$ to $p \times 1_B$, and $(-)^B \colon \mathbf{Set} \to \mathbf{Set}$, sending $C$ to the set $C^B$ of all functions $B \to C$ and $q \colon C \to C'$ to the function $q \circ - \colon C^B \to C'^B$.

    **Theorem 6.** For every set $B$, $(- \times B) \dashv (-)^B$. That is, there is a bijection
    $$\boxed{\;\mathbf{Set}(A \times B, C) \;\cong\; \mathbf{Set}(A, C^B)\;}$$
    natural in $A$ and $C$.

    - **Goal.** For all sets $A$, $C$: a bijection $g \mapsto \bar{g}$ from functions $A \times B \to C$ to functions $A \to C^B$, satisfying (N1) for all $q \colon C \to C'$ and (N2) for all $p \colon A' \to A$.
    - **Given.** The definitions of the two functors on objects and on arrows. Two functions are equal when they agree on every element.
    - **Plan.** The checklist of Section 1. A function of two variables becomes, for each fixed value of the first variable, a function of the second. Every verification is "evaluate both sides on an element".
    - **Proof.**
      *The maps.* For $g \colon A \times B \to C$ define $\bar{g} \colon A \to C^B$ by letting $\bar{g}(a)$ be the function $b \mapsto g(a, b)$. For $f \colon A \to C^B$ define $\bar{f} \colon A \times B \to C$ by $\bar{f}(a, b) = f(a)(b)$.
      *Round trips.* $\bar{\bar{g}}(a, b) = \bar{g}(a)(b) = g(a, b)$, so $\bar{\bar{g}} = g$. And $\bar{\bar{f}}(a)$ is the function $b \mapsto \bar{f}(a, b) = f(a)(b)$, which is the function $f(a)$; so $\bar{\bar{f}} = f$.
      *(N1).* Let $g \colon A \times B \to C$ and $q \colon C \to C'$. For $a \in A$, $\overline{q \circ g}(a)$ is the function $b \mapsto q(g(a, b))$. On the other side, $(q \circ -)(\bar{g}(a)) = q \circ \bar{g}(a)$ is the function $b \mapsto q(\bar{g}(a)(b)) = q(g(a, b))$. They agree for every $a$ and $b$.
      *(N2).* Let $p \colon A' \to A$ and $f \colon A \to C^B$. For $(a', b) \in A' \times B$: $\overline{f \circ p}(a', b) = f(p(a'))(b)$, and $(\bar{f} \circ (p \times 1_B))(a', b) = \bar{f}(p(a'), b) = f(p(a'))(b)$. $\blacksquare$
    - **What made it work.** *Write down what each side does to an element, with every bracket in place.* The only difficulty is bookkeeping: $\bar{g}(a)$ is itself a function, and (N1) is an equation between functions whose values are functions.

    **Non-example.** For a set $B$ with at least two elements, $- \times B$ is not *right* adjoint to anything. If $L \dashv (- \times B)$, then taking $A = \{\ast\}$ and $C = \{\ast\}$ in the hom-set bijection would give a bijection between $\mathbf{Set}(L(\{\ast\}), \{\ast\})$, which has exactly one element, and $\mathbf{Set}(\{\ast\}, \{\ast\} \times B)$, which has as many elements as $B$.

    **Summary of this module's examples.**

    | Left adjoint | Right adjoint | Categories |
    |---|---|---|
    | free monoid / group / vector space | forgetful functor | $\mathbf{Set} \rightleftarrows \mathbf{Mon}, \mathbf{Grp}, \mathbf{Vect}_k$ |
    | abelianization | inclusion | $\mathbf{Grp} \rightleftarrows \mathbf{Ab}$ |
    | discrete space $D$ | forgetful $U$ | $\mathbf{Set} \rightleftarrows \mathbf{Top}$ |
    | forgetful $U$ | indiscrete space $I$ | $\mathbf{Top} \rightleftarrows \mathbf{Set}$ |
    | an initial object | $! \colon \mathcal{A} \to \mathbf{1}$ | $\mathbf{1} \rightleftarrows \mathcal{A}$ |
    | $! \colon \mathcal{A} \to \mathbf{1}$ | a terminal object | $\mathcal{A} \rightleftarrows \mathbf{1}$ |
    | direct image $h_*$ | inverse image $h^*$ | $\mathscr{P}(K) \rightleftarrows \mathscr{P}(L)$ |
    | ceiling | inclusion $\mathbb{Z} \to \mathbb{R}$ | $\mathbb{R} \rightleftarrows \mathbb{Z}$ |
    | diagonal $\Delta$ | product $\times$ | $\mathbf{Set} \rightleftarrows \mathbf{Set} \times \mathbf{Set}$ |
    | $- \times B$ | $(-)^B$ | $\mathbf{Set} \rightleftarrows \mathbf{Set}$ |

    > Reference: [Leinster §2.1](https://arxiv.org/abs/1612.09375) (products, sums and function sets as adjoints); the set-theoretic constructions themselves are revisited in 3A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Stopping at the bijection.** *Diagnosis:* an adjunction is a bijection **plus** (N1) and (N2). The non-example in Section 1 is a family of bijections that fails (N1). A proof of $F \dashv G$ that never mentions an arrow $q \colon B \to B'$ or $p \colon A' \to A$ is incomplete.
    2. **Getting the direction backwards.** *Diagnosis:* $F \dashv G$ means $F$ is in the left slot: arrows *out of* $F(A)$ correspond to arrows *into* $G(B)$. "Free is left adjoint to forgetful" and "$f(a) \le b \iff a \le g(b)$" are worth memorising as anchors. Section 3 shows that $D \dashv U$ holds while $U \dashv D$ fails.
    3. **Forgetting that a transpose must be an arrow of the right category.** *Diagnosis:* in Theorem 2, $\bar{f}$ had to be shown to be a *monoid homomorphism*, not just a function. Until that is done, $\bar{f}$ is not an element of $\mathbf{Mon}(F(S), M)$ and the map $f \mapsto \bar{f}$ is not yet defined.
    4. **Proving "initial" by exhibiting one arrow.** *Diagnosis:* "exactly one" is existence *and* uniqueness, for every object. Exhibiting $\emptyset \to X$ shows existence; you must also say why any two such functions are equal.
    5. **Treating a Galois connection as one implication.** *Diagnosis:* $f(a) \le b \iff a \le g(b)$ is two implications, and $f$ and $g$ must both be order-preserving. Proving only "⇒" shows much less.

    ---

    ## Why This Matters

    - **2B** applies the bijection to identity arrows, producing the unit $\eta_A = \overline{1_{F(A)}}$ and counit $\varepsilon_B = \overline{1_{G(B)}}$, and shows that the whole adjunction can be rebuilt from them. Lemma 1 is used there repeatedly, and brief P02 in the exercises.
    - **2C** recasts the definition a third time: $F \dashv G$ exactly when each $\eta_A$ is an *initial object* of a suitable category. Lemma 3 (uniqueness of initial objects) then proves that adjoints are unique up to isomorphism.
    - **3A** looks closely at the set-theoretic constructions of Section 6.
    - **4A** observes that $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$ says the functor $\mathcal{A}(A, G(-))$ is *representable*.
    - **Part 5 and 6A** define limits; the adjunction $\Delta \dashv \times$ of Section 6.1 is the prototype for "limits are right adjoint to a diagonal functor".
    - **6C** proves the theorem that explains why right adjoints such as $U \colon \mathbf{Grp} \to \mathbf{Set}$ respect products, and uses Galois connections as the fully worked case of the adjoint functor theorem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Your turn. Each exercise gives a skeleton with the essential lines left as `# TODO`. Fill them in, then un-comment the `print` checks and compare with the expected values. A finite poset is given as a list of elements together with a function `leq(a, b)`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Is this pair a Galois connection?

    Write `is_galois(P, leqP, Q, leqQ, f, g)`, where `f` and `g` are dicts. It should return `True` exactly when $f$ and $g$ are both order-preserving and $f(a) \le b \iff a \le g(b)$ for all $a \in P$, $b \in Q$.
    """)
    return


@app.cell
def _():
    def _run():
        def is_galois(P, leqP, Q, leqQ, f, g):
            # TODO: check f is order-preserving and g is order-preserving
            monotone = ...
            # TODO: check  leqQ(f[a], b) == leqP(a, g[b])  for every a in P and b in Q
            adjoint = ...
            return monotone and adjoint

        P = list(range(6))                    # chain 0 < 1 < ... < 5
        Q = list(range(3))                    # chain 0 < 1 < 2
        leq = lambda a, b: a <= b
        f = {a: a // 2 for a in P}
        g_good = {b: 2 * b + 1 for b in Q}
        g_bad = {b: 2 * b for b in Q}

        # print(is_galois(P, leq, Q, leq, f, g_good))   # expect True
        # print(is_galois(P, leq, Q, leq, f, g_bad))    # expect False

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Count the Galois connections between two posets

    The helper `monotone_maps(P, leqP, Q, leqQ)`, provided, lists every order-preserving map $P \to Q$ as a dict. Write `galois_pairs(P, leqP, Q, leqQ)` returning the list of **all** pairs `(f, g)` with $f \colon P \to Q$ and $g \colon Q \to P$ order-preserving and $f(a) \le b \iff a \le g(b)$ for all $a$, $b$. Use brute force over both lists; do not compute $g$ from $f$.

    Then look at what the counts say. In each example, does any $f$ occur in two different pairs? Which result of Section 5 predicted that? And which order-preserving maps occur in no pair at all?
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def monotone_maps(P, leqP, Q, leqQ):
            """All order-preserving maps P -> Q, each as a dict."""
            found = []
            for values in itertools.product(Q, repeat=len(P)):
                f = dict(zip(P, values))
                if all(leqQ(f[a], f[b]) for a in P for b in P if leqP(a, b)):
                    found.append(f)
            return found

        def galois_pairs(P, leqP, Q, leqQ):
            # TODO: every (f, g), f from monotone_maps(P, leqP, Q, leqQ), g from monotone_maps(Q, leqQ, P, leqP),
            #       such that  leqQ(f[a], b) == leqP(a, g[b])  for every a in P and b in Q
            return ...

        chain2, chain3, chain4 = [0, 1], [0, 1, 2], [0, 1, 2, 3]
        leq = lambda a, b: a <= b
        wedge = ["x", "y", "t"]                         # x < t and y < t, x and y incomparable
        leq_wedge = lambda a, b: a == b or b == "t"

        # print(len(monotone_maps(chain3, leq, chain2, leq)), len(galois_pairs(chain3, leq, chain2, leq)))   # expect 4 3
        # print(len(monotone_maps(chain4, leq, chain3, leq)), len(galois_pairs(chain4, leq, chain3, leq)))   # expect 15 10
        # print(len(galois_pairs(wedge, leq_wedge, chain2, leq)))    # expect 3
        # print(len(galois_pairs(chain2, leq, wedge, leq_wedge)))    # expect 0
        # print(galois_pairs(chain3, leq, chain2, leq)[1])           # expect ({0: 0, 1: 0, 2: 1}, {0: 1, 1: 2})

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Initial and terminal objects of a finite category

    Write `initial_objects(cat)` and `terminal_objects(cat)` for a category in the shared finite-category encoding (`cat["arrows"][name] = (domain, codomain)`). An object is initial when it has exactly one arrow to every object (itself included), terminal when it has exactly one arrow from every object. Compare each answer with Section 4: least and greatest elements of a poset, and Lemma 3 for the last example.
    """)
    return


@app.cell
def _():
    def _run():
        def hom_size(cat, x, y):
            return sum(1 for (d, c) in cat["arrows"].values() if d == x and c == y)

        def initial_objects(cat):
            # TODO: the objects x with hom_size(cat, x, y) == 1 for every object y
            return ...

        def terminal_objects(cat):
            # TODO: the objects y with hom_size(cat, x, y) == 1 for every object x
            return ...

        def arrows_of_poset(elements, leq):
            # only the "objects" and "arrows" of the encoding are needed in this exercise
            return {"objects": list(elements),
                    "arrows": {f"{a}<={b}": (a, b) for a in elements for b in elements if leq(a, b)}}

        divides = lambda a, b: b % a == 0
        D12 = arrows_of_poset([1, 2, 3, 4, 6, 12], divides)
        PROPER = arrows_of_poset([2, 3, 4, 6], divides)          # divisors of 12 other than 1 and 12

        Z3 = {"objects": ["*"], "arrows": {n: ("*", "*") for n in "012"}}     # the group Z/3

        PAIR = {"objects": ["X", "Y"],                                         # a parallel pair s, t : X -> Y
                "arrows": {"1X": ("X", "X"), "1Y": ("Y", "Y"), "s": ("X", "Y"), "t": ("X", "Y")}}

        ISO = {"objects": ["P", "Q"],                                          # mutually inverse u : P -> Q, v : Q -> P
               "arrows": {"1P": ("P", "P"), "1Q": ("Q", "Q"), "u": ("P", "Q"), "v": ("Q", "P")}}

        # print(initial_objects(D12), terminal_objects(D12))         # expect [1] [12]
        # print(initial_objects(PROPER), terminal_objects(PROPER))   # expect [] []
        # print(initial_objects(Z3), terminal_objects(Z3))           # expect [] []
        # print(initial_objects(PAIR), terminal_objects(PAIR))       # expect [] []
        # print(initial_objects(ISO), terminal_objects(ISO))         # expect ['P', 'Q'] ['P', 'Q']

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
    | P01 | Adjunctions between discrete categories — `exercises/2a/p01_discrete_adjunctions.md` | warm-up | unpacking the definition |
    | P02 | The second inverse naturality equation (N2') — `exercises/2a/p02_inverse_naturality_in_a.md` | warm-up | working with transposes |
    | P03 | Left adjoints preserve initial objects — `exercises/2a/p03_left_adjoints_preserve_initial.md` | core | existence and uniqueness via a bijection |
    | P04 | Adjunctions compose — `exercises/2a/p04_adjunctions_compose.md` | core | naturality of a bijection |
    | P05 | The group of units is right adjoint to the inclusion — `exercises/2a/p05_units_right_adjoint.md` | core | verifying an adjunction from the checklist |
    | P06 | Orbits and fixed points as adjoints — `exercises/2a/p06_orbits_fixed_points.md` | stretch | constructing a bijection and proving it natural |

    **How to submit.** Write each proof in `proofs/2a/<same file name>.md`, in the five-step proof anatomy (Goal / Given / Plan / Proof / What made it work).
    Then ask Claude to review it: the review points at gaps and asks questions, and never supplies a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [1E: Equivalence of Categories](../1e_equivalence/) &nbsp;|&nbsp; Next: [2B: Units & Counits](../2b_units_counits/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
