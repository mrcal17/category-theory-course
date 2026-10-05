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
    # 4B: The Yoneda Lemma

    > *"The Yoneda lemma is arguably the most important result in category theory."*
    > — Emily Riehl, *Category Theory in Context*, Chapter 2

    In 4A you met the representable presheaves $H_A = \mathcal{A}(-, A)$. This module asks one question about them: **given a presheaf $X$ on $\mathcal{A}$, what are the natural transformations $H_A \Rightarrow X$?** A natural transformation is a large thing: one function for every object of $\mathcal{A}$, subject to one equation for every arrow of $\mathcal{A}$. You might expect the answer to be complicated and to depend heavily on $\mathcal{A}$.

    It does not. The Yoneda lemma says that a natural transformation $H_A \Rightarrow X$ is the same thing as a single element of the set $X(A)$. The whole transformation is determined by one value, the value at the identity arrow $1_A$, and that one value can be chosen freely.

    The statement is short and the proof uses nothing beyond the definitions of functor and natural transformation. What makes it hard on first reading is the bookkeeping: there are several levels (arrows of $\mathcal{A}$, elements of sets, functions, natural transformations) and it is easy to lose track of which level a symbol lives on. So we go slowly. We prove the lemma first in a one-object category, where it is a statement about monoids and gives **Cayley's theorem**; then in a poset, where there is almost nothing to compute; and then in general, in six small labelled stages. By the end you will be able to write out the proof yourself, name the one idea that drives it (**follow the identity**), and use the same idea in proofs of your own.

    Throughout, $\mathcal{A}$ is a locally small category, a presheaf is a functor $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$, and we follow Leinster's variance: the lemma is about presheaves and $H_A$. The version for covariant functors and $H^A$ is stated in Section 8 and left for you to prove.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Question: Maps out of a Representable

    Before answering the question, make sure every word in it is unpacked.

    > **Definition (restated from 1D and 4A, for this situation).** Let $A$ be an object of $\mathcal{A}$ and $X$ a presheaf on $\mathcal{A}$. A **natural transformation** $\alpha \colon H_A \Rightarrow X$ consists of a function
    > $$\alpha_B \colon \mathcal{A}(B, A) \to X(B) \qquad \text{for each object } B \text{ of } \mathcal{A},$$
    > such that for every arrow $g \colon C \to B$ of $\mathcal{A}$ and every $p \in \mathcal{A}(B, A)$,
    > $$X(g)\big(\alpha_B(p)\big) = \alpha_C(p \circ g).$$
    > We write $\mathrm{Nat}(H_A, X)$ for the collection of all such natural transformations. It is the hom-collection $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, X)$ of the presheaf category.

    **Reading the definition.**
    - $\alpha_B$ takes an *arrow* $p \colon B \to A$ as input and returns an *element* of the set $X(B)$.
    - The equation is the naturality square of $\alpha$ at $g$, evaluated at $p$. The left side applies $\alpha_B$ and then the function $X(g) \colon X(B) \to X(C)$. The right side applies $H_A(g)$, which is $p \mapsto p \circ g$, and then $\alpha_C$.
    - Both sides are elements of $X(C)$. If your two sides live in different sets, something is on the wrong side.
    - There is one equation for every pair $(g, p)$ with $g \colon C \to B$ and $p \colon B \to A$.

    **Example (graphs).** Recall from 4A the category $\mathcal{G}$ with arrows $s, t \colon V \to E$, whose presheaves are directed graphs, and its representables: $H_V$ is the graph with one vertex and no edges, $H_E$ is the graph with one edge between two vertices. A natural transformation between presheaves on $\mathcal{G}$ is a map of graphs: a function on vertices and a function on edges that respect sources and targets. So a natural transformation $H_V \Rightarrow X$ is a map from the one-vertex graph into $X$, and to give one you choose a vertex of $X$. A natural transformation $H_E \Rightarrow X$ is a map from the one-edge graph into $X$; you choose an edge of $X$, and then the images of the two vertices are forced to be its source and target. In both cases: **natural transformations $H_A \Rightarrow X$ correspond to elements of $X(A)$.**

    **Example (sets).** Take $\mathcal{A} = \mathbf{Set}$ and $A = \varnothing$. Then $H_\varnothing(B) = \mathbf{Set}(B, \varnothing)$ is empty unless $B = \varnothing$, when it has exactly one element. A natural transformation $H_\varnothing \Rightarrow X$ therefore has only one component that is not an empty function, namely $\alpha_\varnothing$, and that component picks out one element of $X(\varnothing)$.

    **Non-example.** The question is about transformations *out of* $H_A$. Natural transformations $X \Rightarrow H_A$ *into* a representable are not described by the Yoneda lemma, and in general they are not determined by any single element. For graphs, a map from $X$ into the one-edge graph $H_E$ amounts to a way of splitting the vertices of $X$ into two classes with every edge running from the first class to the second; that is a different kind of data altogether.

    > [Leinster §4.2](https://arxiv.org/abs/1612.09375) poses exactly this question before stating the lemma. [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) begins from the same place.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. One Object: Monoids and Cayley's Theorem

    Take the smallest interesting case: a category with one object. Let $M$ be a monoid with identity $1$, regarded as a category with a single object $\star$, with arrows the elements of $M$ and with composition $m \circ n = mn$ (1A).

    **What is a presheaf?** A presheaf $X$ on $M$ is a set $S = X(\star)$ together with a function $X(m) \colon S \to S$ for each $m \in M$, such that $X(1) = 1_S$ and $X(mn) = X(n) \circ X(m)$. Write $x \cdot m$ for $X(m)(x)$. The two conditions become
    $$x \cdot 1 = x, \qquad x \cdot (mn) = (x \cdot m) \cdot n,$$
    where the second holds because $X(mn)(x) = X(n)\big(X(m)(x)\big)$. This is precisely a **right action** of $M$ on $S$. So a presheaf on $M$ is a right $M$-set.

    **What is the representable?** There is one object, so there is one representable presheaf, $H_\star$. Its set is $H_\star(\star) = M$, and $H_\star(m)$ sends $p$ to $p \circ m = pm$. In action notation, $p \cdot m = pm$: the monoid acting on itself by right multiplication.

    **What is a natural transformation $H_\star \Rightarrow X$?** It has one component, a function $\varphi \colon M \to S$, and the naturality equation of Section 1 reads $X(m)(\varphi(p)) = \varphi(pm)$, that is,
    $$\varphi(p) \cdot m = \varphi(pm) \qquad \text{for all } p, m \in M.$$
    Such a $\varphi$ is called an **equivariant map** from $M$ to $S$.

    > **Proposition 2.1 (Yoneda for a monoid).** Let $M$ be a monoid and $S$ a right $M$-set. Then the function
    > $$\{\text{equivariant maps } M \to S\} \to S, \qquad \varphi \mapsto \varphi(1),$$
    > is a bijection. Its inverse sends $x \in S$ to the map $\tilde{x} \colon M \to S$, $\tilde{x}(p) = x \cdot p$.

    - **Goal.** Three things. (i) For every $x \in S$, the map $\tilde{x}$ is equivariant: for all $p, m \in M$, $\tilde{x}(p) \cdot m = \tilde{x}(pm)$. (ii) For every $x \in S$, $\tilde{x}(1) = x$. (iii) For every equivariant $\varphi$, the map $\widetilde{\varphi(1)}$ equals $\varphi$: for all $p \in M$, $\varphi(1) \cdot p = \varphi(p)$.
    - **Given.** The action axioms $x \cdot 1 = x$ and $x \cdot (mn) = (x \cdot m) \cdot n$; the monoid axiom $1p = p$; equivariance of $\varphi$ in (iii).
    - **Plan.** Show that two functions are mutually inverse (0B). First check that the proposed inverse lands in the right set (i), then check the two composites (ii) and (iii). In (iii), apply equivariance of $\varphi$ at the identity element.
    - **Proof.** (i) $\tilde{x}(p) \cdot m = (x \cdot p) \cdot m = x \cdot (pm) = \tilde{x}(pm)$, by the definition of $\tilde{x}$, the second action axiom, and the definition of $\tilde{x}$ again.

      (ii) $\tilde{x}(1) = x \cdot 1 = x$ by the first action axiom.

      (iii) Let $p \in M$. Then $\varphi(1) \cdot p = \varphi(1p) = \varphi(p)$, by equivariance of $\varphi$ (with $1$ in the role of $p$ and $p$ in the role of $m$) and then the monoid identity axiom.

      By (i) the assignment $x \mapsto \tilde{x}$ is a function from $S$ to the set of equivariant maps; by (ii) and (iii) it is a two-sided inverse of $\varphi \mapsto \varphi(1)$. $\blacksquare$
    - **What made it work.** Every $p \in M$ can be written as $1p$, so equivariance transports the single value $\varphi(1)$ to every other value. **The identity element is the one place you need to look; everything else follows from it.** This is the whole Yoneda lemma in miniature.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cayley's theorem

    Now apply Proposition 2.1 to the right $M$-set $S = M$ itself (that is, take $X = H_\star$). For $x \in M$, the equivariant map $\tilde{x} \colon M \to M$ is $p \mapsto xp$: **left** multiplication by $x$. Write it $\lambda_x$. The proposition says:

    - every equivariant map $M \to M$ is $\lambda_x$ for exactly one $x \in M$, namely $x = \varphi(1)$.

    So $x \mapsto \lambda_x$ is a bijection from $M$ to the set $\mathrm{End}_M(M)$ of equivariant maps $M \to M$. It also respects the monoid structures, where $\mathrm{End}_M(M)$ is a monoid under composition of functions:
    $$\lambda_1(p) = 1p = p, \qquad \lambda_{xy}(p) = (xy)p = x(yp) = \lambda_x(\lambda_y(p)),$$
    by the identity axiom and associativity in $M$. So $\lambda_1 = 1_M$ and $\lambda_{xy} = \lambda_x \circ \lambda_y$. (We should also confirm that the composite of two equivariant maps is equivariant and that the identity function is: $\psi(\varphi(p)) \cdot m = \psi(\varphi(p) \cdot m) = \psi(\varphi(pm))$, and $1_M(p) \cdot m = pm = 1_M(pm)$.)

    > **Theorem 2.2 (Cayley, for monoids).** Every monoid $M$ is isomorphic to a monoid of functions from a set to itself under composition. Precisely, $x \mapsto \lambda_x$ is an injective monoid homomorphism $M \to \mathbf{Set}(M, M)$ whose image is $\mathrm{End}_M(M)$.
    >
    > **Corollary 2.3 (Cayley, for groups).** Every group $G$ is isomorphic to a subgroup of the group $\mathrm{Sym}(G)$ of permutations of its underlying set.

    For the corollary: when $G$ is a group, $\lambda_x \circ \lambda_{x^{-1}} = \lambda_{x x^{-1}} = \lambda_1 = 1_G$ and likewise in the other order, so each $\lambda_x$ is a bijection and $x \mapsto \lambda_x$ lands in $\mathrm{Sym}(G)$. It is an injective group homomorphism by Theorem 2.2, hence an isomorphism onto its image, which is a subgroup.

    You probably proved Cayley's theorem in an algebra course by defining $\lambda_x$ and checking these facts directly. What the Yoneda viewpoint adds is the description of the image: the permutations $\lambda_x$ are *exactly* the functions $G \to G$ that commute with all right multiplications. Left multiplications are the natural endomorphisms of right multiplication.

    **Example.** For $M = (\mathbb{Z}/3, +)$, the map $\lambda_1$ is the cyclic permutation $0 \mapsto 1 \mapsto 2 \mapsto 0$, and $\mathbb{Z}/3$ is identified with the three rotations inside the six-element group $\mathrm{Sym}(\{0, 1, 2\})$.

    **Example (a monoid that is not a group).** Let $M = \{e, a, b\}$ with identity $e$ and $xy = x$ whenever $x \ne e$. Then $\lambda_a$ is the constant function with value $a$ and $\lambda_b$ is the constant function with value $b$. These are not permutations, but $x \mapsto \lambda_x$ is still injective, since $\lambda_x(e) = x$.

    **Non-example.** *Right* multiplication $\rho_x \colon p \mapsto px$ is not in general equivariant for the right action: equivariance would require $(px)m = (pm)x$ for all $p, m$, which fails in a non-commutative monoid. In the monoid $\{e, a, b\}$ above, $x \mapsto \rho_x$ is not even a homomorphism into $\mathbf{Set}(M, M)$ under composition: $\rho_{ab} = \rho_a$, whereas $(\rho_a \circ \rho_b)(e) = \rho_a(b) = b$ and $\rho_a(e) = a$. Which side you multiply on matters, and the Yoneda lemma tells you which side is the right one.

    > [Leinster §4.2](https://arxiv.org/abs/1612.09375) discusses the one-object case of the lemma. [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) derives Cayley's theorem as a corollary of the Yoneda lemma.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Many Objects, Few Arrows: Posets

    A monoid has one object and many arrows. A poset is the opposite extreme: many objects, and at most one arrow between any two. Let $P$ be a poset regarded as a category, with one arrow $b \to a$ exactly when $b \le a$.

    **What is a presheaf?** A presheaf $X$ on $P$ is a set $X(a)$ for each $a \in P$ and a function
    $$\rho^a_b \colon X(a) \to X(b) \qquad \text{whenever } b \le a$$
    (we write $\rho^a_b$ for $X$ applied to the unique arrow $b \to a$), such that $\rho^a_a = 1_{X(a)}$ and $\rho^b_c \circ \rho^a_b = \rho^a_c$ whenever $c \le b \le a$. Call $\rho^a_b$ *restriction* from $a$ down to $b$.

    **What is the representable?** $H_a(b) = P(b, a)$ is a one-element set if $b \le a$ and is empty otherwise. Write $\ast_b$ for its unique element when $b \le a$. The function $H_a(c \le b)$ sends $\ast_b$ to $\ast_c$; it has no choice.

    **What is a natural transformation $\alpha \colon H_a \Rightarrow X$?** For each $b \le a$, the component $\alpha_b$ is a function from a one-element set to $X(b)$: it picks out an element $x_b = \alpha_b(\ast_b) \in X(b)$. For each $b \not\le a$, the component $\alpha_b$ is the empty function, and there is nothing to choose. Naturality at $c \le b$ says, when $b \le a$,
    $$\rho^b_c(x_b) = x_c,$$
    and says nothing when $b \not\le a$, because then there is no $p \in H_a(b)$ at which to evaluate the equation.

    So a natural transformation $H_a \Rightarrow X$ is a family $(x_b)_{b \le a}$ with $x_b \in X(b)$, compatible with restriction. Now follow the top of the family. Since $a \le a$, the family has a member $x_a \in X(a)$; and taking $b = a$ in the compatibility condition gives, for every $c \le a$,
    $$x_c = \rho^a_c(x_a).$$
    The whole family is determined by $x_a$. Conversely, given any $x \in X(a)$, the family $x_c = \rho^a_c(x)$ is compatible: $\rho^b_c(x_b) = \rho^b_c(\rho^a_b(x)) = \rho^a_c(x) = x_c$ by the composition rule for restrictions, and its top member is $\rho^a_a(x) = x$ by the identity rule. Hence

    $$\mathrm{Nat}(H_a, X) \cong X(a), \qquad \alpha \mapsto x_a = \alpha_a(\ast_a).$$

    Note that $\ast_a$, the unique element of $P(a, a)$, is the identity arrow $1_a$. Once again the bijection is "evaluate at the identity".

    **Example ($X$ itself representable).** Take $X = H_b$. Then $\mathrm{Nat}(H_a, H_b) \cong H_b(a) = P(a, b)$: there is a natural transformation $H_a \Rightarrow H_b$ if and only if $a \le b$, and then there is exactly one.

    **Example (functions on open sets).** Let $P$ be the poset of open subsets of $\mathbb{R}$ under inclusion, and let $X(U)$ be the set of continuous functions $U \to \mathbb{R}$, with $\rho^U_V$ the restriction of a function to a smaller open set $V \subseteq U$. A natural transformation $H_U \Rightarrow X$ is a compatible choice of a continuous function on every open $V \subseteq U$, and the computation above says that this is the same as one continuous function on $U$ together with all its restrictions.

    **Non-example.** Compatibility in the *upward* direction is not automatic. A family $(x_b)_{b \in D}$ with $x_b \in X(b)$ indexed by a down-closed set $D \subseteq P$ that has no greatest element (for instance $D = \{0, a, b\}$ in the diamond $0 \le a, b \le 1$), compatible with restriction, need not come from any single element of any $X(c)$. Such families are natural transformations out of a presheaf that is not representable, and the Yoneda lemma does not describe them.

    > [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) treats the poset case of the Yoneda lemma; presheaves on a poset of open sets are the original "presheaves" of Leinster §1.2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Statement

    Three examples, one pattern: a natural transformation out of $H_A$ is known once you know where it sends the identity. Here is the general statement.

    > **Theorem 4.1 (the Yoneda lemma).** Let $\mathcal{A}$ be a locally small category. Then
    > $$\boxed{\;[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, X) \;\cong\; X(A)\;}$$
    > naturally in $A \in \mathcal{A}$ and $X \in [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$.

    **Reading the statement.** The left side is $\mathrm{Nat}(H_A, X)$; the right side is a set you can write down without knowing anything about natural transformations. The symbol $\cong$ with the words "naturally in $A$ and $X$" packs in three separate claims.

    - **(Y1) A bijection.** For every object $A$ of $\mathcal{A}$ and every presheaf $X$ on $\mathcal{A}$, the function
      $$\widehat{(\ )} \colon \mathrm{Nat}(H_A, X) \to X(A), \qquad \hat{\alpha} = \alpha_A(1_A),$$
      is a bijection. Its inverse is written $x \mapsto \tilde{x}$ and is given by $\tilde{x}_B(p) = X(p)(x)$ for $p \in \mathcal{A}(B, A)$.
    - **(Y2) Naturality in $X$.** For every natural transformation $\theta \colon X \Rightarrow X'$ between presheaves and every $\alpha \in \mathrm{Nat}(H_A, X)$,
      $$\widehat{\theta \circ \alpha} = \theta_A(\hat{\alpha}).$$
    - **(Y3) Naturality in $A$.** For every arrow $f \colon B \to A$ of $\mathcal{A}$ and every $\alpha \in \mathrm{Nat}(H_A, X)$,
      $$\widehat{\alpha \circ H_f} = X(f)(\hat{\alpha}).$$

    Why are (Y2) and (Y3) the right equations? "Natural in $A$ and $X$" means that both sides are functors of the pair $(A, X)$ and that the bijections form a natural transformation between them. Both sides are functors $\mathcal{A}^{\mathrm{op}} \times [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}] \to \mathbf{Set}$:

    | | on objects | on $\theta \colon X \Rightarrow X'$ | on $f \colon B \to A$ |
    |---|---|---|---|
    | left side | $(A, X) \mapsto \mathrm{Nat}(H_A, X)$ | $\alpha \mapsto \theta \circ \alpha$ | $\alpha \mapsto \alpha \circ H_f$ |
    | right side | $(A, X) \mapsto X(A)$ | $x \mapsto \theta_A(x)$ | $x \mapsto X(f)(x)$ |

    In the last column, $H_f \colon H_B \Rightarrow H_A$ is the natural transformation from 4A with $(H_f)_C(q) = f \circ q$, so $\alpha \circ H_f \colon H_B \Rightarrow X$. Both sides are contravariant in $A$ and covariant in $X$. (Y2) and (Y3) are the naturality squares for the second and third columns.

    A general arrow of the product category is a pair $(f, \theta)$, and you might worry that naturality has to be checked for all pairs at once. It does not: $(f, \theta) = (f, 1_{X'}) \circ (1_A, \theta)$ in $\mathcal{A}^{\mathrm{op}} \times [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$, both functors preserve this composite, and so the naturality square for $(f, \theta)$ is the square for $(1_A, \theta)$ pasted onto the square for $(f, 1_{X'})$. Two commuting squares paste to a commuting rectangle (1D). So (Y2) and (Y3) together give naturality in the pair.

    **Examples of what the statement says.**
    - *Monoid $M$, right $M$-set $S$:* equivariant maps $M \to S$ correspond to elements of $S$ (Proposition 2.1).
    - *Poset $P$:* compatible families below $a$ correspond to elements of $X(a)$ (Section 3).
    - *Graphs:* graph maps from the one-edge graph $H_E$ into a graph $X$ correspond to edges of $X$ (Section 1).

    **Non-example (what it does not say).** The lemma does not say that $H_A \cong X$, and it does not say that $X$ is representable. It describes the *set of maps* from $H_A$ to $X$ for an arbitrary presheaf $X$. Whether one of those maps is an isomorphism is a separate question, taken up in 4C.

    **A remark on size.** The functor category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ need not be locally small when $\mathcal{A}$ is large (3A), so in principle $\mathrm{Nat}(H_A, X)$ might be a proper class. Part of what (Y1) proves is that it is not: it is in bijection with the set $X(A)$.

    > The statement and its unpacking follow [Leinster §4.2](https://arxiv.org/abs/1612.09375). [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) states the covariant form first; the two are dual.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The Proof, Part One: The Bijection

    We prove (Y1) in four stages. Fix an object $A$ of $\mathcal{A}$ and a presheaf $X$ on $\mathcal{A}$ for the whole of this section.

    ### Stage 1. From a transformation to an element: $\alpha \mapsto \hat{\alpha}$

    Given $\alpha \colon H_A \Rightarrow X$, its component at $A$ is a function $\alpha_A \colon \mathcal{A}(A, A) \to X(A)$. The set $\mathcal{A}(A, A)$ is guaranteed to contain one element, the identity $1_A$. Define
    $$\hat{\alpha} = \alpha_A(1_A) \in X(A).$$
    There is nothing to check: $\alpha_A$ is a function and $1_A$ is in its domain. This is the move called **following the identity**: of all the inputs you could feed to $\alpha$, the identity is the only one that every category provides.

    ### Stage 2. From an element to a transformation: $x \mapsto \tilde{x}$, and why $\tilde{x}$ is natural

    Given $x \in X(A)$, we need a function $\tilde{x}_B \colon \mathcal{A}(B, A) \to X(B)$ for each $B$. An arrow $p \colon B \to A$ gives a function $X(p) \colon X(A) \to X(B)$, because $X$ is contravariant, and $x$ is an element of its domain. Define
    $$\tilde{x}_B(p) = X(p)(x).$$
    This is the only thing that type-checks. But a family of functions is not yet a natural transformation; that has to be proved.

    > **Lemma 5.1.** For every $x \in X(A)$, the family $(\tilde{x}_B)_{B \in \mathcal{A}}$ is a natural transformation $H_A \Rightarrow X$.

    - **Goal.** For every arrow $g \colon C \to B$ of $\mathcal{A}$ and every $p \in \mathcal{A}(B, A)$: $\;X(g)\big(\tilde{x}_B(p)\big) = \tilde{x}_C(p \circ g)$.
    - **Given.** The definition $\tilde{x}_B(p) = X(p)(x)$. The fact that $X$ is a functor $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$, so $X(p \circ g) = X(g) \circ X(p)$ for $C \xrightarrow{g} B \xrightarrow{p} A$.
    - **Plan.** Direct computation: expand both sides using the definition of $\tilde{x}$ and compare.
    - **Proof.** Let $g \colon C \to B$ and $p \in \mathcal{A}(B, A)$. Then
      $$X(g)\big(\tilde{x}_B(p)\big) = X(g)\big(X(p)(x)\big) = \big(X(g) \circ X(p)\big)(x) = X(p \circ g)(x) = \tilde{x}_C(p \circ g),$$
      by the definition of $\tilde{x}_B$, the definition of composition of functions, functoriality of $X$, and the definition of $\tilde{x}_C$. $\blacksquare$
    - **What made it work.** Naturality of $\tilde{x}$ *is* functoriality of $X$. The axiom $X(p \circ g) = X(g) \circ X(p)$, which looked like bookkeeping when presheaves were defined, is exactly what makes every element of $X(A)$ generate a natural transformation.

    ### Stage 3. Element $\to$ transformation $\to$ element gives back the element

    > **Lemma 5.2.** For every $x \in X(A)$, $\;\hat{\tilde{x}} = x$.

    - **Goal.** For every $x \in X(A)$: $\tilde{x}_A(1_A) = x$.
    - **Given.** The definitions of $\hat{\ }$ and $\tilde{\ }$; the functor axiom $X(1_A) = 1_{X(A)}$.
    - **Plan.** Direct computation.
    - **Proof.** $\hat{\tilde{x}} = \tilde{x}_A(1_A) = X(1_A)(x) = 1_{X(A)}(x) = x$, by the definition of $\hat{\ }$, the definition of $\tilde{x}_A$, the identity axiom for the functor $X$, and the definition of an identity function. $\blacksquare$
    - **What made it work.** The other functor axiom. Stage 2 used "$X$ preserves composition"; Stage 3 uses "$X$ preserves identities". Together they use up the definition of a presheaf.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Stage 4. Transformation $\to$ element $\to$ transformation gives back the transformation

    This is the stage that carries the content of the lemma: a natural transformation out of $H_A$ is *determined* by its value at $1_A$. Look at the naturality square of $\alpha$ at an arrow $f \colon B \to A$, and at what happens to the element $1_A$ in its top-left corner.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        nodes={
            "TL": (0, 2, r"$\mathcal{A}(A, A)$"), "TR": (4, 2, r"$X(A)$"),
            "BL": (0, 0, r"$\mathcal{A}(B, A)$"), "BR": (4, 0, r"$X(B)$"),
            # invisible anchors keep the horizontal arrows clear of the wide labels
            "TLr": (0.6, 2, ""), "TRl": (3.7, 2, ""), "BLr": (0.6, 0, ""), "BRl": (3.7, 0, ""),
            "L": (-1.1, 1, r"$H_A(f) = - \circ f$"), "R": (4.7, 1, r"$X(f)$"),
        },
        arrows=[
            ("TLr", "TRl", r"$\alpha_A$"),
            ("BLr", "BRl", r"$\alpha_B$", {"side": -1}),
            ("TL", "BL", ""),
            ("TR", "BR", ""),
        ],
        figsize=(7.0, 3.6),
        title=r"Naturality of $\alpha$ at $f : B \to A$",
    )
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        nodes={
            "TL": (0, 2, r"$1_A$"), "TR": (4, 2, r"$\alpha_A(1_A) = \hat{\alpha}$"),
            "BL": (0, 0, r"$1_A \circ f = f$"), "BR": (4, 0, r"$\alpha_B(f) = X(f)(\hat{\alpha})$"),
            "TLr": (0.1, 2, ""), "TRl": (3.1, 2, ""), "BLr": (0.7, 0, ""), "BRl": (2.6, 0, ""),
        },
        arrows=[
            ("TLr", "TRl", r"$\alpha_A$", {"color": "#b45309"}),
            ("BLr", "BRl", r"$\alpha_B$", {"side": -1, "color": "#b45309"}),
            ("TL", "BL", "", {"color": "#b45309"}),
            ("TR", "BR", "", {"color": "#b45309"}),
        ],
        figsize=(7.0, 3.4),
        title=r"Follow the identity: chase the element $1_A$ around the same square",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Lemma 5.3.** For every natural transformation $\alpha \colon H_A \Rightarrow X$, $\;\tilde{\hat{\alpha}} = \alpha$.

    - **Goal.** Two natural transformations are equal when all their components are equal, and two functions are equal when they agree on every input. So the goal is: for every object $B$ of $\mathcal{A}$ and every $f \in \mathcal{A}(B, A)$, $\;\tilde{\hat{\alpha}}_B(f) = \alpha_B(f)$.
    - **Given.** The definitions $\hat{\alpha} = \alpha_A(1_A)$ and $\tilde{x}_B(f) = X(f)(x)$. Naturality of $\alpha$: for every $g \colon C \to B$ and $p \in \mathcal{A}(B, A)$, $X(g)(\alpha_B(p)) = \alpha_C(p \circ g)$. The identity axiom of $\mathcal{A}$.
    - **Plan.** Follow the identity. Use naturality of $\alpha$ at the arrow $f$ itself, evaluated at the element $1_A$. This is the square drawn above.
    - **Proof.** Let $B$ be an object of $\mathcal{A}$ and $f \in \mathcal{A}(B, A)$. Then
      $$\tilde{\hat{\alpha}}_B(f) = X(f)(\hat{\alpha}) = X(f)\big(\alpha_A(1_A)\big) = \alpha_B(1_A \circ f) = \alpha_B(f).$$
      The first equality is the definition of $\tilde{\ }$ applied to the element $\hat{\alpha}$. The second is the definition of $\hat{\alpha}$. The third is naturality of $\alpha$, used with $g = f \colon B \to A$ and $p = 1_A \in \mathcal{A}(A, A)$ (so the roles of "$B$" and "$C$" in the naturality equation are played by $A$ and $B$). The fourth is the identity axiom in $\mathcal{A}$. $\blacksquare$
    - **What made it work.** Every arrow $f \colon B \to A$ is the image of $1_A$ under $H_A(f)$, because $1_A \circ f = f$. So $1_A$ "generates" the presheaf $H_A$, and naturality forces $\alpha$ to be determined by what it does to the generator. Reach for this whenever a proof involves a natural transformation whose domain is a hom-functor: **apply naturality at $f$ and evaluate at the identity.**

    **Conclusion of Part One.** By Lemma 5.1, $x \mapsto \tilde{x}$ is a function $X(A) \to \mathrm{Nat}(H_A, X)$. By Lemmas 5.2 and 5.3 it is a two-sided inverse of $\alpha \mapsto \hat{\alpha}$. So $\widehat{(\ )}$ is a bijection, which is (Y1).

    Compare the three lines of Proposition 2.1 with Lemmas 5.1, 5.2 and 5.3. They are the same three computations: $x \cdot (pm) = (x \cdot p) \cdot m$ became functoriality of $X$, $x \cdot 1 = x$ became $X(1_A) = 1$, and $\varphi(1) \cdot p = \varphi(1p)$ became naturality at $f$ evaluated at $1_A$.

    > The four stages follow the proof in [Leinster §4.2](https://arxiv.org/abs/1612.09375). [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) gives the same argument for covariant functors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. The Proof, Part Two: Naturality

    A bijection for each pair $(A, X)$ is not yet the theorem. We must show that these bijections fit together as $X$ varies and as $A$ varies. It is enough to do this for the maps $\widehat{(\ )}$: a natural transformation whose components are all bijections is a natural isomorphism (1D), so the inverse maps $\tilde{(\ )}$ are then natural too.

    ### Stage 5. Naturality in $X$

    > **Lemma 6.1 (Y2).** Let $A$ be an object of $\mathcal{A}$ and $\theta \colon X \Rightarrow X'$ a natural transformation between presheaves on $\mathcal{A}$. Then for every $\alpha \in \mathrm{Nat}(H_A, X)$, $\;\widehat{\theta \circ \alpha} = \theta_A(\hat{\alpha})$.

    - **Goal.** The equation above, for every $\alpha$. It says that the left-hand square in the figure below commutes.
    - **Given.** The definition of $\hat{\ }$. The definition of vertical composition of natural transformations (1D): $(\theta \circ \alpha)_B = \theta_B \circ \alpha_B$ for every $B$.
    - **Plan.** Direct computation, evaluating at $1_A$.
    - **Proof.** $\widehat{\theta \circ \alpha} = (\theta \circ \alpha)_A(1_A) = \theta_A\big(\alpha_A(1_A)\big) = \theta_A(\hat{\alpha})$, by the definition of $\hat{\ }$, the definition of vertical composition, and the definition of $\hat{\ }$ again. $\blacksquare$
    - **What made it work.** Vertical composition is defined component by component, and $\hat{\ }$ only ever looks at the component at $A$. Nothing about $\theta$ being natural was needed.

    ### Stage 6. Naturality in $A$

    > **Lemma 6.2 (Y3).** Let $X$ be a presheaf on $\mathcal{A}$ and $f \colon B \to A$ an arrow of $\mathcal{A}$. Then for every $\alpha \in \mathrm{Nat}(H_A, X)$, $\;\widehat{\alpha \circ H_f} = X(f)(\hat{\alpha})$.

    - **Goal.** The equation above, for every $\alpha$. Here $\alpha \circ H_f \colon H_B \Rightarrow X$, so the hat on the left is the one for the object $B$: it evaluates the component at $B$ on $1_B$. The equation says that the right-hand square in the figure below commutes.
    - **Given.** The definitions of $\hat{\ }$ and of $H_f$ (4A): $(H_f)_C(q) = f \circ q$. Naturality of $\alpha$. The identity axioms of $\mathcal{A}$.
    - **Plan.** Compute each side separately and show that both equal $\alpha_B(f)$. The right side needs the follow-the-identity step of Lemma 5.3.
    - **Proof.** Left side:
      $$\widehat{\alpha \circ H_f} = (\alpha \circ H_f)_B(1_B) = \alpha_B\big((H_f)_B(1_B)\big) = \alpha_B(f \circ 1_B) = \alpha_B(f),$$
      by the definition of $\hat{\ }$ at $B$, vertical composition, the definition of $H_f$, and the identity axiom. Right side:
      $$X(f)(\hat{\alpha}) = X(f)\big(\alpha_A(1_A)\big) = \alpha_B(1_A \circ f) = \alpha_B(f),$$
      by the definition of $\hat{\ }$ at $A$, naturality of $\alpha$ at $f$ evaluated at $1_A$, and the identity axiom. The two sides are equal. $\blacksquare$
    - **What made it work.** The arrow $f$ can be written as $f \circ 1_B$ or as $1_A \circ f$. The left side of (Y3) uses the first way, the right side uses the second, and the two identity axioms say they are the same arrow.

    As explained in Section 4, (Y2) and (Y3) together give naturality in the pair $(A, X)$. With (Y1), this completes the proof of Theorem 4.1. $\blacksquare$
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        nodes={
            "TL": (0, 2, r"$\mathrm{Nat}(H_A, X)$"), "TR": (3.6, 2, r"$X(A)$"),
            "BL": (0, 0, r"$\mathrm{Nat}(H_A, X')$"), "BR": (3.6, 0, r"$X'(A)$"),
            "TLr": (0.85, 2, ""), "TRl": (3.3, 2, ""), "BLr": (0.85, 0, ""), "BRl": (3.3, 0, ""),
            "L": (-0.75, 1, r"$\theta \circ -$"), "R": (4.05, 1, r"$\theta_A$"),
            "TL2": (6.6, 2, r"$\mathrm{Nat}(H_A, X)$"), "TR2": (10.2, 2, r"$X(A)$"),
            "BL2": (6.6, 0, r"$\mathrm{Nat}(H_B, X)$"), "BR2": (10.2, 0, r"$X(B)$"),
            "TLr2": (7.45, 2, ""), "TRl2": (9.9, 2, ""), "BLr2": (7.45, 0, ""), "BRl2": (9.9, 0, ""),
            "L2": (5.75, 1, r"$- \circ H_f$"), "R2": (10.75, 1, r"$X(f)$"),
        },
        arrows=[
            ("TLr", "TRl", r"$\widehat{(\ )}$"), ("BLr", "BRl", r"$\widehat{(\ )}$", {"side": -1}),
            ("TL", "BL", ""), ("TR", "BR", ""),
            ("TLr2", "TRl2", r"$\widehat{(\ )}$"), ("BLr2", "BRl2", r"$\widehat{(\ )}$", {"side": -1}),
            ("TL2", "BL2", ""), ("TR2", "BR2", ""),
        ],
        figsize=(11.0, 3.4),
        title=r"Left: naturality in $X$, for $\theta : X \Rightarrow X'$.     Right: naturality in $A$, for $f : B \to A$.",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example (Y3 for graphs).** Take $f = s \colon V \to E$ and a graph $X$. An element of $X(E)$ is an edge $e$, and $\tilde{e} \colon H_E \Rightarrow X$ is the graph map that sends the generic edge to $e$. Then $\tilde{e} \circ H_s$ is a map from the one-vertex graph into $X$, and (Y3) says that the vertex it picks out is $X(s)(e)$, the source of $e$. "Restrict the map to the source vertex" on the left matches "take the source" on the right.

    **Example (Y2 for a monoid).** For right $M$-sets $S$ and $S'$ and an equivariant map $\theta \colon S \to S'$, (Y2) says $(\theta \circ \varphi)(1) = \theta(\varphi(1))$.

    **Non-example (bijections that are not natural).** Having a bijection for each object is weaker than having a natural family. Take the bijections $\alpha_B \colon \mathbf{Set}(B, 2) \to \mathscr{P}(B)$, $\chi \mapsto \chi^{-1}\{1\}$, of 4A, and change just one of them: at the set $2 = \{0, 1\}$ use $\beta_2(\chi) = \chi^{-1}\{0\}$ instead, and put $\beta_B = \alpha_B$ for every other set $B$. Every $\beta_B$ is still a bijection. But naturality fails at the function $g \colon 1 \to 2$ with value $0$, evaluated at $\chi = 1_2$: going one way round the square gives $g^{-1}(\beta_2(1_2)) = g^{-1}\{0\} = 1$, and going the other way gives $\beta_1(1_2 \circ g) = g^{-1}\{1\} = \varnothing$. The Yoneda bijection is not an arbitrary matching of sets of the same size; (Y2) and (Y3) are what make it usable in proofs.

    > [Leinster §4.2](https://arxiv.org/abs/1612.09375) proves naturality in $A$ and $X$ after the bijection, as here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. See It: The Yoneda Bijection in a Finite Category

    In a finite category, with a presheaf of finite sets, you can list every natural transformation $H_A \Rightarrow X$ by brute force: try every family of functions and keep those that satisfy every naturality equation. The widget does this without using the Yoneda lemma, then records where each surviving transformation sends $1_A$. Check two things in each scenario: the number of natural transformations equals the number of elements of $X(A)$, and each element of $X(A)$ appears exactly once in the last column.
    """)
    return


@app.cell
def _(mo):
    def _scenarios():
        def _mk(objects, arrows, comp):
            _arr = {"1" + _o: (_o, _o) for _o in objects}
            _arr.update(arrows)
            _c = {}
            for _f, (_a, _b) in _arr.items():
                _c[(_f, "1" + _a)] = _f
                _c[("1" + _b, _f)] = _f
            _c.update(comp)
            return {"objects": list(objects), "arrows": _arr,
                    "identity": {_o: "1" + _o for _o in objects}, "compose": _c}

        def _from_monoid(elements, mul, e):
            return {"objects": ["*"], "arrows": {_m: ("*", "*") for _m in elements}, "identity": {"*": e},
                    "compose": {(_g, _f): mul(_g, _f) for _g in elements for _f in elements}}

        def _graph(vertices, edges):
            return {"objects": {"V": list(vertices), "E": list(edges)},
                    "arrows": {"1V": {_v: _v for _v in vertices}, "1E": {_e: _e for _e in edges},
                               "s": {_e: _st[0] for _e, _st in edges.items()},
                               "t": {_e: _st[1] for _e, _st in edges.items()}}}

        _gcat = _mk(["V", "E"], {"s": ("V", "E"), "t": ("V", "E")}, {})
        _tri = _graph(["v1", "v2", "v3"], {"a": ("v1", "v2"), "b": ("v2", "v3"), "c": ("v1", "v3")})
        _loop = _graph(["x"], {"k": ("x", "x")})

        _z = ["0", "1", "2"]
        _z3 = _from_monoid(_z, lambda _g, _f: str((int(_g) + int(_f)) % 3), "0")
        _s4 = {"objects": {"*": ["x0", "x1", "x2", "y"]},
               "arrows": {_m: {**{f"x{_i}": f"x{(_i + int(_m)) % 3}" for _i in range(3)}, "y": "y"} for _m in _z}}

        _m = ["e", "a", "b"]
        _m3 = _from_monoid(_m, lambda _x, _y: _y if _x == "e" else _x, "e")
        _m3reg = {"objects": {"*": list(_m)},
                  "arrows": {_g: {_p: _m3["compose"][(_p, _g)] for _p in _m} for _g in _m}}

        _els = ["0", "a", "b", "1"]

        def _leq(_x, _y):
            return _x == _y or _x == "0" or _y == "1"

        _dia = {"objects": _els,
                "arrows": {f"{_x}<={_y}": (_x, _y) for _x in _els for _y in _els if _leq(_x, _y)},
                "identity": {_x: f"{_x}<={_x}" for _x in _els},
                "compose": {(f"{_y}<={_w}", f"{_x}<={_y}"): f"{_x}<={_w}"
                            for _x in _els for _y in _els for _w in _els if _leq(_x, _y) and _leq(_y, _w)}}
        _xd = {"objects": {"1": ["u", "v"], "a": ["a1", "a2"], "b": ["b1"], "0": ["z1", "z2"]},
               "arrows": {"0<=0": {"z1": "z1", "z2": "z2"}, "a<=a": {"a1": "a1", "a2": "a2"},
                          "b<=b": {"b1": "b1"}, "1<=1": {"u": "u", "v": "v"},
                          "a<=1": {"u": "a1", "v": "a2"}, "b<=1": {"u": "b1", "v": "b1"},
                          "0<=a": {"a1": "z1", "a2": "z1"}, "0<=b": {"b1": "z1"},
                          "0<=1": {"u": "z1", "v": "z1"}}}
        return {
            "Graphs: A = V, X = a triangle graph (3 vertices, 3 edges)": (_gcat, "V", _tri),
            "Graphs: A = E, X = a triangle graph (3 vertices, 3 edges)": (_gcat, "E", _tri),
            "Graphs: A = E, X = one vertex with a loop": (_gcat, "E", _loop),
            "Group Z/3: X = a right Z/3-set with 4 elements (a 3-cycle and a fixed point)": (_z3, "*", _s4),
            "Monoid {e, a, b}: X = H_* itself (Cayley)": (_m3, "*", _m3reg),
            "Diamond poset: A = 1 (top), X with X(1) = {u, v}": (_dia, "1", _xd),
            "Diamond poset: A = b, X with X(b) = {b1}": (_dia, "b", _xd),
            "Diamond poset: A = 0 (bottom), X with X(0) = {z1, z2}": (_dia, "0", _xd),
        }

    yoneda_scenarios = _scenarios()
    yoneda_choice = mo.ui.dropdown(options=list(yoneda_scenarios), value=list(yoneda_scenarios)[1],
                                   label="Category, object A and presheaf X")
    mo.vstack([mo.md("**Natural transformations $H_A \\Rightarrow X$ versus elements of $X(A)$**"), yoneda_choice])
    return yoneda_choice, yoneda_scenarios


@app.cell(hide_code=True)
def _(mo, yoneda_choice, yoneda_scenarios):
    def _run():
        import itertools

        _cat, _A, _X = yoneda_scenarios[yoneda_choice.value]
        _objs = _cat["objects"]
        _arr = _cat["arrows"]
        _H = {_B: [_p for _p, _dc in _arr.items() if _dc == (_B, _A)] for _B in _objs}
        _Hmap = {_g: {_p: _cat["compose"][(_p, _g)] for _p in _H[_c]} for _g, (_d, _c) in _arr.items()}

        # Brute force: every family of functions H_A(B) -> X(B), filtered by the naturality equations.
        _choices = [list(itertools.product(_X["objects"][_B], repeat=len(_H[_B]))) for _B in _objs]
        _tried = 1
        for _ch in _choices:
            _tried *= len(_ch)
        _nats = []
        for _combo in itertools.product(*_choices):
            _al = {_B: dict(zip(_H[_B], _vals)) for _B, _vals in zip(_objs, _combo)}
            if all(_X["arrows"][_g][_al[_c][_p]] == _al[_d][_Hmap[_g][_p]]
                   for _g, (_d, _c) in _arr.items() for _p in _H[_c]):
                _nats.append(_al)

        def _show(_items):
            return "{ " + ", ".join(f"`{_i}`" for _i in _items) + " }" if _items else "empty set"

        _lines = [f"**Object A = `{_A}`.**  Identity arrow: `{_cat['identity'][_A]}`.", "",
                  "| object B | H_A(B) = arrows B &#8594; A | X(B) |", "|---|---|---|"]
        for _B in _objs:
            _lines.append(f"| `{_B}` | {_show(_H[_B])} | {_show(_X['objects'][_B])} |")
        _lines += ["", f"Families of functions tried: **{_tried}**.  Natural ones: **{len(_nats)}**.  "
                       f"Elements of X(A): **{len(_X['objects'][_A])}**.", "",
                   "| # | the natural transformation, component by component | its value at the identity |",
                   "|---|---|---|"]
        _hats = []
        for _i, _al in enumerate(_nats, start=1):
            _parts = []
            for _B in _objs:
                if _H[_B]:
                    _parts.append(f"at `{_B}`: " + ", ".join(f"`{_p}` &#8614; `{_v}`" for _p, _v in _al[_B].items()))
                else:
                    _parts.append(f"at `{_B}`: empty function")
            _hat = _al[_A][_cat["identity"][_A]]
            _hats.append(_hat)
            _lines.append(f"| {_i} | " + "; ".join(_parts) + f" | `{_hat}` |")
        _ok = sorted(_hats) == sorted(_X["objects"][_A])
        _lines += ["", "Each element of X(A) appears exactly once in the last column: **"
                   + ("yes" if _ok else "no") + "**."]
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to notice. With $A = E$ and the triangle graph, $3^2 \cdot 3 = 27$ families of functions are tried and only $3$ are natural: once the image of the edge `1E` is chosen, the images of `s` and `t` are forced. In the $\mathbb{Z}/3$ scenario the fixed point `y` gives a constant equivariant map. In the Cayley scenario the three natural transformations are the three left multiplications $\lambda_e, \lambda_a, \lambda_b$ of Section 2. In the diamond with $A = 0$, the element `z2` is not a restriction of anything, but it still gives a natural transformation out of $H_0$, because $H_0$ is non-empty only at the bottom element.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8. Variants, and "Follow the Identity" as a Technique

    ### The covariant form

    The lemma was stated for presheaves. Applying it to the category $\mathcal{A}^{\mathrm{op}}$ in place of $\mathcal{A}$ gives a statement about covariant functors on $\mathcal{A}$ and the covariant representables $H^A = \mathcal{A}(A, -)$.

    > **Theorem 8.1 (Yoneda lemma, covariant form).** Let $\mathcal{A}$ be a locally small category. Then for every object $A$ of $\mathcal{A}$ and every functor $X \colon \mathcal{A} \to \mathbf{Set}$,
    > $$[\mathcal{A}, \mathbf{Set}](H^A, X) \cong X(A),$$
    > naturally in $A$ and $X$, via $\alpha \mapsto \alpha_A(1_A)$.

    **Reading the statement.** A natural transformation $\alpha \colon H^A \Rightarrow X$ has components $\alpha_B \colon \mathcal{A}(A, B) \to X(B)$, with naturality equation $X(g)(\alpha_B(p)) = \alpha_C(g \circ p)$ for $g \colon B \to C$ (4A, Section 2). The element $1_A$ lies in $\mathcal{A}(A, A) = H^A(A)$, so $\alpha_A(1_A) \in X(A)$ makes sense. Writing out the inverse map and proving that the two are mutually inverse is proof brief **P03**; it is the best possible check that you have understood Section 5, so we do not spoil it here.

    Be careful with one point of variance when you use the covariant form: $H^\bullet$ is contravariant (4A, Section 3), so the left side $[\mathcal{A}, \mathbf{Set}](H^A, X)$ is *covariant* in $A$, as is the right side $X(A)$.

    ### The technique

    Strip away the notation and the proof of the Yoneda lemma has one idea, used twice (in Lemma 5.3 and again in Lemma 6.2):

    > **Follow the identity.** To learn everything about a natural transformation $\alpha$ whose domain is $H_A$ (or $H^A$), apply the naturality square at an arrow $f$ and evaluate at $1_A$. The square then says $\alpha_B(f) = X(f)(\alpha_A(1_A))$: the value of $\alpha$ at $f$ is computed from its value at the identity.

    Three situations in which to reach for it:
    1. **To show two natural transformations $\alpha, \beta \colon H_A \Rightarrow X$ are equal**, it is enough to show $\alpha_A(1_A) = \beta_A(1_A)$. This is injectivity of $\widehat{(\ )}$.
    2. **To construct a natural transformation $H_A \Rightarrow X$**, it is enough to name an element $x \in X(A)$; the transformation is $\tilde{x}$ and you never have to check naturality by hand again, because Lemma 5.1 did it once and for all.
    3. **To count natural transformations $H_A \Rightarrow X$**, count the elements of $X(A)$.

    **Example of 1.** In the monoid case: two equivariant maps $M \to S$ that agree at $1$ are equal.

    **Example of 3.** In a poset, $\mathrm{Nat}(H_a, H_b)$ has one element if $a \le b$ and none otherwise (Section 3).

    **Non-example.** None of this applies to a natural transformation whose domain is not representable. Two graph maps out of the triangle graph can agree on one vertex and differ elsewhere. Before using the technique, confirm that the domain really is a hom-functor.

    > [Leinster §4.2](https://arxiv.org/abs/1612.09375) and [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf); Riehl states the covariant form as the main theorem and the contravariant one as its dual.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Evaluating at an arrow that need not exist.** Writing "$\alpha_B(1_A)$" or "pick any $p \in \mathcal{A}(B, A)$". *Diagnosis:* $1_A$ lives in $\mathcal{A}(A, A)$ only, and $\mathcal{A}(B, A)$ may be empty. The one element you are entitled to is $1_A \in H_A(A)$, which is why the hat is defined using the component at $A$.
    2. **Defining $\tilde{x}$ and forgetting to prove it is natural.** *Diagnosis:* a family of functions is a natural transformation only after the naturality equation is verified for every arrow. Lemma 5.1 is part of the proof, and it is where functoriality of $X$ is used.
    3. **Checking only one composite.** Proving $\hat{\tilde{x}} = x$ and concluding that the maps are inverse. *Diagnosis:* one composite gives only that $\widehat{(\ )}$ is surjective. The substantial half is $\tilde{\hat{\alpha}} = \alpha$, which says a transformation is determined by its value at the identity.
    4. **Using naturality at the wrong arrow or the wrong element.** In Lemma 5.3 the naturality square is taken at $f \colon B \to A$ and evaluated at $1_A$. *Diagnosis:* state both choices explicitly, "naturality of $\alpha$ at $f$, applied to $1_A$", and check that $1_A$ lies in the top-left corner of that square.
    5. **Getting the variance of $X(f)$ backwards.** Writing $X(f) \colon X(B) \to X(A)$ for $f \colon B \to A$. *Diagnosis:* a presheaf reverses arrows, so $f \colon B \to A$ gives $X(f) \colon X(A) \to X(B)$. Write the domain and codomain of $X(f)$ next to it until this is automatic.

    ## Why This Matters

    - **4C** draws the consequences: the Yoneda embedding $H_\bullet$ is full and faithful (take $X = H_B$ in the lemma), $H_A \cong H_B$ implies $A \cong B$, and a representation of $X$ is the same thing as a *universal element* of $X$. Every one of those proofs is a few lines once the lemma is available.
    - **5A and 6A** define limits by universal properties; the uniqueness of limits up to isomorphism is the uniqueness of representing objects from 4C, and hence rests on this module.
    - **6B** proves that every presheaf is a colimit of representables. The bijection $\mathrm{Nat}(H_A, X) \cong X(A)$ is what indexes that colimit: the elements of $X$ are the maps from representables into $X$.
    - **6C** proves "right adjoints preserve limits" in one line by a Yoneda argument.
    - Outside this course, the lemma is the reason an object of any category can be studied through the maps into it, which is the starting point of the functor-of-points view in algebraic geometry.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Presheaves on a finite category are stored as in 4A: `X["objects"][A]` is the list of elements of $X(A)$, and for an arrow `f` from $A$ to $B$, `X["arrows"][f]` is a dict from $X(B)$ to $X(A)$. A natural transformation between presheaves is a dict `{B: {x: alpha_B(x), ...}, ...}`.

    ### Exercise 1: The map $x \mapsto \tilde{x}$

    Complete `yoneda_tilde(cat, X, A, x)`, which returns the natural transformation $\tilde{x} \colon H_A \Rightarrow X$ as a dict of dicts. The domain of the component at $B$ is the list of arrows $B \to A$, which is computed for you.
    """)
    return


@app.cell
def _():
    def _run():
        def yoneda_tilde(cat, X, A, x):
            _hom_into_A = {_B: [_p for _p, (_d, _c) in cat["arrows"].items() if _d == _B and _c == A]
                           for _B in cat["objects"]}
            # TODO: for each object B and each arrow p : B -> A, the value of the component at B on p
            #       (use the definition from Stage 2 of the proof)
            _tilde = {_B: {_p: ... for _p in _hom_into_A[_B]} for _B in cat["objects"]}
            return _tilde

        graph_cat = {
            "objects": ["V", "E"],
            "arrows": {"1V": ("V", "V"), "1E": ("E", "E"), "s": ("V", "E"), "t": ("V", "E")},
            "identity": {"V": "1V", "E": "1E"},
            "compose": {("1V", "1V"): "1V", ("1E", "1E"): "1E", ("s", "1V"): "s", ("1E", "s"): "s",
                        ("t", "1V"): "t", ("1E", "t"): "t"},
        }
        # Three vertices, edges a: v1->v2, b: v2->v3, c: v1->v3.
        triangle = {
            "objects": {"V": ["v1", "v2", "v3"], "E": ["a", "b", "c"]},
            "arrows": {"1V": {"v1": "v1", "v2": "v2", "v3": "v3"}, "1E": {"a": "a", "b": "b", "c": "c"},
                       "s": {"a": "v1", "b": "v2", "c": "v1"}, "t": {"a": "v2", "b": "v3", "c": "v3"}},
        }

        # print(yoneda_tilde(graph_cat, triangle, "E", "b"))
        #   expect {'V': {'s': 'v2', 't': 'v3'}, 'E': {'1E': 'b'}}
        # print(yoneda_tilde(graph_cat, triangle, "V", "v3"))
        #   expect {'V': {'1V': 'v3'}, 'E': {}}

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Cayley's theorem for a finite monoid

    A finite monoid is given by its list of elements and a multiplication function. Build the left-multiplication maps $\lambda_x$ as dicts, then test the two claims of Theorem 2.2: $x \mapsto \lambda_x$ is injective, and $\lambda_{xy} = \lambda_x \circ \lambda_y$. Then put the embedding to work: an element $x$ has a two-sided inverse exactly when $\lambda_x$ is a bijection (if $\lambda_x$ is a bijection, its inverse function is again equivariant, hence is some $\lambda_p$). Use this to list the invertible elements of the monoid $\{e, a, b\}$ and of $(\mathbb{Z}/6, \times)$.
    """)
    return


@app.cell
def _():
    def _run():
        def left_mults(elements, mul):
            # TODO: the dict  x -> lambda_x,  where lambda_x is itself the dict  p -> x*p
            return {_x: ... for _x in elements}

        def respects_composition(elements, mul, table):
            # TODO: True when  table[mul(x, y)]  equals the composite  table[x] o table[y]  for all x, y
            _result = ...
            return _result

        def is_injective(table):
            # TODO: True when different x give different dicts
            _result = ...
            return _result

        def invertible(elements, table):
            # TODO: the list of x for which the function table[x] is a bijection of `elements`
            _result = ...
            return _result

        m3 = ["e", "a", "b"]

        def mul3(x, y):         # identity e;  xy = x whenever x != e
            return y if x == "e" else x

        z6 = [0, 1, 2, 3, 4, 5]

        def mul6(x, y):         # multiplication modulo 6, identity 1
            return (x * y) % 6

        lam3 = left_mults(m3, mul3)
        lam6 = left_mults(z6, mul6)

        # print(lam3["a"])                              # expect {'e': 'a', 'a': 'a', 'b': 'a'}
        # print(is_injective(lam3))                     # expect True
        # print(respects_composition(m3, mul3, lam3))   # expect True
        # print(invertible(m3, lam3))                   # expect ['e']
        # print(lam6[2])                                # expect {0: 0, 1: 2, 2: 4, 3: 0, 4: 2, 5: 4}
        # print(is_injective(lam6))                     # expect True
        # print(invertible(z6, lam6))                   # expect [1, 5]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Check naturality in $A$ by machine

    `hom_presheaf`, `nat_transformations` and `yoneda_hat` are given. For an arrow $f \colon B \to A$ and a natural transformation $\alpha \colon H_A \Rightarrow X$, complete `precompose(cat, alpha, f)`, which returns $\alpha \circ H_f \colon H_B \Rightarrow X$ as a dict of dicts. Then verify (Y3), Lemma 6.2, in the category of graphs: for **every** $\alpha \colon H_E \Rightarrow X$ and for both $f = s$ and $f = t$, the element $\widehat{\alpha \circ H_f}$ equals $X(f)(\hat{\alpha})$.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def hom_presheaf(cat, A):
            _obj = {_B: [_p for _p, (_d, _c) in cat["arrows"].items() if _d == _B and _c == A]
                    for _B in cat["objects"]}
            _arr = {_g: {_p: cat["compose"][(_p, _g)] for _p in _obj[_c]}
                    for _g, (_d, _c) in cat["arrows"].items()}
            return {"objects": _obj, "arrows": _arr}

        def nat_transformations(cat, X, Y):
            _objs = cat["objects"]
            _choices = [list(itertools.product(Y["objects"][_B], repeat=len(X["objects"][_B]))) for _B in _objs]
            _out = []
            for _combo in itertools.product(*_choices):
                _al = {_B: dict(zip(X["objects"][_B], _vals)) for _B, _vals in zip(_objs, _combo)}
                if all(Y["arrows"][_g][_al[_c][_x]] == _al[_d][X["arrows"][_g][_x]]
                       for _g, (_d, _c) in cat["arrows"].items() for _x in X["objects"][_c]):
                    _out.append(_al)
            return _out

        def yoneda_hat(cat, A, alpha):
            return alpha[A][cat["identity"][A]]

        def precompose(cat, alpha, f):
            _B, _A = cat["arrows"][f]
            _into_B = {_C: [_q for _q, (_d, _c) in cat["arrows"].items() if _d == _C and _c == _B]
                       for _C in cat["objects"]}
            # TODO: the component at C sends an arrow q : C -> B to the value of alpha on the arrow (H_f)_C(q)
            return {_C: {_q: ... for _q in _into_B[_C]} for _C in cat["objects"]}

        graph_cat = {
            "objects": ["V", "E"],
            "arrows": {"1V": ("V", "V"), "1E": ("E", "E"), "s": ("V", "E"), "t": ("V", "E")},
            "identity": {"V": "1V", "E": "1E"},
            "compose": {("1V", "1V"): "1V", ("1E", "1E"): "1E", ("s", "1V"): "s", ("1E", "s"): "s",
                        ("t", "1V"): "t", ("1E", "t"): "t"},
        }
        # Three vertices, edges a: v1->v2, b: v2->v3, c: v1->v3.
        triangle = {
            "objects": {"V": ["v1", "v2", "v3"], "E": ["a", "b", "c"]},
            "arrows": {"1V": {"v1": "v1", "v2": "v2", "v3": "v3"}, "1E": {"a": "a", "b": "b", "c": "c"},
                       "s": {"a": "v1", "b": "v2", "c": "v1"}, "t": {"a": "v2", "b": "v3", "c": "v3"}},
        }

        alphas = nat_transformations(graph_cat, hom_presheaf(graph_cat, "E"), triangle)
        # print(len(alphas))                                              # expect 3
        # print(sorted((yoneda_hat(graph_cat, "E", _al),
        #               yoneda_hat(graph_cat, "V", precompose(graph_cat, _al, "t"))) for _al in alphas))
        #   expect [('a', 'v2'), ('b', 'v3'), ('c', 'v3')]
        # TODO: y3_ok = True when, for every al in alphas and every f in ["s", "t"], the hat (at V) of
        #       precompose(graph_cat, al, f) equals triangle["arrows"][f] applied to the hat (at E) of al
        y3_ok = ...
        # print(y3_ok)                                                    # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | Yoneda by hand in the arrow category: `exercises/4b/p01_yoneda_in_the_arrow_category.md` | warm-up | unpacking naturality in a small example |
    | P02 | Subsets as natural transformations: `exercises/4b/p02_subsets_as_natural_transformations.md` | warm-up | verifying an instance of $x \mapsto \tilde{x}$ |
    | P03 | The covariant Yoneda lemma: `exercises/4b/p03_covariant_yoneda.md` | core | follow the identity; dualizing |
    | P04 | Orbits and stabilizers: `exercises/4b/p04_orbits_and_stabilizers.md` | core | reading the lemma in a group |
    | P05 | Natural maps $B \times B \to B$: `exercises/4b/p05_natural_maps_from_the_square.md` | core | follow the generic element |
    | P06 | Natural operations on groups: `exercises/4b/p06_natural_operations_on_groups.md` | stretch | transporting the Yoneda bijection along a representation |

    **Submitting a proof.** Write your proof in `proofs/4b/pNN_<slug>.md` (the exact filename is at the bottom of each brief), then ask Claude to review it.
    The review points at gaps and asks questions; it does not hand you a model proof. Open the hints in a brief one at a time, and only after a real attempt.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [4A: Representable Functors](../4a_representables/) &nbsp;|&nbsp; Next: [4C: Consequences of Yoneda](../4c_yoneda_consequences/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
