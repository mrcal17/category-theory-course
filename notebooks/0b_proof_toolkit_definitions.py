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
    # 0B: Proof Toolkit I: Definitions & Direct Proof

    > *"The only way to learn mathematics is to do mathematics."*
    > — Paul Halmos, *A Hilbert Space Problem Book*

    The question this module answers is: **when a statement is put in front of you, how do you know what to write?** Most people who find proofs hard are not short of cleverness. They are missing a procedure for the first three lines. The procedure exists, it is mechanical, and it is the subject of this module: read the definitions in the statement as checklists, read the quantifiers to find out what you are allowed to choose and what you must accept, and then verify the checklist.

    The raw material is functions between sets: when two functions are equal, how they compose, what injective and surjective mean, and what one-sided inverses are. This is not a detour. A category (Module 1A) is an abstraction of "functions and composition", and every definition here comes back in Part 1 with the word *function* replaced by *arrow*.

    By the end you will be able to prove, from the definitions and without hand-waving: that composition of functions is associative, that a composite of injections is an injection, that a function with a left inverse is injective, and that an injective function out of a non-empty set has a left inverse. You will also be able to say exactly what a proof of "for all", "there exists", "if ... then" and "if and only if" must contain, and to disprove a false statement with a counterexample.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. A Definition Is a Checklist

    A definition in mathematics is not a description to get the feel of. It is a list of conditions, and an object either meets every one of them or it does not. Proving that something "is an X" means going down the list. Proving that something "is not an X" means finding one item that fails. We practise on the most basic definition of the course.

    > **Definition (function).** A *function* $f \colon A \to B$ consists of a set $A$ (the *domain*), a set $B$ (the *codomain*), and a rule that assigns to **each** element $a \in A$ **exactly one** element $f(a) \in B$.

    **Reading the definition.** To check that a proposed $f$ is a function from $A$ to $B$, verify:

    1. **Every input is covered.** For each $a \in A$ the rule produces a value. (No input is left out.)
    2. **The value is unambiguous.** The rule produces only one value for $a$, and that value does not depend on how $a$ happens to be written down. This is what "$f$ is *well defined*" means.
    3. **The value lands in $B$.** For each $a \in A$, the value $f(a)$ is an element of the stated codomain.

    The domain and the codomain are part of the function. Changing either one gives a different function, even if the formula is the same.

    **Examples.**

    - $s \colon \mathbb{Z} \to \mathbb{Z}$, $s(n) = n^2$. Item 1: every integer can be squared. Item 2: the square of an integer is a single number. Item 3: the square of an integer is an integer.
    - For any set $A$, the **identity function** $1_A \colon A \to A$, $1_A(a) = a$.
    - $q \colon \mathbb{Z} \to \{0, 1, 2\}$, where $q(n)$ is the remainder of $n$ on division by $3$. Each integer has exactly one such remainder, and it is $0$, $1$ or $2$.

    **Non-examples.** Each fails a different item, and you should be able to say which.

    - "$r \colon \mathbb{R} \to \mathbb{R}$, $r(x) = 1/x$" fails item 1: no value is assigned to $0$.
    - "$n \colon \mathbb{Q} \to \mathbb{Z}$, $n(p/q) = p$" fails item 2: the rational number $\tfrac12$ is also written $\tfrac24$, and the rule gives $1$ for one way of writing it and $2$ for the other. The rule depends on the *name* of the input and not only on the input.
    - "$t \colon \mathbb{N} \to \mathbb{N}$, $t(n) = n - 1$" (with $\mathbb{N} = \{0, 1, 2, \ldots\}$) fails item 3: $t(0) = -1$ is not in $\mathbb{N}$.

    Item 2 is the one that is forgotten in real proofs. Whenever you define a function by saying "pick some $x$ with such-and-such a property and let the value be built from $x$", you owe a check that a different pick gives the same value. You will see this check done in Section 6.

    > References: [Hammack Ch 12](https://www.people.vcu.edu/~rhammack/BookOfProof/) (functions); [Leinster §3.1](https://arxiv.org/abs/1612.09375) (what we assume about sets and functions).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Quantifiers Tell You What to Write

    Nearly every statement you will prove is built from two phrases: **for all** ($\forall$) and **there exists** ($\exists$). They are instructions. "For all" means the element is chosen *for* you and you must cope with whichever one it is. "There exists" means *you* get to choose.

    | Statement | How to **prove** it | How to **use** it when it is given |
    |-----------|---------------------|-----------------------------------|
    | $\forall x \in A,\ P(x)$ | Write "Let $x \in A$." Then prove $P(x)$ using nothing about $x$ except that it is in $A$. | Apply it to any particular element of $A$ you like, as often as you like. |
    | $\exists x \in A,\ P(x)$ | Name one specific $x$ (the *witness*), check it is in $A$, check $P(x)$. | Write "Choose $x \in A$ with $P(x)$", using a letter not already in use. You know nothing else about this $x$. |
    | $P \Rightarrow Q$ | Write "Assume $P$." Then derive $Q$. | Once you have established $P$, you may conclude $Q$. |
    | $P \Leftrightarrow Q$ | Two proofs: $P \Rightarrow Q$ and $Q \Rightarrow P$. | Use whichever direction you need. |

    And the negations, which tell you how to **disprove**:

    - To show "$\forall x \in A,\ P(x)$" is **false**, exhibit one $x \in A$ for which $P(x)$ fails. That $x$ is a **counterexample**.
    - To show "$\exists x \in A,\ P(x)$" is **false**, let $x \in A$ be arbitrary and prove that $P(x)$ fails.

    **Order matters.** Compare these two statements about integers:

    $$\text{(i)}\ \ \forall x \in \mathbb{Z}\ \ \exists y \in \mathbb{Z}\ \ (x + y = 0) \qquad\qquad \text{(ii)}\ \ \exists y \in \mathbb{Z}\ \ \forall x \in \mathbb{Z}\ \ (x + y = 0)$$

    In (i) the witness $y$ is chosen *after* $x$ is known, so it may depend on $x$. Statement (i) is true: let $x \in \mathbb{Z}$; take $y = -x$; then $x + y = 0$. In (ii) a single $y$ must be named *first* and must then work for every $x$. Statement (ii) is false, and we prove its negation: let $y \in \mathbb{Z}$ be arbitrary; take $x = 1 - y$; then $x + y = 1 \neq 0$. The rule: **a witness may depend only on the variables introduced before it.**

    Now a definition with a quantifier inside it, and a first complete proof.

    > **Definition (divides).** For integers $a$ and $b$, we say $a$ *divides* $b$, written $a \mid b$, if there exists an integer $k$ such that $b = ak$.

    **Reading the definition.** To prove $a \mid b$: produce an integer $k$ and verify the equation $b = ak$. To use a hypothesis $a \mid b$: choose an integer $k$ with $b = ak$, with a fresh letter.

    **Examples and non-examples.** $3 \mid 12$, with witness $k = 4$. $5 \mid 0$, with witness $k = 0$. $-2 \mid 6$, with witness $k = -3$. But $4 \nmid 6$: for an integer $k$, $4k \le 4$ when $k \le 1$ and $4k \ge 8$ when $k \ge 2$, so $4k$ is never $6$.

    > **Proposition 1.** For all integers $a$, $b$, $c$: if $a \mid b$ and $b \mid c$, then $a \mid c$.

    **Goal.** For all $a, b, c \in \mathbb{Z}$: if (there exists $k \in \mathbb{Z}$ with $b = ak$) and (there exists $m \in \mathbb{Z}$ with $c = bm$), then there exists $n \in \mathbb{Z}$ with $c = an$.

    **Given.** The definition of "divides"; arithmetic of integers (a product of integers is an integer; multiplication is associative).

    **Plan.** Direct proof. The statement is "for all ... if ... then there exists", so: let $a, b, c$ be arbitrary, assume the two hypotheses, unpack each into an equation, and combine the equations to manufacture the witness $n$.

    **Proof.** Let $a, b, c \in \mathbb{Z}$, and assume $a \mid b$ and $b \mid c$. By the definition of $a \mid b$, choose $k \in \mathbb{Z}$ with $b = ak$. By the definition of $b \mid c$, choose $m \in \mathbb{Z}$ with $c = bm$. Then

    $$c = bm = (ak)m = a(km),$$

    where the second equality substitutes $b = ak$ and the third is associativity of multiplication. Put $n = km$. It is an integer because it is a product of integers, and $c = an$. By the definition of "divides", $a \mid c$. $\blacksquare$

    **What made it work.** We did nothing clever. Each hypothesis was a definition containing "there exists", so each handed us a named number and an equation; the conclusion was a definition containing "there exists", so it told us what to build. Notice the two different letters $k$ and $m$: the two hypotheses are separate existence statements, and nothing says their witnesses are the same number. Reach for this pattern, *unpack, combine, repack*, whenever both the hypotheses and the conclusion are definitions.

    > References: [Hammack Ch 2](https://www.people.vcu.edu/~rhammack/BookOfProof/) (logic and quantifiers), [Ch 4](https://www.people.vcu.edu/~rhammack/BookOfProof/) (direct proof), [Ch 9](https://www.people.vcu.edu/~rhammack/BookOfProof/) (disproof).
    """)
    return


@app.cell
def _():
    def _run():
        # Quantifier order, checked by brute force on a finite domain: arithmetic modulo 5.
        _D = range(5)

        def _forall_exists(pred):
            return all(any(pred(_x, _y) for _y in _D) for _x in _D)

        def _exists_forall(pred):
            return any(all(pred(_x, _y) for _x in _D) for _y in _D)

        def _sum_zero(x, y):
            return (x + y) % 5 == 0

        def _prod_zero(x, y):
            return (x * y) % 5 == 0

        print("Domain: {0,1,2,3,4} with arithmetic modulo 5\n")
        print("P(x, y):  x + y = 0")
        print(f"  for all x there exists y, P(x, y): {_forall_exists(_sum_zero)}   (witness y = -x depends on x)")
        print(f"  there exists y, for all x, P(x, y): {_exists_forall(_sum_zero)}  (no single y works for every x)")
        print("\nQ(x, y):  x * y = 0")
        print(f"  for all x there exists y, Q(x, y): {_forall_exists(_prod_zero)}")
        print(f"  there exists y, for all x, Q(x, y): {_exists_forall(_prod_zero)}   (y = 0 works for every x)")
        print("\n'Exists-forall' always implies 'forall-exists'. The first example shows the converse can fail.")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. When Are Two Functions Equal? Composition

    Half the equations in this course have a function on each side. You cannot prove such an equation until you know what it means.

    > **Definition (equality of functions).** Functions $f \colon A \to B$ and $g \colon A' \to B'$ are *equal* if $A = A'$, $B = B'$, and $f(a) = g(a)$ for every $a \in A$.

    **Reading the definition.** To prove $f = g$:

    1. Check the two domains are the same set and the two codomains are the same set. (Usually this is immediate from how $f$ and $g$ were built, but say it.)
    2. Write "Let $a \in A$." and prove the equation $f(a) = g(a)$ between two *elements* of $B$.

    Item 2 is a "for all" statement, so a proof of $f = g$ almost always begins with the words "Let $a \in A$".

    **Examples.** Define $f, g \colon \{0, 1\} \to \{0, 1\}$ by $f(x) = x^2$ and $g(x) = x$. The formulas differ, but $f(0) = 0 = g(0)$ and $f(1) = 1 = g(1)$, so $f = g$. A function is its values, not its formula.

    **Non-examples.** The functions $\mathbb{R} \to \mathbb{R}$ given by $x \mapsto x^2$ and $x \mapsto x$ are not equal, because they differ at $x = 2$: one counterexample is enough. And the squaring function $\mathbb{R} \to \mathbb{R}$ is not equal to the squaring function $\mathbb{R} \to [0, \infty)$, because the codomains differ (item 1).

    > **Definition (composite).** Given functions $f \colon A \to B$ and $g \colon B \to C$, where the codomain of $f$ **is** the domain of $g$, the *composite* $g \circ f \colon A \to C$ is the function defined by $(g \circ f)(a) = g(f(a))$ for each $a \in A$.

    **Reading the definition.** $g \circ f$ is defined only when the codomain of $f$ equals the domain of $g$. It has the domain of $f$ and the codomain of $g$. Read $g \circ f$ as "$g$ after $f$": the function on the right acts first. As a chain: $A \xrightarrow{f} B \xrightarrow{g} C$.

    **Example.** Let $f, g \colon \mathbb{Z} \to \mathbb{Z}$ with $f(n) = n + 1$ and $g(n) = 2n$. Then $(g \circ f)(n) = 2(n + 1) = 2n + 2$ and $(f \circ g)(n) = 2n + 1$. These differ at $n = 0$, so $g \circ f \neq f \circ g$: **composition is not commutative**, even when both composites are defined. **Non-example.** With $p \colon \mathbb{Z} \to \{0, 1\}$ the parity function, $p \circ f$ is defined, but $f \circ p$ is not: the codomain of $p$ is $\{0, 1\}$, and the domain of $f$ is $\mathbb{Z}$, a different set.

    The triangle below is the picture of a composite. It is your first **commutative diagram**: the two routes from $A$ to $C$ give the same function.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (0, 1.6, r"$A$"), "B": (2.4, 1.6, r"$B$"), "C": (2.4, 0, r"$C$")},
        [
            ("A", "B", r"$f$"),
            ("B", "C", r"$g$"),
            ("A", "C", r"$g \circ f$", {"side": -1}),
        ],
        figsize=(4.4, 3.0),
        title="g after f",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Proposition 2.** Let $f \colon A \to B$, $g \colon B \to C$ and $h \colon C \to D$ be functions. Then
    >
    > (a) $h \circ (g \circ f) = (h \circ g) \circ f$ &nbsp; (*associativity*);
    >
    > (b) $f \circ 1_A = f$ and $1_B \circ f = f$ &nbsp; (*identity laws*).

    **Goal.** (a) The functions $h \circ (g \circ f)$ and $(h \circ g) \circ f$ have the same domain, the same codomain, and the same value at every $a \in A$. (b) The same three things for $f \circ 1_A$ and $f$, and for $1_B \circ f$ and $f$.

    **Given.** The definitions of composite, of identity function, and of equality of functions.

    **Plan.** Direct proof from the definition of equality of functions: compare domains and codomains, then let $a \in A$ and compute both sides by unfolding the definition of composite one layer at a time.

    **Proof.** (a) *Domains and codomains.* $g \circ f$ goes from $A$ to $C$, so $h \circ (g \circ f)$ goes from $A$ to $D$. $h \circ g$ goes from $B$ to $D$, so $(h \circ g) \circ f$ goes from $A$ to $D$. Both sides are functions $A \to D$.

    *Values.* Let $a \in A$. Then

    $$\big(h \circ (g \circ f)\big)(a) = h\big((g \circ f)(a)\big) = h\big(g(f(a))\big),$$

    using the definition of composite twice: first for $h$ after $g \circ f$, then for $g$ after $f$. On the other side,

    $$\big((h \circ g) \circ f\big)(a) = (h \circ g)\big(f(a)\big) = h\big(g(f(a))\big),$$

    again by the definition of composite twice: first for $h \circ g$ after $f$, then for $h$ after $g$, applied to the element $f(a) \in B$. The two sides are the same element of $D$. Since $a$ was arbitrary, the two functions are equal.

    (b) $f \circ 1_A$ has the domain of $1_A$, which is $A$, and the codomain of $f$, which is $B$; so it is a function $A \to B$, as $f$ is. Let $a \in A$. Then $(f \circ 1_A)(a) = f(1_A(a)) = f(a)$, by the definition of composite and then of $1_A$. So $f \circ 1_A = f$. Likewise $1_B \circ f$ is a function $A \to B$, and for $a \in A$ we get $(1_B \circ f)(a) = 1_B(f(a)) = f(a)$, by the definition of composite and then of $1_B$ applied to the element $f(a) \in B$. So $1_B \circ f = f$. $\blacksquare$

    **What made it work.** The definition of equality of functions converted a statement about functions into a statement about elements, and then there was nothing to do but unfold. Because of (a) we may write $h \circ g \circ f$ with no brackets. These two laws are the only facts about composition that a category keeps, so from Module 1A onward you will often prove equations between composites **using (a) and (b) alone, without mentioning elements**. Section 6 has the first equations of that kind.

    > References: [Hammack Ch 12](https://www.people.vcu.edu/~rhammack/BookOfProof/) (composition); [Leinster §3.1](https://arxiv.org/abs/1612.09375).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Injective, Surjective, Bijective

    Three definitions that differ only in their quantifiers. Read them slowly; the proofs are dictated by the wording.

    > **Definition.** Let $f \colon A \to B$ be a function.
    >
    > - $f$ is *injective* if for all $a, a' \in A$: if $f(a) = f(a')$ then $a = a'$.
    > - $f$ is *surjective* if for every $b \in B$ there exists $a \in A$ such that $f(a) = b$.
    > - $f$ is *bijective* if it is both injective and surjective.

    **Reading the definition.**

    - **To prove $f$ injective:** write "Let $a, a' \in A$ and assume $f(a) = f(a')$." The last line must be "$a = a'$". (The proof starts from equal *outputs*. Starting from $a = a'$ proves nothing.)
    - **To prove $f$ surjective:** write "Let $b \in B$." Then *produce* an $a \in A$, which may depend on $b$, and verify $f(a) = b$.
    - **To prove $f$ not injective:** exhibit two specific elements $a \neq a'$ with $f(a) = f(a')$.
    - **To prove $f$ not surjective:** exhibit one specific $b \in B$ and prove that no $a \in A$ has $f(a) = b$.
    - **To use** injectivity of $f$: whenever you have an equation $f(x) = f(y)$, you may delete the $f$. **To use** surjectivity: for any $b \in B$ you care about, you may choose an $a$ with $f(a) = b$.

    Surjectivity depends on the codomain; this is one reason the codomain is part of a function.

    **Examples and non-examples.**

    | Function | Injective? | Surjective? | Why |
    |----------|-----------|-------------|-----|
    | $d \colon \mathbb{Z} \to \mathbb{Z}$, $d(n) = 2n$ | yes | no | if $2n = 2n'$ then $n = n'$; but no integer $n$ has $2n = 1$ |
    | parity $p \colon \mathbb{Z} \to \{0, 1\}$ | no | yes | $p(0) = p(2)$ with $0 \neq 2$; and $p(0) = 0$, $p(1) = 1$ |
    | $s \colon \mathbb{R} \to \mathbb{R}$, $s(x) = x^2$ | no | no | $s(1) = s(-1)$; and no real $x$ has $x^2 = -1$ |
    | $s' \colon \mathbb{R} \to [0, \infty)$, $s'(x) = x^2$ | no | yes | every $y \ge 0$ is $(\sqrt{y})^2$ |
    | $u \colon \mathbb{Z} \to \mathbb{Z}$, $u(n) = n + 1$ | yes | yes | if $n + 1 = n' + 1$ then $n = n'$; and $m = u(m - 1)$ |

    > **Proposition 3.** Let $f \colon A \to B$ and $g \colon B \to C$ be functions. If $f$ and $g$ are both injective, then $g \circ f$ is injective.

    **Goal.** For all $a, a' \in A$: if $(g \circ f)(a) = (g \circ f)(a')$ then $a = a'$.

    **Given.** For all $x, x' \in A$: $f(x) = f(x') \Rightarrow x = x'$. For all $y, y' \in B$: $g(y) = g(y') \Rightarrow y = y'$. The definition of composite.

    **Plan.** Direct proof. Start exactly where the definition of "injective" for $g \circ f$ says to start, then peel off $g$ and then $f$, using each hypothesis once.

    **Proof.** Let $a, a' \in A$ and assume $(g \circ f)(a) = (g \circ f)(a')$. By the definition of composite this says $g(f(a)) = g(f(a'))$. The elements $f(a)$ and $f(a')$ are in $B$, and $g$ is injective, so applying injectivity of $g$ with $y = f(a)$ and $y' = f(a')$ gives $f(a) = f(a')$. Now $f$ is injective, so $a = a'$. $\blacksquare$

    **What made it work.** The Goal line told us the first sentence and the last sentence of the proof before we had any idea; the middle then had only one possible move at each step. Write the first and last lines of a proof first, whenever the thing to be proved is a definition.

    > References: [Hammack Ch 12](https://www.people.vcu.edu/~rhammack/BookOfProof/) (injective and surjective functions).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Explorer: Two Functions and Their Composite

    Take $A = \{0, 1, 2\}$, $B = \{0, 1, 2, 3\}$ and $C = \{0, 1, 2\}$. Choose the values of $f \colon A \to B$ and $g \colon B \to C$ below. The panel draws $f$, $g$, and reports for each of $f$, $g$ and $g \circ f$ whether it is injective, whether it is surjective, and how many left inverses and right inverses it has (these are defined in Section 6; the counts are found by trying every function in the opposite direction).

    Experiments to try, writing down what you observe before you read on:

    - Make $f$ injective, then not injective. What happens to its number of left inverses?
    - Can you make $f$ surjective? Can you make $g$ injective? Why not?
    - Make $g \circ f$ injective. What is forced about $f$? Is anything forced about $g$?
    - Make $g \circ f$ surjective. What is forced about $g$?
    """)
    return


@app.cell
def _(mo):
    f0 = mo.ui.dropdown(options=["0", "1", "2", "3"], value="0", label="f(0)")
    f1 = mo.ui.dropdown(options=["0", "1", "2", "3"], value="1", label="f(1)")
    f2 = mo.ui.dropdown(options=["0", "1", "2", "3"], value="1", label="f(2)")
    g0 = mo.ui.dropdown(options=["0", "1", "2"], value="0", label="g(0)")
    g1 = mo.ui.dropdown(options=["0", "1", "2"], value="2", label="g(1)")
    g2 = mo.ui.dropdown(options=["0", "1", "2"], value="2", label="g(2)")
    g3 = mo.ui.dropdown(options=["0", "1", "2"], value="1", label="g(3)")
    mo.vstack([
        mo.hstack([f0, f1, f2], justify="start"),
        mo.hstack([g0, g1, g2, g3], justify="start"),
    ])
    return f0, f1, f2, g0, g1, g2, g3


@app.cell(hide_code=True)
def _(f0, f1, f2, g0, g1, g2, g3, mo):
    def _run():
        import itertools

        import matplotlib.pyplot as plt

        _A, _B, _C = [0, 1, 2], [0, 1, 2, 3], [0, 1, 2]
        _f = {0: int(f0.value), 1: int(f1.value), 2: int(f2.value)}
        _g = {0: int(g0.value), 1: int(g1.value), 2: int(g2.value), 3: int(g3.value)}
        _gf = {_a: _g[_f[_a]] for _a in _A}

        def _functions(dom, cod):
            for _vals in itertools.product(cod, repeat=len(dom)):
                yield dict(zip(dom, _vals))

        def _report(fn, dom, cod):
            _inj = len(set(fn.values())) == len(dom)
            _sur = set(fn.values()) == set(cod)
            _left = sum(1 for _k in _functions(cod, dom) if all(_k[fn[_x]] == _x for _x in dom))
            _right = sum(1 for _k in _functions(cod, dom) if all(fn[_k[_y]] == _y for _y in cod))
            return _inj, _sur, _left, _right

        _fig, _ax = plt.subplots(figsize=(6.4, 3.4))
        _cols = {"A": (0.0, _A), "B": (2.0, _B), "C": (4.0, _C)}
        _ypos = {}
        for _name, (_x, _elems) in _cols.items():
            for _i, _e in enumerate(_elems):
                _y = (len(_elems) - 1) / 2 - _i
                _ypos[(_name, _e)] = (_x, _y)
                _ax.plot([_x], [_y], "o", color="#1f2937", ms=7, zorder=3)
                _ax.text(_x, _y + 0.28, str(_e), ha="center", va="center", fontsize=10)
            _ax.text(_x, 2.35, _name, ha="center", va="center", fontsize=14)
        for _a in _A:
            _p, _q = _ypos[("A", _a)], _ypos[("B", _f[_a])]
            _ax.annotate("", xy=_q, xytext=_p, arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=1.4, shrinkA=5, shrinkB=5))
        for _b in _B:
            _p, _q = _ypos[("B", _b)], _ypos[("C", _g[_b])]
            _ax.annotate("", xy=_q, xytext=_p, arrowprops=dict(arrowstyle="-|>", color="#d97706", lw=1.4, shrinkA=5, shrinkB=5))
        _ax.text(1.0, -2.2, "f", color="#2563eb", fontsize=13, ha="center")
        _ax.text(3.0, -2.2, "g", color="#d97706", fontsize=13, ha="center")
        _ax.set_xlim(-0.6, 4.6)
        _ax.set_ylim(-2.6, 2.8)
        _ax.axis("off")
        _fig.tight_layout()

        _yes = {True: "yes", False: "no"}
        _rows = [
            ("$f \\colon A \\to B$", str([_f[_a] for _a in _A]), _report(_f, _A, _B)),
            ("$g \\colon B \\to C$", str([_g[_b] for _b in _B]), _report(_g, _B, _C)),
            ("$g \\circ f \\colon A \\to C$", str([_gf[_a] for _a in _A]), _report(_gf, _A, _C)),
        ]
        _lines = [
            "| function | list of values | injective | surjective | left inverses | right inverses |",
            "|---|---|---|---|---|---|",
        ]
        for _label, _vals, (_inj, _sur, _left, _right) in _rows:
            _lines.append(
                "| " + _label + " | " + _vals + " | " + _yes[_inj] + " | " + _yes[_sur]
                + " | " + str(_left) + " | " + str(_right) + " |"
            )
        return mo.vstack([_fig, mo.md("\n".join(_lines))])

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Left and Right Inverses

    "Injective" and "surjective" are defined by looking at elements. There is a second way to say almost the same things that mentions only functions and composition. It is the way category theory prefers, because in a general category the arrows need not be functions and there may be no elements to look at.

    > **Definition (one-sided inverses).** Let $f \colon A \to B$ be a function.
    >
    > - A *left inverse* of $f$ is a function $g \colon B \to A$ such that $g \circ f = 1_A$.
    > - A *right inverse* of $f$ is a function $h \colon B \to A$ such that $f \circ h = 1_B$.
    > - $f$ is *invertible* if there is a single function $k \colon B \to A$ that is both: $k \circ f = 1_A$ and $f \circ k = 1_B$. Such a $k$ is called a *two-sided inverse* (or just an *inverse*) of $f$.

    **Reading the definition.** To prove $g$ is a left inverse of $f$: check that $g$ goes from $B$ to $A$, then prove the equation of functions $g \circ f = 1_A$, that is, $g(f(a)) = a$ for every $a \in A$. A left inverse is written on the left of $f$ and acts after $f$: it undoes $f$. To prove $h$ is a right inverse: check that $h$ goes from $B$ to $A$ and that $f(h(b)) = b$ for every $b \in B$. The two conditions are equations between different functions, on different sets ($A$ and $B$), and neither implies the other.

    **Example.** Let $\mathbb{N} = \{0, 1, 2, \ldots\}$ and $u \colon \mathbb{N} \to \mathbb{N}$, $u(n) = n + 1$. Define $v \colon \mathbb{N} \to \mathbb{N}$ by $v(0) = 0$ and $v(n) = n - 1$ for $n \ge 1$. For every $n \in \mathbb{N}$ we have $u(n) = n + 1 \ge 1$, so $v(u(n)) = (n + 1) - 1 = n$. Hence $v \circ u = 1_{\mathbb{N}}$: $v$ is a left inverse of $u$ (and, reading the same equation the other way, $u$ is a right inverse of $v$). Changing $v(0)$ to any other number gives another left inverse of $u$, so **left inverses need not be unique**.

    **Non-example.** The same $v$ is *not* a right inverse of $u$: $(u \circ v)(0) = u(0) = 1 \neq 0$, so $u \circ v \neq 1_{\mathbb{N}}$. In fact $u$ has no right inverse at all: if $h \colon \mathbb{N} \to \mathbb{N}$ had $u \circ h = 1_{\mathbb{N}}$ then $h(0) + 1 = u(h(0)) = 0$, which is impossible for $h(0) \in \mathbb{N}$.

    This example also settles a question from the explorer: $v \circ u$ is injective (it is an identity function), yet $v$ is not injective, since $v(0) = v(1)$.

    The picture of a left inverse is a triangle that commutes: going along $f$ and then $g$ is the same as doing nothing.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (0, 1.6, r"$A$"), "B": (2.4, 1.6, r"$B$"), "A2": (2.4, 0, r"$A$")},
        [
            ("A", "B", r"$f$"),
            ("B", "A2", r"$g$"),
            ("A", "A2", r"$1_A$", {"side": -1}),
        ],
        figsize=(4.4, 3.0),
        title="g is a left inverse of f",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Proposition 4.** Let $f \colon A \to B$ be a function.
    >
    > (a) If $f$ has a left inverse, then $f$ is injective.
    >
    > (b) If $f$ is injective and $A$ is non-empty, then $f$ has a left inverse.

    **Goal.** (a) Assuming there exists $g \colon B \to A$ with $g \circ f = 1_A$: for all $a, a' \in A$, if $f(a) = f(a')$ then $a = a'$. (b) Assuming $f$ is injective and $A \neq \emptyset$: there exists a function $g \colon B \to A$ with $g(f(a)) = a$ for all $a \in A$.

    **Given.** The definitions of injective, of left inverse, of composite and identity; in (b), the three-item checklist for "function" from Section 1.

    **Plan.** (a) Direct: start from $f(a) = f(a')$ and apply $g$ to both sides. (b) An existence proof, so we must *construct* $g$: send each element in the image of $f$ back to where it came from, and send everything else to one fixed element of $A$. Then check that this rule really is a function, and that it is a left inverse.

    **Proof.** (a) Let $g \colon B \to A$ satisfy $g \circ f = 1_A$. Let $a, a' \in A$ and assume $f(a) = f(a')$. Applying the function $g$ to both sides gives $g(f(a)) = g(f(a'))$. By the definition of composite the left side is $(g \circ f)(a) = 1_A(a) = a$, and the right side is $(g \circ f)(a') = 1_A(a') = a'$. So $a = a'$.

    (b) Since $A$ is non-empty, choose an element $a_0 \in A$. Define a rule $g$ on $B$ as follows. Let $b \in B$.

    - If there exists $a \in A$ with $f(a) = b$, let $g(b)$ be such an $a$.
    - Otherwise, let $g(b) = a_0$.

    *$g$ is a function $B \to A$.* Every $b \in B$ falls under exactly one of the two cases, so every input is covered, and in both cases the value is an element of $A$. It remains to check that the value is unambiguous in the first case, where we said "such an $a$" and there might be several. Suppose $a$ and $a'$ both satisfy $f(a) = b$ and $f(a') = b$. Then $f(a) = f(a')$, and since $f$ is injective, $a = a'$. So there is only one such $a$, and $g(b)$ is well defined.

    *$g$ is a left inverse of $f$.* $g \circ f$ and $1_A$ are both functions $A \to A$. Let $a \in A$ and put $b = f(a)$. There exists an element of $A$ that $f$ sends to $b$, namely $a$ itself, so $b$ falls under the first case, and $g(b)$ is the one and only element that $f$ sends to $b$, which is $a$. That is, $g(f(a)) = a = 1_A(a)$. Hence $g \circ f = 1_A$. $\blacksquare$

    **What made it work.** In (a): to get from an equation about $f$ to an equation without $f$, apply something that cancels $f$. In (b): injectivity was used exactly once, and not where you might expect. It was not needed to show $g \circ f = 1_A$; it was needed to show that $g$ is a function at all. Whenever a construction says "pick an element such that ...", the proof is not finished until you have shown the outcome does not depend on the pick.

    **Why "non-empty" is there.** If $A = \emptyset$ and $B \neq \emptyset$, the unique function $f \colon \emptyset \to B$ is injective (there are no $a, a'$ to test), but it has no left inverse, because there is no function at all from the non-empty set $B$ to $\emptyset$. A hypothesis that looks like a technicality usually marks the exact place where the proof would break; here it is the sentence "choose an element $a_0 \in A$".

    **The mirror statements.** The corresponding facts for right inverses and surjections, and the relation between "invertible" and "bijective", are yours to prove: see briefs P03, P04 and P05. One of them hides a subtlety worth knowing about in advance. The statement "every surjective function has a right inverse" cannot be proved from the checklist alone when the sets are infinite: building the right inverse requires choosing one preimage for each $b \in B$, all at once, with no rule to say which. The assertion that this is always possible is the **axiom of choice**; it is an assumption about sets, and it comes up again when equivalences of categories are built in Part 1.

    > References: [Hammack Ch 12](https://www.people.vcu.edu/~rhammack/BookOfProof/) (inverse functions); [Leinster §3.1](https://arxiv.org/abs/1612.09375) (sets, functions and the axiom of choice).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. "If and Only If", Converses and Counterexamples

    Two more pieces of logic finish the toolkit.

    > **Definition.** The *converse* of the statement "if $P$ then $Q$" is the statement "if $Q$ then $P$". The *contrapositive* of "if $P$ then $Q$" is the statement "if not $Q$ then not $P$". The statement "$P$ if and only if $Q$" (written $P \Leftrightarrow Q$) means "if $P$ then $Q$, **and** if $Q$ then $P$".

    **Reading the definition.**

    - A statement and its contrapositive are logically equivalent: proving either one proves the other. For example, "$f$ is injective" can be proved in the form: for all $a, a' \in A$, if $a \neq a'$ then $f(a) \neq f(a')$.
    - A statement and its converse are **independent**: one can be true and the other false. Proving the converse when you were asked for the statement proves nothing.
    - An "if and only if" proof has two halves, labelled ($\Rightarrow$) and ($\Leftarrow$). Each half has its own Goal and its own Given, and it is worth writing them out separately.

    **Examples of a true statement with a false converse.**

    - Proposition 3 says: if $f$ and $g$ are injective then $g \circ f$ is injective. Its converse, "if $g \circ f$ is injective then $f$ and $g$ are injective", is false; the counterexample is the pair $u, v$ of Section 6, where $v \circ u = 1_{\mathbb{N}}$ is injective and $v$ is not.
    - "If $f \colon \mathbb{Z} \to \mathbb{Z}$ is bijective then $f$ is injective" is true by definition. Its converse is false: $d(n) = 2n$ is injective and not bijective.

    **A counterexample must be completely specific.** To disprove "for all integers $a$ and $b$, if $a \mid b$ and $b \mid a$ then $a = b$", it is not enough to say "signs could differ". Write: take $a = 2$ and $b = -2$. Then $-2 = 2 \cdot (-1)$, so $a \mid b$; and $2 = (-2) \cdot (-1)$, so $b \mid a$; but $2 \neq -2$. The reader can check each claim.

    That false statement becomes true once the integers are required to be positive, and the proof is a model "if and only if".

    > **Proposition 5.** For all positive integers $a$ and $b$: ($a \mid b$ and $b \mid a$) if and only if $a = b$.

    **Goal.** For all integers $a, b > 0$: ($\Leftarrow$) if $a = b$ then $a \mid b$ and $b \mid a$; ($\Rightarrow$) if there exist integers $k, m$ with $b = ak$ and $a = bm$, then $a = b$.

    **Given.** The definition of "divides"; arithmetic of integers, in particular: if $xy = xz$ and $x \neq 0$ then $y = z$ (cancellation), and the only pairs of integers with product $1$ are $(1, 1)$ and $(-1, -1)$.

    **Plan.** Two halves. ($\Leftarrow$) is an existence statement: supply the witness. ($\Rightarrow$) unpack both hypotheses, substitute one equation into the other, and use positivity to pin down the witnesses.

    **Proof.** Let $a, b$ be positive integers.

    ($\Leftarrow$) Assume $a = b$. Then $b = a \cdot 1$, so $a \mid b$ with witness $1$; and $a = b \cdot 1$, so $b \mid a$ with witness $1$.

    ($\Rightarrow$) Assume $a \mid b$ and $b \mid a$. Choose $k \in \mathbb{Z}$ with $b = ak$ and choose $m \in \mathbb{Z}$ with $a = bm$. Substituting the first equation into the second, $a = (ak)m = a(km)$, that is, $a \cdot 1 = a \cdot (km)$. Since $a > 0$, in particular $a \neq 0$, and cancellation gives $km = 1$. So $(k, m)$ is $(1, 1)$ or $(-1, -1)$. If $k = -1$ then $b = ak = -a < 0$, contradicting $b > 0$. So $k = 1$, and $b = a \cdot 1 = a$. $\blacksquare$

    **What made it work.** The hypothesis "positive" was used twice in ($\Rightarrow$), once to cancel and once to exclude $k = -1$, and the counterexample $a = 2$, $b = -2$ shows it cannot be dropped. When a proof is finished, look back and find where each hypothesis was used. A hypothesis that was never used means either the statement can be strengthened or the proof has a gap.

    > References: [Hammack Ch 5](https://www.people.vcu.edu/~rhammack/BookOfProof/) (contrapositive), [Ch 6](https://www.people.vcu.edu/~rhammack/BookOfProof/) (contradiction), [Ch 7](https://www.people.vcu.edu/~rhammack/BookOfProof/) (if-and-only-if proofs), [Ch 9](https://www.people.vcu.edu/~rhammack/BookOfProof/) (counterexamples).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Proving "for all" with an example.** Checking that $g \circ f$ is injective for one choice of $f$ and $g$ shows nothing about all choices. *Diagnosis:* the proof does not begin with "Let ... be arbitrary". (An example is a proof only of a "there exists" statement, or a disproof of a "for all" statement.)
    2. **Reusing a letter for two witnesses.** From $a \mid b$ and $b \mid c$, writing $b = ak$ and $c = bk$. *Diagnosis:* two separate "there exists" hypotheses were unpacked with the same letter, which silently assumes the two witnesses are equal.
    3. **Starting an injectivity proof at the wrong end.** "Let $a = a'$. Then $f(a) = f(a')$." *Diagnosis:* this proves the converse of the required implication, and that converse is true of every function, injective or not.
    4. **Using a function before showing it is well defined.** "Define $g(b)$ to be an $a$ with $f(a) = b$" and then computing with $g$. *Diagnosis:* items 1 and 2 of the function checklist were skipped. Is there such an $a$ for every $b$? If there are several, does the choice matter?
    5. **Choosing a witness too early.** In a proof of "for every $b$ there exists $a$ ...", fixing $a$ before $b$ has been introduced. *Diagnosis:* the quantifier order has been swapped; the witness is allowed to depend on $b$ and usually must.
    6. **Composing in the wrong order, or composing functions that do not meet.** Writing $f \circ g$ for "first $f$, then $g$", or forming $g \circ f$ when the codomain of $f$ is not the domain of $g$. *Diagnosis:* write the chain $A \xrightarrow{f} B \xrightarrow{g} C$ and read the composite off it from right to left.

    ---

    ## Why This Matters

    - **The axioms of a category are Proposition 2.** In Module 1A a category is defined as objects and arrows with a composition that is associative and has identities. Everything proved from Proposition 2 alone will then hold in every category.
    - **Equality of functions becomes equality of arrows.** "Two functors are equal", "two natural transformations are equal" (1C, 1D) are all checked the way Section 3 checks $f = g$: componentwise, starting with "Let ...".
    - **Injective and surjective become definitions without elements.** Module 1B replaces them with *monomorphism* and *epimorphism*, and replaces "invertible function" with *isomorphism*. The one-sided inverses of Section 6 are the bridge, and the proofs there use the same moves.
    - **Reading quantifiers is how you read a universal property.** "For every $X$ and every $f, g$ there exists a unique $h$ such that ..." (0A, and all of Parts 2, 4 and 5) is a quantifier string. Its proof has exactly the parts the string dictates.
    - **Well-definedness returns whenever a map is built by choosing.** Quotients and colimits (5B) and maps built out of representatives all need the check you saw in Proposition 4(b).

    The next module, **0C**, adds the two remaining proof shapes: uniqueness arguments and diagram chases.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Set Exercises

    On finite sets every definition in this module can be tested by brute force. A function is encoded as a Python dictionary from inputs to outputs, for example `{0: 0, 1: 1, 2: 3}` for the function $\{0,1,2\} \to \{0,1,2,3\}$ with those values. The codomain is not recorded in the dictionary, so it is passed separately where it matters.

    Each skeleton runs as it stands. Replace the `...` placeholders, then un-comment the `print` lines and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Witnesses Against Injectivity and Surjectivity

    Section 4 says how to prove a function is *not* injective (exhibit two inputs with the same output) and *not* surjective (exhibit an element of the codomain that is never a value). Write `collisions(f)`, the list of all pairs `(a, b)` of inputs with `a < b` and $f(a) = f(b)$, and `missed(f, codomain)`, the list of elements of the codomain that are not values of $f$. A function is injective exactly when the first list is empty and surjective exactly when the second is. Then count functions by how many witnesses they have.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(domain, codomain):
            """Every function domain -> codomain, as a dict."""
            for _vals in itertools.product(codomain, repeat=len(domain)):
                yield dict(zip(domain, _vals))

        def collisions(f):
            # TODO: the list of all pairs (a, b) of inputs of f with a < b and the same output
            _result = ...
            return _result

        def missed(f, codomain):
            # TODO: the list of all elements of codomain that are not f(a) for any input a
            _result = ...
            return _result

        A, B = [0, 1, 2], [0, 1, 2, 3]

        # print(collisions({0: 0, 1: 1, 2: 3}))                    # expect []
        # print(collisions({0: 0, 1: 1, 2: 1}))                    # expect [(1, 2)]
        # print(collisions({0: 2, 1: 2, 2: 2}))                    # expect [(0, 1), (0, 2), (1, 2)]
        # print(missed({0: 0, 1: 1, 2: 3}, B))                     # expect [2]
        # print(missed({0: 0, 1: 1, 2: 2, 3: 2}, A))               # expect []
        # print(sum(1 for f in all_functions(A, B) if collisions(f) == []))        # expect 24  (of 64): the injections
        # print(sum(1 for f in all_functions(A, B) if len(collisions(f)) == 1))    # expect 36
        # print(sum(1 for g in all_functions(B, A) if missed(g, A) == []))         # expect 36  (of 81): the surjections
        # print(sum(1 for g in all_functions(B, A) if len(missed(g, A)) == 1))     # expect 42

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Factoring One Function Through Another

    A left inverse of $f$ is a solution $g$ of the equation $g \circ f = 1_A$. Replace the identity by an arbitrary function and you get a more general question. For $f \colon A \to B$ and $h \colon A \to C$, write `factor_after(h, f, B, C)`, the list of all $g \colon B \to C$ with $g \circ f = h$. For $f \colon A \to B$ and $h \colon C \to B$, write `factor_before(h, f, C, A)`, the list of all $k \colon C \to A$ with $f \circ k = h$. Before un-commenting each check, predict whether the answer is zero, one or several, and say which property of $f$ decides it.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(domain, codomain):
            for _vals in itertools.product(codomain, repeat=len(domain)):
                yield dict(zip(domain, _vals))

        def identity(X):
            return {_x: _x for _x in X}

        def compose(g, f):
            """The dict of g after f; its inputs are the inputs of f."""
            return {_a: g[f[_a]] for _a in f}

        def factor_after(h, f, B, C):
            # TODO: every g : B -> C with compose(g, f) == h
            _result = ...
            return _result

        def factor_before(h, f, C, A):
            # TODO: every k : C -> A with compose(f, k) == h
            _result = ...
            return _result

        A, B, C = [0, 1, 2], [0, 1, 2, 3], [0, 1]
        f = {0: 0, 1: 1, 2: 3}             # A -> B, injective
        f2 = {0: 0, 1: 1, 2: 1}            # A -> B, not injective
        p = {0: 0, 1: 1, 2: 2, 3: 2}       # B -> A, surjective
        h = {0: 0, 1: 1, 2: 1}             # A -> C
        h2 = {0: 0, 1: 1, 2: 0}            # A -> C

        # print(len(factor_after(identity(A), f, B, A)))      # expect 3   (the left inverses of f)
        # print(len(factor_after(h, f, B, C)))                # expect 2
        # print(len(factor_after(identity(A), f2, B, A)))     # expect 0
        # print(len(factor_after(h, f2, B, C)))               # expect 4
        # print(len(factor_after(h2, f2, B, C)))              # expect 0
        # print(factor_before({0: 0, 1: 3}, f, C, A))         # expect [{0: 0, 1: 2}]
        # print(len(factor_before({0: 2, 1: 0}, f, C, A)))    # expect 0
        # print(len(factor_before(identity(A), p, A, B)))     # expect 2   (the right inverses of p)
        # print(len(factor_before({0: 2, 1: 2}, p, C, B)))    # expect 4

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Testing a "For All" Statement, and Finding Counterexamples

    Let $F$ be the set of all $27$ functions $\{0,1,2\} \to \{0,1,2\}$. (i) Confirm Proposition 2(a) by checking $h \circ (g \circ f) = (h \circ g) \circ f$ for every triple in $F$. (ii) Count the ordered pairs $(f, g)$ in $F$ with $g \circ f = f \circ g$. Since the count is less than $27 \times 27 = 729$, any pair outside it is a counterexample to "composition is commutative".
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def all_functions(domain, codomain):
            for _vals in itertools.product(codomain, repeat=len(domain)):
                yield dict(zip(domain, _vals))

        def compose(g, f):
            return {_a: g[f[_a]] for _a in f}

        X = [0, 1, 2]
        F = list(all_functions(X, X))

        # TODO: True exactly when h∘(g∘f) == (h∘g)∘f for every f, g, h in F
        associative = ...

        # TODO: the number of ordered pairs (f, g) in F with g∘f == f∘g
        commuting_pairs = ...

        # print(len(F))               # expect 27
        # print(associative)          # expect True
        # print(commuting_pairs)      # expect 141

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    Six briefs. None of these statements is proved in the lecture; each can be proved with the moves modelled above.

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | `exercises/0b/p01_composite_of_surjections.md` | warm-up | unpack the definition (direct proof) |
    | P02 | `exercises/0b/p02_left_inverses_compose.md` | warm-up | equality of functions from associativity and identity laws |
    | P03 | `exercises/0b/p03_cancelling_from_a_composite.md` | core | direct proof; using a hypothesis about a composite |
    | P04 | `exercises/0b/p04_left_inverse_equals_right_inverse.md` | core | element-free calculation with composites |
    | P05 | `exercises/0b/p05_invertible_iff_bijective.md` | core | if-and-only-if; constructing a function and checking it is well defined |
    | P06 | `exercises/0b/p06_injective_iff_images_preserve_intersections.md` | stretch | if-and-only-if; equality of sets; choosing what to plug in |

    **Submitting a proof.** Write it in `proofs/0b/<same filename as the brief>` using the five steps (Goal, Given, Plan, Proof, What made it work), then ask Claude to review it.
    The review points at gaps and asks questions; it does not supply a model proof. Revise until there are no gaps.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [0A: Orientation](../0a_orientation/) &nbsp;|&nbsp; Next: [0C: Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher](../0c_proof_toolkit_uniqueness/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
