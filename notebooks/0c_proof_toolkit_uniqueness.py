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
    # 0C: Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher

    > *"Mathematics is the art of giving the same name to different things."*
    > — Henri Poincaré, *Science and Method*

    Module 0B gave you the first proof shape: unpack the definitions and verify the checklist. This module gives you the other two shapes that category theory uses constantly, and refreshes the algebra that the examples will come from.

    The questions it answers are: **what does a proof of "there is exactly one" contain? What does it mean for a diagram to commute, and how do you prove things by following arrows around one? And what can "the same" mean for two objects that are not literally equal?** The last question is the one in the epigraph. Category theory almost never says that two objects are equal. It says they are isomorphic, and where possible it says there is only one isomorphism that could be meant.

    By the end you will be able to prove: that a monoid has only one identity element, that a group homomorphism must preserve the identity, that a partially ordered set has at most one least element, that two commutative squares paste to a commutative rectangle, and that any two sets with the universal property of the one-element set are related by exactly one function, which is invertible. That last proof is the template for every "unique up to unique isomorphism" argument in Parts 2, 4 and 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. "Exactly One": Existence and Uniqueness

    Universal properties (0A) all contain the words "there exists a unique". Those words abbreviate two statements, and each needs its own proof.

    > **Definition (exists unique).** "There exists a unique $x \in A$ such that $P(x)$", written $\exists!\, x \in A,\ P(x)$, means that both of the following hold.
    >
    > - **(E) Existence.** There exists $x \in A$ such that $P(x)$.
    > - **(U) Uniqueness.** For all $x, x' \in A$: if $P(x)$ and $P(x')$, then $x = x'$.

    **Reading the definition.**

    - (E) is proved the way any "there exists" is proved: produce a witness and check it.
    - (U) is a "for all ... if ... then" statement. Its proof begins "Let $x$ and $x'$ both satisfy $P$" and ends "$x = x'$". Nothing may be assumed about $x$ and $x'$ except that each satisfies $P$. In particular you may not assume that either of them is the witness you built for (E).
    - (E) and (U) are independent. Either can hold without the other, so proving one never excuses you from the other.
    - Uniqueness says "at most one". It does not say there is one.

    **Examples and non-examples.**

    | Statement about a real number $x$ | (E) | (U) | Why |
    |---|---|---|---|
    | $2x + 3 = 7$ | holds | holds | $x = 2$ works; if $2x + 3 = 2x' + 3$ then $x = x'$ |
    | $x^2 = 4$ | holds | **fails** | $2$ and $-2$ both work and $2 \neq -2$ |
    | $x^2 = -1$ | **fails** | holds | no real number works; (U) holds because there are no $x, x'$ satisfying the hypothesis |
    | $x^2 = 4$ and $x > 0$ | holds | holds | $x = 2$ works; if $x^2 = x'^2$ with $x, x' > 0$ then $(x - x')(x + x') = 0$ and $x + x' > 0$, so $x = x'$ |

    There are two standard ways to prove (U), and you have now seen the second one already.

    - **Two candidates.** Take two things with the property and show they are equal, usually by finding **one expression that each of them simplifies in a different way**.
    - **Forced value.** Take one thing with the property and show the property forces it to equal a specific formula. Two things forced to equal the same formula are equal. (This is how the uniqueness of the map into a product was proved in 0A.)

    The first method is best learned on the cleanest possible example, which needs a definition you know.

    > **Definition (monoid).** A *monoid* $(M, \cdot, e)$ is a set $M$ together with a function $M \times M \to M$, written $(a, b) \mapsto a \cdot b$, and an element $e \in M$, such that
    >
    > - **associativity:** for all $a, b, c \in M$, $(a \cdot b) \cdot c = a \cdot (b \cdot c)$;
    > - **identity laws:** for all $a \in M$, $e \cdot a = a$ and $a \cdot e = a$.

    **Reading the definition.** To check that something is a monoid: (1) the operation is defined on every pair and its result lands back in $M$; (2) associativity, for all triples; (3) an element $e$ is named, and both identity equations hold for every $a$. Commutativity is not required.

    **Examples.** $(\mathbb{N}, +, 0)$. $(\mathbb{Z}, \times, 1)$. The $n \times n$ real matrices under matrix multiplication, with the identity matrix. For any set $A$, the set of all functions $A \to A$ under composition, with identity $1_A$: the two axioms are exactly Proposition 2 of 0B. **Non-examples.** $\mathbb{Z}$ with subtraction is not associative: $(1 - 1) - 1 = -1$ but $1 - (1 - 1) = 1$. The positive integers $\{1, 2, 3, \ldots\}$ with addition have no identity: an identity $e$ would satisfy $e + 1 = 1$, forcing $e = 0$, which is not a positive integer.

    > **Proposition 1 (the identity of a monoid is unique).** Let $M$ be a set with an associative operation $\cdot$. If $e \in M$ and $e' \in M$ both satisfy the identity laws, then $e = e'$.

    **Goal.** For all $e, e' \in M$: if ($e \cdot a = a = a \cdot e$ for all $a \in M$) and ($e' \cdot a = a = a \cdot e'$ for all $a \in M$), then $e = e'$.

    **Given.** The two identity laws, one for $e$ and one for $e'$. Each is a "for all $a$" statement, so each may be applied to any element of $M$ we choose.

    **Plan.** Uniqueness by the two-candidates method. Look for one expression that $e$ simplifies one way and $e'$ simplifies the other way. The only thing a monoid lets us do with two elements is multiply them.

    **Proof.** Let $e$ and $e'$ both satisfy the identity laws. Consider the element $e \cdot e'$.

    - Apply the law "$a \cdot e' = a$ for all $a$" (which holds because $e'$ is an identity) with $a = e$. It gives $e \cdot e' = e$.
    - Apply the law "$e \cdot a = a$ for all $a$" (which holds because $e$ is an identity) with $a = e'$. It gives $e \cdot e' = e'$.

    Therefore $e = e \cdot e' = e'$. $\blacksquare$

    **What made it work.** Each candidate's defining property is a "for all" statement, and we applied each one **to the other candidate**. Associativity was never used, and of the four identity equations we used only two. Reach for this whenever two things are both claimed to satisfy a property that says how they interact with everything: let them interact with each other.

    > References: [Hammack Ch 7](https://www.people.vcu.edu/~rhammack/BookOfProof/) (existence and uniqueness proofs).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Groups and Homomorphisms

    > **Definition (group).** A *group* is a monoid $(G, \cdot, e)$ in which for every $a \in G$ there exists $b \in G$ such that $a \cdot b = e$ and $b \cdot a = e$. Such a $b$ is called an *inverse* of $a$.

    **Reading the definition.** The three monoid checks, and then: for each $a$, produce an element $b$ and verify *both* equations. For a given $a$ the inverse is unique. The argument is the one you write in brief 0B·P04, which uses nothing but associativity and the identity laws and so applies word for word in any monoid. Because of that uniqueness we may speak of *the* inverse of $a$ and write $a^{-1}$.

    **Examples.** $(\mathbb{Z}, +, 0)$, where the inverse of $n$ is $-n$. The non-zero real numbers under multiplication. The invertible $n \times n$ real matrices, $GL_n(\mathbb{R})$. **Non-examples.** $(\mathbb{N}, +, 0)$ is a monoid but not a group: no $b \in \mathbb{N}$ has $1 + b = 0$. $(\mathbb{Z}, \times, 1)$ is a monoid but not a group: no integer $b$ has $2b = 1$.

    Next, the maps. For every kind of structure there is a kind of function that respects it.

    > **Definition (homomorphisms).** Let $(M, \cdot, e_M)$ and $(N, \cdot, e_N)$ be monoids. A *monoid homomorphism* $f \colon M \to N$ is a function $f \colon M \to N$ such that
    >
    > - for all $a, b \in M$, $f(a \cdot b) = f(a) \cdot f(b)$, and
    > - $f(e_M) = e_N$.
    >
    > If $G$ and $H$ are groups, a *group homomorphism* $f \colon G \to H$ is a function such that $f(a \cdot b) = f(a) \cdot f(b)$ for all $a, b \in G$.

    **Reading the definition.** In $f(a \cdot b) = f(a) \cdot f(b)$ the dot on the left is the operation of the domain and the dot on the right is the operation of the codomain. To check a function is a monoid homomorphism there are two things to verify; for a group homomorphism the definition lists only one. The proposition below explains why that is enough for groups.

    **Examples.** The exponential function $\exp \colon (\mathbb{R}, +, 0) \to (\mathbb{R}_{>0}, \times, 1)$, since $\exp(a + b) = \exp(a)\exp(b)$. The determinant $\det \colon GL_n(\mathbb{R}) \to (\mathbb{R} \setminus \{0\}, \times, 1)$, since $\det(AB) = \det(A)\det(B)$. Reduction modulo $n$, from $(\mathbb{Z}, +, 0)$ to $(\mathbb{Z}/n, +, 0)$.

    **Non-examples.** $f \colon \mathbb{Z} \to \mathbb{Z}$, $f(n) = n + 1$, is not a homomorphism of $(\mathbb{Z}, +, 0)$: $f(0 + 0) = 1$ but $f(0) + f(0) = 2$. More instructive: $z \colon (\mathbb{Z}, \times, 1) \to (\mathbb{Z}, \times, 1)$, $z(n) = 0$. It satisfies the first condition, since $z(ab) = 0 = 0 \times 0 = z(a) z(b)$, but $z(1) = 0 \neq 1$, so it is **not** a monoid homomorphism. For monoids, the second condition does not follow from the first.

    > **Proposition 2 (group homomorphisms preserve the identity).** Let $G$ and $H$ be groups with identities $e_G$ and $e_H$, and let $f \colon G \to H$ be a group homomorphism. Then $f(e_G) = e_H$.

    **Goal.** The two elements $f(e_G)$ and $e_H$ of $H$ are equal.

    **Given.** $f(a \cdot b) = f(a) \cdot f(b)$ for all $a, b \in G$. The identity law in $G$. In $H$: associativity, the identity laws, and the existence of an inverse for every element.

    **Plan.** Direct calculation. Get an equation involving only $f(e_G)$ by feeding the homomorphism property the one product we know everything about, $e_G \cdot e_G$; then cancel using an inverse in $H$.

    **Proof.** Write $h = f(e_G)$; it is an element of $H$. By the identity law in $G$, $e_G \cdot e_G = e_G$. Applying $f$ and using the homomorphism property,

    $$h = f(e_G) = f(e_G \cdot e_G) = f(e_G) \cdot f(e_G) = h \cdot h.$$

    Since $H$ is a group, $h$ has an inverse $h^{-1}$. Multiply both sides of $h = h \cdot h$ on the left by $h^{-1}$:

    $$h^{-1} \cdot h = h^{-1} \cdot (h \cdot h) = (h^{-1} \cdot h) \cdot h$$

    by associativity. Now $h^{-1} \cdot h = e_H$ by the definition of inverse, so the left side is $e_H$ and the right side is $e_H \cdot h$, which is $h$ by the identity law. Hence $e_H = h = f(e_G)$. $\blacksquare$

    **What made it work.** The inverse of $h$ let us cancel. The non-example $z$ above shows that this was essential: in the monoid $(\mathbb{Z}, \times, 1)$ the element $0$ satisfies $0 = 0 \times 0$ and is not the identity, and it has no inverse to cancel with. When a hypothesis is used in a proof, it is worth asking what would go wrong without it; here the answer is a concrete counterexample.

    > **Proposition 3 (homomorphisms compose).** Let $f \colon M \to N$ and $g \colon N \to P$ be monoid homomorphisms. Then $g \circ f \colon M \to P$ is a monoid homomorphism. Also, for every monoid $M$ the identity function $1_M$ is a monoid homomorphism.

    **Goal.** (i) For all $a, b \in M$: $(g \circ f)(a \cdot b) = (g \circ f)(a) \cdot (g \circ f)(b)$. (ii) $(g \circ f)(e_M) = e_P$. (iii) For all $a, b \in M$: $1_M(a \cdot b) = 1_M(a) \cdot 1_M(b)$; and $1_M(e_M) = e_M$.

    **Given.** The two homomorphism conditions for $f$ and the two for $g$; the definitions of composite and identity function.

    **Plan.** Direct. Unfold the composite, then use the condition for $f$ (the inner function) first and the condition for $g$ second.

    **Proof.** (i) Let $a, b \in M$. Then

    $$(g \circ f)(a \cdot b) = g\big(f(a \cdot b)\big) = g\big(f(a) \cdot f(b)\big) = g(f(a)) \cdot g(f(b)) = (g \circ f)(a) \cdot (g \circ f)(b).$$

    The first and last equalities are the definition of composite; the second holds because $f$ is a homomorphism; the third holds because $g$ is a homomorphism, applied to the elements $f(a), f(b) \in N$.

    (ii) $(g \circ f)(e_M) = g(f(e_M)) = g(e_N) = e_P$, using the definition of composite, then $f(e_M) = e_N$, then $g(e_N) = e_P$.

    (iii) For $a, b \in M$: $1_M(a \cdot b) = a \cdot b = 1_M(a) \cdot 1_M(b)$ and $1_M(e_M) = e_M$, each by the definition of $1_M$. $\blacksquare$

    **What made it work.** Work from the inside out: the innermost function's hypothesis is the only one that can be applied first. Dropping part (ii) from the argument gives the corresponding statement for group homomorphisms. The fact itself, "structure-preserving maps compose, and identities are structure-preserving", is what will make monoids, groups and the rest into categories in Module 1A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Posets: Where Uniqueness Comes from Antisymmetry

    > **Definition (preorder, poset).** A *preorder* on a set $P$ is a relation $\le$ on $P$ such that
    >
    > - **reflexivity:** for all $x \in P$, $x \le x$;
    > - **transitivity:** for all $x, y, z \in P$, if $x \le y$ and $y \le z$ then $x \le z$.
    >
    > A *partial order* is a preorder that also satisfies
    >
    > - **antisymmetry:** for all $x, y \in P$, if $x \le y$ and $y \le x$ then $x = y$.
    >
    > A *poset* (partially ordered set) is a set together with a partial order on it.

    **Reading the definition.** Three "for all" statements to verify. Nothing says that any two elements are comparable: in a poset it may happen that neither $x \le y$ nor $y \le x$. Antisymmetry is the axiom that produces *equalities*, so it is the one that uniqueness proofs in posets use.

    **Examples.** $(\mathbb{Z}, \le)$. For any set $S$, the set $\mathcal{P}(S)$ of all subsets of $S$, ordered by inclusion $\subseteq$. The positive integers ordered by divisibility: reflexive because $a = a \cdot 1$, transitive by Proposition 1 of 0B, antisymmetric by Proposition 5 of 0B. In this poset $4$ and $6$ are not comparable.

    **Non-examples.** Divisibility on *all* of $\mathbb{Z}$ is a preorder but not a partial order: $2 \mid -2$ and $-2 \mid 2$ but $2 \neq -2$. The relation $<$ on $\mathbb{Z}$ is not a preorder, since $0 < 0$ is false.

    > **Definition (monotone map).** Let $P$ and $Q$ be posets. A function $f \colon P \to Q$ is *monotone* (or *order-preserving*) if for all $x, y \in P$: if $x \le y$ then $f(x) \le f(y)$.

    **Example.** For a finite set $S$, the function $\mathcal{P}(S) \to (\mathbb{N}, \le)$ sending a subset to its number of elements: if $X \subseteq Y$ then $|X| \le |Y|$. **Non-example.** $n \mapsto -n$ on $(\mathbb{Z}, \le)$: we have $0 \le 1$, but $-0 \le -1$ is false.

    > **Definition (least element).** An element $m$ of a poset $P$ is a *least element* if $m \le x$ for all $x \in P$.

    **Examples and non-examples.** $\emptyset$ is a least element of $(\mathcal{P}(S), \subseteq)$. $1$ is a least element of the positive integers under divisibility, since $1 \mid x$ for every $x$. $(\mathbb{Z}, \le)$ has no least element: for any $m \in \mathbb{Z}$, $m \le m - 1$ is false. The set $\{2, 3, 12\}$ under divisibility has no least element: $2 \nmid 3$ and $3 \nmid 2$, and $12$ divides neither.

    > **Proposition 4.** A poset has at most one least element: if $m$ and $m'$ are both least elements of $P$, then $m = m'$.

    **Goal.** For all $m, m' \in P$: if ($m \le x$ for all $x \in P$) and ($m' \le x$ for all $x \in P$), then $m = m'$.

    **Given.** The property of $m$, the property of $m'$, and antisymmetry. No existence claim: this is a pure uniqueness statement, and it is true even in posets with no least element.

    **Plan.** Two candidates, each applied to the other, as in Proposition 1. This time that yields two inequalities, and antisymmetry turns two inequalities into an equality.

    **Proof.** Let $m$ and $m'$ be least elements of $P$. Apply the property of $m$ with $x = m'$: this gives $m \le m'$. Apply the property of $m'$ with $x = m$: this gives $m' \le m$. By antisymmetry, $m = m'$. $\blacksquare$

    **What made it work.** The same move as for the identity of a monoid: let the two candidates interact with each other. Keep this proof in mind for Section 7. There, "$m \le m'$ and $m' \le m$" will become "a map $T \to T'$ and a map $T' \to T$", and the job done here by antisymmetry will be done by a uniqueness clause. In a mere preorder the proof stops one line early: the two inequalities hold, but the candidates need not be equal. Divisibility on $\mathbb{Z}$ shows this: $1$ and $-1$ both divide everything.

    > References: [Hammack Ch 11](https://www.people.vcu.edu/~rhammack/BookOfProof/) (relations and their properties).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Pattern: Structures and Their Maps

    Two more kinds of structure will be used for examples. They are recalled here only so that the definitions of their maps are in front of you.

    > **Definition (linear map).** Let $V$ and $W$ be vector spaces over a field $k$. A function $f \colon V \to W$ is *linear* if for all $u, v \in V$ and all $\lambda \in k$: $f(u + v) = f(u) + f(v)$ and $f(\lambda v) = \lambda f(v)$.

    > **Definition (topological space, continuous map).** A *topological space* is a set $X$ together with a collection of subsets of $X$, called *open*, such that $\emptyset$ and $X$ are open, every union of open sets is open, and the intersection of any two open sets is open. A function $f \colon X \to Y$ between topological spaces is *continuous* if for every open set $U \subseteq Y$, the preimage $f^{-1}(U) = \{x \in X : f(x) \in U\}$ is open in $X$.

    **Reading the definitions.** Linear: two equations, each a "for all". Continuous: one "for all open $U$ in the codomain"; the condition is about preimages, so it runs *backwards* along $f$. On $\mathbb{R}$, a set is open when each of its points has an open interval around it contained in the set, and for functions $\mathbb{R} \to \mathbb{R}$ this definition of continuity agrees with the $\varepsilon$-$\delta$ one from calculus.

    **Examples.** Differentiation is a linear map from the space of real polynomials to itself. Every polynomial function $\mathbb{R} \to \mathbb{R}$ is continuous. **Non-examples.** $x \mapsto x + 1$ is not a linear map $\mathbb{R} \to \mathbb{R}$: it sends $0 + 0$ to $1$, not to $1 + 1$. The step function $s \colon \mathbb{R} \to \mathbb{R}$ with $s(x) = 0$ for $x < 0$ and $s(x) = 1$ for $x \ge 0$ is not continuous: the interval $U = (\tfrac12, \tfrac32)$ is open, but $s^{-1}(U) = [0, \infty)$ is not, because no open interval around $0$ lies inside it.

    Now put every structure of this module in one table.

    | Structure | Structure-preserving map | Condition on $f$ |
    |-----------|--------------------------|------------------|
    | set | function | none |
    | monoid | monoid homomorphism | $f(a \cdot b) = f(a) \cdot f(b)$ and $f(e) = e$ |
    | group | group homomorphism | $f(a \cdot b) = f(a) \cdot f(b)$ |
    | poset | monotone map | $x \le y \Rightarrow f(x) \le f(y)$ |
    | vector space over $k$ | linear map | $f(u + v) = f(u) + f(v)$ and $f(\lambda v) = \lambda f(v)$ |
    | topological space | continuous map | $f^{-1}(U)$ is open for every open $U$ |

    In every row two things are true: **the identity function is a structure-preserving map, and the composite of two structure-preserving maps is again one.** Proposition 3 did the monoid and group rows in full. The others take one calculation each, with the same inside-out order:

    - *Monotone.* If $x \le y$ then $f(x) \le f(y)$ because $f$ is monotone, and then $g(f(x)) \le g(f(y))$ because $g$ is monotone.
    - *Linear.* $g(f(u + v)) = g(f(u) + f(v)) = g(f(u)) + g(f(v))$ and $g(f(\lambda v)) = g(\lambda f(v)) = \lambda g(f(v))$, using linearity of $f$ and then of $g$.
    - *Continuous.* For $U$ open in the codomain of $g$, a point $x$ lies in $(g \circ f)^{-1}(U)$ exactly when $g(f(x)) \in U$, that is, exactly when $f(x) \in g^{-1}(U)$, that is, exactly when $x \in f^{-1}(g^{-1}(U))$. So $(g \circ f)^{-1}(U) = f^{-1}(g^{-1}(U))$. The set $g^{-1}(U)$ is open because $g$ is continuous, and then its preimage under $f$ is open because $f$ is continuous.

    In each row the identity function passes the test because it changes nothing: for instance $1_X^{-1}(U) = U$.

    This table is the reason category theory exists. Each row is "things, maps, composition, identities", and Module 1A turns that phrase into a definition.

    > References: [Leinster §1.1](https://arxiv.org/abs/1612.09375) lists these as the first examples of categories; [Riehl §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Commutative Diagrams

    An equation between composites, such as $g \circ f = k \circ h$, is hard to read once there are four or five functions in play: you have to keep track of which sets each one goes between. A diagram shows the same information as a picture.

    > **Definition (commutative diagram).** A *diagram* of sets and functions consists of some sets, drawn as nodes, and some functions between them, drawn as arrows. Every directed path of one or more arrows from a node $X$ to a node $Y$ determines a function $X \to Y$: the composite of the arrows along the path. The diagram *commutes* if for every pair of nodes $X$ and $Y$, all the directed paths from $X$ to $Y$ determine the same function.

    **Reading the definition.** To check that a diagram commutes:

    1. List the pairs of nodes joined by more than one path.
    2. For each such pair, write down one equation of functions for each pair of paths.
    3. Prove each equation, as an equality of functions (0B, Section 3).

    "This diagram commutes" is therefore shorthand for a list of equations. As a **hypothesis** it hands you all of those equations. As a **goal** it obliges you to prove all of them.

    **The two basic shapes.** A triangle with sides $f \colon A \to B$, $g \colon B \to C$ and $h \colon A \to C$ has one pair of nodes with two paths ($A$ to $C$), so it commutes exactly when $h = g \circ f$. A square, drawn below, also has only one such pair ($A$ to $D$), so it commutes exactly when $g \circ f = k \circ h$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (0, 1.8, r"$A$"), "B": (2.4, 1.8, r"$B$"), "C": (0, 0, r"$C$"), "D": (2.4, 0, r"$D$")},
        [
            ("A", "B", r"$f$"),
            ("B", "D", r"$g$"),
            ("A", "C", r"$h$", {"side": -1}),
            ("C", "D", r"$k$", {"side": -1}),
        ],
        figsize=(4.4, 3.2),
        title="A square: it commutes when g after f equals k after h",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** Let $p \colon \mathbb{Z} \to \{0, 1\}$ be the parity function ($p(n) = 0$ for even $n$ and $1$ for odd $n$) and let $t \colon \mathbb{Z} \to \mathbb{Z}$ be $t(n) = n + 2$. Take the square with $A = B = \mathbb{Z}$, $C = D = \{0, 1\}$, top arrow $f = t$, both vertical arrows $g = h = p$, and bottom arrow $k = 1_{\{0,1\}}$. It commutes: for every $n \in \mathbb{Z}$, the integers $n + 2$ and $n$ are both even or both odd, so $p(t(n)) = p(n) = 1_{\{0,1\}}(p(n))$.

    **Non-example.** Replace the top arrow by $u(n) = n + 1$ and keep the rest. Now the square does not commute: at $n = 0$ the top-right path gives $p(u(0)) = p(1) = 1$ and the left-bottom path gives $p(0) = 0$. One element at which the two paths differ is enough. (It commutes again if the bottom arrow is changed to the function that swaps $0$ and $1$.)

    **Familiar equations are diagrams.** The homomorphism condition $f(a \cdot b) = f(a) \cdot f(b)$ says that a square commutes: from $M \times M$, either multiply in $M$ and then apply $f$, or apply $f$ to both entries and then multiply in $N$. A left inverse (0B, Section 6) is a commuting triangle. A universal property (0A) is a statement that a dashed arrow exists, uniquely, making certain triangles commute.

    ### The commutativity checker

    All four sets below are $\{0, 1, 2\}$. Choose each of the four functions of the square by its list of values: the entry $(1, 2, 0)$ means $0 \mapsto 1$, $1 \mapsto 2$, $2 \mapsto 0$. The panel computes both paths at each element and reports whether the square commutes.

    Experiments: fix $f$, $g$ and $h$ and hunt for every $k$ that makes the square commute. Can there be none? More than one? What property of $h$ decides whether $k$ is determined by the other three?
    """)
    return


@app.cell
def _(mo):
    def _options():
        import itertools
        return [str(_t) for _t in itertools.product(range(3), repeat=3)]

    sq_f = mo.ui.dropdown(options=_options(), value="(1, 2, 0)", label="f : A → B")
    sq_g = mo.ui.dropdown(options=_options(), value="(0, 0, 1)", label="g : B → D")
    sq_h = mo.ui.dropdown(options=_options(), value="(0, 1, 0)", label="h : A → C")
    sq_k = mo.ui.dropdown(options=_options(), value="(0, 1, 2)", label="k : C → D")
    mo.hstack([sq_f, sq_g, sq_h, sq_k], justify="start")
    return sq_f, sq_g, sq_h, sq_k


@app.cell(hide_code=True)
def _(draw_diagram, mo, sq_f, sq_g, sq_h, sq_k):
    def _run():
        def _parse(text):
            return [int(_c) for _c in text.strip("()").split(",")]

        _f, _g, _h, _k = _parse(sq_f.value), _parse(sq_g.value), _parse(sq_h.value), _parse(sq_k.value)
        _top = [_g[_f[_a]] for _a in range(3)]
        _bottom = [_k[_h[_a]] for _a in range(3)]
        _commutes = _top == _bottom
        _color = "#15803d" if _commutes else "#b91c1c"

        _fig = draw_diagram(
            {"A": (0, 1.8, r"$A$"), "B": (2.4, 1.8, r"$B$"), "C": (0, 0, r"$C$"), "D": (2.4, 0, r"$D$")},
            [
                ("A", "B", r"$f$", {"color": _color}),
                ("B", "D", r"$g$", {"color": _color}),
                ("A", "C", r"$h$", {"side": -1, "color": _color}),
                ("C", "D", r"$k$", {"side": -1, "color": _color}),
            ],
            figsize=(4.0, 3.0),
            title="commutes" if _commutes else "does NOT commute",
        )

        _lines = [
            "| $a$ | $f(a)$ | $g(f(a))$ | $h(a)$ | $k(h(a))$ | paths agree at $a$? |",
            "|---|---|---|---|---|---|",
        ]
        for _a in range(3):
            _lines.append(
                "| " + str(_a) + " | " + str(_f[_a]) + " | **" + str(_top[_a]) + "** | " + str(_h[_a])
                + " | **" + str(_bottom[_a]) + "** | " + ("yes" if _top[_a] == _bottom[_a] else "**no**") + " |"
            )
        _lines.append("")
        if _commutes:
            _lines.append("**The square commutes:** $g \\circ f = k \\circ h$, because the two paths agree at every element of $A$.")
        else:
            _bad = [str(_a) for _a in range(3) if _top[_a] != _bottom[_a]]
            _lines.append(
                "**The square does not commute:** the two paths differ at $a = " + ", ".join(_bad)
                + "$. A single such element is a counterexample to $g \\circ f = k \\circ h$."
            )
        return mo.vstack([_fig, mo.md("\n".join(_lines))])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > References: [Leinster §1.1](https://arxiv.org/abs/1612.09375) (commutative diagrams are introduced alongside the definition of a category); [Riehl §1.6](https://math.jhu.edu/~eriehl/context.pdf).

    ---

    ## 6. Diagram Chasing

    A **diagram chase** is a proof that follows paths around a diagram, trading one path for another each time a region is known to commute. There are two styles. In an *equation chase* you rewrite composites using associativity and the given equations; no elements appear. In an *element chase* you pick an element at one node and follow where the arrows send it. The first style works in every category. The second needs elements, so it is available for sets, groups, vector spaces and the like. We do one of each.

    The first result is about the diagram below: two squares sharing an edge.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 1.8, r"$A$"), "B": (2.4, 1.8, r"$B$"), "C": (4.8, 1.8, r"$C$"),
            "A2": (0, 0, r"$A'$"), "B2": (2.4, 0, r"$B'$"), "C2": (4.8, 0, r"$C'$"),
        },
        [
            ("A", "B", r"$f$"),
            ("B", "C", r"$g$"),
            ("A2", "B2", r"$f'$", {"side": -1}),
            ("B2", "C2", r"$g'$", {"side": -1}),
            ("A", "A2", r"$a$", {"side": -1}),
            ("B", "B2", r"$b$"),
            ("C", "C2", r"$c$"),
        ],
        figsize=(6.6, 3.2),
        title="Two squares pasted along b",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Proposition 5 (pasting squares).** In the diagram above, suppose the left square commutes, $b \circ f = f' \circ a$, and the right square commutes, $c \circ g = g' \circ b$. Then the outer rectangle commutes:
    > $$c \circ (g \circ f) = (g' \circ f') \circ a.$$

    **Goal.** The functions $c \circ (g \circ f)$ and $(g' \circ f') \circ a$, both from $A$ to $C'$, are equal.

    **Given.** The equations $b \circ f = f' \circ a$ and $c \circ g = g' \circ b$; associativity of composition (0B, Proposition 2).

    **Plan.** Equation chase. Start with the path along the top and down the right side. Re-bracket so that a composite appearing in one of the given equations is visible, replace it, and repeat. Each replacement pushes the vertical arrow one square to the left.

    **Proof.**

    $$\begin{aligned}
    c \circ (g \circ f) &= (c \circ g) \circ f && \text{associativity} \\
    &= (g' \circ b) \circ f && \text{right square} \\
    &= g' \circ (b \circ f) && \text{associativity} \\
    &= g' \circ (f' \circ a) && \text{left square} \\
    &= (g' \circ f') \circ a && \text{associativity.} \qquad \blacksquare
    \end{aligned}$$

    **What made it work.** At every line there was only one thing to do: find a sub-path that is one side of a commuting square and swap it for the other side. Associativity is what lets you regroup to expose that sub-path. In the picture, the path $A \to B \to C \to C'$ slides to $A \to B \to B' \to C'$ and then to $A \to A' \to B' \to C'$. The third line also shows that the middle path equals the outer two, so the whole diagram commutes in the sense of Section 5.

    **The converse is false.** If the outer rectangle commutes, the two squares need not. Take all six sets to be $\{0, 1\}$; let $f$, $f'$, $a$ and $c$ be the identity; let $g$ and $g'$ both be the constant function with value $0$; and let $b$ swap $0$ and $1$. The outer rectangle commutes: both paths are the constant function $0$. But the left square does not: $b \circ f$ is the swap and $f' \circ a$ is the identity, and these differ at $0$. (The cell after the next proposition verifies this.)

    For the element chase we need one more definition from group theory.

    > **Definition (kernel).** The *kernel* of a group homomorphism $\alpha \colon G \to G'$ is the set $\ker \alpha = \{x \in G : \alpha(x) = e_{G'}\}$.

    **Reading the definition.** To prove $x \in \ker \alpha$: check $x \in G$ and prove the equation $\alpha(x) = e_{G'}$. To use $x \in \ker \alpha$: you are handed that equation. **Example:** the kernel of reduction modulo $n$, $\mathbb{Z} \to \mathbb{Z}/n$, is the set of multiples of $n$. **Non-example:** for $\det \colon GL_n(\mathbb{R}) \to \mathbb{R} \setminus \{0\}$ the identity of the codomain is the number $1$, not $0$, so the kernel is the set of matrices of determinant $1$. The matrix $2I$ is not in it, since $\det(2I) = 2^n \neq 1$ for $n \ge 1$.

    > **Proposition 6 (a commuting square maps kernels to kernels).** Let $G, G', H, H'$ be groups and let $f \colon G \to H$, $f' \colon G' \to H'$, $\alpha \colon G \to G'$ and $\beta \colon H \to H'$ be group homomorphisms such that $\beta \circ f = f' \circ \alpha$. Then for every $x \in \ker \alpha$ we have $f(x) \in \ker \beta$.

    **Goal.** For all $x \in G$: if $\alpha(x) = e_{G'}$ then $\beta(f(x)) = e_{H'}$.

    **Given.** The equation of functions $\beta \circ f = f' \circ \alpha$; Proposition 2 applied to $f'$, which says $f'(e_{G'}) = e_{H'}$.

    **Plan.** Element chase. Start with $x$ in the top-left corner. We want to know where the path "across, then down" sends it. Commutativity lets us compute the path "down, then across" instead, and the hypothesis on $x$ tells us what "down" does.

    **Proof.** Let $x \in \ker \alpha$, so $\alpha(x) = e_{G'}$. Then

    $$\beta(f(x)) = (\beta \circ f)(x) = (f' \circ \alpha)(x) = f'(\alpha(x)) = f'(e_{G'}) = e_{H'}.$$

    The first and third equalities are the definition of composite; the second is the commutativity of the square; the fourth is the hypothesis on $x$; the fifth is Proposition 2 for the homomorphism $f'$. Hence $f(x) \in \ker \beta$. $\blacksquare$

    **What made it work.** We knew something about $x$ along one path ($\alpha$ kills it) and wanted something along the other path; commutativity is exactly the licence to switch paths. In an element chase, write under each node what you know about the element sitting there, and move along whichever arrow lets you use a hypothesis.

    > References: [Riehl §1.6](https://math.jhu.edu/~eriehl/context.pdf) (the art of the diagram chase).
    """)
    return


@app.cell
def _():
    def _run():
        # Check the counterexample to the converse of Proposition 5, and confirm
        # Proposition 5 itself by brute force over every choice of the seven functions on {0,1}.
        import itertools

        def _compose(g, f):
            return tuple(g[f[_x]] for _x in range(len(f)))

        _ident, _swap, _zero = (0, 1), (1, 0), (0, 0)
        _f, _fp, _a, _c, _g, _gp, _b = _ident, _ident, _ident, _ident, _zero, _zero, _swap
        print("Counterexample to the converse (all sets are {0,1}):")
        print(f"  left square commutes?   {_compose(_b, _f) == _compose(_fp, _a)}")
        print(f"  right square commutes?  {_compose(_c, _g) == _compose(_gp, _b)}")
        print(f"  outer rectangle commutes? {_compose(_c, _compose(_g, _f)) == _compose(_compose(_gp, _fp), _a)}")

        _maps = list(itertools.product(range(2), repeat=2))
        _both = _outer_given_both = _outer_total = 0
        for _f, _g, _fp, _gp, _a, _b, _c in itertools.product(_maps, repeat=7):
            _left = _compose(_b, _f) == _compose(_fp, _a)
            _right = _compose(_c, _g) == _compose(_gp, _b)
            _outer = _compose(_c, _compose(_g, _f)) == _compose(_compose(_gp, _fp), _a)
            _outer_total += _outer
            if _left and _right:
                _both += 1
                _outer_given_both += _outer
        print(f"\nAll 4^7 = {4 ** 7} diagrams of this shape on the set {{0,1}}:")
        print(f"  both squares commute in {_both} of them; the rectangle commutes in {_outer_given_both} of those")
        print(f"  the rectangle commutes in {_outer_total} diagrams altogether (more than {_both}: the converse fails)")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Unique up to Unique Isomorphism

    In 0A you saw that $\{\star\}$, $\{7\}$ and $\{\emptyset\}$ all satisfy the universal property of "the" one-element set. So a universal property does not determine a set. What it determines is described by a phrase that you will meet in every later Part, and this section proves an instance of it using nothing but the property itself.

    > **Definition (isomorphism of sets).** An *isomorphism* between sets $A$ and $B$ is an invertible function $u \colon A \to B$: a function for which there exists $v \colon B \to A$ with $v \circ u = 1_A$ and $u \circ v = 1_B$. If one exists we say $A$ and $B$ are *isomorphic* and write $A \cong B$.

    **Reading the definition.** To prove $u$ is an isomorphism, produce a function $v$ in the opposite direction and prove **two** equations of functions. (By brief 0B·P05, the isomorphisms of sets are exactly the bijections; we will not need that here.)

    > **Definition (terminal set).** A set $T$ is *terminal* if for every set $X$ there exists a unique function $X \to T$.

    **Reading the definition.** This is property (T) of 0A. Used as a hypothesis, "$T$ is terminal" gives you, **for any set $X$ you choose**, two separate tools: (E) a function $X \to T$ exists; (U) any two functions $X \to T$ are equal. The proof below uses both, and chooses $X$ three different ways. **Examples:** every one-element set (0A). **Non-examples:** $\emptyset$, for which (E) fails at $X = \{0\}$; $\{0, 1\}$, for which (U) fails at $X = \{0\}$.

    > **Theorem 7 (terminal sets are unique up to unique isomorphism).** Let $T$ and $T'$ be terminal sets. Then there is exactly one function $u \colon T \to T'$, and $u$ is an isomorphism.

    **Goal.** (1) There exists a unique function $u \colon T \to T'$. (2) There exists a function $v \colon T' \to T$ with $v \circ u = 1_T$ and $u \circ v = 1_{T'}$.

    **Given.** For every set $X$: there is a function $X \to T$, and any two functions $X \to T$ are equal. For every set $X$: there is a function $X \to T'$, and any two functions $X \to T'$ are equal. Nothing else. In particular we may **not** use that $T$ and $T'$ have one element; the point is to argue from the property alone.

    **Plan.** Get $u$ from the property of $T'$ and $v$ from the property of $T$. Then $v \circ u$ and $1_T$ are two functions from $T$ to $T$, and the uniqueness clause of $T$, applied with $X = T$ itself, says there is only one such function. The same for $u \circ v$ and $1_{T'}$.

    **Proof.** *Step 1.* Apply the property of $T'$ with $X = T$: there exists a unique function $T \to T'$. Call it $u$. This is claim (1).

    *Step 2.* Apply the property of $T$ with $X = T'$: there exists a function $T' \to T$. Call it $v$.

    *Step 3.* The composite $v \circ u$ is a function $T \to T$, and so is the identity $1_T$. Apply the uniqueness clause of the property of $T$ with $X = T$: any two functions $T \to T$ are equal. Hence $v \circ u = 1_T$.

    *Step 4.* The composite $u \circ v$ is a function $T' \to T'$, and so is $1_{T'}$. Apply the uniqueness clause of the property of $T'$ with $X = T'$: any two functions $T' \to T'$ are equal. Hence $u \circ v = 1_{T'}$.

    By Steps 3 and 4, $v$ is a two-sided inverse of $u$, so $u$ is an isomorphism. This is claim (2). $\blacksquare$

    **What made it work.** Two ideas. First, an object with a universal property can be **probed with itself**: taking $X = T$ shows that the only function $T \to T$ is the identity. Second, uniqueness clauses are how you prove equations between maps when you have no formula for the maps: we never computed $v \circ u$; we showed it had no choice. Compare Proposition 4: there the two candidates gave $m \le m'$ and $m' \le m$ and antisymmetry finished; here they give $u$ and $v$ and the uniqueness clause finishes.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"T": (0, 0, r"$T$"), "T2": (3.0, 0, r"$T'$")},
        [
            ("T", "T2", r"$u$", {"rad": -0.3, "dashed": True}),
            ("T2", "T", r"$v$", {"rad": -0.3, "dashed": True}),
            ("T", "T", r"$1_T$", {"loop": "left"}),
            ("T2", "T2", r"$1_{T'}$", {"loop": "right"}),
        ],
        figsize=(6.4, 2.8),
        title="v after u can only be the identity of T; u after v the identity of T'",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What the phrase means.** Suppose some property picks out certain objects. The objects with the property are

    - **unique** if any two of them are equal;
    - **unique up to isomorphism** if any two of them are isomorphic;
    - **unique up to unique isomorphism** if between any two of them there is exactly one isomorphism that respects the data of the property.

    Theorem 7 is the third kind, and in fact says more: there is only one *function* $T \to T'$ of any sort. For terminal sets the property comes with no extra data, so "respects the data" asks nothing. For other universal properties it matters. A product of $A$ and $B$ (0A) comes with its two projections, and between two products of the same pair of sets there are in general many bijections, but only one that is compatible with the projections. Making that precise and proving it is brief P06.

    **A non-example.** Consider the property "has exactly two elements". Any two sets with this property are isomorphic, so such sets are unique up to isomorphism. But they are not unique up to *unique* isomorphism: between $\{0, 1\}$ and $\{a, b\}$ there are two bijections, and nothing in the property prefers one. This is why category theory cares about the stronger phrase. When the isomorphism is unique, identifying the two objects involves no choice, and it is safe to say "the" terminal set or "the" product.

    > References: [Leinster, Introduction (Ch 0)](https://arxiv.org/abs/1612.09375) proves a uniqueness result of exactly this shape; [Hammack Ch 7](https://www.people.vcu.edu/~rhammack/BookOfProof/) for the existence-and-uniqueness pattern.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Proving uniqueness by exhibiting one map.** "The map $h(x) = (f(x), g(x))$ works, so it is the unique map." *Diagnosis:* that is (E) only. A uniqueness proof must contain a sentence that begins "Let $h'$ be any map with the property".
    2. **Giving the arbitrary candidate the features of the constructed one.** In the uniqueness half, writing "since $h'(x) = (f(x), g(x))$ ..." before it has been derived. *Diagnosis:* the second candidate is known only through the stated property; anything else about it has to be proved from that.
    3. **Using a commutativity that was not given.** Swapping one path for another around a region of the diagram that has not been shown to commute. *Diagnosis:* list the equations the hypotheses actually provide (Section 5, step 2) and cite one of them at each swap.
    4. **Running an arrow backwards.** Writing $f^{-1}$, or "the element that $f$ sends to $y$", when $f$ is not known to be invertible. *Diagnosis:* arrows may only be followed in their own direction; going backwards along $f$ needs surjectivity (to find a preimage) and injectivity (for the preimage to be unambiguous).
    5. **Saying "unique" when only "unique up to isomorphism" is true.** "The one-element set", "the product" are figures of speech. *Diagnosis:* ask whether two objects with the property must be *equal*. If not, the correct statement names the isomorphism between them and says in what sense it is unique.
    6. **Forgetting the identity condition for monoid homomorphisms.** Checking only $f(a \cdot b) = f(a) \cdot f(b)$. *Diagnosis:* for groups this suffices (Proposition 2); for monoids it does not, as the map $n \mapsto 0$ on $(\mathbb{Z}, \times, 1)$ shows.

    ---

    ## Why This Matters

    - **Every universal property ends in "unique".** Adjunctions (Part 2), representations (Part 4) and limits (Part 5) are all defined by a sentence of the form "for every ... there exists a unique map such that ...". The proofs there are the (E)/(U) split of Section 1, and the uniqueness of the object itself is Theorem 7 with different nouns.
    - **"Probe the object with itself"** is the engine of the Yoneda lemma (4B), where the technique appears as "follow the identity".
    - **Diagrams are the notation of the subject.** Naturality (1D) is a commuting square, the triangle identities (2B) are commuting triangles, and cones (5A) are families of commuting triangles. Pasting squares, Proposition 5, is how natural transformations are composed.
    - **Equation chases are the only chases that survive.** From Module 1A, arrows need not be functions, so there may be no elements to chase. Proposition 5 used only associativity and so holds in every category; Proposition 6 used elements and is specific to groups.
    - **The table of Section 4 becomes the list of standard categories** in 1A: $\mathbf{Set}$, $\mathbf{Mon}$, $\mathbf{Grp}$, $\mathbf{Vect}_k$, $\mathbf{Top}$, and posets with monotone maps. A single monoid and a single poset will also each turn out to *be* a category.
    - **Posets are the testing ground.** In a poset, "unique up to isomorphism" collapses to "unique" by antisymmetry, so every big theorem of the course has a small poset version that can be checked by hand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Structure Exercises

    Functions on finite sets are encoded as dictionaries, as in 0B. Each skeleton runs as it stands; replace the `...` placeholders, then un-comment the `print` lines and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Completing a Square

    Write `square_commutes(f, g, h, k)` for a square with $f \colon A \to B$, $g \colon B \to D$, $h \colon A \to C$, $k \colon C \to D$. Then, with $f$, $g$ and $k$ fixed as below, count the functions $h \colon A \to C$ that make the square commute.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(domain, codomain):
            for _vals in itertools.product(codomain, repeat=len(domain)):
                yield dict(zip(domain, _vals))

        def square_commutes(f, g, h, k):
            # TODO: True exactly when g∘f and k∘h agree at every element of the domain of f
            _result = ...
            return _result

        A, B, C, D = [0, 1, 2], [0, 1, 2], [0, 1, 2, 3], [0, 1]
        f = {0: 0, 1: 1, 2: 1}             # A -> B
        g = {0: 0, 1: 1, 2: 1}             # B -> D
        k = {0: 0, 1: 0, 2: 1, 3: 1}       # C -> D

        # TODO: the list of all h : A -> C for which the square commutes
        completions = ...

        # print(square_commutes(f, g, {0: 0, 1: 2, 2: 3}, k))    # expect True
        # print(square_commutes(f, g, {0: 0, 1: 2, 2: 1}, k))    # expect False
        # print(len(completions))                                # expect 8

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Counting Homomorphisms

    Write `is_hom(phi, m, n)`, which decides whether a function $\varphi \colon \mathbb{Z}/m \to \mathbb{Z}/n$ (a dictionary on `range(m)`) satisfies $\varphi(x + y) = \varphi(x) + \varphi(y)$, with the sum on the left taken modulo $m$ and the sum on the right modulo $n$. Count the homomorphisms for a few $(m, n)$, and confirm Proposition 2 on all of them.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(domain, codomain):
            for _vals in itertools.product(codomain, repeat=len(domain)):
                yield dict(zip(domain, _vals))

        def is_hom(phi, m, n):
            # TODO: True exactly when phi[(x + y) % m] == (phi[x] + phi[y]) % n for all x, y in range(m)
            _result = ...
            return _result

        def homs(m, n):
            return [_phi for _phi in all_functions(range(m), range(n)) if is_hom(_phi, m, n)]

        # print(len(homs(4, 6)))     # expect 2
        # print(len(homs(6, 6)))     # expect 6
        # print(len(homs(5, 3)))     # expect 1
        # print(len(homs(6, 3)))     # expect 3
        # print(all(phi[0] == 0 for phi in homs(6, 6)))   # expect True  (Proposition 2)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: How Many Greatest Lower Bounds?

    In a poset $P$, a *lower bound* of elements $a$ and $b$ is an $x \in P$ with $x \le a$ and $x \le b$. A *greatest lower bound* of $a$ and $b$ is a lower bound $m$ such that $x \le m$ for every lower bound $x$. Work in sets of positive integers ordered by divisibility ($x \le y$ means $x$ divides $y$). Write `lower_bounds` and `greatest_lower_bounds`, each returning a list, and find the largest number of greatest lower bounds any pair has.
    """)
    return


@app.cell
def _():
    def _run():
        def leq(x, y):
            """x <= y in the divisibility order."""
            return y % x == 0

        def lower_bounds(P, a, b):
            # TODO: the list of all x in P with x <= a and x <= b
            _result = ...
            return _result

        def greatest_lower_bounds(P, a, b):
            # TODO: the list of all lower bounds m of a, b such that every lower bound x has x <= m
            _result = ...
            return _result

        P = [1, 2, 3, 4, 6, 12]
        Q = [2, 3, 12, 18]

        # print(lower_bounds(P, 4, 6))                 # expect [1, 2]
        # print(greatest_lower_bounds(P, 4, 6))        # expect [2]
        # print(greatest_lower_bounds(P, 12, 6))       # expect [6]
        # print(lower_bounds(Q, 12, 18))               # expect [2, 3]
        # print(greatest_lower_bounds(Q, 12, 18))      # expect []
        # print(max(len(greatest_lower_bounds(R, a, b)) for R in (P, Q) for a in R for b in R))   # expect 1

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six briefs. None of these statements is proved in the lecture; each uses one of the three shapes: unpack the definition, existence and uniqueness, diagram chase.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | `exercises/0c/p01_unique_solution_in_a_group.md` | warm-up | existence and uniqueness |
    | P02 | `exercises/0c/p02_meets_are_unique.md` | warm-up | uniqueness from antisymmetry |
    | P03 | `exercises/0c/p03_homomorphisms_preserve_inverses.md` | core | direct calculation, then an appeal to uniqueness |
    | P04 | `exercises/0c/p04_inverting_a_commutative_square.md` | core | diagram chase (equation chase) |
    | P05 | `exercises/0c/p05_injectivity_across_a_square.md` | core | diagram chase (element chase) |
    | P06 | `exercises/0c/p06_products_unique_up_to_unique_iso.md` | stretch | unique up to unique isomorphism |

    **Submitting a proof.** Write it in `proofs/0c/<same filename as the brief>` using the five steps (Goal, Given, Plan, Proof, What made it work), then ask Claude to review it.
    The review points at gaps and asks questions; it does not supply a model proof. Revise until there are no gaps.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [0B: Proof Toolkit I: Definitions & Direct Proof](../0b_proof_toolkit_definitions/) &nbsp;|&nbsp; Next: [1A: Categories](../1a_categories/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
