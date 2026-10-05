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
    # 2B: Units & Counits

    > *Apply the bijection to the one arrow you are sure exists: the identity.*
    > — the idea behind this module

    In 2A an adjunction $F \dashv G$ was a whole family of bijections $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$, one for each pair of objects, tied together by two naturality equations. That is a lot of data. This module shows that all of it is determined by something far smaller: for each object $A$ a single arrow $\eta_A \colon A \to GF(A)$, and for each object $B$ a single arrow $\varepsilon_B \colon FG(B) \to B$. These are the **unit** and the **counit**. You have met them already without the names: "insert a generator into the free monoid" is a unit, "multiply out a word" and "evaluate a function at a point" are counits.

    The question this module answers is: *exactly which pairs $(\eta, \varepsilon)$ come from an adjunction?* The answer is two equations, the **triangle identities**. The main theorem says that an adjunction between $F$ and $G$ is the same thing as a pair of natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ satisfying them. So there are two definitions of adjunction, and we prove in full that they agree.

    By the end you will be able to compute the unit and counit of any adjunction from 2A; to recover any transpose from them; to prove the triangle identities; to prove the equivalence of the two definitions, in both directions and including the claim that the passage back and forth loses nothing; and to derive closure operators from Galois connections.

    Throughout, $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ are functors, and we use the four equations of 2A:

    | | equation | for |
    |---|---|---|
    | (N1) | $\overline{q \circ g} = G(q) \circ \bar{g}$ | $g \colon F(A) \to B$, $q \colon B \to B'$ |
    | (N2) | $\overline{f \circ p} = \bar{f} \circ F(p)$ | $p \colon A' \to A$, $f \colon A \to G(B)$ |
    | (N1') | $\overline{G(q) \circ f} = q \circ \bar{f}$ | $f \colon A \to G(B)$, $q \colon B \to B'$ |
    | (N2') | $\overline{g \circ F(p)} = \bar{g} \circ p$ | $g \colon F(A) \to B$, $p \colon A' \to A$ |

    (N1) and (N2) are part of the definition; (N1') is Lemma 1 of 2A; (N2') is brief 2A·P02. The proofs in this lecture use only the first three; (N2') is listed because it is handy in the briefs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Unit and the Counit

    A bijection $\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$ is only useful if you have an element to feed it. For arbitrary $A$ and $B$ the set $\mathcal{B}(F(A), B)$ might be empty. But if we *choose* $B = F(A)$, there is always one element: the identity. Likewise, choosing $A = G(B)$ makes $\mathcal{A}(A, G(B))$ contain $1_{G(B)}$.

    > **Definition (unit and counit).** Let $F \dashv G$.
    > For each object $A$ of $\mathcal{A}$, the **unit at $A$** is the transpose of the identity on $F(A)$:
    > $$\eta_A = \overline{1_{F(A)}} \colon A \to GF(A).$$
    > For each object $B$ of $\mathcal{B}$, the **counit at $B$** is the transpose of the identity on $G(B)$:
    > $$\varepsilon_B = \overline{1_{G(B)}} \colon FG(B) \to B.$$

    **Reading the definition.**

    1. $1_{F(A)}$ is an element of $\mathcal{B}(F(A), F(A))$. That is the left-hand hom-set of the adjunction with $B$ taken to be $F(A)$. Its transpose is therefore an element of $\mathcal{A}(A, G(F(A)))$. So $\eta_A$ goes **from $A$ to $GF(A)$**, in $\mathcal{A}$.
    2. $1_{G(B)}$ is an element of $\mathcal{A}(G(B), G(B))$. That is the right-hand hom-set with $A$ taken to be $G(B)$. Its transpose is an element of $\mathcal{B}(F(G(B)), B)$. So $\varepsilon_B$ goes **from $FG(B)$ to $B$**, in $\mathcal{B}$.
    3. Because the two bars are mutually inverse: $\overline{\eta_A} = 1_{F(A)}$ and $\overline{\varepsilon_B} = 1_{G(B)}$.
    4. The unit starts at the identity functor ($1_{\mathcal{A}} \Rightarrow GF$); the counit ends at the identity functor ($FG \Rightarrow 1_{\mathcal{B}}$). The left adjoint $F$ is applied *first* in the unit and *last* in the counit.

    **Examples.** In each case, take the description of the transpose from 2A and apply it to an identity.

    | Adjunction | Unit $\eta_A \colon A \to GF(A)$ | Counit $\varepsilon_B \colon FG(B) \to B$ |
    |---|---|---|
    | free monoid $F \dashv U$ | $S \to UF(S)$, $s \mapsto (s)$: a letter as a one-letter word | $FU(M) \to M$, $m_1 \cdots m_n \mapsto m_1 \cdot \ldots \cdot m_n$: multiply out a word of elements of $M$ |
    | $D \dashv U$ (discrete spaces) | $S \to UD(S)$, the identity function | $DU(X) \to X$, the identity function on points |
    | $(- \times B) \dashv (-)^B$ | $A \to (A \times B)^B$, $a \mapsto (b \mapsto (a, b))$ | $C^B \times B \to C$, $(h, b) \mapsto h(b)$: evaluation |
    | Galois connection $f \dashv g$ | the inequality $a \le g(f(a))$ | the inequality $f(g(b)) \le b$ |

    Check one: in the free monoid adjunction $\bar{g}(s) = g((s))$, so $\eta_S(s) = \overline{1_{F(S)}}(s) = 1_{F(S)}((s)) = (s)$. And $\bar{f}(s_1 \cdots s_n) = f(s_1) \cdots f(s_n)$, so with $f = 1_{U(M)}$ we get $\varepsilon_M(m_1 \cdots m_n) = m_1 \cdots m_n$, where on the left $m_1 \cdots m_n$ is a formal word and on the right it is a product in $M$.

    Notice the second row. The counit $DU(X) \to X$ is a continuous bijection, but when $X$ is not discrete it is **not** a homeomorphism: its inverse is not continuous. Units and counits are usually not isomorphisms.

    **Non-example (wrong direction).** There is in general no arrow $GF(A) \to A$. For the free monoid on $S = \emptyset$: $UF(\emptyset) = \{e\}$ has one element, and there is no function $\{e\} \to \emptyset$. The unit points *from* $A$.

    ### The unit is a natural transformation

    The components $\eta_A$ were defined one object at a time. We now show that they fit together.

    **Lemma 1.** Let $F \dashv G$. The arrows $\eta_A$ are the components of a natural transformation $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$. That is, for every arrow $p \colon A' \to A$ of $\mathcal{A}$,
    $$GF(p) \circ \eta_{A'} = \eta_A \circ p.$$

    - **Goal.** For all objects $A', A$ and every arrow $p \colon A' \to A$: the arrows $GF(p) \circ \eta_{A'}$ and $\eta_A \circ p$, both from $A'$ to $GF(A)$, are equal.
    - **Given.** $\eta_A = \overline{1_{F(A)}}$, hence $\overline{\eta_A} = 1_{F(A)}$; equations (N2) and (N1'); the identity axioms.
    - **Plan.** Both sides are arrows of the form $A' \to G(\text{something})$, so each has a transpose. Transposition is a bijection, so it is enough to show the two transposes are equal. Compute each.
    - **Proof.** *Left side.* Apply (N1') with $f = \eta_{A'} \colon A' \to G(F(A'))$ and $q = F(p) \colon F(A') \to F(A)$:
      $$\overline{G(F(p)) \circ \eta_{A'}} = F(p) \circ \overline{\eta_{A'}} = F(p) \circ 1_{F(A')} = F(p).$$
      *Right side.* Apply (N2) with $f = \eta_A \colon A \to G(F(A))$ and the arrow $p \colon A' \to A$:
      $$\overline{\eta_A \circ p} = \overline{\eta_A} \circ F(p) = 1_{F(A)} \circ F(p) = F(p).$$
      The two arrows $GF(p) \circ \eta_{A'}$ and $\eta_A \circ p$ have the same transpose, $F(p)$. Since transposition is injective, they are equal. $\blacksquare$
    - **What made it work.** *Two arrows with the same transpose are equal.* Neither side could be simplified where it stood; after transposing, each collapsed in one step because $\overline{\eta} = 1$.

    The counit is natural too: $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$. We prove that at the end of Section 2, where a shorter argument becomes available. (The unit and counit of the remaining adjunction of 2A, $\Delta \dashv \times$, are left for you to find in brief P01.)
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A1": (0, 2, r"$A'$"), "GFA1": (3.4, 2, r"$GF(A')$"), "GFA1_w": (3.05, 2, ""),
            "A": (0, 0, r"$A$"), "GFA": (3.4, 0, r"$GF(A)$"), "GFA_w": (3.05, 0, ""),
        },
        [
            ("A1", "GFA1_w", r"$\eta_{A'}$"),
            ("A", "GFA_w", r"$\eta_A$", {"side": -1}),
            ("A1", "A", r"$p$", {"side": -1}),
            ("GFA1", "GFA", r"$\qquad GF(p)$"),
        ],
        figsize=(5.4, 3.6),
        title=r"Naturality of the unit $\eta : 1_{\mathcal{A}} \Rightarrow GF$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Reference: [Leinster §2.2](https://arxiv.org/abs/1612.09375) (definition of unit and counit); [Riehl §4.2](https://math.jhu.edu/~eriehl/context.pdf) (the unit and counit as natural transformations).

    ---

    ## 2. Every Transpose Comes From the Unit or the Counit

    Here is the payoff of naturality. Knowing only the transposes of identities, we can compute the transpose of *every* arrow.

    **Lemma 2.** Let $F \dashv G$ with unit $\eta$ and counit $\varepsilon$.

    - (a) For every $g \colon F(A) \to B$: $\quad \bar{g} = G(g) \circ \eta_A$.
    - (b) For every $f \colon A \to G(B)$: $\quad \bar{f} = \varepsilon_B \circ F(f)$.

    $$\boxed{\;\bar{g} = \big(A \xrightarrow{\ \eta_A\ } GF(A) \xrightarrow{\ G(g)\ } G(B)\big) \qquad\qquad \bar{f} = \big(F(A) \xrightarrow{\ F(f)\ } FG(B) \xrightarrow{\ \varepsilon_B\ } B\big)\;}$$

    - **Goal.** (a) For all $A$, $B$ and all $g \colon F(A) \to B$, the arrows $\bar{g}$ and $G(g) \circ \eta_A$ from $A$ to $G(B)$ are equal. (b) For all $A$, $B$ and all $f \colon A \to G(B)$, the arrows $\bar{f}$ and $\varepsilon_B \circ F(f)$ from $F(A)$ to $B$ are equal.
    - **Given.** The definitions $\eta_A = \overline{1_{F(A)}}$ and $\varepsilon_B = \overline{1_{G(B)}}$; equations (N1) and (N2); the identity axioms.
    - **Plan.** Direct. Write the arrow as itself composed with an identity, so that a naturality equation can pull the arrow outside the bar and leave the transpose of an identity inside.
    - **Proof.**
      (a) By the identity axiom, $g = g \circ 1_{F(A)}$. Apply (N1) to the composable pair $1_{F(A)} \colon F(A) \to F(A)$ followed by $g \colon F(A) \to B$ (so $1_{F(A)}$ plays the role of "$g$" in (N1) and our $g$ plays the role of "$q$"):
      $$\bar{g} = \overline{g \circ 1_{F(A)}} = G(g) \circ \overline{1_{F(A)}} = G(g) \circ \eta_A.$$
      (b) By the identity axiom, $f = 1_{G(B)} \circ f$. Apply (N2) to the pair $f \colon A \to G(B)$ followed by $1_{G(B)} \colon G(B) \to G(B)$ (so our $f$ plays the role of "$p$" and $1_{G(B)}$ plays the role of "$f$"):
      $$\bar{f} = \overline{1_{G(B)} \circ f} = \overline{1_{G(B)}} \circ F(f) = \varepsilon_B \circ F(f). \qquad \blacksquare$$
    - **What made it work.** *Insert an identity, then let naturality move everything else outside the bar.* This is the first appearance of a "follow the identity" argument; it returns in a starring role in the Yoneda lemma (4B).

    **Examples.** For the free monoid, (b) says: to extend a function $f \colon S \to U(M)$ to a homomorphism $F(S) \to M$, apply $f$ to each letter (that is $F(f)$) and then multiply out (that is $\varepsilon_M$). For function sets, (b) says: $\bar{f}(a, b)$ is obtained by forming $(f(a), b)$ and then evaluating. For a Galois connection, (a) says: if $f(a) \le b$ then $a \le g(f(a)) \le g(b)$, the unit followed by $g$ applied to the given inequality.

    **Non-example.** The formulas are not interchangeable. $\varepsilon_B \circ F(g)$ does not even make sense for $g \colon F(A) \to B$: $F$ can only be applied to arrows of $\mathcal{A}$, and $g$ is an arrow of $\mathcal{B}$. Always check which category an arrow lives in before applying a functor to it.

    ### The counit is a natural transformation

    **Lemma 2'.** Let $F \dashv G$. The arrows $\varepsilon_B$ are the components of a natural transformation $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$. That is, for every arrow $q \colon B \to B'$ of $\mathcal{B}$,
    $$q \circ \varepsilon_B = \varepsilon_{B'} \circ FG(q).$$

    - **Goal.** For all objects $B, B'$ of $\mathcal{B}$ and every arrow $q \colon B \to B'$: the arrows $q \circ \varepsilon_B$ and $\varepsilon_{B'} \circ FG(q)$, both from $FG(B)$ to $B'$, are equal.
    - **Given.** $\varepsilon_B = \overline{1_{G(B)}}$; equation (N1'); Lemma 2(b); the identity axiom.
    - **Plan.** Direct. Show that each side is equal to the transpose of the single arrow $G(q) \colon G(B) \to G(B')$.
    - **Proof.** *Left side.* Apply (N1') with $f = 1_{G(B)} \colon G(B) \to G(B)$ and the arrow $q \colon B \to B'$. It says $\overline{G(q) \circ 1_{G(B)}} = q \circ \overline{1_{G(B)}}$. The right-hand side of this is $q \circ \varepsilon_B$ by the definition of the counit, and the left-hand side is $\overline{G(q)}$ by the identity axiom. So $q \circ \varepsilon_B = \overline{G(q)}$.
      *Right side.* The arrow $G(q) \colon G(B) \to G(B')$ has the form "$A \to G(\text{something})$" with $A = G(B)$. Lemma 2(b), applied to it, says $\overline{G(q)} = \varepsilon_{B'} \circ F(G(q))$.
      Both sides equal $\overline{G(q)}$, so they are equal to each other. $\blacksquare$
    - **What made it work.** *Once transposes are expressed through $\varepsilon$ (Lemma 2), naturality of $\varepsilon$ is one more instance of naturality of the bijection.* Compare with Lemma 1: there we transposed both sides and compared; here both sides are already transposes of the same arrow.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram, mo):
    mo.hstack(
        [
            draw_diagram(
                {"A": (0, 1.8, r"$A$"), "GFA": (3, 1.8, r"$GF(A)$"), "GFA_w": (2.65, 1.8, ""), "GB": (3, 0, r"$G(B)$")},
                [
                    ("A", "GFA_w", r"$\eta_A$"),
                    ("GFA", "GB", r"$\quad G(g)$"),
                    ("A", "GB", r"$\bar{g}$", {"side": -1, "color": "#1d4ed8"}),
                ],
                figsize=(4.4, 3.2),
                title=r"(a) in $\mathcal{A}$:  $\bar{g} = G(g) \circ \eta_A$",
            ),
            draw_diagram(
                {"FA": (0, 1.8, r"$F(A)$"), "FGB": (3, 1.8, r"$FG(B)$"), "FGB_w": (2.65, 1.8, ""), "B": (3, 0, r"$B$")},
                [
                    ("FA", "FGB_w", r"$F(f)$"),
                    ("FGB", "B", r"$\varepsilon_B$"),
                    ("FA", "B", r"$\bar{f}$", {"side": -1, "color": "#1d4ed8"}),
                ],
                figsize=(4.4, 3.2),
                title=r"(b) in $\mathcal{B}$:  $\bar{f} = \varepsilon_B \circ F(f)$",
            ),
        ],
        justify="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Reference: [Leinster §2.2](https://arxiv.org/abs/1612.09375) (transposes in terms of the unit and counit).

    ---

    ## 3. The Triangle Identities

    Lemma 2 expresses the bijection through $\eta$ and $\varepsilon$. But the bijection came with the constraint that the two bars are mutually inverse. What does that constraint say about $\eta$ and $\varepsilon$ themselves? Apply Lemma 2 to the unit and counit.

    **Lemma 3 (triangle identities).** Let $F \dashv G$ with unit $\eta$ and counit $\varepsilon$. Then

    $$\boxed{\;\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)} \ \text{ for every } A \in \mathcal{A}, \qquad G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)} \ \text{ for every } B \in \mathcal{B}.\;}$$

    **Reading the statement.** Check that the composites make sense before believing them.

    1. $\eta_A \colon A \to GF(A)$, so $F(\eta_A) \colon F(A) \to FGF(A)$. The counit at the object $F(A)$ of $\mathcal{B}$ is $\varepsilon_{F(A)} \colon FG(F(A)) \to F(A)$. The composite goes $F(A) \to FGF(A) \to F(A)$, in $\mathcal{B}$.
    2. The unit at the object $G(B)$ of $\mathcal{A}$ is $\eta_{G(B)} \colon G(B) \to GF(G(B))$, and $G(\varepsilon_B) \colon GFG(B) \to G(B)$. The composite goes $G(B) \to GFG(B) \to G(B)$, in $\mathcal{A}$.
    3. The identities say: *the unit, then the counit, is the identity*, once $F$ or $G$ has been applied to make them composable. They do **not** say that $\eta$ and $\varepsilon$ are inverse to each other; those two do not even live in the same category.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram, mo):
    mo.hstack(
        [
            draw_diagram(
                {"FA": (0, 1.8, r"$F(A)$"), "FGFA": (3.2, 1.8, r"$FGF(A)$"), "FGFA_w": (2.75, 1.8, ""), "FA2": (3.2, 0, r"$F(A)$")},
                [
                    ("FA", "FGFA_w", r"$F(\eta_A)$"),
                    ("FGFA", "FA2", r"$\quad\varepsilon_{F(A)}$"),
                    ("FA", "FA2", r"$1_{F(A)}$", {"side": -1}),
                ],
                figsize=(4.6, 3.2),
                title=r"First triangle identity (in $\mathcal{B}$)",
            ),
            draw_diagram(
                {"GB": (0, 1.8, r"$G(B)$"), "GFGB": (3.2, 1.8, r"$GFG(B)$"), "GFGB_w": (2.75, 1.8, ""), "GB2": (3.2, 0, r"$G(B)$")},
                [
                    ("GB", "GFGB_w", r"$\eta_{G(B)}$"),
                    ("GFGB", "GB2", r"$\quad G(\varepsilon_B)$"),
                    ("GB", "GB2", r"$1_{G(B)}$", {"side": -1}),
                ],
                figsize=(4.6, 3.2),
                title=r"Second triangle identity (in $\mathcal{A}$)",
            ),
        ],
        justify="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - **Goal.** For every object $A$ of $\mathcal{A}$: $\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}$. For every object $B$ of $\mathcal{B}$: $G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}$.
    - **Given.** Lemma 2, and $\overline{\eta_A} = 1_{F(A)}$, $\overline{\varepsilon_B} = 1_{G(B)}$ (item 3 of "Reading the definition" in Section 1).
    - **Plan.** Direct. Each left-hand side is, by Lemma 2, the transpose of a unit or counit; and those transposes are identities by definition.
    - **Proof.** *First identity.* Fix $A$. The unit $\eta_A$ is an arrow $A \to G(F(A))$, so Lemma 2(b) applies to it, with $F(A)$ in the role of "$B$" and $\eta_A$ in the role of "$f$":
      $$\overline{\eta_A} = \varepsilon_{F(A)} \circ F(\eta_A).$$
      But $\overline{\eta_A} = 1_{F(A)}$. Hence $\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}$.
      *Second identity.* Fix $B$. The counit $\varepsilon_B$ is an arrow $F(G(B)) \to B$, so Lemma 2(a) applies to it, with $G(B)$ in the role of "$A$" and $\varepsilon_B$ in the role of "$g$":
      $$\overline{\varepsilon_B} = G(\varepsilon_B) \circ \eta_{G(B)}.$$
      But $\overline{\varepsilon_B} = 1_{G(B)}$. Hence $G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}$. $\blacksquare$
    - **What made it work.** *The triangle identities are the two round trips $\bar{\bar{g}} = g$ and $\bar{\bar{f}} = f$, applied to identity arrows.* That is why exactly two equations appear, and why (as Section 5 shows) they are enough to get the round trips back for all arrows.

    **Seeing the identities in examples.**

    - *Free monoid, first identity.* $F(\eta_S) \colon F(S) \to FUF(S)$ sends a word $s_1 \cdots s_n$ to the word whose letters are the one-letter words $(s_1), \ldots, (s_n)$. Then $\varepsilon_{F(S)}$ multiplies these out in the monoid $F(S)$, that is, concatenates them: $(s_1)(s_2)\cdots(s_n) = s_1 \cdots s_n$. We are back where we started.
    - *Free monoid, second identity.* $\eta_{U(M)}$ sends $m \in M$ to the one-letter word $(m)$, and $U(\varepsilon_M)$ multiplies out the one-letter word $(m)$, giving $m$.
    - *Function sets, first identity.* $(a, b) \mapsto (\eta_A(a), b) \mapsto \eta_A(a)(b) = (a, b)$.
    - *Function sets, second identity.* $h \in C^B$ goes to the function $b \mapsto (h, b)$ in $(C^B \times B)^B$, and then composing with evaluation gives $b \mapsto h(b)$, which is $h$.
    - *Posets.* $f(a) \le f(g(f(a))) \le f(a)$, so $f g f = f$; and $g(b) \le g(f(g(b))) \le g(b)$, so $g f g = g$.

    **Non-example (natural, but no triangle identities).** Let $\mathcal{A} = \mathcal{B}$ be the group $\mathbb{Z}/3$ regarded as a one-object category (1A), and $F = G = $ the identity functor. A natural transformation $1 \Rightarrow GF$ has a single component, an element $\eta \in \mathbb{Z}/3$; naturality holds for every choice because the group is abelian. The same goes for $\varepsilon$. Take $\eta = 1$ and $\varepsilon = 1$. Both are natural, but the first triangle composite is $\varepsilon + F(\eta) = 1 + 1 = 2$, which is not the identity element $0$. So *naturality of $\eta$ and $\varepsilon$ alone does not make an adjunction*. The explorer in the next section lets you see which pairs do.

    > Reference: [Leinster §2.2](https://arxiv.org/abs/1612.09375) (the triangle identities); [Riehl §4.2](https://math.jhu.edu/~eriehl/context.pdf) (the same identities, drawn as pasting diagrams).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Explore: Which Pairs $(\eta, \varepsilon)$ Satisfy the Triangle Identities?

    For finite categories everything can be enumerated. Choose a pair of functors $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$. The checker lists **every** natural transformation $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and every natural transformation $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$. Pick one of each; it computes both triangle composites at every object and compares them with identities. The grid shows all pairs at once.

    The examples:

    - **$\mathbb{Z}/3$, identity functors.** One object $\ast$; arrows $0, 1, 2$; composition is addition mod 3.
    - **$\mathbb{Z}/3$, negation.** $F = G$ is the automorphism $x \mapsto -x$.
    - **Monoid $\{1, e\}$ with $e \cdot e = e$**, identity functors, and then the constant functors sending both arrows to $1$.
    - **$F$ picks an object $X$, $G = \,!$.** Here $\mathcal{A} = \mathbf{1}$ and $\mathcal{B}$ has objects $X, Y$ and non-identity arrows $t \colon X \to X$ (with $t \circ t = t$) and $u \colon X \to Y$ (with $u \circ t = u$). By Proposition 4 of 2A, $F \dashv\, !$ would make $X$ initial; it is not, because there are two arrows $X \to X$.
    - **Halving.** The Galois connection $a \mapsto \lfloor a/2 \rfloor$, $b \mapsto 2b + 1$ between the chains $\{0, \ldots, 5\}$ and $\{0, 1, 2\}$, as categories.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    tri_example = mo.ui.dropdown(
        options=[
            "Z/3, F = G = identity",
            "Z/3, F = G = negation",
            "monoid {1, e}, F = G = identity",
            "monoid {1, e}, F = G = constant at 1",
            "F picks X, G = !",
            "halving: a Galois connection",
        ],
        value="Z/3, F = G = identity",
        label="Functors F, G",
    )
    mo.vstack([mo.md("**Triangle-identity checker**"), tri_example])
    return (tri_example,)


@app.cell(hide_code=True)
def _(mo, tri_example):
    def _candidates():
        import itertools

        def _monoid(names, op):
            return {
                "objects": ["*"],
                "arrows": {_n: ("*", "*") for _n in names},
                "identity": {"*": names[0]},
                "compose": {(_g, _f): op(_g, _f) for _g in names for _f in names},
            }

        def _chain(n):
            _arr = {f"{_a}<={_b}": (_a, _b) for _a in range(n) for _b in range(n) if _a <= _b}
            return {
                "objects": list(range(n)),
                "arrows": _arr,
                "identity": {_a: f"{_a}<={_a}" for _a in range(n)},
                "compose": {(f"{_b}<={_c}", f"{_a}<={_b}"): f"{_a}<={_c}"
                            for _a in range(n) for _b in range(_a, n) for _c in range(_b, n)},
            }

        def _example(name):
            _z3 = _monoid(["0", "1", "2"], lambda _g, _f: str((int(_g) + int(_f)) % 3))
            _m2 = _monoid(["1", "e"], lambda _g, _f: "1" if (_g, _f) == ("1", "1") else "e")
            if name == "Z/3, F = G = identity":
                _i = {"objects": {"*": "*"}, "arrows": {_n: _n for _n in "012"}}
                return _z3, _z3, _i, _i
            if name == "Z/3, F = G = negation":
                _i = {"objects": {"*": "*"}, "arrows": {"0": "0", "1": "2", "2": "1"}}
                return _z3, _z3, _i, _i
            if name == "monoid {1, e}, F = G = identity":
                _i = {"objects": {"*": "*"}, "arrows": {"1": "1", "e": "e"}}
                return _m2, _m2, _i, _i
            if name == "monoid {1, e}, F = G = constant at 1":
                _i = {"objects": {"*": "*"}, "arrows": {"1": "1", "e": "1"}}
                return _m2, _m2, _i, _i
            if name == "F picks X, G = !":
                _one = {"objects": ["*"], "arrows": {"1*": ("*", "*")}, "identity": {"*": "1*"},
                        "compose": {("1*", "1*"): "1*"}}
                _b = {
                    "objects": ["X", "Y"],
                    "arrows": {"1X": ("X", "X"), "1Y": ("Y", "Y"), "t": ("X", "X"), "u": ("X", "Y")},
                    "identity": {"X": "1X", "Y": "1Y"},
                    "compose": {("1X", "1X"): "1X", ("t", "1X"): "t", ("1X", "t"): "t", ("t", "t"): "t",
                                ("u", "1X"): "u", ("u", "t"): "u", ("1Y", "u"): "u", ("1Y", "1Y"): "1Y"},
                }
                _f = {"objects": {"*": "X"}, "arrows": {"1*": "1X"}}
                _g = {"objects": {"X": "*", "Y": "*"}, "arrows": {_n: "1*" for _n in _b["arrows"]}}
                return _one, _b, _f, _g
            _p, _q = _chain(6), _chain(3)
            _fo = {_a: _a // 2 for _a in range(6)}
            _go = {_b: 2 * _b + 1 for _b in range(3)}
            _f = {"objects": _fo, "arrows": {_n: f"{_fo[_a]}<={_fo[_b]}" for _n, (_a, _b) in _p["arrows"].items()}}
            _g = {"objects": _go, "arrows": {_n: f"{_go[_a]}<={_go[_b]}" for _n, (_a, _b) in _q["arrows"].items()}}
            return _p, _q, _f, _g

        def _after(second, first):
            return {"objects": {_x: second["objects"][_y] for _x, _y in first["objects"].items()},
                    "arrows": {_x: second["arrows"][_y] for _x, _y in first["arrows"].items()}}

        def _ident(cat):
            return {"objects": {_x: _x for _x in cat["objects"]}, "arrows": {_x: _x for _x in cat["arrows"]}}

        def _nats(src, tgt, H, K):
            """All natural transformations H => K between functors src -> tgt."""
            _choices = [
                [_n for _n, (_d, _c) in tgt["arrows"].items() if _d == H["objects"][_x] and _c == K["objects"][_x]]
                for _x in src["objects"]
            ]
            _found = []
            for _combo in itertools.product(*_choices):
                _alpha = dict(zip(src["objects"], _combo))
                if all(
                    tgt["compose"][(K["arrows"][_k], _alpha[_d])] == tgt["compose"][(_alpha[_c], H["arrows"][_k])]
                    for _k, (_d, _c) in src["arrows"].items()
                ):
                    _found.append(_alpha)
            return _found

        _A, _B, _F, _G = _example(tri_example.value)
        _etas = _nats(_A, _A, _ident(_A), _after(_G, _F))
        _epss = _nats(_B, _B, _after(_F, _G), _ident(_B))

        def _label(alpha):
            return ",  ".join(f"at {_x}: {_v}" for _x, _v in alpha.items())

        _eta_opts = {_label(_a): tuple(_a.items()) for _a in _etas} or {"(none exists)": None}
        _eps_opts = {_label(_a): tuple(_a.items()) for _a in _epss} or {"(none exists)": None}
        return _eta_opts, _eps_opts

    _eta_opts, _eps_opts = _candidates()
    eta_choice = mo.ui.dropdown(options=_eta_opts, value=list(_eta_opts)[0],
                                label=f"eta : 1 => GF   ({len(_eta_opts)} natural choices)")
    eps_choice = mo.ui.dropdown(options=_eps_opts, value=list(_eps_opts)[0],
                                label=f"epsilon : FG => 1   ({len(_eps_opts)} natural choices)")
    mo.vstack([eta_choice, eps_choice])
    return eps_choice, eta_choice


@app.cell(hide_code=True)
def _(eps_choice, eta_choice, tri_example):
    def _run():
        import itertools
        import logging
        logging.getLogger("matplotlib").setLevel(logging.ERROR)
        import matplotlib.pyplot as plt

        def _monoid(names, op):
            return {
                "objects": ["*"],
                "arrows": {_n: ("*", "*") for _n in names},
                "identity": {"*": names[0]},
                "compose": {(_g, _f): op(_g, _f) for _g in names for _f in names},
            }

        def _chain(n):
            _arr = {f"{_a}<={_b}": (_a, _b) for _a in range(n) for _b in range(n) if _a <= _b}
            return {
                "objects": list(range(n)),
                "arrows": _arr,
                "identity": {_a: f"{_a}<={_a}" for _a in range(n)},
                "compose": {(f"{_b}<={_c}", f"{_a}<={_b}"): f"{_a}<={_c}"
                            for _a in range(n) for _b in range(_a, n) for _c in range(_b, n)},
            }

        def _example(name):
            _z3 = _monoid(["0", "1", "2"], lambda _g, _f: str((int(_g) + int(_f)) % 3))
            _m2 = _monoid(["1", "e"], lambda _g, _f: "1" if (_g, _f) == ("1", "1") else "e")
            if name == "Z/3, F = G = identity":
                _i = {"objects": {"*": "*"}, "arrows": {_n: _n for _n in "012"}}
                return _z3, _z3, _i, _i
            if name == "Z/3, F = G = negation":
                _i = {"objects": {"*": "*"}, "arrows": {"0": "0", "1": "2", "2": "1"}}
                return _z3, _z3, _i, _i
            if name == "monoid {1, e}, F = G = identity":
                _i = {"objects": {"*": "*"}, "arrows": {"1": "1", "e": "e"}}
                return _m2, _m2, _i, _i
            if name == "monoid {1, e}, F = G = constant at 1":
                _i = {"objects": {"*": "*"}, "arrows": {"1": "1", "e": "1"}}
                return _m2, _m2, _i, _i
            if name == "F picks X, G = !":
                _one = {"objects": ["*"], "arrows": {"1*": ("*", "*")}, "identity": {"*": "1*"},
                        "compose": {("1*", "1*"): "1*"}}
                _b = {
                    "objects": ["X", "Y"],
                    "arrows": {"1X": ("X", "X"), "1Y": ("Y", "Y"), "t": ("X", "X"), "u": ("X", "Y")},
                    "identity": {"X": "1X", "Y": "1Y"},
                    "compose": {("1X", "1X"): "1X", ("t", "1X"): "t", ("1X", "t"): "t", ("t", "t"): "t",
                                ("u", "1X"): "u", ("u", "t"): "u", ("1Y", "u"): "u", ("1Y", "1Y"): "1Y"},
                }
                _f = {"objects": {"*": "X"}, "arrows": {"1*": "1X"}}
                _g = {"objects": {"X": "*", "Y": "*"}, "arrows": {_n: "1*" for _n in _b["arrows"]}}
                return _one, _b, _f, _g
            _p, _q = _chain(6), _chain(3)
            _fo = {_a: _a // 2 for _a in range(6)}
            _go = {_b: 2 * _b + 1 for _b in range(3)}
            _f = {"objects": _fo, "arrows": {_n: f"{_fo[_a]}<={_fo[_b]}" for _n, (_a, _b) in _p["arrows"].items()}}
            _g = {"objects": _go, "arrows": {_n: f"{_go[_a]}<={_go[_b]}" for _n, (_a, _b) in _q["arrows"].items()}}
            return _p, _q, _f, _g

        def _after(second, first):
            return {"objects": {_x: second["objects"][_y] for _x, _y in first["objects"].items()},
                    "arrows": {_x: second["arrows"][_y] for _x, _y in first["arrows"].items()}}

        def _ident(cat):
            return {"objects": {_x: _x for _x in cat["objects"]}, "arrows": {_x: _x for _x in cat["arrows"]}}

        def _nats(src, tgt, H, K):
            _choices = [
                [_n for _n, (_d, _c) in tgt["arrows"].items() if _d == H["objects"][_x] and _c == K["objects"][_x]]
                for _x in src["objects"]
            ]
            _found = []
            for _combo in itertools.product(*_choices):
                _alpha = dict(zip(src["objects"], _combo))
                if all(
                    tgt["compose"][(K["arrows"][_k], _alpha[_d])] == tgt["compose"][(_alpha[_c], H["arrows"][_k])]
                    for _k, (_d, _c) in src["arrows"].items()
                ):
                    _found.append(_alpha)
            return _found

        _A, _B, _F, _G = _example(tri_example.value)

        def _triangles(eta, eps):
            """Composites of both triangles at every object, each paired with the identity it should equal."""
            _first = [(_a, _B["compose"][(eps[_F["objects"][_a]], _F["arrows"][eta[_a]])],
                       _B["identity"][_F["objects"][_a]]) for _a in _A["objects"]]
            _second = [(_b, _A["compose"][(_G["arrows"][eps[_b]], eta[_G["objects"][_b]])],
                        _A["identity"][_G["objects"][_b]]) for _b in _B["objects"]]
            return _first, _second

        _etas = _nats(_A, _A, _ident(_A), _after(_G, _F))
        _epss = _nats(_B, _B, _after(_F, _G), _ident(_B))

        if eta_choice.value is None or eps_choice.value is None:
            print("There is no natural transformation of the required kind, so F is not left adjoint to G.")
            return None
        _eta, _eps = dict(eta_choice.value), dict(eps_choice.value)
        if any(_x not in _eta for _x in _A["objects"]) or any(_x not in _eps for _x in _B["objects"]):
            print("Pick eta and epsilon again for the new example.")
            return None

        _first, _second = _triangles(_eta, _eps)
        print(f"Example: {tri_example.value}")
        print("\nFirst triangle identity   eps_F(A) o F(eta_A) = 1_F(A):")
        for _a, _comp, _id in _first:
            print(f"   A = {_a}:  composite = {_comp:8s} identity = {_id:8s} {'holds' if _comp == _id else 'FAILS'}")
        print("\nSecond triangle identity  G(eps_B) o eta_G(B) = 1_G(B):")
        for _b, _comp, _id in _second:
            print(f"   B = {_b}:  composite = {_comp:8s} identity = {_id:8s} {'holds' if _comp == _id else 'FAILS'}")
        _ok1 = all(_c == _i for _, _c, _i in _first)
        _ok2 = all(_c == _i for _, _c, _i in _second)
        print("\nVerdict:", "this pair (eta, epsilon) is the unit and counit of an adjunction F -| G."
              if _ok1 and _ok2 else "this pair does not define an adjunction.")

        # grid of all pairs
        _fig, _ax = plt.subplots(figsize=(max(3.2, 1.0 + 0.9 * len(_etas)), max(2.4, 1.0 + 0.7 * len(_epss))))
        _colors = {0: "#dc2626", 1: "#f59e0b", 2: "#16a34a"}
        _good = 0
        for _i, _e in enumerate(_etas):
            for _j, _p in enumerate(_epss):
                _f1, _f2 = _triangles(_e, _p)
                _score = int(all(_c == _d for _, _c, _d in _f1)) + int(all(_c == _d for _, _c, _d in _f2))
                _good += _score == 2
                _ax.scatter([_i], [_j], s=520, color=_colors[_score], zorder=2,
                            edgecolors="black" if (_e == _eta and _p == _eps) else "none", linewidths=2.5)
        _ax.set_xticks(range(len(_etas)))
        _ax.set_yticks(range(len(_epss)))
        _ax.set_xticklabels([f"eta #{_i + 1}" for _i in range(len(_etas))], fontsize=8)
        _ax.set_yticklabels([f"eps #{_j + 1}" for _j in range(len(_epss))], fontsize=8)
        _ax.set_xlim(-0.6, len(_etas) - 0.4)
        _ax.set_ylim(-0.6, len(_epss) - 0.4)
        _ax.set_title(f"{len(_etas) * len(_epss)} natural pairs, {_good} satisfy both identities\n"
                      "green: both hold   amber: one holds   red: neither   (outlined: your choice)", fontsize=9)
        _fig.tight_layout()
        return _fig

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to notice. For $\mathbb{Z}/3$ with identity functors there are nine natural pairs and exactly three satisfy the identities: those with $\varepsilon = -\eta$. So the same two functors can be adjoint in more than one way, and *an adjunction is the pair of functors together with a choice of $(\eta, \varepsilon)$*. For the monoid $\{1, e\}$ with constant functors there is a natural $\eta$ and a natural $\varepsilon$, yet neither identity holds: these functors are not adjoint. For "$F$ picks $X$" the second identity holds and the first fails, so the two identities are independent conditions.

    ---

    ## 5. The Main Theorem: Two Definitions of Adjunction Agree

    Sections 1 to 3 went from an adjunction to a pair $(\eta, \varepsilon)$ of natural transformations satisfying the triangle identities. Now we go back, and show that the two passages are mutually inverse.

    **Theorem 4.** Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be functors. There is a one-to-one correspondence between

    - **(a)** adjunctions between $F$ and $G$ with $F$ on the left: families of bijections $\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$ satisfying (N1) and (N2); and
    - **(b)** pairs $(\eta, \varepsilon)$ of natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ satisfying the two triangle identities.

    The correspondence sends an adjunction to its unit and counit. In the other direction it sends $(\eta, \varepsilon)$ to the bijections $g \mapsto G(g) \circ \eta_A$, with inverse $f \mapsto \varepsilon_B \circ F(f)$.

    - **Goal.** Three things. (1) Every adjunction as in (a) yields a pair as in (b). (2) Every pair as in (b) yields an adjunction as in (a) by the stated formulas. (3) Doing (1) then (2) returns the adjunction we started with, and doing (2) then (1) returns the pair we started with.
    - **Given.** For (1): the definition of adjunction and Sections 1 to 3. For (2): only that $F$, $G$ are functors, that $\eta$, $\varepsilon$ are natural, and the two triangle identities. Naturality of $\eta$ at an arrow $f \colon A \to A_1$ reads $GF(f) \circ \eta_A = \eta_{A_1} \circ f$; naturality of $\varepsilon$ at an arrow $g \colon B_1 \to B$ reads $\varepsilon_B \circ FG(g) = g \circ \varepsilon_{B_1}$.
    - **Plan.** Translate between the two definitions. (1) is already done. For (2), run the five-item checklist of 2A: the two maps are given by formulas, each round trip uses functoriality, then one naturality square, then one triangle identity; (N1) and (N2) need only functoriality. (3) is two short computations using Lemma 2.
    - **Proof.**

      **(1) From (a) to (b).** Given an adjunction, define $\eta_A = \overline{1_{F(A)}}$ and $\varepsilon_B = \overline{1_{G(B)}}$. By Lemma 1, $\eta$ is natural. By Lemma 2', $\varepsilon$ is natural. The triangle identities hold by Lemma 3.

      **(2) From (b) to (a).** Let $(\eta, \varepsilon)$ be as in (b). For $g \colon F(A) \to B$ and $f \colon A \to G(B)$ *define*
      $$\bar{g} = G(g) \circ \eta_A \colon A \to G(B), \qquad \bar{f} = \varepsilon_B \circ F(f) \colon F(A) \to B.$$
      These are composites of arrows of $\mathcal{A}$ and of $\mathcal{B}$ respectively, with the domains and codomains shown. At this point the two bars are just two formulas; we must prove they are mutually inverse.

      *Round trip from $g$.* Let $g \colon F(A) \to B$. Then
      $$\bar{\bar{g}} = \varepsilon_B \circ F\big(G(g) \circ \eta_A\big) = \varepsilon_B \circ FG(g) \circ F(\eta_A) = g \circ \varepsilon_{F(A)} \circ F(\eta_A) = g \circ 1_{F(A)} = g.$$
      The five equalities are, in order: the two defining formulas (first the bar of $g$, then the bar of the arrow $G(g) \circ \eta_A \colon A \to G(B)$); $F$ preserves composition; naturality of $\varepsilon$ at $g \colon F(A) \to B$, which reads $\varepsilon_B \circ FG(g) = g \circ \varepsilon_{F(A)}$; the first triangle identity; the identity axiom.

      *Round trip from $f$.* Let $f \colon A \to G(B)$. Then
      $$\bar{\bar{f}} = G\big(\varepsilon_B \circ F(f)\big) \circ \eta_A = G(\varepsilon_B) \circ GF(f) \circ \eta_A = G(\varepsilon_B) \circ \eta_{G(B)} \circ f = 1_{G(B)} \circ f = f.$$
      In order: the two defining formulas; $G$ preserves composition; naturality of $\eta$ at $f \colon A \to G(B)$, which reads $GF(f) \circ \eta_A = \eta_{G(B)} \circ f$; the second triangle identity; the identity axiom.

      So $g \mapsto \bar{g}$ is a bijection $\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$ with inverse $f \mapsto \bar{f}$.

      *(N1).* Let $g \colon F(A) \to B$ and $q \colon B \to B'$. Then $\overline{q \circ g} = G(q \circ g) \circ \eta_A = G(q) \circ G(g) \circ \eta_A = G(q) \circ \bar{g}$, using the definition, functoriality of $G$, and the definition again.

      *(N2).* Let $p \colon A' \to A$ and $f \colon A \to G(B)$. Then $\overline{f \circ p} = \varepsilon_B \circ F(f \circ p) = \varepsilon_B \circ F(f) \circ F(p) = \bar{f} \circ F(p)$, using the definition, functoriality of $F$, and the definition again.

      So the formulas define an adjunction.

      **(3) The two passages are mutually inverse.**
      *Start with an adjunction*, take its unit and counit, and build the bijections of (2) from them: $g \mapsto G(g) \circ \eta_A$ and $f \mapsto \varepsilon_B \circ F(f)$. By Lemma 2 these are exactly the original $g \mapsto \bar{g}$ and $f \mapsto \bar{f}$. So we recover the adjunction we started with.
      *Start with a pair $(\eta, \varepsilon)$* as in (b), build the adjunction of (2), and take its unit and counit. Its unit at $A$ is the transpose of $1_{F(A)}$, which by the defining formula is $G(1_{F(A)}) \circ \eta_A = 1_{GF(A)} \circ \eta_A = \eta_A$, since $G$ preserves identities. Its counit at $B$ is the transpose of $1_{G(B)}$, namely $\varepsilon_B \circ F(1_{G(B)}) = \varepsilon_B \circ 1_{FG(B)} = \varepsilon_B$. So we recover the pair we started with. $\blacksquare$
    - **What made it work.** *Each hypothesis in (b) is used exactly once per round trip: functoriality to split the composite, one naturality square to slide $g$ (or $f$) past $\varepsilon$ (or $\eta$), one triangle identity to cancel.* When a proof asks you to simplify an expression containing $\varepsilon \circ F(\ldots)$ or $G(\ldots) \circ \eta$, try those three moves in that order.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "FA": (0, 2, r"$F(A)$"), "FGFA": (3.4, 2, r"$FGF(A)$"), "FGB": (6.8, 2, r"$FG(B)$"),
            "FGFA_w": (2.95, 2, ""), "FGFA_e": (3.85, 2, ""), "FGB_w": (6.45, 2, ""),
            "FA2": (3.4, 0, r"$F(A)$"), "B": (6.8, 0, r"$B$"),
        },
        [
            ("FA", "FGFA_w", r"$F(\eta_A)$"),
            ("FGFA_e", "FGB_w", r"$FG(g)$"),
            ("FGFA", "FA2", r"$\quad\varepsilon_{F(A)}$"),
            ("FGB", "B", r"$\varepsilon_B$"),
            ("FA2", "B", r"$g$", {"side": -1}),
            ("FA", "FA2", r"$1_{F(A)}$", {"side": -1}),
        ],
        figsize=(7.6, 3.6),
        title=r"Round trip from $g$: a triangle identity (left) pasted to a naturality square of $\varepsilon$ (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How to use the theorem.** You now have two ways to prove $F \dashv G$:

    - *hom-set route*: build the bijection, check both round trips, check (N1) and (N2);
    - *unit–counit route*: give $\eta_A$ and $\varepsilon_B$ for all objects, check each is natural, check the two triangle identities.

    The second route is usually shorter when $\eta$ and $\varepsilon$ are simple maps (an inclusion, an evaluation, a quotient). The first is usually shorter when the bijection is evident (as for $D \dashv U$).

    **Example (using the unit–counit route).** For $(- \times B) \dashv (-)^B$, take $\eta_A(a) = (b \mapsto (a, b))$ and $\varepsilon_C(h, b) = h(b)$. The triangle identities were verified in Section 3; naturality of each is a one-line element check. By Theorem 4 this alone establishes the adjunction, with transposes $\bar{g}(a) = (g \circ -)(\eta_A(a)) = (b \mapsto g(a, b))$, matching 2A.

    **Non-example.** In the explorer, "monoid $\{1, e\}$, constant functors" has natural $\eta$ and $\varepsilon$ and fails both identities. The formulas $g \mapsto G(g) \circ \eta$ and $f \mapsto \varepsilon \circ F(f)$ still define functions between hom-sets, but they are not mutually inverse: both send every arrow to $e$.

    > Reference: [Leinster §2.2](https://arxiv.org/abs/1612.09375) (the correspondence between adjunctions and unit–counit pairs satisfying the triangle identities); [Riehl §4.2](https://math.jhu.edu/~eriehl/context.pdf) (adjunction defined by unit and counit, and its equivalence with the hom-set definition).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Posets Again: Closure Operators

    Specialise Theorem 4 to posets. Let $f \colon P \to Q$ and $g \colon Q \to P$ be order-preserving maps. A natural transformation $\eta \colon 1_P \Rightarrow gf$ needs a component $a \to g(f(a))$ for each $a$, that is, an inequality $a \le g(f(a))$; its naturality squares are equations between parallel arrows of a poset, which always hold. Likewise $\varepsilon$ exists exactly when $f(g(b)) \le b$ for all $b$. The triangle identities are again equations between parallel arrows in a poset, so they hold automatically. Theorem 4 therefore gives:

    $$\boxed{\; f \dashv g \iff \big(a \le g(f(a)) \text{ for all } a \in P\big) \ \text{ and } \ \big(f(g(b)) \le b \text{ for all } b \in Q\big). \;}$$

    Two families of inequalities, each involving only *one* variable, replace the two-variable condition $f(a) \le b \iff a \le g(b)$.
    Now look at the composite $g \circ f \colon P \to P$. It goes around the adjunction and comes back, and it has a recognisable shape.

    > **Definition (closure operator).** Let $P$ be a poset. A **closure operator** on $P$ is a function $c \colon P \to P$ such that for all $a, a' \in P$:
    > 1. (order-preserving) if $a \le a'$ then $c(a) \le c(a')$;
    > 2. (extensive) $a \le c(a)$;
    > 3. (idempotent) $c(c(a)) = c(a)$.
    >
    > An element $a$ is **closed** if $c(a) = a$.

    **Reading the definition.** Three separate conditions, each universally quantified. Extensive says closing never shrinks; idempotent says closing twice is the same as closing once. Note that 3 is an *equality*; given 1 and 2, the inequality $c(a) \le c(c(a))$ is free, so the content of 3 is $c(c(a)) \le c(a)$.

    **Proposition 5.** Let $f \colon P \to Q$ and $g \colon Q \to P$ be order-preserving maps of posets with $f \dashv g$. Then $f \circ g \circ f = f$, and $c = g \circ f$ is a closure operator on $P$.

    - **Goal.** (i) For every $a \in P$: $f(g(f(a))) = f(a)$. (ii) $c = g \circ f$ satisfies conditions 1, 2, 3 of the definition for all $a, a' \in P$.
    - **Given.** $f$, $g$ order-preserving; the unit inequalities $a \le g(f(a))$ for all $a \in P$; the counit inequalities $f(g(b)) \le b$ for all $b \in Q$; antisymmetry of $\le$.
    - **Plan.** Direct. For (i), prove two inequalities and use antisymmetry; one comes from applying $f$ to a unit inequality, the other is a counit inequality at a well-chosen element. Then (ii) follows quickly.
    - **Proof.**
      (i) Fix $a \in P$. The unit inequality is $a \le g(f(a))$. Since $f$ is order-preserving, $f(a) \le f(g(f(a)))$. The counit inequality at the element $b = f(a)$ of $Q$ is $f(g(f(a))) \le f(a)$. By antisymmetry, $f(g(f(a))) = f(a)$.
      (ii) *Order-preserving:* if $a \le a'$ then $f(a) \le f(a')$ because $f$ is order-preserving, and then $g(f(a)) \le g(f(a'))$ because $g$ is. *Extensive:* $a \le g(f(a)) = c(a)$ is the unit inequality. *Idempotent:* apply $g$ to both sides of the equation in (i): $g(f(g(f(a)))) = g(f(a))$, that is, $c(c(a)) = c(a)$. $\blacksquare$
    - **What made it work.** *Part (i) is the first triangle identity, read in a poset:* the composite $f(a) \le f g f(a) \le f(a)$ is "$F(\eta_A)$ then $\varepsilon_{F(A)}$". In a poset, a composite being an identity forces the objects to be equal.

    The mirror-image argument gives $g \circ f \circ g = g$; writing it out is part of brief P02. Consequently the closed elements of $c$ are exactly the elements of the form $g(b)$: if $a = g(b)$ then $c(a) = g(f(g(b))) = g(b) = a$, and if $c(a) = a$ then $a = g(f(a))$ is of that form.

    **Examples.**

    | Galois connection $f \dashv g$ | Closure operator $g \circ f$ | Closed elements |
    |---|---|---|
    | for a group $G$: $\mathscr{P}(G) \to \mathrm{Sub}(G)$, $S \mapsto \langle S \rangle$; and the inclusion $\mathrm{Sub}(G) \to \mathscr{P}(G)$ | $S \mapsto$ the underlying set of the subgroup generated by $S$ | subsets that are subgroups |
    | for a vector space $V$: $S \mapsto \mathrm{span}(S)$; and the inclusion of subspaces into subsets | $S \mapsto \mathrm{span}(S)$ | subsets that are subspaces |
    | for a topological space $X$: $S \mapsto \overline{S}$ into the closed subsets; and the inclusion of closed subsets into all subsets | topological closure | closed sets |
    | for a function $h \colon K \to L$: $h_* \dashv h^*$ | $S \mapsto h^{*}(h_*(S))$, all points with the same image as some point of $S$ | unions of fibres of $h$ |
    | ceiling $\dashv$ inclusion $\mathbb{Z} \to \mathbb{R}$ | $x \mapsto \lceil x \rceil$ | the integers |

    For the first row, the adjunction condition is $\langle S \rangle \subseteq H \iff S \subseteq H$ for a subset $S$ and a subgroup $H$: the subgroup generated by $S$ is the smallest subgroup containing $S$. The next two rows are the same statement for "smallest subspace" and "smallest closed set".

    **Non-examples.**

    - On $(\mathbb{N}, \le)$, the map $a \mapsto a + 1$ is order-preserving and extensive but not idempotent. So it is not $g \circ f$ for any Galois connection.
    - For a topological space $X$, the interior operator $S \mapsto S^{\circ}$ on $\mathscr{P}(X)$ is order-preserving and idempotent, but $S^{\circ} \subseteq S$: the inequality points the wrong way, so it is not a closure operator. It has the shape of the *other* composite, $f \circ g$, which satisfies $f(g(b)) \le b$.

    Whether every closure operator arises from a Galois connection is taken up in 6D, where closure operators reappear as the simplest monads.

    > Reference: [Leinster §2.2](https://arxiv.org/abs/1612.09375) (unit and counit for adjunctions between ordered sets); [Riehl §4.2](https://math.jhu.edu/~eriehl/context.pdf) for further examples.
    """)
    return


@app.cell
def _():
    def _run():
        # The closure operator of the Galois connection h_* -| h^* for a function h : K -> L.
        import itertools

        _K = ["k1", "k2", "k3", "k4"]
        _h = {"k1": "x", "k2": "x", "k3": "y", "k4": "z"}

        def _direct(S):
            return frozenset(_h[_k] for _k in S)

        def _inverse(T):
            return frozenset(_k for _k in _K if _h[_k] in T)

        _subsets = [frozenset(_c) for _n in range(len(_K) + 1) for _c in itertools.combinations(_K, _n)]
        _c = {_S: _inverse(_direct(_S)) for _S in _subsets}

        def _show(S):
            return "{" + ", ".join(sorted(S)) + "}"

        print("h:", _h)
        print("\nc(S) = h^*(h_*(S)) for a few subsets S of K:")
        for _S in [frozenset(), frozenset({"k1"}), frozenset({"k3"}), frozenset({"k1", "k4"})]:
            print(f"   c({_show(_S)}) = {_show(_c[_S])}")
        print("\nextensive  (S <= c(S)) for all 16 subsets:", all(_S <= _c[_S] for _S in _subsets))
        print("idempotent (c(c(S)) = c(S)) for all 16:    ", all(_c[_c[_S]] == _c[_S] for _S in _subsets))
        print("order-preserving for all pairs:            ",
              all(_c[_S] <= _c[_T] for _S in _subsets for _T in _subsets if _S <= _T))
        _closed = [_S for _S in _subsets if _c[_S] == _S]
        print(f"\n{len(_closed)} closed subsets (the unions of fibres of h):")
        print("  ", ",  ".join(_show(_S) for _S in _closed))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Reversing the unit or the counit.** *Diagnosis:* writing $\eta_A \colon GF(A) \to A$ or $\varepsilon_B \colon B \to FG(B)$. Re-derive the direction each time from the definition: $1_{F(A)} \in \mathcal{B}(F(A), F(A))$ transposes into $\mathcal{A}(A, GF(A))$.
    2. **Writing a triangle identity that does not type-check.** *Diagnosis:* "$\varepsilon \circ \eta = 1$" is meaningless, since $\eta_A$ lives in $\mathcal{A}$ and $\varepsilon_B$ in $\mathcal{B}$. The identities are $\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}$ and $G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}$; write the domain and codomain of every arrow before composing.
    3. **Concluding that $\eta$ or $\varepsilon$ is an isomorphism.** *Diagnosis:* the first triangle identity says $F(\eta_A)$ has a left inverse, nothing more. The counit $DU(X) \to X$ of Section 1 is not an isomorphism.
    4. **Checking the triangle identities but not naturality (or the reverse).** *Diagnosis:* Theorem 4(b) has four hypotheses: $\eta$ natural, $\varepsilon$ natural, and two identities. The explorer in Section 4 shows natural pairs failing the identities; the round-trip computations in Theorem 4 use every one of the four.
    5. **Using a bar before it is known to be a bijection.** *Diagnosis:* in part (2) of Theorem 4 the bars are *defined* by formulas, and "$\bar{\bar{g}} = g$" is the thing to be proved. Arguing "two arrows with the same transpose are equal" there would be circular.

    ---

    ## Why This Matters

    - **2C** shows that the unit alone already determines the adjunction: $\eta_A$ is an initial object in a category of "arrows from $A$ to something of the form $G(B)$". The proof there leans on Theorem 4.
    - **1E revisited.** An equivalence of categories is a pair of functors with natural *isomorphisms* $1 \cong GF$ and $FG \cong 1$; an adjunction relaxes "isomorphism" to "natural transformation satisfying the triangle identities". Brief P06 makes the comparison precise.
    - **4A–4C.** Lemma 2 is your first "follow the identity" argument. The Yoneda lemma is the same idea in its purest form.
    - **6A.** The counit of the adjunction "diagonal $\dashv$ limit" is the limit cone itself.
    - **6D.** The composite $GF$ with the unit $\eta$ and the natural transformation $G\varepsilon F$ is a *monad*; Proposition 5 is the poset case, where a monad is a closure operator, and the triangle identities become the monad axioms.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Fill in each `# TODO`, then un-comment the `print` checks and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Unit and counit inequalities

    For order-preserving maps `f` and `g` between finite posets, write `unit_counit(P, leqP, Q, leqQ, f, g)` returning a pair of booleans: whether $a \le g(f(a))$ for all $a \in P$, and whether $f(g(b)) \le b$ for all $b \in Q$.
    """)
    return


@app.cell
def _():
    def _run():
        def unit_counit(P, leqP, Q, leqQ, f, g):
            # TODO: unit_ok  = "a <= g(f(a)) for every a in P"
            unit_ok = ...
            # TODO: counit_ok = "f(g(b)) <= b for every b in Q"
            counit_ok = ...
            return unit_ok, counit_ok

        P, Q = list(range(6)), list(range(3))
        leq = lambda a, b: a <= b
        f = {a: a // 2 for a in P}
        g_good = {b: 2 * b + 1 for b in Q}
        g_bad = {b: 2 * b for b in Q}

        # print(unit_counit(P, leq, Q, leq, f, g_good))   # expect (True, True)
        # print(unit_counit(P, leq, Q, leq, f, g_bad))    # expect (False, True)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Closed elements of a Galois connection

    Given a Galois connection $f \dashv g$, write `closure(P, f, g)` returning the dict $a \mapsto g(f(a))$, and `closed_elements(P, f, g)` returning the list of $a$ with $g(f(a)) = a$, in the order they appear in `P`.
    """)
    return


@app.cell
def _():
    def _run():
        def closure(P, f, g):
            # TODO: the dict a -> g(f(a))
            return ...

        def closed_elements(P, f, g):
            # TODO: the elements of P fixed by the closure operator
            return ...

        chain6 = list(range(6))
        halve = {a: a // 2 for a in chain6}
        odd = {b: 2 * b + 1 for b in range(3)}

        divisors = [1, 2, 3, 4, 6, 12]                               # ordered by divisibility
        gcd4 = {1: 1, 2: 2, 3: 1, 4: 4, 6: 2, 12: 4}                 # a -> gcd(a, 4)
        gcd4_right = {1: 3, 2: 6, 3: 3, 4: 12, 6: 6, 12: 12}         # its right adjoint

        # print(closure(chain6, halve, odd))                    # expect {0: 1, 1: 1, 2: 3, 3: 3, 4: 5, 5: 5}
        # print(closed_elements(chain6, halve, odd))            # expect [1, 3, 5]
        # print(closure(divisors, gcd4, gcd4_right))            # expect {1: 3, 2: 6, 3: 3, 4: 12, 6: 6, 12: 12}
        # print(closed_elements(divisors, gcd4, gcd4_right))    # expect [3, 6, 12]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Transposes from a unit and a counit

    Categories, functors and natural transformations are given in the shared encoding (`compose[(g, f)]` is $g \circ f$; a functor is `{"objects": ..., "arrows": ...}`; a natural transformation is a dict from objects to arrow names). Given natural transformations `eta` and `eps` of the right shapes, with no assumption that the triangle identities hold, implement the two formulas of Theorem 4:

    - `bar_g(A, B, F, G, eta, a, g)`: for an arrow `g` of `B` with domain `F(a)`, the arrow $G(g) \circ \eta_a$ of `A`;
    - `bar_f(A, B, F, G, eps, f, b)`: for an arrow `f` of `A` with codomain `G(b)`, the arrow $\varepsilon_b \circ F(f)$ of `B`.

    Then complete `round_trips`, which sends each pair `(a, g)`, with `g` an arrow of `B` out of `F(a)`, to the result of applying `bar_g` and then `bar_f`. For which of the four examples is every `g` returned unchanged? Compare with what the explorer of Section 4 reports for the same four pairs $(\eta, \varepsilon)$.
    """)
    return


@app.cell
def _():
    def _run():
        def bar_g(A, B, F, G, eta, a, g):
            # TODO: the composite in A of G(g) after eta[a]
            return ...

        def bar_f(A, B, F, G, eps, f, b):
            # TODO: the composite in B of eps[b] after F(f)
            return ...

        def round_trips(A, B, F, G, eta, eps):
            result = {}
            for a in A["objects"]:
                for g, (dom, cod) in B["arrows"].items():
                    if dom == F["objects"][a]:
                        # TODO: bar_f of bar_g of g   (at which object b is the counit taken?)
                        result[(a, g)] = ...
            return result

        # Z/3 as a one-object category: arrows "0", "1", "2", composition = addition mod 3
        Z3 = {
            "objects": ["*"],
            "arrows": {n: ("*", "*") for n in "012"},
            "identity": {"*": "0"},
            "compose": {(g, f): str((int(g) + int(f)) % 3) for g in "012" for f in "012"},
        }
        ident = {"objects": {"*": "*"}, "arrows": {"0": "0", "1": "1", "2": "2"}}
        neg = {"objects": {"*": "*"}, "arrows": {"0": "0", "1": "2", "2": "1"}}

        # A = the one-arrow category; B has objects X, Y, an idempotent t : X -> X and u : X -> Y
        ONE = {"objects": ["*"], "arrows": {"1*": ("*", "*")}, "identity": {"*": "1*"},
               "compose": {("1*", "1*"): "1*"}}
        B = {
            "objects": ["X", "Y"],
            "arrows": {"1X": ("X", "X"), "1Y": ("Y", "Y"), "t": ("X", "X"), "u": ("X", "Y")},
            "identity": {"X": "1X", "Y": "1Y"},
            "compose": {("1X", "1X"): "1X", ("t", "1X"): "t", ("1X", "t"): "t", ("t", "t"): "t",
                        ("u", "1X"): "u", ("u", "t"): "u", ("1Y", "u"): "u", ("1Y", "1Y"): "1Y"},
        }
        pickX = {"objects": {"*": "X"}, "arrows": {"1*": "1X"}}
        bang = {"objects": {"X": "*", "Y": "*"}, "arrows": {"1X": "1*", "1Y": "1*", "t": "1*", "u": "1*"}}

        # print(bar_g(Z3, Z3, ident, ident, {"*": "1"}, "*", "2"))      # expect 0
        # print(bar_f(Z3, Z3, ident, ident, {"*": "2"}, "2", "*"))      # expect 1
        # print(round_trips(Z3, Z3, ident, ident, {"*": "1"}, {"*": "2"}))
        # expect {('*', '0'): '0', ('*', '1'): '1', ('*', '2'): '2'}
        # print(round_trips(Z3, Z3, ident, ident, {"*": "1"}, {"*": "1"}))
        # expect {('*', '0'): '2', ('*', '1'): '0', ('*', '2'): '1'}
        # print(round_trips(Z3, Z3, neg, neg, {"*": "1"}, {"*": "1"}))
        # expect {('*', '0'): '0', ('*', '1'): '1', ('*', '2'): '2'}
        # print(round_trips(ONE, B, pickX, bang, {"*": "1*"}, {"X": "t", "Y": "u"}))
        # expect {('*', '1X'): 't', ('*', 't'): 't', ('*', 'u'): 'u'}

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
    | P01 | The unit and counit of the product adjunction — `exercises/2b/p01_product_unit_counit.md` | warm-up | unpacking a definition in an example |
    | P02 | The other composite of a Galois connection — `exercises/2b/p02_interior_operator.md` | warm-up | dualizing a lecture proof |
    | P03 | A right adjoint is faithful exactly when the counit is epic — `exercises/2b/p03_faithful_iff_counit_epic.md` | core | translating a property through the transpose |
    | P04 | Inverse image has a right adjoint — `exercises/2b/p04_inverse_image_right_adjoint.md` | core | unit–counit criterion in a poset |
    | P05 | Unit and counit of a composite adjunction — `exercises/2b/p05_composite_unit_counit.md` | core | triangle identities |
    | P06 | An adjunction restricts to an equivalence — `exercises/2b/p06_fixed_points_equivalence.md` | stretch | triangle identities and isomorphisms |

    **How to submit.** Write each proof in `proofs/2b/<same file name>.md`, in the five-step proof anatomy (Goal / Given / Plan / Proof / What made it work).
    Then ask Claude to review it: the review points at gaps and asks questions, and never supplies a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [2A: Adjunctions: Definition & Examples](../2a_adjunctions/) &nbsp;|&nbsp; Next: [2C: Adjunctions via Initial Objects](../2c_universal_arrows/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
