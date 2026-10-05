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
    # 1B: Isomorphisms, Duality & New Categories from Old

    > *Every theorem about all categories is two theorems: the one you proved, and the one you get by turning every arrow around.*
    > — the principle of duality, as a slogan

    In 1A you learned what a category is. A category gives you very little to work with: arrows, composition, identities. This module asks how much can be said using only that. In particular: **when are two objects "the same" as far as the category can tell, and which arrows play the roles that injective and surjective functions play in $\mathbf{Set}$?** The answers are *isomorphism*, *monomorphism* and *epimorphism*, each defined purely by how an arrow composes with other arrows.

    The second theme is that categories can be manufactured from other categories. Reversing every arrow of $\mathcal{A}$ gives the *opposite* category $\mathcal{A}^{\mathrm{op}}$, and this simple construction has a large consequence: every definition has a mirror-image definition and every proof a mirror-image proof, which you get for free. You will also meet the product $\mathcal{A} \times \mathcal{B}$ of two categories and the special categories called groupoids.

    By the end you will be able to prove that inverses are unique, prove and use cancellation properties of monics and epics, tell apart "monic and epic" from "isomorphism" with a counterexample, and **dualize** a proof instead of writing it twice.

    A note on sources: Leinster introduces isomorphisms, opposites and products in §1.1 but postpones monics and epics to Chapter 5. We follow Riehl §1.2 and meet them now, because they are the best early practice in proofs that use nothing but composition.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Isomorphisms

    In $\mathbf{Set}$, a bijection $f \colon A \to B$ lets you treat $A$ and $B$ as the same set with the elements renamed. "Bijection" is defined using elements, which a general category does not have. But 0B gave a second description: a function is a bijection exactly when it has a two-sided inverse. That description mentions only composition and identities, so it makes sense anywhere.

    > **Definition (isomorphism).** Let $\mathcal{A}$ be a category. An arrow $f \colon A \to B$ is an **isomorphism** if there exists an arrow $g \colon B \to A$ such that
    > $$g \circ f = 1_A \qquad\text{and}\qquad f \circ g = 1_B.$$
    > Such a $g$ is called an **inverse** of $f$. Objects $A$ and $B$ are **isomorphic**, written $A \cong B$, if there exists an isomorphism $A \to B$.

    **Reading the definition.** To prove $f \colon A \to B$ is an isomorphism:

    1. produce an arrow $g$, and check it goes from $B$ to $A$;
    2. verify $g \circ f = 1_A$ (an equation in $\mathcal{A}(A, A)$);
    3. verify $f \circ g = 1_B$ (an equation in $\mathcal{A}(B, B)$).

    Steps 2 and 3 are separate obligations; neither implies the other. To prove $f$ is **not** an isomorphism you must show that *no* arrow $B \to A$ satisfies both equations.

    **Examples.**

    - In $\mathbf{Set}$, the isomorphisms are the bijections (0B).
    - In $\mathbf{Grp}$, the isomorphisms are the bijective homomorphisms: the inverse function of a bijective homomorphism is again a homomorphism, so it is an inverse in $\mathbf{Grp}$.
    - In a monoid regarded as a one-object category, an arrow is an isomorphism exactly when it is an invertible element. In $(\mathbb{Z}/4, \times, 1)$ the isomorphisms are $1$ and $3$, since $3 \times 3 = 9 \equiv 1$.
    - In any category, every identity $1_A$ is an isomorphism with inverse $1_A$, because $1_A \circ 1_A = 1_A$ by the identity law.

    **Non-examples.**

    - In $\mathbf{Set}$, let $f \colon \{1, 2\} \to \{1\}$ be the only function and $g \colon \{1\} \to \{1, 2\}$ send $1$ to $1$. Then $f \circ g = 1_{\{1\}}$, but $g \circ f$ sends $2$ to $1$, so $g \circ f \neq 1_{\{1,2\}}$. One of the two equations is not enough.
    - In $\mathbf{Top}$, a continuous bijection need not be an isomorphism. The map $[0, 1) \to S^1$, $t \mapsto (\cos 2\pi t, \sin 2\pi t)$, is continuous and bijective, but its inverse function is not continuous, so it has no inverse *in $\mathbf{Top}$*. (The isomorphisms of $\mathbf{Top}$ are called homeomorphisms.) This is why isomorphism is defined by an inverse arrow and not by bijectivity.

    The definition says "an inverse". The first theorem of the subject is that it could have said "the inverse".

    > **Proposition 1.1 (inverses are unique).** Let $f \colon A \to B$ be an arrow in a category $\mathcal{A}$. If $g \colon B \to A$ and $g' \colon B \to A$ are both inverses of $f$, then $g = g'$.

    **Goal.** For all arrows $g, g' \colon B \to A$: if $g \circ f = 1_A$, $f \circ g = 1_B$, $g' \circ f = 1_A$ and $f \circ g' = 1_B$, then $g = g'$.

    **Given.** The four equations, the identity laws and associativity. Nothing about elements.

    **Plan.** A uniqueness argument of the kind from 0C: write down one expression involving both candidates, and simplify it in two ways. The expression is $g \circ f \circ g'$.

    **Proof.**
    $$
    \begin{aligned}
    g &= g \circ 1_B && \text{(identity law)} \\
      &= g \circ (f \circ g') && \text{(because } f \circ g' = 1_B\text{)} \\
      &= (g \circ f) \circ g' && \text{(associativity)} \\
      &= 1_A \circ g' && \text{(because } g \circ f = 1_A\text{)} \\
      &= g' && \text{(identity law).}
    \end{aligned}
    $$
    $\blacksquare$

    **What made it work.** The "sandwich" $g \circ f \circ g'$ collapses to $g$ if you bracket one way and to $g'$ if you bracket the other. Notice that only two of the four hypotheses were used: $g \circ f = 1_A$ and $f \circ g' = 1_B$. So the proof shows slightly more: *if $g$ is a left inverse of $f$ and $g'$ is a right inverse of $f$, then $g = g'$.* Reach for a sandwich whenever two arrows are each characterised by cancelling against the same third arrow.

    Because the inverse is unique we may give it a name: $f^{-1}$.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (0, 0, "$A$"), "B": (3, 0, "$B$")},
        [
            ("A", "B", "$f$", {"rad": -0.3}),
            ("B", "A", "$g$", {"rad": -0.3}),
            ("A", "A", "$1_A$", {"loop": "left"}),
            ("B", "B", "$1_B$", {"loop": "right"}),
        ],
        figsize=(5.6, 2.8),
        title=r"An isomorphism: $g \circ f = 1_A$ and $f \circ g = 1_B$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Monomorphisms and Epimorphisms

    Injective and surjective functions are also defined using elements. What is the arrow-only version? The idea is to ask how $f$ behaves when other arrows are composed with it: can $f$ be *cancelled*?

    > **Definition (monic, epic).** Let $f \colon A \to B$ be an arrow in a category $\mathcal{A}$.
    >
    > - $f$ is a **monomorphism** (or is **monic**) if for every object $C$ and every pair of arrows $g, h \colon C \to A$,
    >   $$f \circ g = f \circ h \quad\text{implies}\quad g = h.$$
    > - $f$ is an **epimorphism** (or is **epic**) if for every object $C$ and every pair of arrows $g, h \colon B \to C$,
    >   $$g \circ f = h \circ f \quad\text{implies}\quad g = h.$$

    So a monic can be cancelled on the left, and an epic can be cancelled on the right.

    **Reading the definition.** To prove $f$ is monic:

    1. let $C$ be an arbitrary object and $g, h \colon C \to A$ arbitrary arrows *into the domain of $f$*;
    2. assume $f \circ g = f \circ h$;
    3. deduce $g = h$.

    To prove $f$ is **not** monic, exhibit one object $C$ and two *different* arrows $g \neq h \colon C \to A$ with $f \circ g = f \circ h$. For epic, the test arrows go *out of the codomain* of $f$. The two pictures below show where the test arrows sit.

    > **Proposition 2.1.** In $\mathbf{Set}$, a function $f \colon A \to B$ is monic if and only if it is injective.

    **Goal.** Two implications. ($\Leftarrow$) If for all $a, a' \in A$, $f(a) = f(a')$ implies $a = a'$, then for all sets $C$ and functions $g, h \colon C \to A$, $f \circ g = f \circ h$ implies $g = h$. ($\Rightarrow$) The converse.

    **Given.** The definitions of injective and of monic; two functions are equal when they have the same domain and codomain and agree at every element (0B).

    **Plan.** ($\Leftarrow$) Direct: evaluate at an arbitrary element of $C$. ($\Rightarrow$) We are given a property quantified over *all* test sets $C$ and must choose a useful one. An element of $A$ is the same thing as a function from a one-element set to $A$; so test against the one-element set.

    **Proof.**
    ($\Leftarrow$) Suppose $f$ is injective. Let $C$ be a set and $g, h \colon C \to A$ functions with $f \circ g = f \circ h$. Let $c \in C$. Then $f(g(c)) = (f \circ g)(c) = (f \circ h)(c) = f(h(c))$. Because $f$ is injective, $g(c) = h(c)$. This holds for every $c \in C$, and $g, h$ have the same domain and codomain, so $g = h$.

    ($\Rightarrow$) Suppose $f$ is monic. Let $a, a' \in A$ with $f(a) = f(a')$. Let $C = \{\ast\}$ be a one-element set, and define $g, h \colon C \to A$ by $g(\ast) = a$ and $h(\ast) = a'$. Then $(f \circ g)(\ast) = f(a) = f(a') = (f \circ h)(\ast)$, and $\ast$ is the only element of $C$, so $f \circ g = f \circ h$. Because $f$ is monic, $g = h$. Evaluating at $\ast$ gives $a = a'$. So $f$ is injective. $\blacksquare$

    **What made it work.** In the ($\Rightarrow$) direction the hypothesis was a "for all $C$" statement, and the proof *chose* $C$. Functions out of a one-element set pick out elements, which is how a statement about arrows was turned back into a statement about elements. Whenever you are handed a universally quantified hypothesis, ask what it says for a well-chosen special case.

    The matching statement for epics, "epic in $\mathbf{Set}$ if and only if surjective", is exercise P03.

    **Examples in categories whose arrows are not functions.**

    - In the category of a preorder, **every** arrow is both monic and epic: any two arrows $g, h \colon C \to A$ lie in a hom-set with at most one element, so $g = h$ whatever $f$ is.
    - In a monoid regarded as a one-object category, the arrow $m$ is monic exactly when $m \cdot g = m \cdot h$ implies $g = h$ (left cancellation) and epic exactly when $g \cdot m = h \cdot m$ implies $g = h$. In $(\mathbb{N}, +, 0)$ every arrow is monic and epic. In $(\mathbb{Z}/4, \times, 1)$ the arrow $2$ is neither: $2 \times 1 = 2 \times 3$ although $1 \neq 3$.

    **Monic and epic does not imply isomorphism.** In $\mathbf{Set}$ a function that is injective and surjective is a bijection. It is tempting to guess that in any category an arrow that is monic and epic is an isomorphism. That is false. The preorder $\{0 \le 1\}$ already shows it (its arrow $0 \to 1$ is monic and epic, and there is no arrow $1 \to 0$ to be an inverse), and here is an example among structured sets.

    > **Proposition 2.2.** In $\mathbf{Mon}$, the inclusion $i \colon (\mathbb{N}, +, 0) \to (\mathbb{Z}, +, 0)$ is monic and epic but is not an isomorphism.

    **Goal.** (i) For all monoids $C$ and homomorphisms $g, h \colon C \to \mathbb{N}$: $i \circ g = i \circ h$ implies $g = h$. (ii) For all monoids $M$ and homomorphisms $g, h \colon \mathbb{Z} \to M$: $g \circ i = h \circ i$ implies $g = h$. (iii) There is no homomorphism $j \colon \mathbb{Z} \to \mathbb{N}$ with $i \circ j = 1_{\mathbb{Z}}$ and $j \circ i = 1_{\mathbb{N}}$.

    **Given.** $i(n) = n$. A monoid homomorphism preserves the operation and the unit. Proposition 1.1, applied in the one-object category of $M$.

    **Plan.** (i) uses injectivity of $i$. (ii) is the interesting part: a homomorphism out of $\mathbb{Z}$ is determined by its values on $\mathbb{N}$, because the value at $-n$ must be the inverse of the value at $n$, and inverses are unique. (iii) is a proof by contradiction.

    **Proof.**
    (i) Let $g, h \colon C \to \mathbb{N}$ be homomorphisms with $i \circ g = i \circ h$. For each $c \in C$, $g(c) = i(g(c)) = i(h(c)) = h(c)$. So $g = h$.

    (ii) Write the operation of $M$ as multiplication, with unit $e$. Let $g, h \colon \mathbb{Z} \to M$ be homomorphisms with $g \circ i = h \circ i$; that is, $g(n) = h(n)$ for all $n \ge 0$. Let $n > 0$. Then
    $$g(-n) \cdot g(n) = g(-n + n) = g(0) = e \qquad\text{and}\qquad g(n) \cdot g(-n) = g(n + (-n)) = g(0) = e,$$
    using that $g$ preserves the operation and the unit. So in the one-object category of $M$, the arrow $g(-n)$ is an inverse of the arrow $g(n)$. By the same computation with $h$, the arrow $h(-n)$ is an inverse of $h(n)$, and $h(n) = g(n)$. So $g(-n)$ and $h(-n)$ are both inverses of the same arrow, and by Proposition 1.1, $g(-n) = h(-n)$. Hence $g$ and $h$ agree on all of $\mathbb{Z}$, so $g = h$.

    (iii) Suppose such a $j$ existed. Then $-1 = 1_{\mathbb{Z}}(-1) = i(j(-1)) = j(-1)$. But $j(-1) \in \mathbb{N}$, so $j(-1) \ge 0$. This contradicts $-1 < 0$. $\blacksquare$

    **What made it work.** Epic does not mean "hits every element". It means "two arrows out of the codomain that agree on the image of $f$ agree everywhere". In $\mathbf{Mon}$, the structure forces the values off the image, so a non-surjective homomorphism can still be epic. The lesson for proofs: in a general category, never replace "monic" by "injective" or "epic" by "surjective".

    > Reference: [Riehl §1.2](https://math.jhu.edu/~eriehl/context.pdf). Leinster treats monics in §5.1 and epics in §5.2 of [Basic Category Theory](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "C": (0, 0, "$C$"), "A": (2, 0, "$A$"), "B": (4, 0, "$B$"),
            "A2": (6, 0, "$A$"), "B2": (8, 0, "$B$"), "C2": (10, 0, "$C$"),
        },
        [
            ("C", "A", "$g$", {"rad": -0.35, "color": "#1d4ed8"}),
            ("C", "A", "$h$", {"rad": 0.35, "color": "#1d4ed8"}),
            ("A", "B", "$f$"),
            ("A2", "B2", "$f$"),
            ("B2", "C2", "$g$", {"rad": -0.35, "color": "#b45309"}),
            ("B2", "C2", "$h$", {"rad": 0.35, "color": "#b45309"}),
        ],
        figsize=(9.0, 2.4),
        title="Testing whether $f$ is monic (left) and whether $f$ is epic (right)",
    )
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(dom, cod):
            return [dict(zip(dom, _vals)) for _vals in itertools.product(cod, repeat=len(dom))]

        def is_monic_in_finset(f, dom, test_sets):
            for _C in test_sets:
                for _g in all_functions(_C, dom):
                    for _h in all_functions(_C, dom):
                        if _g != _h and all(f[_g[_c]] == f[_h[_c]] for _c in _C):
                            return False
            return True

        _A, _B = [0, 1, 2], ["x", "y", "z", "w"]
        _tests = [["*"], ["p", "q"]]
        _agree = 0
        _fs = all_functions(_A, _B)
        for _f in _fs:
            _injective = len(set(_f.values())) == len(_A)
            if _injective == is_monic_in_finset(_f, _A, _tests):
                _agree += 1
        print("=== Proposition 2.1, checked by brute force ===")
        print(f"  functions from a 3-element set to a 4-element set : {len(_fs)}")
        print(f"  of which injective                                : {sum(len(set(_f.values())) == 3 for _f in _fs)}")
        print(f"  'injective' and 'left-cancellable' agree for      : {_agree} of {len(_fs)}")
        print("  (test sets C: a one-element set and a two-element set)")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Monics Under Composition

    Proofs about monics follow one pattern: you are handed an equation between composites, and you peel arrows off the left one at a time, each time citing the cancellation property that allows it. The next proposition is the standard model.

    > **Proposition 3.1.** Let $f \colon A \to B$ and $g \colon B \to C$ be arrows in a category $\mathcal{A}$.
    > (a) If $f$ and $g$ are both monic, then $g \circ f$ is monic.
    > (b) If $g \circ f$ is monic, then $f$ is monic.

    **Goal.** (a) For every object $X$ and all $x, y \colon X \to A$: if $(g \circ f) \circ x = (g \circ f) \circ y$ then $x = y$. (b) For every object $X$ and all $x, y \colon X \to A$: if $f \circ x = f \circ y$ then $x = y$.

    **Given.** (a) $f$ is monic and $g$ is monic. (b) $g \circ f$ is monic. In both: associativity.

    **Plan.** (a) Rebracket, cancel $g$, then cancel $f$. (b) We want to use the hypothesis about $g \circ f$, so we manufacture an equation that begins with $g \circ f$ by composing both sides of the given equation with $g$.

    **Proof.**
    (a) Let $x, y \colon X \to A$ with $(g \circ f) \circ x = (g \circ f) \circ y$. By associativity, $g \circ (f \circ x) = g \circ (f \circ y)$. Here $f \circ x$ and $f \circ y$ are two arrows $X \to B$, into the domain of $g$; because $g$ is monic, $f \circ x = f \circ y$. Now $x, y$ are two arrows into the domain of $f$; because $f$ is monic, $x = y$.

    (b) Let $x, y \colon X \to A$ with $f \circ x = f \circ y$. Composing both sides with $g$ gives $g \circ (f \circ x) = g \circ (f \circ y)$. By associativity, $(g \circ f) \circ x = (g \circ f) \circ y$. Because $g \circ f$ is monic, $x = y$. $\blacksquare$

    **What made it work.** Associativity moves the brackets so that the arrow you are allowed to cancel is outermost. In (b) the trick was to apply $g$ to both sides: equal arrows stay equal after composing with anything, and this turned the equation into one the hypothesis could act on.

    **Non-example for the "other half" of (b).** If $g \circ f$ is monic, $g$ need not be. In $\mathbf{Set}$ take $f \colon \{1\} \to \{1, 2\}$ with $f(1) = 1$ and $g \colon \{1, 2\} \to \{1\}$ the only function. Then $g \circ f = 1_{\{1\}}$, which is injective and so monic by Proposition 2.1, but $g$ is not injective and so not monic.

    > Reference: [Riehl §1.2](https://math.jhu.edu/~eriehl/context.pdf); Leinster §5.1.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Opposite Category and the Principle of Duality

    The definitions of monic and epic are mirror images: one tests with arrows *into* the domain, the other with arrows *out of* the codomain; one cancels on the left, the other on the right. That symmetry runs through the whole subject, and the following construction makes it precise.

    > **Definition (opposite category).** Let $\mathcal{A}$ be a category. Its **opposite** (or **dual**) $\mathcal{A}^{\mathrm{op}}$ is defined by:
    >
    > - the objects of $\mathcal{A}^{\mathrm{op}}$ are the objects of $\mathcal{A}$;
    > - $\mathcal{A}^{\mathrm{op}}(A, B) = \mathcal{A}(B, A)$: an arrow $A \to B$ in $\mathcal{A}^{\mathrm{op}}$ is an arrow $B \to A$ in $\mathcal{A}$;
    > - for arrows $A \xrightarrow{f} B \xrightarrow{g} C$ of $\mathcal{A}^{\mathrm{op}}$, the composite in $\mathcal{A}^{\mathrm{op}}$ is
    >   $$g \circ^{\mathrm{op}} f = f \circ g \quad\text{(computed in } \mathcal{A}\text{)};$$
    > - the identity on $A$ in $\mathcal{A}^{\mathrm{op}}$ is $1_A$.

    **Reading the definition.** Check that the composite makes sense. In $\mathcal{A}$, $f$ is an arrow $B \to A$ and $g$ is an arrow $C \to B$. So $f \circ g$ is defined in $\mathcal{A}$ and is an arrow $C \to A$ there, which is an arrow $A \to C$ in $\mathcal{A}^{\mathrm{op}}$, as required. To work in $\mathcal{A}^{\mathrm{op}}$: (1) reverse the direction of every arrow; (2) reverse the order of every composite; (3) leave objects and identities alone.

    > **Proposition 4.1.** $\mathcal{A}^{\mathrm{op}}$ is a category.

    **Goal.** For all arrows $A \xrightarrow{f} B \xrightarrow{g} C \xrightarrow{h} D$ of $\mathcal{A}^{\mathrm{op}}$: $(h \circ^{\mathrm{op}} g) \circ^{\mathrm{op}} f = h \circ^{\mathrm{op}} (g \circ^{\mathrm{op}} f)$; and for every arrow $f \colon A \to B$ of $\mathcal{A}^{\mathrm{op}}$: $f \circ^{\mathrm{op}} 1_A = f = 1_B \circ^{\mathrm{op}} f$. (That composites and identities lie in the right hom-sets was checked just above.)

    **Given.** $\mathcal{A}$ is a category. In $\mathcal{A}$ the three arrows are $f \colon B \to A$, $g \colon C \to B$, $h \colon D \to C$.

    **Plan.** Translate each side into $\mathcal{A}$ using the definition of $\circ^{\mathrm{op}}$, then use the axioms of $\mathcal{A}$.

    **Proof.** By the definition of $\circ^{\mathrm{op}}$, applied twice on each side,
    $$(h \circ^{\mathrm{op}} g) \circ^{\mathrm{op}} f = f \circ (h \circ^{\mathrm{op}} g) = f \circ (g \circ h), \qquad h \circ^{\mathrm{op}} (g \circ^{\mathrm{op}} f) = (g \circ^{\mathrm{op}} f) \circ h = (f \circ g) \circ h.$$
    These are equal by associativity in $\mathcal{A}$. For the identity laws: $f \circ^{\mathrm{op}} 1_A = 1_A \circ f = f$, by the identity law in $\mathcal{A}$ for the arrow $f \colon B \to A$, whose codomain is $A$; and $1_B \circ^{\mathrm{op}} f = f \circ 1_B = f$, by the other identity law in $\mathcal{A}$, since the domain of $f$ in $\mathcal{A}$ is $B$. $\blacksquare$

    **What made it work.** Each axiom for $\mathcal{A}^{\mathrm{op}}$ is the *same* axiom for $\mathcal{A}$ read backwards: the two bracketings swap, and the two identity laws swap. The axioms of a category are symmetric under reversing arrows, and that is the source of duality.

    **Examples.**

    - If $P$ is a preorder, $P^{\mathrm{op}}$ is the preorder with the reversed relation: $x \le^{\mathrm{op}} y$ exactly when $y \le x$. The opposite of the divisibility order is "is a multiple of".
    - If $M$ is a monoid, $M^{\mathrm{op}}$ is the monoid with the same elements and the multiplication $g \cdot^{\mathrm{op}} f = f \cdot g$. When $M$ is commutative, $M^{\mathrm{op}}$ has the same multiplication table as $M$.
    - $(\mathcal{A}^{\mathrm{op}})^{\mathrm{op}} = \mathcal{A}$: reversing twice restores every hom-set and every composite.

    **Non-example.** An arrow of $\mathbf{Set}^{\mathrm{op}}$ is *not* a function from its domain to its codomain. An arrow $A \to B$ of $\mathbf{Set}^{\mathrm{op}}$ is a function $B \to A$; it is not a function $A \to B$, and it cannot be applied to elements of $A$. The opposite of a category of functions is usually not a category of functions.

    ### Duality

    Every statement about a category that is phrased in terms of objects, arrows, composition and identities has a **dual statement**: reverse every arrow and the order of every composite. For example:

    | Notion | Dual notion |
    |---|---|
    | domain | codomain |
    | $g \circ f$ | $f \circ g$ |
    | monic | epic |
    | $g$ is a left inverse of $f$ ($g \circ f = 1$) | $g$ is a right inverse of $f$ ($f \circ g = 1$) |
    | isomorphism | isomorphism (the notion is its own dual) |

    > **Principle of duality.** If a statement holds in every category, then its dual statement holds in every category.

    The reason is one line: the dual statement holds in $\mathcal{A}$ exactly when the original statement holds in $\mathcal{A}^{\mathrm{op}}$, and $\mathcal{A}^{\mathrm{op}}$ is a category (Proposition 4.1), so the original statement does hold there. Here is the principle in action, with the bookkeeping written out in full once.

    > **Proposition 4.2.** Let $f \colon A \to B$ be an arrow of $\mathcal{A}$. Then $f$ is epic in $\mathcal{A}$ if and only if $f$, regarded as an arrow $B \to A$ of $\mathcal{A}^{\mathrm{op}}$, is monic in $\mathcal{A}^{\mathrm{op}}$.

    **Goal.** The two conditions are the same statement.

    **Given.** The definitions of monic, epic and $\mathcal{A}^{\mathrm{op}}$.

    **Plan.** Write out "monic in $\mathcal{A}^{\mathrm{op}}$" and translate it into $\mathcal{A}$ symbol by symbol.

    **Proof.** "$f \colon B \to A$ is monic in $\mathcal{A}^{\mathrm{op}}$" says: for every object $C$ and all arrows $g, h \colon C \to B$ of $\mathcal{A}^{\mathrm{op}}$, if $f \circ^{\mathrm{op}} g = f \circ^{\mathrm{op}} h$ then $g = h$. Arrows $C \to B$ of $\mathcal{A}^{\mathrm{op}}$ are arrows $B \to C$ of $\mathcal{A}$, and $f \circ^{\mathrm{op}} g = g \circ f$. So the statement reads: for every object $C$ and all arrows $g, h \colon B \to C$ of $\mathcal{A}$, if $g \circ f = h \circ f$ then $g = h$. That is the definition of "$f$ is epic in $\mathcal{A}$". $\blacksquare$

    **What made it work.** Nothing was proved; a definition was translated. That is the point: "epic" was *designed* to be "monic in the opposite category".

    > **Corollary 4.3.** Let $f \colon A \to B$ and $g \colon B \to C$ be arrows in a category $\mathcal{A}$.
    > (a) If $f$ and $g$ are both epic, then $g \circ f$ is epic.
    > (b) If $g \circ f$ is epic, then $g$ is epic.

    **Goal.** As stated, for every category $\mathcal{A}$.

    **Given.** Proposition 3.1, which holds in every category, in particular in $\mathcal{A}^{\mathrm{op}}$. Proposition 4.2.

    **Plan.** Dualize Proposition 3.1: apply it in $\mathcal{A}^{\mathrm{op}}$ and translate back.

    **Proof.** In $\mathcal{A}^{\mathrm{op}}$ the arrows are $g \colon C \to B$ and $f \colon B \to A$, and their composite there is $f \circ^{\mathrm{op}} g = g \circ f$, an arrow $C \to A$. So in $\mathcal{A}^{\mathrm{op}}$, $g$ is the arrow applied first and $f$ the arrow applied second.

    (a) Suppose $f$ and $g$ are epic in $\mathcal{A}$. By Proposition 4.2 they are monic in $\mathcal{A}^{\mathrm{op}}$. By Proposition 3.1(a) applied in the category $\mathcal{A}^{\mathrm{op}}$, their composite $f \circ^{\mathrm{op}} g$ is monic in $\mathcal{A}^{\mathrm{op}}$. That composite is $g \circ f$, so by Proposition 4.2 again $g \circ f$ is epic in $\mathcal{A}$.

    (b) Suppose $g \circ f$ is epic in $\mathcal{A}$. Then $f \circ^{\mathrm{op}} g$ is monic in $\mathcal{A}^{\mathrm{op}}$. By Proposition 3.1(b) applied in $\mathcal{A}^{\mathrm{op}}$, the arrow applied *first* is monic in $\mathcal{A}^{\mathrm{op}}$; that arrow is $g$. By Proposition 4.2, $g$ is epic in $\mathcal{A}$. $\blacksquare$

    **What made it work.** No cancellation argument was repeated. Notice what duality did to (b): "the first arrow is monic" became "the *second* arrow is epic", because the order of composition flipped. When you dualize, re-derive which arrow is which; do not guess. From now on a proof may simply say "by duality", but only once you could write out the translation as above.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375) (opposite category, duality); [Riehl §1.2](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Product Categories

    A second way to build a new category: take two and form pairs.

    > **Definition (product category).** Let $\mathcal{A}$ and $\mathcal{B}$ be categories. The **product category** $\mathcal{A} \times \mathcal{B}$ has
    >
    > - objects: pairs $(A, B)$ with $A$ an object of $\mathcal{A}$ and $B$ an object of $\mathcal{B}$;
    > - arrows $(A, B) \to (A', B')$: pairs $(f, g)$ with $f \colon A \to A'$ in $\mathcal{A}$ and $g \colon B \to B'$ in $\mathcal{B}$;
    > - composition: $(f', g') \circ (f, g) = (f' \circ f, \; g' \circ g)$;
    > - identities: $1_{(A, B)} = (1_A, 1_B)$.

    **Reading the definition.** Everything happens in each coordinate separately. To check that this is a category you would verify that $(f' \circ f, g' \circ g)$ is an arrow between the right pairs, and that associativity and the identity laws hold; each should reduce to the corresponding fact in $\mathcal{A}$ and in $\mathcal{B}$. That verification is exercise P02.

    **Examples.**

    - If $P$ and $Q$ are preorders, $P \times Q$ is the preorder on pairs with $(p, q) \le (p', q')$ exactly when $p \le p'$ and $q \le q'$: there is at most one pair $(f, g)$, and there is one exactly when both components exist.
    - If $M$ and $N$ are monoids, $M \times N$ is the one-object category of the product monoid, with $(m', n') \cdot (m, n) = (m'm, n'n)$.
    - Let $\mathbf{2}$ be the category of the poset $\{0 \le 1\}$: two objects, one non-identity arrow $u \colon 0 \to 1$. Then $\mathbf{2} \times \mathbf{2}$ has four objects and $3 \times 3 = 9$ arrows: four identities, the four sides of a square, and the diagonal $(u, u)$. It is drawn below. Both ways round the square compose to the diagonal: $(u, 1_1) \circ (1_0, u) = (u \circ 1_0, 1_1 \circ u) = (u, u) = (1_1 \circ u, u \circ 1_0) = (1_1, u) \circ (u, 1_0)$.

    **Non-example.** The square with its four objects, four identities and four sides but *without* the diagonal is not a category: the composable pair $(1_0, u)$ then $(u, 1_1)$ would have no composite. And the arrows of $\mathcal{A} \times \mathcal{B}$ are not "arrows of $\mathcal{A}$ together with arrows of $\mathcal{B}$": if $\mathcal{A}$ has $m$ arrows and $\mathcal{B}$ has $n$, the product has $mn$ arrows, not $m + n$.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "00": (0, 2.4, "$(0,0)$"), "10": (3, 2.4, "$(1,0)$"),
            "01": (0, 0, "$(0,1)$"), "11": (3, 0, "$(1,1)$"),
        },
        [
            ("00", "10", "$(u, 1_0)$"),
            ("00", "01", r"$(1_0, u)\qquad\quad$", {"side": -1}),
            ("10", "11", r"$\qquad\quad(1_1, u)$"),
            ("01", "11", "$(u, 1_1)$", {"side": -1}),
            ("00", "11", "$(u, u)$", {"color": "#b45309"}),
        ],
        figsize=(5.4, 4.0),
        title=r"$\mathbf{2} \times \mathbf{2}$ (identities omitted)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Groupoids

    In a group, every element has an inverse. The many-object version of that condition:

    > **Definition (groupoid).** A **groupoid** is a category in which every arrow is an isomorphism.

    **Reading the definition.** To prove a category is a groupoid: (1) take an arbitrary arrow $f \colon A \to B$; (2) produce $g \colon B \to A$; (3) check $g \circ f = 1_A$ and $f \circ g = 1_B$. To prove it is not a groupoid, find one arrow with no inverse.

    > **Proposition 6.1.** Let $M$ be a monoid, regarded as a one-object category. Then that category is a groupoid if and only if $M$ is a group.

    **Goal.** "Every arrow $\star \to \star$ is an isomorphism" holds if and only if "every element of $M$ has a two-sided inverse in $M$".

    **Given.** Proposition 4.1 of 1A: arrows are elements of $M$, composition is multiplication, $1_\star = e$. A group is a monoid in which for every $m$ there is $n$ with $nm = e = mn$.

    **Plan.** Unpack both definitions and compare.

    **Proof.** Let $m \in M$. As an arrow $\star \to \star$, $m$ is an isomorphism exactly when there is an arrow $n \colon \star \to \star$ with $n \circ m = 1_\star$ and $m \circ n = 1_\star$. Arrows $\star \to \star$ are elements of $M$, $\circ$ is the multiplication and $1_\star = e$, so this says: there is $n \in M$ with $nm = e$ and $mn = e$. That is the statement that $m$ has an inverse in $M$. So "every arrow is an isomorphism" and "every element has an inverse" are the same condition. $\blacksquare$

    **What made it work.** The dictionary of 1A turns a definition about arrows into a definition about elements of a monoid. So a group *is* a one-object groupoid, and Proposition 1.1 specialises to the fact that inverses in a group are unique.

    **More examples.**

    - Every discrete category is a groupoid: its only arrows are identities, and identities are isomorphisms.
    - For any object $A$ of any category, the isomorphisms $A \to A$ are called the **automorphisms** of $A$. Exercise P05 shows that the isomorphisms of a category are closed under composition and inverses; it follows that the automorphisms of $A$ form a group, $\mathrm{Aut}(A)$.

    **Non-examples.**

    - $(\mathbb{N}, +, 0)$ as a one-object category is not a groupoid: the arrow $1$ has no inverse, because no natural number $n$ satisfies $n + 1 = 0$.
    - The category $\mathbf{2}$ is not a groupoid: there is no arrow $1 \to 0$ at all, so $u \colon 0 \to 1$ has no inverse.
    - $\mathbf{Set}$ is not a groupoid: a non-bijective function is not an isomorphism.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Classifying the Arrows of a Finite Category

    In a finite category, "for every object $C$ and every pair $g, h$" is a finite search, so monic, epic and isomorphism can all be decided by machine. Choose a category below. For each arrow the table says whether it is monic, epic and an isomorphism, and when it fails to be monic or epic it shows a witness: a pair $g \neq h$ that $f$ fails to distinguish.

    The first category in the list is drawn here. It has two objects and arrows $s \colon A \to B$, $r \colon B \to A$ and $e \colon B \to B$, with $r \circ s = 1_A$ and $s \circ r = e$. Before you look at the table, predict: is $s$ monic? Is $r$ monic? Is $e$ either?
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (0, 0, "$A$"), "B": (3, 0, "$B$")},
        [
            ("A", "B", "$s$", {"rad": -0.3}),
            ("B", "A", "$r$", {"rad": -0.3}),
            ("B", "B", "$e$", {"loop": "right"}),
        ],
        figsize=(5.8, 2.8),
        title=r"A section and a retraction: $r \circ s = 1_A$ and $s \circ r = e$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    category_choice = mo.ui.dropdown(
        options=[
            "Section and retraction (s, r, e)",
            "Parallel pair f, g: A -> B",
            "Monoid (Z/4, x, 1)",
            "Monoid (Z/6, x, 1)",
            "Group (Z/3, +, 0)",
            "Poset: divisors of 12",
            "Two isomorphic objects",
        ],
        value="Section and retraction (s, r, e)",
        label="Category",
    )
    category_choice
    return (category_choice,)


@app.cell(hide_code=True)
def _(category_choice, mo):
    def _run(choice):
        def monoid(elements, op, unit):
            return {
                "objects": ["*"],
                "arrows": {str(_m): ("*", "*") for _m in elements},
                "identity": {"*": str(unit)},
                "compose": {(str(_g), str(_f)): str(op(_g, _f)) for _g in elements for _f in elements},
            }

        def poset(elements, leq):
            _arrows = {f"{_a}->{_b}": (_a, _b) for _a in elements for _b in elements if leq(_a, _b)}
            _comp = {}
            for _g, (_b, _c) in _arrows.items():
                for _f, (_a, _b2) in _arrows.items():
                    if _b2 == _b:
                        _comp[(_g, _f)] = f"{_a}->{_c}"
            return {"objects": list(elements), "arrows": _arrows,
                    "identity": {_a: f"{_a}->{_a}" for _a in elements}, "compose": _comp}

        _ids = {("1A", "1A"): "1A", ("1B", "1B"): "1B"}
        _cats = {
            "Section and retraction (s, r, e)": {
                "objects": ["A", "B"],
                "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "s": ("A", "B"), "r": ("B", "A"), "e": ("B", "B")},
                "identity": {"A": "1A", "B": "1B"},
                "compose": {
                    **_ids,
                    ("s", "1A"): "s", ("1B", "s"): "s", ("r", "1B"): "r", ("1A", "r"): "r",
                    ("e", "1B"): "e", ("1B", "e"): "e",
                    ("r", "s"): "1A", ("s", "r"): "e", ("e", "e"): "e", ("e", "s"): "s", ("r", "e"): "r",
                },
            },
            "Parallel pair f, g: A -> B": {
                "objects": ["A", "B"],
                "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "f": ("A", "B"), "g": ("A", "B")},
                "identity": {"A": "1A", "B": "1B"},
                "compose": {**_ids, ("f", "1A"): "f", ("1B", "f"): "f", ("g", "1A"): "g", ("1B", "g"): "g"},
            },
            "Monoid (Z/4, x, 1)": monoid(range(4), lambda _a, _b: (_a * _b) % 4, 1),
            "Monoid (Z/6, x, 1)": monoid(range(6), lambda _a, _b: (_a * _b) % 6, 1),
            "Group (Z/3, +, 0)": monoid(range(3), lambda _a, _b: (_a + _b) % 3, 0),
            "Poset: divisors of 12": poset([1, 2, 3, 4, 6, 12], lambda _a, _b: _b % _a == 0),
            "Two isomorphic objects": {
                "objects": ["A", "B"],
                "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "f": ("A", "B"), "g": ("B", "A")},
                "identity": {"A": "1A", "B": "1B"},
                "compose": {
                    **_ids,
                    ("f", "1A"): "f", ("1B", "f"): "f", ("g", "1B"): "g", ("1A", "g"): "g",
                    ("g", "f"): "1A", ("f", "g"): "1B",
                },
            },
        }
        _cat = _cats[choice]
        _arr, _comp, _one = _cat["arrows"], _cat["compose"], _cat["identity"]

        def mono_witness(f):
            _into = [_g for _g in _arr if _arr[_g][1] == _arr[f][0]]
            for _g in _into:
                for _h in _into:
                    if _g < _h and _arr[_g][0] == _arr[_h][0] and _comp[(f, _g)] == _comp[(f, _h)]:
                        return (_g, _h)
            return None

        def epi_witness(f):
            _out = [_g for _g in _arr if _arr[_g][0] == _arr[f][1]]
            for _g in _out:
                for _h in _out:
                    if _g < _h and _arr[_g][1] == _arr[_h][1] and _comp[(_g, f)] == _comp[(_h, f)]:
                        return (_g, _h)
            return None

        def two_sided_inverse(f):
            _dom, _cod = _arr[f]
            for _g in _arr:
                if _arr[_g] == (_cod, _dom) and _comp[(_g, f)] == _one[_dom] and _comp[(f, _g)] == _one[_cod]:
                    return _g
            return None

        _rows = ["| arrow $f$ | from, to | monic? | epic? | isomorphism? |", "|---|---|---|---|---|"]
        _both_not_iso = []
        for _f, (_dom, _cod) in _arr.items():
            _mw, _ew, _inv = mono_witness(_f), epi_witness(_f), two_sided_inverse(_f)
            _m = "yes" if _mw is None else "no: `" + _f + " . " + _mw[0] + " = " + _f + " . " + _mw[1] + "`"
            _e = "yes" if _ew is None else "no: `" + _ew[0] + " . " + _f + " = " + _ew[1] + " . " + _f + "`"
            _i = "no" if _inv is None else "yes, inverse `" + _inv + "`"
            _rows.append("| `" + _f + "` | `" + str(_dom) + "` to `" + str(_cod) + "` | " + _m + " | " + _e + " | " + _i + " |")
            if _mw is None and _ew is None and _inv is None:
                _both_not_iso.append("`" + _f + "`")
        _n_iso = sum(1 for _f in _arr if two_sided_inverse(_f) is not None)
        _summary = (
            "\n\n**Summary.** " + str(len(_cat["objects"])) + " object(s), " + str(len(_arr)) + " arrow(s), "
            + str(_n_iso) + " isomorphism(s). "
            + ("This category is a groupoid. " if _n_iso == len(_arr) else "This category is not a groupoid. ")
        )
        if _both_not_iso:
            _summary += "Monic and epic but **not** an isomorphism: " + ", ".join(_both_not_iso) + "."
        else:
            _summary += "Here every arrow that is both monic and epic happens to be an isomorphism."
        return "\n".join(_rows) + _summary

    _table = _run(category_choice.value)
    mo.md(_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to notice as you switch between categories:

    - **Section and retraction.** $s$ is monic but not epic, $r$ is epic but not monic, and $e$ is neither. None of the non-identity arrows is an isomorphism, even though $r \circ s = 1_A$: one of the two equations is not enough.
    - **Parallel pair.** $f$ and $g$ are monic and epic for a dull reason: there are no two different test arrows to compare. Neither is an isomorphism because there is no arrow $B \to A$ at all.
    - **The two monoids.** In these finite monoids the monic arrows, the epic arrows and the isomorphisms coincide. Compare with the infinite monoid $(\mathbb{N}, +, 0)$ from Section 2, where every arrow is monic and epic and only $0$ is an isomorphism.
    - **The poset.** Every arrow is monic and epic; only the identities are isomorphisms.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Checking one of the two inverse equations.** Showing $g \circ f = 1_A$ and concluding that $f$ is an isomorphism. *Diagnosis:* the definition has two equations in two different hom-sets; the arrows $s$ and $r$ of Section 7 satisfy one and not the other.
    2. **Proving monic by injectivity.** Writing "suppose $f(a) = f(a')$" in a general category. *Diagnosis:* there are no elements; a proof that $f$ is monic must begin "let $g, h \colon C \to A$ with $f \circ g = f \circ h$".
    3. **Assuming monic and epic gives an isomorphism.** *Diagnosis:* true in $\mathbf{Set}$, false in general (Proposition 2.2, and every non-identity arrow of a poset). To prove an arrow is an isomorphism you must produce its inverse.
    4. **Cancelling an arrow that is not known to be cancellable.** Passing from $f \circ g = f \circ h$ to $g = h$ with no reason. *Diagnosis:* that step *is* the statement "$f$ is monic"; either it is a hypothesis you can cite, or it needs its own proof.
    5. **Dualizing by guesswork.** Turning "if $g \circ f$ is monic then $f$ is monic" into "if $g \circ f$ is epic then $f$ is epic". *Diagnosis:* reversing arrows reverses the order of composition, so the roles of $f$ and $g$ swap (Corollary 4.3(b)). Write out the translation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why This Matters

    - **Isomorphism is the course's notion of sameness.** From 2C onwards, almost every major theorem ends "unique up to isomorphism": adjoints, representing objects, limits. The sandwich argument of Proposition 1.1 is the prototype for all of those uniqueness proofs.
    - In **1C** you will prove that functors carry isomorphisms to isomorphisms, which is how invariants work; 1C also defines contravariant functors as functors out of an opposite category.
    - **Product categories and opposites** are how functors of two variables are handled: the hom-sets $\mathcal{A}(A, B)$ depend on $A$ in one direction and on $B$ in the other, which 1C and Part 4 express using $\mathcal{A}^{\mathrm{op}} \times \mathcal{A}$.
    - **Duality halves the work** of Part 5: colimits are limits in the opposite category, sums are dual to products, and epics are characterised by the dual of the characterisation of monics. Leinster's own treatment of monics and epics appears there.
    - **4B** (Yoneda) rests on the idea in exercise P06: an arrow can be understood completely through what it does to the arrows composed with it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Each exercise has a skeleton with the scaffolding done and the essential lines left as `# TODO`. The cells run as shipped. Fill in the `...`, uncomment the `print` checks, and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: The opposite category

    Write `opposite(cat)`, returning the encoding of $\mathcal{A}^{\mathrm{op}}$: same objects, same arrow names, same identities, with every arrow's domain and codomain swapped and the composition table re-indexed according to the definition in Section 4. The test category is the section-and-retraction category of Section 7.
    """)
    return


@app.cell
def _():
    def _run():
        _cat = {
            "objects": ["A", "B"],
            "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "s": ("A", "B"), "r": ("B", "A"), "e": ("B", "B")},
            "identity": {"A": "1A", "B": "1B"},
            "compose": {
                ("1A", "1A"): "1A", ("1B", "1B"): "1B",
                ("s", "1A"): "s", ("1B", "s"): "s", ("r", "1B"): "r", ("1A", "r"): "r",
                ("e", "1B"): "e", ("1B", "e"): "e",
                ("r", "s"): "1A", ("s", "r"): "e", ("e", "e"): "e", ("e", "s"): "s", ("r", "e"): "r",
            },
        }

        def opposite(cat):
            # TODO: swap domain and codomain of every arrow
            arrows = ...
            # TODO: the composite of g after f in the opposite is a composite in cat -- in which order?
            compose = ...
            return {"objects": list(cat["objects"]), "arrows": arrows,
                    "identity": dict(cat["identity"]), "compose": compose}

        _op = opposite(_cat)
        # print(_op["arrows"]["s"])                 # expect ('B', 'A')
        # print(_op["compose"][("s", "r")])         # expect 1A
        # print(_op["compose"][("r", "s")])         # expect e
        # print(len(_op["compose"]))                # expect 13
        # print(opposite(_op) == _cat)              # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: The product category

    Write `product(cat1, cat2)` following the definition in Section 5. Name the objects by tuples `(A, B)` and the arrows by tuples `(f, g)`. The tests use the category $\mathbf{2}$ and the section-and-retraction category.
    """)
    return


@app.cell
def _():
    def _run():
        _two = {
            "objects": ["0", "1"],
            "arrows": {"id0": ("0", "0"), "id1": ("1", "1"), "u": ("0", "1")},
            "identity": {"0": "id0", "1": "id1"},
            "compose": {("id0", "id0"): "id0", ("id1", "id1"): "id1", ("u", "id0"): "u", ("id1", "u"): "u"},
        }
        _retract = {
            "objects": ["A", "B"],
            "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "s": ("A", "B"), "r": ("B", "A"), "e": ("B", "B")},
            "identity": {"A": "1A", "B": "1B"},
            "compose": {
                ("1A", "1A"): "1A", ("1B", "1B"): "1B",
                ("s", "1A"): "s", ("1B", "s"): "s", ("r", "1B"): "r", ("1A", "r"): "r",
                ("e", "1B"): "e", ("1B", "e"): "e",
                ("r", "s"): "1A", ("s", "r"): "e", ("e", "e"): "e", ("e", "s"): "s", ("r", "e"): "r",
            },
        }

        def product(cat1, cat2):
            objects = [(_A, _B) for _A in cat1["objects"] for _B in cat2["objects"]]
            # TODO: arrows[(f, g)] = ((dom f, dom g), (cod f, cod g))
            arrows = ...
            # TODO: identity[(A, B)] = the pair of identities
            identity = ...
            # TODO: compose[((f2, g2), (f1, g1))] = (f2∘f1, g2∘g1), whenever both composites exist
            compose = ...
            return {"objects": objects, "arrows": arrows, "identity": identity, "compose": compose}

        _sq = product(_two, _two)
        # print(len(_sq["objects"]), len(_sq["arrows"]), len(_sq["compose"]))     # expect 4 9 16
        # print(_sq["arrows"][("u", "u")])                                        # expect (('0', '0'), ('1', '1'))
        # print(_sq["compose"][(("u", "id1"), ("id0", "u"))])                     # expect ('u', 'u')
        # print(_sq["compose"][(("id1", "u"), ("u", "id0"))])                     # expect ('u', 'u')
        _big = product(_retract, _two)
        # print(len(_big["objects"]), len(_big["arrows"]), len(_big["compose"]))  # expect 4 15 52

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Dividing one arrow by another

    Write `divide_after(cat, f, h)`, the sorted list of all arrows $g$ for which $g \circ f$ is defined and equals $h$, and `divide_before(cat, f, h)`, the sorted list of all arrows $g$ for which $f \circ g$ is defined and equals $h$. A left inverse of $f$ is the special case $h = 1_{\mathrm{dom} f}$ of the first. Then read the output against Section 2: what does a list of length two say about whether $f$ is monic, or epic?
    """)
    return


@app.cell
def _():
    def _run():
        _retract = {
            "objects": ["A", "B"],
            "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "s": ("A", "B"), "r": ("B", "A"), "e": ("B", "B")},
            "identity": {"A": "1A", "B": "1B"},
            "compose": {
                ("1A", "1A"): "1A", ("1B", "1B"): "1B",
                ("s", "1A"): "s", ("1B", "s"): "s", ("r", "1B"): "r", ("1A", "r"): "r",
                ("e", "1B"): "e", ("1B", "e"): "e",
                ("r", "s"): "1A", ("s", "r"): "e", ("e", "e"): "e", ("e", "s"): "s", ("r", "e"): "r",
            },
        }
        _z6 = {
            "objects": ["*"],
            "arrows": {str(_m): ("*", "*") for _m in range(6)},
            "identity": {"*": "1"},
            "compose": {(str(_g), str(_f)): str((_g * _f) % 6) for _g in range(6) for _f in range(6)},
        }

        def divide_after(cat, f, h):
            # TODO: the sorted names of all arrows g such that g∘f is defined and equals h
            return ...

        def divide_before(cat, f, h):
            # TODO: the sorted names of all arrows g such that f∘g is defined and equals h
            return ...

        # print(divide_after(_retract, "s", "1A"), divide_before(_retract, "s", "1B"))   # expect ['r'] []
        # print(divide_after(_retract, "s", "s"), divide_before(_retract, "s", "s"))     # expect ['1B', 'e'] ['1A']
        # print(divide_after(_retract, "r", "r"), divide_before(_retract, "r", "r"))     # expect ['1A'] ['1B', 'e']
        # print(divide_after(_retract, "e", "e"), divide_before(_retract, "e", "e"))     # expect ['1B', 'e'] ['1B', 'e']
        # print(divide_after(_z6, "2", "4"), divide_after(_z6, "2", "3"))                # expect ['2', '5'] []
        # print(divide_after(_z6, "5", "4"))                                             # expect ['2']
        # print([_f for _f in _z6["arrows"] if divide_after(_z6, _f, "1")])              # expect ['1', '5']

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six briefs, each with a statement, what you may assume, what a complete proof must show, and hints that open one at a time. There are no solutions anywhere in the repository.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | Isomorphisms in a preorder and in a poset — `exercises/1b/p01_isomorphisms_in_a_preorder.md` | warm-up | unpacking a definition |
    | P02 | The product of two categories is a category — `exercises/1b/p02_product_category.md` | warm-up | verifying axioms componentwise |
    | P03 | Epic in Set means surjective — `exercises/1b/p03_epics_in_set.md` | core | choosing a test object; contrapositive |
    | P04 | A one-sided inverse and a cancellation property give an isomorphism — `exercises/1b/p04_split_monics_and_epics.md` | core | cancellation; dualizing a proof |
    | P05 | The isomorphisms of a category form a groupoid — `exercises/1b/p05_isomorphisms_form_a_groupoid.md` | core | producing inverses; verifying axioms |
    | P06 | Isomorphisms are detected by composition — `exercises/1b/p06_isomorphisms_via_composition.md` | stretch | choosing where to evaluate a "for all" hypothesis |

    **Submitting a proof.** Write your proof in `proofs/1b/pNN_<slug>.md` (same filename as the brief), then ask Claude to review it. The review points at gaps and asks questions; it does not supply a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [1A: Categories](../1a_categories/) &nbsp;|&nbsp; Next: [1C: Functors](../1c_functors/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
