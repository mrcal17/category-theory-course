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
    # 1A: Categories

    > *A category is a collection of things, a collection of arrows between them, and a way of composing arrows that is associative and has identities. Nothing more is assumed.*
    > — the definition, before the fine print

    You have met groups and homomorphisms, vector spaces and linear maps, topological spaces and continuous maps. Each time, the pattern was the same: a kind of *thing*, a kind of *map* between things, a way to *compose* two maps when the first ends where the second begins, and an *identity* map on each thing. This module turns that pattern into a definition. The question it answers is: **what exactly is the common structure, and what do you have to check to claim that something has it?**

    The definition of a category is short, and almost nothing follows from it alone. Its value is as a checklist. To prove "these things and these maps form a category" you will always verify the same four items, and to prove a statement about *all* categories you may use only what the definition grants: composition, associativity, identities. In particular you may not assume an arrow is a function. Two of this module's main examples, a monoid and a poset, are categories whose arrows are not functions at all, and they will be test cases for every later idea in the course.

    By the end you will be able to prove that a given collection of objects and arrows is a category (or exhibit the axiom that fails), translate between "monoid" and "category with one object" and between "preorder" and "category with at most one arrow between any two objects", and check any finite candidate by machine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Definition

    Take the pattern from the introduction and keep only what was common to every instance.

    > **Definition (category).** A **category** $\mathcal{A}$ consists of
    >
    > - a collection $\mathrm{ob}(\mathcal{A})$ of **objects**;
    > - for each pair of objects $A, B$, a collection $\mathcal{A}(A, B)$ of **arrows** (also called **maps** or **morphisms**) from $A$ to $B$;
    > - for each triple of objects $A, B, C$, a function
    >   $$\mathcal{A}(B, C) \times \mathcal{A}(A, B) \to \mathcal{A}(A, C), \qquad (g, f) \mapsto g \circ f,$$
    >   called **composition**;
    > - for each object $A$, an arrow $1_A \in \mathcal{A}(A, A)$, called the **identity** on $A$;
    >
    > such that the following axioms hold:
    >
    > - **associativity:** for all objects $A, B, C, D$ and all $f \in \mathcal{A}(A, B)$, $g \in \mathcal{A}(B, C)$, $h \in \mathcal{A}(C, D)$,
    >   $$(h \circ g) \circ f = h \circ (g \circ f);$$
    > - **identity laws:** for all objects $A, B$ and all $f \in \mathcal{A}(A, B)$,
    >   $$f \circ 1_A = f = 1_B \circ f.$$

    We write $f \colon A \to B$ or $A \xrightarrow{f} B$ to mean $f \in \mathcal{A}(A, B)$, and call $A$ the **domain** and $B$ the **codomain** of $f$. Every arrow has exactly one domain and exactly one codomain. The composite $g \circ f$ is read "$g$ after $f$" and is often written $gf$. Leinster says "map" where this course mostly says "arrow"; they mean the same thing.

    **Reading the definition.** To show that some data form a category you must supply four things and verify four things.

    *Supply:*
    1. what the objects are;
    2. for each pair of objects $A, B$, what the arrows $A \to B$ are;
    3. a rule that, for every $f \colon A \to B$ and $g \colon B \to C$, produces one arrow $g \circ f$;
    4. for every object $A$, one chosen arrow $1_A$.

    *Verify:*
    1. **Composition lands in the right place:** $g \circ f$ really is one of the arrows $A \to C$ you declared in step 2. (This is the part hidden inside the phrase "a function $\mathcal{A}(B,C) \times \mathcal{A}(A,B) \to \mathcal{A}(A,C)$".)
    2. **Identities are arrows:** $1_A$ really is one of the arrows $A \to A$ you declared.
    3. **Associativity**, for every composable triple.
    4. **Both identity laws**, for every arrow.

    Notice what the definition does *not* say. It does not say objects are sets, that arrows are functions, or that an arrow can be applied to an element. Composition is defined **only** for pairs where the codomain of the first arrow equals the domain of the second: there is no $g \circ f$ for $f \colon A \to B$ and $g \colon B' \to C$ with $B' \neq B$.

    The picture below shows the associativity axiom. There are two ways to get a single arrow $A \to D$ out of $f$, $g$, $h$: go round the top, composing $h$ with $g \circ f$, or round the bottom, composing $h \circ g$ with $f$. The axiom says they agree, which is why you may write $h \circ g \circ f$ with no brackets.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (0, 0, "$A$"), "B": (2, 0, "$B$"), "C": (4, 0, "$C$"), "D": (6, 0, "$D$")},
        [
            ("A", "B", "$f$"),
            ("B", "C", "$g$"),
            ("C", "D", "$h$"),
            ("A", "C", r"$g \circ f$", {"rad": -0.28, "color": "#b45309"}),
            ("B", "D", r"$h \circ g$", {"rad": 0.28, "color": "#1d4ed8"}),
        ],
        figsize=(7.4, 2.6),
        title=r"Associativity: $h \circ (g \circ f) = (h \circ g) \circ f$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Categories of Sets with Structure

    The examples that motivated the definition all have the same form: objects are sets carrying some structure, arrows are the functions that respect it, composition is composition of functions, and the identity arrow is the identity function.

    | Category | Objects | Arrows | Composition |
    |---|---|---|---|
    | $\mathbf{Set}$ | sets | functions | composition of functions |
    | $\mathbf{Grp}$ | groups | group homomorphisms | composition of functions |
    | $\mathbf{Ab}$ | abelian groups | group homomorphisms | composition of functions |
    | $\mathbf{Vect}_k$ | vector spaces over a field $k$ | $k$-linear maps | composition of functions |
    | $\mathbf{Top}$ | topological spaces | continuous maps | composition of functions |

    For $\mathbf{Set}$, the four verifications are facts about functions from 0B: the composite of a function $A \to B$ with a function $B \to C$ is a function $A \to C$; composition of functions is associative, because both $(h \circ g) \circ f$ and $h \circ (g \circ f)$ send $a$ to $h(g(f(a)))$; and $f \circ 1_A = f = 1_B \circ f$ because $1_A(a) = a$.

    For the others, associativity and the identity laws come for free, because composition and identities are those of $\mathbf{Set}$ and two homomorphisms are equal exactly when they are equal as functions. What is **not** free is items 1 and 2 of the checklist: that the composite of two structure-respecting functions respects the structure, and that the identity function does. Here is that verification for groups, in the proof-anatomy form used throughout the course.

    > **Proposition 2.1.** Groups and group homomorphisms, with composition of functions and identity functions, form a category $\mathbf{Grp}$.

    **Goal.** (i) For all groups $G, H, K$ and all homomorphisms $\varphi \colon G \to H$ and $\psi \colon H \to K$, the function $\psi \circ \varphi \colon G \to K$ is a homomorphism. (ii) For every group $G$, the identity function $1_G$ is a homomorphism. (iii) Associativity and the identity laws hold.

    **Given.** A function $\varphi \colon G \to H$ between groups is a homomorphism when $\varphi(xy) = \varphi(x)\varphi(y)$ for all $x, y \in G$. We also have the facts about composition of functions listed above.

    **Plan.** Direct proof by unpacking the definition of homomorphism for (i) and (ii); for (iii), inherit from $\mathbf{Set}$.

    **Proof.**
    (i) Let $x, y \in G$. Then
    $$(\psi \circ \varphi)(xy) = \psi(\varphi(xy)) = \psi(\varphi(x)\varphi(y)) = \psi(\varphi(x))\,\psi(\varphi(y)) = (\psi \circ \varphi)(x)\,(\psi \circ \varphi)(y).$$
    The first and last equalities are the definition of composition of functions; the second holds because $\varphi$ is a homomorphism; the third holds because $\psi$ is a homomorphism, applied to the elements $\varphi(x), \varphi(y)$ of $H$. So $\psi \circ \varphi$ is a homomorphism.

    (ii) Let $x, y \in G$. Then $1_G(xy) = xy = 1_G(x)\,1_G(y)$, by the definition of the identity function used three times.

    (iii) Let $\varphi, \psi, \chi$ be composable homomorphisms. As functions, $(\chi \circ \psi) \circ \varphi = \chi \circ (\psi \circ \varphi)$ and $\varphi \circ 1_G = \varphi = 1_H \circ \varphi$, by the corresponding facts in $\mathbf{Set}$. Two homomorphisms that are equal as functions are equal as arrows of $\mathbf{Grp}$, so the axioms hold. $\blacksquare$

    **What made it work.** The axioms that look hardest (associativity, identity laws) cost nothing, because they were inherited from functions. The real content was **closure**: the composite is again an arrow of the permitted kind, and so is the identity. Whenever a category is defined as "sets with structure and structure-respecting functions", closure is the thing to prove.

    The same argument, with "respects multiplication" replaced by "is linear" or "is continuous", gives $\mathbf{Ab}$, $\mathbf{Vect}_k$ and $\mathbf{Top}$. Each one needs its own closure check. For monoids and monoid homomorphisms the closure check is Proposition 3 of 0C, so $\mathbf{Mon}$ is a category too. Exercise P01 asks you to carry out the whole verification for a category you have not met yet.

    **A non-example.** Take sets as objects and *non-injective* functions as arrows, with the usual composition. This is not a category. Let $A = \{\ast\}$ be a one-element set. Every function $A \to A$ is injective, so there are no arrows $A \to A$ at all, and so there is nothing that could serve as $1_A$. Item 4 of "supply" cannot be met.

    **A second non-example.** Take sets as objects, functions as arrows and the usual composition, but for the two-element set $A = \{0, 1\}$ declare the "identity" to be the constant function $c \colon A \to A$ with value $0$. The identity law demands $f \circ c = f$ for every $f \colon A \to A$. Take $f$ to be the function that swaps $0$ and $1$: then $(f \circ c)(1) = f(0) = 1$ but $f(1) = 0$, so $f \circ c \neq f$. The choice of identity arrow is part of the data, and a wrong choice breaks the axioms; you will prove in P03 that there is never a second correct choice.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Hom-Sets, and a Word about Size

    The collection $\mathcal{A}(A, B)$ of all arrows from $A$ to $B$ is called a **hom-set** (after "homomorphism"). Other books write $\mathrm{Hom}_{\mathcal{A}}(A, B)$ or $\mathrm{Hom}(A, B)$. Much of this course consists of studying an object by studying the hom-sets into it and out of it, so it is worth getting used to thinking of $\mathcal{A}(A, B)$ as a thing in its own right.

    > **Definition (hom-set).** For objects $A, B$ of a category $\mathcal{A}$, the **hom-set** $\mathcal{A}(A, B)$ is the collection of all arrows of $\mathcal{A}$ with domain $A$ and codomain $B$.

    **Reading the definition.** To describe a hom-set you must say (1) which category you are in, (2) which object is the domain and which is the codomain, in that order, and (3) list or count the arrows. The same pair of objects can have very different hom-sets in different categories.

    **Examples.**

    - In $\mathbf{Set}$, if $A$ has $m$ elements and $B$ has $n$ elements, then $\mathbf{Set}(A, B)$ has $n^m$ elements: a function is a choice of one of $n$ values for each of $m$ inputs. The code cell below confirms this by listing them.
    - In $\mathbf{Vect}_k$, once bases are chosen, $\mathbf{Vect}_k(k^n, k^m)$ corresponds to the set of $m \times n$ matrices over $k$.
    - In $\mathbf{Grp}$, a homomorphism $\varphi \colon \mathbb{Z}/2 \to \mathbb{Z}$ must send the generator to an element $x$ with $x + x = 0$, so $x = 0$. Hence $\mathbf{Grp}(\mathbb{Z}/2, \mathbb{Z})$ has exactly one element, although $\mathbf{Set}(\mathbb{Z}/2, \mathbb{Z})$ is infinite.

    **Non-example.** "The set of functions between $A$ and $B$" is not a hom-set until you say which way they go: $\mathbf{Set}(A, B)$ and $\mathbf{Set}(B, A)$ are different sets. If $A = \emptyset$ and $B = \{\ast\}$, the first has one element (the empty function) and the second has none.

    Two conventions about hom-sets:

    - **Different hom-sets share no arrows.** An arrow knows its domain and codomain. The inclusion $\mathbb{Z} \to \mathbb{Q}$ and the inclusion $\mathbb{Z} \to \mathbb{R}$ are different arrows of $\mathbf{Set}$, although they have the same values, because their codomains differ.
    - **Size.** The definition says "collection", not "set", because the objects of $\mathbf{Set}$ do not form a set (3A explains why). In every category this course works with, each individual $\mathcal{A}(A, B)$ *is* a set, and we will use that freely. Until 3A, nothing depends on the distinction.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf) (remarks on size).
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(dom, cod):
            return [dict(zip(dom, _vals)) for _vals in itertools.product(cod, repeat=len(dom))]

        _A = ["a1", "a2", "a3"]
        _B = ["x", "y"]
        _empty = []
        _point = ["*"]
        print("=== Hom-sets in Set, by listing every function ===")
        print(f"  |Set(A, B)| with |A|=3, |B|=2 : {len(all_functions(_A, _B))}   (2^3)")
        print(f"  |Set(B, A)| with |A|=3, |B|=2 : {len(all_functions(_B, _A))}   (3^2)")
        print(f"  |Set(empty, point)|           : {len(all_functions(_empty, _point))}   (the empty function)")
        print(f"  |Set(point, empty)|           : {len(all_functions(_point, _empty))}   (no functions at all)")
        print(f"  |Set(empty, empty)|           : {len(all_functions(_empty, _empty))}   (the identity on the empty set)")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. A Monoid Is a Category with One Object

    Now the first example in which arrows are not functions. Recall from 0C that a **monoid** is a set $M$ with an associative binary operation and a two-sided unit $e$. A group is a monoid in which every element has an inverse.

    Look again at the definition of a category and suppose there is only one object, say $\star$. Then there is only one hom-set, $\mathcal{A}(\star, \star)$; every pair of arrows is composable; and there is one identity. The axioms say composition is associative and $1_\star$ is a two-sided unit. That is the definition of a monoid, word for word.

    > **Proposition 4.1.** (a) Let $\mathcal{A}$ be a category with exactly one object $\star$. Then the set $M = \mathcal{A}(\star, \star)$, with operation $(g, f) \mapsto g \circ f$ and unit $1_\star$, is a monoid.
    > (b) Let $(M, \cdot, e)$ be a monoid. Then there is a category with exactly one object $\star$, with $\mathcal{A}(\star, \star) = M$, composition $g \circ f = g \cdot f$, and $1_\star = e$.

    **Goal.** (a) Show: for all $f, g, h \in M$, $(h \circ g) \circ f = h \circ (g \circ f)$; and for all $f \in M$, $f \circ 1_\star = f = 1_\star \circ f$; and $\circ$ is an operation on $M$, that is, $g \circ f \in M$ for all $f, g \in M$. (b) Show the four "verify" items of Section 1 for the stated data.

    **Given.** The definition of a category and the definition of a monoid. In (a), $\mathcal{A}(\star,\star)$ is assumed to be a set, as agreed in Section 3.

    **Plan.** Direct proof: write down each axiom of one structure and observe that it is an axiom of the other with the names changed. The only care needed is to check that every composite that the monoid axioms mention is defined in the category.

    **Proof.**
    (a) Let $f, g \in M$. Both are arrows $\star \to \star$, so the codomain of $f$ equals the domain of $g$ and the composite $g \circ f$ is defined; by the definition of composition it lies in $\mathcal{A}(\star, \star) = M$. So $\circ$ is a binary operation on $M$. Let $f, g, h \in M$. They form a composable triple $\star \to \star \to \star \to \star$, so the associativity axiom of $\mathcal{A}$ gives $(h \circ g) \circ f = h \circ (g \circ f)$. Finally, for $f \in M$ the identity laws of $\mathcal{A}$, with $A = B = \star$, give $f \circ 1_\star = f = 1_\star \circ f$. So $(M, \circ, 1_\star)$ is a monoid.

    (b) Objects: the single object $\star$. Arrows $\star \to \star$: the elements of $M$. Composition lands in the right place because $g \cdot f \in M$ for all $f, g \in M$ (a monoid operation is a function $M \times M \to M$). The identity $e$ is an element of $M$, hence an arrow $\star \to \star$. Associativity of $\circ$ is associativity of $\cdot$. The identity laws $f \cdot e = f = e \cdot f$ are the unit laws of the monoid. $\blacksquare$

    **What made it work.** With one object, the side condition "codomain of $f$ equals domain of $g$" is always satisfied, so composition becomes an everywhere-defined binary operation. A category is a "monoid with many objects": the same axioms, but composition is only partially defined.

    **Examples.**

    - $(\mathbb{N}, +, 0)$ gives a one-object category whose arrows are the natural numbers; composing the arrows $3$ and $4$ gives the arrow $7$, and the identity arrow is $0$.
    - The monoid $(\mathbb{Z}/4, \times, 1)$ gives a one-object category with four arrows $0, 1, 2, 3$, drawn below. The composite of the arrow $2$ with itself is the arrow $0$.
    - Every group, regarded as a monoid, gives a one-object category.

    In none of these is an arrow a function, and the object $\star$ has no elements. Asking "what does the arrow $3$ do to an element of $\star$?" has no answer.

    **Non-example.** The positive integers under addition are not a monoid (there is no unit), so they do not form a one-object category in this way: there is no arrow to serve as $1_\star$. The set $\{e, a, b\}$ with a multiplication table that has a unit but is not associative is likewise not a category; Section 7 lets you test such a table.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"*": (0, 0, r"$\star$")},
        [
            ("*", "*", "$1$", {"loop": "up"}),
            ("*", "*", "$2$", {"loop": "right"}),
            ("*", "*", "$0$", {"loop": "down"}),
            ("*", "*", "$3$", {"loop": "left"}),
        ],
        figsize=(3.4, 3.4),
        title=r"$(\mathbb{Z}/4, \times, 1)$ as a one-object category",
    )
    return


@app.cell
def _():
    def _run():
        _elements = [0, 1, 2, 3]
        print("=== Composition table of the one-object category (Z/4, x, 1) ===")
        print("  row g, column f, entry g∘f = g*f mod 4\n")
        print("    g\\f | " + "  ".join(str(_f) for _f in _elements))
        print("    ----+" + "-" * 11)
        for _g in _elements:
            print(f"     {_g}  | " + "  ".join(str((_g * _f) % 4) for _f in _elements))
        _assoc = all(
            ((_h * _g) % 4 * _f) % 4 == (_h * ((_g * _f) % 4)) % 4
            for _h in _elements for _g in _elements for _f in _elements
        )
        _unit = all((_f * 1) % 4 == _f == (1 * _f) % 4 for _f in _elements)
        print(f"\n  associativity holds for all 64 triples : {_assoc}")
        print(f"  1 is a two-sided identity              : {_unit}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. A Preorder Is a Category with at Most One Arrow Between Any Two Objects

    The monoid example had one object and many arrows. The opposite extreme has many objects and very few arrows.

    A **preorder** on a set $P$ is a relation $\le$ that is reflexive ($x \le x$ for all $x \in P$) and transitive (if $x \le y$ and $y \le z$ then $x \le z$). A **poset** (0C) is a preorder that is also antisymmetric (if $x \le y$ and $y \le x$ then $x = y$).

    > **Definition (the category of a preorder).** Let $(P, \le)$ be a preordered set. Its associated category, also written $P$, has
    >
    > - objects: the elements of $P$;
    > - arrows: for $x, y \in P$, the hom-set $P(x, y)$ has exactly one element, written $(x \le y)$, if $x \le y$, and is empty otherwise;
    > - composition: $(y \le z) \circ (x \le y) = (x \le z)$;
    > - identities: $1_x = (x \le x)$.

    **Reading the definition.** For this to make sense you must check: (1) the composite named in the third bullet exists, that is, whenever $x \le y$ and $y \le z$ there is an arrow $x \to z$; (2) the identity named in the fourth bullet exists; (3) associativity; (4) the identity laws.

    > **Proposition 5.1.** For every preordered set $(P, \le)$, the data above form a category.

    **Goal.** For all $x, y, z, w \in P$: (i) if $P(x, y)$ and $P(y, z)$ are non-empty then $P(x, z)$ is non-empty; (ii) $P(x, x)$ is non-empty; (iii) for all $f \in P(x,y)$, $g \in P(y,z)$, $h \in P(z,w)$, $(h \circ g) \circ f = h \circ (g \circ f)$; (iv) for all $f \in P(x, y)$, $f \circ 1_x = f = 1_y \circ f$.

    **Given.** $\le$ is reflexive and transitive. Each hom-set $P(x, y)$ has at most one element.

    **Plan.** Existence of composites and identities comes from transitivity and reflexivity. Each axiom is an equation between two arrows *in the same hom-set*, and a hom-set with at most one element cannot contain two different arrows.

    **Proof.**
    (i) Suppose $P(x, y)$ and $P(y, z)$ are non-empty. By the definition of the arrows, $x \le y$ and $y \le z$. By transitivity, $x \le z$, so $P(x, z)$ contains the arrow $(x \le z)$, and composition is defined.

    (ii) By reflexivity, $x \le x$, so $P(x, x)$ contains $(x \le x)$.

    (iii) Both $(h \circ g) \circ f$ and $h \circ (g \circ f)$ are arrows from $x$ to $w$, that is, elements of $P(x, w)$. That hom-set has at most one element. So the two arrows are equal.

    (iv) The arrows $f \circ 1_x$, $f$ and $1_y \circ f$ all lie in $P(x, y)$, which has at most one element. So they are equal. $\blacksquare$

    **What made it work.** *If a hom-set has at most one element, any two arrows in it are equal.* In a category coming from a preorder, every equation between arrows with the same domain and codomain holds automatically, so the only content is whether arrows *exist*. Reach for this whenever you work in a poset: "does this diagram commute?" is never the question, "is there an arrow?" always is.

    **Examples.**

    - $(\mathbb{Z}, \le)$: one arrow $m \to n$ exactly when $m \le n$.
    - The positive divisors of $6$ under divisibility: an arrow $a \to b$ exactly when $a$ divides $b$. All its arrows are drawn below, apart from the four identities.
    - The subsets of a set $S$ under inclusion: an arrow $U \to V$ exactly when $U \subseteq V$.

    **Non-example.** Take $\mathbb{Z}$ with the *strict* order: one arrow $m \to n$ exactly when $m < n$. There is no arrow $n \to n$, so no identities, so this is not a category.

    **Non-example, with proof.** Take the real numbers as objects and declare exactly one arrow $x \to y$ when $|x - y| \le 1$, and none otherwise.

    **Goal.** Show these data cannot be made into a category: there is no composition function satisfying the definition.

    **Given.** The definition requires, for all objects $x, y, z$, a function $\mathcal{A}(y, z) \times \mathcal{A}(x, y) \to \mathcal{A}(x, z)$.

    **Plan.** Counterexample: find one triple $x, y, z$ for which the domain of that function is non-empty and its codomain is empty.

    **Proof.** Take $x = 0$, $y = 1$, $z = 2$. Since $|0 - 1| = 1 \le 1$ and $|1 - 2| = 1 \le 1$, there is an arrow $f \colon 0 \to 1$ and an arrow $g \colon 1 \to 2$, so $\mathcal{A}(1, 2) \times \mathcal{A}(0, 1)$ contains the pair $(g, f)$. Since $|0 - 2| = 2 > 1$, the hom-set $\mathcal{A}(0, 2)$ is empty. A function must assign a value to $(g, f)$, and there is no value available. So no composition exists. $\blacksquare$

    **What made it work.** A universal claim ("for every composable pair there is a composite") is refuted by a single explicit instance. The relation here is reflexive and symmetric but not transitive, and transitivity is exactly what step (i) of Proposition 5.1 used.

    > Reference: [Leinster §1.1–1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"1": (2, 0, "$1$"), "2": (0, 1.6, "$2$"), "3": (4, 1.6, "$3$"), "6": (2, 3.2, "$6$")},
        [
            ("1", "2", r"$1 \mid 2$"),
            ("1", "3", r"$1 \mid 3$", {"side": -1}),
            ("2", "6", r"$2 \mid 6$"),
            ("3", "6", r"$3 \mid 6$", {"side": -1}),
            ("1", "6", r"$1 \mid 6$", {"color": "#b45309"}),
        ],
        figsize=(5.2, 4.6),
        title="Divisors of 6: both routes from 1 to 6 equal the one arrow $1 \\mid 6$",
    )
    return


@app.cell
def _():
    def _run():
        _divisors = [1, 2, 3, 4, 6, 12]
        print("=== Hom-set sizes in the divisibility order on the divisors of 12 ===")
        print("  entry in row a, column b = number of arrows a -> b  (1 if a divides b, else 0)\n")
        print("   a\\b | " + " ".join(f"{_b:>2}" for _b in _divisors))
        print("   ----+" + "-" * 19)
        for _a in _divisors:
            print(f"   {_a:>3} | " + " ".join(f"{int(_b % _a == 0):>2}" for _b in _divisors))
        _transitive = all(
            _c % _a == 0
            for _a in _divisors for _b in _divisors for _c in _divisors
            if _b % _a == 0 and _c % _b == 0
        )
        print(f"\n  every composable pair has a composite (transitivity): {_transitive}")
        print(f"  every object has an identity (reflexivity)          : {all(_a % _a == 0 for _a in _divisors)}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Discrete Categories and Other Very Small Categories

    The smallest possible supply of arrows is: identities and nothing else.

    > **Definition (discrete category).** A category is **discrete** if its only arrows are identities: for all objects $A \neq B$ the hom-set $\mathcal{A}(A, B)$ is empty, and for every object $A$, $\mathcal{A}(A, A) = \{1_A\}$.

    **Reading the definition.** To check a category is discrete: (1) pick an arbitrary arrow $f \colon A \to B$; (2) show $A = B$; (3) show $f = 1_A$.

    Any set $S$ gives a discrete category with object set $S$: composition has only the cases $1_A \circ 1_A = 1_A$, and the axioms reduce to that single equation. So a discrete category "is" a set. It is also the category of the preorder in which $x \le y$ means $x = y$.

    **Examples and non-examples.**

    - The **empty category** has no objects and no arrows. Every axiom starts "for all objects ..." and so holds vacuously. It is discrete.
    - The category with one object and one arrow (its identity) is discrete. It is also the one-object category of the one-element monoid.
    - The category with two objects $A, B$ and one non-identity arrow $f \colon A \to B$ (below, left) is **not** discrete. It is the category of the poset $\{0 \le 1\}$. The only composites are those forced by the identity laws: $f \circ 1_A = f$ and $1_B \circ f = f$.
    - Two objects and two **parallel** arrows $f, g \colon A \to B$ (below, right) form a category that is not discrete and does *not* come from a preorder, because $\mathcal{A}(A, B)$ has two elements.
    - A one-object category is discrete only when its monoid has one element. $(\mathbb{Z}/4, \times, 1)$ is not discrete.

    In the two pictures, identity arrows are omitted, which is the usual convention: every object has one, so drawing them adds no information.

    > Reference: [Leinster §1.1](https://arxiv.org/abs/1612.09375); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 0, "$A$"), "B": (2, 0, "$B$"),
            "A2": (4.2, 0, "$A$"), "B2": (6.2, 0, "$B$"),
        },
        [
            ("A", "B", "$f$"),
            ("A2", "B2", "$f$", {"rad": -0.35}),
            ("A2", "B2", "$g$", {"rad": 0.35}),
        ],
        figsize=(7.0, 2.4),
        title="One non-identity arrow (left); a parallel pair (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Finite Categories as Tables: the Validator

    A category with finitely many objects and arrows can be written down completely: list the objects, list the arrows with their domains and codomains, say which arrow is each identity, and give a **composition table**. Then every item of the checklist from Section 1 becomes a finite check, which a machine can do.

    Throughout the course, finite categories are stored in one fixed shape:

    ```python
    cat = {
        "objects": ["A", "B"],
        "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "f": ("A", "B")},   # name -> (domain, codomain)
        "identity": {"A": "1A", "B": "1B"},
        "compose": {("1B", "f"): "f", ("f", "1A"): "f", ("1A", "1A"): "1A", ("1B", "1B"): "1B"},
        # compose[(g, f)] = g∘f, defined exactly when cod(f) == dom(g)
    }
    ```

    The validator below reads the same information in a plain-text form and reports, in order, every way the candidate fails the definition:

    - `objects: A B` lists the objects;
    - `f: A -> B` declares an arrow;
    - `id A = 1A` says which arrow is the identity on `A`;
    - `g . f = h` is one line of the composition table: $g \circ f = h$.

    Pick a starting point, then edit the text. Things to try: delete a line of the composition table; change `a . e = a` to `a . e = e`; add an arrow `g: B -> A` to the first preset and see how many composites you are then obliged to define.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    preset_choice = mo.ui.dropdown(
        options=[
            "Valid: one arrow f: A -> B",
            "Valid: the monoid {e, a} with a.a = e",
            "Broken: a composite is missing",
            "Broken: the identity law fails",
            "Broken: associativity fails",
        ],
        value="Valid: one arrow f: A -> B",
        label="Start from",
    )
    preset_choice
    return (preset_choice,)


@app.cell(hide_code=True)
def _(mo, preset_choice):
    _presets = {
        "Valid: one arrow f: A -> B": "\n".join([
            "objects: A B",
            "1A: A -> A",
            "1B: B -> B",
            "f: A -> B",
            "id A = 1A",
            "id B = 1B",
            "1A . 1A = 1A",
            "1B . 1B = 1B",
            "f . 1A = f",
            "1B . f = f",
        ]),
        "Valid: the monoid {e, a} with a.a = e": "\n".join([
            "objects: *",
            "e: * -> *",
            "a: * -> *",
            "id * = e",
            "e . e = e",
            "e . a = a",
            "a . e = a",
            "a . a = e",
        ]),
        "Broken: a composite is missing": "\n".join([
            "objects: A B C",
            "1A: A -> A",
            "1B: B -> B",
            "1C: C -> C",
            "f: A -> B",
            "g: B -> C",
            "id A = 1A",
            "id B = 1B",
            "id C = 1C",
            "1A . 1A = 1A",
            "1B . 1B = 1B",
            "1C . 1C = 1C",
            "f . 1A = f",
            "1B . f = f",
            "g . 1B = g",
            "1C . g = g",
        ]),
        "Broken: the identity law fails": "\n".join([
            "objects: *",
            "e: * -> *",
            "a: * -> *",
            "id * = e",
            "e . e = e",
            "e . a = a",
            "a . e = e",
            "a . a = a",
        ]),
        "Broken: associativity fails": "\n".join([
            "objects: *",
            "e: * -> *",
            "a: * -> *",
            "b: * -> *",
            "id * = e",
            "e . e = e",
            "e . a = a",
            "e . b = b",
            "a . e = a",
            "b . e = b",
            "a . a = b",
            "a . b = a",
            "b . a = e",
            "b . b = a",
        ]),
    }
    table_input = mo.ui.text_area(
        value=_presets[preset_choice.value],
        rows=17,
        full_width=True,
        label="Candidate category (edit me)",
    )
    table_input
    return (table_input,)


@app.cell(hide_code=True)
def _(mo, table_input):
    def _run(text):
        _objects, _arrows, _identity, _compose, _bad = [], {}, {}, {}, []
        for _raw in text.splitlines():
            _line = _raw.strip()
            if not _line or _line.startswith("#"):
                continue
            if _line.startswith("objects:"):
                _objects += _line[len("objects:"):].split()
            elif _line.startswith("id ") and "=" in _line:
                _left, _right = _line[3:].split("=", 1)
                _identity[_left.strip()] = _right.strip()
            elif "->" in _line and ":" in _line:
                _name, _rest = _line.split(":", 1)
                _dom, _cod = _rest.split("->", 1)
                _arrows[_name.strip()] = (_dom.strip(), _cod.strip())
            elif " . " in _line and "=" in _line:
                _left, _right = _line.split("=", 1)
                _g, _f = _left.split(" . ", 1)
                _compose[(_g.strip(), _f.strip())] = _right.strip()
            else:
                _bad.append(_line)

        _problems = []
        for _line in _bad:
            _problems.append("**Could not read the line** `" + _line + "`.")
        for _name, (_dom, _cod) in _arrows.items():
            for _end in (_dom, _cod):
                if _end not in _objects:
                    _problems.append("**Arrow with an undeclared object:** `" + _name + "` mentions `" + _end + "`, which is not in the list of objects.")
        for _obj in _objects:
            if _obj not in _identity:
                _problems.append("**No identity supplied** for the object `" + _obj + "`.")
            elif _identity[_obj] not in _arrows:
                _problems.append("**Identity is not an arrow:** `" + _identity[_obj] + "` was named as the identity on `" + _obj + "` but was never declared.")
            elif _arrows[_identity[_obj]] != (_obj, _obj):
                _problems.append("**Identity in the wrong hom-set:** `" + _identity[_obj] + "` is not an arrow `" + _obj + " -> " + _obj + "`.")
        for _g in _arrows:
            for _f in _arrows:
                _composable = _arrows[_f][1] == _arrows[_g][0]
                if _composable and (_g, _f) not in _compose:
                    _problems.append("**Composition is not defined everywhere:** `" + _g + " . " + _f + "` is missing, although the codomain of `" + _f + "` is the domain of `" + _g + "`.")
                if not _composable and (_g, _f) in _compose:
                    _problems.append("**Composite of a non-composable pair:** `" + _g + " . " + _f + "` is given, but the codomain of `" + _f + "` is not the domain of `" + _g + "`.")
        for (_g, _f), _h in _compose.items():
            if _g not in _arrows or _f not in _arrows:
                _problems.append("**Table mentions an undeclared arrow** in `" + _g + " . " + _f + "`.")
            elif _h not in _arrows:
                _problems.append("**Composite is not an arrow:** `" + _g + " . " + _f + " = " + _h + "`, but `" + _h + "` was never declared.")
            elif _arrows[_f][1] == _arrows[_g][0] and _arrows[_h] != (_arrows[_f][0], _arrows[_g][1]):
                _problems.append("**Composite lands in the wrong hom-set:** `" + _g + " . " + _f + " = " + _h + "` should be an arrow `" + _arrows[_f][0] + " -> " + _arrows[_g][1] + "`.")

        _structural = len(_problems)
        _id_fail, _assoc_fail = [], []
        for _f, (_dom, _cod) in _arrows.items():
            _one_dom, _one_cod = _identity.get(_dom), _identity.get(_cod)
            if (_f, _one_dom) in _compose and _compose[(_f, _one_dom)] != _f:
                _id_fail.append("`" + _f + " . " + _one_dom + " = " + _compose[(_f, _one_dom)] + "`, but it should be `" + _f + "`")
            if (_one_cod, _f) in _compose and _compose[(_one_cod, _f)] != _f:
                _id_fail.append("`" + _one_cod + " . " + _f + " = " + _compose[(_one_cod, _f)] + "`, but it should be `" + _f + "`")
        for _h in _arrows:
            for _g in _arrows:
                for _f in _arrows:
                    if (_g, _f) in _compose and (_h, _g) in _compose:
                        _gf, _hg = _compose[(_g, _f)], _compose[(_h, _g)]
                        if (_h, _gf) in _compose and (_hg, _f) in _compose:
                            _lhs, _rhs = _compose[(_hg, _f)], _compose[(_h, _gf)]
                            if _lhs != _rhs:
                                _assoc_fail.append("`(" + _h + " . " + _g + ") . " + _f + " = " + _lhs + "` but `" + _h + " . (" + _g + " . " + _f + ") = " + _rhs + "`")
        for _item in _id_fail:
            _problems.append("**Identity law fails:** " + _item + ".")
        for _item in _assoc_fail[:6]:
            _problems.append("**Associativity fails:** " + _item + ".")
        if len(_assoc_fail) > 6:
            _problems.append("... and " + str(len(_assoc_fail) - 6) + " more associativity failures.")

        _n_pairs = sum(1 for _g in _arrows for _f in _arrows if _arrows[_f][1] == _arrows[_g][0])
        _summary = (
            "**Read:** " + str(len(_objects)) + " object(s), " + str(len(_arrows)) + " arrow(s), "
            + str(len(_compose)) + " table entries; " + str(_n_pairs) + " composable pairs need a composite.\n\n"
        )
        if not _problems:
            return _summary + "**Verdict: this is a category.** Composition is defined exactly on the composable pairs, every identity law holds, and every composable triple is associative."
        _verdict = "**Verdict: not a category.** " + str(len(_problems)) + " problem(s) found"
        if _structural:
            _verdict += " (fix the first " + str(_structural) + " before trusting the axiom checks)"
        return _summary + _verdict + ":\n\n" + "\n".join("- " + _p for _p in _problems)

    _report = _run(table_input.value)
    mo.md(_report)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two things to take from the validator.

    First, the order of its checks is the order of a proof. Before associativity can even be *stated* for a triple, the composites involved must exist and lie in the right hom-sets. A written proof that some data form a category should likewise establish "composition is defined and lands in the right place" before it touches the axioms.

    Second, the amount of checking grows quickly: a one-object category with $n$ arrows has $n^3$ associativity conditions. A proof by hand never checks cases one by one. It finds a *reason*: "inherited from functions" (Section 2), "this is the monoid axiom" (Section 4), "the hom-set has at most one element" (Section 5).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Applying an arrow to an element.** Writing "$f(a)$" in a proof about an arbitrary category. *Diagnosis:* objects of a general category have no elements (Sections 4 and 5); the only operations available are composition and identities.
    2. **Composing arrows that do not meet.** Writing $g \circ f$ without checking that the codomain of $f$ is the domain of $g$. *Diagnosis:* composition is a function on $\mathcal{A}(B,C) \times \mathcal{A}(A,B)$ only; before every composite, name the three objects.
    3. **Skipping closure.** Proving associativity and the identity laws for "homomorphisms" without first proving that a composite of homomorphisms is a homomorphism and that the identity function is one. *Diagnosis:* that is items 1 and 2 of the checklist, and in categories of structured sets it is the only part with content.
    4. **Checking one identity law.** Verifying $f \circ 1_A = f$ and stopping. *Diagnosis:* the definition demands both $f \circ 1_A = f$ and $1_B \circ f = f$; the "identity law fails" preset in Section 7 satisfies one and not the other.
    5. **Treating arrows with the same values as the same arrow.** *Diagnosis:* the domain and codomain are part of an arrow; the inclusions $\mathbb{Z} \to \mathbb{Q}$ and $\mathbb{Z} \to \mathbb{R}$ lie in different hom-sets, so they are different arrows of $\mathbf{Set}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why This Matters

    Everything else in the course is built from the four items of this definition.

    - **1B** asks which arrows behave like "the same thing in two guises" (isomorphisms) and like injections and surjections (monics and epics), using only composition, and shows that reversing all arrows of a category gives another category.
    - **1C** defines maps *between* categories. For one-object categories they turn out to be monoid homomorphisms; for posets, order-preserving maps. Propositions 4.1 and 5.1 are what make those statements meaningful.
    - **2A** on adjunctions takes its first examples from posets, where an adjunction is a Galois connection and every proof reduces to "is there an arrow?".
    - **4B**, the Yoneda lemma, becomes Cayley's theorem when read in a one-object category.
    - **5A–5B**: products and sums in a poset are meets and joins.

    Each time a new definition appears, the first two questions to ask are: what does it say in a monoid, and what does it say in a poset?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Each exercise has a skeleton with the scaffolding done and the essential lines left as `# TODO`. The cells run as shipped (they do nothing yet). Fill in the `...`, uncomment the `print` checks, and compare with the expected values in the comments.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: From a preorder to the encoding

    Write `preorder_to_category(elements, leq)`, which turns a finite preorder into the course's encoding, following the definition in Section 5. Name the unique arrow $x \to y$ by the string `"x->y"` (the helper `name` does this). The table entry `compose[(g, f)]` must exist exactly when the codomain of `f` equals the domain of `g`.
    """)
    return


@app.cell
def _():
    def _run():
        def name(x, y):
            return f"{x}->{y}"

        def preorder_to_category(elements, leq):
            # TODO: one arrow name(x, y) -> (x, y) for each pair with leq(x, y)
            arrows = ...
            # TODO: the identity on x is the arrow x -> x
            identity = ...
            # TODO: compose[(name(y, z), name(x, y))] = name(x, z) for every x <= y <= z
            compose = ...
            return {"objects": list(elements), "arrows": arrows, "identity": identity, "compose": compose}

        _divisors = [1, 2, 3, 4, 6, 12]
        _cat = preorder_to_category(_divisors, lambda a, b: b % a == 0)
        # print(len(_cat["objects"]))                    # expect 6
        # print(len(_cat["arrows"]))                     # expect 18
        # print(len(_cat["compose"]))                    # expect 40
        # print(_cat["compose"][("2->12", "1->2")])      # expect 1->12
        # print(("3->6", "1->2") in _cat["compose"])     # expect False (not composable)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Hom-sets and the monoid at an object

    Write `hom(cat, X, Y)`, returning the sorted list of names of the arrows $X \to Y$, and `endo_table(cat, X)`, returning the composition table restricted to $\mathcal{A}(X, X)$ as a dictionary `{(g, f): g∘f}`. By the argument of Proposition 4.1(a), applied to the arrows $X \to X$ only, that table is the multiplication table of a monoid. The test category has two objects and five arrows.
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

        def hom(cat, X, Y):
            # TODO: the sorted names of all arrows with domain X and codomain Y
            return ...

        def endo_table(cat, X):
            # TODO: {(g, f): cat["compose"][(g, f)]} for all g, f in hom(cat, X, X)
            return ...

        # print(hom(_cat, "A", "B"))                    # expect ['s']
        # print(hom(_cat, "B", "B"))                    # expect ['1B', 'e']
        # print({(X, Y): len(hom(_cat, X, Y)) for X in "AB" for Y in "AB"})
        #                                               # expect {('A','A'): 1, ('A','B'): 1, ('B','A'): 1, ('B','B'): 2}
        # print(endo_table(_cat, "B"))
        #     # expect {('1B','1B'): '1B', ('1B','e'): 'e', ('e','1B'): 'e', ('e','e'): 'e'}

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: How many one-object categories?

    By Proposition 4.1, a one-object category with arrow set $\{e, a\}$ and identity $e$ is a monoid structure on $\{e, a\}$ with unit $e$. The unit laws fix every product involving $e$, so the only freedom is the value of $a \cdot a$. With arrow set $\{e, a, b\}$ the free entries are $a \cdot a$, $a \cdot b$, $b \cdot a$, $b \cdot b$, giving $3^4 = 81$ candidate tables. Write `is_associative(table, elements)` and count how many candidates are monoids.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def candidate_tables(elements, unit):
            _others = [_x for _x in elements if _x != unit]
            _free = [(_x, _y) for _x in _others for _y in _others]
            for _values in itertools.product(elements, repeat=len(_free)):
                _table = dict(zip(_free, _values))
                for _x in elements:
                    _table[(unit, _x)] = _x
                    _table[(_x, unit)] = _x
                yield _table

        def is_associative(table, elements):
            # TODO: True exactly when table[(table[(x, y)], z)] == table[(x, table[(y, z)])]
            #       for all x, y, z in elements
            return ...

        def count_monoids(elements, unit):
            return sum(1 for _t in candidate_tables(elements, unit) if is_associative(_t, elements) is True)

        # print(count_monoids(["e", "a"], "e"))          # expect 2   (out of 2 candidates)
        # print(count_monoids(["e", "a", "b"], "e"))     # expect 11  (out of 81 candidates)

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
    | P01 | Sets over a fixed set form a category — `exercises/1a/p01_sets_over_a_fixed_set.md` | warm-up | verifying axioms (closure) |
    | P02 | A category with thin hom-sets is a preorder — `exercises/1a/p02_thin_categories_are_preorders.md` | warm-up | unpacking a definition |
    | P03 | Identities are unique — `exercises/1a/p03_identities_unique.md` | core | uniqueness argument |
    | P04 | Sets and relations form a category — `exercises/1a/p04_relations_form_a_category.md` | core | verifying axioms; equality of sets |
    | P05 | Four-fold composites need no brackets — `exercises/1a/p05_fourfold_composites.md` | core | chains of equalities justified by one axiom |
    | P06 | The quotient of a category by a congruence — `exercises/1a/p06_quotient_category.md` | stretch | well-definedness, then verifying axioms |

    **Submitting a proof.** Write your proof in `proofs/1a/pNN_<slug>.md` (same filename as the brief), then ask Claude to review it. The review points at gaps and asks questions; it does not supply a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [0C: Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher](../0c_proof_toolkit_uniqueness/) &nbsp;|&nbsp; Next: [1B: Isomorphisms, Duality & New Categories from Old](../1b_isomorphisms_duality/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
