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
    # 7A: Definition & Theorem Study Guide

    > *"Category theory takes a bird's eye view of mathematics. From high in the sky, details become invisible, but we can spot patterns that were impossible to detect from ground level."*
    > — Tom Leinster, Basic Category Theory

    This module is **not** a lecture. It is the map of the course: every definition and every main theorem from modules 0B to 6D, stated precisely and in one place, with a line on how each theorem is proved and a note on where it is used later.

    Use it in two ways.

    - **As a study guide.** Pick a Part in the dropdown below and read one module at a time. For each definition, cover the statement and try to write it out with its quantifiers before you look. For each theorem, read the statement, then try to say which *kind* of proof it has before you read the "Idea" line.
    - **As a reference.** When you are writing a proof in `proofs/` and need the exact wording of a definition, or you want to know which hypothesis a theorem needs ("does this require $\mathcal{A}$ to be locally small?"), look it up here.

    What this guide deliberately does **not** contain is proofs. The lectures prove their theorems in full; here you get the statement and at most a one-line idea and the name of a technique. For a result that is set as a proof exercise, only the technique is named: the idea is yours to find. If a one-line idea is not enough for you to reconstruct the argument, that is the signal to go back to the lecture, not a gap in the guide.

    The guide has five sections: notation (§1), the module-by-module catalogue with its filter (§2), pictures of the main universal properties (§3), a table comparing those universal properties (§4), and a catalogue of the proof techniques of the course (§5).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Notation

    The course uses Leinster's conventions throughout.

    | Notation | Meaning | Introduced |
    |----------|---------|------------|
    | $\mathcal{A}, \mathcal{B}, \mathcal{C}$ | categories | 1A |
    | $\mathrm{ob}(\mathcal{A})$; $A \in \mathcal{A}$ | the objects of $\mathcal{A}$; "$A$ is an object of $\mathcal{A}$" | 1A |
    | $\mathcal{A}(A, B)$ | the maps from $A$ to $B$ in $\mathcal{A}$ (a hom-set when $\mathcal{A}$ is locally small) | 1A |
    | $f \colon A \to B$ | a map with domain $A$ and codomain $B$ | 1A |
    | $g \circ f$, $gf$ | composite, "$g$ after $f$": first $f$, then $g$ | 0B, 1A |
    | $1_A$ | the identity map on $A$ | 1A |
    | $A \cong B$ | $A$ and $B$ are isomorphic | 1B |
    | $\mathcal{A}^{\mathrm{op}}$ | the opposite category | 1B |
    | $\mathcal{A} \times \mathcal{B}$ | the product category | 1B |
    | $\mathbf{Set}, \mathbf{Grp}, \mathbf{Ab}, \mathbf{Mon}, \mathbf{Vect}_k, \mathbf{Top}$ | sets, groups, abelian groups, monoids, vector spaces over a field $k$, topological spaces, each with its structure-preserving maps | 1A |
    | $\mathbf{Cat}$ | small categories and functors | 1C, 3A |
    | $F \colon \mathcal{A} \to \mathcal{B}$ | a functor | 1C |
    | $\alpha \colon F \Rightarrow G$, with components $\alpha_A$ | a natural transformation | 1D |
    | $[\mathcal{A}, \mathcal{B}]$ | the functor category: functors $\mathcal{A} \to \mathcal{B}$ and natural transformations | 1D |
    | $\mathcal{A} \simeq \mathcal{B}$ | $\mathcal{A}$ and $\mathcal{B}$ are equivalent | 1E |
    | $F \dashv G$ | $F$ is left adjoint to $G$; always $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ | 2A |
    | $\bar{f}$ | the transpose of $f$ across an adjunction (in either direction) | 2A |
    | $\eta$, $\varepsilon$ | unit $1_{\mathcal{A}} \Rightarrow GF$ and counit $FG \Rightarrow 1_{\mathcal{B}}$ of an adjunction | 2B |
    | $(P \Rightarrow Q)$, $(A \Rightarrow G)$ | comma categories | 2C |
    | $\mathcal{A}/A$, $A/\mathcal{A}$ | slice and coslice categories | 2C |
    | $B^A$ | the set of functions from $A$ to $B$; in a cartesian closed category, the exponential | 3A, 6C |
    | $H^A = \mathcal{A}(A, -)$ | the **covariant** representable $\mathcal{A} \to \mathbf{Set}$ | 4A |
    | $H_A = \mathcal{A}(-, A)$ | the **contravariant** representable $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ | 4A |
    | $H_\bullet$ | the Yoneda embedding $\mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ | 4A, 4C |
    | $X \times Y$, $X + Y$ | product and sum (coproduct) | 5A, 5B |
    | $1$, $0$ | terminal object and initial object | 2A, 5A, 5B |
    | $\mathbf{I}$, $D \colon \mathbf{I} \to \mathcal{A}$ | a small category used as a shape, and a diagram of that shape | 5A |
    | $\lim D$, $\operatorname{colim} D$ | (the vertex of) a limit cone, a colimit cocone | 5A, 5B |
    | $\Delta$ | the diagonal functor $\mathcal{A} \to [\mathbf{I}, \mathcal{A}]$ | 6A |
    | $\mathrm{Cone}(A, D)$ | the set of cones on $D$ with vertex $A$ | 6A |
    | $\mathbf{E}(X)$ | the category of elements of a presheaf $X$ | 6B |
    | $(T, \eta, \mu)$ | a monad | 6D |
    | $\mathcal{C}^T$, $\mathcal{C}_T$ | the Eilenberg–Moore and Kleisli categories of a monad $T$ on $\mathcal{C}$ | 6D |

    Two reading habits that prevent most notational slips:

    - In $g \circ f$ the map on the **right** is applied first. In a chain $A \xrightarrow{f} B \xrightarrow{g} C$ the composite is written $g \circ f$.
    - $H^A$ (index up) has $A$ in the **first** slot of the hom-set and is covariant; $H_A$ (index down) has $A$ in the **second** slot and is contravariant.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. The Catalogue, Module by Module

    Every module entry below has the same four blocks:

    - **Definitions** — stated with their quantifiers. These are what you unpack at the start of a proof.
    - **Theorems** — the statement, then *Idea* (one line on why it is true) and *Technique* (which of the proof shapes of §5 it uses).
    - **Standard examples** — the ones worth knowing by heart, including non-examples.
    - **Used later in** — where the module's material is needed again.

    Standing conventions: "map" means a map (arrow, morphism) of the category in question; "exactly one" and "a unique" mean the same thing; and in an adjunction $F \dashv G$ the left adjoint is always $F \colon \mathcal{A} \to \mathcal{B}$.

    Choose a Part to show. "All" shows the whole course.
    """)
    return


@app.function(hide_code=True)
def build_guide():
    """The catalogue: a list of (part, module id, markdown) triples, in course order."""
    _L = "https://arxiv.org/abs/1612.09375"
    _R = "https://math.jhu.edu/~eriehl/context.pdf"
    _H = "https://www.people.vcu.edu/~rhammack/BookOfProof/"
    _guide = []

    # ------------------------------------------------------------------ Part 0
    _guide.append(("0", "0B", r"""
    ### 0B: Proof Toolkit I — Definitions & Direct Proof

    *Sources: [Hammack Ch 4–6, 12](HAMMACK) · [Leinster §3.1](LEINSTER)*

    **Definitions**

    - **Function.** A function $f \colon A \to B$ assigns to each $a \in A$ exactly one element $f(a) \in B$. The domain $A$ and the codomain $B$ are part of the data.
    - **Equality of functions.** $f = g$ means: $f$ and $g$ have the same domain, the same codomain, and $f(a) = g(a)$ for all $a$ in the domain.
    - **Composite and identity.** For $f \colon A \to B$ and $g \colon B \to C$, the composite $g \circ f \colon A \to C$ is defined by $(g \circ f)(a) = g(f(a))$ for all $a \in A$. The identity $1_A \colon A \to A$ is defined by $1_A(a) = a$.
    - **Injective.** For all $a, a' \in A$: if $f(a) = f(a')$ then $a = a'$.
    - **Surjective.** For every $b \in B$ there exists $a \in A$ with $f(a) = b$.
    - **Bijective.** Injective and surjective.
    - **Left inverse, right inverse, inverse.** For $f \colon A \to B$: a left inverse is $g \colon B \to A$ with $g \circ f = 1_A$; a right inverse is $h \colon B \to A$ with $f \circ h = 1_B$; an inverse is a map that is both.

    **Theorems**

    - **Composition is associative and unital.** $h \circ (g \circ f) = (h \circ g) \circ f$ and $f \circ 1_A = f = 1_B \circ f$. *Idea:* both sides have the same domain and codomain; evaluate both at an arbitrary $a$. *Technique:* equality of functions.
    - **Composites.** A composite of injections is injective; a composite of surjections is surjective. *Technique:* direct proof, unpacking the definition twice.
    - **Cancelling.** If $g \circ f$ is injective then $f$ is injective. If $g \circ f$ is surjective then $g$ is surjective. *Technique:* direct proof.
    - **Inverses and bijections.** $f$ has an inverse if and only if $f$ is bijective, and then the inverse is unique. For $A$ non-empty, $f$ has a left inverse if and only if $f$ is injective. $f$ has a right inverse if and only if $f$ is surjective (the "if" direction makes a choice of one preimage for each $b$, which for infinite sets is the axiom of choice). *Technique:* an "if and only if" is two proofs; "there exists" is proved by constructing.
    - **A left inverse and a right inverse agree.** If $g \circ f = 1_A$ and $f \circ h = 1_B$ then $g = h$. *Technique:* direct proof.

    **Standard examples.** $n \mapsto 2n$ on $\mathbb{Z}$ is injective, not surjective, and has many left inverses. $\mathbb{Z} \to \{0, 1\}$, $n \mapsto n \bmod 2$, is surjective, not injective. Non-example of equality: $x \mapsto x^2$ as a function $\mathbb{R} \to \mathbb{R}$ and as a function $\mathbb{R} \to [0, \infty)$ are different functions, because their codomains differ.

    **Used later in.** 1A (the axioms of a category are the first theorem here); 1B (isomorphism, monic and epic are the arrow-only versions of bijective, injective and surjective); 3A; every proof that two maps are equal.
    """))

    _guide.append(("0", "0C", r"""
    ### 0C: Proof Toolkit II — Uniqueness, Diagrams & Algebra Refresher

    *Sources: [Hammack Ch 7, 11](HAMMACK) · [Riehl §1.6](RIEHL)*

    **Definitions**

    - **"There exists a unique $x$ such that $P(x)$".** Two claims: (existence) there is an $x$ with $P(x)$; (uniqueness) for all $x, x'$, if $P(x)$ and $P(x')$ then $x = x'$.
    - **Unique up to isomorphism; up to unique isomorphism.** Objects with a given property are *unique up to isomorphism* if any two of them are isomorphic. They are *unique up to unique isomorphism* if between any two of them there is exactly one isomorphism compatible with the structure that the property refers to.
    - **Commutative diagram.** A diagram of objects and maps commutes if, for every pair of objects $X, Y$ in it, all composites along directed paths from $X$ to $Y$ are equal.
    - **Monoid.** A set $M$ with a binary operation $\cdot$ and an element $e \in M$ such that $(x \cdot y) \cdot z = x \cdot (y \cdot z)$ and $e \cdot x = x = x \cdot e$ for all $x, y, z \in M$. A **monoid homomorphism** $f \colon M \to N$ satisfies $f(x \cdot y) = f(x) \cdot f(y)$ for all $x, y$, and $f(e_M) = e_N$.
    - **Group.** A monoid in which every $x$ has an inverse: an element $x^{-1}$ with $x \cdot x^{-1} = e = x^{-1} \cdot x$. A **group homomorphism** satisfies $f(x \cdot y) = f(x) \cdot f(y)$ for all $x, y$.
    - **Preorder, poset.** A preorder is a set with a relation $\le$ that is reflexive ($x \le x$) and transitive ($x \le y$ and $y \le z$ imply $x \le z$). A poset (partially ordered set) is a preorder that is also antisymmetric ($x \le y$ and $y \le x$ imply $x = y$). An **order-preserving map** satisfies: $x \le y$ implies $f(x) \le f(y)$.
    - **Linear map.** For vector spaces $V, W$ over a field $k$: a function $f \colon V \to W$ with $f(v + v') = f(v) + f(v')$ and $f(\lambda v) = \lambda f(v)$ for all $v, v' \in V$, $\lambda \in k$.
    - **Continuous map.** For topological spaces $X, Y$: a function $f \colon X \to Y$ such that for every open $U \subseteq Y$, the preimage $f^{-1}(U)$ is open in $X$.

    **Theorems**

    - **Identity elements and inverses are unique.** A monoid has exactly one identity element; an element of a group has exactly one inverse. *Idea:* take two and combine them. *Technique:* uniqueness argument.
    - **Group homomorphisms preserve identity and inverses.** If $f(xy) = f(x)f(y)$ for all $x, y$ then $f(e) = e$ and $f(x^{-1}) = f(x)^{-1}$. For monoids, $f(e) = e$ does not follow and must be required. *Technique:* direct proof.
    - **Pasting.** If two adjacent squares commute, then so does the outer rectangle. *Technique:* diagram chase.
    - **The one-element set.** For every set $X$ there is exactly one function $X \to \{\ast\}$; any two one-element sets are isomorphic by exactly one bijection. *Technique:* existence and uniqueness. This is the first universal property of the course.

    **Standard examples.** $(\mathbb{N}, +, 0)$ is a monoid that is not a group. Divisibility on the positive integers is a poset; divisibility on all non-zero integers is a preorder that is not a poset, since $2 \mid -2$ and $-2 \mid 2$. The inclusion $(\mathbb{N}, +) \to (\mathbb{Z}, +)$ is a monoid homomorphism.

    **Used later in.** Uniqueness arguments: 1A, 1B, 2C, 4C, and every universal property in Parts 5 and 6. Diagram chasing: 1D onwards. The algebra refresher supplies the examples of every module.
    """))

    # ------------------------------------------------------------------ Part 1
    _guide.append(("1", "1A", r"""
    ### 1A: Categories

    *Sources: [Leinster §1.1](LEINSTER) · [Riehl §1.1](RIEHL)*

    **Definitions**

    - **Category.** A category $\mathcal{A}$ consists of:
        - a collection $\mathrm{ob}(\mathcal{A})$ of **objects**;
        - for each pair of objects $A, B$, a collection $\mathcal{A}(A, B)$ of **maps** from $A$ to $B$;
        - for each triple of objects $A, B, C$, a function $\mathcal{A}(B, C) \times \mathcal{A}(A, B) \to \mathcal{A}(A, C)$, written $(g, f) \mapsto g \circ f$, called **composition**;
        - for each object $A$, an element $1_A \in \mathcal{A}(A, A)$, the **identity** on $A$;

        such that **associativity** holds: for all $f \in \mathcal{A}(A, B)$, $g \in \mathcal{A}(B, C)$, $h \in \mathcal{A}(C, D)$, we have $(h \circ g) \circ f = h \circ (g \circ f)$; and the **identity laws** hold: for all $f \in \mathcal{A}(A, B)$, we have $f \circ 1_A = f = 1_B \circ f$.
    - **Domain and codomain.** If $f \in \mathcal{A}(A, B)$ then $A$ is the domain and $B$ the codomain of $f$. Every map has exactly one of each.
    - **Discrete category.** A category in which the only maps are identities.
    - **A monoid as a category.** A category with exactly one object is the same thing as a monoid: the maps are the elements, composition is the operation, the identity map is the identity element.
    - **A preorder as a category.** A category in which, for each pair of objects $A, B$, there is at most one map $A \to B$. Write $A \le B$ when there is one. Composition gives transitivity, identities give reflexivity. A poset is a preorder in which $A \le B$ and $B \le A$ imply $A = B$.

    **Theorems**

    - **Identities are unique.** If $e \in \mathcal{A}(A, A)$ satisfies $f \circ e = f$ for all maps $f$ out of $A$ and $e \circ g = g$ for all maps $g$ into $A$, then $e = 1_A$. *Technique:* uniqueness argument, as for monoids in 0C.
    - **Each standard example is a category.** *Idea:* for categories of sets with structure, one must check that composites of structure-preserving maps and identity functions are structure-preserving; associativity and the identity laws are then inherited from functions (0B). *Technique:* verifying axioms.

    **Standard examples.** $\mathbf{Set}$, $\mathbf{Grp}$, $\mathbf{Ab}$, $\mathbf{Mon}$, $\mathbf{Vect}_k$, $\mathbf{Top}$. A group or monoid as a one-object category. A poset such as the subsets of a set under $\subseteq$. The empty category; the category $\mathbf{1}$ with one object and one map. Non-example: sets and injections do form a category, but sets with "functions that are not surjective" do not, because identities are missing.

    **Used later in.** Everything. The habit to keep: a claim "this is a category" is a list of things to check, and "composition is well defined" (the composite lands in the right collection) is on that list.
    """))

    _guide.append(("1", "1B", r"""
    ### 1B: Isomorphisms, Duality & New Categories from Old

    *Sources: [Leinster §1.1](LEINSTER) · [Riehl §1.1–1.2](RIEHL)*

    **Definitions**

    - **Isomorphism.** A map $f \colon A \to B$ is an isomorphism if there exists a map $g \colon B \to A$ with $g \circ f = 1_A$ and $f \circ g = 1_B$. Such a $g$ is called the inverse of $f$ and written $f^{-1}$. Objects $A, B$ are isomorphic, $A \cong B$, if there exists an isomorphism $A \to B$.
    - **Monic (monomorphism).** $f \colon A \to B$ is monic if for all objects $X$ and all maps $x, x' \colon X \to A$: $f \circ x = f \circ x'$ implies $x = x'$.
    - **Epic (epimorphism).** $f \colon A \to B$ is epic if for all objects $Z$ and all maps $z, z' \colon B \to Z$: $z \circ f = z' \circ f$ implies $z = z'$.
    - **Split monic, split epic.** $f$ is split monic if it has a left inverse ($g \circ f = 1_A$ for some $g$) and split epic if it has a right inverse.
    - **Opposite category.** $\mathcal{A}^{\mathrm{op}}$ has the same objects as $\mathcal{A}$, with $\mathcal{A}^{\mathrm{op}}(B, A) = \mathcal{A}(A, B)$, the same identities, and composition reversed.
    - **Principle of duality.** Every definition, theorem and proof about categories has a dual, obtained by reversing every arrow. If a statement holds in all categories then so does its dual.
    - **Product category.** $\mathcal{A} \times \mathcal{B}$ has objects the pairs $(A, B)$ and maps $(A, B) \to (A', B')$ the pairs $(f, g)$ with $f \colon A \to A'$ in $\mathcal{A}$ and $g \colon B \to B'$ in $\mathcal{B}$; composition and identities are componentwise.
    - **Groupoid.** A category in which every map is an isomorphism. A group is the same thing as a one-object groupoid.

    **Theorems**

    - **Inverses are unique.** If $g$ and $g'$ are both inverses of $f$ then $g = g'$. *Technique:* uniqueness argument (compute $g \circ f \circ g'$ in two ways).
    - **Isomorphism is an equivalence relation on objects.** Identities are isomorphisms; the inverse of an isomorphism is an isomorphism; a composite of isomorphisms is an isomorphism. *Technique:* exhibit the inverse and check both equations.
    - **Isomorphisms are monic and epic; the converse fails.** *Idea:* cancel by composing with the inverse. The inclusion $\mathbb{N} \to \mathbb{Z}$ in $\mathbf{Mon}$ is monic and epic but not an isomorphism.
    - **Split monics are monic; split epics are epic; a map that is split monic and epic is an isomorphism.** *Technique:* direct proof.
    - **In $\mathbf{Set}$:** monic $\iff$ injective, epic $\iff$ surjective, isomorphism $\iff$ bijective. *Idea:* for "monic implies injective", test against maps out of a one-element set. *Technique* for the epic statement: proof by contrapositive.
    - **Composites.** A composite of monics is monic. If $g \circ f$ is monic then $f$ is monic. Dually: a composite of epics is epic, and if $g \circ f$ is epic then $g$ is epic. *Technique:* prove the monic statements; **dualize** for the epic ones.

    **Standard examples.** Isomorphisms in $\mathbf{Grp}$ are the bijective homomorphisms; isomorphisms in $\mathbf{Top}$ are the homeomorphisms, and a bijective continuous map need not be one. In a poset regarded as a category, every map is monic and epic, and the only isomorphisms are identities. The opposite of a poset is the poset with the order reversed.

    **Used later in.** Duality: 5B is the dual of 5A, and every "dually" in Parts 2 and 6. Monic and epic: 5A, 5B (characterisation by pullbacks and pushouts). Isomorphism: every "unique up to isomorphism" statement.
    """))

    _guide.append(("1", "1C", r"""
    ### 1C: Functors

    *Sources: [Leinster §1.2](LEINSTER) · [Riehl §1.3](RIEHL)*

    **Definitions**

    - **Functor.** A functor $F \colon \mathcal{A} \to \mathcal{B}$ consists of a function $\mathrm{ob}(\mathcal{A}) \to \mathrm{ob}(\mathcal{B})$, written $A \mapsto F(A)$, and for each pair $A, A' \in \mathcal{A}$ a function $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$, written $f \mapsto F(f)$, such that $F(f' \circ f) = F(f') \circ F(f)$ whenever $f, f'$ are composable in $\mathcal{A}$, and $F(1_A) = 1_{F(A)}$ for every $A \in \mathcal{A}$.
    - **Contravariant functor.** A contravariant functor from $\mathcal{A}$ to $\mathcal{B}$ is a functor $\mathcal{A}^{\mathrm{op}} \to \mathcal{B}$: a map $f \colon A \to A'$ is sent to $F(f) \colon F(A') \to F(A)$, and $F(f' \circ f) = F(f) \circ F(f')$.
    - **Presheaf.** A presheaf on $\mathcal{A}$ is a functor $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$.
    - **Faithful, full.** $F$ is faithful (respectively full) if for each pair $A, A' \in \mathcal{A}$ the function $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$, $f \mapsto F(f)$, is injective (respectively surjective).
    - **Essentially surjective on objects.** For every $B \in \mathcal{B}$ there exists $A \in \mathcal{A}$ with $F(A) \cong B$.
    - **Subcategory; full subcategory.** A subcategory of $\mathcal{A}$ is a choice of some objects and some maps between them, closed under composition and identities. It is full if it contains every map of $\mathcal{A}$ between its chosen objects.
    - **$\mathbf{Cat}$.** The category of small categories (see 3A) and functors, with composition of functors and identity functors.
    - **Forgetful and free functors (informal).** A forgetful functor forgets structure or properties, for instance $U \colon \mathbf{Grp} \to \mathbf{Set}$ sending a group to its set of elements. Free functors go the other way, for instance $F \colon \mathbf{Set} \to \mathbf{Grp}$ sending a set to the free group on it. The precise relationship is $F \dashv U$ (2A).

    **Theorems**

    - **Functors preserve isomorphisms.** If $f$ is an isomorphism in $\mathcal{A}$ then $F(f)$ is an isomorphism in $\mathcal{B}$, with inverse $F(f^{-1})$; hence $A \cong A'$ implies $F(A) \cong F(A')$. *Technique:* direct proof.
    - **Functors compose.** The composite of functors $\mathcal{A} \to \mathcal{B} \to \mathcal{C}$ is a functor, and composition of functors is associative and unital. *Technique:* verifying functoriality.
    - **Functors between monoids and between posets.** Between one-object categories, functors are exactly monoid homomorphisms. Between posets regarded as categories, functors are exactly order-preserving maps. *Technique:* unpack the definition in each case.
    - **Warning about faithful.** Faithful is a condition on each hom-set separately. A faithful functor may send two different maps with different domains or codomains to the same map, and need not be injective on objects.

    **Standard examples.** Forgetful functors $\mathbf{Grp} \to \mathbf{Set}$ (faithful, not full), $\mathbf{Ab} \to \mathbf{Grp}$ (full and faithful). For a group $G$ regarded as a one-object category, a functor $G \to \mathbf{Set}$ is a set with a left $G$-action. Contravariant: the dual space $(-)^{\ast} \colon \mathbf{Vect}_k^{\mathrm{op}} \to \mathbf{Vect}_k$; the power set with inverse image $\mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$. The hom-functors $\mathcal{A}(A, -)$ and $\mathcal{A}(-, A)$ (4A). Non-example: sending each group to its centre does not extend to a functor $\mathbf{Grp} \to \mathbf{Grp}$ acting on homomorphisms by restriction, because a homomorphism need not map centre into centre.

    **Used later in.** 1D, 1E (full, faithful and essentially surjective characterise equivalences); 4A–4C (hom-functors and the Yoneda embedding); 5C (functors and limits).
    """))

    _guide.append(("1", "1D", r"""
    ### 1D: Natural Transformations

    *Sources: [Leinster §1.3](LEINSTER) · [Riehl §1.4](RIEHL)*

    **Definitions**

    - **Natural transformation.** Let $F, G \colon \mathcal{A} \to \mathcal{B}$ be functors. A natural transformation $\alpha \colon F \Rightarrow G$ is a family $(\alpha_A \colon F(A) \to G(A))_{A \in \mathcal{A}}$ of maps in $\mathcal{B}$ such that for every map $f \colon A \to A'$ in $\mathcal{A}$, $$\alpha_{A'} \circ F(f) = G(f) \circ \alpha_A.$$ The maps $\alpha_A$ are the **components**; the equation says that the **naturality square** for $f$ commutes.
    - **Vertical composition.** For $\alpha \colon F \Rightarrow G$ and $\beta \colon G \Rightarrow H$ (all functors $\mathcal{A} \to \mathcal{B}$), $(\beta \circ \alpha)_A = \beta_A \circ \alpha_A$. The identity $1_F$ has components $1_{F(A)}$.
    - **Functor category.** $[\mathcal{A}, \mathcal{B}]$ has the functors $\mathcal{A} \to \mathcal{B}$ as objects and natural transformations as maps, with vertical composition.
    - **Natural isomorphism.** An isomorphism in $[\mathcal{A}, \mathcal{B}]$. The phrase "$F(A) \cong G(A)$ **naturally in** $A$" means that there is a natural isomorphism $F \Rightarrow G$.
    - **Horizontal composition.** For $\alpha \colon F \Rightarrow G$ between functors $\mathcal{A} \to \mathcal{B}$ and $\alpha' \colon F' \Rightarrow G'$ between functors $\mathcal{B} \to \mathcal{C}$, the natural transformation $\alpha' \ast \alpha \colon F'F \Rightarrow G'G$ has components $$(\alpha' \ast \alpha)_A = \alpha'_{G(A)} \circ F'(\alpha_A) = G'(\alpha_A) \circ \alpha'_{F(A)}.$$ Special cases: $F'\alpha$ with components $F'(\alpha_A)$, and $\alpha' F$ with components $\alpha'_{F(A)}$.

    **Theorems**

    - **Natural isomorphisms are componentwise.** $\alpha \colon F \Rightarrow G$ is a natural isomorphism if and only if $\alpha_A$ is an isomorphism in $\mathcal{B}$ for every $A \in \mathcal{A}$. *Technique:* diagram chase.
    - **$[\mathcal{A}, \mathcal{B}]$ is a category.** *Technique:* verifying axioms, component by component (**pointwise argument**).
    - **The two formulas for $\alpha' \ast \alpha$ agree.** *Idea:* this is the naturality square of $\alpha'$ at the map $\alpha_A$.
    - **Interchange law.** $(\beta' \circ \alpha') \ast (\beta \circ \alpha) = (\beta' \ast \beta) \circ (\alpha' \ast \alpha)$ whenever both sides are defined. *Technique:* pasting naturality squares.

    **Standard examples.** The determinant: for each commutative ring $R$, $\det_R \colon M_n(R) \to R$ is a homomorphism of multiplicative monoids, natural in $R$. The canonical map $V \to V^{\ast\ast}$ is natural in $V \in \mathbf{Vect}_k$, and is an isomorphism when $V$ is finite-dimensional. Reversal of finite sequences is a natural transformation from the functor "finite sequences in a set" to itself. For a group $G$, natural transformations between functors $G \to \mathbf{Set}$ are the $G$-equivariant maps. For order-preserving maps $F, G$ between posets there is at most one natural transformation $F \Rightarrow G$, and there is one exactly when $F(a) \le G(a)$ for all $a$.

    **Used later in.** 1E (equivalence), 2A (naturality of the adjunction bijection), 2B (unit, counit, triangle identities use $F\eta$ and $\varepsilon F$), 4B (the Yoneda lemma is about natural transformations out of $H_A$), 6A (cones are natural transformations).
    """))

    _guide.append(("1", "1E", r"""
    ### 1E: Equivalence of Categories

    *Sources: [Leinster §1.3](LEINSTER) · [Riehl §1.5](RIEHL)*

    **Definitions**

    - **Isomorphism of categories.** Functors $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ with $G \circ F = 1_{\mathcal{A}}$ and $F \circ G = 1_{\mathcal{B}}$ (an isomorphism in the category of categories).
    - **Equivalence of categories.** An equivalence between $\mathcal{A}$ and $\mathcal{B}$ consists of functors $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ together with natural isomorphisms $\eta \colon 1_{\mathcal{A}} \Rightarrow G \circ F$ and $\varepsilon \colon F \circ G \Rightarrow 1_{\mathcal{B}}$. If one exists, $\mathcal{A}$ and $\mathcal{B}$ are equivalent, $\mathcal{A} \simeq \mathcal{B}$, and $F$ and $G$ are each called *an equivalence*.
    - **Skeletal category; skeleton.** A category is skeletal if isomorphic objects are equal. A skeleton of $\mathcal{A}$ is a full subcategory containing exactly one object from each isomorphism class of objects of $\mathcal{A}$.
    - **Duality.** A duality between $\mathcal{A}$ and $\mathcal{B}$ is an equivalence $\mathcal{A}^{\mathrm{op}} \simeq \mathcal{B}$.

    **Theorems**

    - **Characterisation of equivalences.** A functor is an equivalence if and only if it is full, faithful and essentially surjective on objects. *Idea:* for "if", choose for each $B \in \mathcal{B}$ an object $G(B)$ and an isomorphism $\varepsilon_B \colon F(G(B)) \to B$; fullness and faithfulness then determine $G$ on maps. The choice uses the axiom of choice. *Technique:* building an inverse up to isomorphism.
    - **Full and faithful functors as inclusions.** If $F \colon \mathcal{C} \to \mathcal{D}$ is full and faithful then $\mathcal{C}$ is equivalent to the full subcategory of $\mathcal{D}$ whose objects are those of the form $F(C)$. *Idea:* the previous theorem, applied to $F$ with its codomain cut down.
    - **Skeletons.** The inclusion of a skeleton into $\mathcal{A}$ is an equivalence. *Idea:* it is full and faithful by definition and essentially surjective by construction.
    - **Equivalence is an equivalence relation on categories.** *Technique:* composing natural isomorphisms (horizontal composition, 1D).

    **Standard examples.** The category of finite sets is equivalent to its full subcategory on the sets $\{1, \dots, n\}$, $n \ge 0$; the two are not isomorphic. $\mathbf{FDVect}_k$ is equivalent to the category whose objects are the natural numbers and whose maps $n \to m$ are $m \times n$ matrices over $k$. Taking duals gives a duality $\mathbf{FDVect}_k^{\mathrm{op}} \simeq \mathbf{FDVect}_k$. Non-example: a functor that is full and faithful but not essentially surjective, such as $\mathbf{Ab} \to \mathbf{Grp}$.

    **Used later in.** 2B (an equivalence is a special adjunction once $\eta$, $\varepsilon$ are suitably chosen); 3A (essentially small); 4C (the Yoneda embedding identifies $\mathcal{A}$ with a full subcategory of presheaves); 6D (monadic functors).
    """))

    # ------------------------------------------------------------------ Part 2
    _guide.append(("2", "2A", r"""
    ### 2A: Adjunctions — Definition & Examples

    *Sources: [Leinster §2.1](LEINSTER) · [Riehl §4.1](RIEHL)*

    **Definitions**

    - **Adjunction.** Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be functors. $F$ is **left adjoint** to $G$, and $G$ **right adjoint** to $F$, written $F \dashv G$, if $$\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$$ naturally in $A \in \mathcal{A}$ and $B \in \mathcal{B}$. An **adjunction** between $F$ and $G$ is a choice of such a natural isomorphism.
    - **Transpose.** The map corresponding to $g \colon F(A) \to B$ is written $\bar{g} \colon A \to G(B)$, and the map corresponding to $f \colon A \to G(B)$ is written $\bar{f} \colon F(A) \to B$. So $\bar{\bar{g}} = g$ and $\bar{\bar{f}} = f$.
    - **Naturality, spelled out.** For all $g \colon F(A) \to B$ and $q \colon B \to B'$: $\overline{q \circ g} = G(q) \circ \bar{g}$. For all $f \colon A \to G(B)$ and $p \colon A' \to A$: $\overline{f \circ p} = \bar{f} \circ F(p)$.
    - **Initial object, terminal object.** An object $I$ of $\mathcal{A}$ is initial if for every $A \in \mathcal{A}$ there is exactly one map $I \to A$. An object $T$ is terminal if for every $A \in \mathcal{A}$ there is exactly one map $A \to T$.
    - **Galois connection.** For posets $A, B$ and order-preserving maps $f \colon A \to B$, $g \colon B \to A$: $f \dashv g$ means that for all $a \in A$, $b \in B$, $$f(a) \le b \iff a \le g(b).$$

    **Theorems**

    - **Initial objects are unique up to unique isomorphism.** If $I$ and $I'$ are initial then there is exactly one isomorphism $I \to I'$ (indeed exactly one map). Dually for terminal objects. *Idea:* the only map $I \to I$ is $1_I$. *Technique:* uniqueness argument; this is the prototype for every "unique up to unique isomorphism" proof.
    - **Initial and terminal objects as adjoints.** Let $\mathbf{1}$ be the category with one object and one map. The unique functor $\mathcal{A} \to \mathbf{1}$ has a left adjoint if and only if $\mathcal{A}$ has an initial object, and a right adjoint if and only if $\mathcal{A}$ has a terminal object. *Technique:* unpack the definition.
    - **Adjunctions compose.** Given $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$ and $F' \dashv G'$ with $F' \colon \mathcal{B} \to \mathcal{C}$, we have $F' F \dashv G G'$. *Technique:* working with transposes.
    - **In a poset, naturality is automatic.** For order-preserving maps between posets, the condition $f(a) \le b \iff a \le g(b)$ is the whole definition, because any two maps with the same domain and codomain are equal.

    **Standard examples.** Free $\dashv$ forgetful for $\mathbf{Mon}$, $\mathbf{Grp}$, $\mathbf{Vect}_k$ over $\mathbf{Set}$: a homomorphism out of a free object is the same as a function out of the generating set. For $\mathbf{Top}$: $D \dashv U \dashv I$, where $D$ gives a set the discrete topology and $I$ the indiscrete one. Abelianization is left adjoint to the inclusion $\mathbf{Ab} \to \mathbf{Grp}$. Currying: for each set $B$, $(- \times B) \dashv (-)^B$ on $\mathbf{Set}$. Galois connection: for a function $p \colon X \to Y$, direct image and inverse image between the power sets satisfy $p(S) \subseteq T \iff S \subseteq p^{-1}(T)$.

    **Used later in.** 2B and 2C give two more descriptions of the same notion. 4A (adjunctions give representables), 6A (limits as an adjoint), 6C (adjoints and limits), 6D (monads from adjunctions).
    """))

    _guide.append(("2", "2B", r"""
    ### 2B: Units & Counits

    *Sources: [Leinster §2.2](LEINSTER) · [Riehl §4.2](RIEHL)*

    **Definitions**

    - **Unit and counit.** Given an adjunction $F \dashv G$: the unit is $\eta \colon 1_{\mathcal{A}} \Rightarrow G F$ with $\eta_A = \overline{1_{F(A)}} \colon A \to G(F(A))$, and the counit is $\varepsilon \colon F G \Rightarrow 1_{\mathcal{B}}$ with $\varepsilon_B = \overline{1_{G(B)}} \colon F(G(B)) \to B$.
    - **Triangle identities.** For all $A \in \mathcal{A}$ and $B \in \mathcal{B}$: $$\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}, \qquad G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}.$$ In the notation of 1D: $\varepsilon F \circ F \eta = 1_F$ and $G \varepsilon \circ \eta G = 1_G$.
    - **Closure operator.** On a poset $A$: an order-preserving map $c \colon A \to A$ with $a \le c(a)$ and $c(c(a)) \le c(a)$ for all $a \in A$ (so $c(c(a)) = c(a)$).

    **Theorems**

    - **The unit and counit are natural and satisfy the triangle identities.** *Idea:* each identity is the naturality of the adjunction bijection applied to an identity map. *Technique:* follow the identity.
    - **Transposes from the unit and counit.** For every $g \colon F(A) \to B$, $\bar{g} = G(g) \circ \eta_A$. For every $f \colon A \to G(B)$, $\bar{f} = \varepsilon_B \circ F(f)$. *Idea:* write $g = g \circ 1_{F(A)}$ and use naturality. *Technique:* follow the identity.
    - **Two descriptions of an adjunction.** Given functors $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$, there is a one-to-one correspondence between adjunctions $F \dashv G$ (natural isomorphisms $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$) and pairs of natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$, $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$ satisfying the triangle identities. *Idea:* the previous theorem gives the formulas in one direction; the triangle identities are exactly what makes the two formulas mutually inverse. *Technique:* translating between two definitions.
    - **Poset case.** For order-preserving maps $f \colon A \to B$, $g \colon B \to A$ between posets: $f \dashv g$ if and only if $a \le g(f(a))$ for all $a \in A$ and $f(g(b)) \le b$ for all $b \in B$. The triangle identities hold automatically.
    - **Closure operators from Galois connections.** If $f \dashv g$ between posets then $g \circ f$ is a closure operator on $A$; moreover $f g f = f$ and $g f g = g$. *Technique:* two inequalities give an equality (antisymmetry).

    **Standard examples.** For free $\dashv$ forgetful on groups: $\eta_A$ is the insertion of generators $A \to U(F(A))$, and $\varepsilon_G \colon F(U(G)) \to G$ evaluates a formal word in $G$. For $(- \times B) \dashv (-)^B$ on $\mathbf{Set}$: $\varepsilon$ is evaluation $C^B \times B \to C$. For direct and inverse image along $p \colon X \to Y$: the closure operator is $S \mapsto p^{-1}(p(S))$.

    **Used later in.** 2C (the unit as a universal arrow), 6C, and 6D, where $(GF, \eta, G \varepsilon F)$ is the monad of the adjunction.
    """))

    _guide.append(("2", "2C", r"""
    ### 2C: Adjunctions via Initial Objects

    *Sources: [Leinster §2.3](LEINSTER) · [Riehl §2.4, §4.6](RIEHL)*

    **Definitions**

    - **Comma category.** Given functors $P \colon \mathcal{A} \to \mathcal{C}$ and $Q \colon \mathcal{B} \to \mathcal{C}$, the comma category $(P \Rightarrow Q)$ has as objects the triples $(A, h, B)$ with $A \in \mathcal{A}$, $B \in \mathcal{B}$ and $h \colon P(A) \to Q(B)$ in $\mathcal{C}$. A map $(A, h, B) \to (A', h', B')$ is a pair $(f \colon A \to A', \; g \colon B \to B')$ with $Q(g) \circ h = h' \circ P(f)$.
    - **Slice and coslice.** For $A \in \mathcal{A}$, the slice category $\mathcal{A}/A$ has objects the pairs $(X, h \colon X \to A)$; a map $(X, h) \to (X', h')$ is a map $f \colon X \to X'$ with $h' \circ f = h$. The coslice category $A/\mathcal{A}$ is the dual: objects are maps out of $A$.
    - **The category $(A \Rightarrow G)$.** For $G \colon \mathcal{B} \to \mathcal{A}$ and $A \in \mathcal{A}$: objects are pairs $(B, f \colon A \to G(B))$ with $B \in \mathcal{B}$; a map $(B, f) \to (B', f')$ is a map $q \colon B \to B'$ in $\mathcal{B}$ with $G(q) \circ f = f'$.
    - **Universal arrow.** A universal arrow from $A$ to $G$ is an initial object of $(A \Rightarrow G)$: a pair $(B_0, u \colon A \to G(B_0))$ such that for every $B \in \mathcal{B}$ and every $f \colon A \to G(B)$ there is exactly one $q \colon B_0 \to B$ with $G(q) \circ u = f$.

    **Theorems**

    - **The unit is initial.** Given an adjunction $F \dashv G$ with unit $\eta$, for every $A \in \mathcal{A}$ the pair $(F(A), \eta_A)$ is an initial object of $(A \Rightarrow G)$. *Idea:* the required unique $q$ is the transpose of $f$, by the formula $\bar{g} = G(g) \circ \eta_A$ of 2B. *Technique:* initial-object argument.
    - **Adjunctions from initial objects.** Given $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$, there is a one-to-one correspondence between adjunctions $F \dashv G$ and natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ such that $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$ for every $A \in \mathcal{A}$.
    - **Existence of a left adjoint.** A functor $G \colon \mathcal{B} \to \mathcal{A}$ has a left adjoint if and only if $(A \Rightarrow G)$ has an initial object for every $A \in \mathcal{A}$. *Idea:* choose an initial object $(F(A), \eta_A)$ for each $A$; the universal property then defines $F$ on maps and forces functoriality and naturality. *Technique:* universal-property argument (define a map by its universal property, prove equations by uniqueness).
    - **Adjoints are unique.** If $F \dashv G$ and $F' \dashv G$ then $F \cong F'$; dually, right adjoints are unique up to natural isomorphism. *Idea:* $(F(A), \eta_A)$ and $(F'(A), \eta'_A)$ are both initial in $(A \Rightarrow G)$. *Technique:* uniqueness up to unique isomorphism. (A second proof appears in 4C.)

    **Standard examples.** The free vector space on a set $S$, with the insertion of $S$ as a basis, is a universal arrow from $S$ to the forgetful functor $\mathbf{Vect}_k \to \mathbf{Set}$: this is the statement "a linear map is determined by its values on a basis, and any values may be chosen". The slice $\mathbf{Set}/I$ is equivalent to the category of $I$-indexed families of sets. In a poset $P$, the slice $P/a$ is the down-set of $a$.

    **Used later in.** 4C (universal elements), 5A (a limit is a terminal cone), 6C (the general adjoint functor theorem is stated in terms of $(A \Rightarrow G)$), 6D.
    """))

    # ------------------------------------------------------------------ Part 3
    _guide.append(("3", "3A", r"""
    ### 3A: Sets & Size

    *Sources: [Leinster §3.1–3.3](LEINSTER) · [Riehl §1.1](RIEHL)*

    **Definitions**

    - **Constructions with sets.** The empty set $\emptyset$ and a one-element set $1$. The product $A \times B$ (ordered pairs). The sum $A + B$ (disjoint union). The function set $B^A = \mathbf{Set}(A, B)$. The two-element set $2 = \{\mathrm{true}, \mathrm{false}\}$.
    - **Characteristic function.** For $S \subseteq A$, the function $\chi_S \colon A \to 2$ with $\chi_S(a) = \mathrm{true}$ if and only if $a \in S$.
    - **Equalizer (of sets).** For $f, g \colon A \to B$, the subset $\{a \in A : f(a) = g(a)\}$ of $A$.
    - **Quotient.** For an equivalence relation $\sim$ on $A$, the set $A/{\sim}$ of equivalence classes, with the quotient map $p \colon A \to A/{\sim}$.
    - **Small, locally small, large.** A category is **small** if the collection of all its maps is a set, and **large** otherwise. It is **locally small** if for each pair of objects $A, B$ the collection $\mathcal{A}(A, B)$ is a set; that set is then called a **hom-set**.
    - **Essentially small.** Equivalent to some small category.
    - **$\mathbf{Cat}$ and $\mathbf{CAT}$.** $\mathbf{Cat}$ is the category of small categories and functors; $\mathbf{CAT}$ is the (very large) category of all categories.

    **Theorems**

    - **Subsets and maps into $2$.** $S \mapsto \chi_S$ is a bijection between the subsets of $A$ and the functions $A \to 2$. *Technique:* explicit bijection (write down both directions, check both composites).
    - **Currying.** $\mathbf{Set}(A \times B, C) \cong \mathbf{Set}(A, C^B)$, naturally in $A$ and $C$. *Technique:* explicit bijection.
    - **Universal property of the quotient.** For every function $f \colon A \to B$ such that $a \sim a'$ implies $f(a) = f(a')$, there is exactly one function $\bar{f} \colon A/{\sim} \to B$ with $\bar{f} \circ p = f$. *Technique:* existence and uniqueness.
    - **Cantor's theorem.** For every set $A$ there is no surjection $A \to \mathscr{P}(A)$. *Technique:* diagonal argument.
    - **$\mathbf{Set}$ is not small.** $\mathbf{Set}$ is locally small but not essentially small, hence not small. *Idea:* a set of sets always misses some set up to isomorphism, by Cantor's theorem applied to a set built from all of them.

    **Standard examples.** A monoid or group as a one-object category, and any poset, are small. $\mathbf{Set}$, $\mathbf{Grp}$, $\mathbf{Vect}_k$, $\mathbf{Top}$ are locally small and not small. The category of finite sets is not small but is essentially small (1E). $\lvert A \times B \rvert = \lvert A \rvert \cdot \lvert B \rvert$, $\lvert A + B \rvert = \lvert A \rvert + \lvert B \rvert$, $\lvert B^A \rvert = \lvert B \rvert^{\lvert A \rvert}$ for finite sets.

    **Used later in.** "Locally small" is a hypothesis in 4A–4C (hom-functors take values in $\mathbf{Set}$) and "small" in 5A (shapes of diagrams), 6A, 6B (presheaves on a small category) and 6C (the adjoint functor theorems). The constructions reappear in 5A and 5B as limits and colimits in $\mathbf{Set}$.
    """))

    # ------------------------------------------------------------------ Part 4
    _guide.append(("4", "4A", r"""
    ### 4A: Representable Functors

    *Sources: [Leinster §4.1](LEINSTER) · [Riehl §2.1](RIEHL)*

    Throughout, $\mathcal{A}$ is a **locally small** category.

    **Definitions**

    - **$H^A$.** For $A \in \mathcal{A}$, the functor $H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$ sends an object $B$ to the set $\mathcal{A}(A, B)$ and a map $g \colon B \to B'$ to the function $\mathcal{A}(A, B) \to \mathcal{A}(A, B')$, $p \mapsto g \circ p$.
    - **Representable (covariant).** A functor $X \colon \mathcal{A} \to \mathbf{Set}$ is representable if $X \cong H^A$ for some $A \in \mathcal{A}$. A **representation** of $X$ is a choice of an object $A$ and a natural isomorphism between $H^A$ and $X$.
    - **$H_A$.** For $A \in \mathcal{A}$, the functor $H_A = \mathcal{A}(-, A) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ sends $B$ to $\mathcal{A}(B, A)$ and a map $g \colon B' \to B$ to the function $\mathcal{A}(B, A) \to \mathcal{A}(B', A)$, $p \mapsto p \circ g$.
    - **Representable (contravariant).** A presheaf $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ is representable if $X \cong H_A$ for some $A \in \mathcal{A}$.
    - **$H^f$ and $H_f$.** A map $f \colon A' \to A$ induces a natural transformation $H^f \colon H^A \Rightarrow H^{A'}$, $p \mapsto p \circ f$ (note the reversal). A map $f \colon A \to A'$ induces $H_f \colon H_A \Rightarrow H_{A'}$, $p \mapsto f \circ p$.
    - **Yoneda embedding.** The functor $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ with $A \mapsto H_A$ and $f \mapsto H_f$. Similarly $H^\bullet \colon \mathcal{A}^{\mathrm{op}} \to [\mathcal{A}, \mathbf{Set}]$.
    - **Generalized element.** A generalized element of $A$ of shape $S$ is a map $S \to A$.

    **Theorems**

    - **$H^A$, $H_A$, $H^\bullet$ and $H_\bullet$ are functors.** *Technique:* verifying functoriality.
    - **Adjunctions give representables.** Let $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$, both categories locally small, and let $A \in \mathcal{A}$. Then the functor $\mathcal{A}(A, G(-)) \colon \mathcal{B} \to \mathbf{Set}$ is representable, represented by $F(A)$. *Idea:* this is the adjunction isomorphism with $A$ held fixed. *Technique:* naturality in one variable.
    - **Set-valued functors with a left adjoint are representable.** If $G \colon \mathcal{A} \to \mathbf{Set}$ has a left adjoint $F$, then $G \cong H^{F(1)}$, where $1$ is a one-element set. *Idea:* $G(A) \cong \mathbf{Set}(1, G(A)) \cong \mathcal{A}(F(1), A)$.

    **Standard examples.** The forgetful functor $\mathbf{Grp} \to \mathbf{Set}$ is represented by $\mathbb{Z}$; $\mathbf{Mon} \to \mathbf{Set}$ by $\mathbb{N}$; $\mathbf{Vect}_k \to \mathbf{Set}$ by $k$; $\mathbf{Top} \to \mathbf{Set}$ by the one-point space. The identity functor on $\mathbf{Set}$ is represented by $1$. The contravariant power-set functor $\mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$ is represented by $2$. For vector spaces $U, V$, the functor sending $W$ to the set of bilinear maps $U \times V \to W$ is represented by $U \otimes V$. Non-example: the functor $\mathbf{Set} \to \mathbf{Set}$ that is constant at $\emptyset$ is not representable, because $H^A(A)$ always contains $1_A$.

    **Used later in.** 4B and 4C. In 6A a limit is a representation of a functor of cones; in 6B every presheaf is built from representables.
    """))

    _guide.append(("4", "4B", r"""
    ### 4B: The Yoneda Lemma

    *Sources: [Leinster §4.2](LEINSTER) · [Riehl §2.2](RIEHL)*

    **Definitions.** No new definitions. The lemma is about the set $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, X)$ of natural transformations from the representable $H_A$ to a presheaf $X$.

    **Theorems**

    - **The Yoneda lemma.** Let $\mathcal{A}$ be a locally small category. Then $$\boxed{[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, X) \cong X(A)}$$ naturally in $A \in \mathcal{A}$ and $X \in [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$.
        - *The two maps.* A natural transformation $\alpha \colon H_A \Rightarrow X$ is sent to the element $\alpha_A(1_A) \in X(A)$. An element $x \in X(A)$ is sent to the natural transformation $\tilde{x}$ whose component at $B$ is $\tilde{x}_B \colon \mathcal{A}(B, A) \to X(B)$, $f \mapsto (X(f))(x)$.
        - *What "naturally" means.* Both sides are functors $\mathcal{A}^{\mathrm{op}} \times [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}] \to \mathbf{Set}$ in the pair $(A, X)$, and the bijection is a natural isomorphism between them.
        - *Idea:* every $f \in H_A(B)$ is $H_A(f)$ applied to $1_A$, so naturality of $\alpha$ at $f$ forces $\alpha_B(f) = (X(f))(\alpha_A(1_A))$: the whole of $\alpha$ is determined by where it sends the identity. *Technique:* **follow the identity**.
    - **Covariant form.** For a locally small $\mathcal{A}$, $[\mathcal{A}, \mathbf{Set}](H^A, X) \cong X(A)$ naturally in $A \in \mathcal{A}$ and $X \in [\mathcal{A}, \mathbf{Set}]$. *Technique:* dualize (apply the lemma to $\mathcal{A}^{\mathrm{op}}$).
    - **A remark on size.** The category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ need not be locally small when $\mathcal{A}$ is not small, but the lemma shows that the particular collection $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, X)$ is a set.

    **Standard examples.**

    - *In a monoid.* Let $M$ be a monoid regarded as a one-object category. A presheaf is a set $X$ with a right $M$-action, the unique representable is $M$ acting on itself by right multiplication, and the lemma says that $M$-equivariant maps $M \to X$ correspond to elements of $X$ (the image of the identity element). Taking $X = M$ gives Cayley's theorem: $M$ is isomorphic to the monoid of equivariant maps $M \to M$, a submonoid of the monoid of all functions $M \to M$. For a group this embeds the group in a symmetric group.
    - *In a poset.* Let $P$ be a poset. $H_a(b)$ is a one-element set if $b \le a$ and empty otherwise, so $H_a$ is the down-set $\{b : b \le a\}$. For a down-set $D$ regarded as a presheaf, the lemma reads: $\{b : b \le a\} \subseteq D$ if and only if $a \in D$.

    **Used later in.** 4C draws the consequences. 6A, 6B and 6C use the lemma repeatedly, usually through the corollary "to prove $A \cong A'$, prove $H_A \cong H_{A'}$".
    """))

    _guide.append(("4", "4C", r"""
    ### 4C: Consequences of Yoneda

    *Sources: [Leinster §4.3](LEINSTER) · [Riehl §2.3](RIEHL)*

    Throughout, $\mathcal{A}$ is a **locally small** category.

    **Definitions**

    - **Universal element.** Let $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$. A universal element of $X$ is a pair $(A, u)$ with $A \in \mathcal{A}$ and $u \in X(A)$ such that for every $B \in \mathcal{A}$ and every $x \in X(B)$ there is exactly one map $\bar{x} \colon B \to A$ with $(X(\bar{x}))(u) = x$.
    - **Reflecting isomorphisms.** A functor $J$ reflects isomorphisms if, whenever $J(f)$ is an isomorphism, so is $f$.

    **Theorems**

    - **Representations are universal elements.** For $A \in \mathcal{A}$ and $u \in X(A)$, the natural transformation $\tilde{u} \colon H_A \Rightarrow X$ corresponding to $u$ under the Yoneda lemma is an isomorphism if and only if $(A, u)$ is a universal element. So a representation of $X$ is the same thing as a universal element of $X$. *Idea:* $\tilde{u}$ is an isomorphism exactly when each component $\tilde{u}_B$ is a bijection (1D), and "bijection" unpacks to "exactly one". *Technique:* translating between two definitions.
    - **The Yoneda embedding is full and faithful.** $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is full and faithful: every natural transformation $H_A \Rightarrow H_{A'}$ is $H_f$ for exactly one $f \colon A \to A'$. *Idea:* the Yoneda lemma with $X = H_{A'}$.
    - **Full and faithful functors and isomorphisms.** Let $J \colon \mathcal{A} \to \mathcal{B}$ be full and faithful. Then $J$ reflects isomorphisms, and for $A, A' \in \mathcal{A}$, every isomorphism $J(A) \to J(A')$ is $J(f)$ for exactly one isomorphism $f \colon A \to A'$; in particular $J(A) \cong J(A')$ implies $A \cong A'$. *Technique:* direct proof.
    - **Objects are determined by their hom-functors.** $H_A \cong H_{A'} \iff A \cong A'$, and $H^A \cong H^{A'} \iff A \cong A'$. In words: $A \cong A'$ if and only if $\mathcal{A}(B, A) \cong \mathcal{A}(B, A')$ naturally in $B$.
    - **Representing objects are unique.** If $H_A \cong X \cong H_{A'}$ then $A \cong A'$; if $(A, u)$ and $(A', u')$ are universal elements of $X$ then there is exactly one isomorphism $i \colon A \to A'$ with $(X(i))(u') = u$.
    - **Uniqueness of adjoints, again.** If $F \dashv G$ and $F' \dashv G$ then $F(A) \cong F'(A)$ naturally in $A$. *Idea:* $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B)) \cong \mathcal{B}(F'(A), B)$ naturally in $B$. *Technique:* **Yoneda-style proof** — compare hom-functors instead of objects.

    **Standard examples.** For a poset $P$ the Yoneda embedding sends $a$ to its down-set, and "full and faithful" says $a \le b \iff \{c : c \le a\} \subseteq \{c : c \le b\}$. The universal element of the forgetful functor $\mathbf{Grp} \to \mathbf{Set}$ (covariant case) is $1 \in \mathbb{Z}$: for every group $G$ and every $x \in G$ there is exactly one homomorphism $\mathbb{Z} \to G$ sending $1$ to $x$. The universal element for bilinear maps out of $U \times V$ is the bilinear map $U \times V \to U \otimes V$.

    **Used later in.** 5A (a limit cone is a universal element), 6A, 6C (the proof that right adjoints preserve limits is a chain of natural isomorphisms followed by this module's corollary).
    """))

    # ------------------------------------------------------------------ Part 5
    _guide.append(("5", "5A", r"""
    ### 5A: Limits

    *Sources: [Leinster §5.1](LEINSTER) · [Riehl §3.1–3.2](RIEHL)*

    **Definitions**

    - **Product.** A product of objects $X, Y$ of $\mathcal{A}$ is an object $P$ with maps $p_1 \colon P \to X$, $p_2 \colon P \to Y$ such that for every object $A$ and every pair of maps $f_1 \colon A \to X$, $f_2 \colon A \to Y$ there is exactly one map $f \colon A \to P$ with $p_1 \circ f = f_1$ and $p_2 \circ f = f_2$. More generally, a product of a family $(X_i)_{i \in I}$ is an object $P$ with maps $p_i \colon P \to X_i$ such that every family $(f_i \colon A \to X_i)_{i \in I}$ factors as $f_i = p_i \circ f$ for exactly one $f \colon A \to P$. A product of the empty family is a terminal object.
    - **Equalizer.** An equalizer of $s, t \colon X \to Y$ is an object $E$ with a map $i \colon E \to X$ such that $s \circ i = t \circ i$, and for every object $A$ and every map $f \colon A \to X$ with $s \circ f = t \circ f$ there is exactly one map $\bar{f} \colon A \to E$ with $i \circ \bar{f} = f$.
    - **Pullback.** A pullback of maps $s \colon X \to Z$, $t \colon Y \to Z$ is an object $P$ with maps $p_1 \colon P \to X$, $p_2 \colon P \to Y$ such that $s \circ p_1 = t \circ p_2$, and for every object $A$ and maps $f_1 \colon A \to X$, $f_2 \colon A \to Y$ with $s \circ f_1 = t \circ f_2$ there is exactly one map $f \colon A \to P$ with $p_1 \circ f = f_1$ and $p_2 \circ f = f_2$.
    - **Diagram.** For a small category $\mathbf{I}$, a diagram of shape $\mathbf{I}$ in $\mathcal{A}$ is a functor $D \colon \mathbf{I} \to \mathcal{A}$.
    - **Cone.** A cone on $D$ is an object $A \in \mathcal{A}$ (the vertex) with a family of maps $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ such that $D(u) \circ f_I = f_J$ for every map $u \colon I \to J$ in $\mathbf{I}$.
    - **Limit.** A limit of $D$ is a cone $(p_I \colon L \to D(I))_{I \in \mathbf{I}}$ such that for every cone $(f_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$ there is exactly one map $\bar{f} \colon A \to L$ with $p_I \circ \bar{f} = f_I$ for all $I \in \mathbf{I}$. The maps $p_I$ are the projections.
    - **Having limits.** $\mathcal{A}$ has limits of shape $\mathbf{I}$ if every diagram of shape $\mathbf{I}$ has a limit; it has all limits (is complete) if this holds for every small $\mathbf{I}$, and finite limits if it holds for every finite $\mathbf{I}$.

    **Theorems**

    - **Limits are unique up to unique isomorphism.** If $(p_I \colon L \to D(I))$ and $(p'_I \colon L' \to D(I))$ are both limit cones on $D$, there is exactly one map $i \colon L \to L'$ with $p'_I \circ i = p_I$ for all $I$, and it is an isomorphism. *Technique:* uniqueness argument, exactly as for initial objects (2A).
    - **Limits in $\mathbf{Set}$.** Every diagram $D \colon \mathbf{I} \to \mathbf{Set}$ with $\mathbf{I}$ small has a limit, namely $$\Bigl\{ (x_I)_{I \in \mathbf{I}} \in \prod_{I \in \mathbf{I}} D(I) \; : \; (D(u))(x_I) = x_J \text{ for every } u \colon I \to J \text{ in } \mathbf{I} \Bigr\}$$ with the projections $(x_I)_{I} \mapsto x_J$. *Technique:* existence and uniqueness of the mediating function.
    - **All limits from products and equalizers.** If $\mathcal{A}$ has all products and all equalizers then it has all limits. If $\mathcal{A}$ has binary products, a terminal object and equalizers then it has all finite limits. *Idea:* the formula for limits in $\mathbf{Set}$ describes a limit as an equalizer of two maps between products; that description makes sense in any category.
    - **Monics via pullbacks.** A map $f \colon X \to Y$ is monic if and only if the square with both projections $1_X \colon X \to X$ is a pullback of $f$ along $f$. *Technique:* unpack both definitions and compare.
    - **Equalizers are monic.** If $i \colon E \to X$ is an equalizer of some pair of maps then $i$ is monic. *Technique:* universal-property argument.

    **Standard examples.** In $\mathbf{Set}$: the cartesian product; the equalizer $\{x : s(x) = t(x)\}$; the pullback $\{(x, y) \in X \times Y : s(x) = t(y)\}$, with inverse images and intersections of subsets as special cases. In $\mathbf{Grp}$, $\mathbf{Vect}_k$ and $\mathbf{Top}$: the product is the cartesian product with componentwise operations, respectively the product topology. The kernel of a group homomorphism $\theta$ is the equalizer of $\theta$ and the homomorphism sending everything to the identity element. In a poset: a product is a meet (greatest lower bound) and the terminal object is a greatest element. Non-example: the category of fields has no terminal object and no product of $\mathbb{F}_2$ with $\mathbb{F}_3$, since there are no homomorphisms between fields of different characteristic.

    **Used later in.** 5B (dual), 5C, and all of Part 6.
    """))

    _guide.append(("5", "5B", r"""
    ### 5B: Colimits

    *Sources: [Leinster §5.2](LEINSTER) · [Riehl §3.1, §3.5](RIEHL)*

    **Definitions**

    - **Sum (coproduct).** A sum of $X, Y$ is an object $S$ with maps $i_1 \colon X \to S$, $i_2 \colon Y \to S$ such that for every object $A$ and maps $f_1 \colon X \to A$, $f_2 \colon Y \to A$ there is exactly one map $f \colon S \to A$ with $f \circ i_1 = f_1$ and $f \circ i_2 = f_2$. A sum of the empty family is an initial object.
    - **Coequalizer.** A coequalizer of $s, t \colon X \to Y$ is an object $C$ with a map $p \colon Y \to C$ such that $p \circ s = p \circ t$, and for every object $A$ and map $f \colon Y \to A$ with $f \circ s = f \circ t$ there is exactly one map $\bar{f} \colon C \to A$ with $\bar{f} \circ p = f$.
    - **Pushout.** A pushout of maps $s \colon Z \to X$, $t \colon Z \to Y$ is an object $P$ with maps $i_1 \colon X \to P$, $i_2 \colon Y \to P$ such that $i_1 \circ s = i_2 \circ t$, and for every object $A$ and maps $f_1 \colon X \to A$, $f_2 \colon Y \to A$ with $f_1 \circ s = f_2 \circ t$ there is exactly one map $f \colon P \to A$ with $f \circ i_1 = f_1$ and $f \circ i_2 = f_2$.
    - **Cocone.** A cocone on $D \colon \mathbf{I} \to \mathcal{A}$ is an object $A$ with a family $(f_I \colon D(I) \to A)_{I \in \mathbf{I}}$ such that $f_J \circ D(u) = f_I$ for every map $u \colon I \to J$ in $\mathbf{I}$.
    - **Colimit.** A colimit of $D$ is a cocone $(p_I \colon D(I) \to C)_{I \in \mathbf{I}}$ such that for every cocone $(f_I \colon D(I) \to A)_{I \in \mathbf{I}}$ there is exactly one map $\bar{f} \colon C \to A$ with $\bar{f} \circ p_I = f_I$ for all $I$. Equivalently: a limit of the diagram $D^{\mathrm{op}} \colon \mathbf{I}^{\mathrm{op}} \to \mathcal{A}^{\mathrm{op}}$.

    **Theorems**

    - **Duality.** Every theorem of 5A has a dual. In particular colimits are unique up to unique isomorphism, and a category with all sums and all coequalizers has all colimits. *Technique:* dualize.
    - **Colimits in $\mathbf{Set}$.** Every diagram $D \colon \mathbf{I} \to \mathbf{Set}$ with $\mathbf{I}$ small has a colimit, namely the quotient $\bigl( \sum_{I \in \mathbf{I}} D(I) \bigr) / {\sim}$, where $\sim$ is the equivalence relation generated by $x \sim (D(u))(x)$ for all $u \colon I \to J$ in $\mathbf{I}$ and $x \in D(I)$. *Idea:* a cocone is a function out of the disjoint union that respects these identifications; apply the universal property of the quotient (3A).
    - **Coequalizers in $\mathbf{Set}$.** The coequalizer of $s, t \colon X \to Y$ is $Y/{\sim}$ with $\sim$ generated by $s(x) \sim t(x)$ for $x \in X$.
    - **Epics via pushouts.** A map $f \colon X \to Y$ is epic if and only if the square with both coprojections $1_Y \colon Y \to Y$ is a pushout of $f$ along $f$. *Technique:* dualize the statement about monics in 5A.
    - **Coequalizers are epic.** *Technique:* dualize.

    **Standard examples.** In $\mathbf{Set}$: disjoint union; quotient by a generated equivalence relation; the pushout of the inclusions $X \cap Y \to X$ and $X \cap Y \to Y$ is $X \cup Y$. In $\mathbf{Vect}_k$: the direct sum $X \oplus Y$ is both the sum and the product of $X$ and $Y$. In $\mathbf{Grp}$: the sum is the free product, whose underlying set is not the disjoint union. In $\mathbf{Top}$: disjoint unions, quotient spaces, and gluing along a subspace as a pushout. In a poset: a sum is a join (least upper bound) and the initial object is a least element.

    **Used later in.** 5C, 6B (every presheaf is a colimit of representables), 6C (left adjoints preserve colimits).
    """))

    _guide.append(("5", "5C", r"""
    ### 5C: Functors & Limits

    *Sources: [Leinster §5.3](LEINSTER) · [Riehl §3.3, §3.8](RIEHL)*

    **Definitions.** Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor and $\mathbf{I}$ a small category.

    - **Preserves.** $F$ preserves limits of shape $\mathbf{I}$ if for every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every cone $(p_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$: if $(p_I)$ is a limit cone on $D$, then $(F(p_I) \colon F(A) \to F(D(I)))_{I \in \mathbf{I}}$ is a limit cone on $F \circ D$.
    - **Reflects.** $F$ reflects limits of shape $\mathbf{I}$ if for every $D$ and every cone $(p_I)$ on $D$: if $(F(p_I))$ is a limit cone on $F \circ D$, then $(p_I)$ is a limit cone on $D$.
    - **Creates.** $F$ creates limits of shape $\mathbf{I}$ if for every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every limit cone $(q_I \colon B \to F(D(I)))_{I \in \mathbf{I}}$ on $F \circ D$, there is exactly one cone $(p_I \colon A \to D(I))_{I \in \mathbf{I}}$ on $D$ with $F(A) = B$ and $F(p_I) = q_I$ for all $I$, and this cone is a limit cone on $D$. (This is Leinster's definition; Riehl uses a slightly different one.)
    - The same three definitions with cocones and colimits.

    **Theorems**

    - **Creation gives existence and preservation.** If $\mathcal{B}$ has all limits of shape $\mathbf{I}$ and $F \colon \mathcal{A} \to \mathcal{B}$ creates them, then $\mathcal{A}$ has all limits of shape $\mathbf{I}$ and $F$ preserves them. *Technique:* unpack the definition, then use uniqueness of limits.
    - **Forgetful functors from algebra create limits.** The forgetful functors from $\mathbf{Grp}$, $\mathbf{Ab}$, $\mathbf{Mon}$ and $\mathbf{Vect}_k$ to $\mathbf{Set}$ create all limits. *Idea:* on the limit of the underlying sets there is exactly one algebraic structure making every projection a homomorphism, namely the componentwise one.
    - **Full and faithful functors reflect limits.** If $F$ is full and faithful then $F$ reflects all limits and colimits. *Technique:* existence from fullness, uniqueness from faithfulness.
    - **Limits in functor categories are pointwise.** Stated precisely and proved in 6B.
    - **Limits commute with limits.** Let $\mathbf{I}$ and $\mathbf{J}$ be small categories and $\mathcal{A}$ a locally small category with limits of shape $\mathbf{I}$ and of shape $\mathbf{J}$. Then for every $D \colon \mathbf{I} \times \mathbf{J} \to \mathcal{A}$, $$\lim_{J} \lim_{I} D(I, J) \;\cong\; \lim_{(I, J)} D(I, J) \;\cong\; \lim_{I} \lim_{J} D(I, J),$$ and all of these limits exist. *Technique:* Yoneda-style, by comparing cones (the tools are in 6A and 6B).

    **Standard examples.** The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ preserves all limits but not sums (the underlying set of a free product is not a disjoint union) and not the initial object (the one-element group is initial in $\mathbf{Grp}$, but its underlying set is not empty). The forgetful functor $\mathbf{Top} \to \mathbf{Set}$ preserves both limits and colimits. Limits do not in general commute with colimits: in $\mathbf{Set}$, $(A + B) \times (C + D)$ is not isomorphic to $(A \times C) + (B \times D)$ when all four sets have one element.

    **Used later in.** 6A (representables preserve limits), 6B, 6C (adjoints preserve limits; preservation of limits is the hypothesis of the adjoint functor theorems).
    """))

    # ------------------------------------------------------------------ Part 6
    _guide.append(("6", "6A", r"""
    ### 6A: Limits via Representables & Adjoints

    *Sources: [Leinster §6.1–6.2](LEINSTER) · [Riehl §3.4](RIEHL)*

    **Definitions.** Let $\mathbf{I}$ be a small category.

    - **Diagonal functor.** $\Delta \colon \mathcal{A} \to [\mathbf{I}, \mathcal{A}]$ sends an object $A$ to the constant functor $\Delta A$ (every object of $\mathbf{I}$ goes to $A$, every map to $1_A$) and a map $f$ to the natural transformation with every component equal to $f$.
    - **Cones as natural transformations.** A cone on $D \colon \mathbf{I} \to \mathcal{A}$ with vertex $A$ is exactly a natural transformation $\Delta A \Rightarrow D$.
    - **The cone functor.** For $\mathcal{A}$ locally small, $\mathrm{Cone}(A, D) = [\mathbf{I}, \mathcal{A}](\Delta A, D)$ is a set, and $\mathrm{Cone}(-, D) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ is a functor: a map $g \colon A' \to A$ sends a cone $(f_I)$ with vertex $A$ to the cone $(f_I \circ g)$ with vertex $A'$.

    **Theorems**

    - **A limit is a representation.** Let $\mathbf{I}$ be small, $\mathcal{A}$ locally small and $D \colon \mathbf{I} \to \mathcal{A}$. There is a one-to-one correspondence between limit cones on $D$ and representations of $\mathrm{Cone}(-, D)$, with the representing objects being the vertices of the limit cones. Briefly: if $D$ has a limit then $$\mathcal{A}(A, \lim D) \cong \mathrm{Cone}(A, D) \quad \text{naturally in } A.$$ *Idea:* a limit cone is a universal element of $\mathrm{Cone}(-, D)$ (4C). *Technique:* re-expressing one universal property as another.
    - **Limits are functorial.** Let $D, D' \colon \mathbf{I} \to \mathcal{A}$ have limit cones $(p_I \colon \lim D \to D(I))$ and $(p'_I \colon \lim D' \to D'(I))$. For every natural transformation $\alpha \colon D \Rightarrow D'$ there is exactly one map $\lim \alpha \colon \lim D \to \lim D'$ with $p'_I \circ \lim \alpha = \alpha_I \circ p_I$ for all $I$. *Technique:* universal-property argument.
    - **Limits as a right adjoint.** If $\mathcal{A}$ has all limits of shape $\mathbf{I}$, then (after choosing a limit cone for each diagram) $\lim \colon [\mathbf{I}, \mathcal{A}] \to \mathcal{A}$ is a functor and is right adjoint to the diagonal: $\Delta \dashv \lim$. Dually, if $\mathcal{A}$ has all colimits of shape $\mathbf{I}$ then $\operatorname{colim} \dashv \Delta$. *Idea:* $[\mathbf{I}, \mathcal{A}](\Delta A, D) = \mathrm{Cone}(A, D) \cong \mathcal{A}(A, \lim D)$.
    - **Cones as a limit of hom-sets.** For $\mathcal{A}$ locally small, $\mathrm{Cone}(A, D) \cong \lim_{I} \mathcal{A}(A, D(I))$ naturally in $A$ and $D$, where the limit on the right is taken in $\mathbf{Set}$. *Idea:* compare with the explicit formula for limits in $\mathbf{Set}$ (5A).
    - **Representables preserve limits.** For $\mathcal{A}$ locally small and $A \in \mathcal{A}$, the functor $\mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$ preserves limits: $\mathcal{A}(A, \lim_I D(I)) \cong \lim_I \mathcal{A}(A, D(I))$. Dually, $\mathcal{A}(-, A) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ preserves limits, which means that it turns colimits in $\mathcal{A}$ into limits in $\mathbf{Set}$: $\mathcal{A}(\operatorname{colim}_I D(I), A) \cong \lim_I \mathcal{A}(D(I), A)$. *Idea:* combine the two previous isomorphisms.

    **Standard examples.** For a product: $\mathcal{A}(A, X \times Y) \cong \mathcal{A}(A, X) \times \mathcal{A}(A, Y)$, and the binary product functor $\mathcal{A} \times \mathcal{A} \to \mathcal{A}$ is right adjoint to the diagonal $\mathcal{A} \to \mathcal{A} \times \mathcal{A}$. For a sum: $\mathcal{A}(X + Y, A) \cong \mathcal{A}(X, A) \times \mathcal{A}(Y, A)$. In $\mathbf{Set}$: a function into a product is a pair of functions; a function out of a disjoint union is a pair of functions.

    **Used later in.** 6B (pointwise limits), 6C (the proof that right adjoints preserve limits).
    """))

    _guide.append(("6", "6B", r"""
    ### 6B: Limits & Colimits of Presheaves

    *Sources: [Leinster §6.2](LEINSTER) · [Riehl §3.3, §2.4](RIEHL)*

    **Definitions**

    - **Evaluation functor.** For $A \in \mathcal{A}$, $\mathrm{ev}_A \colon [\mathcal{A}, \mathcal{S}] \to \mathcal{S}$ sends a functor $X$ to $X(A)$ and a natural transformation $\alpha$ to its component $\alpha_A$.
    - **Computed pointwise.** A limit of $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ is computed pointwise if each $\mathrm{ev}_A$ sends its limit cone to a limit cone in $\mathcal{S}$: the value of the limit at $A$ is the limit of the values at $A$.
    - **Category of elements.** Let $X$ be a presheaf on $\mathcal{A}$. The category of elements $\mathbf{E}(X)$ has as objects the pairs $(A, x)$ with $A \in \mathcal{A}$ and $x \in X(A)$. A map $(A', x') \to (A, x)$ is a map $f \colon A' \to A$ in $\mathcal{A}$ with $(X(f))(x) = x'$. The projection functor $P \colon \mathbf{E}(X) \to \mathcal{A}$ sends $(A, x)$ to $A$ and $f$ to $f$.

    **Theorems**

    - **Limits in functor categories.** Let $\mathcal{A}$ and $\mathbf{I}$ be small categories and $\mathcal{S}$ a locally small category. Let $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ be a diagram, and suppose that for each $A \in \mathcal{A}$ the diagram $\mathrm{ev}_A \circ D \colon \mathbf{I} \to \mathcal{S}$ has a limit cone $(p_{I, A} \colon L(A) \to D(I)(A))_{I \in \mathbf{I}}$. Then there is exactly one way to extend $L$ to a functor $\mathcal{A} \to \mathcal{S}$ such that each $p_I = (p_{I, A})_{A \in \mathcal{A}}$ is a natural transformation $L \Rightarrow D(I)$, and $(p_I \colon L \Rightarrow D(I))_{I \in \mathbf{I}}$ is then a limit cone on $D$. The same holds for colimits. *Idea:* the action of $L$ on a map of $\mathcal{A}$, and each mediating map, is defined component by component by the universal property in $\mathcal{S}$; every equation is checked by uniqueness. *Technique:* **pointwise argument**.
    - **Corollary.** If $\mathcal{S}$ has all limits (respectively colimits) of shape $\mathbf{I}$ then so does $[\mathcal{A}, \mathcal{S}]$, and each evaluation functor $\mathrm{ev}_A$ preserves them. In particular $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ has all limits and colimits for every small $\mathcal{A}$.
    - **The Yoneda embedding preserves limits.** For every small category $\mathcal{A}$, $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ preserves limits. It does not in general preserve colimits. *Idea:* evaluate at each object and use "representables preserve limits" (6A).
    - **Monics and epics of presheaves are pointwise.** For a small category $\mathcal{A}$, a map $\alpha$ in $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is monic if and only if every component $\alpha_A$ is injective, and epic if and only if every component is surjective. *Technique:* pointwise argument.
    - **Density theorem.** Let $\mathcal{A}$ be a small category and $X$ a presheaf on $\mathcal{A}$. Then $X$ is the colimit of the diagram $$\mathbf{E}(X) \xrightarrow{\;P\;} \mathcal{A} \xrightarrow{\;H_\bullet\;} [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}],$$ that is, $X \cong \operatorname{colim}_{(A, x) \in \mathbf{E}(X)} H_A$. In words: every presheaf is a colimit of representables. *Idea:* by the Yoneda lemma, a cocone on this diagram with vertex $Y$ is a family of elements $y_{(A, x)} \in Y(A)$ compatible with the maps of $\mathbf{E}(X)$, and that is the same thing as a natural transformation $X \Rightarrow Y$. *Technique:* Yoneda-style, then a universal-property argument.

    **Standard examples.** If $\mathcal{A}$ is discrete, a presheaf is a family of sets $(X(A))_{A}$ and the density theorem says that each set is the disjoint union of its one-element subsets. For a presheaf on a poset given by a down-set $D$, $\mathbf{E}(D)$ is $D$ itself and the theorem says $D = \bigcup_{a \in D} \{b : b \le a\}$. For a group $G$ and a right $G$-set $X$, $\mathbf{E}(X)$ has the elements of $X$ as objects and a map $x' \to x$ for each $g$ with $x \cdot g = x'$. For a representable $H_A$, the pair $(A, 1_A)$ is a terminal object of $\mathbf{E}(H_A)$.

    **Used later in.** 6C (presheaf categories are cartesian closed). The fact that $(A, u)$ is a universal element of $X$ exactly when it is a terminal object of $\mathbf{E}(X)$ ties this module to 4C.
    """))

    _guide.append(("6", "6C", r"""
    ### 6C: Adjoints & Limits

    *Sources: [Leinster §6.3, Appendix A](LEINSTER) · [Riehl §4.5–4.6](RIEHL)*

    **Definitions**

    - **Complete.** A category is complete if it has all limits, that is, a limit for every diagram whose shape is a small category. A poset is complete in this sense exactly when every subset has a meet.
    - **Weakly initial set.** A weakly initial set in a category $\mathcal{C}$ is a **set** $\mathbf{S}$ of objects of $\mathcal{C}$ such that for every object $C \in \mathcal{C}$ there exist $S \in \mathbf{S}$ and a map $S \to C$.
    - **Subobject; well-powered.** A subobject of $B$ is an isomorphism class of monics into $B$ (monics $m \colon X \to B$ and $m' \colon X' \to B$ being isomorphic if $m' \circ i = m$ for some isomorphism $i \colon X \to X'$). A category is well-powered if each object has only a set of subobjects.
    - **Coseparating (cogenerating) set.** A set $\mathbf{S}$ of objects of $\mathcal{B}$ such that for every pair of distinct maps $f \ne g \colon B \to B'$ in $\mathcal{B}$ there exist $S \in \mathbf{S}$ and a map $h \colon B' \to S$ with $h \circ f \ne h \circ g$.
    - **Cartesian closed.** A category $\mathcal{A}$ is cartesian closed if it has finite products and, for each $B \in \mathcal{A}$, the functor $- \times B \colon \mathcal{A} \to \mathcal{A}$ has a right adjoint, written $(-)^B$. So $\mathcal{A}(A \times B, C) \cong \mathcal{A}(A, C^B)$ naturally in $A$ and $C$.

    **Theorems**

    - **Adjoints preserve limits.** Let $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$, both categories locally small. Then $G$ preserves limits and $F$ preserves colimits. *Idea:* $\mathcal{A}(A, G(\lim D)) \cong \mathcal{B}(F(A), \lim D) \cong \lim \mathcal{B}(F(A), D(I)) \cong \lim \mathcal{A}(A, G(D(I)))$, naturally in $A$; then use 6A and the corollaries of Yoneda (4C). *Technique:* Yoneda-style chain of natural isomorphisms.
    - **Contrapositive, used as a test.** A functor that fails to preserve some limit has no left adjoint; a functor that fails to preserve some colimit has no right adjoint.
    - **Adjoint functor theorem for posets.** Let $B$ be a complete poset, $A$ a poset and $G \colon B \to A$ an order-preserving map. Then $G$ has a left adjoint if and only if $G$ preserves all meets. When it does, the left adjoint is $$F(a) = \bigwedge \{ b \in B : a \le G(b) \}.$$ *Idea:* $F(a)$ must be the least $b$ with $a \le G(b)$, that is, an initial object of $(a \Rightarrow G)$ (2C); preservation of meets is what puts the meet of all candidates among the candidates. *Technique:* universal-property argument in a poset, where every uniqueness clause is automatic.
    - **General adjoint functor theorem.** Let $\mathcal{A}$ be a category, $\mathcal{B}$ a complete category and $G \colon \mathcal{B} \to \mathcal{A}$ a functor. Suppose that $\mathcal{B}$ is locally small and that for each $A \in \mathcal{A}$ the category $(A \Rightarrow G)$ has a weakly initial set. Then $$G \text{ has a left adjoint} \iff G \text{ preserves limits}.$$ (Statement only in this course.)
    - **Special adjoint functor theorem.** Let $\mathcal{A}$ be a locally small category and let $\mathcal{B}$ be a category that is complete, locally small and well-powered and has a coseparating set. Then a functor $G \colon \mathcal{B} \to \mathcal{A}$ has a left adjoint if and only if it preserves limits. (Statement only in this course.)
    - **Set and presheaf categories are cartesian closed.** $\mathbf{Set}$ is cartesian closed, with $C^B$ the set of functions $B \to C$. For every small category $\mathcal{A}$, the presheaf category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is cartesian closed.
    - **Distributivity.** In a cartesian closed category with finite sums, $- \times B$ preserves them: $0 \times B \cong 0$ and $(A + A') \times B \cong (A \times B) + (A' \times B)$. *Idea:* $- \times B$ is a left adjoint, so it preserves colimits.

    **Standard examples.** The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ preserves limits, as it must since it has a left adjoint; it does not preserve the initial object, so it has no right adjoint. In the poset theorem the size condition disappears: completeness and preservation of meets are enough. A poset with finite meets is cartesian closed when for all $b, c$ there is an element $(b \Rightarrow c)$ with $a \wedge b \le c \iff a \le (b \Rightarrow c)$ for all $a$; the open sets of a topological space are an example. Non-examples of cartesian closed categories: $\mathbf{Vect}_k$ and $\mathbf{Grp}$, where the initial object $0$ is also terminal, so $0 \times B \cong B$ is not initial unless $B$ is.

    **Used later in.** 6D (monads arise from adjunctions). This module is the meeting point of Parts 2, 4 and 5.
    """))

    _guide.append(("6", "6D", r"""
    ### 6D: Monads *(advanced)*

    *Sources: [Riehl §5.1–5.3](RIEHL)*

    **Definitions**

    - **Monad.** A monad on a category $\mathcal{C}$ consists of a functor $T \colon \mathcal{C} \to \mathcal{C}$ and natural transformations $\eta \colon 1_{\mathcal{C}} \Rightarrow T$ (the unit) and $\mu \colon T^2 \Rightarrow T$ (the multiplication) such that, for every $A \in \mathcal{C}$, $$\mu_A \circ T(\mu_A) = \mu_A \circ \mu_{T(A)} \quad \text{(associativity)}, \qquad \mu_A \circ \eta_{T(A)} = 1_{T(A)} = \mu_A \circ T(\eta_A) \quad \text{(unit laws)}.$$
    - **Algebra.** An algebra for a monad $(T, \eta, \mu)$, or $T$-algebra, is a pair $(A, a)$ with $A \in \mathcal{C}$ and $a \colon T(A) \to A$ such that $a \circ \eta_A = 1_A$ and $a \circ \mu_A = a \circ T(a)$. A map of algebras $(A, a) \to (B, b)$ is a map $f \colon A \to B$ in $\mathcal{C}$ with $f \circ a = b \circ T(f)$.
    - **Eilenberg–Moore category.** $\mathcal{C}^T$ is the category of $T$-algebras and their maps. The forgetful functor $U^T \colon \mathcal{C}^T \to \mathcal{C}$ sends $(A, a)$ to $A$; the free-algebra functor $F^T \colon \mathcal{C} \to \mathcal{C}^T$ sends $A$ to $(T(A), \mu_A)$ and $f$ to $T(f)$.
    - **Kleisli category.** $\mathcal{C}_T$ has the same objects as $\mathcal{C}$; a map from $A$ to $B$ in $\mathcal{C}_T$ is a map $A \to T(B)$ in $\mathcal{C}$. The identity on $A$ is $\eta_A$, and the composite of $f \colon A \to T(B)$ and $g \colon B \to T(C)$ is $\mu_C \circ T(g) \circ f \colon A \to T(C)$.
    - **Comparison functor.** For an adjunction $F \dashv G$ ($F \colon \mathcal{A} \to \mathcal{B}$) with counit $\varepsilon$ and induced monad $T = GF$ on $\mathcal{A}$, the comparison functor $K \colon \mathcal{B} \to \mathcal{A}^T$ sends $B$ to $(G(B), G(\varepsilon_B))$ and a map $h$ to $G(h)$.
    - **Monadic.** An adjunction $F \dashv G$ is monadic if its comparison functor $K$ is an equivalence of categories. A functor $G$ is monadic if it has a left adjoint and the resulting adjunction is monadic.

    **Theorems**

    - **Monads from adjunctions.** Every adjunction $F \dashv G$ ($F \colon \mathcal{A} \to \mathcal{B}$) with unit $\eta$ and counit $\varepsilon$ gives a monad $(GF, \eta, G \varepsilon F)$ on $\mathcal{A}$, where $G \varepsilon F$ has components $G(\varepsilon_{F(A)})$. *Idea:* the unit laws are the triangle identities (2B); associativity is naturality of $\varepsilon$.
    - **Adjunctions from monads.** For every monad $T$ on $\mathcal{C}$: $F^T \dashv U^T$, and the monad of this adjunction is $T$. There is also an adjunction between $\mathcal{C}$ and $\mathcal{C}_T$ whose monad is $T$. So every monad comes from an adjunction, in general from more than one. *Technique:* checking algebra axioms; verifying an adjunction by unit and counit.
    - **The comparison functor.** $K$ is a functor, and it satisfies $U^T \circ K = G$ and $K \circ F = F^T$; it is the only functor $\mathcal{B} \to \mathcal{A}^T$ satisfying these two equations. *Technique:* building a comparison functor; uniqueness argument.
    - **Kleisli maps are maps of free algebras.** The canonical functor $\mathcal{C}_T \to \mathcal{C}^T$ sending $A$ to the free algebra $(T(A), \mu_A)$ is full and faithful, so $\mathcal{C}_T$ is equivalent to the full subcategory of $\mathcal{C}^T$ on the free algebras.
    - **Monads on a poset are closure operators.** A monad on a poset $P$ is exactly a closure operator $T$ (2B); the monad laws hold automatically. A $T$-algebra is an element $p$ with $T(p) \le p$, equivalently $T(p) = p$: a closed element. So $P^T$ is the sub-poset of closed elements. The Kleisli category is the set $P$ with the preorder "$p \sqsubseteq q$ if and only if $p \le T(q)$".

    **Standard examples.** The free-monoid monad on $\mathbf{Set}$ (finite sequences, with $\mu$ concatenating a sequence of sequences): its algebras are monoids, and the forgetful functor $\mathbf{Mon} \to \mathbf{Set}$ is monadic. Likewise $\mathbf{Grp} \to \mathbf{Set}$ and $\mathbf{Vect}_k \to \mathbf{Set}$ are monadic. For a group $G$, the monad $G \times -$ on $\mathbf{Set}$ has the left $G$-sets as its algebras. The monad $X \mapsto X + 1$ on $\mathbf{Set}$ has pointed sets as its algebras. Non-example: the forgetful functor $\mathbf{Top} \to \mathbf{Set}$ has a left adjoint (the discrete topology), but the induced monad is the identity monad, whose category of algebras is $\mathbf{Set}$ itself; the comparison functor is the forgetful functor, which is not an equivalence, so $\mathbf{Top} \to \mathbf{Set}$ is not monadic.

    **Used later in.** This is the last teaching module. It revisits 2B (triangle identities, closure operators) and 1E (equivalence).
    """))

    return [
        (_part, _mod, _text.replace("LEINSTER", _L).replace("RIEHL", _R).replace("HAMMACK", _H))
        for _part, _mod, _text in _guide
    ]


@app.cell
def _(mo):
    part_filter = mo.ui.dropdown(
        options={
            "All parts": "All",
            "Part 0 — Proof Toolkit (0B, 0C)": "0",
            "Part 1 — Categories, Functors, Natural Transformations (1A–1E)": "1",
            "Part 2 — Adjoints (2A–2C)": "2",
            "Part 3 — Interlude on Sets (3A)": "3",
            "Part 4 — Representables & the Yoneda Lemma (4A–4C)": "4",
            "Part 5 — Limits (5A–5C)": "5",
            "Part 6 — Adjoints, Representables & Limits Together (6A–6D)": "6",
        },
        value="All parts",
        label="Show",
    )
    part_filter
    return (part_filter,)


@app.cell(hide_code=True)
def _(mo, part_filter):
    def _run():
        import textwrap

        _choice = part_filter.value
        _entries = [
            textwrap.dedent(_text).strip()
            for _part, _mod, _text in build_guide()
            if _choice in ("All", _part)
        ]
        _mods = [_mod for _part, _mod, _text in build_guide() if _choice in ("All", _part)]
        _head = "**Showing " + str(len(_mods)) + " of 21 modules:** " + ", ".join(_mods)
        return mo.md(_head + "\n\n---\n\n" + "\n\n---\n\n".join(_entries))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Pictures of the Main Universal Properties

    Every universal property in the course has the same shape: *some given data* (solid arrows), and *exactly one* map (dashed arrow) making the diagram commute. The five pictures below are the ones to be able to draw from memory. In each, the dashed arrow is the one whose existence and uniqueness the definition asserts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    def _run():
        _fig = draw_diagram(
            {
                "A": (2, 2, "$A$"),
                "X": (0, 0, "$X$"),
                "P": (2, 0, r"$X \times Y$"),
                "Y": (4, 0, "$Y$"),
                "Pl": (1.7, 0, ""),
                "Pr": (2.3, 0, ""),
            },
            [
                ("A", "X", "$f_1$", {"side": -1}),
                ("A", "Y", "$f_2$"),
                ("A", "P", "$f$", {"dashed": True}),
                ("Pl", "X", "$p_1$"),
                ("Pr", "Y", "$p_2$", {"side": -1}),
            ],
            figsize=(5.4, 3.2),
            title="Product (5A)",
        )
        return mo.vstack([
            mo.md(r"""
            **Product.** Given $f_1$ and $f_2$, there is exactly one $f$ with $p_1 \circ f = f_1$ and $p_2 \circ f = f_2$. Reverse every arrow to get the picture for a sum $X + Y$ (5B).
            """),
            _fig,
        ])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    def _run():
        _fig = draw_diagram(
            {
                "A": (0, 1.8, "$A$"),
                "E": (0, 0, "$E$"),
                "X": (2, 0, "$X$"),
                "Y": (4, 0, "$Y$"),
            },
            [
                ("A", "E", r"$\bar{f}$", {"dashed": True, "side": -1}),
                ("A", "X", "$f$"),
                ("E", "X", "$i$", {"side": -1}),
                ("X", "Y", "$s$", {"rad": 0.25}),
                ("X", "Y", "$t$", {"rad": -0.25}),
            ],
            figsize=(5.4, 3.0),
            title="Equalizer (5A)",
        )
        return mo.vstack([
            mo.md(r"""
            **Equalizer.** Here $s \circ i = t \circ i$. Given $f$ with $s \circ f = t \circ f$, there is exactly one $\bar{f}$ with $i \circ \bar{f} = f$. Note that this diagram does **not** commute in the strict sense: $s$ and $t$ are different maps. Only the composites through $i$ (and through $f$) agree.
            """),
            _fig,
        ])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    def _run():
        _fig = draw_diagram(
            {
                "A": (0, 3.4, "$A$"),
                "P": (1.4, 2, "$P$"),
                "Y": (3.4, 2, "$Y$"),
                "X": (1.4, 0, "$X$"),
                "Z": (3.4, 0, "$Z$"),
            },
            [
                ("A", "P", "$f$", {"dashed": True}),
                ("A", "Y", "$f_2$", {"rad": -0.3}),
                ("A", "X", "$f_1$", {"rad": 0.3}),
                ("P", "Y", "$p_2$", {"side": -1}),
                ("P", "X", "$p_1$"),
                ("X", "Z", "$s$", {"side": -1}),
                ("Y", "Z", "$t$"),
            ],
            figsize=(5.0, 4.4),
            title="Pullback (5A)",
        )
        return mo.vstack([
            mo.md(r"""
            **Pullback.** The square commutes: $s \circ p_1 = t \circ p_2$. Given $f_1$ and $f_2$ with $s \circ f_1 = t \circ f_2$, there is exactly one $f$ with $p_1 \circ f = f_1$ and $p_2 \circ f = f_2$. Reverse every arrow to get a pushout (5B).
            """),
            _fig,
        ])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    def _run():
        _fig = draw_diagram(
            {
                "A": (0, 1.2, "$A$"),
                "L": (2.2, 1.2, r"$\lim D$"),
                "DI": (4.6, 2.4, "$D(I)$"),
                "DJ": (4.6, 0, "$D(J)$"),
                "Ll": (1.85, 1.2, ""),
            },
            [
                ("A", "Ll", r"$\bar{f}$", {"dashed": True}),
                ("L", "DI", "$p_I$", {"side": -1}),
                ("L", "DJ", "$p_J$"),
                ("DI", "DJ", r"$\qquad D(u)$"),
                ("A", "DI", "$f_I$", {"rad": -0.3}),
                ("A", "DJ", "$f_J$", {"rad": 0.3}),
            ],
            figsize=(6.0, 3.8),
            title="Limit cone (5A, 6A)",
        )
        return mo.vstack([
            mo.md(r"""
            **Limit.** Only two objects $I, J$ of the shape $\mathbf{I}$ and one map $u \colon I \to J$ are drawn. The $p$'s form a cone ($D(u) \circ p_I = p_J$) and so do the $f$'s. Given the cone $(f_I)$, there is exactly one $\bar{f}$ with $p_I \circ \bar{f} = f_I$ for **every** $I$. Products, equalizers and pullbacks are the cases where $\mathbf{I}$ is a discrete two-object category, a parallel pair, and a cospan.
            """),
            _fig,
        ])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    def _run():
        _fig = draw_diagram(
            {
                "A": (0, 2, "$A$"),
                "GFA": (2.6, 2, "$G(F(A))$"),
                "GB": (2.6, 0, "$G(B)$"),
                "FA": (5.4, 2, "$F(A)$"),
                "B": (5.4, 0, "$B$"),
                "GFAl": (2.1, 2, ""),
            },
            [
                ("A", "GFAl", r"$\eta_A$"),
                ("A", "GB", "$f$", {"side": -1}),
                ("GFA", "GB", r"$\qquad G(q)$"),
                ("FA", "B", "$q$", {"dashed": True}),
            ],
            figsize=(6.8, 3.2),
            title=r"Unit of an adjunction as a universal arrow (2C)",
        )
        return mo.vstack([
            mo.md(r"""
            **Left adjoint.** The triangle on the left lives in $\mathcal{A}$; the single arrow on the right lives in $\mathcal{B}$. Given any $B$ and any $f \colon A \to G(B)$, there is exactly one $q \colon F(A) \to B$ in $\mathcal{B}$ with $G(q) \circ \eta_A = f$. That $q$ is the transpose $\bar{f}$.
            """),
            _fig,
        ])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Which Universal Property Is Which

    All of these say "there is exactly one map such that ...". They differ in two respects: what data you are given, and whether the unique map goes **into** the universal object or **out of** it. Constructions in the same row of a dual pair are obtained from each other by reversing arrows.

    | Construction | Comes with | Universal property: for every ... there is exactly one ... | Unique map goes | As a hom-set isomorphism | Module |
    |---|---|---|---|---|---|
    | **Terminal object** $1$ | nothing | object $A$; map $A \to 1$ | into $1$ | $\mathcal{A}(A, 1) \cong$ one-element set | 2A, 5A |
    | **Initial object** $0$ | nothing | object $A$; map $0 \to A$ | out of $0$ | $\mathcal{A}(0, A) \cong$ one-element set | 2A, 5B |
    | **Product** $X \times Y$ | projections $p_1, p_2$ | pair $f_1 \colon A \to X$, $f_2 \colon A \to Y$; map $f \colon A \to X \times Y$ with $p_k \circ f = f_k$ | into | $\mathcal{A}(A, X \times Y) \cong \mathcal{A}(A, X) \times \mathcal{A}(A, Y)$ | 5A |
    | **Sum** $X + Y$ | coprojections $i_1, i_2$ | pair $f_1 \colon X \to A$, $f_2 \colon Y \to A$; map $f \colon X + Y \to A$ with $f \circ i_k = f_k$ | out of | $\mathcal{A}(X + Y, A) \cong \mathcal{A}(X, A) \times \mathcal{A}(Y, A)$ | 5B |
    | **Equalizer** of $s, t \colon X \to Y$ | $i \colon E \to X$ with $s i = t i$ | $f \colon A \to X$ with $s f = t f$; map $\bar{f} \colon A \to E$ with $i \bar{f} = f$ | into | $\mathcal{A}(A, E) \cong \{ f \in \mathcal{A}(A, X) : s f = t f \}$ | 5A |
    | **Coequalizer** of $s, t \colon X \to Y$ | $p \colon Y \to C$ with $p s = p t$ | $f \colon Y \to A$ with $f s = f t$; map $\bar{f} \colon C \to A$ with $\bar{f} p = f$ | out of | $\mathcal{A}(C, A) \cong \{ f \in \mathcal{A}(Y, A) : f s = f t \}$ | 5B |
    | **Pullback** of $X \xrightarrow{s} Z \xleftarrow{t} Y$ | $p_1, p_2$ with $s p_1 = t p_2$ | pair $f_1, f_2$ out of $A$ with $s f_1 = t f_2$; map $f \colon A \to P$ with $p_k f = f_k$ | into | $\mathcal{A}(A, P) \cong \{ (f_1, f_2) : s f_1 = t f_2 \}$ | 5A |
    | **Pushout** of $X \xleftarrow{s} Z \xrightarrow{t} Y$ | $i_1, i_2$ with $i_1 s = i_2 t$ | pair $f_1, f_2$ into $A$ with $f_1 s = f_2 t$; map $f \colon P \to A$ with $f i_k = f_k$ | out of | $\mathcal{A}(P, A) \cong \{ (f_1, f_2) : f_1 s = f_2 t \}$ | 5B |
    | **Limit** of $D \colon \mathbf{I} \to \mathcal{A}$ | a cone $(p_I \colon \lim D \to D(I))$ | cone $(f_I \colon A \to D(I))$; map $\bar{f} \colon A \to \lim D$ with $p_I \bar{f} = f_I$ for all $I$ | into | $\mathcal{A}(A, \lim D) \cong [\mathbf{I}, \mathcal{A}](\Delta A, D)$ | 5A, 6A |
    | **Colimit** of $D \colon \mathbf{I} \to \mathcal{A}$ | a cocone $(p_I \colon D(I) \to \operatorname{colim} D)$ | cocone $(f_I \colon D(I) \to A)$; map $\bar{f} \colon \operatorname{colim} D \to A$ with $\bar{f} p_I = f_I$ for all $I$ | out of | $\mathcal{A}(\operatorname{colim} D, A) \cong [\mathbf{I}, \mathcal{A}](D, \Delta A)$ | 5B, 6A |
    | **Left adjoint** $F$ of $G \colon \mathcal{B} \to \mathcal{A}$, at $A$ | unit $\eta_A \colon A \to G(F(A))$ | $B \in \mathcal{B}$ and $f \colon A \to G(B)$; map $q \colon F(A) \to B$ with $G(q) \circ \eta_A = f$ | out of $F(A)$ | $\mathcal{B}(F(A), B) \cong \mathcal{A}(A, G(B))$ | 2A–2C |
    | **Right adjoint** $G$ of $F \colon \mathcal{A} \to \mathcal{B}$, at $B$ | counit $\varepsilon_B \colon F(G(B)) \to B$ | $A \in \mathcal{A}$ and $g \colon F(A) \to B$; map $p \colon A \to G(B)$ with $\varepsilon_B \circ F(p) = g$ | into $G(B)$ | $\mathcal{A}(A, G(B)) \cong \mathcal{B}(F(A), B)$ | 2A–2C |
    | **Representation** of $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ | universal element $u \in X(A)$ | $B \in \mathcal{A}$ and $x \in X(B)$; map $\bar{x} \colon B \to A$ with $(X(\bar{x}))(u) = x$ | into $A$ | $\mathcal{A}(B, A) \cong X(B)$ | 4A, 4C |

    How the rows are related:

    - **Each row is a special case of a later one.** A terminal object, a product, an equalizer and a pullback are limits of particular shapes (the empty shape, two objects with no other maps, a parallel pair, a cospan). A limit of shape $\mathbf{I}$ is a value of the right adjoint to $\Delta$ (6A). A value of a right adjoint is a representation: $G(B)$ represents the presheaf $\mathcal{B}(F(-), B)$ on $\mathcal{A}$ (4A).
    - **Each is an initial or terminal object of some category.** A limit is a terminal object in the category of cones on $D$; a colimit is an initial cocone; $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$ (2C); a universal element $(A, u)$ of a presheaf $X$ is a terminal object of the category of elements $\mathbf{E}(X)$ (6B).
    - **Rule of thumb for direction.** Limits, right adjoints and representations of presheaves are characterised by maps **into** them. Colimits and left adjoints are characterised by maps **out of** them. Consistently with this, right adjoints preserve limits and left adjoints preserve colimits (6C).
    - **All are unique up to unique isomorphism**, by one and the same argument: the one for initial objects in 2A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The Proof Techniques of the Course

    Seven proof shapes account for nearly every proof in the lectures and the exercises. When you start a proof, the *Plan* step of the proof anatomy is the place to name which of these you are using.

    ### 5.1 Direct proof by unpacking definitions

    - **What it is.** Write out what the hypothesis says and what the conclusion says, with all quantifiers, and connect them. For "for all $x$": let $x$ be arbitrary. For "there exists $x$": construct one and check it. For an equation between maps: transform one side into the other, naming the axiom used at each step.
    - **Reach for it when** the statement is about a single definition ("a composite of monics is monic", "functors preserve isomorphisms") and no universal property is in sight.
    - **Practised in** 0B, 1A, 1B, 1C; used as a component everywhere.

    ### 5.2 Existence and uniqueness

    - **What it is.** Two separate proofs. Existence: build the thing and verify its properties. Uniqueness: take two things with the property and prove them equal (not: observe that your construction produced only one).
    - **Reach for it when** you see "exactly one", "a unique", or "unique up to isomorphism". For the last of these, the standard pattern is: get maps in both directions from existence, then show both composites are identities using uniqueness.
    - **Practised in** 0C, 1A (identities), 1B (inverses), 2A (initial objects), 2C, 3A (quotients), 5A.

    ### 5.3 Diagram chase

    - **What it is.** Prove an equation between composites by moving through a diagram one commuting region at a time, replacing one path by another and citing which square or triangle justifies each replacement.
    - **Reach for it when** the hypotheses are commuting squares or triangles: naturality squares, pasted squares, cones.
    - **Practised in** 0C, 1D, 2B, 5A; used throughout Part 6.

    ### 5.4 Dualization

    - **What it is.** If a statement has been proved for all categories, then the statement with every arrow reversed is also true, because it is the original statement applied to $\mathcal{A}^{\mathrm{op}}$. The proof is one sentence, provided you state the dual correctly: monic $\leftrightarrow$ epic, product $\leftrightarrow$ sum, limit $\leftrightarrow$ colimit, initial $\leftrightarrow$ terminal, left adjoint $\leftrightarrow$ right adjoint, and $g \circ f$ becomes $f \circ g$.
    - **Reach for it when** a result is the mirror image of one already proved. It does **not** apply to statements about one particular category: a fact about $\mathbf{Set}$ dualizes to a fact about $\mathbf{Set}^{\mathrm{op}}$, not about $\mathbf{Set}$.
    - **Practised in** 1B, 5B, 6C.

    ### 5.5 Follow the identity (Yoneda-style arguments)

    - **What it is.** Two related moves. (a) A natural transformation out of a representable, or a natural family of bijections, is determined by what it does to an identity map: feed in $1_A$ and use naturality to recover everything else. (b) To prove $A \cong A'$, prove instead $\mathcal{A}(B, A) \cong \mathcal{A}(B, A')$ naturally in $B$, and quote the corollary of the Yoneda lemma.
    - **Reach for it when** you have something natural in a variable and need to pin it down by a single piece of data (move a), or when you need an isomorphism between objects that are each defined by a universal property (move b).
    - **Practised in** 2B (unit and counit as transposes of identities), 4B, 4C, 6A, 6B, 6C.

    ### 5.6 Universal-property arguments

    - **What it is.** Use a universal property as a tool in both of its halves. *Existence* lets you **define** a map by saying what its composites with the projections (or with the unit, or with the coprojections) are. *Uniqueness* lets you **prove two maps equal** by showing that they have the same composites with the projections.
    - **Reach for it when** you need a map into a limit or out of a colimit, or need to prove that two such maps agree. Typical sentence: "both $h$ and $k$ satisfy $p_I \circ - = f_I$ for all $I$, so by the uniqueness part of the universal property, $h = k$."
    - **Practised in** 2C, 5A, 5B, 5C, 6A, 6C (the poset adjoint functor theorem).

    ### 5.7 Pointwise arguments

    - **What it is.** A statement about functors and natural transformations is checked one object at a time: two natural transformations are equal if and only if all their components are equal; a natural transformation is an isomorphism if and only if every component is; a limit in $[\mathcal{A}, \mathcal{S}]$ is built from limits in $\mathcal{S}$ at each object of $\mathcal{A}$.
    - **Reach for it when** you are working in a functor category. The step that is easy to forget is the return journey: after constructing something component by component, you must still check that the components fit together naturally.
    - **Practised in** 1D, 4A, 6B.

    ### Which technique for which kind of statement

    | The statement says ... | First technique to try |
    |---|---|
    | "$f$ is monic / epic / an isomorphism", "$F$ is a functor", "$\alpha$ is natural" | 5.1 unpack the definition |
    | "there is exactly one ..." | 5.2 existence, then uniqueness |
    | "these two composites are equal" and you have commuting squares | 5.3 diagram chase |
    | "these two maps into a limit (out of a colimit) are equal" | 5.6 uniqueness half of the universal property |
    | "dually, ..." or the mirror image of a known result | 5.4 dualize |
    | "$A \cong A'$" where both are defined by universal properties | 5.5(b) compare hom-functors, or 5.2 |
    | "this natural family is determined by ..." | 5.5(a) follow the identity |
    | "these two natural transformations are equal", "this functor category has ..." | 5.7 pointwise |

    > Sources for the whole guide: [Leinster, *Basic Category Theory*](https://arxiv.org/abs/1612.09375) (Chapters 1–6 and Appendix A); [Riehl, *Category Theory in Context*](https://math.jhu.edu/~eriehl/context.pdf) (Chapters 1–5); [Hammack, *Book of Proof*](https://www.people.vcu.edu/~rhammack/BookOfProof/) for Part 0. Each module entry in §2 cites the sections it draws on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) | &#8592; Prev: [6D: Monads](../6d_monads/)
    """)
    return


if __name__ == "__main__":
    app.run()
