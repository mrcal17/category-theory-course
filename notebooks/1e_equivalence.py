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
    # 1E: Equivalence of Categories

    > *Two categories are "the same" when nothing you can say in the language of categories tells them apart, and that is a weaker demand than being isomorphic.*

    When are two groups "the same"? Not when they are equal, but when they are isomorphic. The lesson of 1B was that inside any category, isomorphism rather than equality is the right notion of sameness for *objects*. This module asks the same question one level up: when are two *categories* the same?

    The first guess, isomorphism of categories, turns out to be too strict. The category of finite sets has an enormous number of one-element sets, all isomorphic; a category with one object for each natural number $n$ and all functions between the sets $\{1, \dots, n\}$ contains everything a mathematician ever does with finite sets, yet the two are not isomorphic. The right notion is **equivalence**: functors in both directions whose composites are not *equal* to identity functors but *naturally isomorphic* to them. This is the first place the natural isomorphisms of 1D do real work.

    **What you will be able to prove by the end.** You will be able to show that two categories are equivalent in either of two ways: by exhibiting the functors and natural isomorphisms, or by showing that a single functor is full, faithful and essentially surjective on objects. You will see the complete proof that these two descriptions agree, including the one step where a **choice** has to be made, and you will know what a skeleton of a category is and why every category is equivalent to any of its skeletons.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Isomorphism of Categories, and Why It Is Too Strict

    Small categories and functors form a category $\mathbf{Cat}$ (1C), so the definition of isomorphism from 1B applies to categories themselves. The definition below spells this out directly in terms of functors, so it also makes sense for categories such as $\mathbf{FinSet}$ that are not small and therefore are not objects of $\mathbf{Cat}$.

    > **Definition (isomorphism of categories).** A functor $F \colon \mathcal{A} \to \mathcal{B}$ is an **isomorphism of categories** if there exists a functor $G \colon \mathcal{B} \to \mathcal{A}$ such that
    > $$G \circ F = 1_{\mathcal{A}} \qquad \text{and} \qquad F \circ G = 1_{\mathcal{B}}.$$
    > If such an $F$ exists, $\mathcal{A}$ and $\mathcal{B}$ are **isomorphic**, written $\mathcal{A} \cong \mathcal{B}$.

    **Reading the definition.** The equations are equalities of functors. So you must check:

    1. $G(F(A)) = A$ for every object $A$ of $\mathcal{A}$, and $G(F(f)) = f$ for every arrow $f$ of $\mathcal{A}$;
    2. $F(G(B)) = B$ for every object $B$ of $\mathcal{B}$, and $F(G(g)) = g$ for every arrow $g$ of $\mathcal{B}$.

    The demand "$G(F(A)) = A$" is an *equality of objects*, which is exactly the kind of statement 1B taught you to distrust.

    **Example (a group and its opposite).** Let $G$ be a group regarded as a one-object category. Define $F \colon G \to G^{\mathrm{op}}$ to be the identity on the object and $F(g) = g^{-1}$ on arrows. Composition in $G^{\mathrm{op}}$ is multiplication in the reverse order, so functoriality asks for $F(gh) = F(h)F(g)$ as a product in $G$; and $(gh)^{-1} = h^{-1}g^{-1}$. Also $F(e) = e$. The same formula defines a functor $G^{\mathrm{op}} \to G$, and the two composites are identities because $(g^{-1})^{-1} = g$. So $G \cong G^{\mathrm{op}}$.

    **Example (posets).** For posets $P$ and $Q$ regarded as categories, an isomorphism of categories $P \to Q$ is an order-preserving bijection whose inverse is also order-preserving: an isomorphism of posets.

    **Non-example (finite sets).** Let $\mathbf{FinSet}$ be the category of finite sets and functions, and let $\mathcal{N}$ be its full subcategory whose objects are the sets $[n] = \{1, 2, \dots, n\}$ for $n \geq 0$ (so $[0] = \emptyset$). Every finite set is in bijection with exactly one $[n]$, so $\mathcal{N}$ already contains "one copy of each finite set". But $\mathcal{N} \not\cong \mathbf{FinSet}$. Suppose $F \colon \mathbf{FinSet} \to \mathcal{N}$ were an isomorphism of categories with inverse $G$. The sets $\{1\}$ and $\{2\}$ are isomorphic in $\mathbf{FinSet}$, and functors preserve isomorphisms (1C), so $F(\{1\}) \cong F(\{2\})$ in $\mathcal{N}$. Two objects $[n]$ and $[m]$ of $\mathcal{N}$ are isomorphic only if $n = m$, so $F(\{1\}) = F(\{2\})$. Applying $G$ gives $\{1\} = \{2\}$, which is false.

    So isomorphism of categories distinguishes two categories that every working mathematician would treat as interchangeable. The culprit is the equality sign between functors.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (isomorphism versus equivalence); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. The Definition of Equivalence

    Functors $\mathcal{A} \to \mathcal{A}$ are objects of the functor category $[\mathcal{A}, \mathcal{A}]$, and 1D tells us what it means for two of them to be isomorphic there. Replace each "$=$" in the definition of isomorphism of categories by "$\cong$".

    > **Definition (equivalence of categories).** An **equivalence** between categories $\mathcal{A}$ and $\mathcal{B}$ consists of a pair of functors
    > $$F \colon \mathcal{A} \to \mathcal{B}, \qquad G \colon \mathcal{B} \to \mathcal{A}$$
    > together with natural isomorphisms
    > $$\eta \colon 1_{\mathcal{A}} \Rightarrow G \circ F, \qquad \varepsilon \colon F \circ G \Rightarrow 1_{\mathcal{B}}.$$
    > If an equivalence exists, $\mathcal{A}$ and $\mathcal{B}$ are **equivalent**, written $\mathcal{A} \simeq \mathcal{B}$. A functor $F$ is called **an equivalence** if there exist $G$, $\eta$ and $\varepsilon$ making $(F, G, \eta, \varepsilon)$ an equivalence.

    **Reading the definition.** To exhibit an equivalence from scratch you must supply and check:

    1. a functor $F \colon \mathcal{A} \to \mathcal{B}$ and a functor $G \colon \mathcal{B} \to \mathcal{A}$ (functoriality of each);
    2. for **every** object $A$ of $\mathcal{A}$, an isomorphism $\eta_A \colon A \to GF(A)$ in $\mathcal{A}$, such that the family is natural: $GF(f) \circ \eta_A = \eta_{A'} \circ f$ for every $f \colon A \to A'$;
    3. for **every** object $B$ of $\mathcal{B}$, an isomorphism $\varepsilon_B \colon FG(B) \to B$ in $\mathcal{B}$, such that the family is natural: $g \circ \varepsilon_B = \varepsilon_{B'} \circ FG(g)$ for every $g \colon B \to B'$.

    (By Lemma 5 of 1D, "natural isomorphism" is the same as "natural transformation whose components are isomorphisms", which is how items 2 and 3 are phrased.) The directions of $\eta$ and $\varepsilon$ are a convention chosen to match the unit and counit of an adjunction in Part 2; since both are isomorphisms, nothing depends on it.

    **Example (every isomorphism is an equivalence).** If $GF = 1_{\mathcal{A}}$ and $FG = 1_{\mathcal{B}}$, take $\eta$ and $\varepsilon$ to be identity natural transformations, which are natural isomorphisms.

    **Example (the walking isomorphism).** Let $\mathcal{I}$ be the category with two objects $a, b$ and exactly four arrows: $1_a$, $1_b$, $u \colon a \to b$ and $v \colon b \to a$, with $v \circ u = 1_a$ and $u \circ v = 1_b$. Let $\mathbf{1}$ be the category with one object $\star$ and only its identity arrow. These are not isomorphic categories (an isomorphism would give a bijection between their sets of objects). But they are equivalent:

    - $F \colon \mathcal{I} \to \mathbf{1}$ is the only functor there is; $G \colon \mathbf{1} \to \mathcal{I}$ sends $\star$ to $a$.
    - $FG = 1_{\mathbf{1}}$, so take $\varepsilon$ to be the identity.
    - $GF \colon \mathcal{I} \to \mathcal{I}$ sends both objects to $a$ and all four arrows to $1_a$. Define $\eta_a = 1_a \colon a \to a$ and $\eta_b = v \colon b \to a$. Both are isomorphisms. For naturality at an arrow $f \colon x \to y$ of $\mathcal{I}$ we need $GF(f) \circ \eta_x = \eta_y \circ f$, an equation between two arrows $x \to a$. In $\mathcal{I}$ there is exactly one arrow from any object to any object, so the two sides are equal.

    **Non-example (two points are not one point).** Let $\mathcal{D}$ be the discrete category with two objects $a \neq b$. Suppose $(F, G, \eta, \varepsilon)$ were an equivalence between $\mathcal{D}$ and $\mathbf{1}$. The component $\eta_a$ is an arrow $a \to GF(a)$ of $\mathcal{D}$; the only arrows of $\mathcal{D}$ are identities, so $GF(a) = a$, and likewise $GF(b) = b$. But $F(a) = F(b) = \star$, so $GF(a) = GF(b)$, giving $a = b$. Contradiction.

    **Non-example (a group is not a point).** Let $\mathbb{Z}/2 = \{e, t\}$ be regarded as a one-object category, with object $\star$. Suppose $(F, G, \eta, \varepsilon)$ were an equivalence between $\mathbb{Z}/2$ and $\mathbf{1}$. Then $F(t)$ is the identity arrow of $\mathbf{1}$, so $GF(t) = e$. Naturality of $\eta$ at $t$ reads $GF(t) \circ \eta_\star = \eta_\star \circ t$, that is, $\eta_\star = \eta_\star t$ in the group. Cancelling $\eta_\star$ gives $t = e$. Contradiction. Equivalence forgets how many isomorphic copies of an object there are, but it does not forget symmetries of an object.

    **Is $\simeq$ an equivalence relation?** Yes: reflexivity and symmetry are exercise P01, and transitivity is exercise P03.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (definition of equivalence); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "a": (0.0, 0.0, r"$a$"),
            "b": (2.4, 0.0, r"$b$"),
            "s": (5.4, 0.0, r"$\star$"),
        },
        [
            ("a", "b", r"$u$", {"rad": -0.35}),
            ("b", "a", r"$v$", {"rad": -0.35}),
            ("a", "a", r"$1_a$", {"loop": "left"}),
            ("b", "b", r"$1_b$", {"loop": "right"}),
            ("s", "s", r"$1_\star$", {"loop": "right"}),
        ],
        figsize=(6.8, 2.6),
        title=r"$\mathcal{I}$ (left) is equivalent, but not isomorphic, to $\mathbf{1}$ (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Full, Faithful, Essentially Surjective

    Exhibiting four pieces of data and checking two families of naturality squares is a lot of work. In practice one almost always proves that a functor is an equivalence by checking three properties of the functor alone. They were defined in 1C; here they are again with their quantifiers.

    > **Definition.** Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor. For objects $A, A'$ of $\mathcal{A}$ write $F_{A,A'} \colon \mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$ for the function $f \mapsto F(f)$.
    > - $F$ is **faithful** if for all $A, A'$ the function $F_{A,A'}$ is injective.
    > - $F$ is **full** if for all $A, A'$ the function $F_{A,A'}$ is surjective.
    > - $F$ is **essentially surjective on objects** if for every object $B$ of $\mathcal{B}$ there exist an object $A$ of $\mathcal{A}$ and an isomorphism $F(A) \cong B$ in $\mathcal{B}$.

    **Reading the definition.**

    1. *Faithful:* if $f, f' \colon A \to A'$ have the **same domain and the same codomain** and $F(f) = F(f')$, then $f = f'$. It says nothing about arrows that are not parallel.
    2. *Full:* for every arrow $g \colon F(A) \to F(A')$ of $\mathcal{B}$ **between objects in the image**, there is some $f \colon A \to A'$ with $F(f) = g$.
    3. *Full and faithful:* for every $g \colon F(A) \to F(A')$ there is a **unique** $f \colon A \to A'$ with $F(f) = g$.
    4. *Essentially surjective on objects:* every object of $\mathcal{B}$ is isomorphic (not necessarily equal) to one of the form $F(A)$.

    **Example.** The inclusion $\mathcal{N} \hookrightarrow \mathbf{FinSet}$ of Section 1 is faithful and full (the arrows $[n] \to [m]$ of $\mathcal{N}$ are, by definition of a full subcategory, all the functions $[n] \to [m]$), and essentially surjective on objects (a finite set with $n$ elements is, by definition, one in bijection with $[n]$).

    **Example.** The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ is faithful: two homomorphisms that are equal as functions are equal. **Non-example:** it is not full, since the function $\mathbb{Z}/2 \to \mathbb{Z}/2$ swapping the two elements is not a homomorphism. And non-isomorphic groups can have isomorphic images: $U(\mathbb{Z}/4) \cong U(\mathbb{Z}/2 \times \mathbb{Z}/2)$ in $\mathbf{Set}$, both having four elements. The next lemma says that this cannot happen for a functor that is full as well as faithful.

    ### Full and faithful functors reflect isomorphisms

    **Lemma 1.** Let $F \colon \mathcal{A} \to \mathcal{B}$ be a full and faithful functor.

    (a) If $f \colon A \to A'$ is an arrow of $\mathcal{A}$ and $F(f)$ is an isomorphism in $\mathcal{B}$, then $f$ is an isomorphism in $\mathcal{A}$.

    (b) If $A, A'$ are objects of $\mathcal{A}$ with $F(A) \cong F(A')$ in $\mathcal{B}$, then $A \cong A'$ in $\mathcal{A}$.

    This is the statement you proved yourself in exercise 1C·P06. Before reading on, put your own proof next to this one and compare them: where each uses fullness, where each uses faithfulness, and whether each says that the arrows being compared are parallel.

    - **Goal.** (a) Produce an arrow $g \colon A' \to A$ of $\mathcal{A}$ with $g \circ f = 1_A$ and $f \circ g = 1_{A'}$. (b) Produce an isomorphism $A \to A'$ in $\mathcal{A}$.
    - **Given.** $F$ is full: every arrow $F(X) \to F(Y)$ of $\mathcal{B}$ is $F$ of some arrow $X \to Y$. $F$ is faithful: parallel arrows of $\mathcal{A}$ with the same image under $F$ are equal. $F$ preserves composition and identities.
    - **Plan.** Use fullness to pull the inverse back from $\mathcal{B}$ to $\mathcal{A}$; use faithfulness to pull back the two equations that say it is an inverse.
    - **Proof.** (a) Let $h \colon F(A') \to F(A)$ be the inverse of $F(f)$ in $\mathcal{B}$. Since $F$ is full, there is an arrow $g \colon A' \to A$ in $\mathcal{A}$ with $F(g) = h$. Then
      $$F(g \circ f) = F(g) \circ F(f) = h \circ F(f) = 1_{F(A)} = F(1_A),$$
      by functoriality, the choice of $g$, the definition of $h$, and functoriality. The arrows $g \circ f$ and $1_A$ are both arrows $A \to A$, so they are parallel; since $F$ is faithful, $g \circ f = 1_A$. In the same way $F(f \circ g) = F(f) \circ h = 1_{F(A')} = F(1_{A'})$, and $f \circ g$, $1_{A'}$ are parallel arrows $A' \to A'$, so $f \circ g = 1_{A'}$. Hence $f$ is an isomorphism with inverse $g$.

      (b) Let $k \colon F(A) \to F(A')$ be an isomorphism in $\mathcal{B}$. Since $F$ is full there is $f \colon A \to A'$ with $F(f) = k$. By (a), $f$ is an isomorphism. $\blacksquare$
    - **What made it work.** "Full" turns arrows of $\mathcal{B}$ into arrows of $\mathcal{A}$; "faithful" turns equations in $\mathcal{B}$ into equations in $\mathcal{A}$. Every time faithfulness is used you must first say that the two arrows being compared are parallel. This two-step pattern is the engine of the main theorem below.

    > Reference: [Leinster §1.2–1.3](https://arxiv.org/abs/1612.09375); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Main Theorem, First Half: an Equivalence Is Full, Faithful and Essentially Surjective

    > **Theorem 2.** A functor $F \colon \mathcal{A} \to \mathcal{B}$ is an equivalence if and only if it is full, faithful and essentially surjective on objects.

    The two directions are quite different in character, so we prove them separately. This section proves "only if".

    **Theorem 2, "only if".** Let $(F, G, \eta, \varepsilon)$ be an equivalence between $\mathcal{A}$ and $\mathcal{B}$. Then $F$ is faithful, full and essentially surjective on objects.

    - **Goal.** (1) For all parallel $f, f' \colon A \to A'$ in $\mathcal{A}$: if $F(f) = F(f')$ then $f = f'$. (2) For every $g \colon F(A) \to F(A')$ in $\mathcal{B}$ there exists $f \colon A \to A'$ with $F(f) = g$. (3) For every object $B$ of $\mathcal{B}$ there exist an object $A$ of $\mathcal{A}$ and an isomorphism $F(A) \cong B$.
    - **Given.** Functors $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$; natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ all of whose components are isomorphisms.
    - **Plan.** The naturality square of $\eta$ at $f$ lets us *recover $f$ from $GF(f)$*, because the vertical sides are invertible. That gives faithfulness of $F$. The same argument with $\varepsilon$ gives faithfulness of $G$. Fullness of $F$ then follows by writing down the only possible candidate and using that $G$ is faithful. Essential surjectivity is read off from $\varepsilon$.
    - **Proof.**

      *Step 1: a formula for $f$.* Let $f \colon A \to A'$ be any arrow of $\mathcal{A}$. Naturality of $\eta$ at $f$ says $GF(f) \circ \eta_A = \eta_{A'} \circ f$. Composing on the left with $\eta_{A'}^{-1}$ gives
      $$f = \eta_{A'}^{-1} \circ GF(f) \circ \eta_A. \tag{$\ast$}$$

      *Step 2: $F$ is faithful.* Let $f, f' \colon A \to A'$ with $F(f) = F(f')$. Then $GF(f) = GF(f')$, so by $(\ast)$ applied to $f$ and to $f'$,
      $f = \eta_{A'}^{-1} \circ GF(f) \circ \eta_A = \eta_{A'}^{-1} \circ GF(f') \circ \eta_A = f'$.

      *Step 3: $G$ is faithful.* Let $g \colon B \to B'$ be any arrow of $\mathcal{B}$. Naturality of $\varepsilon$ at $g$ says $g \circ \varepsilon_B = \varepsilon_{B'} \circ FG(g)$; composing on the right with $\varepsilon_B^{-1}$ gives $g = \varepsilon_{B'} \circ FG(g) \circ \varepsilon_B^{-1}$. So if $g, g' \colon B \to B'$ satisfy $G(g) = G(g')$, then $FG(g) = FG(g')$ and therefore $g = g'$.

      *Step 4: $F$ is full.* Let $g \colon F(A) \to F(A')$ be an arrow of $\mathcal{B}$. Define
      $$f = \eta_{A'}^{-1} \circ G(g) \circ \eta_A \colon A \to A'.$$
      (Check the types: $\eta_A \colon A \to GF(A)$, then $G(g) \colon GF(A) \to GF(A')$, then $\eta_{A'}^{-1} \colon GF(A') \to A'$.) By $(\ast)$ we also have $f = \eta_{A'}^{-1} \circ GF(f) \circ \eta_A$. So
      $$\eta_{A'}^{-1} \circ G(g) \circ \eta_A = \eta_{A'}^{-1} \circ GF(f) \circ \eta_A.$$
      Composing on the left with $\eta_{A'}$ and on the right with $\eta_A^{-1}$ gives $G(g) = G(F(f))$. The arrows $g$ and $F(f)$ are parallel, both $F(A) \to F(A')$, and $G$ is faithful by Step 3. Hence $g = F(f)$.

      *Step 5: $F$ is essentially surjective on objects.* Let $B$ be an object of $\mathcal{B}$. Put $A = G(B)$. Then $\varepsilon_B \colon F(A) = FG(B) \to B$ is an isomorphism. $\blacksquare$
    - **What made it work.** A naturality square with invertible vertical sides can be solved for the top edge: equation $(\ast)$. That is why a natural *isomorphism* $1 \cong GF$ is so much stronger than a mere natural transformation. Notice also what was *not* used: no relation between $\eta$ and $\varepsilon$, and no choices.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "tl": (0.0, 1.7, r"$A$"),
            "tr": (3.2, 1.7, r"$A'$"),
            "bl": (0.0, 0.0, r"$GF(A)$"),
            "br": (3.2, 0.0, r"$GF(A')$"),
            # unlabelled anchor points, so that horizontal arrows clear the wide node labels
            "tl+": (0.4, 1.7, ""),
            "tr-": (2.8000000000000003, 1.7, ""),
            "bl+": (0.4, 0.0, ""),
            "br-": (2.8000000000000003, 0.0, ""),
        },
        [
            ("tl+", "tr-", r"$f$", {"side": -1}),
            ("tl", "bl", r"$\quad\eta_A$"),
            ("tr", "br", r"$\quad\eta_{A'}$"),
            ("bl+", "br-", r"$GF(f)$"),
        ],
        figsize=(5.2, 3.2),
        title=r"$\eta_A$, $\eta_{A'}$ invertible: $f$ is determined by $GF(f)$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The Main Theorem, Second Half: Building the Inverse, and Where a Choice Is Made

    Now the converse. We are given only the functor $F$ and three properties of it, and we must *construct* a functor $G$ in the other direction together with $\eta$ and $\varepsilon$. This is the longest proof so far in the course. Its length comes from the number of things that have to be checked, not from any single hard step, and every step is one of the two moves from Lemma 1: "by fullness, there is an arrow", "by faithfulness, these parallel arrows are equal".

    **Theorem 2, "if".** Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor that is full, faithful and essentially surjective on objects. Then there exist a functor $G \colon \mathcal{B} \to \mathcal{A}$ and natural isomorphisms $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$.

    - **Goal.** Construct: (1) $G$ on objects and the components $\varepsilon_B$; (2) $G$ on arrows; then prove (3) $G$ is a functor; (4) $\varepsilon$ is a natural isomorphism; then construct (5) the components $\eta_A$ and prove (6) $\eta$ is a natural isomorphism.
    - **Given.** For all objects $X, Y$ of $\mathcal{A}$ and every arrow $k \colon F(X) \to F(Y)$ of $\mathcal{B}$ there is a **unique** arrow $h \colon X \to Y$ of $\mathcal{A}$ with $F(h) = k$ (full and faithful). For every object $B$ of $\mathcal{B}$ there exist an object $A$ of $\mathcal{A}$ and an isomorphism $F(A) \to B$ (essentially surjective).
    - **Plan.** Essential surjectivity tells us where $G$ should send each object and hands us $\varepsilon$ at the same time. After that, everything else is forced: $G$ on arrows is the unique thing making $\varepsilon$ natural, and $\eta$ is the unique thing that $F$ sends to $\varepsilon^{-1}$.
    - **Proof.**

      *Step 1: $G$ on objects, and $\varepsilon$.* For each object $B$ of $\mathcal{B}$, the collection of pairs $(A, e)$ with $A$ an object of $\mathcal{A}$ and $e \colon F(A) \to B$ an isomorphism is non-empty, by essential surjectivity. **Choose one such pair for each $B$**, and call it $(G(B), \varepsilon_B)$. So $\varepsilon_B \colon FG(B) \to B$ is an isomorphism.

      > **This is where a choice is made.** Nothing singles out one pair $(A, e)$ among the possibly many that exist, and we choose one for *every* object $B$ of $\mathcal{B}$ simultaneously. Making infinitely many arbitrary choices at once is exactly what the **axiom of choice** licenses. It is the only step of the proof that uses it. If you happen to have a rule that specifies $G(B)$ and $\varepsilon_B$ for each $B$, no appeal to the axiom is needed.

      *Step 2: $G$ on arrows.* Let $g \colon B \to B'$ be an arrow of $\mathcal{B}$. The composite $\varepsilon_{B'}^{-1} \circ g \circ \varepsilon_B$ is an arrow $FG(B) \to FG(B')$. Since $F$ is full and faithful, there is a unique arrow $G(g) \colon G(B) \to G(B')$ of $\mathcal{A}$ with
      $$F(G(g)) = \varepsilon_{B'}^{-1} \circ g \circ \varepsilon_B. \tag{$\dagger$}$$
      No choice is involved here: uniqueness means $G(g)$ is determined.

      *Step 3: $G$ is a functor.* *Identities.* For an object $B$, $(\dagger)$ gives $F(G(1_B)) = \varepsilon_B^{-1} \circ 1_B \circ \varepsilon_B = 1_{FG(B)} = F(1_{G(B)})$. The arrows $G(1_B)$ and $1_{G(B)}$ are parallel, both $G(B) \to G(B)$, so by faithfulness $G(1_B) = 1_{G(B)}$. *Composition.* For $g \colon B \to B'$ and $g' \colon B' \to B''$,
      $$F\big(G(g') \circ G(g)\big) = FG(g') \circ FG(g) = \varepsilon_{B''}^{-1} \circ g' \circ \varepsilon_{B'} \circ \varepsilon_{B'}^{-1} \circ g \circ \varepsilon_B = \varepsilon_{B''}^{-1} \circ (g' \circ g) \circ \varepsilon_B = F\big(G(g' \circ g)\big),$$
      by functoriality of $F$, then $(\dagger)$ twice, then cancelling $\varepsilon_{B'} \circ \varepsilon_{B'}^{-1}$, then $(\dagger)$ for $g' \circ g$. The arrows $G(g') \circ G(g)$ and $G(g' \circ g)$ are parallel, both $G(B) \to G(B'')$, so by faithfulness they are equal.

      *Step 4: $\varepsilon$ is a natural isomorphism $FG \Rightarrow 1_{\mathcal{B}}$.* Each $\varepsilon_B$ is an isomorphism by Step 1. For naturality, let $g \colon B \to B'$. Composing $(\dagger)$ on the left with $\varepsilon_{B'}$ gives $\varepsilon_{B'} \circ FG(g) = g \circ \varepsilon_B$, which is the naturality square of $\varepsilon$ at $g$ (first diagram below). By Lemma 5 of 1D, a natural transformation whose components are isomorphisms is a natural isomorphism.

      *Step 5: the components of $\eta$.* Let $A$ be an object of $\mathcal{A}$. The arrow $\varepsilon_{F(A)} \colon FGF(A) \to F(A)$ is an isomorphism, so $\varepsilon_{F(A)}^{-1}$ is an arrow $F(A) \to F(GF(A))$. Since $F$ is full and faithful there is a unique arrow $\eta_A \colon A \to GF(A)$ of $\mathcal{A}$ with
      $$F(\eta_A) = \varepsilon_{F(A)}^{-1}. \tag{$\ddagger$}$$
      Since $F(\eta_A)$ is an isomorphism, Lemma 1(a) shows that $\eta_A$ is an isomorphism.

      *Step 6: $\eta$ is natural.* Let $f \colon A \to A'$ be an arrow of $\mathcal{A}$. We must show $GF(f) \circ \eta_A = \eta_{A'} \circ f$. Both sides are arrows $A \to GF(A')$, so they are parallel, and by faithfulness it is enough to show that $F$ sends them to the same arrow. Apply naturality of $\varepsilon$ (Step 4) at the arrow $F(f) \colon F(A) \to F(A')$ of $\mathcal{B}$:
      $$\varepsilon_{F(A')} \circ FGF(f) = F(f) \circ \varepsilon_{F(A)}.$$
      Composing on the left with $\varepsilon_{F(A')}^{-1}$ and on the right with $\varepsilon_{F(A)}^{-1}$ gives
      $$FGF(f) \circ \varepsilon_{F(A)}^{-1} = \varepsilon_{F(A')}^{-1} \circ F(f).$$
      By $(\ddagger)$ and functoriality of $F$, the left side is $F(GF(f)) \circ F(\eta_A) = F\big(GF(f) \circ \eta_A\big)$ and the right side is $F(\eta_{A'}) \circ F(f) = F\big(\eta_{A'} \circ f\big)$. So $F$ takes the same value on the two parallel arrows, and they are equal. Thus $\eta$ is a natural transformation whose components are isomorphisms, hence a natural isomorphism. $\blacksquare$
    - **What made it work.** One arbitrary choice (Step 1), after which a full and faithful functor leaves no freedom: each remaining piece of data is *defined* by the equation it must satisfy after applying $F$, and each remaining equation is *proved* by applying $F$ and using faithfulness. When you meet a full and faithful functor, expect to define things by "the unique arrow whose image is ..." and to prove equations by "apply $F$".

    **About the choice.** It is tempting to think a cleverer proof would avoid it. It is known that in general it cannot be avoided: the statement "every full, faithful and essentially surjective functor is an equivalence" needs the axiom of choice. The first half of the theorem (Section 4) uses no choice at all. This is the first proof in the course where the axiom of choice appears, and good practice is what we did above: say exactly which step uses it and why.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "tl": (0.0, 1.7, r"$FG(B)$"),
            "tr": (3.2, 1.7, r"$FG(B')$"),
            "bl": (0.0, 0.0, r"$B$"),
            "br": (3.2, 0.0, r"$B'$"),
            # unlabelled anchor points, so that horizontal arrows clear the wide node labels
            "tl+": (0.42, 1.7, ""),
            "tr-": (2.7800000000000002, 1.7, ""),
            "bl+": (0.42, 0.0, ""),
            "br-": (2.7800000000000002, 0.0, ""),
        },
        [
            ("tl+", "tr-", r"$F(G(g))$", {"side": -1, "dashed": True}),
            ("tl", "bl", r"$\quad\varepsilon_B$"),
            ("tr", "br", r"$\quad\varepsilon_{B'}$"),
            ("bl+", "br-", r"$g$"),
        ],
        figsize=(5.2, 3.2),
        title=r"Step 2: $G(g)$ is defined by this square",
    )
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "tl": (0.0, 1.7, r"$F(A)$"),
            "tr": (3.8, 1.7, r"$F(A')$"),
            "bl": (0.0, 0.0, r"$FGF(A)$"),
            "br": (3.8, 0.0, r"$FGF(A')$"),
            # unlabelled anchor points, so that horizontal arrows clear the wide node labels
            "tl+": (0.5, 1.7, ""),
            "tr-": (3.3, 1.7, ""),
            "bl+": (0.5, 0.0, ""),
            "br-": (3.3, 0.0, ""),
        },
        [
            ("tl+", "tr-", r"$F(f)$", {"side": -1}),
            ("tl", "bl", r"$\qquad\qquad F(\eta_A)$"),
            ("tr", "br", r"$\qquad\qquadF(\eta_{A'})$"),
            ("bl+", "br-", r"$FGF(f)$"),
        ],
        figsize=(6.0, 3.2),
        title=r"Step 6: $F$ applied to the naturality square of $\eta$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Using the theorem.**

    **Example (finite sets).** The inclusion $\mathcal{N} \hookrightarrow \mathbf{FinSet}$ is full, faithful and essentially surjective on objects (Section 3). By Theorem 2 it is an equivalence: $\mathcal{N} \simeq \mathbf{FinSet}$, although $\mathcal{N} \not\cong \mathbf{FinSet}$ (Section 1). Look at what Step 1 of the proof asks for here: for each finite set $B$, an object $[n]$ and a bijection $\varepsilon_B \colon [n] \to B$. The number $n$ is determined by $B$, but the bijection is not: it is an enumeration of the elements of $B$, and a set with $n$ elements has $n!$ of them, none preferred.

    **Example (matrices).** Fix a field $k$. Let $\mathbf{Mat}_k$ be the category whose objects are the natural numbers $0, 1, 2, \dots$, in which an arrow $n \to m$ is an $m \times n$ matrix over $k$, composition is matrix multiplication, and the identity on $n$ is the identity matrix $I_n$. (There is exactly one $m \times n$ matrix when $m = 0$ or $n = 0$, the empty one.) There is a functor
    $$\Phi \colon \mathbf{Mat}_k \to \mathbf{FDVect}_k, \qquad n \mapsto k^n, \qquad M \mapsto (x \mapsto Mx).$$
    This functor is an equivalence, which is the precise form of the statement that "linear algebra is the same as matrix algebra". Proving it is exercise P04. Notice that $\mathbf{Mat}_k$ is not a subcategory of $\mathbf{FDVect}_k$: a number is not a vector space.

    **Non-example.** The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ is not an equivalence, because it is not full (Section 3). The theorem is an "if and only if", so failing any one of the three properties rules a functor out.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (the theorem is stated there); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf) (a full proof, with the role of the axiom of choice made explicit).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Skeletons

    Equivalence ignores how many isomorphic copies of each object a category has. So we can ask for the most economical category equivalent to a given one: keep one object from each isomorphism class and throw the rest away, but keep all the arrows between the objects that remain.

    > **Definition (skeletal category, skeleton).** A category is **skeletal** if any two isomorphic objects in it are equal. A **skeleton** of a category $\mathcal{A}$ is a full subcategory $\mathcal{S}$ of $\mathcal{A}$ such that every object of $\mathcal{A}$ is isomorphic to **exactly one** object of $\mathcal{S}$.

    **Reading the definition.** To check that $\mathcal{S}$ is a skeleton of $\mathcal{A}$:

    1. $\mathcal{S}$ is a **full** subcategory: for objects $S, S'$ of $\mathcal{S}$, $\mathcal{S}(S, S') = \mathcal{A}(S, S')$. Nothing is removed except objects (and the arrows into or out of removed objects).
    2. *At least one:* every object $A$ of $\mathcal{A}$ is isomorphic in $\mathcal{A}$ to some object of $\mathcal{S}$.
    3. *At most one:* if $S, S'$ are objects of $\mathcal{S}$ and $S \cong S'$ in $\mathcal{A}$, then $S = S'$.

    **Example.** $\mathcal{N}$ is a skeleton of $\mathbf{FinSet}$: it is a full subcategory, every finite set is in bijection with some $[n]$, and $[n] \cong [m]$ only when $n = m$.

    **Example.** A poset regarded as a category is skeletal: if $p \cong q$ then there are arrows $p \to q$ and $q \to p$, so $p \leq q$ and $q \leq p$, so $p = q$ by antisymmetry. A group regarded as a one-object category is skeletal because it has only one object.

    **Non-example.** The walking isomorphism $\mathcal{I}$ of Section 2 is not skeletal: $a \cong b$ but $a \neq b$. It has two skeletons, the full subcategory on $\{a\}$ and the full subcategory on $\{b\}$. A category usually has many skeletons, so one says "a skeleton", not "the skeleton".

    **Proposition 3.** Let $\mathcal{S}$ be a skeleton of $\mathcal{A}$. Then the inclusion functor $J \colon \mathcal{S} \to \mathcal{A}$ is an equivalence. In particular $\mathcal{S} \simeq \mathcal{A}$.

    - **Goal.** $J$ is faithful, full and essentially surjective on objects; then Theorem 2 applies.
    - **Given.** $J(S) = S$ and $J(f) = f$. For objects $S, S'$ of $\mathcal{S}$: $\mathcal{S}(S, S') = \mathcal{A}(S, S')$. Every object of $\mathcal{A}$ is isomorphic to an object of $\mathcal{S}$.
    - **Plan.** Check the three properties directly from the definition of a skeleton.
    - **Proof.** For objects $S, S'$ of $\mathcal{S}$, the function $J_{S,S'} \colon \mathcal{S}(S, S') \to \mathcal{A}(S, S')$ is $f \mapsto f$, the identity function of the set $\mathcal{S}(S, S') = \mathcal{A}(S, S')$. It is a bijection, so $J$ is full and faithful. If $A$ is an object of $\mathcal{A}$ then, by the definition of a skeleton, there is an object $S$ of $\mathcal{S}$ with $A \cong S = J(S)$; so $J$ is essentially surjective on objects. By Theorem 2, $J$ is an equivalence. $\blacksquare$
    - **What made it work.** The theorem of Sections 4 and 5 converts "is an equivalence", which asks for a great deal of data, into three properties that can be checked by inspection. Note that only "at least one" was needed here; "at most one" is what makes the skeleton as small as possible.

    Two remarks on choice. Proposition 3 uses Theorem 2 and therefore the axiom of choice: the inverse equivalence $\mathcal{A} \to \mathcal{S}$ must choose, for each object $A$, an isomorphism from $A$ to its representative. And to show that a given category *has* a skeleton one must choose one object from each isomorphism class, which in general is again an application of the axiom of choice.

    ### Explore: build a skeleton

    Pick a finite category. The cell below computes the isomorphism classes of its objects, picks a representative from each, and forms the full subcategory on the representatives. Change which representative is picked and watch what stays the same.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sk_category = mo.ui.dropdown(
        options=[
            "walking isomorphism",
            "a preorder on six points",
            "five small sets and all functions",
            "the group Z/3 (one object)",
        ],
        value="five small sets and all functions",
        label="category",
    )
    sk_pick = mo.ui.radio(
        options=["first object of each class", "last object of each class"],
        value="first object of each class",
        label="representative",
    )
    mo.hstack([sk_category, sk_pick], justify="start", gap=2)
    return sk_category, sk_pick


@app.cell(hide_code=True)
def _(mo, sk_category, sk_pick):
    def _run():
        import itertools

        def _preorder_cat(objects, pairs):
            _leq = {(_x, _x) for _x in objects} | set(pairs)
            _changed = True
            while _changed:
                _changed = False
                for (_a, _b), (_c, _d) in itertools.product(list(_leq), repeat=2):
                    if _b == _c and (_a, _d) not in _leq:
                        _leq.add((_a, _d))
                        _changed = True
            return {
                "objects": list(objects),
                "arrows": {_x + "<=" + _y: (_x, _y) for (_x, _y) in sorted(_leq)},
                "identity": {_x: _x + "<=" + _x for _x in objects},
                "compose": {
                    (_y + "<=" + _z, _x + "<=" + _y): _x + "<=" + _z
                    for (_x, _y) in _leq for (_y2, _z) in _leq if _y == _y2
                },
            }

        def _set_cat(sets):
            # full subcategory of Set on the given named finite sets
            _arrows, _table = {}, {}
            for _X, _xs in sets.items():
                for _Y, _ys in sets.items():
                    for _images in itertools.product(_ys, repeat=len(_xs)):
                        _n = _X + "->" + _Y + ":" + "".join(_images)
                        _arrows[_n] = (_X, _Y)
                        _table[_n] = dict(zip(_xs, _images))
            _lookup = {(_arrows[_n], tuple(sorted(_t.items()))): _n for _n, _t in _table.items()}
            _compose = {}
            for _f, (_X, _Y) in _arrows.items():
                for _g, (_Y2, _Z) in _arrows.items():
                    if _Y == _Y2:
                        _c = {_x: _table[_g][_table[_f][_x]] for _x in sets[_X]}
                        _compose[(_g, _f)] = _lookup[((_X, _Z), tuple(sorted(_c.items())))]
            _identity = {_X: _lookup[((_X, _X), tuple(sorted((_x, _x) for _x in _xs)))] for _X, _xs in sets.items()}
            return {"objects": list(sets), "arrows": _arrows, "identity": _identity, "compose": _compose}

        if sk_category.value == "walking isomorphism":
            _cat = _preorder_cat(["a", "b"], [("a", "b"), ("b", "a")])
        elif sk_category.value == "a preorder on six points":
            _cat = _preorder_cat(
                ["a", "b", "c", "d", "e", "f"],
                [("a", "b"), ("b", "a"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "c"), ("a", "f")],
            )
        elif sk_category.value == "five small sets and all functions":
            _cat = _set_cat({"{}": (), "{0}": ("0",), "{1}": ("1",), "{0,1}": ("0", "1"), "{p,q}": ("p", "q")})
        else:
            _cat = {
                "objects": ["*"],
                "arrows": {"0": ("*", "*"), "1": ("*", "*"), "2": ("*", "*")},
                "identity": {"*": "0"},
                "compose": {(str(_g), str(_f)): str((_g + _f) % 3) for _g in range(3) for _f in range(3)},
            }

        def _is_iso(f):
            _X, _Y = _cat["arrows"][f]
            return any(
                _d == _Y and _c == _X
                and _cat["compose"][(_g, f)] == _cat["identity"][_X]
                and _cat["compose"][(f, _g)] == _cat["identity"][_Y]
                for _g, (_d, _c) in _cat["arrows"].items()
            )

        def _isomorphic(X, Y):
            return any(_d == X and _c == Y and _is_iso(_f) for _f, (_d, _c) in _cat["arrows"].items())

        _classes = []
        for _X in _cat["objects"]:
            for _cls in _classes:
                if _isomorphic(_cls[0], _X):
                    _cls.append(_X)
                    break
            else:
                _classes.append([_X])
        _index = 0 if sk_pick.value.startswith("first") else -1
        _reps = [_cls[_index] for _cls in _classes]

        def _hom(X, Y):
            return sum(1 for (_d, _c) in _cat["arrows"].values() if _d == X and _c == Y)

        _kept = sum(1 for (_d, _c) in _cat["arrows"].values() if _d in _reps and _c in _reps)
        _lines = [
            "| isomorphism class | chosen representative |",
            "|---|---|",
        ]
        for _cls, _r in zip(_classes, _reps):
            _lines.append("| " + ", ".join("`" + _o + "`" for _o in _cls) + " | `" + _r + "` |")
        _lines += [
            "",
            "| | objects | arrows |",
            "|---|---|---|",
            "| original category | " + str(len(_cat["objects"])) + " | " + str(len(_cat["arrows"])) + " |",
            "| skeleton | " + str(len(_reps)) + " | " + str(_kept) + " |",
            "",
            "**Number of arrows between representatives** (row = domain, column = codomain):",
            "",
            "| | " + " | ".join("`" + _r + "`" for _r in _reps) + " |",
            "|---|" + "---|" * len(_reps),
        ]
        for _r in _reps:
            _lines.append("| `" + _r + "` | " + " | ".join(str(_hom(_r, _s)) for _s in _reps) + " |")
        _lines.append("")
        if len(_reps) == len(_cat["objects"]):
            _lines.append("Every isomorphism class has one member: this category is already **skeletal**, and it is its own skeleton.")
        else:
            _lines.append("The category is **not skeletal**. The skeleton is the full subcategory on the chosen representatives; by Proposition 3 its inclusion is an equivalence.")
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Things to notice.**

    - Switch the representative between "first" and "last". The objects of the skeleton change, but the table of arrow counts does not. Different skeletons of the same category look alike; in fact any two are isomorphic as categories, which is a consequence of exercise P06.
    - In "five small sets", the skeleton has one set of each size $0, 1, 2$, and the count of arrows from a set of size $m$ to a set of size $n$ is $n^m$ (with $0^0 = 1$). This is a small piece of $\mathcal{N}$.
    - The group $\mathbb{Z}/3$ is already skeletal and none of its three arrows is discarded. A skeleton removes redundant *objects*, never arrows between the objects that remain.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (examples of equivalences); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf) (skeletons).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Duality as Equivalence with an Opposite

    Many of the famous "dualities" of mathematics are statements of one shape: a category of algebraic objects is equivalent to the *opposite* of a category of geometric ones, so that maps one way on one side are maps the other way on the other.

    > **Definition (dual equivalence).** Categories $\mathcal{A}$ and $\mathcal{B}$ are **dually equivalent** if $\mathcal{A}^{\mathrm{op}} \simeq \mathcal{B}$. A **duality** between $\mathcal{A}$ and $\mathcal{B}$ is an equivalence between $\mathcal{A}^{\mathrm{op}}$ and $\mathcal{B}$.

    **Reading the definition.** A functor $\mathcal{A}^{\mathrm{op}} \to \mathcal{B}$ is the same thing as a contravariant functor from $\mathcal{A}$ to $\mathcal{B}$ (1C). So, by Theorem 2, to establish a duality you can exhibit a contravariant functor $D$ from $\mathcal{A}$ to $\mathcal{B}$ and check:

    1. *faithful:* parallel arrows $f, f' \colon A \to A'$ with $D(f) = D(f')$ are equal;
    2. *full:* every arrow $D(A') \to D(A)$ of $\mathcal{B}$ is $D(f)$ for some $f \colon A \to A'$ (note the reversal);
    3. *essentially surjective on objects:* every object of $\mathcal{B}$ is isomorphic to some $D(A)$.

    **Example (subsets and complements).** Let $S$ be a set and $\mathcal{P}(S)$ the poset of subsets of $S$ under $\subseteq$, regarded as a category. Complementation $X \mapsto S \setminus X$ reverses inclusions: $X \subseteq Y$ if and only if $S \setminus Y \subseteq S \setminus X$. So it is a functor $\mathcal{P}(S)^{\mathrm{op}} \to \mathcal{P}(S)$, and it is its own inverse because $S \setminus (S \setminus X) = X$. Hence $\mathcal{P}(S)^{\mathrm{op}} \cong \mathcal{P}(S)$: an isomorphism of categories, and in particular a duality of $\mathcal{P}(S)$ with itself. This is why every statement about unions and inclusions of subsets has a mirror-image statement about intersections and reverse inclusions.

    **Example (finite-dimensional vector spaces).** The dual-space functor $D = (-)^*$ is a contravariant functor from $\mathbf{FDVect}_k$ to itself, that is, a functor $\mathbf{FDVect}_k^{\mathrm{op}} \to \mathbf{FDVect}_k$. Doing it twice gives the double dual, and in 1D you saw that $\mathrm{ev} \colon 1 \Rightarrow (-)^{**}$ is a natural isomorphism on $\mathbf{FDVect}_k$. The components of that natural isomorphism and their inverses supply both $\eta$ and $\varepsilon$ of an equivalence in which $F$ and $G$ are both "take the dual" (one regarded as a functor $\mathbf{FDVect}_k^{\mathrm{op}} \to \mathbf{FDVect}_k$, the other as a functor $\mathbf{FDVect}_k \to \mathbf{FDVect}_k^{\mathrm{op}}$). So
    $$\mathbf{FDVect}_k^{\mathrm{op}} \simeq \mathbf{FDVect}_k.$$
    In matrix terms the duality is the transpose: a linear map with matrix $M$ has dual with matrix $M^{\mathsf T}$, and $(MN)^{\mathsf T} = N^{\mathsf T} M^{\mathsf T}$ is contravariance. The restriction to finite dimensions is essential: for infinite-dimensional $V$ the map $\mathrm{ev}_V$ is not surjective.

    **Further examples (stated without proof, for orientation only).** The opposite of the category of finite sets is equivalent to the category of finite Boolean algebras, via the power set. Stone duality, Gelfand duality and Pontryagin duality are theorems of the same form in topology, analysis and the theory of abelian groups. You do not need any of them for this course.

    **Non-example.** A category need not be equivalent to its own opposite. $\mathbf{Set}$ is not equivalent to $\mathbf{Set}^{\mathrm{op}}$. One way to see the asymmetry of $\mathbf{Set}$: every function *into* the empty set is a bijection (its domain must be empty), whereas functions *out of* the one-element set are far from being bijections. Turning this observation into a proof needs the notions of initial and terminal object, which arrive in 2A, together with the fact that equivalences preserve them.

    **What survives an equivalence.** A property of a category that is stated purely in terms of objects, arrows, composition and identities, and that does not mention equality of objects, is preserved by equivalences. Exercise P05 is one instance (monomorphisms). The number of objects is *not* such a property, as $\mathcal{I} \simeq \mathbf{1}$ shows.

    > Reference: [Leinster §1.3](https://arxiv.org/abs/1612.09375) (dualities as equivalences $\mathcal{A}^{\mathrm{op}} \simeq \mathcal{B}$); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Using faithfulness on arrows that are not parallel.** "$F(f) = F(f')$, so $f = f'$" is valid only after you have said that $f$ and $f'$ have the same domain and the same codomain. Every use of faithfulness in Sections 3 to 5 is preceded by that sentence.
    2. **Reading "essentially surjective" as "surjective on objects".** The definition gives an isomorphism $F(A) \cong B$, not an equality $F(A) = B$. A proof that writes $B = F(A)$ has assumed too much.
    3. **Hiding the choice.** Writing "let $G(B)$ be *the* object with $F(G(B)) \cong B$" suggests that the object is unique. It is not, and neither is the isomorphism. Say "choose", and choose the isomorphism $\varepsilon_B$ at the same time as the object.
    4. **Defining $G$ on objects and stopping.** A functor also acts on arrows, and must preserve identities and composition. In Section 5 that is Steps 2 and 3, and it is where full and faithful are used.
    5. **Proving the components of $\eta$ are isomorphisms but not that $\eta$ is natural (or the reverse).** A natural isomorphism needs both. In Section 5, Step 5 gives the isomorphisms and Step 6 the naturality.
    6. **Confusing $\mathcal{A} \simeq \mathcal{B}$ with $\mathcal{A} \cong \mathcal{B}$.** Equivalent categories can have different numbers of objects. An argument that counts objects is an argument about isomorphism.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why This Matters

    - **2A–2C (adjunctions).** An adjunction $F \dashv G$ has a unit $\eta \colon 1 \Rightarrow GF$ and a counit $\varepsilon \colon FG \Rightarrow 1$ that are natural transformations but usually *not* isomorphisms. An equivalence is the special case in which they are. The notation of this module was chosen to match.
    - **3A (sets and size).** A category is called *essentially small* when it is equivalent to a small one. $\mathbf{FinSet}$ is essentially small because of its skeleton $\mathcal{N}$; $\mathbf{Set}$ is not, and the proof there combines the definition of equivalence from this module with Cantor's diagonal argument.
    - **4C (consequences of Yoneda).** The Yoneda embedding is full and faithful, so by Lemma 1 it reflects isomorphisms: $H_A \cong H_B$ implies $A \cong B$. The proof pattern "apply a full and faithful functor, argue there, come back" is the one you practised in Section 5.
    - **Everywhere.** From now on, a statement in category theory is considered meaningful only if it is invariant under equivalence. This is why later definitions (limits, adjoints, representations) all determine their objects "up to isomorphism" and never "up to equality".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Both exercises use the shared finite-category encoding: a category is a dictionary with keys `objects`, `arrows` (name $\mapsto$ (domain, codomain)), `identity` and `compose`, where `compose[(g, f)]` is $g \circ f$; a functor is `{"objects": {...}, "arrows": {...}}`. The cells run as shipped; fill in each `# TODO`, then uncomment the `print` checks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Essentially Surjective on Objects

    Write `is_essentially_surjective(A, B, F)`. The helper `isomorphic(cat, X, Y)`, which decides whether two objects of a finite category are isomorphic, is provided.

    The test category `P` is the preorder on $\{a, b, c\}$ with $a \leq b$, $b \leq a$ and $a \leq c$ (so $a \cong b$, and $c$ is in a class of its own), and `two` is the category $\mathbf{2}$ with one non-identity arrow $0 \to 1$.
    """)
    return


@app.cell
def _():
    def _run():
        def preorder_cat(objects, leq_pairs):
            # leq_pairs must already be reflexive and transitive
            return {
                "objects": list(objects),
                "arrows": {_x + "<=" + _y: (_x, _y) for (_x, _y) in leq_pairs},
                "identity": {_x: _x + "<=" + _x for _x in objects},
                "compose": {
                    (_y + "<=" + _z, _x + "<=" + _y): _x + "<=" + _z
                    for (_x, _y) in leq_pairs for (_y2, _z) in leq_pairs if _y == _y2
                },
            }

        def isomorphic(cat, X, Y):
            for _f, (_d, _c) in cat["arrows"].items():
                if (_d, _c) != (X, Y):
                    continue
                for _g, (_d2, _c2) in cat["arrows"].items():
                    if (_d2, _c2) == (Y, X) and cat["compose"][(_g, _f)] == cat["identity"][X] \
                            and cat["compose"][(_f, _g)] == cat["identity"][Y]:
                        return True
            return False

        P = preorder_cat(
            ["a", "b", "c"],
            [("a", "a"), ("b", "b"), ("c", "c"), ("a", "b"), ("b", "a"), ("a", "c"), ("b", "c")],
        )
        two = preorder_cat(["0", "1"], [("0", "0"), ("1", "1"), ("0", "1")])

        F1 = {"objects": {"0": "a", "1": "c"}, "arrows": {"0<=0": "a<=a", "1<=1": "c<=c", "0<=1": "a<=c"}}
        F2 = {"objects": {"0": "a", "1": "b"}, "arrows": {"0<=0": "a<=a", "1<=1": "b<=b", "0<=1": "a<=b"}}

        def is_essentially_surjective(A, B, F):
            # TODO: every object of B must be isomorphic (in B) to F(X) for some object X of A
            _result = ...
            return _result

        # print(isomorphic(P, "a", "b"), isomorphic(P, "a", "c"))   # expect True False
        # print(is_essentially_surjective(two, P, F1))               # expect True
        # print(is_essentially_surjective(two, P, F2))               # expect False

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Carry Out Step 2 of the Proof

    Here `B` is the full subcategory of $\mathbf{Set}$ on the two sets $X = \{0, 1\}$ and $Y = \{p, q\}$: sixteen arrows, named like `"XY:qp"` for the function $X \to Y$ with $0 \mapsto q$, $1 \mapsto p$. `A` is the full subcategory on $X$ alone, and `F` is the inclusion, which is full, faithful and essentially surjective on objects.

    Step 1 of the proof has been done for you: `G_ob` and `eps` record a choice of $G(B)$ and of an isomorphism $\varepsilon_B \colon FG(B) \to B$ for each object $B$. Carry out Step 2: for every arrow $g \colon B \to B'$ of `B`, find the unique arrow $G(g)$ of `A` satisfying equation $(\dagger)$ of Section 5. The helper `inverse(cat, f)` returns the name of the inverse of an isomorphism.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def set_cat(sets):
            # full subcategory of Set on the named finite sets; arrow "XY:qp" sends the elements
            # of X, in order, to q and p
            _arrows, _table = {}, {}
            for _X, _xs in sets.items():
                for _Y, _ys in sets.items():
                    for _images in itertools.product(_ys, repeat=len(_xs)):
                        _n = _X + _Y + ":" + "".join(_images)
                        _arrows[_n] = (_X, _Y)
                        _table[_n] = dict(zip(_xs, _images))
            _lookup = {(_arrows[_n], tuple(sorted(_t.items()))): _n for _n, _t in _table.items()}
            _compose = {}
            for _f, (_X, _Y) in _arrows.items():
                for _g, (_Y2, _Z) in _arrows.items():
                    if _Y == _Y2:
                        _c = {_x: _table[_g][_table[_f][_x]] for _x in sets[_X]}
                        _compose[(_g, _f)] = _lookup[((_X, _Z), tuple(sorted(_c.items())))]
            _identity = {_X: _lookup[((_X, _X), tuple(sorted((_x, _x) for _x in _xs)))] for _X, _xs in sets.items()}
            return {"objects": list(sets), "arrows": _arrows, "identity": _identity, "compose": _compose}

        def inverse(cat, f):
            _X, _Y = cat["arrows"][f]
            for _g, (_d, _c) in cat["arrows"].items():
                if (_d, _c) == (_Y, _X) and cat["compose"][(_g, f)] == cat["identity"][_X] \
                        and cat["compose"][(f, _g)] == cat["identity"][_Y]:
                    return _g
            return None

        B = set_cat({"X": ("0", "1"), "Y": ("p", "q")})
        A = set_cat({"X": ("0", "1")})
        F = {"objects": {"X": "X"}, "arrows": {_a: _a for _a in A["arrows"]}}

        G_ob = {"X": "X", "Y": "X"}                 # Step 1: the chosen objects G(B) ...
        eps = {"X": "XX:01", "Y": "XY:pq"}          # ... and the chosen isomorphisms F(G(B)) -> B

        G_arr = {}
        for _g, (_dom, _cod) in B["arrows"].items():
            # TODO: compute in B the arrow that F(G(g)) must equal, then search the arrows of A
            #       from G_ob[_dom] to G_ob[_cod] for the one that F sends to it
            G_arr[_g] = ...

        # print(len(G_arr))                                        # expect 16
        # print(G_arr["YY:qp"], G_arr["XY:qq"], G_arr["YX:10"])    # expect XX:10 XX:11 XX:10
        # print(all(A["compose"][(G_arr[g2], G_arr[g1])] == G_arr[g2g1]
        #           for (g2, g1), g2g1 in B["compose"].items()))   # expect True  (G preserves composition)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six proof briefs, in `exercises/1e/`. Each has the statement, what you may assume, what a complete proof must contain, and hints that open one at a time. There are no solutions anywhere in the course.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | Equivalence is reflexive and symmetric — `exercises/1e/p01_reflexive_symmetric.md` | warm-up | unpacking the definition |
    | P02 | When are two discrete categories equivalent? — `exercises/1e/p02_discrete_categories.md` | warm-up | unpacking the definition, both directions |
    | P03 | Equivalences compose — `exercises/1e/p03_equivalences_compose.md` | core | closure of three properties under composition, or whiskering |
    | P04 | Matrices and finite-dimensional vector spaces — `exercises/1e/p04_matrices_and_vector_spaces.md` | core | full, faithful, essentially surjective |
    | P05 | Equivalences preserve monomorphisms — `exercises/1e/p05_equivalences_preserve_monics.md` | core | apply a full and faithful functor and come back |
    | P06 | Equivalent skeletal categories are isomorphic — `exercises/1e/p06_skeletal_equivalent_isomorphic.md` | stretch | building an inverse functor |

    **How to submit a proof.** Write your proof in `proofs/1e/pNN_<slug>.md` (the same file name as the brief), then ask Claude to review it.
    The review points at gaps and asks questions; it does not supply a model proof, so the proof stays yours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [1D: Natural Transformations](../1d_natural_transformations/) | Next: [2A: Adjunctions: Definition & Examples](../2a_adjunctions/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
