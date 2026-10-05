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
    # 0A: Orientation

    > *"Category theory takes a bird's eye view of mathematics."*
    > — Tom Leinster, *Basic Category Theory*, Introduction

    Welcome. This page is not a lecture. It is a map to look at before the walk: what category theory is about, one idea (the *universal property*) seen twice with nothing more than sets and functions, how the modules are laid out, and how the proof exercises and proof review work.

    You already know what a group and a vector space are. You have also said that proofs were the hard part. This course is built around that. Category theory has very few calculations in it; almost everything is a short proof assembled from definitions, and the same three or four proof shapes come back in every chapter. So the plan is to learn those shapes on purpose, in Part 0, on familiar ground, and then use them again and again. By the end you should be able to read a definition you have never seen, list what has to be checked, and check it.

    Nothing on this page needs to be memorised. Read it once, play with the widget in Section 4, and move on to **0B**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. What Category Theory Is

    Most of the mathematics you have met comes in the same two-layer package:

    | Things | Maps between the things |
    |--------|-------------------------|
    | sets | functions |
    | groups | group homomorphisms |
    | vector spaces over a field $k$ | linear maps |
    | topological spaces | continuous maps |
    | partially ordered sets | order-preserving maps |

    In each row, two maps that meet head to tail can be **composed**, composition is associative, and every thing has an **identity** map that does nothing. A *category* is exactly this package and nothing more: a collection of objects, a collection of maps (also called arrows) between them, a composition rule, and identities. Module 1A gives the precise definition.

    The surprising part is how much can be said using *only* the maps. Category theory deliberately refuses to look inside an object. It never asks "what are the elements of this group?"; it asks "what are the homomorphisms into it and out of it, and how do they compose?" From that height the details of any one subject disappear, and patterns that are shared by algebra, topology and order theory become visible. That is the bird's-eye view of the epigraph.

    Three ideas organise the whole course, and they turn out to be three views of one thing:

    - **Adjoint functors** (Part 2): pairs of constructions that go in opposite directions and fit together, such as "free vector space on a set" and "underlying set of a vector space".
    - **Representable functors and the Yoneda lemma** (Part 4): an object is completely determined by the maps into it.
    - **Limits** (Part 5): products, kernels, intersections and many other constructions are a single construction.

    What all three have in common is the idea of a **universal property**, and you can already understand one today.

    > Reference: [Leinster, Introduction (Ch 0)](https://arxiv.org/abs/1612.09375). A second gentle voice: [Perrone Ch 1](https://arxiv.org/abs/1912.10642).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. A First Universal Property: The One-Element Set

    Fix a set with exactly one element and call it $1$; say $1 = \{\star\}$. Here is a fact about it that mentions no elements of $1$ at all, only functions:

    > **Property (T).** A set $T$ has property (T) if for every set $X$ there is **exactly one** function $X \to T$.

    **The set $1$ has property (T).** Take any set $X$. There is at least one function $X \to 1$: send every $x \in X$ to $\star$. There is at most one: if $f, g \colon X \to 1$ are functions then for each $x$ both $f(x)$ and $g(x)$ are elements of $1$, and $1$ has only the element $\star$, so $f(x) = \star = g(x)$. Two functions with the same domain and codomain and the same value at every point are the same function.

    **No other size of set has it.** This needs two separate checks, one for each way of failing "exactly one".

    - *The empty set fails by having too few maps into it.* Take $X = \{0\}$. A function $\{0\} \to \emptyset$ would have to assign to $0$ an element of $\emptyset$, and there is none. So there is no function $\{0\} \to \emptyset$.
    - *A set with two or more elements fails by having too many.* Suppose $t \neq t'$ are elements of $T$ and take $X = \{0\}$ again. Then $0 \mapsto t$ and $0 \mapsto t'$ are two different functions $\{0\} \to T$.

    So property (T) holds for a set $T$ **exactly when** $T$ has one element. The property has located the one-element sets among all sets, without ever saying the words "one element".

    Notice what it has *not* done: it has not picked out a single set. $\{\star\}$, $\{7\}$ and $\{\emptyset\}$ all have property (T). They are different sets, but there is exactly one function from any of them to any other, and that function is a bijection. This is the typical outcome. A universal property determines an object *up to a unique isomorphism*, and that phrase gets a careful proof in Module 0C.

    **The shape to remember.** A universal property always reads

    $$\boxed{\text{for every } \ldots \text{ there exists a unique map } \ldots \text{ such that } \ldots}$$

    and so every proof about universal properties has two halves: an **existence** half (build a map) and a **uniqueness** half (show any two candidates are equal).

    The same sentence describes very different-looking objects elsewhere. Two examples you can check against what you know:

    - For every ring $R$ with a multiplicative identity there is exactly one ring homomorphism $\mathbb{Z} \to R$ (ring homomorphisms being required to preserve $1$).
    - If a vector space $V$ has a basis $(v_s)_{s \in S}$, then for every vector space $W$ and every function $f \colon S \to W$ there is exactly one linear map $V \to W$ sending each $v_s$ to $f(s)$.

    > Reference: [Leinster, Introduction (Ch 0)](https://arxiv.org/abs/1612.09375) opens with these examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. A Second Universal Property: The Product of Two Sets

    Let $A$ and $B$ be sets. You know the product $A \times B = \{(a, b) : a \in A,\ b \in B\}$, and it comes with two **projection** functions

    $$p_1 \colon A \times B \to A, \quad p_1(a, b) = a, \qquad\qquad p_2 \colon A \times B \to B, \quad p_2(a, b) = b.$$

    Here is what the product does, said using only functions:

    > **Universal property of the product.** For every set $X$ and every pair of functions $f \colon X \to A$ and $g \colon X \to B$, there is exactly one function $h \colon X \to A \times B$ such that
    > $$p_1 \circ h = f \qquad \text{and} \qquad p_2 \circ h = g.$$

    The picture is drawn below. The solid arrows are given; the dashed arrow is the one whose existence and uniqueness is being claimed. Saying the two triangles **commute** means precisely the two displayed equations.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "X": (2, 2, r"$X$"),
            "P": (2, 0, r"$A{\times}B$"),
            "A": (0, 0, r"$A$"),
            "B": (4, 0, r"$B$"),
        },
        [
            ("X", "A", r"$f$", {"side": -1}),
            ("X", "B", r"$g$"),
            ("X", "P", r"$h$", {"dashed": True, "color": "#b91c1c"}),
            ("P", "A", r"$p_1$"),
            ("P", "B", r"$p_2$", {"side": -1}),
        ],
        figsize=(5.6, 3.4),
        title="The universal property of the product",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the first proof of the course, so it is laid out in the five labelled steps that every lecture proof will use. Read it for its *shape*; you will be imitating that shape soon.

    **Goal.** For all sets $X$ and all functions $f \colon X \to A$, $g \colon X \to B$: (existence) there is a function $h \colon X \to A \times B$ with $p_1 \circ h = f$ and $p_2 \circ h = g$; (uniqueness) if $h'$ is another function $X \to A \times B$ with $p_1 \circ h' = f$ and $p_2 \circ h' = g$, then $h' = h$.

    **Given.** The definition of $A \times B$ as the set of ordered pairs; the formulas for $p_1$ and $p_2$; the fact that two ordered pairs are equal exactly when their first entries are equal and their second entries are equal; the fact that two functions with the same domain and codomain are equal when they agree at every element.

    **Plan.** Existence: write down a formula for $h$ and check the two equations. Uniqueness: take any $h'$ satisfying the two equations and show the equations *force* its value at each point.

    **Proof.** *Existence.* Define $h \colon X \to A \times B$ by $h(x) = (f(x), g(x))$. This is an element of $A \times B$ because $f(x) \in A$ and $g(x) \in B$. For every $x \in X$ we have $(p_1 \circ h)(x) = p_1(f(x), g(x)) = f(x)$ by the formula for $p_1$, so $p_1 \circ h = f$. In the same way $(p_2 \circ h)(x) = p_2(f(x), g(x)) = g(x)$, so $p_2 \circ h = g$.

    *Uniqueness.* Let $h' \colon X \to A \times B$ satisfy $p_1 \circ h' = f$ and $p_2 \circ h' = g$, and let $x \in X$. The value $h'(x)$ is an element of $A \times B$, so it is a pair; call it $(a, b)$. Then $a = p_1(a, b) = p_1(h'(x)) = f(x)$ by the first equation, and $b = p_2(a, b) = p_2(h'(x)) = g(x)$ by the second. So $h'(x) = (f(x), g(x)) = h(x)$. This holds for every $x \in X$, so $h' = h$. $\blacksquare$

    **What made it work.** In the uniqueness half we did not guess; we let the two equations tell us what $h'(x)$ had to be. Whenever you must show "any map with these properties equals this one", feed the properties an arbitrary input and see what they force.

    The cell below confirms the count by brute force on small sets, and then tries two impostors: a set that is too big (the mediating map exists but is not unique) and one that is too small (for some $f, g$ it does not exist at all). The universal property rejects both.
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def _functions(dom, cod):
            for _vals in itertools.product(cod, repeat=len(dom)):
                yield dict(zip(dom, _vals))

        def _count_mediating(X, P, p1, p2, f, g):
            return sum(
                1 for _h in _functions(X, P)
                if all(p1[_h[_x]] == f[_x] and p2[_h[_x]] == g[_x] for _x in X)
            )

        _X, _A, _B = [0, 1, 2], ["a0", "a1"], ["b0", "b1", "b2"]
        _f = {0: "a0", 1: "a1", 2: "a1"}
        _g = {0: "b2", 1: "b0", 2: "b2"}

        _prod = [(_a, _b) for _a in _A for _b in _B]
        _big = [(_a, _b, _t) for _a in _A for _b in _B for _t in (0, 1)]
        _small = [("a0", "b0"), ("a1", "b1")]

        print("X = {0,1,2},  A = {a0,a1},  B = {b0,b1,b2}")
        print(f"f = {_f}")
        print(f"g = {_g}\n")
        for _name, _P in [("A x B (6 elements)", _prod), ("A x B x {0,1} (12 elements)", _big), ("{(a0,b0), (a1,b1)} (2 elements)", _small)]:
            _p1 = {_p: _p[0] for _p in _P}
            _p2 = {_p: _p[1] for _p in _P}
            _n = _count_mediating(_X, _P, _p1, _p2, _f, _g)
            print(f"candidate {_name:32s} functions h with p1.h = f and p2.h = g: {_n}")

        print("\nNow every pair (f, g) at once, for the genuine product:")
        _p1 = {_p: _p[0] for _p in _prod}
        _p2 = {_p: _p[1] for _p in _prod}
        _counts = {
            _count_mediating(_X, _prod, _p1, _p2, _ff, _gg)
            for _ff in _functions(_X, _A) for _gg in _functions(_X, _B)
        }
        print(f"  set of counts over all 8 x 27 = 216 pairs (f, g): {_counts}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Teaser: Guess the Object from Its Maps

    Sections 2 and 3 described a set by the functions into it. How much can functions tell you? Try it.

    Below is a mystery finite set $M$. You are not allowed to look at its elements. You may choose a **probe** set $X$ with $0$ to $4$ elements, and you will be told two numbers: how many functions there are $X \to M$, and how many there are $M \to X$. Work out how many elements $M$ has, then enter a guess.

    Things to try: Which single probe settles the question on its own? Which mystery set answers "exactly one function" to every probe into it, and where have you seen that? Which mystery set has exactly one function *out of* it to every probe?
    """)
    return


@app.cell
def _(mo):
    mystery = mo.ui.dropdown(
        options=["Mystery set P", "Mystery set Q", "Mystery set R", "Mystery set S"],
        value="Mystery set P",
        label="Mystery set $M$",
    )
    probe = mo.ui.slider(start=0, stop=4, step=1, value=2, label="Number of elements of the probe set $X$")
    guess = mo.ui.dropdown(
        options=["?", "0", "1", "2", "3", "4"],
        value="?",
        label="My guess for the number of elements of $M$",
    )
    mo.vstack([mystery, probe, guess])
    return guess, mystery, probe


@app.cell(hide_code=True)
def _(guess, mo, mystery, probe):
    def _run():
        _hidden = {"Mystery set P": 3, "Mystery set Q": 1, "Mystery set R": 0, "Mystery set S": 2}
        _m = _hidden[mystery.value]
        _n = int(probe.value)
        _into = _m ** _n      # functions X -> M   (Python's 0 ** 0 is 1, which is the right count)
        _out = _n ** _m       # functions M -> X
        _lines = [
            "**Probe:** a set $X$ with " + str(_n) + " element" + ("" if _n == 1 else "s") + ".",
            "",
            "| | count |",
            "|---|---|",
            "| functions $X \\to M$ | **" + str(_into) + "** |",
            "| functions $M \\to X$ | **" + str(_out) + "** |",
            "",
        ]
        if guess.value == "?":
            _lines.append("*Enter a guess when you are ready.*")
        elif int(guess.value) == _m:
            _lines.append(
                "**Correct.** $M$ has " + str(_m) + " element" + ("" if _m == 1 else "s")
                + ". The probe with one element would have told you directly: a function "
                "$\\{0\\} \\to M$ is the same thing as a choice of one element of $M$."
            )
        else:
            _lines.append(
                "**Not yet.** That guess does not match the counts. "
                "Try the probe with one element and think about what a function out of it is."
            )
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What the teaser is showing.** The functions *out of* a one-element probe into $M$ are in bijection with the elements of $M$: so even "element" can be said in the language of maps. More generally, the collection of all maps into an object, from all possible probes, pins the object down completely (up to isomorphism). That statement, made precise, is the **Yoneda lemma** of Part 4, and it is the reason category theory can afford never to look inside an object.

    ---

    ## 5. How This Course Works

    **One textbook, in order.** The course follows Tom Leinster's *Basic Category Theory*, one section per module, with extra examples from Emily Riehl's *Category Theory in Context*. Both are free; the links are in the reference line at the end of every section. Part 0 leans on Richard Hammack's *Book of Proof*.

    **Every teaching module has the same layout.**

    1. An opening that says what question the module answers and what you will be able to *prove* at the end.
    2. Numbered concept sections. Each gives the motivation, then the **definition** in a quote block, then a list headed **Reading the definition** that turns it into a checklist, then examples and at least one non-example, then full proofs.
    3. **Common Proof Mistakes** for that module's material.
    4. **Why This Matters**: where the module is used later.
    5. **Compute It**: two or three short code skeletons on finite sets or finite categories, where a claim can be checked by brute force. You fill in the lines marked `# TODO`.
    6. **Prove It**: six proof exercises.

    **Proof anatomy.** Every proof in a lecture is written in five labelled steps, as in Section 3:

    | Step | What it contains |
    |------|------------------|
    | **Goal.** | The statement, with every "for all" and "there exists" written out |
    | **Given.** | Exactly which definitions and hypotheses may be used |
    | **Plan.** | One or two sentences: the shape of the argument |
    | **Proof.** | The steps, each justified by name |
    | **What made it work.** | The one idea to keep, and when to reach for it again |

    When you write your own proofs, write the first three steps *before* attempting the fourth. Most of the difficulty of a proof is in not knowing what is to be shown; the Goal and Given lines remove that difficulty.

    **Prove It: the proof exercises.** Each module has six briefs in `exercises/<module>/`, for example `exercises/0b/p01_composite_of_surjections.md`: two warm-ups, three core, one stretch. A brief has the statement, what you may use, what a complete proof must show, three or four hints that open one at a time, and a self-check list. **There are no solutions anywhere in this repository**, by design. A theorem proved in a lecture is never set as an exercise, so every exercise is yours to do.

    **How proof review works.**

    1. Write your proof in `proofs/<module>/pNN_<slug>.md` (the brief tells you the exact filename). The `proofs/` folder is yours and is not tracked by git.
    2. Ask Claude to review it. The review reads your argument line by line, points at any gap, and asks you a question about it. It will not rewrite the proof or hand you a model answer.
    3. Revise and ask again. When a proof has been reviewed and has no gaps, its row in `PROGRESS.md` is ticked.

    Open hints slowly. A good rule: write down your Goal, Given and Plan, and spend ten minutes stuck, before opening the next hint.

    **Flashcards.** `flashcards/` has one deck per Part: definitions, statements, and "which technique proves this?". They never contain the proof of an exercise.

    **Opening a lecture.** From the repository root: `pwsh ./launch.ps1 0b` (or `bash launch.sh 0b`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Notation

    The course uses Leinster's notation throughout. Only the first block is needed for Part 0; the rest is here so you can come back to it.

    | Symbol | Meaning | First used |
    |--------|---------|-----------|
    | $f \colon A \to B$ | a function (later: a map, an arrow) with domain $A$ and codomain $B$ | 0B |
    | $g \circ f$, also $gf$ | the composite "$g$ after $f$": first $f$, then $g$ | 0B |
    | $1_A$ | the identity on $A$ | 0B |
    | $\forall$, $\exists$, $\exists!$ | for all, there exists, there exists exactly one | 0B, 0C |
    | $A \cong B$ | $A$ is isomorphic to $B$ | 0C, 1B |
    | $A \times B$, $A + B$ | product, sum (for sets: the disjoint union) | 0A, 5A, 5B |
    | $1$, $0$ | a terminal object (for sets: a one-element set), an initial object (for sets: the empty set) | 0A, 2A |
    | $\mathcal{A}, \mathcal{B}, \mathcal{C}$ | categories | 1A |
    | $\mathbf{Set}, \mathbf{Grp}, \mathbf{Ab}, \mathbf{Mon}, \mathbf{Vect}_k, \mathbf{Top}, \mathbf{Cat}$ | the categories of sets, groups, abelian groups, monoids, vector spaces over $k$, topological spaces, small categories | 1A, 1C |
    | $\mathcal{A}(A, B)$ | the set of maps from $A$ to $B$ in the category $\mathcal{A}$ | 1A |
    | $\mathcal{A}^{\mathrm{op}}$ | the opposite category | 1B |
    | $[\mathcal{A}, \mathcal{B}]$ | the category of functors from $\mathcal{A}$ to $\mathcal{B}$ | 1D |
    | $F \dashv G$ | $F$ is left adjoint to $G$ | 2A |
    | $\bar{f}$ | the transpose of $f$ across an adjunction | 2A |
    | $\eta$, $\varepsilon$ | unit and counit of an adjunction | 2B |
    | $H^A = \mathcal{A}(A, -)$, $H_A = \mathcal{A}(-, A)$ | the two hom-functors of an object $A$ | 4A |

    One convention deserves a warning now, because it causes more wrong proofs than any other: **$g \circ f$ means $f$ first.** The composite $A \xrightarrow{f} B \xrightarrow{g} C$ is written $g \circ f$, because $(g \circ f)(a) = g(f(a))$.

    ---

    ## 7. The Road Ahead

    | Part | Modules | What it is about |
    |------|---------|------------------|
    | 0 | 0A, 0B, 0C | Orientation and the proof toolkit: definitions, direct proof, uniqueness, diagrams |
    | 1 | 1A to 1E | Categories, functors, natural transformations, equivalence |
    | 2 | 2A, 2B, 2C | Adjoint functors, three ways |
    | 3 | 3A | What we assume about sets, and questions of size |
    | 4 | 4A, 4B, 4C | Representable functors and the Yoneda lemma |
    | 5 | 5A, 5B, 5C | Limits and colimits |
    | 6 | 6A to 6D | Adjoints, representables and limits as one idea; monads |
    | 7 | 7A | Study guide: every definition and theorem in one place |

    The course is linear. The next two modules contain no category theory at all: **0B** is about reading definitions and writing direct proofs about functions, and **0C** is about uniqueness proofs and commutative diagrams. They are the most important two modules in the course for you, because every later proof is built from the moves practised there.

    > Sources for Part 0: [Leinster, Introduction (Ch 0)](https://arxiv.org/abs/1612.09375); [Hammack, *Book of Proof*](https://www.people.vcu.edu/~rhammack/BookOfProof/); [Riehl, Preface and §1.1](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [Course home](../) &nbsp;|&nbsp; Next: [0B: Proof Toolkit I: Definitions & Direct Proof](../0b_proof_toolkit_definitions/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
