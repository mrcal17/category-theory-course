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
    # 4C: Consequences of Yoneda

    > *An object is known by the maps into it.*
    > — the slogan of Part 4

    The Yoneda lemma of 4B says that for a presheaf $X$ on a locally small category $\mathcal{A}$,
    $$\mathrm{Nat}(H_A, X) \cong X(A) \qquad \text{naturally in } A \text{ and } X,$$
    via $\alpha \mapsto \hat{\alpha} = \alpha_A(1_A)$, with inverse $x \mapsto \tilde{x}$, $\tilde{x}_B(p) = X(p)(x)$. On its own that is a statement about one hom-set of a presheaf category. This module is about what it buys you.

    The question this module answers is: **how much does an object's hom-functor know about the object?** The answer is: everything. Three results make that precise, and each is a short deduction from the lemma.

    1. **Representations are universal elements.** A natural isomorphism $H_A \cong X$ is the same thing as one element $u \in X(A)$ with a universal property. This is how representability is used in practice.
    2. **The Yoneda embedding is full and faithful.** Natural transformations $H_A \Rightarrow H_B$ are exactly the arrows $A \to B$. So $\mathcal{A}$ sits inside $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ as a full subcategory.
    3. **$H_A \cong H_B$ implies $A \cong B$.** Two objects with the same maps into them are isomorphic. Hence representing objects are unique up to isomorphism, and it makes sense to say "the" tensor product or "the" free group.

    By the end you will be able to prove two objects isomorphic *without writing down an arrow between them*, by comparing their hom-functors. This "Yoneda-style" argument is used repeatedly in Parts 5 and 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Representations Are Universal Elements

    In 4A, a representation of a presheaf $X$ was an object $A$ with a natural isomorphism $\alpha \colon H_A \Rightarrow X$: infinitely many bijections and infinitely many equations. In both worked examples there, the proof came down to one special element (the element $\star \in 1$, the subset $\{1\} \subseteq 2$). The Yoneda lemma explains why: $\alpha$ *is* one element of $X(A)$. The only question left is which elements give isomorphisms.

    > **Definition (universal element).** Let $X$ be a presheaf on a locally small category $\mathcal{A}$. A **universal element** of $X$ is a pair $(A, u)$, where $A$ is an object of $\mathcal{A}$ and $u \in X(A)$, such that:
    >
    > for every object $B$ of $\mathcal{A}$ and every element $x \in X(B)$, there exists a unique arrow $\bar{x} \colon B \to A$ such that $X(\bar{x})(u) = x$.

    **Reading the definition.**
    - The data: one object $A$ and one element $u$ of the set $X(A)$.
    - The condition quantifies over **all** objects $B$ and **all** elements $x \in X(B)$.
    - For each such $x$ there are two things to check: *existence* of an arrow $\bar{x} \colon B \to A$ with $X(\bar{x})(u) = x$, and *uniqueness*: if $f, f' \colon B \to A$ both satisfy $X(f)(u) = x = X(f')(u)$ then $f = f'$.
    - Types: $\bar{x} \colon B \to A$ gives $X(\bar{x}) \colon X(A) \to X(B)$, since $X$ is contravariant. So $X(\bar{x})(u)$ is an element of $X(B)$, as it must be to equal $x$.
    - In words: every element of every $X(B)$ is obtained from $u$ by applying $X$ to exactly one arrow.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        nodes={
            "A": (0, 2, r"$A$"), "B": (0, 0, r"$B$"),
            "XA": (3.2, 2, r"$u \in X(A)$"), "XB": (3.2, 0, r"$x \in X(B)$"),
            "lab": (4.1, 1, r"$X(\bar{x})$"), "xbar": (-0.4, 1, r"$\bar{x}$"),
        },
        arrows=[
            ("B", "A", "", {"dashed": True}),
            ("XA", "XB", ""),
        ],
        figsize=(6.2, 3.4),
        title=r"A universal element: each $x$ equals $X(\bar{x})(u)$ for exactly one arrow $\bar{x}$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Theorem 1.1 (representations are universal elements).** Let $\mathcal{A}$ be a locally small category, $X$ a presheaf on $\mathcal{A}$ and $A$ an object of $\mathcal{A}$. For an element $u \in X(A)$, the following are equivalent:
    >
    > 1. the natural transformation $\tilde{u} \colon H_A \Rightarrow X$ is a natural isomorphism;
    > 2. $(A, u)$ is a universal element of $X$.
    >
    > Consequently the Yoneda bijection $\alpha \mapsto \alpha_A(1_A)$ restricts to a bijection between natural isomorphisms $H_A \Rightarrow X$ and elements $u \in X(A)$ such that $(A, u)$ is universal.

    - **Goal.** For a fixed $u \in X(A)$: statement 1 holds if and only if statement 2 holds. Then the final sentence.
    - **Given.** The definition $\tilde{u}_B(f) = X(f)(u)$ for $f \in \mathcal{A}(B, A)$, and the fact that $\tilde{u}$ is a natural transformation (4B, Lemma 5.1). The fact from 1D that a natural transformation is a natural isomorphism if and only if every component is an isomorphism; in $\mathbf{Set}$, an isomorphism is a bijection. The Yoneda bijection (4B, Theorem 4.1).
    - **Plan.** Unpack statement 1 until it reads the same as statement 2. A chain of "if and only if" steps, each justified, proves both directions at once.
    - **Proof.** We have
      $$\tilde{u} \text{ is a natural isomorphism}$$
      $$\iff \text{for every object } B, \text{ the function } \tilde{u}_B \colon \mathcal{A}(B, A) \to X(B) \text{ is a bijection}$$
      $$\iff \text{for every object } B \text{ and every } x \in X(B), \text{ there is exactly one } f \in \mathcal{A}(B, A) \text{ with } \tilde{u}_B(f) = x$$
      $$\iff \text{for every object } B \text{ and every } x \in X(B), \text{ there is exactly one } f \colon B \to A \text{ with } X(f)(u) = x.$$
      The first step is the fact from 1D. The second is the definition of a bijection: every element of the codomain has exactly one preimage. The third is the definition of $\tilde{u}_B$. The last line is the definition of "$(A, u)$ is a universal element".

      For the final sentence: by the Yoneda lemma every natural transformation $\alpha \colon H_A \Rightarrow X$ equals $\tilde{u}$ for exactly one $u \in X(A)$, namely $u = \alpha_A(1_A)$. By what we have just shown, $\alpha = \tilde{u}$ is an isomorphism exactly when $(A, u)$ is universal. $\blacksquare$
    - **What made it work.** The Yoneda lemma converted the transformation into an element; after that, "isomorphism" unpacked into "bijection in each component", and "bijection" unpacked into "exists unique". When a statement looks like "there exists a unique arrow such that...", suspect that it says some function between a hom-set and another set is a bijection.

    **The covariant version.** For a functor $X \colon \mathcal{A} \to \mathbf{Set}$, a universal element is a pair $(A, u)$ with $u \in X(A)$ such that for every $B$ and every $x \in X(B)$ there is a unique arrow $\bar{x} \colon A \to B$ with $X(\bar{x})(u) = x$. By the covariant Yoneda lemma (4B, Theorem 8.1) the same argument shows that these correspond to natural isomorphisms $H^A \Rightarrow X$.

    **Example (power set).** For $\mathscr{P} \colon \mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$, the pair $(2, \{1\})$ is a universal element: for every set $B$ and every subset $S \subseteq B$ there is a unique function $\chi \colon B \to 2$ with $\chi^{-1}\{1\} = S$. This is Proposition 4.1 of 4A, which now takes one sentence to state.

    **Example (groups).** For the forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ (covariant), $(\mathbb{Z}, 1)$ is a universal element: for every group $G$ and every $x \in G$ there is a unique homomorphism $\varphi \colon \mathbb{Z} \to G$ with $\varphi(1) = x$. So is $(\mathbb{Z}, -1)$. The integer $2$ does not give one: there is no homomorphism $\varphi \colon \mathbb{Z} \to \mathbb{Z}$ with $\varphi(2) = 1$, so existence fails.

    **Example (graphs).** In the category $\mathcal{G}$ with arrows $s, t \colon V \to E$ (4A), let $X$ be the graph with one edge $k$ from a vertex $x$ to a different vertex $y$. Then $(E, k)$ is a universal element. Check it: for $B = E$, the only element of $X(E)$ is $k = X(1_E)(k)$, and $1_E$ is the only arrow $E \to E$. For $B = V$, the elements of $X(V)$ are $x = X(s)(k)$ and $y = X(t)(k)$, and $s, t$ are the only arrows $V \to E$.

    **Example (the unit of an adjunction).** Let $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$, and fix $A \in \mathcal{A}$. By 4A (Lemma 6.1) the functor $\mathcal{A}(A, G(-)) \colon \mathcal{B} \to \mathbf{Set}$ is represented by $F(A)$, via $q \mapsto \bar{q}$. The corresponding universal element is the image of $1_{F(A)}$, which is the unit $\eta_A \colon A \to G(F(A))$ (2B). Universality says: for every $B \in \mathcal{B}$ and every $f \colon A \to G(B)$ there is a unique $q \colon F(A) \to B$ with $G(q) \circ \eta_A = f$. That is the universal property of the unit from 2C, recovered as a special case.

    **Example (tensor product).** A tensor product of $U$ and $V$ (4A, Section 7) is a universal element of $\mathrm{Bilin}(U, V; -)$: a vector space $U \otimes V$ and a bilinear map $\otimes \colon U \times V \to U \otimes V$ such that every bilinear map $\beta \colon U \times V \to W$ equals $\bar{\beta} \circ \otimes$ for a unique linear map $\bar{\beta} \colon U \otimes V \to W$. This is the form in which the tensor product is usually defined in algebra.

    **Non-example.** The triangle graph $T$ (three vertices, three edges) has no universal element. If $(E, u)$ were universal, the elements of $T(E)$ would correspond one-to-one with arrows $E \to E$, of which there is one; but $T$ has three edges. If $(V, u)$ were universal, the elements of $T(E)$ would correspond to arrows $E \to V$, of which there are none; but $T(E)$ is not empty. By Theorem 1.1, $T$ is not representable.

    > [Leinster §4.3](https://arxiv.org/abs/1612.09375) derives this description of representations as the first corollary of the Yoneda lemma. [Riehl §2.3](https://math.jhu.edu/~eriehl/context.pdf) calls the pair $(A, u)$ a universal element and builds the notion of universal property on it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. The Yoneda Embedding Is Full and Faithful

    In 4A the functor $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$, $A \mapsto H_A$, $f \mapsto H_f$, was called the Yoneda *embedding*, with a promise that the name would be justified. Recall from 1C what must be shown.

    > **Definition (restated from 1C).** A functor $J \colon \mathcal{A} \to \mathcal{B}$ is **faithful** (respectively **full**) if for every pair of objects $A, A'$ of $\mathcal{A}$ the function
    > $$\mathcal{A}(A, A') \to \mathcal{B}(J(A), J(A')), \qquad f \mapsto J(f),$$
    > is injective (respectively surjective).

    **Reading the definition for $J = H_\bullet$.**
    - *Faithful:* if $f, f' \colon A \to B$ and $H_f = H_{f'}$ then $f = f'$.
    - *Full:* every natural transformation $\alpha \colon H_A \Rightarrow H_B$ is equal to $H_f$ for some arrow $f \colon A \to B$.
    - Both together: $f \mapsto H_f$ is a bijection $\mathcal{A}(A, B) \to \mathrm{Nat}(H_A, H_B)$, for every $A$ and $B$.

    > **Theorem 2.1.** For every locally small category $\mathcal{A}$, the Yoneda embedding $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is full and faithful.

    - **Goal.** For all objects $A, B$ of $\mathcal{A}$, the function $\mathcal{A}(A, B) \to \mathrm{Nat}(H_A, H_B)$, $f \mapsto H_f$, is a bijection.
    - **Given.** The Yoneda lemma (4B) applied to the presheaf $X = H_B$: the function $\tilde{(\ )} \colon H_B(A) \to \mathrm{Nat}(H_A, H_B)$ is a bijection, where $\tilde{x}_C(p) = H_B(p)(x)$ for $p \in \mathcal{A}(C, A)$. The definitions $H_B(A) = \mathcal{A}(A, B)$, $H_B(p)(x) = x \circ p$ and $(H_f)_C(p) = f \circ p$ from 4A.
    - **Plan.** The domain $H_B(A)$ of the Yoneda bijection is exactly $\mathcal{A}(A, B)$. So we already have *a* bijection $\mathcal{A}(A, B) \to \mathrm{Nat}(H_A, H_B)$. Show that it is the function $f \mapsto H_f$, by computing $\tilde{f}$.
    - **Proof.** Let $f \in \mathcal{A}(A, B) = H_B(A)$. For every object $C$ and every $p \in \mathcal{A}(C, A)$,
      $$\tilde{f}_C(p) = H_B(p)(f) = f \circ p = (H_f)_C(p),$$
      by the definition of $\tilde{\ }$, the definition of $H_B$ on arrows, and the definition of $H_f$. So $\tilde{f}$ and $H_f$ have the same components, hence $\tilde{f} = H_f$. Therefore the function $f \mapsto H_f$ is equal to the function $f \mapsto \tilde{f}$, which is a bijection by the Yoneda lemma. $\blacksquare$
    - **What made it work.** Choosing the presheaf in the Yoneda lemma to be itself a representable. The lemma is about arbitrary $X$; a great many of its uses come from taking $X = H_B$.

    Unwinding the inverse: the arrow $f$ with $H_f = \alpha$ is $f = \hat{\alpha} = \alpha_A(1_A)$. **Every natural transformation between representables is "compose with $f$", and you find $f$ by following the identity.**

    **Example (monoids).** For a monoid $M$ as a one-object category, Theorem 2.1 says that the natural transformations $H_\star \Rightarrow H_\star$ are exactly the maps $H_x = \lambda_x$, left multiplication by $x$, one for each $x \in M$. That is Cayley's theorem (4B, Theorem 2.2).

    **Example (graphs).** In $\mathcal{G}$ there are exactly two arrows $V \to E$ and none $E \to V$. So there are exactly two graph maps from the one-vertex graph $H_V$ to the one-edge graph $H_E$ (onto the source, onto the target) and none from $H_E$ to $H_V$; the latter is as it should be, since the one edge would have nowhere to go.

    **Non-example (not an equivalence).** Full and faithful does not mean that every presheaf is representable. The Yoneda embedding is in general not essentially surjective: the triangle graph of Section 1, and the empty presheaf of 4A, are not isomorphic to any $H_A$. The category $\mathcal{A}$ is a *part* of its presheaf category, usually a small part.

    **The covariant embedding.** Dually, $H^\bullet \colon \mathcal{A}^{\mathrm{op}} \to [\mathcal{A}, \mathbf{Set}]$ is full and faithful: every natural transformation $H^A \Rightarrow H^{A'}$ is $H^f$ for a unique $f \colon A' \to A$. This is Theorem 2.1 applied to the category $\mathcal{A}^{\mathrm{op}}$.

    > [Leinster §4.3](https://arxiv.org/abs/1612.09375) proves this as a corollary of the Yoneda lemma. [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) proves it for both the covariant and contravariant embeddings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Isomorphic Hom-Functors, Isomorphic Objects

    A full and faithful functor cannot tell you that two objects are *equal*, but it can tell you that they are *isomorphic*. The general fact was proved in 1E (Lemma 1 there); we restate it, adding part (b), which follows at once and is justified below.

    > **Lemma 3.1 (full and faithful functors and isomorphisms; from 1E).** Let $J \colon \mathcal{A} \to \mathcal{B}$ be a full and faithful functor and let $A, A'$ be objects of $\mathcal{A}$.
    >
    > - **(a)** An arrow $f$ of $\mathcal{A}$ is an isomorphism if and only if $J(f)$ is an isomorphism of $\mathcal{B}$.
    > - **(b)** For every isomorphism $g \colon J(A) \to J(A')$ of $\mathcal{B}$ there is a unique arrow $f \colon A \to A'$ of $\mathcal{A}$ with $J(f) = g$, and $f$ is an isomorphism.
    > - **(c)** $A \cong A'$ in $\mathcal{A}$ if and only if $J(A) \cong J(A')$ in $\mathcal{B}$.

    **Reading the lemma.** One direction of (a) and of (c) holds for every functor: functors preserve isomorphisms (1C). The content is the converse, which uses both fullness (to pull an inverse back from $\mathcal{B}$ to $\mathcal{A}$) and faithfulness (to show that what you pulled back really is an inverse). In (b), existence of $f$ is fullness, uniqueness of $f$ is faithfulness, and $f$ is an isomorphism by (a). Reread the proof in 1E if the lemma is not fresh; here we only use it.

    > **Corollary 3.2.** Let $\mathcal{A}$ be a locally small category and $A, B$ objects of $\mathcal{A}$. Then
    > $$H_A \cong H_B \iff A \cong B \iff H^A \cong H^B.$$

    - **Goal.** Four implications: $A \cong B \Rightarrow H_A \cong H_B$; $H_A \cong H_B \Rightarrow A \cong B$; and the same two with upper indices.
    - **Given.** Theorem 2.1: $H_\bullet$ is full and faithful. Lemma 3.1(c). The fact that $A \cong B$ in $\mathcal{A}$ if and only if $A \cong B$ in $\mathcal{A}^{\mathrm{op}}$ (1B: an inverse pair of arrows in $\mathcal{A}$ is an inverse pair in $\mathcal{A}^{\mathrm{op}}$, with the roles swapped).
    - **Plan.** Apply Lemma 3.1(c) to $J = H_\bullet$. For the covariant statement, apply the result just proved to $\mathcal{A}^{\mathrm{op}}$.
    - **Proof.** By Theorem 2.1, $J = H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is full and faithful, so Lemma 3.1(c) gives $A \cong B$ in $\mathcal{A}$ if and only if $H_A \cong H_B$ in $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$. An isomorphism in a functor category is a natural isomorphism (1D), so this is the first equivalence.

      For the second, note that the functor $H^A = \mathcal{A}(A, -)$ on $\mathcal{A}$ is the functor $\mathcal{A}^{\mathrm{op}}(-, A)$, the contravariant representable of the category $\mathcal{A}^{\mathrm{op}}$ at $A$. Applying the first equivalence to $\mathcal{A}^{\mathrm{op}}$: $H^A \cong H^B$ if and only if $A \cong B$ in $\mathcal{A}^{\mathrm{op}}$, if and only if $A \cong B$ in $\mathcal{A}$. $\blacksquare$
    - **What made it work.** Two earlier results did all the work; the proof only had to line them up. Notice also what we did *not* do: we never constructed an arrow $A \to B$. The lemma constructs it for us. If you want to see it: given a natural isomorphism $\alpha \colon H_A \Rightarrow H_B$, the isomorphism $A \to B$ is $\alpha_A(1_A)$.

    ### Generalized elements

    Corollary 3.2 has a reading that makes it feel less abstract.

    > **Definition (generalized element).** Let $A$ be an object of a category $\mathcal{A}$. A **generalized element of $A$ of shape $C$** is an arrow $C \to A$. So $H_A(C) = \mathcal{A}(C, A)$ is the set of generalized elements of $A$ of shape $C$.

    **Reading the definition.** It is only a change of name for "arrow into $A$", but the name suggests the right examples.
    - In $\mathbf{Set}$, generalized elements of shape $1$ are ordinary elements (4A, Proposition 2.1).
    - In $\mathbf{Grp}$, generalized elements of $G$ of shape $\mathbb{Z}$ are the elements of $G$; those of shape $\mathbb{Z}/2$ are the elements $x \in G$ with $x^2 = 1$.
    - In $\mathbf{Top}$, generalized elements of shape $1$ are points; those of shape $[0, 1]$ are paths.
    - An arrow $f \colon A \to B$ turns generalized elements of $A$ into generalized elements of $B$ of the same shape, by $p \mapsto f \circ p$. That function is $(H_f)_C$.

    > **Corollary 3.3.** Let $A, B$ be objects of a locally small category $\mathcal{A}$.
    >
    > - **(a)** $A \cong B$ if and only if $\mathcal{A}(C, A) \cong \mathcal{A}(C, B)$ naturally in $C$.
    > - **(b)** An arrow $f \colon A \to B$ is an isomorphism if and only if, for every object $C$, the function $f \circ - \colon \mathcal{A}(C, A) \to \mathcal{A}(C, B)$ is a bijection.

    Part (a) is Corollary 3.2 with the definition of $H_A$ written out. Part (b) is a statement you were asked to prove by hand in 1B (proof brief P06 there), before any of this machinery existed. Look at it again now: the function $f \circ -$ is the component $(H_f)_C$, so (b) is a statement about when the natural transformation $H_f$ is an isomorphism, and you can recognise it as an instance of Lemma 3.1(a). The Yoneda embedding explains *why* your 1B proof had to work.

    So: **two objects are isomorphic exactly when they have the same generalized elements of every shape, in a way compatible with change of shape.**

    **Non-example (one shape is not enough).** The groups $\mathbb{Z}/4$ and $\mathbb{Z}/2 \times \mathbb{Z}/2$ both have four elements, so their sets of generalized elements of shape $\mathbb{Z}$ are in bijection. They are not isomorphic, and another shape detects it: there are two homomorphisms $\mathbb{Z}/2 \to \mathbb{Z}/4$ (one for each element of order dividing $2$, namely $0$ and $2$) and four homomorphisms $\mathbb{Z}/2 \to \mathbb{Z}/2 \times \mathbb{Z}/2$. Corollary 3.3 needs all shapes.

    **Non-example (naturality is needed).** A separate bijection $\mathcal{A}(C, A) \cong \mathcal{A}(C, B)$ for each $C$, with no compatibility between them, is not what Corollary 3.3(a) asks for. The hypothesis is an isomorphism *of functors* $H_A \cong H_B$; drop "naturally in $C$" and Theorem 2.1 can no longer be applied, because it is a statement about natural transformations.

    > [Leinster §4.3](https://arxiv.org/abs/1612.09375) states Lemma 3.1 and deduces Corollary 3.2; generalized elements are introduced in Leinster §4.1. [Riehl §2.2–2.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Embedding You Can Draw: A Poset and Its Down-Sets

    In a poset every hom-set has at most one element, so presheaves and natural transformations collapse to something you can picture.

    Let $P$ be a poset regarded as a category. For $a \in P$ the representable $H_a$ has $H_a(b)$ a one-element set when $b \le a$ and empty otherwise (4B, Section 3). All the information in $H_a$ is the subset of $P$ on which it is non-empty:

    > **Definition.** A **down-set** of a poset $P$ is a subset $D \subseteq P$ such that $b \in D$ and $c \le b$ imply $c \in D$. The **principal down-set** of $a \in P$ is
    > $${\downarrow} a = \{b \in P : b \le a\}.$$

    **Reading the definition.** ${\downarrow}a$ is a down-set: if $b \le a$ and $c \le b$ then $c \le a$ by transitivity. A down-set $D$ determines a presheaf $X_D$ on $P$ with $X_D(b)$ a one-element set for $b \in D$ and empty for $b \notin D$; the restriction functions are forced, and the down-set condition is exactly what makes them exist (there is no function from a non-empty set to an empty one). The representable $H_a$ is a presheaf of this kind, with $D = {\downarrow}a$.

    Between two such presheaves there is at most one natural transformation, and $X_D \Rightarrow X_{D'}$ exists exactly when $D \subseteq D'$: a component $X_D(b) \to X_{D'}(b)$ exists unless $b \in D$ and $b \notin D'$, it is unique when it exists, and the naturality equations compare elements of sets with at most one element, so they hold automatically. So this part of the presheaf category is the poset of down-sets of $P$ ordered by inclusion, and the Yoneda embedding becomes the map
    $$P \to \{\text{down-sets of } P\}, \qquad a \mapsto {\downarrow}a.$$
    Theorem 2.1 and Corollary 3.2 turn into a statement you can prove with your bare hands. Doing so is a good check on what those theorems mean.

    > **Proposition 4.1.** Let $P$ be a poset and $a, b \in P$. Then $a \le b$ if and only if ${\downarrow}a \subseteq {\downarrow}b$. Consequently ${\downarrow}a = {\downarrow}b$ implies $a = b$.

    - **Goal.** (i) If $a \le b$ then every $c \in {\downarrow}a$ lies in ${\downarrow}b$. (ii) If ${\downarrow}a \subseteq {\downarrow}b$ then $a \le b$. (iii) If ${\downarrow}a = {\downarrow}b$ then $a = b$.
    - **Given.** The definition of ${\downarrow}a$; reflexivity, transitivity and antisymmetry of $\le$.
    - **Plan.** (i) is direct. For (ii), follow the identity: the poset version of $1_a \in H_a(a)$ is the fact that $a \in {\downarrow}a$. (iii) follows from (ii) used twice.
    - **Proof.** (i) Suppose $a \le b$ and let $c \in {\downarrow}a$, so $c \le a$. By transitivity $c \le b$, so $c \in {\downarrow}b$.

      (ii) Suppose ${\downarrow}a \subseteq {\downarrow}b$. By reflexivity $a \le a$, so $a \in {\downarrow}a$. By the hypothesis $a \in {\downarrow}b$, which says $a \le b$.

      (iii) Suppose ${\downarrow}a = {\downarrow}b$. Then ${\downarrow}a \subseteq {\downarrow}b$ and ${\downarrow}b \subseteq {\downarrow}a$, so $a \le b$ and $b \le a$ by (ii), and $a = b$ by antisymmetry. $\blacksquare$
    - **What made it work.** In (ii), the single element $a \in {\downarrow}a$ carried the whole inclusion, exactly as $1_A \in H_A(A)$ carries a whole natural transformation. Part (i) is "the embedding is a functor", part (ii) is "the embedding is full" (faithfulness is automatic in a poset), and part (iii) is Corollary 3.2, where "isomorphic" in a poset means "equal".

    **Which down-sets are representable?** Exactly the principal ones; proving that a representable presheaf on a poset must look like ${\downarrow}a$ was proof brief P02 of 4A. A down-set with no greatest element, such as $\{0, a, b\}$ in the diamond, is a presheaf that is not representable. The widget lists all the down-sets of a small poset and marks the principal ones, so you can see how much room there is in the presheaf category beyond the image of $P$.
    """)
    return


@app.cell
def _(mo):
    poset_presets = {
        "Divisors of 12 under divisibility": {
            "pos": {"1": (1, 0), "2": (0.2, 1), "3": (1.8, 1), "4": (0.2, 2), "6": (1.8, 2), "12": (1, 3)},
            "covers": [("1", "2"), ("1", "3"), ("2", "4"), ("2", "6"), ("3", "6"), ("4", "12"), ("6", "12")],
        },
        "Diamond: 0 <= a, b <= 1": {
            "pos": {"0": (1, 0), "a": (0, 1), "b": (2, 1), "1": (1, 2)},
            "covers": [("0", "a"), ("0", "b"), ("a", "1"), ("b", "1")],
        },
        "Chain: 1 <= 2 <= 3 <= 4": {
            "pos": {"1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3)},
            "covers": [("1", "2"), ("2", "3"), ("3", "4")],
        },
        "No top: 0 <= a, 0 <= b": {
            "pos": {"0": (1, 0), "a": (0, 1), "b": (2, 1)},
            "covers": [("0", "a"), ("0", "b")],
        },
        "No bottom: a <= t, b <= t": {
            "pos": {"a": (0, 0), "b": (2, 0), "t": (1, 1)},
            "covers": [("a", "t"), ("b", "t")],
        },
        "Three incomparable elements": {
            "pos": {"a": (0, 0), "b": (1, 0), "c": (2, 0)},
            "covers": [],
        },
    }
    poset_choice = mo.ui.dropdown(options=list(poset_presets), value="Divisors of 12 under divisibility",
                                  label="Poset")
    mo.vstack([mo.md("**The Yoneda embedding of a finite poset: each element becomes its down-set**"), poset_choice])
    return poset_choice, poset_presets


@app.cell(hide_code=True)
def _(draw_diagram, mo, poset_choice, poset_presets):
    def _run():
        import itertools

        _p = poset_presets[poset_choice.value]
        _els = list(_p["pos"])
        # reflexive-transitive closure of the covering relation
        _leq = {(_x, _x) for _x in _els} | set(_p["covers"])
        for _k, _i, _j in itertools.product(_els, repeat=3):
            if (_i, _k) in _leq and (_k, _j) in _leq:
                _leq.add((_i, _j))

        def _show(_s):
            return "{" + ", ".join(_x for _x in _els if _x in _s) + "}" if _s else "the empty set"

        _down = {_a: frozenset(_b for _b in _els if (_b, _a) in _leq) for _a in _els}
        _agree = all(((_a, _b) in _leq) == (_down[_a] <= _down[_b]) for _a in _els for _b in _els)
        _all = []
        for _r in range(len(_els) + 1):
            for _sub in itertools.combinations(_els, _r):
                _s = frozenset(_sub)
                if all(_c in _s for _b in _s for _c in _els if (_c, _b) in _leq):
                    _all.append(_s)
        _principal = {_d: _a for _a, _d in _down.items()}

        _lines = ["| element a | its down-set (the presheaf H_a) |", "|---|---|"]
        for _a in _els:
            _lines.append(f"| `{_a}` | {_show(_down[_a])} |")
        _lines += ["", "a &#8804; b holds exactly when the down-set of a is contained in the down-set of b, "
                       "for every pair (a, b): **" + ("verified" if _agree else "FAILED") + "**.", "",
                   f"All **{len(_all)}** down-sets of this poset "
                   f"({len(_els)} of them principal, {len(_all) - len(_els)} not):", "",
                   "| down-set | representable? |", "|---|---|"]
        for _s in _all:
            _tag = f"yes, by `{_principal[_s]}`" if _s in _principal else "no"
            _lines.append(f"| {_show(_s)} | {_tag} |")

        _fig = draw_diagram(
            nodes={_x: (_xy[0] * 1.3, _xy[1] * 1.1, _x) for _x, _xy in _p["pos"].items()},
            arrows=[(_lo, _hi, "") for _lo, _hi in _p["covers"]],
            figsize=(4.2, 3.6),
            title="Hasse diagram (arrows point upward: x -> y means x <= y)",
        )
        return mo.vstack([_fig, mo.md("\n".join(_lines))])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try. In the chain, every non-empty down-set is principal: the only non-representable presheaf of this kind is the empty one. With three incomparable elements, the embedded copy of $P$ is three one-element down-sets among eight. In "no top", the whole poset $\{0, a, b\}$ is a down-set that is not principal; if you add a top element (the diamond) it becomes principal. Adding a greatest element to a down-set is what "making a presheaf representable" looks like in a poset.

    > The poset case of the Yoneda embedding is discussed in [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf); see also the remarks on ordered sets in [Leinster §4.1](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Representing Objects Are Unique, and Yoneda-Style Proofs

    In 4A the tensor product was defined as "a" representing object for bilinear maps, with the question left open of whether two representing objects must agree. Corollary 3.2 settles it.

    > **Corollary 5.1 (uniqueness of representing objects).** Let $X$ be a presheaf on a locally small category $\mathcal{A}$. If $A$ and $A'$ both represent $X$, then $A \cong A'$. The same holds for a covariant functor $X \colon \mathcal{A} \to \mathbf{Set}$.

    - **Goal.** Given natural isomorphisms $\alpha \colon H_A \Rightarrow X$ and $\alpha' \colon H_{A'} \Rightarrow X$, show that $A \cong A'$.
    - **Given.** Natural isomorphisms have inverses and compose (1D). Corollary 3.2.
    - **Plan.** Build a natural isomorphism $H_A \cong H_{A'}$ out of $\alpha$ and $\alpha'$, then apply Corollary 3.2.
    - **Proof.** The inverse $\alpha'^{-1} \colon X \Rightarrow H_{A'}$ is a natural isomorphism, so the composite $\alpha'^{-1} \circ \alpha \colon H_A \Rightarrow H_{A'}$ is a natural isomorphism. Hence $H_A \cong H_{A'}$, and by Corollary 3.2, $A \cong A'$. In the covariant case the same composite gives $H^A \cong H^{A'}$, and Corollary 3.2 again gives $A \cong A'$. $\blacksquare$
    - **What made it work.** "Represents the same functor" is a relation between hom-functors; Corollary 3.2 converts relations between hom-functors into relations between objects.

    So any two tensor products of $U$ and $V$ are isomorphic; any two objects representing "open subsets" on $\mathbf{Top}$ are homeomorphic; and so on. In fact more is true, and the stronger statement is the one used in practice:

    > **Proposition 5.2 (universal elements are unique up to unique isomorphism).** If $(A, u)$ and $(A', u')$ are universal elements of a presheaf $X$, then there is a unique arrow $j \colon A \to A'$ with $X(j)(u') = u$, and $j$ is an isomorphism.

    Not only are $A$ and $A'$ isomorphic: there is exactly one isomorphism that matches up the universal elements. Proving this is proof brief **P04**. (Compare the "unique up to unique isomorphism" arguments of 0C and 2C; this is the same shape.)

    **Example.** $(\mathbb{Z}, 1)$ and $(\mathbb{Z}, -1)$ are both universal elements of $U \colon \mathbf{Grp} \to \mathbf{Set}$. The unique compatible isomorphism between them is $n \mapsto -n$. The object is the same; the representations differ by an automorphism.

    ### The Yoneda-style proof

    Corollary 3.2 gives a method for proving that two objects are isomorphic.

    > **Recipe.** To prove $A \cong B$ in a locally small category $\mathcal{A}$, produce bijections
    > $$\mathcal{A}(C, A) \cong \mathcal{A}(C, B) \quad \text{natural in } C, \qquad \text{or} \qquad \mathcal{A}(A, C) \cong \mathcal{A}(B, C) \quad \text{natural in } C.$$
    > Usually the bijection is a chain of natural bijections that are already known (adjunctions, representations, universal properties). Then cite Corollary 3.2.

    Here is the recipe at work on a statement from Part 2. In 2C, uniqueness of adjoints was proved using initial objects of comma categories. The object-level statement has a three-line Yoneda-style proof.

    > **Proposition 5.3.** Let $G \colon \mathcal{B} \to \mathcal{A}$ be a functor between locally small categories, and suppose $F \dashv G$ and $F' \dashv G$ for two functors $F, F' \colon \mathcal{A} \to \mathcal{B}$. Then $F(A) \cong F'(A)$ for every object $A$ of $\mathcal{A}$.

    - **Goal.** For each object $A$ of $\mathcal{A}$, an isomorphism $F(A) \cong F'(A)$ in $\mathcal{B}$.
    - **Given.** 4A, Lemma 6.1, applied to each adjunction: natural isomorphisms $H^{F(A)} \cong \mathcal{A}(A, G(-))$ and $H^{F'(A)} \cong \mathcal{A}(A, G(-))$ of functors $\mathcal{B} \to \mathbf{Set}$. Corollary 5.1 in its covariant form.
    - **Plan.** Yoneda-style: both $F(A)$ and $F'(A)$ represent the same functor, so they are isomorphic.
    - **Proof.** Fix $A$. By Lemma 6.1 of 4A applied to $F \dashv G$, the object $F(A)$ represents the functor $\mathcal{A}(A, G(-)) \colon \mathcal{B} \to \mathbf{Set}$. By the same lemma applied to $F' \dashv G$, the object $F'(A)$ represents the same functor. By Corollary 5.1 (covariant form), $F(A) \cong F'(A)$. Written as a chain:
      $$\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B)) \cong \mathcal{B}(F'(A), B) \qquad \text{naturally in } B. \qquad \blacksquare$$
    - **What made it work.** The functor $\mathcal{A}(A, G(-))$ mentions only $G$. Anything that represents it is determined up to isomorphism by $G$ alone. Whenever an object is characterized by "maps out of it (or into it) correspond naturally to [something that does not mention the object]", it is unique up to isomorphism for this reason.

    (Proposition 5.3 gives an isomorphism for each $A$ separately. That these isomorphisms are natural in $A$, so that $F \cong F'$ as functors, is also true and was the content of 2C; we do not reprove it here.)

    **Non-example.** A Yoneda-style proof needs the *whole* functor. Showing that $\mathcal{A}(C_0, A) \cong \mathcal{A}(C_0, B)$ for one well-chosen $C_0$ proves nothing about $A$ and $B$ (Section 3). And the bijections must be natural in $C$: each link in your chain has to be a natural isomorphism, and you should say why each one is.

    > [Leinster §4.3](https://arxiv.org/abs/1612.09375) deduces uniqueness of representing objects and of adjoints from the Yoneda lemma in this way. [Riehl §2.3](https://math.jhu.edu/~eriehl/context.pdf) treats uniqueness of universal elements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Proving existence and stopping.** Showing that for each $x \in X(B)$ *some* arrow $\bar{x}$ has $X(\bar{x})(u) = x$, and calling $(A, u)$ universal. *Diagnosis:* that proves each $\tilde{u}_B$ is surjective. Universality needs a bijection, so uniqueness of $\bar{x}$ must be proved as well.
    2. **Dropping "naturally in $C$".** Concluding $A \cong B$ from a bijection $\mathcal{A}(C, A) \cong \mathcal{A}(C, B)$ for each $C$. *Diagnosis:* Corollary 3.2 is about an isomorphism of functors. Without naturality there is no natural transformation to feed to the Yoneda lemma.
    3. **Confusing full and faithful with injective on objects, or with an equivalence.** *Diagnosis:* Theorem 2.1 is a statement about hom-sets: $\mathcal{A}(A, B) \to \mathrm{Nat}(H_A, H_B)$ is a bijection. It does not say every presheaf is representable, and it yields $A \cong B$ (not $A = B$) from $H_A \cong H_B$.
    4. **Using Lemma 3.1 for a functor that is only full, or only faithful.** *Diagnosis:* the forgetful functor $\mathbf{Grp} \to \mathbf{Set}$ is faithful, and $\mathbb{Z}/4$ and $\mathbb{Z}/2 \times \mathbb{Z}/2$ have isomorphic images, yet they are not isomorphic. Both hypotheses are needed to reflect isomorphisms of objects.
    5. **Mixing variances in a Yoneda-style chain.** Starting with $\mathcal{A}(C, A)$ and ending with $\mathcal{A}(B, C)$. *Diagnosis:* every link of the chain must be a functor of $C$ of the same variance, so that the two ends are $H_A$ and $H_B$, or $H^A$ and $H^B$.

    ## Why This Matters

    - **5A and 5B.** Products, equalizers, pullbacks and their duals are defined by universal properties. "The limit is unique up to unique isomorphism" is Proposition 5.2 for a particular presheaf, and you will prove it there in the limit-specific form.
    - **6A** shows that a limit of a diagram is exactly a universal element of the presheaf of cones, so everything in Section 1 applies to limits at once. It also proves that representables preserve limits.
    - **6B** uses the embedding $H_\bullet$ to show that every presheaf is built from representables by a colimit.
    - **6C** proves that right adjoints preserve limits by a Yoneda-style chain of natural bijections, exactly following the recipe of Section 5.
    - The habit to take away: **to study an object, study the functor it represents.** Objects are hard to compare directly; functors into $\mathbf{Set}$ can be compared element by element.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Presheaves are stored as in 4A and 4B: `X["objects"][A]` lists the elements of $X(A)$, and for an arrow `f` from $A$ to $B$, `X["arrows"][f]` is a dict from $X(B)$ to $X(A)$.

    ### Exercise 1: Find every universal element

    Complete `universal_elements(cat, X)`, returning the list of all pairs `(A, u)` that are universal elements of the presheaf `X`. Work straight from the definition in Section 1: for every object $B$, each element of $X(B)$ must equal $X(f)(u)$ for exactly one arrow $f \colon B \to A$.
    """)
    return


@app.cell
def _():
    def _run():
        def universal_elements(cat, X):
            _found = []
            for _A in cat["objects"]:
                for _u in X["objects"][_A]:
                    # TODO: decide whether (_A, _u) is universal; if so, append it to _found.
                    #       The arrows B -> A are the names f with cat["arrows"][f] == (B, _A).
                    ...
            return _found

        graph_cat = {
            "objects": ["V", "E"],
            "arrows": {"1V": ("V", "V"), "1E": ("E", "E"), "s": ("V", "E"), "t": ("V", "E")},
            "identity": {"V": "1V", "E": "1E"},
            "compose": {("1V", "1V"): "1V", ("1E", "1E"): "1E", ("s", "1V"): "s", ("1E", "s"): "s",
                        ("t", "1V"): "t", ("1E", "t"): "t"},
        }

        def graph(vertices, edges):  # edges: {name: (source, target)}
            return {"objects": {"V": list(vertices), "E": list(edges)},
                    "arrows": {"1V": {_v: _v for _v in vertices}, "1E": {_e: _e for _e in edges},
                               "s": {_e: _st[0] for _e, _st in edges.items()},
                               "t": {_e: _st[1] for _e, _st in edges.items()}}}

        one_edge = graph(["x", "y"], {"k": ("x", "y")})
        one_loop = graph(["x"], {"k": ("x", "x")})
        triangle = graph(["v1", "v2", "v3"], {"a": ("v1", "v2"), "b": ("v2", "v3"), "c": ("v1", "v3")})

        # The group Z/3 as a one-object category, acting on {r0, r1, r2} by rotation.
        _z = ["0", "1", "2"]
        z3 = {"objects": ["*"], "arrows": {_m: ("*", "*") for _m in _z}, "identity": {"*": "0"},
              "compose": {(_g, _f): str((int(_g) + int(_f)) % 3) for _g in _z for _f in _z}}
        rotation = {"objects": {"*": ["r0", "r1", "r2"]},
                    "arrows": {_m: {f"r{_i}": f"r{(_i + int(_m)) % 3}" for _i in range(3)} for _m in _z}}

        # print(universal_elements(graph_cat, one_edge))   # expect [('E', 'k')]
        # print(universal_elements(graph_cat, one_loop))   # expect []
        # print(universal_elements(graph_cat, triangle))   # expect []
        # print(universal_elements(z3, rotation))          # expect [('*', 'r0'), ('*', 'r1'), ('*', 'r2')]
        #   Three universal elements with the same object: compare Proposition 5.2.

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Check that the Yoneda embedding is full and faithful

    Theorem 2.1 predicts that the number of natural transformations $H_A \Rightarrow H_B$ equals the number of arrows $A \to B$, for every pair of objects. `hom_presheaf` and `nat_transformations` are given. Compute both tables for the category below and compare them.
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

        # Objects A, B, C.  u : A -> B and v : B -> A are mutually inverse;  w : A -> C;  x = w o v : B -> C.
        cat = {
            "objects": ["A", "B", "C"],
            "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "1C": ("C", "C"),
                       "u": ("A", "B"), "v": ("B", "A"), "w": ("A", "C"), "x": ("B", "C")},
            "identity": {"A": "1A", "B": "1B", "C": "1C"},
            "compose": {("1A", "1A"): "1A", ("1B", "1B"): "1B", ("1C", "1C"): "1C",
                        ("u", "1A"): "u", ("1B", "u"): "u", ("v", "1B"): "v", ("1A", "v"): "v",
                        ("w", "1A"): "w", ("1C", "w"): "w", ("x", "1B"): "x", ("1C", "x"): "x",
                        ("v", "u"): "1A", ("u", "v"): "1B", ("w", "v"): "x", ("x", "u"): "w"},
        }

        # TODO: arrows_count[(P, Q)] = number of arrows P -> Q in cat
        arrows_count = {(_P, _Q): ... for _P in cat["objects"] for _Q in cat["objects"]}
        # TODO: nat_count[(P, Q)] = number of natural transformations H_P => H_Q
        nat_count = {(_P, _Q): ... for _P in cat["objects"] for _Q in cat["objects"]}

        # print(nat_count == arrows_count)                              # expect True
        # print([nat_count[(_P, "C")] for _P in cat["objects"]])        # expect [1, 1, 1]
        # print([nat_count[("C", _Q)] for _Q in cat["objects"]])        # expect [0, 0, 1]

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Detect isomorphisms through generalized elements

    Corollary 3.3(b): an arrow $f \colon A \to B$ is an isomorphism exactly when $p \mapsto f \circ p$ is a bijection $\mathcal{A}(C, A) \to \mathcal{A}(C, B)$ for every object $C$. `has_inverse` tests the definition of isomorphism directly. Complete `iso_by_elements`, which tests the criterion of the corollary, and confirm that the two agree on every arrow.
    """)
    return


@app.cell
def _():
    def _run():
        def has_inverse(cat, f):
            _A, _B = cat["arrows"][f]
            return any(_dc == (_B, _A) and cat["compose"][(_g, f)] == cat["identity"][_A]
                       and cat["compose"][(f, _g)] == cat["identity"][_B]
                       for _g, _dc in cat["arrows"].items())

        def iso_by_elements(cat, f):
            _A, _B = cat["arrows"][f]
            for _C in cat["objects"]:
                _into_A = [_p for _p, _dc in cat["arrows"].items() if _dc == (_C, _A)]
                _into_B = [_p for _p, _dc in cat["arrows"].items() if _dc == (_C, _B)]
                # TODO: return False if  p |-> f o p  is not a bijection from _into_A onto _into_B
                ...
            return True

        cat = {
            "objects": ["A", "B", "C"],
            "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "1C": ("C", "C"),
                       "u": ("A", "B"), "v": ("B", "A"), "w": ("A", "C"), "x": ("B", "C")},
            "identity": {"A": "1A", "B": "1B", "C": "1C"},
            "compose": {("1A", "1A"): "1A", ("1B", "1B"): "1B", ("1C", "1C"): "1C",
                        ("u", "1A"): "u", ("1B", "u"): "u", ("v", "1B"): "v", ("1A", "v"): "v",
                        ("w", "1A"): "w", ("1C", "w"): "w", ("x", "1B"): "x", ("1C", "x"): "x",
                        ("v", "u"): "1A", ("u", "v"): "1B", ("w", "v"): "x", ("x", "u"): "w"},
        }

        # print({_f: has_inverse(cat, _f) for _f in ["u", "v", "w", "x"]})
        #   expect {'u': True, 'v': True, 'w': False, 'x': False}
        # print({_f: iso_by_elements(cat, _f) for _f in ["u", "v", "w", "x"]})
        #   expect {'u': True, 'v': True, 'w': False, 'x': False}
        # print(all(has_inverse(cat, _f) == iso_by_elements(cat, _f) for _f in cat["arrows"]))   # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | Monics and split epics through $H_f$: `exercises/4c/p01_monics_and_split_epics_via_hom.md` | warm-up | unpacking definitions; follow the identity |
    | P02 | A universal element for vector spaces: `exercises/4c/p02_universal_element_for_vector_spaces.md` | warm-up | verifying a universal element |
    | P03 | Restricting a representable along a full and faithful functor: `exercises/4c/p03_restricting_along_full_faithful.md` | core | existence and uniqueness, transported along a functor |
    | P04 | Universal elements are unique up to unique isomorphism: `exercises/4c/p04_universal_elements_unique.md` | core | uniqueness up to unique isomorphism |
    | P05 | An exponent law by a Yoneda-style proof: `exercises/4c/p05_exponent_law_by_yoneda.md` | core | comparing hom-functors |
    | P06 | Composing with a full and faithful functor: `exercises/4c/p06_postcomposition_full_faithful.md` | stretch | building a natural transformation componentwise |

    **Submitting a proof.** Write your proof in `proofs/4c/pNN_<slug>.md` (the exact filename is at the bottom of each brief), then ask Claude to review it.
    The review points at gaps and asks questions; it does not hand you a model proof. Open the hints in a brief one at a time, and only after a real attempt.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [4B: The Yoneda Lemma](../4b_yoneda_lemma/) &nbsp;|&nbsp; Next: [5A: Limits](../5a_limits/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
