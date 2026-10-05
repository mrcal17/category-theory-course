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
    # 1C: Functors

    > *Categories were defined in order to define functors, and functors in order to define natural transformations.*
    > — a remark of Saunders Mac Lane, paraphrased

    Whenever mathematicians define a kind of structure, they next define the maps that respect it: homomorphisms for groups, linear maps for vector spaces, continuous maps for spaces. A category is itself a kind of structure. **What is a structure-respecting map from one category to another?** The answer is a *functor*: something that sends objects to objects and arrows to arrows, and respects the only structure a category has, namely composition and identities.

    Functors are everywhere once you look. "Forget that this group is a group and keep the set" is a functor. "Build the free monoid on this set" is a functor. "Take the set of all arrows out of a fixed object" is a functor. For the two families of small examples from 1A, functors turn out to be things you already know: a functor between monoids is a monoid homomorphism, and a functor between posets is an order-preserving map.

    By the end of this module you will be able to prove that a given construction is a functor (or show which requirement fails), work with contravariant functors without losing track of the direction of arrows, decide whether a functor is faithful, full or essentially surjective and give counterexamples, and prove that functors compose.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Definition

    A category consists of objects and arrows, with composition and identities. A map of categories should send each kind of thing to the same kind of thing and respect the operations.

    > **Definition (functor).** Let $\mathcal{A}$ and $\mathcal{B}$ be categories. A **functor** $F \colon \mathcal{A} \to \mathcal{B}$ consists of
    >
    > - a function $\mathrm{ob}(\mathcal{A}) \to \mathrm{ob}(\mathcal{B})$, written $A \mapsto F(A)$;
    > - for each pair of objects $A, A'$ of $\mathcal{A}$, a function $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$, written $f \mapsto F(f)$;
    >
    > such that
    >
    > - **composition is preserved:** $F(f' \circ f) = F(f') \circ F(f)$ for all arrows $A \xrightarrow{f} A' \xrightarrow{f'} A''$ of $\mathcal{A}$;
    > - **identities are preserved:** $F(1_A) = 1_{F(A)}$ for every object $A$ of $\mathcal{A}$.

    **Reading the definition.** To show that a construction is a functor:

    *Supply:* (1) its value $F(A)$ on every object; (2) its value $F(f)$ on every arrow. A rule that only says what happens to objects is not yet a functor.

    *Verify:*
    1. **$F(f)$ lands in the right hom-set:** if $f \colon A \to A'$ then $F(f)$ is an arrow of $\mathcal{B}$ from $F(A)$ to $F(A')$. In categories of structured sets this includes checking that $F(f)$ is a homomorphism, or continuous, or whatever the arrows of $\mathcal{B}$ are required to be.
    2. **Composition:** $F(f' \circ f) = F(f') \circ F(f)$ for every composable pair. Item 1 guarantees the right-hand side is defined.
    3. **Identities:** $F(1_A) = 1_{F(A)}$ for every object.

    The picture shows what preserving composition means: a commuting triangle in $\mathcal{A}$ is carried to a commuting triangle in $\mathcal{B}$.

    **First examples.**

    - The **identity functor** $1_{\mathcal{A}} \colon \mathcal{A} \to \mathcal{A}$ sends every object and every arrow to itself. Both axioms read "$x = x$".
    - For a fixed object $B$ of $\mathcal{B}$, the **constant functor** $\mathcal{A} \to \mathcal{B}$ sends every object to $B$ and every arrow to $1_B$. Composition: $1_B = 1_B \circ 1_B$, by the identity law. Identities: $1_B = 1_B$.
    - The **inclusion** $\mathbf{Ab} \to \mathbf{Grp}$ sends each abelian group to itself, regarded as a group, and each homomorphism to itself.

    **A non-example.** Sending each group $G$ to its centre $Z(G) = \{ z \in G : zg = gz \text{ for all } g \in G \}$ looks like it should be a functor $\mathbf{Grp} \to \mathbf{Grp}$. It is not, and not merely because nobody has said what it does to arrows: *no* choice of what to do on arrows works.

    > **Proposition 1.1.** There is no functor $F \colon \mathbf{Grp} \to \mathbf{Grp}$ with $F(G) = Z(G)$ for every group $G$.

    **Goal.** For every assignment $f \mapsto F(f)$ on homomorphisms with $F(f) \colon Z(G) \to Z(H)$ for $f \colon G \to H$, at least one functor axiom fails.

    **Given.** Two facts from group theory: the centre of an abelian group is the whole group, and the centre of the symmetric group $S_3$ is the trivial subgroup $\{\mathrm{id}\}$. Also: every group homomorphism sends the identity element to the identity element.

    **Plan.** Proof by contradiction. Find homomorphisms $C_2 \xrightarrow{i} S_3 \xrightarrow{p} C_2$ whose composite is the identity of $C_2$, where $C_2 = \{1, t\}$ is the group of order two. A functor would have to send this to arrows $Z(C_2) \to Z(S_3) \to Z(C_2)$ composing to an identity; but the middle group has one element, and the outer groups have two.

    **Proof.** Suppose such a functor $F$ exists. Define $i \colon C_2 \to S_3$ by $i(1) = \mathrm{id}$, $i(t) = (1\,2)$; this is a homomorphism because $(1\,2)(1\,2) = \mathrm{id}$. Let $p \colon S_3 \to C_2$ send even permutations to $1$ and odd permutations to $t$; this is the sign homomorphism. Since $(1\,2)$ is odd, $p(i(t)) = t$, and $p(i(1)) = 1$, so $p \circ i = 1_{C_2}$.

    Apply $F$. Because $C_2$ is abelian, $F(C_2) = Z(C_2) = C_2$, and $F(S_3) = Z(S_3) = \{\mathrm{id}\}$. Then
    $$F(p) \circ F(i) = F(p \circ i) = F(1_{C_2}) = 1_{F(C_2)} = 1_{C_2},$$
    using preservation of composition, then $p \circ i = 1_{C_2}$, then preservation of identities. Evaluate at $t$: the right-hand side gives $t$. On the left, $F(i)(t)$ is an element of $\{\mathrm{id}\}$, so $F(i)(t) = \mathrm{id}$, and $F(p)$ is a homomorphism, so $F(p)(\mathrm{id}) = 1$. So the left-hand side gives $1$. Hence $1 = t$, a contradiction. $\blacksquare$

    **What made it work.** The two functor axioms together say that $F$ carries any equation between composites to an equation between composites. So an equation in $\mathcal{A}$ whose image *cannot* hold in $\mathcal{B}$ rules out a functor. Factoring an identity through an object whose image is too small is the standard way to show that a construction on objects is not functorial.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 0, "$A$"), "A1": (1.5, 2.2, "$A'$"), "A2": (3, 0, "$A''$"),
            "FA": (5.2, 0, "$F(A)$"), "FA1": (7.0, 2.2, "$F(A')$"), "FA2": (8.8, 0, "$F(A'')$"),
        },
        [
            ("A", "A1", "$f$"),
            ("A1", "A2", "$f'$"),
            ("A", "A2", r"$f' \circ f$", {"side": -1}),
            ("FA", "FA1", "$F(f)$"),
            ("FA1", "FA2", "$F(f')$"),
            ("FA", "FA2", r"$F(f' \circ f)$", {"side": -1, "color": "#b45309"}),
        ],
        figsize=(9.0, 3.6),
        title=r"A commuting triangle in $\mathcal{A}$ and its image: $F(f' \circ f) = F(f') \circ F(f)$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Forgetful and Free Functors

    Two families of functors connect the categories of structured sets from 1A.

    **Forgetful functors** discard structure. The functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ sends a group $G$ to its underlying set and a homomorphism $\varphi$ to the same $\varphi$, regarded as a mere function. Check the three items: a homomorphism $G \to H$ is in particular a function between the underlying sets (item 1); composition in $\mathbf{Grp}$ *is* composition of functions (item 2); the identity homomorphism *is* the identity function (item 3). The same reasoning gives forgetful functors $\mathbf{Mon} \to \mathbf{Set}$, $\mathbf{Vect}_k \to \mathbf{Set}$ and $\mathbf{Top} \to \mathbf{Set}$, and functors that forget only part of the structure, such as $\mathbf{Vect}_k \to \mathbf{Ab}$ (forget scalar multiplication, keep addition) and $\mathbf{Grp} \to \mathbf{Mon}$ (forget that inverses exist).

    **Free functors** go the other way and build structure from nothing. The simplest is the free monoid.

    > **Definition (free monoid on a set).** For a set $S$, let $W(S)$ be the set of all finite **words** $s_1 s_2 \cdots s_n$ with $n \ge 0$ and each $s_i \in S$, including the empty word $\varepsilon$ ($n = 0$). Concatenation of words makes $W(S)$ a monoid with unit $\varepsilon$. For a function $f \colon S \to T$, define $W(f) \colon W(S) \to W(T)$ by applying $f$ to each letter:
    > $$W(f)(s_1 s_2 \cdots s_n) = f(s_1) f(s_2) \cdots f(s_n), \qquad W(f)(\varepsilon) = \varepsilon.$$

    **Reading the definition.** For $W$ to be a functor $\mathbf{Set} \to \mathbf{Mon}$ we must check: (1) $W(f)$ is a monoid homomorphism, not just a function; (2) $W(g \circ f) = W(g) \circ W(f)$; (3) $W(1_S) = 1_{W(S)}$.

    > **Proposition 2.1.** $W$ is a functor $\mathbf{Set} \to \mathbf{Mon}$.

    **Goal.** The three items above, for all sets $S, T, R$ and all functions $f \colon S \to T$, $g \colon T \to R$.

    **Given.** The definitions of $W(S)$, concatenation and $W(f)$. Two functions with the same domain and codomain are equal when they agree on every element; here an element is a word.

    **Plan.** Direct: evaluate both sides on an arbitrary word $s_1 \cdots s_n$.

    **Proof.**
    (1) Let $v = s_1 \cdots s_m$ and $w = s'_1 \cdots s'_n$ be words in $S$. Their concatenation is $vw = s_1 \cdots s_m s'_1 \cdots s'_n$, so
    $$W(f)(vw) = f(s_1) \cdots f(s_m) f(s'_1) \cdots f(s'_n) = W(f)(v)\, W(f)(w),$$
    by the definition of $W(f)$ and of concatenation in $W(T)$. Also $W(f)(\varepsilon) = \varepsilon$ by definition. So $W(f)$ preserves the operation and the unit.

    (2) Let $s_1 \cdots s_n \in W(S)$. Then
    $$W(g \circ f)(s_1 \cdots s_n) = g(f(s_1)) \cdots g(f(s_n)) = W(g)\big(f(s_1) \cdots f(s_n)\big) = W(g)\big(W(f)(s_1 \cdots s_n)\big).$$
    The first equality is the definition of $W(g \circ f)$, the second the definition of $W(g)$, the third the definition of $W(f)$. Both functions agree on every word, so $W(g \circ f) = W(g) \circ W(f)$.

    (3) $W(1_S)(s_1 \cdots s_n) = 1_S(s_1) \cdots 1_S(s_n) = s_1 \cdots s_n$, so $W(1_S)$ is the identity function on $W(S)$. $\blacksquare$

    **What made it work.** $W(f)$ was defined "letter by letter", and both functor axioms hold letter by letter. The step that is easy to forget is (1): $F(f)$ must be an arrow of the *target* category.

    Other free functors follow the same pattern: the free vector space $\mathbf{Set} \to \mathbf{Vect}_k$ sends $S$ to the space of formal finite linear combinations of elements of $S$, and a function $f$ to the linear map that applies $f$ to each basis element. In what sense these are "free", and how they are tied to the forgetful functors, is the subject of 2A.

    **A non-example.** Keep $S \mapsto W(S)$ on objects but send every function $f \colon S \to T$ to the homomorphism $c_f \colon W(S) \to W(T)$ that maps every word to $\varepsilon$. Items 1 and 2 hold: $c_f$ is a homomorphism, and $c_g \circ c_f = c_{g \circ f}$ because both send every word to $\varepsilon$. Item 3 fails: for $S = \{s\}$, $c_{1_S}$ sends the one-letter word $s$ to $\varepsilon$, so $c_{1_S} \neq 1_{W(S)}$. Preserving composition does not imply preserving identities.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell
def _():
    def _run():
        import itertools

        def W(f):
            return lambda word: tuple(f[_s] for _s in word)

        def words(alphabet, max_len):
            for _n in range(max_len + 1):
                yield from itertools.product(alphabet, repeat=_n)

        _S, _T = ["a", "b"], ["x", "y", "z"]
        _f = {"a": "x", "b": "z"}
        _g = {"x": 0, "y": 0, "z": 1}
        _gf = {_s: _g[_f[_s]] for _s in _S}
        _ws = list(words(_S, 4))
        print("=== Proposition 2.1 on all words of length <= 4 in {a, b} ===")
        print(f"  number of words tested                 : {len(_ws)}")
        print(f"  example: W(f)(a b b a)                 = {' '.join(W(_f)(('a', 'b', 'b', 'a')))}")
        print(f"  W(f)(vw) == W(f)(v) W(f)(w) for all v,w: {all(W(_f)(_v + _w) == W(_f)(_v) + W(_f)(_w) for _v in _ws for _w in _ws)}")
        print(f"  W(g∘f) == W(g)∘W(f) on every word      : {all(W(_gf)(_w) == W(_g)(W(_f)(_w)) for _w in _ws)}")
        print(f"  W(1_S) is the identity on every word   : {all(W({_s: _s for _s in _S})(_w) == _w for _w in _ws)}")

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Functors Between Monoids and Between Posets

    In 1A a monoid became a one-object category and a preorder became a category with at most one arrow between any two objects. What is a functor between such categories?

    > **Proposition 3.1.** Let $M$ and $N$ be monoids, regarded as one-object categories with objects $\star_M$ and $\star_N$. A functor $F \colon M \to N$ is the same thing as a monoid homomorphism $M \to N$: the function on arrows of any functor is a monoid homomorphism, and every monoid homomorphism is the function on arrows of exactly one functor.

    **Goal.** (i) If $F$ is a functor, the function $\varphi \colon M \to N$, $\varphi(m) = F(m)$, satisfies $\varphi(m'm) = \varphi(m')\varphi(m)$ for all $m, m' \in M$ and $\varphi(e_M) = e_N$. (ii) If $\varphi \colon M \to N$ is a monoid homomorphism, there is exactly one functor $F$ with $F(m) = \varphi(m)$ for all $m \in M$.

    **Given.** Proposition 4.1 of 1A: the arrows of $M$ are its elements, $\circ$ is the multiplication, and $1_{\star_M} = e_M$; likewise for $N$.

    **Plan.** Unpack the definition of a functor when each category has one object, and compare with the definition of a monoid homomorphism.

    **Proof.**
    (i) Let $F$ be a functor. For $m, m' \in M$, preservation of composition gives $F(m' \circ m) = F(m') \circ F(m)$, which in the notation of the monoids reads $\varphi(m'm) = \varphi(m')\varphi(m)$. Preservation of identities gives $F(1_{\star_M}) = 1_{F(\star_M)} = 1_{\star_N}$, that is, $\varphi(e_M) = e_N$.

    (ii) Let $\varphi$ be a monoid homomorphism. On objects there is no choice: $N$ has only one object, so $F(\star_M) = \star_N$. On arrows put $F(m) = \varphi(m)$, which is an arrow $\star_N \to \star_N$, so item 1 of the checklist holds. Every pair of arrows of $M$ is composable, and $F(m' \circ m) = \varphi(m'm) = \varphi(m')\varphi(m) = F(m') \circ F(m)$ because $\varphi$ preserves multiplication. Finally $F(1_{\star_M}) = \varphi(e_M) = e_N = 1_{\star_N}$ because $\varphi$ preserves the unit. So $F$ is a functor, and it is the only one with these values on arrows, because a functor is determined by its values on objects and arrows. $\blacksquare$

    **What made it work.** With one object, "for every composable pair" becomes "for every pair", and the functor axioms become the homomorphism axioms word for word. Functors generalise homomorphisms in the same way categories generalise monoids.

    **Examples.**

    - The homomorphism $(\mathbb{N}, +, 0) \to (\mathbb{N}, \times, 1)$, $n \mapsto 2^n$, is a functor: $2^{m+n} = 2^m 2^n$ and $2^0 = 1$.
    - **Posets.** If $P$ and $Q$ are posets regarded as categories, a functor $P \to Q$ is the same thing as an order-preserving map, that is, a function $\varphi$ with $x \le y \Rightarrow \varphi(x) \le \varphi(y)$. Proving this is exercise P01.
    - **Group actions.** Let $G$ be a group regarded as a one-object category. A functor $F \colon G \to \mathbf{Set}$ consists of one set $S = F(\star)$ and, for each $g \in G$, a function $F(g) \colon S \to S$, with $F(gh) = F(g) \circ F(h)$ and $F(e) = 1_S$. That is exactly a set with a left action of $G$. A functor $G \to \mathbf{Vect}_k$ is, in the same way, a linear representation of $G$.

    **Non-examples.** As maps on arrows from the one-object category $(\mathbb{N}, +, 0)$ to itself:

    - $n \mapsto n + 1$ fails to preserve the identity: it sends the identity arrow $0$ to $1$.
    - $n \mapsto n^2$ preserves the identity ($0 \mapsto 0$) but not composition: the composite of the arrows $1$ and $1$ is $2$, which is sent to $4$, whereas the composite of the images is $1 + 1 = 2$.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Functors Out of Tiny Categories, and What Functors Do Not Preserve

    Let $\mathbf{2}$ be the category with two objects $0, 1$ and one non-identity arrow $u \colon 0 \to 1$ (1B, Section 5). A functor out of $\mathbf{2}$ has very little to do, and working out exactly how little is a good exercise in the definition.

    > **Proposition 4.1.** Let $\mathcal{B}$ be a category. For every arrow $b \colon X \to Y$ of $\mathcal{B}$ there is exactly one functor $F \colon \mathbf{2} \to \mathcal{B}$ with $F(u) = b$.

    **Goal.** Existence: some functor $F$ has $F(u) = b$. Uniqueness: any two functors $F, F'$ with $F(u) = b = F'(u)$ agree on all objects and all arrows of $\mathbf{2}$.

    **Given.** $\mathbf{2}$ has objects $0, 1$, arrows $1_0, 1_1, u$, and its only composable pairs are $(1_0, 1_0)$, $(u, 1_0)$, $(1_1, u)$, $(1_1, 1_1)$.

    **Plan.** Existence and uniqueness, proved separately (0C). For uniqueness, see which values the definition forces. For existence, take the forced values and verify the axioms.

    **Proof.**
    *Uniqueness.* Let $F$ be a functor with $F(u) = b$. By the definition of a functor, $F(u)$ is an arrow from $F(0)$ to $F(1)$. Since $b$ has domain $X$ and codomain $Y$, and an arrow has only one domain and one codomain, $F(0) = X$ and $F(1) = Y$. By preservation of identities, $F(1_0) = 1_X$ and $F(1_1) = 1_Y$. So every value of $F$ is determined by $b$.

    *Existence.* Define $F(0) = X$, $F(1) = Y$, $F(1_0) = 1_X$, $F(1_1) = 1_Y$, $F(u) = b$. Each arrow is sent to an arrow between the right objects. Identities are preserved by definition. For composition, every composable pair of $\mathbf{2}$ contains an identity. If the pair is $(g, 1_A)$, with $g \colon A \to A'$, then $F(g \circ 1_A) = F(g)$ by the identity law in $\mathbf{2}$, and $F(g) \circ F(1_A) = F(g) \circ 1_{F(A)} = F(g)$ by the identity law in $\mathcal{B}$. If the pair is $(1_{A'}, g)$ the argument is the same with the other identity law. So composition is preserved. $\blacksquare$

    **What made it work.** In any functor-checking proof, the composition axiom is automatic for pairs in which one arrow is an identity. Only composites of two non-identity arrows need real work, and $\mathbf{2}$ has none.

    So functors $\mathbf{2} \to \mathcal{B}$ correspond to arrows of $\mathcal{B}$. In the same way, a functor from the one-object, one-arrow category to $\mathcal{B}$ is a choice of an object of $\mathcal{B}$. Section 9 lets you confirm these counts.

    **A consequence: functors need not preserve monics or epics.** In $\mathbf{2}$ the arrow $u$ is monic and epic (1B, Section 2: $\mathbf{2}$ is a poset). Take $\mathcal{B} = \mathbf{Set}$ and let $b$ be the unique function $\{1, 2\} \to \{1\}$, which is not injective and so not monic. By Proposition 4.1 there is a functor $F \colon \mathbf{2} \to \mathbf{Set}$ with $F(u) = b$. So $F$ sends a monic to a non-monic. The reason is that "monic" quantifies over all test arrows into the domain, and $\mathbf{Set}$ has many more test arrows than $\mathbf{2}$ has.

    What a functor certainly preserves is any **equation between composites**: if $h = g \circ f$ in $\mathcal{A}$ then $F(h) = F(g) \circ F(f)$ in $\mathcal{B}$. Whether it preserves isomorphisms is exercise P03.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Contravariant Functors

    Some constructions reverse arrows. Given a function $f \colon X \to Y$ and a subset $S \subseteq Y$, the natural thing to form is the preimage $f^{-1}(S) \subseteq X$: subsets of $Y$ are turned into subsets of $X$, against the direction of $f$. The opposite category of 1B lets us describe this without a new definition.

    > **Definition (contravariant functor).** A **contravariant functor from $\mathcal{A}$ to $\mathcal{B}$** is a functor $F \colon \mathcal{A}^{\mathrm{op}} \to \mathcal{B}$. An ordinary functor $\mathcal{A} \to \mathcal{B}$ is called **covariant** when the contrast is needed.

    **Reading the definition.** Unpack it using the definition of $\mathcal{A}^{\mathrm{op}}$. An arrow $f \colon A \to A'$ of $\mathcal{A}$ is an arrow $A' \to A$ of $\mathcal{A}^{\mathrm{op}}$, so $F$ sends it to an arrow $F(A') \to F(A)$. For $A \xrightarrow{f} A' \xrightarrow{f'} A''$ in $\mathcal{A}$, the composite $f' \circ f$ is $f \circ^{\mathrm{op}} f'$ in $\mathcal{A}^{\mathrm{op}}$, and a functor preserves composition, so $F(f' \circ f) = F(f) \circ F(f')$. So a contravariant functor from $\mathcal{A}$ to $\mathcal{B}$ amounts to:

    1. an object $F(A)$ of $\mathcal{B}$ for each object $A$ of $\mathcal{A}$;
    2. for each arrow $f \colon A \to A'$ of $\mathcal{A}$, an arrow $F(f) \colon F(A') \to F(A)$ **in the reverse direction**;
    3. $F(f' \circ f) = F(f) \circ F(f')$: the **order of composition is reversed**;
    4. $F(1_A) = 1_{F(A)}$.

    > **Proposition 5.1 (the contravariant power-set functor).** For a set $X$ let $\mathcal{P}(X)$ be the set of all subsets of $X$, and for a function $f \colon X \to Y$ let $\mathcal{P}(f) \colon \mathcal{P}(Y) \to \mathcal{P}(X)$ be the preimage function $S \mapsto f^{-1}(S) = \{ x \in X : f(x) \in S \}$. Then $\mathcal{P}$ is a functor $\mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$.

    **Goal.** For all functions $X \xrightarrow{f} Y \xrightarrow{g} Z$: $\mathcal{P}(g \circ f) = \mathcal{P}(f) \circ \mathcal{P}(g)$ as functions $\mathcal{P}(Z) \to \mathcal{P}(X)$. For every set $X$: $\mathcal{P}(1_X) = 1_{\mathcal{P}(X)}$.

    **Given.** The definition of preimage. Two subsets of $X$ are equal when they have the same elements.

    **Plan.** Fix a subset $S \subseteq Z$ and show the two subsets of $X$ have the same elements, by a chain of equivalences.

    **Proof.** $\mathcal{P}(f)$ is a function from $\mathcal{P}(Y)$ to $\mathcal{P}(X)$, the reverse direction, as item 2 requires. Let $S \subseteq Z$ and $x \in X$. Then
    $$x \in (g \circ f)^{-1}(S) \iff g(f(x)) \in S \iff f(x) \in g^{-1}(S) \iff x \in f^{-1}\big(g^{-1}(S)\big).$$
    Each step is the definition of preimage (for $g \circ f$, for $g$, for $f$). So $\mathcal{P}(g \circ f)(S) = \mathcal{P}(f)(\mathcal{P}(g)(S))$ for every $S$, which is $\mathcal{P}(g \circ f) = \mathcal{P}(f) \circ \mathcal{P}(g)$. For identities: $x \in 1_X^{-1}(S) \iff 1_X(x) \in S \iff x \in S$, so $\mathcal{P}(1_X)(S) = S$ for every $S \subseteq X$. $\blacksquare$

    **What made it work.** The preimage is defined by *composing with $f$ and then testing*, and composing first with $f$ and then with $g$ is why the order flips. Whenever a construction is "things defined on the codomain, pulled back along $f$", expect a contravariant functor.

    **More examples.**

    - The **dual space**: $V \mapsto V^* = \mathbf{Vect}_k(V, k)$, and a linear map $f \colon V \to W$ is sent to $f^* \colon W^* \to V^*$, $\theta \mapsto \theta \circ f$. This is a functor $\mathbf{Vect}_k^{\mathrm{op}} \to \mathbf{Vect}_k$.
    - **Real-valued continuous functions**: a space $X$ is sent to the set $C(X)$ of continuous maps $X \to \mathbb{R}$, and a continuous map $f \colon X \to Y$ to $C(Y) \to C(X)$, $q \mapsto q \circ f$.
    - For comparison, the **direct image** is covariant: sending $f \colon X \to Y$ to $\mathcal{P}(X) \to \mathcal{P}(Y)$, $S \mapsto f(S) = \{f(x) : x \in S\}$, gives a functor $\mathbf{Set} \to \mathbf{Set}$, because $(g \circ f)(S)$ and $g(f(S))$ are both $\{g(f(x)) : x \in S\}$ and $1_X(S) = S$.

    **Non-example.** The assignment $X \mapsto \mathcal{P}(X)$, $f \mapsto f^{-1}$ is *not* a functor $\mathbf{Set} \to \mathbf{Set}$: for $f \colon X \to Y$, the function $f^{-1}$ goes from $\mathcal{P}(Y)$ to $\mathcal{P}(X)$, so it is not an element of $\mathbf{Set}(\mathcal{P}(X), \mathcal{P}(Y))$. Item 1 of the checklist in Section 1 fails before the axioms can be stated. The same data *is* a functor once the domain is declared to be $\mathbf{Set}^{\mathrm{op}}$.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {
            "A": (0, 2.2, "$A$"), "A1": (0, 0, "$A'$"),
            "FA": (3.2, 2.2, "$F(A)$"), "FA1": (3.2, 0, "$F(A')$"),
            "GA": (6.6, 2.2, "$F(A)$"), "GA1": (6.6, 0, "$F(A')$"),
        },
        [
            ("A", "A1", "$f$", {"side": -1}),
            ("FA", "FA1", "$F(f)$", {"color": "#1d4ed8"}),
            ("GA1", "GA", "$F(f)$", {"color": "#b45309"}),
        ],
        figsize=(7.6, 3.4),
        title="An arrow of $\\mathcal{A}$ (left), its image under a covariant functor (middle)\nand under a contravariant functor (right)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Hom-Functors

    1A suggested treating a hom-set $\mathcal{A}(A, B)$ as an object of study. Fix $A$ and let $B$ vary: we get a set for each object $B$. Composition makes this assignment a functor, and it is the most important functor in the course.

    Throughout this section $\mathcal{A}$ is a category whose hom-sets are sets.

    > **Definition (covariant hom-functor).** Fix an object $A$ of $\mathcal{A}$. The functor $H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$ is defined by
    >
    > - on objects: $H^A(B) = \mathcal{A}(A, B)$;
    > - on arrows: for $g \colon B \to B'$, the function $H^A(g) \colon \mathcal{A}(A, B) \to \mathcal{A}(A, B')$ is $p \mapsto g \circ p$.

    **Reading the definition.** An element of $H^A(B)$ is an arrow $p \colon A \to B$. Given $g \colon B \to B'$, the only thing to do with $p$ and $g$ is compose them, and $g \circ p$ is an arrow $A \to B'$, an element of $H^A(B')$. To check $H^A$ is a functor we must verify (1) $H^A(g)$ is a function between the right sets, which we have just done; (2) $H^A(g' \circ g) = H^A(g') \circ H^A(g)$; (3) $H^A(1_B) = 1_{H^A(B)}$.

    > **Proposition 6.1.** $H^A$ is a functor $\mathcal{A} \to \mathbf{Set}$.

    **Goal.** For all arrows $B \xrightarrow{g} B' \xrightarrow{g'} B''$ and every $p \in \mathcal{A}(A, B)$: $H^A(g' \circ g)(p) = H^A(g')\big(H^A(g)(p)\big)$. For every object $B$ and every $p \in \mathcal{A}(A, B)$: $H^A(1_B)(p) = p$.

    **Given.** The definition of $H^A$ and the axioms of the category $\mathcal{A}$. Two functions are equal when they agree at every element of their common domain; here an element is an arrow $p$.

    **Plan.** Evaluate both sides at an arbitrary $p$ and see which axiom of $\mathcal{A}$ is needed.

    **Proof.** Let $p \colon A \to B$. Then
    $$H^A(g' \circ g)(p) = (g' \circ g) \circ p = g' \circ (g \circ p) = H^A(g')(g \circ p) = H^A(g')\big(H^A(g)(p)\big).$$
    The first, third and fourth equalities are the definition of $H^A$ on arrows; the second is associativity in $\mathcal{A}$. This holds for every $p$, so $H^A(g' \circ g) = H^A(g') \circ H^A(g)$. Next, $H^A(1_B)(p) = 1_B \circ p = p$ by the identity law in $\mathcal{A}$, so $H^A(1_B)$ is the identity function on $\mathcal{A}(A, B)$. $\blacksquare$

    **What made it work.** The two functor axioms for $H^A$ *are* the associativity axiom and one identity law of $\mathcal{A}$, read as statements about the function "compose with $g$". The elements of the sets involved are arrows, so "evaluate at an element" means "evaluate at an arrow $p$".

    Fixing the second variable instead gives a contravariant functor.

    > **Definition (contravariant hom-functor).** Fix an object $A$ of $\mathcal{A}$. The functor $H_A = \mathcal{A}(-, A) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ is defined by $H_A(B) = \mathcal{A}(B, A)$ on objects and, for $g \colon B \to B'$ in $\mathcal{A}$, by the function $H_A(g) \colon \mathcal{A}(B', A) \to \mathcal{A}(B, A)$, $q \mapsto q \circ g$.

    Proving that $H_A$ is a functor is exercise P04.

    **Examples.**

    - In $\mathbf{Set}$ with $A = \{\ast\}$ a one-element set: a function $\{\ast\} \to B$ is a choice of an element of $B$, so $H^{\{\ast\}}(B)$ corresponds to $B$ itself, and $H^{\{\ast\}}(g)$ corresponds to $g$.
    - In $\mathbf{Vect}_k$ with $A = k$: $H_k(V) = \mathbf{Vect}_k(V, k)$ is the underlying set of the dual space $V^*$, and $H_k(f)$ is $\theta \mapsto \theta \circ f$, the map $f^*$ of Section 5.
    - In a monoid $M$ regarded as a one-object category: $H^\star(\star) = M$, and $H^\star(m)$ is the function $M \to M$, $p \mapsto m \cdot p$: left multiplication by $m$.
    - In a poset $P$: $H^x(y) = P(x, y)$ is a one-element set if $x \le y$ and the empty set otherwise.

    **Non-example.** For a fixed $A$, sending $B$ to $\mathcal{A}(A, B)$ and $g \colon B \to B'$ to "$p \mapsto p \circ g$" is not a functor, and not even well formed: $p \colon A \to B$ and $g \colon B \to B'$ compose only in the order $g \circ p$. Before checking an axiom, check that each composite you write is defined.

    > Reference: [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf). Leinster introduces $H^A$ and $H_A$ in §4.1 of [Basic Category Theory](https://arxiv.org/abs/1612.09375); we meet them early because they are such useful examples.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        {"A": (1.6, 2.3, "$A$"), "B": (0, 0, "$B$"), "B1": (3.2, 0, "$B'$")},
        [
            ("A", "B", "$p$", {"side": -1}),
            ("B", "B1", "$g$", {"side": -1}),
            ("A", "B1", r"$H^A(g)(p) = g \circ p$", {"color": "#b45309"}),
        ],
        figsize=(5.4, 3.6),
        title=r"$H^A(g)$ turns an arrow $A \to B$ into an arrow $A \to B'$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Faithful, Full, Essentially Surjective

    A function can be injective or surjective. For a functor, the useful versions of these properties are stated **one hom-set at a time**.

    > **Definition.** A functor $F \colon \mathcal{A} \to \mathcal{B}$ is
    >
    > - **faithful** if for every pair of objects $A, A'$ of $\mathcal{A}$, the function $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$, $f \mapsto F(f)$, is injective;
    > - **full** if for every pair of objects $A, A'$ of $\mathcal{A}$, that function is surjective;
    > - **essentially surjective on objects** if for every object $B$ of $\mathcal{B}$ there exists an object $A$ of $\mathcal{A}$ with $F(A) \cong B$.

    **Reading the definition.**

    - To prove $F$ is **faithful**: take two arrows $f_1, f_2 \colon A \to A'$ **with the same domain and the same codomain**, assume $F(f_1) = F(f_2)$, and deduce $f_1 = f_2$.
    - To prove $F$ is **full**: take objects $A, A'$ of $\mathcal{A}$ and an arbitrary arrow $b \colon F(A) \to F(A')$ of $\mathcal{B}$, and produce $f \colon A \to A'$ with $F(f) = b$.
    - To prove $F$ is **essentially surjective**: take an object $B$ of $\mathcal{B}$ and produce an object $A$ **and an isomorphism** $F(A) \to B$.
    - To disprove any of them, one counterexample is enough.

    Two warnings. Faithful does **not** say that $F$ is injective on the collection of all arrows: arrows from different hom-sets may have the same image. Full does **not** say that every arrow of $\mathcal{B}$ is $F$ of something: only arrows between objects of the form $F(A)$ and $F(A')$ are at stake.

    > **Proposition 7.1.** The forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ is faithful, is not full, and is not essentially surjective on objects.

    **Goal.** (i) For all groups $G, H$ and homomorphisms $\varphi, \psi \colon G \to H$: if $U(\varphi) = U(\psi)$ then $\varphi = \psi$. (ii) There exist groups $G, H$ and a function $U(G) \to U(H)$ that is not $U(\varphi)$ for any homomorphism $\varphi \colon G \to H$. (iii) There exists a set $B$ such that no group $G$ has $U(G) \cong B$.

    **Given.** $U(\varphi)$ is $\varphi$ regarded as a function. Homomorphisms send the identity element to the identity element. Isomorphisms in $\mathbf{Set}$ are bijections.

    **Plan.** (i) Direct. (ii) and (iii) Counterexamples.

    **Proof.**
    (i) Let $\varphi, \psi \colon G \to H$ be homomorphisms with $U(\varphi) = U(\psi)$. Then $\varphi$ and $\psi$ are the same function between the underlying sets. Two homomorphisms $G \to H$ that are equal as functions are equal as arrows of $\mathbf{Grp}$. So $\varphi = \psi$.

    (ii) Take $G = H = (\mathbb{Z}, +)$ and the function $s \colon \mathbb{Z} \to \mathbb{Z}$, $s(n) = n + 1$. If $s = U(\varphi)$ for a homomorphism $\varphi$, then $\varphi(0) = s(0) = 1$; but a homomorphism sends $0$ to $0$. So $s$ is not in the image of $\mathbf{Grp}(\mathbb{Z}, \mathbb{Z}) \to \mathbf{Set}(\mathbb{Z}, \mathbb{Z})$, and $U$ is not full.

    (iii) Take $B = \emptyset$. For any group $G$, the set $U(G)$ contains the identity element of $G$, so it is non-empty, and there is no bijection from a non-empty set to $\emptyset$. So $U(G) \not\cong \emptyset$ for every $G$. $\blacksquare$

    **What made it work.** For forgetful functors, faithfulness is built in: an arrow *is* its underlying function together with a property. Fullness fails because most functions lack the property. In each negative part a single explicit counterexample was the whole proof.

    **More examples.**

    - The inclusion $\mathbf{Ab} \to \mathbf{Grp}$ is faithful and full: for abelian groups $A, A'$, the arrows $A \to A'$ in $\mathbf{Ab}$ and in $\mathbf{Grp}$ are the same homomorphisms. It is not essentially surjective: a group isomorphic to an abelian group is abelian, and $S_3$ is not.
    - The forgetful functor $\mathbf{Top} \to \mathbf{Set}$ is faithful, not full (not every function is continuous), and essentially surjective: every set is the underlying set of a space, for instance with the discrete topology.
    - Let $\mathcal{D}$ be the discrete category with two objects $A, B$ and let $\mathbf{1}$ be the category with one object $\star$ and one arrow. The only functor $F \colon \mathcal{D} \to \mathbf{1}$ is **faithful**, because each hom-set of $\mathcal{D}$ has at most one element, so each function on hom-sets is injective. Yet $F(1_A) = F(1_B)$: it is not injective on arrows. It is **not full**, because $\mathcal{D}(A, B)$ is empty while $\mathbf{1}(F(A), F(B)) = \{1_\star\}$ is not.

    **Subcategories.** A **subcategory** $\mathcal{S}$ of $\mathcal{A}$ consists of some of the objects of $\mathcal{A}$ and, for each pair $S, S'$ of them, some of the arrows $S \to S'$ of $\mathcal{A}$, such that $\mathcal{S}$ contains the identity of each of its objects and the composite of any two composable arrows it contains. It is a **full subcategory** if it contains *all* arrows of $\mathcal{A}$ between its objects. The inclusion functor of a subcategory is always faithful, and it is full exactly when the subcategory is full. So $\mathbf{Ab}$ is a full subcategory of $\mathbf{Grp}$, and a full subcategory is specified just by saying which objects it has.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375) (faithful, full, subcategories) and §1.3 (essentially surjective on objects); [Riehl §1.5](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8. Composing Functors: the Category of Categories

    Functors are maps, so we should be able to compose them.

    > **Definition (composite functor).** Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{C}$ be functors. The composite $G \circ F \colon \mathcal{A} \to \mathcal{C}$ is defined by $(G \circ F)(A) = G(F(A))$ on objects and $(G \circ F)(f) = G(F(f))$ on arrows.

    **Reading the definition.** For this to be a functor: (1) $G(F(f))$ must be an arrow from $G(F(A))$ to $G(F(A'))$ when $f \colon A \to A'$; (2) composition must be preserved; (3) identities must be preserved.

    > **Proposition 8.1.** $G \circ F$ is a functor $\mathcal{A} \to \mathcal{C}$.

    **Goal.** The three items above, for all arrows $A \xrightarrow{f} A' \xrightarrow{f'} A''$ and all objects $A$ of $\mathcal{A}$.

    **Given.** $F$ and $G$ are functors: each satisfies the three items.

    **Plan.** Direct. Each item for $G \circ F$ follows by using the same item for $F$ and then for $G$.

    **Proof.**
    (1) Let $f \colon A \to A'$. Since $F$ is a functor, $F(f) \colon F(A) \to F(A')$ in $\mathcal{B}$. Since $G$ is a functor, $G(F(f)) \colon G(F(A)) \to G(F(A'))$ in $\mathcal{C}$.

    (2) $(G \circ F)(f' \circ f) = G\big(F(f' \circ f)\big) = G\big(F(f') \circ F(f)\big) = G(F(f')) \circ G(F(f)) = (G \circ F)(f') \circ (G \circ F)(f)$. The first and last equalities are the definition of $G \circ F$; the second holds because $F$ preserves composition; the third because $G$ preserves composition, applied to the composable pair $F(f), F(f')$ of $\mathcal{B}$.

    (3) $(G \circ F)(1_A) = G(F(1_A)) = G(1_{F(A)}) = 1_{G(F(A))} = 1_{(G \circ F)(A)}$, because $F$ preserves identities and then $G$ does. $\blacksquare$

    **What made it work.** This is the proof from 1A that a composite of homomorphisms is a homomorphism, one level up. "Maps that preserve structure are closed under composition" is always proved by applying the preservation property of the inner map, then of the outer map.

    Composition of functors is associative and the identity functors $1_{\mathcal{A}}$ act as identities, because on objects and on arrows a composite functor is a composite of functions, and composition of functions has these properties. So categories and functors are themselves the objects and arrows of a category.

    > **Definition ($\mathbf{Cat}$).** $\mathbf{Cat}$ is the category whose objects are the **small** categories (those whose objects form a set, and whose hom-sets are sets) and whose arrows are functors, with composition and identities as above.

    The word "small" is there to avoid paradoxes of the "set of all sets" kind; 3A explains the issue. By Proposition 3.1 and exercise P01, monoids with their homomorphisms and posets with their order-preserving maps both sit inside $\mathbf{Cat}$.

    **Examples of composites.**

    - Composing the free monoid functor $W \colon \mathbf{Set} \to \mathbf{Mon}$ with the forgetful functor $U \colon \mathbf{Mon} \to \mathbf{Set}$ gives a functor $U \circ W \colon \mathbf{Set} \to \mathbf{Set}$ sending a set to the set of words in it.
    - Composing a contravariant functor with a contravariant functor gives a covariant one, since reversing twice restores the direction: the "double dual" $V \mapsto V^{**}$ is a covariant functor $\mathbf{Vect}_k \to \mathbf{Vect}_k$.

    **Non-example.** For $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B}' \to \mathcal{C}$ with $\mathcal{B}' \neq \mathcal{B}$, there is no composite $G \circ F$. Functors compose under the same condition as arrows in any category: the codomain of the first must be the domain of the second.

    > Reference: [Leinster §1.2](https://arxiv.org/abs/1612.09375); [Riehl §1.3](https://math.jhu.edu/~eriehl/context.pdf).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 9. Every Functor Between Two Small Categories

    Between finite categories there are finitely many candidate assignments, so all functors can be found by trying every assignment of objects and arrows and keeping those that satisfy the three items of Section 1. Choose a source and a target. The table lists every functor, with where it sends each object and each non-identity arrow, and whether it is faithful, full and essentially surjective on objects.

    Predictions to test:

    - From **1** to $\mathcal{B}$: one functor per object of $\mathcal{B}$. From **2** to $\mathcal{B}$: one per arrow of $\mathcal{B}$ (Proposition 4.1).
    - From the group $\mathbb{Z}/2$ to the group $\mathbb{Z}/3$: only the functor sending everything to the identity (Proposition 3.1: there is only one homomorphism).
    - From **3** to **3**: the order-preserving maps of a three-element chain.
    - Into "two isomorphic objects": a functor can be essentially surjective without hitting every object.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _names = [
        "1: one object, one arrow",
        "2: one arrow u: 0 -> 1",
        "3: the chain 0 -> 1 -> 2",
        "Parallel pair f, g: A -> B",
        "Two isomorphic objects",
        "Section and retraction (s, r, e)",
        "Group Z/2",
        "Group Z/3",
        "Monoid {e, a} with a.a = a",
    ]
    source_choice = mo.ui.dropdown(options=_names, value="2: one arrow u: 0 -> 1", label="Source category")
    target_choice = mo.ui.dropdown(options=_names, value="3: the chain 0 -> 1 -> 2", label="Target category")
    mo.hstack([source_choice, target_choice], justify="start")
    return source_choice, target_choice


@app.cell(hide_code=True)
def _(mo, source_choice, target_choice):
    def _run(source_name, target_name):
        import itertools

        def build(identities, others, composites):
            _arrows = {_one: (_obj, _obj) for _obj, _one in identities.items()}
            _arrows.update(others)
            _comp = dict(composites)
            for _f, (_dom, _cod) in _arrows.items():
                _comp[(_f, identities[_dom])] = _f
                _comp[(identities[_cod], _f)] = _f
            return {"objects": list(identities), "arrows": _arrows, "identity": dict(identities), "compose": _comp}

        _cats = {
            "1: one object, one arrow": build({"*": "id"}, {}, {}),
            "2: one arrow u: 0 -> 1": build({"0": "id0", "1": "id1"}, {"u": ("0", "1")}, {}),
            "3: the chain 0 -> 1 -> 2": build(
                {"0": "id0", "1": "id1", "2": "id2"},
                {"a": ("0", "1"), "b": ("1", "2"), "c": ("0", "2")},
                {("b", "a"): "c"},
            ),
            "Parallel pair f, g: A -> B": build({"A": "1A", "B": "1B"}, {"f": ("A", "B"), "g": ("A", "B")}, {}),
            "Two isomorphic objects": build(
                {"A": "1A", "B": "1B"}, {"f": ("A", "B"), "g": ("B", "A")},
                {("g", "f"): "1A", ("f", "g"): "1B"},
            ),
            "Section and retraction (s, r, e)": build(
                {"A": "1A", "B": "1B"}, {"s": ("A", "B"), "r": ("B", "A"), "e": ("B", "B")},
                {("r", "s"): "1A", ("s", "r"): "e", ("e", "e"): "e", ("e", "s"): "s", ("r", "e"): "r"},
            ),
            "Group Z/2": build({"*": "e"}, {"t": ("*", "*")}, {("t", "t"): "e"}),
            "Group Z/3": build(
                {"*": "e"}, {"w": ("*", "*"), "w2": ("*", "*")},
                {("w", "w"): "w2", ("w", "w2"): "e", ("w2", "w"): "e", ("w2", "w2"): "w"},
            ),
            "Monoid {e, a} with a.a = a": build({"*": "e"}, {"a": ("*", "*")}, {("a", "a"): "a"}),
        }
        _A, _B = _cats[source_name], _cats[target_name]
        _ar_A, _ar_B = _A["arrows"], _B["arrows"]

        def is_functor(obj_map, arr_map):
            for _obj in _A["objects"]:
                if arr_map[_A["identity"][_obj]] != _B["identity"][obj_map[_obj]]:
                    return False
            for (_g, _f), _h in _A["compose"].items():
                if _B["compose"][(arr_map[_g], arr_map[_f])] != arr_map[_h]:
                    return False
            return True

        def isomorphic_in_B(X, Y):
            for _f, (_dom, _cod) in _ar_B.items():
                if (_dom, _cod) != (X, Y):
                    continue
                for _g, _ends in _ar_B.items():
                    if _ends == (Y, X) and _B["compose"][(_g, _f)] == _B["identity"][X] and _B["compose"][(_f, _g)] == _B["identity"][Y]:
                        return True
            return False

        _found = []
        for _values in itertools.product(_B["objects"], repeat=len(_A["objects"])):
            _obj_map = dict(zip(_A["objects"], _values))
            _options = [
                [_b for _b, _ends in _ar_B.items() if _ends == (_obj_map[_dom], _obj_map[_cod])]
                for _f, (_dom, _cod) in _ar_A.items()
            ]
            for _choice in itertools.product(*_options):
                _arr_map = dict(zip(_ar_A, _choice))
                if is_functor(_obj_map, _arr_map):
                    _found.append((_obj_map, _arr_map))

        _non_id = [_f for _f in _ar_A if _f not in _A["identity"].values()]
        _rows = ["| # | on objects | on non-identity arrows | faithful | full | ess. surjective |", "|---|---|---|---|---|---|"]
        for _k, (_obj_map, _arr_map) in enumerate(_found[:24], start=1):
            _faithful = all(
                not (_f1 != _f2 and _ar_A[_f1] == _ar_A[_f2] and _arr_map[_f1] == _arr_map[_f2])
                for _f1 in _ar_A for _f2 in _ar_A
            )
            _full = all(
                {_arr_map[_f] for _f, _ends in _ar_A.items() if _ends == (_X, _Y)}
                == {_b for _b, _ends in _ar_B.items() if _ends == (_obj_map[_X], _obj_map[_Y])}
                for _X in _A["objects"] for _Y in _A["objects"]
            )
            _eso = all(any(isomorphic_in_B(_obj_map[_X], _Y) for _X in _A["objects"]) for _Y in _B["objects"])
            _on_obj = ", ".join("`" + _X + "` to `" + _obj_map[_X] + "`" for _X in _A["objects"])
            _on_arr = ", ".join("`" + _f + "` to `" + _arr_map[_f] + "`" for _f in _non_id) or "(none)"
            _rows.append(
                "| " + str(_k) + " | " + _on_obj + " | " + _on_arr + " | "
                + ("yes" if _faithful else "no") + " | " + ("yes" if _full else "no") + " | " + ("yes" if _eso else "no") + " |"
            )
        _head = (
            "**" + str(len(_found)) + " functor(s)** from *" + source_name + "* (" + str(len(_A["objects"])) + " object(s), "
            + str(len(_ar_A)) + " arrow(s)) to *" + target_name + "* (" + str(len(_B["objects"])) + " object(s), "
            + str(len(_ar_B)) + " arrow(s)).\n\n"
        )
        _tail = "\n\n(Showing the first 24.)" if len(_found) > 24 else ""
        return _head + "\n".join(_rows) + _tail

    _listing = _run(source_choice.value, target_choice.value)
    mo.md(_listing)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Defining a functor on objects only.** "The functor sending $G$ to $Z(G)$." *Diagnosis:* a functor is two assignments; until $F(f)$ is specified there is nothing to check, and Proposition 1.1 shows that sometimes no specification works.
    2. **Not checking that $F(f)$ is an arrow of the target category.** Verifying $F(g \circ f) = F(g) \circ F(f)$ for the free monoid without showing $W(f)$ is a homomorphism. *Diagnosis:* item 1 of the checklist; the right-hand side is not even a composite in $\mathcal{B}$ until it is done.
    3. **Checking composition and forgetting identities.** *Diagnosis:* the two axioms are independent; the "send everything to $\varepsilon$" assignment in Section 2 preserves composition and fails identities.
    4. **Reading "faithful" as "injective on arrows" and "full" as "surjective on arrows".** *Diagnosis:* both are conditions on each hom-set separately; a faithful functor can identify arrows from different hom-sets, and a full functor can miss arrows between objects outside its image (Section 7).
    5. **Writing $F(g \circ f) = F(g) \circ F(f)$ for a contravariant functor.** *Diagnosis:* for $F \colon \mathcal{A}^{\mathrm{op}} \to \mathcal{B}$ the order reverses, $F(g \circ f) = F(f) \circ F(g)$; check by confirming that the composite on the right is defined.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why This Matters

    - **1D** defines natural transformations, which are maps between two functors with the same domain and codomain. Every example there starts from functors met here: the double dual, the power set, the free and forgetful functors.
    - **1E** uses the three properties of Section 7 together: a functor that is full, faithful and essentially surjective on objects is what it takes for two categories to be "the same for all practical purposes".
    - **Part 2** is about pairs of functors going in opposite directions, such as $W \colon \mathbf{Set} \to \mathbf{Mon}$ and $U \colon \mathbf{Mon} \to \mathbf{Set}$, and the precise sense in which $W$ is "free".
    - **Part 4** studies the functors that are isomorphic to some $H^A$ or $H_A$. The Yoneda lemma says that an object is determined by its hom-functor; Proposition 6.1 and exercise P04 are the first steps.
    - **5C** asks which functors preserve limits, sharpening the question of Section 4 about what functors do and do not preserve.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    A functor between finite categories is stored as `{"objects": {A: FA, ...}, "arrows": {f: Ff, ...}}`. Each exercise has a skeleton with the essential lines left as `# TODO`. The cells run as shipped. Fill in the `...`, uncomment the `print` checks, and compare with the expected values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Composing functors

    Write `compose_functors(G, F)`, returning the functor $G \circ F$ of Section 8, and `identity_functor(cat)`. The test uses $F \colon \mathbf{2} \to \mathcal{R}$ picking out the arrow $s$ of the section-and-retraction category $\mathcal{R}$ (Proposition 4.1), and a functor $G \colon \mathcal{R} \to \mathbb{Z}/2$ into the group $\mathbb{Z}/2 = \{e, t\}$ regarded as a one-object category.
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
        # F: 2 -> R picks out the arrow s: A -> B
        _F = {"objects": {"0": "A", "1": "B"}, "arrows": {"id0": "1A", "id1": "1B", "u": "s"}}
        # G: R -> Z/2 sends both objects to * and every arrow to the identity e
        _G = {"objects": {"A": "*", "B": "*"}, "arrows": {"1A": "e", "1B": "e", "s": "e", "r": "e", "e": "e"}}

        def compose_functors(G, F):
            # TODO: apply F, then G, on objects and on arrows
            return {"objects": ..., "arrows": ...}

        def identity_functor(cat):
            # TODO: every object and every arrow goes to itself
            return {"objects": ..., "arrows": ...}

        _GF = compose_functors(_G, _F)
        # print(_GF["objects"])                                   # expect {'0': '*', '1': '*'}
        # print(_GF["arrows"])                                    # expect {'id0': 'e', 'id1': 'e', 'u': 'e'}
        # print(compose_functors(_F, identity_functor(_two)) == _F)   # expect True

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: The hom-functor of a finite category

    Write `hom_functor(cat, A)`, returning the two parts of $H^A$ from Section 6: a dictionary `on_objects` with `on_objects[B]` the sorted list of arrows $A \to B$, and a dictionary `on_arrows` with `on_arrows[g]` the function $p \mapsto g \circ p$, stored as a dictionary `{p: g∘p}` over all $p \in H^A(\mathrm{dom}\, g)$.
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
        _z4 = {
            "objects": ["*"],
            "arrows": {str(_m): ("*", "*") for _m in range(4)},
            "identity": {"*": "1"},
            "compose": {(str(_g), str(_f)): str((_g * _f) % 4) for _g in range(4) for _f in range(4)},
        }

        def hom_functor(cat, A):
            # TODO: on_objects[B] = sorted names of the arrows A -> B
            on_objects = ...
            # TODO: on_arrows[g] = {p: g∘p for every p in on_objects[dom g]}
            on_arrows = ...
            return on_objects, on_arrows

        # _obj, _arr = hom_functor(_retract, "B")
        # print(_obj)                 # expect {'A': ['r'], 'B': ['1B', 'e']}
        # print(_arr["r"])            # expect {'1B': 'r', 'e': 'r'}
        # print(_arr["e"])            # expect {'1B': 'e', 'e': 'e'}
        # _obj, _arr = hom_functor(_z4, "*")
        # print(_arr["2"])            # expect {'0': '0', '1': '2', '2': '0', '3': '2'}   (left multiplication by 2)
        # print(_arr["3"])            # expect {'0': '0', '1': '3', '2': '2', '3': '1'}

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: From a map of posets to a functor

    Two posets are given in the encoding, with the arrow $x \to y$ named `"x->y"`. Write `functor_from_map(P, Q, phi)`: if the function `phi` on objects is order-preserving, return the functor it determines (what must each arrow `"x->y"` be sent to?); if not, return `None`. The test poset is the set of divisors of 12 under divisibility.
    """)
    return


@app.cell
def _():
    def _run():
        import math

        _divisors = [1, 2, 3, 4, 6, 12]
        _arrows = {f"{_a}->{_b}": (_a, _b) for _a in _divisors for _b in _divisors if _b % _a == 0}
        _D = {
            "objects": _divisors,
            "arrows": _arrows,
            "identity": {_a: f"{_a}->{_a}" for _a in _divisors},
            "compose": {
                (f"{_b}->{_c}", f"{_a}->{_b}"): f"{_a}->{_c}"
                for _a in _divisors for _b in _divisors for _c in _divisors
                if _b % _a == 0 and _c % _b == 0
            },
        }

        def functor_from_map(P, Q, phi):
            # TODO: return None if some arrow x->y of P has no arrow phi(x)->phi(y) in Q
            # TODO: otherwise send each object x to phi(x) and each arrow x->y to the arrow phi(x)->phi(y)
            return ...

        _F = functor_from_map(_D, _D, lambda _x: math.gcd(_x, 4))
        # print(_F["objects"])               # expect {1: 1, 2: 2, 3: 1, 4: 4, 6: 2, 12: 4}
        # print(_F["arrows"]["2->6"])        # expect 2->2
        # print(_F["arrows"]["3->12"])       # expect 1->4
        # print(functor_from_map(_D, _D, lambda _x: 12 // _x))   # expect None (this map reverses the order)

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
    | P01 | Functors between posets are order-preserving maps — `exercises/1c/p01_functors_between_posets.md` | warm-up | unpacking a definition; verifying functoriality |
    | P02 | Faithful and full for functors between monoids — `exercises/1c/p02_faithful_full_for_monoids.md` | warm-up | unpacking a definition |
    | P03 | Functors preserve isomorphisms — `exercises/1c/p03_functors_preserve_isomorphisms.md` | core | applying a functor to an equation; counterexample |
    | P04 | The contravariant hom-functor — `exercises/1c/p04_contravariant_hom_functor.md` | core | verifying functoriality |
    | P05 | Faithful functors reflect monics and epics — `exercises/1c/p05_faithful_functors_reflect_monics.md` | core | cancellation; using faithfulness |
    | P06 | Full and faithful functors reflect isomorphisms — `exercises/1c/p06_full_faithful_reflect_isomorphisms.md` | stretch | using fullness to produce an arrow, faithfulness to prove an equation |

    **Submitting a proof.** Write your proof in `proofs/1c/pNN_<slug>.md` (same filename as the brief), then ask Claude to review it. The review points at gaps and asks questions; it does not supply a model proof.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [1B: Isomorphisms, Duality & New Categories from Old](../1b_isomorphisms_duality/) &nbsp;|&nbsp; Next: [1D: Natural Transformations](../1d_natural_transformations/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
