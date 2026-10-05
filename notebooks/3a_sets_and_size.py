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
    # 3A: Sets & Size

    > *So far we have used sets without asking what we assume about them, and spoken of "the category of all sets" without asking whether there can be such a thing. This module asks.*

    Every example in Parts 1 and 2 leaned on the category $\mathbf{Set}$: hom-sets are sets, functors land in $\mathbf{Set}$, and adjunctions are bijections between sets. This interlude does two jobs before the Yoneda lemma puts even more weight on $\mathbf{Set}$.

    The first job is to list the constructions on sets that the rest of the course uses, and to describe each one *by the functions into or out of it*: the empty set and the one-element set, products and sums, sets of functions, subsets and the two-element set, equalizers and quotients. Each description is a small universal property, and the proofs are explicit bijections.

    The second job is about **size**. The collection of all sets is too big to be a set. That is a theorem, proved by the diagonal argument, and it forces a distinction between *small* categories, whose arrows form a set, and *large* ones like $\mathbf{Set}$ and $\mathbf{Grp}$. The distinction matters later: several theorems in Parts 4 to 6 are true only under a size hypothesis.

    **What you will be able to prove by the end.** You will be able to prove that two sets built by different constructions are in bijection by writing down a function each way and checking both composites; to run a diagonal argument; and to say precisely what "small", "locally small" and "essentially small" mean and why $\mathbf{Set}$ is none but the second. On foundations we follow Leinster: we say plainly what is being assumed, and we do not pretend to derive it from an axiom system.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. What We Assume, and the Two Smallest Sets

    We take for granted that there are **sets** and **functions** between them, and that functions compose associatively with identities, so that sets and functions form a category $\mathbf{Set}$. A function $f \colon A \to B$ assigns to each element of $A$ exactly one element of $B$; formally it is a subset $\Gamma \subseteq A \times B$ such that for each $a \in A$ there is exactly one $b \in B$ with $(a, b) \in \Gamma$. Two functions $A \to B$ are equal when they take the same value at every element of $A$ (0B).

    Beyond that we assume the constructions described in Sections 1 to 5 can always be carried out. We do not fix a formal axiom system. Leinster's point of view, which we adopt, is that what a mathematician actually uses about sets is a short list of properties of the *category* of sets, and that this list can itself be made into an axiomatisation; the details belong to a course on set theory, not this one.

    > **Definition.** The **empty set** $\emptyset$ is the set with no elements. A **one-element set** is a set with exactly one element; we fix one and call it $1 = \{\ast\}$.

    **Reading the definition.** The interesting content is in the maps:

    1. For every set $A$ there is exactly one function $\emptyset \to A$ (Proposition 1 below).
    2. For every set $A$ there is exactly one function $A \to 1$ (proved in 0A, Section 2).
    3. A function $1 \to A$ is the same thing as an element of $A$ (exercise P02).

    Items 1 and 2 say that $\emptyset$ is an **initial** object and $1$ a **terminal** object of $\mathbf{Set}$, in the language of 2A.

    **Proposition 1.** For every set $A$ there is exactly one function $\emptyset \to A$.

    - **Goal.** *Existence:* there is a function $\emptyset \to A$. *Uniqueness:* any two functions $f, g \colon \emptyset \to A$ are equal.
    - **Given.** The definition of a function as a subset of the product satisfying "for each element of the domain there is exactly one ..."; the criterion for equality of functions.
    - **Plan.** Existence and uniqueness, proved separately (0C). Both conditions quantify over the elements of $\emptyset$, of which there are none, so both hold vacuously.
    - **Proof.** *Existence.* The product $\emptyset \times A$ has no elements, so its only subset is $\Gamma = \emptyset$. The condition "for each $a \in \emptyset$ there is exactly one $b \in A$ with $(a, b) \in \Gamma$" is a statement about every element of $\emptyset$; there are no such elements, so there is nothing to check and the condition holds. So $\Gamma$ is a function $\emptyset \to A$. *Uniqueness.* Let $f, g \colon \emptyset \to A$. They are equal if $f(a) = g(a)$ for every $a \in \emptyset$. Again there is no $a$ to check. So $f = g$. $\blacksquare$
    - **What made it work.** A "for all $x \in X$" statement is true when $X$ is empty. Note that this proves there is exactly *one* function, not zero: the empty function exists.

    **Example.** There is exactly one function $\emptyset \to \emptyset$, namely the identity. So the number of functions from a $0$-element set to a $0$-element set is $1$.

    **Non-example.** If $A$ is non-empty there is **no** function $A \to \emptyset$: an element $a \in A$ would need a value in $\emptyset$. So $\emptyset$ is not terminal, and the situation is not symmetric.

    **Non-example.** The one-element set is not unique: $\{0\}$ and $\{1\}$ are different sets. But any two one-element sets are in bijection, and by exactly one bijection. "Unique up to unique isomorphism" (0C) is the only uniqueness these descriptions can give, and the only one we need.

    > Reference: [Leinster §3.1](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Products and Sums

    Two ways to combine sets $A$ and $B$: take pairs, or put the two sets side by side.

    > **Definition (product).** The **product** $A \times B$ is the set of ordered pairs $(a, b)$ with $a \in A$ and $b \in B$. It comes with the **projections** $p_1 \colon A \times B \to A$, $p_1(a, b) = a$, and $p_2 \colon A \times B \to B$, $p_2(a, b) = b$.
    >
    > **Definition (sum).** The **sum** (or disjoint union, or coproduct) $A + B$ is the set $(A \times \{1\}) \cup (B \times \{2\})$. It comes with the **inclusions** $i_1 \colon A \to A + B$, $i_1(a) = (a, 1)$, and $i_2 \colon B \to A + B$, $i_2(b) = (b, 2)$.

    **Reading the definitions.** What matters about each construction is how functions interact with it:

    1. *Into a product:* for every set $X$ and functions $f \colon X \to A$, $g \colon X \to B$ there is exactly one function $h \colon X \to A \times B$ with $p_1 \circ h = f$ and $p_2 \circ h = g$.
    2. *Out of a sum:* for every set $X$ and functions $f \colon A \to X$, $g \colon B \to X$ there is exactly one function $h \colon A + B \to X$ with $h \circ i_1 = f$ and $h \circ i_2 = g$.
    3. Every element of $A + B$ is $i_1(a)$ for a unique $a$ or $i_2(b)$ for a unique $b$, and never both. The tags $1$ and $2$ exist only to guarantee this.

    **Checking item 1.** *Existence:* define $h(x) = (f(x), g(x))$; then $p_1(h(x)) = f(x)$ and $p_2(h(x)) = g(x)$ for all $x$. *Uniqueness:* if $h'$ also satisfies the two equations, write $h'(x) = (a, b)$; then $a = p_1(h'(x)) = f(x)$ and $b = p_2(h'(x)) = g(x)$, so $h'(x) = h(x)$. In other words, composing with the projections is a bijection
    $$\mathbf{Set}(X, A \times B) \;\cong\; \mathbf{Set}(X, A) \times \mathbf{Set}(X, B).$$
    Item 2, in the form of a bijection of the same kind, is exercise P03.

    **Example.** If $A$ has $m$ elements and $B$ has $n$, then $A \times B$ has $mn$ elements and $A + B$ has $m + n$. The notation is chosen to make this true.

    **Example.** $A \times 1 \cong A$ via $p_1$, and $A + \emptyset \cong A$ via $i_1$; also $A \times \emptyset = \emptyset$.

    **Non-example (union is not sum).** Take $A = B = \{0\}$. The union $A \cup B = \{0\}$ has one element, but $A + B = \{(0,1), (0,2)\}$ has two. With the union, item 2 fails: for $X = \{\text{x}, \text{y}\}$, $f(0) = \text{x}$ and $g(0) = \text{y}$, no function $h \colon A \cup B \to X$ restricts to both $f$ and $g$. The union only behaves like the sum when $A$ and $B$ are disjoint.

    > Reference: [Leinster §3.1](https://arxiv.org/abs/1612.09375). Products and sums in a general category are the subject of 5A and 5B.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "X": (2.0, 2.0, r"$X$"),
            "P": (2.0, 0.0, r"$A \times B$"),
            "A": (0.0, 0.0, r"$A$"),
            "B": (4.0, 0.0, r"$B$"),
            # unlabelled anchor points, so that the projections clear the wide label of the product
            "P-": (1.55, 0.0, ""),
            "P+": (2.45, 0.0, ""),
        },
        [
            ("X", "A", r"$f$", {"side": -1}),
            ("X", "B", r"$g$"),
            ("X", "P", r"$\ \ h$", {"dashed": True}),
            ("P-", "A", r"$p_1$"),
            ("P+", "B", r"$p_2$", {"side": -1}),
        ],
        figsize=(5.2, 3.2),
        title=r"Exactly one $h$ makes both triangles commute",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Sets of Functions, and Currying

    The functions from one set to another themselves form a set. This is the construction that makes $\mathbf{Set}(A, B)$ an *object* of $\mathbf{Set}$ and not only a collection.

    > **Definition (function set).** For sets $A$ and $B$, the **function set** $B^A$ is the set of all functions from $A$ to $B$. So $B^A = \mathbf{Set}(A, B)$.

    **Reading the definition.**

    1. The exponent is the **domain**: $B^A$ is "functions *from* $A$ *to* $B$". The notation is chosen so that if $A$ has $m$ elements and $B$ has $n$, then $B^A$ has $n^m$ elements: a function is a choice of one of $n$ values for each of the $m$ elements of $A$.
    2. An element of $B^A$ is a whole function. To give a function *into* $B^A$ you must give, for each input, a function $A \to B$.

    **Example.** $B^1 \cong B$ (a function $1 \to B$ is an element of $B$) and $B^\emptyset$ has exactly one element (Proposition 1), matching $n^1 = n$ and $n^0 = 1$.

    **Non-example.** $\emptyset^A$ is empty when $A$ is non-empty, but $\emptyset^\emptyset$ has one element. The rule "$0^m = 0$" holds for $m \geq 1$ only, and $0^0 = 1$ here is a count, not a convention.

    A function of two variables $f \colon A \times B \to C$ can be read as a family of functions of one variable: fix $a$, and $f(a, -)$ is a function $B \to C$. This turns $f$ into a function from $A$ to $C^B$.

    **Proposition 2 (currying).** For all sets $A$, $B$, $C$ there is a bijection
    $$\boxed{\,\mathbf{Set}(A \times B, C) \;\cong\; \mathbf{Set}(A, C^B)\,}$$
    sending $f \colon A \times B \to C$ to the function $\bar f \colon A \to C^B$ defined by $\bar f(a)(b) = f(a, b)$.

    - **Goal.** The function $\Theta \colon \mathbf{Set}(A \times B, C) \to \mathbf{Set}(A, C^B)$, $\Theta(f) = \bar f$, is a bijection.
    - **Given.** The definitions of $A \times B$ and $C^B$; a function is a bijection if and only if it has a two-sided inverse (0B); two functions are equal when they agree at every element.
    - **Plan.** Write down a function $\Psi$ in the opposite direction and check that $\Psi \circ \Theta$ and $\Theta \circ \Psi$ are identities. Each check is an equality of functions, verified on elements.
    - **Proof.** First, $\bar f$ is well defined: for each $a \in A$, the rule $b \mapsto f(a, b)$ is a function $B \to C$, that is, an element of $C^B$. For the other direction, given $g \colon A \to C^B$ define $\Psi(g) = \hat g \colon A \times B \to C$ by $\hat g(a, b) = g(a)(b)$; this makes sense because $g(a)$ is a function $B \to C$ and $b \in B$.

      *$\Psi \circ \Theta$ is the identity.* Let $f \colon A \times B \to C$. For every $(a, b) \in A \times B$,
      $$\hat{\bar f}(a, b) = \bar f(a)(b) = f(a, b),$$
      by the definition of $\hat{\ }$ and then of $\bar{\ }$. So $\Psi(\Theta(f)) = f$.

      *$\Theta \circ \Psi$ is the identity.* Let $g \colon A \to C^B$. For every $a \in A$ and $b \in B$,
      $$\bar{\hat g}(a)(b) = \hat g(a, b) = g(a)(b).$$
      So for each $a$ the functions $\bar{\hat g}(a)$ and $g(a)$ agree at every $b$, hence are equal elements of $C^B$; and so $\bar{\hat g}$ and $g$ agree at every $a$, hence $\Theta(\Psi(g)) = g$. $\blacksquare$
    - **What made it work.** The standard way to prove a bijection: exhibit the inverse. When the sets involved are sets of functions, an equality has to be checked "all the way down", here at $a$ and then at $b$.

    For finite sets the proposition says $c^{\,ab} = (c^{\,b})^{a}$. If you have done Part 2 you will recognise the bijection, which is natural in $A$ and $C$, as the adjunction $(- \times B) \dashv (-)^B$ of 2A, with $\bar f$ the transpose of $f$. Nothing below depends on that.

    ### Explore: count, and watch the bijection

    Choose the sizes of $A$, $B$ and $C$. The cell lists the sizes of the constructed sets, then enumerates **every** function $A \times B \to C$, curries each one, and checks that the results are exactly the functions $A \to C^B$, each once. The last slider picks one $f$ to display next to $\bar f$.

    > Reference: [Leinster §3.1](https://arxiv.org/abs/1612.09375) (function sets and the bijection); [Leinster §2.1](https://arxiv.org/abs/1612.09375) for the adjunction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    size_a = mo.ui.slider(start=0, stop=3, step=1, value=2, label="|A|", show_value=True)
    size_b = mo.ui.slider(start=0, stop=3, step=1, value=2, label="|B|", show_value=True)
    size_c = mo.ui.slider(start=0, stop=3, step=1, value=2, label="|C|", show_value=True)
    which_f = mo.ui.slider(start=0, stop=40, step=1, value=6, label="which f to show", show_value=True)
    mo.vstack([mo.hstack([size_a, size_b, size_c], justify="start"), which_f])
    return size_a, size_b, size_c, which_f


@app.cell(hide_code=True)
def _(mo, size_a, size_b, size_c, which_f):
    def _run():
        import itertools

        _A = ["a" + str(_i + 1) for _i in range(size_a.value)]
        _B = ["b" + str(_i + 1) for _i in range(size_b.value)]
        _C = ["c" + str(_i + 1) for _i in range(size_c.value)]
        _pairs = [(_a, _b) for _a in _A for _b in _B]

        # every function A x B -> C, as a dictionary
        _fs = [dict(zip(_pairs, _vals)) for _vals in itertools.product(_C, repeat=len(_pairs))]

        def _curry(f):
            # f-bar as a tuple (indexed by A) of tuples (indexed by B)
            return tuple(tuple(f[(_a, _b)] for _b in _B) for _a in _A)

        _curried = [_curry(_f) for _f in _fs]
        # every function A -> C^B, in the same representation
        _all_g = set(itertools.product(itertools.product(_C, repeat=len(_B)), repeat=len(_A)))
        _injective = len(set(_curried)) == len(_curried)
        _onto = set(_curried) == _all_g

        _na, _nb, _nc = len(_A), len(_B), len(_C)
        _lines = [
            "| set | size | formula |",
            "|---|---|---|",
            "| $A \\times B$ | " + str(_na * _nb) + " | $ab$ |",
            "| $A + B$ | " + str(_na + _nb) + " | $a + b$ |",
            "| $B^A$ | " + str(_nb ** _na) + " | $b^a$ |",
            "| $C^B$ | " + str(_nc ** _nb) + " | $c^b$ |",
            "| $\\mathbf{Set}(A \\times B, C)$ | " + str(len(_fs)) + " | $c^{ab}$ |",
            "| $\\mathbf{Set}(A, C^B)$ | " + str(len(_all_g)) + " | $(c^b)^a$ |",
            "",
            "Currying is injective on these functions: **" + str(_injective)
            + "**. Every function $A \\to C^B$ is hit: **" + str(_onto) + "**.",
            "",
        ]
        if not _fs:
            _lines.append("There is no function $A \\times B \\to C$ here: $A \\times B$ is non-empty and $C$ is empty. Both sides of the bijection are empty.")
        elif not _pairs:
            _lines.append("$A \\times B$ is empty, so there is exactly one function $A \\times B \\to C$, the empty one. On the other side there is exactly one function $A \\to C^B$ as well. (Why? Treat $A = \\emptyset$ and $B = \\emptyset$ separately.)")
        else:
            _k = which_f.value % len(_fs)
            _f = _fs[_k]
            _lines.append("**Function number " + str(_k) + " of " + str(len(_fs)) + "**, as a table of values $f(a, b)$:")
            _lines.append("")
            _lines.append("| $f$ | " + " | ".join(_B) + " |")
            _lines.append("|---|" + "---|" * len(_B))
            for _a in _A:
                _lines.append("| " + _a + " | " + " | ".join(_f[(_a, _b)] for _b in _B) + " |")
            _lines.append("")
            _lines.append("and its curried form $\\bar f \\colon A \\to C^B$, which sends each $a$ to a *function* $B \\to C$ (a row of the table):")
            _lines.append("")
            for _a in _A:
                _lines.append("- $\\bar f($" + _a + "$)$ is the function " + ", ".join(_b + " $\\mapsto$ " + _f[(_a, _b)] for _b in _B))
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Things to try.** Set $|C| = 0$ with $|A|, |B| \geq 1$, and then set $|A| = 0$ as well: the count on both sides jumps from $0$ to $1$. Set $|B| = 0$ and explain why both sides have exactly one element whatever $A$ and $C$ are.

    ---

    ## 4. The Two-Element Set and Subsets

    > **Definition.** Fix a **two-element set** $2 = \{\mathrm{true}, \mathrm{false}\}$. For a set $A$ and a subset $S \subseteq A$, the **characteristic function** of $S$ is
    > $$\chi_S \colon A \to 2, \qquad \chi_S(a) = \begin{cases} \mathrm{true} & \text{if } a \in S, \\ \mathrm{false} & \text{if } a \notin S. \end{cases}$$
    > The **power set** $\mathcal{P}(A)$ is the set of all subsets of $A$.

    **Reading the definition.**

    1. $\chi_S$ is a function with domain all of $A$, not only $S$: it answers the question "is $a$ in $S$?" for every $a \in A$.
    2. From any function $\chi \colon A \to 2$ you get a subset back: $\chi^{-1}(\mathrm{true}) = \{a \in A : \chi(a) = \mathrm{true}\}$.
    3. The claim that these two passages are mutually inverse, so that $\mathcal{P}(A) \cong 2^A$, is exercise P01.

    **Example.** For $A = \{1, 2, 3\}$ and $S = \{1, 3\}$: $\chi_S(1) = \chi_S(3) = \mathrm{true}$ and $\chi_S(2) = \mathrm{false}$. The empty subset has the constant function $\mathrm{false}$, and $A$ itself the constant function $\mathrm{true}$.

    **Example.** A set with $n$ elements has $2^n$ subsets, because $2^A$ has $2^n$ elements (Section 3) and $\mathcal{P}(A) \cong 2^A$.

    **Non-example (a subset is not an injection).** Every injection $i \colon X \to A$ determines a subset of $A$, its image. But different injections can have the same image: the two bijections $\{0, 1\} \to \{0, 1\}$ both have image $\{0, 1\}$. So subsets of $A$ correspond to functions $A \to 2$ exactly, but to injections into $A$ only up to a bijection of the domain.

    This is the first appearance of a pattern that Part 4 is devoted to: a construction on $A$ (its set of subsets) is described as the set of maps from $A$ into one fixed object (here $2$).

    > Reference: [Leinster §3.1](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Equalizers and Quotients

    Two more ways to make a new set: cut one down by an equation, or glue elements of one together.

    > **Definition (equalizer).** Let $f, g \colon A \to B$ be two functions with the same domain and codomain. Their **equalizer** is the subset
    > $$\mathrm{Eq}(f, g) = \{a \in A : f(a) = g(a)\} \subseteq A,$$
    > together with the inclusion function $i \colon \mathrm{Eq}(f, g) \to A$, $i(a) = a$.

    **Reading the definition.**

    1. $f \circ i = g \circ i$: on elements of the equalizer, $f$ and $g$ agree. That is what membership means.
    2. The equalizer is the *largest* subset on which $f$ and $g$ agree. The precise form of "largest", phrased with maps, is Proposition 3.

    **Example.** For $f, g \colon \mathbb{R} \to \mathbb{R}$ with $f(x) = x^2$ and $g(x) = x$: $\mathrm{Eq}(f, g) = \{0, 1\}$. Solution sets of equations are equalizers.

    **Example.** For a group homomorphism $\varphi \colon G \to H$, the kernel is $\mathrm{Eq}(\varphi, c)$ where $c \colon G \to H$ is the constant function with value the identity of $H$.

    **Non-example.** The subset $\{0\} \subseteq \mathbb{R}$ also satisfies item 1 for $f(x) = x^2$, $g(x) = x$, but it is not the equalizer: it misses $1$. Satisfying $f \circ i = g \circ i$ is necessary, not sufficient.

    **Proposition 3.** Let $f, g \colon A \to B$ and $i \colon \mathrm{Eq}(f, g) \to A$ be as above. For every set $X$ and every function $h \colon X \to A$ with $f \circ h = g \circ h$, there is exactly one function $\bar h \colon X \to \mathrm{Eq}(f, g)$ with $i \circ \bar h = h$.

    - **Goal.** *Existence* of $\bar h$ with $i \circ \bar h = h$, and *uniqueness*: if $k \colon X \to \mathrm{Eq}(f, g)$ also satisfies $i \circ k = h$ then $k = \bar h$.
    - **Given.** $f(h(x)) = g(h(x))$ for all $x \in X$. The definition of $\mathrm{Eq}(f, g)$ and of $i$.
    - **Plan.** The hypothesis says precisely that $h$ takes values in the equalizer, so $\bar h$ should be "$h$ with a smaller codomain". Uniqueness follows because $i$ is injective.
    - **Proof.** *Existence.* Let $x \in X$. By hypothesis $f(h(x)) = g(h(x))$, so $h(x) \in \mathrm{Eq}(f, g)$. So we may define $\bar h \colon X \to \mathrm{Eq}(f, g)$ by $\bar h(x) = h(x)$. Then $i(\bar h(x)) = \bar h(x) = h(x)$ for all $x$, that is, $i \circ \bar h = h$. *Uniqueness.* Suppose $k \colon X \to \mathrm{Eq}(f, g)$ satisfies $i \circ k = h$. For every $x \in X$, $k(x) = i(k(x)) = h(x) = \bar h(x)$, using the definition of $i$, the assumption on $k$, and the definition of $\bar h$. So $k = \bar h$. $\blacksquare$
    - **What made it work.** Before defining a function into a subset you must check that its values land in the subset; that check *was* the hypothesis. This is the "well defined" step that proofs most often skip.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "X": (0.0, 1.8, r"$X$"),
            "E": (0.0, 0.0, r"$\mathrm{Eq}(f,g)$"),
            "E+": (0.5, 0.0, ""),
            "A": (3.0, 0.0, r"$A$"),
            "B": (5.4, 0.0, r"$B$"),
        },
        [
            ("X", "E", r"$\quad\bar{h}$", {"dashed": True}),
            ("X", "A", r"$h$", {"side": -1}),
            ("E+", "A", r"$i$"),
            ("A", "B", r"$f$", {"rad": -0.3}),
            ("A", "B", r"$g$", {"rad": 0.3}),
        ],
        figsize=(6.6, 3.2),
        title=r"If $f \circ h = g \circ h$, then $h$ factors uniquely through $i$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Definition (quotient).** An **equivalence relation** on a set $A$ is a relation $\sim$ that is reflexive ($a \sim a$), symmetric ($a \sim a'$ implies $a' \sim a$) and transitive ($a \sim a'$ and $a' \sim a''$ imply $a \sim a''$). The **equivalence class** of $a$ is $[a] = \{a' \in A : a' \sim a\}$. The **quotient set** $A/{\sim}$ is the set of equivalence classes, and the **quotient map** is $p \colon A \to A/{\sim}$, $p(a) = [a]$.

    **Reading the definition.**

    1. $p(a) = p(a')$ if and only if $a \sim a'$. (This uses all three properties of $\sim$.)
    2. $p$ is surjective: every class is the class of something.
    3. *Maps out of a quotient:* for every set $B$ and every function $f \colon A \to B$ such that $a \sim a'$ implies $f(a) = f(a')$, there is exactly one function $\bar f \colon A/{\sim} \to B$ with $\bar f \circ p = f$. Proving this is exercise P04.

    Compare item 3 with Proposition 3: an equalizer receives maps *into* it, a quotient emits maps *out of* it. They are dual, in a sense made precise in 5B.

    **Example.** On $\mathbb{Z}$ let $a \sim a'$ mean that $n$ divides $a - a'$. The quotient is $\mathbb{Z}/n$, and item 3 is the familiar rule that a function on $\mathbb{Z}/n$ may be defined by a formula on representatives, provided the formula gives the same answer on congruent integers.

    **Example.** For any function $f \colon A \to B$, "$a \sim a'$ if and only if $f(a) = f(a')$" is an equivalence relation on $A$.

    **Non-example.** On $\mathbb{Z}$, "$|a - a'| \leq 1$" is reflexive and symmetric but not transitive ($0$ is related to $1$ and $1$ to $2$, but $0$ is not related to $2$). Its "classes" $\{a - 1, a, a + 1\}$ overlap without being equal, so they do not partition $\mathbb{Z}$ and item 1 fails.

    Given any relation $R$ on $A$ there is a smallest equivalence relation containing it, the intersection of all equivalence relations on $A$ that contain $R$; it is called the equivalence relation **generated by** $R$. Colimits in 5B are built from sums and quotients by generated equivalence relations.

    > Reference: [Leinster §3.1](https://arxiv.org/abs/1612.09375); equalizers and coequalizers in general categories are in [Leinster §5.1–5.2](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Comparing Sizes: Cantor's Theorem

    To talk about categories being "too big" we first need to compare sizes of sets without counting.

    > **Definition.** Let $A$ and $B$ be sets.
    > - $A$ and $B$ **have the same cardinality**, written $A \cong B$, if there is a bijection $A \to B$ (an isomorphism in $\mathbf{Set}$).
    > - $|A| \leq |B|$ means there is an injection $A \to B$.
    > - $|A| < |B|$ means $|A| \leq |B|$ and there is no bijection $A \to B$.

    **Reading the definition.** $|A| \leq |B|$ is a claim that some injection *exists*; to refute $A \cong B$ you must show that *every* function $A \to B$ fails to be a bijection. The second kind of statement is the harder one, because it quantifies over all functions.

    **Example.** For finite sets these agree with comparing numbers of elements. $\mathbb{N} \cong \mathbb{Z}$, by listing the integers as $0, 1, -1, 2, -2, \dots$

    **Non-example.** A proper subset can have the same cardinality as the whole set: the even numbers are in bijection with $\mathbb{N}$ via $n \mapsto 2n$. "Smaller as a subset" does not imply "smaller in cardinality".

    A fact we state without proof, the **Cantor–Bernstein theorem**: if $|A| \leq |B|$ and $|B| \leq |A|$ then $A \cong B$. We shall not need it.

    **Theorem 4 (Cantor).** For every set $A$ and every function $f \colon A \to \mathcal{P}(A)$, $f$ is not surjective.

    - **Goal.** Given an arbitrary $f \colon A \to \mathcal{P}(A)$, produce a subset $D \subseteq A$ such that $D \neq f(a)$ for every $a \in A$.
    - **Given.** For each $a \in A$, $f(a)$ is a subset of $A$, so the question "is $a \in f(a)$?" has an answer. Two subsets are different if some element belongs to one and not the other.
    - **Plan.** The diagonal argument: build $D$ so that it disagrees with $f(a)$ about the element $a$ itself, for each $a$.
    - **Proof.** Define
      $$D = \{a \in A : a \notin f(a)\}.$$
      Let $a \in A$ be arbitrary; we show $D \neq f(a)$. Either $a \in f(a)$ or $a \notin f(a)$. If $a \in f(a)$, then by the definition of $D$, $a \notin D$; so $a$ belongs to $f(a)$ but not to $D$. If $a \notin f(a)$, then $a \in D$; so $a$ belongs to $D$ but not to $f(a)$. In both cases the sets $D$ and $f(a)$ differ at the element $a$. Hence $D$ is not in the image of $f$, and $f$ is not surjective. $\blacksquare$
    - **What made it work.** We needed one subset different from *every* $f(a)$, and we got it by using each $a$ twice: as the label of the subset $f(a)$ and as a potential member of it. Whenever you must defeat every member of a list indexed by the same things the members are about, try the diagonal.

    **Corollary 5.** $|A| < |\mathcal{P}(A)|$ for every set $A$. Indeed $a \mapsto \{a\}$ is an injection $A \to \mathcal{P}(A)$, and by Theorem 4 no function $A \to \mathcal{P}(A)$ is surjective, so none is a bijection. In particular there is no largest set.

    For a finite set with $n$ elements this says $n < 2^n$; the theorem is the version that does not need counting.

    > Reference: [Leinster §3.2](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Small, Locally Small and Large Categories

    Is there a set of all sets? If there were, $\mathbf{Set}$ would be a category whose objects form a set, like a monoid or a poset. Cantor's theorem says no.

    **Proposition 6.** Let $I$ be a set and $(A_i)_{i \in I}$ a family of sets indexed by $I$. Then there is a set $B$ that is not in bijection with $A_i$ for any $i \in I$.

    - **Goal.** Construct a set $B$ such that for every $i \in I$ there is no bijection $A_i \to B$.
    - **Given.** The sum of a family: $S = \sum_{i \in I} A_i = \{(i, a) : i \in I,\ a \in A_i\}$ is a set (the many-summand version of Section 2). Theorem 4.
    - **Plan.** Take a set that is bigger than all the $A_i$ together, namely the power set of their sum, and reduce to Cantor's theorem by contradiction.
    - **Proof.** Let $B = \mathcal{P}(S)$. Suppose, for a contradiction, that for some $j \in I$ there is a bijection $k \colon A_j \to \mathcal{P}(S)$. Define $s \colon S \to \mathcal{P}(S)$ by
      $$s(i, a) = \begin{cases} k(a) & \text{if } i = j, \\ \emptyset & \text{if } i \neq j. \end{cases}$$
      Then $s$ is surjective: given $T \in \mathcal{P}(S)$, surjectivity of $k$ gives $a \in A_j$ with $k(a) = T$, and then $s(j, a) = T$. This contradicts Theorem 4 applied to the set $S$. So no such $j$ exists. $\blacksquare$
    - **What made it work.** One set, the sum, contains a copy of every $A_i$; its power set is then too big for any of them. The family has to be indexed by a *set* for the sum to be a set, and this is exactly where size enters.

    In words: **no set-indexed family of sets contains every set up to bijection.** This is the precise sense in which there is no set of all sets. It is a cousin of Russell's paradox: in a theory where one may ask whether a set is a member of itself, the "set" $\{x : x \notin x\}$ is contradictory, by the same diagonal move as in Theorem 4.

    So we need a word for collections that may be too big to be sets. Following Leinster, we use **class** informally for any collection of mathematical objects, and call a class **small** if it is a set (more exactly: if its members can be indexed by the elements of a set) and **large** otherwise. Making "class" formal is the business of set theory, and can be done in several ways; we shall not do it, and nothing in this course depends on how it is done.

    > **Definition.** A category $\mathcal{A}$ is
    > - **small** if the class of all its arrows is a set;
    > - **locally small** if for every pair of objects $A, B$ the class $\mathcal{A}(A, B)$ of arrows from $A$ to $B$ is a set;
    > - **large** if it is not small;
    > - **essentially small** if it is equivalent to some small category.

    **Reading the definition.**

    1. *Small* is a condition on **all arrows at once**. It implies that the objects form a set too, since objects correspond one-to-one with identity arrows. It also implies locally small, since each $\mathcal{A}(A, B)$ is a subclass of the class of all arrows.
    2. *Locally small* is a condition on **one hom-class at a time**. It allows any number of objects.
    3. *Essentially small* uses equivalence (1E), so it ignores how many isomorphic copies of each object there are. Every small category is essentially small, because a category is equivalent to itself.

    **Example (small).** A monoid or group as a one-object category; a poset; every finite category in the Compute It exercises; the category $\mathcal{N}$ of 1E, with objects the sets $\{1, \dots, n\}$ and all functions between them.

    **Example (locally small, not small).** $\mathbf{Set}$ is locally small because $\mathbf{Set}(A, B) = B^A$ is a set (Section 3). It is not small by Theorem 7 below. $\mathbf{Grp}$, $\mathbf{Vect}_k$ and $\mathbf{Top}$ are locally small because their hom-classes are subsets of function sets.

    **Example (essentially small, not small).** $\mathbf{FinSet}$ is not small: for every set $x$ whatsoever, $\{x\}$ is a finite set, so there are at least as many finite sets as there are sets. But $\mathbf{FinSet} \simeq \mathcal{N}$ (1E), and $\mathcal{N}$ is small. So $\mathbf{FinSet}$ is essentially small.

    **Non-example.** $\mathbf{Set}$ is not essentially small:

    **Theorem 7.** $\mathbf{Set}$ is not equivalent to any small category. In particular $\mathbf{Set}$ is not small.

    - **Goal.** For every small category $\mathcal{B}$, there is no equivalence between $\mathbf{Set}$ and $\mathcal{B}$.
    - **Given.** The definition of equivalence (1E): functors $F \colon \mathbf{Set} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathbf{Set}$ and natural isomorphisms $\eta \colon 1_{\mathbf{Set}} \Rightarrow GF$, $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$. Proposition 6. An isomorphism in $\mathbf{Set}$ is a bijection.
    - **Plan.** Contradiction. A small category has only a set of objects, so the functor $G$ produces only a set-indexed family of sets; but an equivalence would make every set isomorphic to a member of that family.
    - **Proof.** Suppose $(F, G, \eta, \varepsilon)$ is an equivalence between $\mathbf{Set}$ and a small category $\mathcal{B}$. Since $\mathcal{B}$ is small, its objects form a set $I$. Consider the family of sets $(G(b))_{b \in I}$. By Proposition 6 there is a set $X$ that is not in bijection with $G(b)$ for any $b \in I$. But $\eta_X \colon X \to GF(X)$ is an isomorphism in $\mathbf{Set}$, that is, a bijection from $X$ to $G(b)$ with $b = F(X) \in I$. This is a contradiction. For the last sentence of the theorem: if $\mathbf{Set}$ were small it would be equivalent to a small category, namely itself. $\blacksquare$
    - **What made it work.** Equivalence cannot shrink the class of isomorphism classes of objects, and $\mathbf{Set}$ has too many of those for any set to index. The only fact about equivalences used was that each object is isomorphic to its image under $GF$.

    A similar argument applies to $\mathbf{Top}$: every set carries the discrete topology, and two discrete spaces are homeomorphic exactly when their underlying sets are in bijection, so Proposition 6 gives a space not isomorphic to any member of a given set-indexed family of spaces. $\mathbf{Grp}$ and $\mathbf{Vect}_k$ are not essentially small either; showing it requires a supply of groups, or vector spaces, of unboundedly large size, and we omit it.

    **Three conventions that follow.**

    - $\mathbf{Cat}$ denotes the category of **small** categories and functors. This avoids a "category of all categories" that would have to contain itself. $\mathbf{Cat}$ is locally small and not small.
    - If $\mathcal{A}$ is small and $\mathcal{B}$ is locally small, then the functor category $[\mathcal{A}, \mathcal{B}]$ is locally small. (We state this without proof. It is the reason the warning in 1D about $[\mathcal{A}, \mathcal{B}]$ mentioned large $\mathcal{A}$.)
    - When a later theorem says "let $\mathcal{A}$ be a small category" or "locally small category", the hypothesis is doing work. The Yoneda lemma (4B) needs hom-*sets*; limit theorems in Part 6 distinguish small limits from large ones.

    **A word on foundations.** The usual formal background for mathematics is the axiom system ZFC, in which everything is a set and the basic relation is membership. Leinster's chapter describes a different presentation, going back to Lawvere, in which the basic notions are sets, functions and composition, and the axioms are properties of the category of sets like those in Sections 1 to 5. For the purposes of this course the two support the same working rules, and you may hold either picture. What you should not do is treat "the set of all sets", "the set of all groups" or "the category of all categories" as if they were sets or small categories.

    > Reference: [Leinster §3.2](https://arxiv.org/abs/1612.09375) (small and large categories), [Leinster §3.3](https://arxiv.org/abs/1612.09375) (historical remarks on foundations); [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf) (remarks on size).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Proving a bijection by giving a map in one direction only.** A function $\Theta$ with a function $\Psi$ such that $\Psi \circ \Theta = 1$ is injective, not yet bijective. Check **both** composites, as in Proposition 2, or prove injectivity and surjectivity separately.
    2. **Defining a function into a subset, or out of a quotient, without checking it is well defined.** Into $\mathrm{Eq}(f, g)$: show the values satisfy the equation. Out of $A/{\sim}$: show the formula gives the same answer on related elements. In both cases the check is where the hypothesis is used.
    3. **Treating vacuous cases as failures.** There *is* a function $\emptyset \to A$, exactly one. "There are no elements to send anywhere" proves uniqueness and existence, not non-existence.
    4. **Mixing up $B^A$ and $A^B$.** $B^A$ is functions from $A$ to $B$; count check: $|B^A| = |B|^{|A|}$.
    5. **In a diagonal argument, exhibiting a set that differs from *one* $f(a)$.** The set $D$ must differ from $f(a)$ for **every** $a$, and the proof must begin "let $a \in A$ be arbitrary".
    6. **Saying "the set of all sets" or assuming a category has a set of objects.** If an argument forms a product, sum or family indexed by the objects of a category, it needs that category to be small. Say so.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why This Matters

    - **4A (representables).** The functors $H^A = \mathcal{A}(A, -)$ take values in $\mathbf{Set}$ only if $\mathcal{A}$ is locally small. The bijection $\mathcal{P}(A) \cong \mathbf{Set}(A, 2)$ of Section 4 is the first example of a *representable* functor, and Proposition 2 is another.
    - **4B (Yoneda).** The lemma is a bijection between two sets, proved exactly as in Proposition 2: a map each way and both composites. One of the sets is a class of natural transformations, and local smallness is what keeps the statement meaningful.
    - **5A, 5B (limits and colimits).** Products and equalizers in $\mathbf{Set}$ (Sections 2, 5) are the building blocks of all limits; sums and quotients are the building blocks of all colimits. The universal properties you met here are the definitions there.
    - **6C (adjoint functor theorems).** Their hypotheses are size conditions. Without the vocabulary of this module they cannot be stated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Set Exercises

    This module is about $\mathbf{Set}$, so the exercises use finite sets directly: a set is a Python list or set, and a function is a dictionary sending each element of the domain to its value. The cells run as shipped; fill in each `# TODO`, then uncomment the `print` checks and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Subsets and Characteristic Functions

    Write `chi(A, S)`, the characteristic function of the subset `S` of `A` as a dictionary with values `True` / `False`, and `subset_of(A, c)`, which recovers the subset from a characteristic function. Then check on a four-element set that going there and back returns the subset you started with, for all sixteen subsets.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        A = [0, 1, 2, 3]

        def chi(A, S):
            # TODO: the dictionary a -> True/False answering "is a in S?"
            _result = ...
            return _result

        def subset_of(A, c):
            # TODO: the set of elements of A that c sends to True
            _result = ...
            return _result

        all_subsets = [set(_s) for _r in range(len(A) + 1) for _s in itertools.combinations(A, _r)]

        # print(chi(A, {1, 3}))                                             # expect {0: False, 1: True, 2: False, 3: True}
        # print(subset_of(A, {0: False, 1: True, 2: False, 3: True}))       # expect {1, 3}
        # print(len(all_subsets))                                           # expect 16
        # print(all(subset_of(A, chi(A, S)) == S for S in all_subsets))     # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Equalizers and the Factorisation

    Write `equalizer(A, f, g)`, returning the list of elements of `A` on which the functions `f` and `g` agree, and `factor(h, E)`, which returns the function $\bar h$ of Proposition 3 when `h` takes all its values in `E` and returns `None` when it does not. The example has $A = \{0, \dots, 5\}$, $f(a) = a^2 \bmod 6$ and $g(a) = a$.
    """)
    return


@app.cell
def _():
    def _run():
        A = list(range(6))
        f = {_a: (_a * _a) % 6 for _a in A}
        g = {_a: _a for _a in A}

        def equalizer(A, f, g):
            # TODO: the elements of A where f and g take the same value, in the order of A
            _result = ...
            return _result

        def factor(h, E):
            # TODO: if every value of h lies in E, return h regarded as a function into E;
            #       otherwise return None
            _result = ...
            return _result

        h_good = {"x": 3, "y": 0, "z": 3}     # satisfies f(h(t)) == g(h(t)) for every t
        h_bad = {"x": 2, "y": 0, "z": 3}      # f(2) = 4 but g(2) = 2

        # E = equalizer(A, f, g)
        # print(E)                      # expect [0, 1, 3, 4]
        # print(factor(h_good, E))      # expect {'x': 3, 'y': 0, 'z': 3}
        # print(factor(h_bad, E))       # expect None

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: The Diagonal Set

    Write `diagonal(A, f)`, which for a function `f` from `A` to subsets of `A` (a dictionary whose values are `frozenset`s) returns the set $D$ from the proof of Cantor's theorem. Then confirm the theorem by brute force for $A = \{0, 1, 2\}$: among all $8^3 = 512$ functions $A \to \mathcal{P}(A)$, count how many are surjective and how many have their diagonal set in their image.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        A = [0, 1, 2]
        subsets = [frozenset(_s) for _r in range(len(A) + 1) for _s in itertools.combinations(A, _r)]

        def diagonal(A, f):
            # TODO: the frozenset D defined in the proof of Theorem 4
            _result = ...
            return _result

        f0 = {0: frozenset({0, 1}), 1: frozenset(), 2: frozenset({0, 2})}

        n_surjective = 0
        n_diagonal_in_image = 0
        for _values in itertools.product(subsets, repeat=len(A)):
            _f = dict(zip(A, _values))
            # TODO: update the two counters for this function _f
            pass

        # print(diagonal(A, f0))                         # expect frozenset({1})
        # print(diagonal(A, f0) in f0.values())          # expect False
        # print(n_surjective, n_diagonal_in_image)       # expect 0 0

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six proof briefs, in `exercises/3a/`. Each has the statement, what you may assume, what a complete proof must contain, and hints that open one at a time. There are no solutions anywhere in the course.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | Subsets are functions into the two-element set — `exercises/3a/p01_subsets_characteristic_functions.md` | warm-up | explicit bijection |
    | P02 | Elements are maps from the one-element set — `exercises/3a/p02_elements_as_maps.md` | warm-up | explicit bijection; equality of functions |
    | P03 | Functions out of a sum — `exercises/3a/p03_functions_out_of_a_sum.md` | core | explicit bijection, case analysis |
    | P04 | Functions out of a quotient — `exercises/3a/p04_functions_out_of_a_quotient.md` | core | well-definedness, existence and uniqueness |
    | P05 | An essentially small category is locally small — `exercises/3a/p05_essentially_small_locally_small.md` | core | transporting a property along a full and faithful functor |
    | P06 | A fixed-point form of the diagonal argument — `exercises/3a/p06_diagonal_fixed_point.md` | stretch | diagonal argument |

    **How to submit a proof.** Write your proof in `proofs/3a/pNN_<slug>.md` (the same file name as the brief), then ask Claude to review it.
    The review points at gaps and asks questions; it does not supply a model proof, so the proof stays yours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [2C: Adjunctions via Initial Objects](../2c_universal_arrows/) | Next: [4A: Representable Functors](../4a_representables/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
