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
    # 4A: Representable Functors

    > *"A category is a world of objects, all looking at one another."*
    > — Tom Leinster, *Basic Category Theory*, Chapter 4

    Fix an object $A$ of a category $\mathcal{A}$ and ask: *what does the rest of the category look like from where $A$ stands?* The answer is a list: for every object $B$, the set $\mathcal{A}(A, B)$ of arrows from $A$ to $B$. In 1C you saw that this list is not just a list. It is a functor $H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$. This module studies the functors that arise this way, and the functors that are isomorphic to one that arises this way. Those are the **representable** functors.

    The question this module answers is: **which set-valued functors are "really" hom-functors in disguise, and how do you prove that one is?** A surprising number of familiar constructions pass the test. "The underlying set of a group" is $\mathbf{Grp}(\mathbb{Z}, -)$. "The set of subsets of a set" is $\mathbf{Set}(-, 2)$. "Bilinear maps out of $U \times V$" is $\mathbf{Vect}_k(U \otimes V, -)$. In each case a construction that looked like it needed its own definition turns out to be "maps out of (or into) one particular object".

    By the end you will be able to **prove** that a given functor is representable by exhibiting a representation, which always comes down to the same two checks: each component is a bijection, and the family of components is natural in one variable. You will also be able to prove that a functor is *not* representable, and to prove that every set-valued functor with a left adjoint is representable. The next module, 4B, asks what the maps out of a representable functor are; the answer is the Yoneda lemma. Everything there rests on the definitions made here, so we take them slowly.

    Throughout, $\mathcal{A}$ is a **locally small** category (3A): each $\mathcal{A}(A, B)$ is a set. That is exactly what is needed for $\mathcal{A}(A, -)$ to take values in $\mathbf{Set}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The View from an Object: $H^A$

    Start with what you already have from 1C, restated so that every piece is in front of you.

    > **Definition (covariant hom-functor).** Let $\mathcal{A}$ be a locally small category and $A$ an object of $\mathcal{A}$. The functor
    > $$H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$$
    > is defined as follows.
    > - On objects: $H^A(B) = \mathcal{A}(A, B)$ for each object $B$ of $\mathcal{A}$.
    > - On arrows: for each arrow $g \colon B \to C$ of $\mathcal{A}$, the function $H^A(g) \colon \mathcal{A}(A, B) \to \mathcal{A}(A, C)$ sends $p$ to $g \circ p$.

    **Reading the definition.**
    - The object $A$ is fixed once and for all; the variable is the *codomain*.
    - An element of $H^A(B)$ is an arrow $p \colon A \to B$ of $\mathcal{A}$. It is an arrow, not a function, unless $\mathcal{A}$ happens to be a category of sets with structure.
    - $H^A(g)$ is "compose with $g$ afterwards". Check the types: $p \colon A \to B$ and $g \colon B \to C$ give $g \circ p \colon A \to C$, which does lie in $H^A(C)$.
    - The functor axioms were verified in 1C: $H^A(1_B)(p) = 1_B \circ p = p$ by the identity axiom, and $H^A(h \circ g)(p) = (h \circ g) \circ p = h \circ (g \circ p) = H^A(h)\big(H^A(g)(p)\big)$ by associativity.

    **Example (sets).** Take $\mathcal{A} = \mathbf{Set}$ and $A = 1 = \{\star\}$, a one-element set. Then $H^1(B) = \mathbf{Set}(1, B)$ is the set of functions $1 \to B$. There is one such function for each element of $B$.

    **Example (groups).** Take $\mathcal{A} = \mathbf{Grp}$ and $A = \mathbb{Z}$. Then $H^{\mathbb{Z}}(G)$ is the set of group homomorphisms $\mathbb{Z} \to G$, and for a homomorphism $\theta \colon G \to G'$ the function $H^{\mathbb{Z}}(\theta)$ sends $\varphi$ to $\theta \circ \varphi$.

    **Example (a poset).** Let $P$ be a poset regarded as a category: there is exactly one arrow $a \to b$ when $a \le b$ and none otherwise. Then $H^a(b)$ is a one-element set if $a \le b$ and is empty if not. So $H^a$ records the *up-set* of $a$: all the elements above it.

    **Example (a monoid).** Let $M$ be a monoid regarded as a one-object category with object $\star$. Then $H^\star(\star) = M$ as a set, and $H^\star(m)$ is the function $p \mapsto m p$: left multiplication by $m$.

    **Non-example.** For a fixed $B$, the assignment $A \mapsto \mathcal{A}(A, B)$ is *not* a covariant functor on $\mathcal{A}$. An arrow $f \colon A' \to A$ and an arrow $p \colon A \to B$ compose to $p \circ f \colon A' \to B$, so $f$ induces a function $\mathcal{A}(A, B) \to \mathcal{A}(A', B)$, in the direction opposite to $f$. That is a contravariant functor, and it gets its own name, $H_B$, in Section 4.

    The widget below computes $H^A$ (and, looking ahead, $H_A$) for a few small categories in the finite-category encoding. Read each row as a sentence: "the arrows from $A$ to $B$ are ...", "composing with $g$ sends ... to ...".

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) opens with this picture of objects viewing one another; hom-functors were first defined in Leinster §1.2. [Riehl §2.1](https://math.jhu.edu/~eriehl/context.pdf) introduces them as the functors represented by an object.
    """)
    return


@app.cell
def _(mo):
    def _presets():
        def _mk(objects, arrows, comp):
            _arr = {"1" + _o: (_o, _o) for _o in objects}
            _arr.update(arrows)
            _c = {}
            for _f, (_a, _b) in _arr.items():
                _c[(_f, "1" + _a)] = _f
                _c[("1" + _b, _f)] = _f
            _c.update(comp)
            return {"objects": list(objects), "arrows": _arr,
                    "identity": {_o: "1" + _o for _o in objects}, "compose": _c}

        def _from_poset(elements, leq):
            return {
                "objects": list(elements),
                "arrows": {f"{_x}<={_y}": (_x, _y) for _x in elements for _y in elements if leq(_x, _y)},
                "identity": {_x: f"{_x}<={_x}" for _x in elements},
                "compose": {(f"{_y}<={_z}", f"{_x}<={_y}"): f"{_x}<={_z}"
                            for _x in elements for _y in elements for _z in elements
                            if leq(_x, _y) and leq(_y, _z)},
            }

        def _from_monoid(elements, mul, e):
            return {"objects": ["*"], "arrows": {_m: ("*", "*") for _m in elements}, "identity": {"*": e},
                    "compose": {(_g, _f): mul(_g, _f) for _g in elements for _f in elements}}

        _cats = {
            "Parallel pair  s, t : V -> E": _mk(["V", "E"], {"s": ("V", "E"), "t": ("V", "E")}, {}),
            "Diamond poset  0 <= a, b <= 1": _from_poset(
                ["0", "a", "b", "1"], lambda _x, _y: _x == _y or _x == "0" or _y == "1"),
            "Chain  0 <= 1 <= 2": _from_poset(["0", "1", "2"], lambda _x, _y: _x <= _y),
            "Group Z/3 (one object *)": _from_monoid(
                ["0", "1", "2"], lambda _g, _f: str((int(_g) + int(_f)) % 3), "0"),
            "Monoid {e, a, b} with xy = x for x != e": _from_monoid(
                ["e", "a", "b"], lambda _x, _y: _y if _x == "e" else _x, "e"),
        }
        return {f"{_name}   |   A = {_o}": (_cat, _o) for _name, _cat in _cats.items() for _o in _cat["objects"]}

    hom_presets = _presets()
    hom_choice = mo.ui.dropdown(options=list(hom_presets), value=list(hom_presets)[1],
                                label="Category and object A")
    hom_variance = mo.ui.radio(
        options=["covariant  H^A = A(A, -)", "contravariant  H_A = A(-, A)"],
        value="covariant  H^A = A(A, -)", label="Which hom-functor?")
    mo.vstack([mo.md("**Hom-functor table for a finite category**"), hom_choice, hom_variance])
    return hom_choice, hom_presets, hom_variance


@app.cell(hide_code=True)
def _(hom_choice, hom_presets, hom_variance, mo):
    def _run():
        _cat, _A = hom_presets[hom_choice.value]
        _cov = hom_variance.value.startswith("covariant")
        _arr = _cat["arrows"]

        def _hom(_x, _y):
            return [_p for _p, _dc in _arr.items() if _dc == (_x, _y)]

        def _show(_items):
            return "{ " + ", ".join(f"`{_i}`" for _i in _items) + " }" if _items else "empty set"

        _name = "H^A" if _cov else "H_A"
        _lines = [f"**{_name} with A = `{_A}`**", "", f"| object B | {_name}(B) | size |", "|---|---|---|"]
        for _B in _cat["objects"]:
            _set = _hom(_A, _B) if _cov else _hom(_B, _A)
            _lines.append(f"| `{_B}` | {_show(_set)} | {len(_set)} |")
        _lines += ["", f"| arrow g | {_name}(g) goes from ... to ... | what it does |", "|---|---|---|"]
        for _g, (_d, _c) in _arr.items():
            if _cov:
                _src, _pairs = _hom(_A, _d), [(_p, _cat["compose"][(_g, _p)]) for _p in _hom(_A, _d)]
                _typ = f"H^A(`{_d}`) to H^A(`{_c}`),  p &#8614; g &#8728; p"
            else:
                _src, _pairs = _hom(_c, _A), [(_p, _cat["compose"][(_p, _g)]) for _p in _hom(_c, _A)]
                _typ = f"H_A(`{_c}`) to H_A(`{_d}`),  p &#8614; p &#8728; g"
            _what = ", ".join(f"`{_p}` &#8614; `{_q}`" for _p, _q in _pairs) if _src else "the empty function"
            _lines.append(f"| `{_g}` : `{_d}` &#8594; `{_c}` | {_typ} | {_what} |")
        _note = ("Covariant: an arrow g : B &#8594; C gives a function in the **same** direction."
                 if _cov else
                 "Contravariant: an arrow g : C &#8594; B gives a function in the **opposite** direction.")
        _lines += ["", _note]
        return mo.md("\n".join(_lines))

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try. In the diamond poset, compare $A = 0$ with $A = 1$ in the covariant table: the bottom element sees every object, the top sees only itself. Switch to the contravariant table and the two swap roles. In the group $\mathbb{Z}/3$, every $H^\star(g)$ is a permutation of the three arrows; in the monoid $\{e, a, b\}$ the covariant functions $H^\star(a)$ and $H^\star(b)$ are constant, while the contravariant ones are not. Variance is not a formality: $p \mapsto g \circ p$ and $p \mapsto p \circ g$ are different functions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Representable Functors

    Many functors $\mathcal{A} \to \mathbf{Set}$ are not written as $\mathcal{A}(A, -)$, yet carry the same information as one that is. "The same information" has a precise meaning for functors: naturally isomorphic (1D).

    > **Definition (representable functor).** Let $\mathcal{A}$ be a locally small category. A functor $X \colon \mathcal{A} \to \mathbf{Set}$ is **representable** if $X \cong H^A$ for some object $A$ of $\mathcal{A}$. A **representation** of $X$ is a choice of an object $A$ of $\mathcal{A}$ together with a natural isomorphism $\alpha \colon H^A \Rightarrow X$. We then say that $A$ **represents** $X$.

    **Reading the definition.** To prove that $X$ is representable you must supply, and check, all of the following.
    1. An object $A$ of $\mathcal{A}$.
    2. For **every** object $B$ of $\mathcal{A}$, a function $\alpha_B \colon \mathcal{A}(A, B) \to X(B)$.
    3. Each $\alpha_B$ is a bijection. (Recall from 1D that a natural transformation is a natural isomorphism exactly when every component is an isomorphism, and an isomorphism in $\mathbf{Set}$ is a bijection.)
    4. Naturality: for every arrow $g \colon B \to C$ of $\mathcal{A}$ and every $p \in \mathcal{A}(A, B)$,
       $$X(g)\big(\alpha_B(p)\big) = \alpha_C(g \circ p).$$

    Item 4 is the one that is forgotten most often. A family of bijections $\mathcal{A}(A, B) \cong X(B)$ chosen separately for each $B$, with no relation between them, is not a representation.

    ### First example, proved in full

    The simplest functor $\mathbf{Set} \to \mathbf{Set}$ is the identity functor $1_{\mathbf{Set}}$. It is representable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Proposition 2.1.** Let $1 = \{\star\}$ be a one-element set. Then $H^1 \cong 1_{\mathbf{Set}}$. That is, the identity functor on $\mathbf{Set}$ is represented by $1$.

    - **Goal.** Produce, for every set $B$, a function $\alpha_B \colon \mathbf{Set}(1, B) \to B$ such that (a) every $\alpha_B$ is a bijection and (b) for every function $g \colon B \to C$ and every $p \in \mathbf{Set}(1, B)$ we have $g(\alpha_B(p)) = \alpha_C(g \circ p)$.
    - **Given.** The definition of $H^1$ from Section 1: $H^1(B) = \mathbf{Set}(1, B)$ and $H^1(g)(p) = g \circ p$. The identity functor sends $B$ to $B$ and $g$ to $g$.
    - **Plan.** Direct proof. A function $1 \to B$ is determined by the one value it takes, so define $\alpha_B$ by evaluating at $\star$. Then check the two items of the goal separately.
    - **Proof.** For a set $B$ and a function $p \colon 1 \to B$, define $\alpha_B(p) = p(\star)$.

      *(a) Each $\alpha_B$ is a bijection.* We give an inverse. For $b \in B$ let $\beta_B(b) \colon 1 \to B$ be the function with $\beta_B(b)(\star) = b$. Then $\alpha_B(\beta_B(b)) = \beta_B(b)(\star) = b$ by the definitions of $\alpha_B$ and $\beta_B$. In the other direction, $\beta_B(\alpha_B(p))$ is the function $1 \to B$ sending $\star$ to $p(\star)$; it agrees with $p$ at the only element of $1$, so the two functions are equal. Hence $\beta_B$ is a two-sided inverse of $\alpha_B$.

      *(b) Naturality.* Let $g \colon B \to C$ be a function and $p \in \mathbf{Set}(1, B)$. Then
      $$\alpha_C(g \circ p) = (g \circ p)(\star) = g(p(\star)) = g(\alpha_B(p)),$$
      using the definition of $\alpha_C$, the definition of composition of functions, and the definition of $\alpha_B$.

      By (b), $\alpha$ is a natural transformation $H^1 \Rightarrow 1_{\mathbf{Set}}$; by (a) and the fact from 1D, it is a natural isomorphism. $\blacksquare$
    - **What made it work.** The representing object $1$ carries a distinguished thing, the element $\star$, and a map out of $1$ is completely determined by where that thing goes. Whenever you suspect $X \cong H^A$, look for the element of $X(A)$ that "generates everything". In 4B this turns into following the identity arrow $1_A$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### More examples

    **The underlying set of a group.** Let $U \colon \mathbf{Grp} \to \mathbf{Set}$ be the forgetful functor. For a group $G$ define
    $$\alpha_G \colon \mathbf{Grp}(\mathbb{Z}, G) \to U(G), \qquad \alpha_G(\varphi) = \varphi(1).$$
    A homomorphism $\varphi \colon \mathbb{Z} \to G$ satisfies $\varphi(n) = \varphi(1)^n$ for all $n \in \mathbb{Z}$, so it is determined by $\varphi(1)$; and for any $x \in G$ the function $n \mapsto x^n$ is a homomorphism $\mathbb{Z} \to G$ by the laws of exponents. So $\alpha_G$ is a bijection. Naturality is the same one-line computation as in Proposition 2.1: for a homomorphism $\theta \colon G \to G'$, $\alpha_{G'}(\theta \circ \varphi) = \theta(\varphi(1)) = U(\theta)(\alpha_G(\varphi))$. Hence $U \cong H^{\mathbb{Z}}$: *an element of a group is the same thing as a homomorphism out of $\mathbb{Z}$.* Section 6 explains why $\mathbb{Z}$, of all groups, appears here.

    **The underlying set of a space.** Let $U \colon \mathbf{Top} \to \mathbf{Set}$ be the forgetful functor and $1$ the one-point space. Every function from the one-point space to a space $S$ is continuous, so $\mathbf{Top}(1, S)$ is the set of all functions $1 \to U(S)$, and evaluating at the point gives $U \cong H^1$ by the argument of Proposition 2.1.

    **A representation is a choice.** In the group example, $\varphi \mapsto \varphi(-1)$ is also a natural bijection $\mathbf{Grp}(\mathbb{Z}, G) \to U(G)$; the same two checks go through with $-1$ in place of $1$. So the same object can represent the same functor in more than one way. Module 4C makes precise the sense in which this is the only freedom there is.

    **Non-example.** Let $G$ be a group with at least two elements, regarded as a one-object category with object $\star$. A functor $X \colon G \to \mathbf{Set}$ is a set $X(\star)$ with a left action of $G$ (1C). Let $X$ be the one-element set $\{\mathrm{pt}\}$ with the only possible action. The category has just one object, so the only candidate representing object is $\star$, and $H^\star(\star) = G(\star, \star)$ is the underlying set of $G$. A natural isomorphism $H^\star \Rightarrow X$ would have as its single component a bijection from a set with at least two elements to a set with one element. There is none, so $X$ is **not** representable.

    This is the standard way to prove non-representability: find a property that every $H^A$ has (here, "the value at $\star$ has $|G|$ elements") and show that $X$ lacks it. Proof brief P05 asks you to do this for functors on $\mathbf{Set}$.

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) gives the definition of representability and these forgetful-functor examples. [Riehl §2.1](https://math.jhu.edu/~eriehl/context.pdf) has a longer catalogue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Maps between Representables: $H^f$

    So far the object $A$ was fixed. Now let it vary. If $f \colon A' \to A$ is an arrow, how are the views from $A$ and from $A'$ related? Every arrow $p \colon A \to B$ out of $A$ can be turned into an arrow out of $A'$ by first travelling along $f$.

    > **Definition.** Let $f \colon A' \to A$ be an arrow of a locally small category $\mathcal{A}$. The natural transformation
    > $$H^f \colon H^A \Rightarrow H^{A'}$$
    > has, for each object $B$ of $\mathcal{A}$, the component
    > $$(H^f)_B \colon \mathcal{A}(A, B) \to \mathcal{A}(A', B), \qquad p \mapsto p \circ f.$$

    **Reading the definition.**
    - The direction reverses: $f$ goes from $A'$ to $A$, and $H^f$ goes from $H^A$ to $H^{A'}$.
    - Each component is "compose with $f$ beforehand". Check the types: $f \colon A' \to A$ and $p \colon A \to B$ give $p \circ f \colon A' \to B$.
    - The definition *claims* that these components form a natural transformation. A claim inside a definition is a proof obligation. We discharge it now.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        nodes={
            "TL": (0, 2, r"$\mathcal{A}(A, B)$"), "TR": (4, 2, r"$\mathcal{A}(A, C)$"),
            "BL": (0, 0, r"$\mathcal{A}(A', B)$"), "BR": (4, 0, r"$\mathcal{A}(A', C)$"),
            # invisible anchors keep the horizontal arrows clear of the wide labels
            "TLr": (0.6, 2, ""), "TRl": (3.4, 2, ""), "BLr": (0.6, 0, ""), "BRl": (3.4, 0, ""),
            "L": (-0.8, 1, r"$- \circ f$"), "R": (4.8, 1, r"$- \circ f$"),
        },
        arrows=[
            ("TLr", "TRl", r"$g \circ -$"),
            ("BLr", "BRl", r"$g \circ -$", {"side": -1}),
            ("TL", "BL", ""),
            ("TR", "BR", ""),
        ],
        figsize=(6.6, 3.6),
        title=r"Naturality of $H^f$ at $g : B \to C$: both routes send $p$ to $g \circ p \circ f$",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Proposition 3.1.** For every arrow $f \colon A' \to A$ of $\mathcal{A}$, the family $\big((H^f)_B\big)_{B \in \mathcal{A}}$ is a natural transformation $H^A \Rightarrow H^{A'}$.

    - **Goal.** For every arrow $g \colon B \to C$ of $\mathcal{A}$ and every $p \in \mathcal{A}(A, B)$: $\;H^{A'}(g)\big((H^f)_B(p)\big) = (H^f)_C\big(H^A(g)(p)\big)$. This says that the square above commutes.
    - **Given.** $H^A(g)(p) = g \circ p$ and $H^{A'}(g)(q) = g \circ q$ (Section 1); $(H^f)_B(p) = p \circ f$ (the definition just made); the axioms of a category.
    - **Plan.** Direct proof: two functions are equal when they agree on every element (0B). Take an arbitrary $p$ and compute both sides.
    - **Proof.** Let $g \colon B \to C$ and $p \in \mathcal{A}(A, B)$. Going down and then right,
      $$H^{A'}(g)\big((H^f)_B(p)\big) = H^{A'}(g)(p \circ f) = g \circ (p \circ f).$$
      Going right and then down,
      $$(H^f)_C\big(H^A(g)(p)\big) = (H^f)_C(g \circ p) = (g \circ p) \circ f.$$
      These are equal by associativity of composition in $\mathcal{A}$. $\blacksquare$
    - **What made it work.** Composing before and composing after do not interfere with each other. Whenever a naturality square is built from "$g \circ -$" on one pair of sides and "$- \circ f$" on the other, it commutes by associativity, and by nothing else.

    **$H^\bullet$ is a functor.** The assignment $A \mapsto H^A$, $f \mapsto H^f$ respects identities and composition, in the reversed order:
    - $(H^{1_A})_B(p) = p \circ 1_A = p$ by the identity axiom, so $H^{1_A} = 1_{H^A}$.
    - For $A'' \xrightarrow{f'} A' \xrightarrow{f} A$ and $p \in \mathcal{A}(A, B)$: $(H^{f \circ f'})_B(p) = p \circ (f \circ f') = (p \circ f) \circ f' = (H^{f'})_B\big((H^f)_B(p)\big)$ by associativity, so $H^{f \circ f'} = H^{f'} \circ H^f$.

    Two natural transformations are equal when all their components are equal, and two functions are equal when they agree on every element, so those two computations are complete proofs. Together they say that there is a functor
    $$H^\bullet \colon \mathcal{A}^{\mathrm{op}} \to [\mathcal{A}, \mathbf{Set}], \qquad A \mapsto H^A, \quad f \mapsto H^f.$$

    **Example (a poset).** If $a' \le a$ in a poset $P$, then $H^{a' \le a}$ is the natural transformation $H^a \Rightarrow H^{a'}$ whose component at $b$ sends the unique element of $H^a(b)$, when there is one, to the unique element of $H^{a'}(b)$. It exists because $a' \le a \le b$ forces $a' \le b$: the up-set of $a$ is contained in the up-set of $a'$. Smaller elements have bigger up-sets, which is the reversal of direction again.

    **Example (groups).** The homomorphism $f \colon \mathbb{Z} \to \mathbb{Z}$, $n \mapsto 2n$, induces $H^f \colon H^{\mathbb{Z}} \Rightarrow H^{\mathbb{Z}}$. Under the representation $H^{\mathbb{Z}} \cong U$ of Section 2, the component at $G$ becomes the function $U(G) \to U(G)$, $x \mapsto x^2$, because $(\varphi \circ f)(1) = \varphi(2) = \varphi(1)^2$. Squaring is not a homomorphism in general, yet it is natural in $G$.

    **Non-example.** The components of $H^f$ are functions between hom-sets. They are not arrows of $\mathcal{A}$, and $H^f$ is not "$f$ applied to something". In a poset, for instance, $f$ is not a function at all.

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) defines $H^f$ and the functor $H^\bullet$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Presheaves and the Contravariant $H_A$

    Everything so far looked *out* from $A$. Dually, you can ask which arrows come *in* to $A$. Because precomposition reverses direction (the non-example in Section 1), the resulting functor is contravariant. Functors of this kind are important enough to have a name.

    > **Definition (presheaf).** A **presheaf** on a category $\mathcal{A}$ is a functor $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$.

    **Reading the definition.** Unpacking what a functor out of $\mathcal{A}^{\mathrm{op}}$ is (1C), a presheaf $X$ consists of:
    - a set $X(A)$ for each object $A$ of $\mathcal{A}$;
    - a function $X(f) \colon X(B) \to X(A)$ for each arrow $f \colon A \to B$ of $\mathcal{A}$ (note the direction);
    - such that $X(1_A) = 1_{X(A)}$ for every object $A$, and $X(g \circ f) = X(f) \circ X(g)$ for every composable pair $A \xrightarrow{f} B \xrightarrow{g} C$ (note the order).

    > **Definition (contravariant hom-functor).** Let $\mathcal{A}$ be locally small and $A$ an object of $\mathcal{A}$. The presheaf
    > $$H_A = \mathcal{A}(-, A) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$$
    > sends an object $B$ to the set $\mathcal{A}(B, A)$, and an arrow $g \colon C \to B$ to the function
    > $$H_A(g) \colon \mathcal{A}(B, A) \to \mathcal{A}(C, A), \qquad p \mapsto p \circ g.$$

    > **Definition (representable presheaf).** A presheaf $X$ on $\mathcal{A}$ is **representable** if $X \cong H_A$ for some object $A$ of $\mathcal{A}$; a **representation** of $X$ is a choice of such an $A$ and a natural isomorphism $H_A \Rightarrow X$.

    **Reading the definitions.** $H_A$ is a presheaf: $H_A(1_B)(p) = p \circ 1_B = p$, and for $D \xrightarrow{h} C \xrightarrow{g} B$ we get $H_A(g \circ h)(p) = p \circ (g \circ h) = (p \circ g) \circ h = H_A(h)\big(H_A(g)(p)\big)$ by associativity. To prove that a presheaf $X$ is representable you need an object $A$, a bijection $\alpha_B \colon \mathcal{A}(B, A) \to X(B)$ for every $B$, and naturality: for every $g \colon C \to B$ and every $p \in \mathcal{A}(B, A)$,
    $$X(g)\big(\alpha_B(p)\big) = \alpha_C(p \circ g).$$

    Keep the two notations apart: the index is **up** in $H^A$ (covariant, maps *out of* $A$) and **down** in $H_A$ (contravariant, maps *into* $A$).

    ### Example: directed graphs are presheaves

    Let $\mathcal{G}$ be the category with two objects $V$ and $E$ and, besides the identities, exactly two arrows $s, t \colon V \to E$ (the first preset in the widget above). A presheaf $X$ on $\mathcal{G}$ consists of two sets $X(V)$ and $X(E)$ and two functions $X(s), X(t) \colon X(E) \to X(V)$. Call the elements of $X(V)$ *vertices*, the elements of $X(E)$ *edges*, and read $X(s)(e)$ and $X(t)(e)$ as the source and the target of the edge $e$. A presheaf on $\mathcal{G}$ is then exactly a directed graph (loops and parallel edges allowed). There are no composites to check, because no two non-identity arrows of $\mathcal{G}$ are composable.

    What are the two representable presheaves?
    - $H_V$: we have $H_V(V) = \{1_V\}$ and $H_V(E) = \mathcal{G}(E, V) = \varnothing$. This is the graph with **one vertex and no edges**.
    - $H_E$: we have $H_E(V) = \{s, t\}$ and $H_E(E) = \{1_E\}$, and the source of the edge $1_E$ is $H_E(s)(1_E) = 1_E \circ s = s$, its target is $1_E \circ t = t$. This is the graph with **two vertices and one edge between them**.

    So the representable presheaves on $\mathcal{G}$ are "the generic vertex" and "the generic edge". Keep this example in mind: 4B and 4C return to it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example: the power set, proved in full

    For a set $B$, let $\mathscr{P}(B)$ be the set of all subsets of $B$. For a function $g \colon C \to B$, let $\mathscr{P}(g) \colon \mathscr{P}(B) \to \mathscr{P}(C)$ send a subset $S \subseteq B$ to its preimage $g^{-1}(S) = \{c \in C : g(c) \in S\}$. Preimage along an identity function changes nothing, and $(g \circ h)^{-1}(S) = h^{-1}(g^{-1}(S))$, so $\mathscr{P}$ is a presheaf on $\mathbf{Set}$: the **contravariant power-set functor** $\mathscr{P} \colon \mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$.

    > **Proposition 4.1.** Let $2 = \{0, 1\}$. Then $H_2 \cong \mathscr{P}$. That is, the contravariant power-set functor is represented by the two-element set.

    - **Goal.** Produce, for every set $B$, a function $\alpha_B \colon \mathbf{Set}(B, 2) \to \mathscr{P}(B)$ such that (a) every $\alpha_B$ is a bijection and (b) for every function $g \colon C \to B$ and every $\chi \in \mathbf{Set}(B, 2)$ we have $\mathscr{P}(g)(\alpha_B(\chi)) = \alpha_C(\chi \circ g)$.
    - **Given.** $H_2(B) = \mathbf{Set}(B, 2)$ and $H_2(g)(\chi) = \chi \circ g$; $\mathscr{P}(g)(S) = g^{-1}(S)$; the correspondence between subsets and characteristic functions from 3A.
    - **Plan.** Direct proof. A function $\chi \colon B \to 2$ marks some elements of $B$ with $1$; send it to the set of marked elements. Check bijectivity by giving an inverse, then check naturality by showing two subsets of $C$ have the same elements.
    - **Proof.** For $\chi \colon B \to 2$ define $\alpha_B(\chi) = \chi^{-1}\{1\} = \{b \in B : \chi(b) = 1\}$.

      *(a) Each $\alpha_B$ is a bijection.* For $S \subseteq B$ let $\beta_B(S) \colon B \to 2$ be the characteristic function of $S$: it sends $b$ to $1$ if $b \in S$ and to $0$ if $b \notin S$. Then $\alpha_B(\beta_B(S)) = \{b : \beta_B(S)(b) = 1\} = S$ by the definition of $\beta_B(S)$. Conversely, $\beta_B(\alpha_B(\chi))$ sends $b$ to $1$ exactly when $b \in \alpha_B(\chi)$, that is, exactly when $\chi(b) = 1$; since the only other value available is $0$, it sends $b$ to $0$ exactly when $\chi(b) = 0$. So $\beta_B(\alpha_B(\chi))$ and $\chi$ agree at every $b \in B$ and are equal. Hence $\beta_B$ is a two-sided inverse of $\alpha_B$.

      *(b) Naturality.* Let $g \colon C \to B$ and $\chi \colon B \to 2$. For $c \in C$,
      $$c \in \mathscr{P}(g)(\alpha_B(\chi)) \iff g(c) \in \alpha_B(\chi) \iff \chi(g(c)) = 1 \iff (\chi \circ g)(c) = 1 \iff c \in \alpha_C(\chi \circ g),$$
      using in turn the definition of preimage, the definition of $\alpha_B$, the definition of composition, and the definition of $\alpha_C$. The two subsets of $C$ have the same elements, so they are equal.

      By (b), $\alpha$ is a natural transformation $H_2 \Rightarrow \mathscr{P}$, and by (a) each component is a bijection, so $\alpha$ is a natural isomorphism. $\blacksquare$
    - **What made it work.** The set $2$ contains a distinguished subset, $\{1\}$, and *every* subset of *every* set is the preimage of $\{1\}$ along exactly one function into $2$. Again there is one special element of $\mathscr{P}(2)$ from which everything else is obtained. Naturality came down to a single fact about preimages: $g^{-1}(\chi^{-1}\{1\}) = (\chi \circ g)^{-1}\{1\}$.
    """)
    return


@app.cell(hide_code=True)
def _(draw_diagram):
    draw_diagram(
        nodes={
            "TL": (0, 2, r"$\mathbf{Set}(B, 2)$"), "TR": (4, 2, r"$\mathscr{P}(B)$"),
            "BL": (0, 0, r"$\mathbf{Set}(C, 2)$"), "BR": (4, 0, r"$\mathscr{P}(C)$"),
            "TLr": (0.7, 2, ""), "TRl": (3.6, 2, ""), "BLr": (0.7, 0, ""), "BRl": (3.6, 0, ""),
            "L": (-0.8, 1, r"$- \circ g$"), "R": (4.7, 1, r"$g^{-1}$"),
        },
        arrows=[
            ("TLr", "TRl", r"$\alpha_B$"),
            ("BLr", "BRl", r"$\alpha_C$", {"side": -1}),
            ("TL", "BL", ""),
            ("TR", "BR", ""),
        ],
        figsize=(6.6, 3.6),
        title=r"Naturality of $\alpha$ at $g : C \to B$ (both vertical maps go against $g$)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A topological cousin.** For a topological space $S$, let $\mathscr{O}(S)$ be the set of open subsets of $S$. The preimage of an open set under a continuous map is open, so $\mathscr{O}$ is a presheaf on $\mathbf{Top}$. It too is representable, by a two-point space with a carefully chosen topology. Finding that topology and proving the claim is proof brief P06.

    **Non-example (the empty presheaf).** Let $\mathcal{A}$ be any category with at least one object, and let $X$ be the presheaf with $X(B) = \varnothing$ for every $B$ and every $X(g)$ the empty function. Then $X$ is not representable. Suppose $\alpha \colon H_A \Rightarrow X$ were a natural isomorphism for some object $A$. Its component $\alpha_A \colon \mathcal{A}(A, A) \to X(A) = \varnothing$ would be a function into the empty set from a set that contains $1_A$. No such function exists. The property used here is worth remembering: **$H_A(A)$ is never empty, because it contains $1_A$.**

    **Non-example (variance matters).** The *covariant* power-set functor $\mathbf{Set} \to \mathbf{Set}$, which sends a function $g \colon B \to C$ to the direct-image function $S \mapsto g(S)$, has the same values on objects as $\mathscr{P}$ but is a different functor on a different category. Proposition 4.1 says nothing about it. A representation is a statement about a functor, arrows included, and never just about its values on objects.

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) treats $H_A$, the power-set example and the open-set example; presheaves are defined in Leinster §1.2. [Riehl §2.1](https://math.jhu.edu/~eriehl/context.pdf) covers contravariant representables alongside covariant ones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The Yoneda Embedding $H_\bullet$

    Section 3 let the object vary in $H^A$. Do the same for $H_A$. This time an arrow $f \colon A \to B$ acts on arrows *into* $A$ by composing afterwards, so nothing reverses.

    > **Definition.** Let $f \colon A \to B$ be an arrow of a locally small category $\mathcal{A}$. The natural transformation $H_f \colon H_A \Rightarrow H_B$ has, for each object $C$ of $\mathcal{A}$, the component
    > $$(H_f)_C \colon \mathcal{A}(C, A) \to \mathcal{A}(C, B), \qquad p \mapsto f \circ p.$$
    >
    > **Definition (Yoneda embedding).** The **Yoneda embedding** of $\mathcal{A}$ is the functor
    > $$H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}], \qquad A \mapsto H_A, \quad f \mapsto H_f.$$

    **Reading the definitions.**
    - The first definition claims that the components $(H_f)_C$ are natural in $C$. That claim is proof brief **P01**; it is the mirror image of Proposition 3.1 and you should prove it before going further.
    - The second definition claims that $H_\bullet$ is a functor. Here is the check. For every $C$ and every $p \in \mathcal{A}(C, A)$: $(H_{1_A})_C(p) = 1_A \circ p = p$ by the identity axiom, so $H_{1_A} = 1_{H_A}$. For $A \xrightarrow{f} B \xrightarrow{g} D$: $(H_{g \circ f})_C(p) = (g \circ f) \circ p = g \circ (f \circ p) = (H_g)_C\big((H_f)_C(p)\big)$ by associativity, so $H_{g \circ f} = H_g \circ H_f$.
    - $H_\bullet$ is **covariant**: its domain is $\mathcal{A}$, not $\mathcal{A}^{\mathrm{op}}$. Each individual $H_A$ is contravariant, but the way $H_A$ depends on $A$ is covariant.
    - The word "embedding" is a promise that $\mathcal{A}$ sits inside $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ without loss of information. Nothing proved so far justifies that word. It is justified in 4C, using the Yoneda lemma of 4B.

    The four constructions, side by side:

    | Notation | What it is | Variance | Rule |
    |---|---|---|---|
    | $H^A$ | functor $\mathcal{A} \to \mathbf{Set}$ | covariant in the blank | $H^A(g)(p) = g \circ p$ |
    | $H_A$ | functor $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ | contravariant in the blank | $H_A(g)(p) = p \circ g$ |
    | $H^\bullet$ | functor $\mathcal{A}^{\mathrm{op}} \to [\mathcal{A}, \mathbf{Set}]$ | contravariant in $A$ | $(H^f)_B(p) = p \circ f$ |
    | $H_\bullet$ | functor $\mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ | covariant in $A$ | $(H_f)_C(p) = f \circ p$ |

    The first two rows and the last two rows are two ways of slicing one object: the functor
    $$\mathrm{Hom}_{\mathcal{A}} \colon \mathcal{A}^{\mathrm{op}} \times \mathcal{A} \to \mathbf{Set}, \qquad (A, B) \mapsto \mathcal{A}(A, B), \qquad (f, g) \mapsto g \circ - \circ f,$$
    which is contravariant in its first variable and covariant in its second. Fix the first variable and you get $H^A$; fix the second and you get $H_B$.

    **Example (graphs).** In the category $\mathcal{G}$ of Section 4, the arrows $s, t \colon V \to E$ give natural transformations $H_s, H_t \colon H_V \Rightarrow H_E$. On vertices, $(H_s)_V$ sends $1_V$ to $s \circ 1_V = s$ and $(H_t)_V$ sends $1_V$ to $t$. So $H_s$ and $H_t$ are the two ways of mapping the one-vertex graph into the one-edge graph: onto the source, and onto the target.

    **Example (a poset).** In a poset $P$, the presheaf $H_a$ is non-empty exactly on the elements $b \le a$, and if $a \le a'$ then $H_{a \le a'}$ maps $H_a$ into $H_{a'}$. The Yoneda embedding turns each element into the set of elements below it. Module 4C examines this in detail.

    **Non-example.** There is no functor "$\mathcal{A} \to [\mathcal{A}, \mathbf{Set}]$, $A \mapsto H^A$". Section 3 showed that $f \colon A' \to A$ induces a map from $H^A$ to $H^{A'}$, the wrong way round for a covariant functor on $\mathcal{A}$. Writing $H^\bullet \colon \mathcal{A} \to [\mathcal{A}, \mathbf{Set}]$ is a variance error.

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) defines the Yoneda embedding and $\mathrm{Hom}_{\mathcal{A}}$. [Riehl §2.2](https://math.jhu.edu/~eriehl/context.pdf) introduces both the covariant and contravariant embeddings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Adjunctions Give Representables

    Why was it $\mathbb{Z}$ that represented the forgetful functor on groups, and the one-point space for spaces? In both cases the representing object is the *free* object on one generator. That is not a coincidence. It is a theorem with a short proof, and the proof shows how much of Part 2 was already about representables.

    Recall the definition from 2A. An adjunction $F \dashv G$, with $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$, consists of a bijection
    $$\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B)), \qquad q \mapsto \bar{q},$$
    for each $A \in \mathcal{A}$ and $B \in \mathcal{B}$, natural in $A$ and in $B$. Naturality in $B$ is the statement that for every $q \colon F(A) \to B$ and every $g \colon B \to B'$,
    $$\overline{g \circ q} = G(g) \circ \bar{q}.$$

    > **Lemma 6.1.** Let $\mathcal{A}$ and $\mathcal{B}$ be locally small categories, let $F \dashv G$ be an adjunction with $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$, and let $A$ be an object of $\mathcal{A}$. Then the functor
    > $$\mathcal{A}(A, G(-)) \colon \mathcal{B} \to \mathbf{Set}$$
    > (the composite $\mathcal{B} \xrightarrow{G} \mathcal{A} \xrightarrow{H^A} \mathbf{Set}$) is representable, and is represented by $F(A)$.

    - **Goal.** Produce a natural isomorphism $\alpha \colon H^{F(A)} \Rightarrow H^A \circ G$. In components: for every object $B$ of $\mathcal{B}$ a bijection $\alpha_B \colon \mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$, such that for every arrow $g \colon B \to B'$ of $\mathcal{B}$ and every $q \in \mathcal{B}(F(A), B)$ we have $(H^A \circ G)(g)\big(\alpha_B(q)\big) = \alpha_{B'}(g \circ q)$.
    - **Given.** The adjunction $F \dashv G$: the bijections $q \mapsto \bar{q}$ and their naturality in $B$, displayed above. The definition of $H^A$, which gives $(H^A \circ G)(g)(p) = H^A(G(g))(p) = G(g) \circ p$.
    - **Plan.** Unpack both definitions and compare. The components we need are exactly the transposition maps, and the naturality we need is exactly naturality of the adjunction in $B$.
    - **Proof.** Define $\alpha_B(q) = \bar{q}$. Each $\alpha_B$ is a bijection because transposition is a bijection, by the definition of an adjunction. For naturality, let $g \colon B \to B'$ and $q \in \mathcal{B}(F(A), B)$. Then
      $$(H^A \circ G)(g)\big(\alpha_B(q)\big) = G(g) \circ \bar{q} = \overline{g \circ q} = \alpha_{B'}(g \circ q),$$
      where the first equality is the formula for $H^A \circ G$ on arrows, the second is naturality of the adjunction in $B$, and the third is the definition of $\alpha_{B'}$. So $\alpha$ is a natural transformation with bijective components, hence a natural isomorphism. $\blacksquare$
    - **What made it work.** Nothing was constructed. The definition of an adjunction, read with $A$ held fixed, *is* a representation of $\mathcal{A}(A, G(-))$. When two definitions unpack to the same list of conditions, the proof is the unpacking.

    > **Proposition 6.2.** Let $\mathcal{A}$ be a locally small category. Any functor $G \colon \mathcal{A} \to \mathbf{Set}$ that has a left adjoint is representable. Precisely: if $F \dashv G$ with $F \colon \mathbf{Set} \to \mathcal{A}$, then $G \cong H^{F(1)}$, where $1$ is a one-element set.

    - **Goal.** A natural isomorphism $H^{F(1)} \Rightarrow G$ of functors $\mathcal{A} \to \mathbf{Set}$.
    - **Given.** Proposition 2.1: a natural isomorphism $\varepsilon \colon H^1 \Rightarrow 1_{\mathbf{Set}}$ with $\varepsilon_S(p) = p(\star)$ (it was called $\alpha$ there). Lemma 6.1, applied with the roles of the two categories played by $\mathbf{Set}$ and $\mathcal{A}$ and with the object $1$ of $\mathbf{Set}$: a natural isomorphism $\alpha \colon H^{F(1)} \Rightarrow H^1 \circ G$.
    - **Plan.** Chain two natural isomorphisms: $H^{F(1)} \cong H^1 \circ G \cong G$. The first is Lemma 6.1; the second is Proposition 2.1 "evaluated at $G$".
    - **Proof.** For each object $A$ of $\mathcal{A}$ put $\gamma_A = \varepsilon_{G(A)} \colon \mathbf{Set}(1, G(A)) \to G(A)$. Each $\gamma_A$ is a bijection because each component of $\varepsilon$ is. The family $\gamma$ is natural in $A$: for $g \colon A \to A'$ in $\mathcal{A}$, the naturality square of $\gamma$ at $g$ is the naturality square of $\varepsilon$ at the function $G(g) \colon G(A) \to G(A')$, which commutes by Proposition 2.1. So $\gamma \colon H^1 \circ G \Rightarrow G$ is a natural isomorphism. The composite $\gamma \circ \alpha \colon H^{F(1)} \Rightarrow G$ is a composite of natural isomorphisms, hence a natural isomorphism (1D). $\blacksquare$
    - **What made it work.** "An element of the set $G(A)$" was rewritten as "a function $1 \to G(A)$", which is something an adjunction can act on. Converting elements into arrows out of $1$ is the standard first move when a $\mathbf{Set}$-valued functor meets an adjunction.

    **Examples.** Tracing through the proof, the isomorphism $\mathcal{A}(F(1), A) \to G(A)$ sends $q$ to $\bar{q}(\star)$.
    - $U \colon \mathbf{Grp} \to \mathbf{Set}$ has the free-group functor as left adjoint (2A), and the free group on one generator is $\mathbb{Z}$ up to isomorphism. This recovers $U \cong \mathbf{Grp}(\mathbb{Z}, -)$.
    - $U \colon \mathbf{Top} \to \mathbf{Set}$ has the discrete-space functor $D$ as left adjoint (2A), and $D(1)$ is the one-point space. This recovers $U \cong \mathbf{Top}(1, -)$.
    - $U \colon \mathbf{Mon} \to \mathbf{Set}$ has the free-monoid functor as left adjoint, and the free monoid on one generator is $(\mathbb{N}, +, 0)$ up to isomorphism. So $U \cong \mathbf{Mon}(\mathbb{N}, -)$: an element of a monoid is a monoid homomorphism out of $\mathbb{N}$.

    (In the first and third examples we replaced $F(1)$ by an isomorphic object. That is harmless: if $j \colon A' \to A$ is an isomorphism then $H^j \colon H^A \Rightarrow H^{A'}$ is a natural isomorphism, because the functor $H^\bullet$ of Section 3, like every functor, preserves isomorphisms.)

    **Non-example.** The proposition gives a necessary condition for having a left adjoint. The one-element $G$-set of Section 2 is a functor to $\mathbf{Set}$ that is not representable, so by Proposition 6.2 it has no left adjoint. The proposition does **not** say that every representable functor has a left adjoint.

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) proves both results. [Riehl §4.1](https://math.jhu.edu/~eriehl/context.pdf) rephrases adjunctions in terms of representability.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Representability as a Definition: The Tensor Product

    So far the functor came first and the representing object was something already familiar. The idea can be run in reverse: *define* a new object by saying which functor it represents.

    Fix a field $k$ and vector spaces $U$ and $V$ over $k$. For a vector space $W$, a function $\beta \colon U \times V \to W$ is **bilinear** if it is linear in each variable when the other is held fixed: $\beta(u + u', v) = \beta(u, v) + \beta(u', v)$, $\beta(\lambda u, v) = \lambda \beta(u, v)$, and likewise in $v$. Write $\mathrm{Bilin}(U, V; W)$ for the set of bilinear functions $U \times V \to W$.

    If $\beta \colon U \times V \to W$ is bilinear and $g \colon W \to W'$ is linear, then $g \circ \beta$ is bilinear: for instance $g(\beta(u + u', v)) = g(\beta(u, v) + \beta(u', v)) = g(\beta(u, v)) + g(\beta(u', v))$, first because $\beta$ is bilinear and then because $g$ is linear, and the other three conditions are checked the same way. Composition with identities and composites behaves as it does for hom-functors. So there is a functor
    $$\mathrm{Bilin}(U, V; -) \colon \mathbf{Vect}_k \to \mathbf{Set}, \qquad W \mapsto \mathrm{Bilin}(U, V; W), \qquad g \mapsto g \circ -.$$

    > **Definition (tensor product, by what it represents).** A **tensor product** of $U$ and $V$ is a representation of the functor $\mathrm{Bilin}(U, V; -)$: a vector space $U \otimes V$ together with a natural isomorphism
    > $$\mathbf{Vect}_k(U \otimes V, W) \cong \mathrm{Bilin}(U, V; W) \qquad \text{natural in } W.$$

    **Reading the definition.**
    - It asks for a vector space $T = U \otimes V$ and, for every $W$, a bijection between linear maps $T \to W$ and bilinear maps $U \times V \to W$.
    - Naturality in $W$ says: if the linear map $q \colon T \to W$ corresponds to the bilinear map $\beta$, then for every linear $g \colon W \to W'$ the linear map $g \circ q$ corresponds to $g \circ \beta$.
    - The definition does not say that a tensor product exists. That is a theorem of linear algebra (one builds $U \otimes V$ as a quotient of a large free vector space), and we take it as known rather than prove it here.
    - The definition says "a" tensor product. In what sense is it "the" tensor product? You would hope that any two representing objects are isomorphic. They are, and the proof is one of the main results of 4C.

    **Example.** For $U = k^m$ and $V = k^n$, the space $k^{mn}$ of $m \times n$ matrices, with the bilinear map $(u, v) \mapsto u v^{\mathsf{T}}$, is a tensor product. A bilinear map out of $k^m \times k^n$ is determined by its values on the pairs of standard basis vectors $(e_i, e_j)$, and those values can be chosen freely; the same is true of a linear map out of the matrices and its values on the matrix units $e_i e_j^{\mathsf{T}}$.

    **Non-example.** The product vector space $U \times V$ does not represent $\mathrm{Bilin}(U, V; -)$ in general. Take $U = V = W = k$. A linear map $k \times k \to k$ has the form $(u, v) \mapsto au + bv$, so $\mathbf{Vect}_k(k \times k, k)$ is a two-dimensional space of maps, while a bilinear map $k \times k \to k$ has the form $(u, v) \mapsto c\,uv$. When $k$ is a finite field with $q$ elements there are $q^2$ of the former and $q$ of the latter, so no bijection exists. Bilinear is not the same as linear on the product; that is why a new object is needed.

    This pattern, an object defined by "maps out of it are the same as [some other kind of data]", is a **universal property**. Products, quotients, free objects and limits are all defined this way in Part 5 and Part 6. Representability is the precise form of the statement.

    > [Leinster §4.1](https://arxiv.org/abs/1612.09375) presents the tensor product as a representing object. [Riehl §2.3](https://math.jhu.edu/~eriehl/context.pdf) develops the same example under the heading of universal properties.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common Proof Mistakes

    1. **Giving bijections and stopping.** "For each $B$ the sets $\mathcal{A}(A, B)$ and $X(B)$ have the same number of elements, so $X \cong H^A$." *Diagnosis:* a representation is a **natural** isomorphism. You must name one specific bijection for each $B$ and verify the naturality equation for every arrow $g$.
    2. **Checking naturality only on objects.** Writing "$\alpha_B$ is defined the same way for every $B$, so it is natural". *Diagnosis:* naturality is an equation involving an arrow $g \colon B \to C$; "defined by the same formula" is a feeling, the equation $X(g)(\alpha_B(p)) = \alpha_C(g \circ p)$ is the proof.
    3. **Composing on the wrong side.** Using $p \mapsto g \circ p$ for $H_A(g)$, or $p \mapsto p \circ f$ for $H_f$. *Diagnosis:* write the domains and codomains of $p$ and $g$ before composing. Only one order type-checks, and it tells you the variance.
    4. **Treating arrows as functions.** Writing "$p(a)$" for an arrow $p$ of an arbitrary category. *Diagnosis:* in a poset or a monoid, arrows have no elements to act on. Only elements of the *sets* $\mathcal{A}(A, B)$ and $X(B)$ may be picked, and those elements are arrows.
    5. **Proving non-representability by one failed attempt.** "The map I tried is not a bijection, so $X$ is not representable." *Diagnosis:* "not representable" means *no* object and *no* natural isomorphism works. You need a property shared by every $H^A$ that $X$ fails to have.

    ## Why This Matters

    - **4B (the Yoneda lemma)** answers the question "what are the natural transformations out of $H_A$?". It needs the presheaf $H_A$, the transformations $H_f$, and the habit of looking for the special element, all from this module.
    - **4C** proves that the Yoneda embedding $H_\bullet$ of Section 5 is full and faithful, and that representing objects are unique up to isomorphism, which settles the "a tensor product versus the tensor product" question of Section 7.
    - **5A and 6A** define limits by a universal property and then show that a limit of a diagram is exactly a representation of a certain presheaf of cones. The statement "representables preserve limits" is proved there.
    - **6C** uses the strategy of the non-example in Section 6: to show a functor has no left adjoint, show that it fails a property that every functor with a left adjoint has. The property used there is preservation of limits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Compute It: Finite-Category Exercises

    Finite categories use the shared encoding. A **presheaf** $X$ on a finite category `cat` is stored as

    ```python
    X = {
        "objects": {A: [elements of X(A)], ...},
        "arrows":  {f: {x: X(f)(x), ...}, ...},   # for f : A -> B, a dict from X(B) to X(A)
    }
    ```

    so `X["arrows"][f]` goes *against* the direction of `f`. Each exercise below is a skeleton: the scaffolding runs as shipped, the essential lines are left as `# TODO`, and the commented `print` lines carry the values you should get.

    ### Exercise 1: Is it a presheaf?

    Complete `is_presheaf(cat, X)`. Part (i), that each `X["arrows"][f]` is a function from $X(\text{cod } f)$ to $X(\text{dom } f)$, is done. You add (ii) identities go to identity functions, and (iii) $X(g \circ f) = X(f) \circ X(g)$ for every composable pair. Mind the order in (iii).
    """)
    return


@app.cell
def _():
    def _run():
        def is_presheaf(cat, X):
            # (i) each X(f) is a function X(cod f) -> X(dom f)        [done]
            for _f, (_dom, _cod) in cat["arrows"].items():
                _fn = X["arrows"][_f]
                if set(_fn) != set(X["objects"][_cod]) or not set(_fn.values()) <= set(X["objects"][_dom]):
                    return False
            # TODO (ii): for every object A, X(1_A) is the identity function on X(A)
            ok_identities = ...
            # TODO (iii): for every (g, f) in cat["compose"], X(g o f) == X(f) o X(g) as functions
            ok_composition = ...
            return ok_identities, ok_composition  # TODO: return a single bool

        # The category  s, t : V -> E  and the chain  0 <= 1 <= 2.
        graph_cat = {
            "objects": ["V", "E"],
            "arrows": {"1V": ("V", "V"), "1E": ("E", "E"), "s": ("V", "E"), "t": ("V", "E")},
            "identity": {"V": "1V", "E": "1E"},
            "compose": {("1V", "1V"): "1V", ("1E", "1E"): "1E", ("s", "1V"): "s", ("1E", "s"): "s",
                        ("t", "1V"): "t", ("1E", "t"): "t"},
        }
        _els = ["0", "1", "2"]
        chain = {
            "objects": _els,
            "arrows": {f"{_x}<={_y}": (_x, _y) for _x in _els for _y in _els if _x <= _y},
            "identity": {_x: f"{_x}<={_x}" for _x in _els},
            "compose": {(f"{_y}<={_z}", f"{_x}<={_y}"): f"{_x}<={_z}"
                        for _x in _els for _y in _els for _z in _els if _x <= _y <= _z},
        }

        # A directed graph: three vertices, edges a: v1->v2, b: v2->v3, c: v1->v3.
        triangle = {
            "objects": {"V": ["v1", "v2", "v3"], "E": ["a", "b", "c"]},
            "arrows": {"1V": {"v1": "v1", "v2": "v2", "v3": "v3"}, "1E": {"a": "a", "b": "b", "c": "c"},
                       "s": {"a": "v1", "b": "v2", "c": "v1"}, "t": {"a": "v2", "b": "v3", "c": "v3"}},
        }
        # Restriction maps on the chain that do NOT compose correctly.
        broken = {
            "objects": {"0": ["z1", "z2"], "1": ["y1", "y2"], "2": ["x"]},
            "arrows": {"0<=0": {"z1": "z1", "z2": "z2"}, "1<=1": {"y1": "y1", "y2": "y2"}, "2<=2": {"x": "x"},
                       "0<=1": {"y1": "z1", "y2": "z2"}, "1<=2": {"x": "y1"}, "0<=2": {"x": "z2"}},
        }
        repaired = {"objects": broken["objects"], "arrows": dict(broken["arrows"])}
        repaired["arrows"]["0<=2"] = {"x": "z1"}
        twisted = {"objects": repaired["objects"], "arrows": dict(repaired["arrows"])}
        twisted["arrows"]["0<=0"] = {"z1": "z2", "z2": "z1"}

        # print(is_presheaf(graph_cat, triangle))   # expect True
        # print(is_presheaf(chain, broken))         # expect False  (composition fails)
        # print(is_presheaf(chain, repaired))       # expect True
        # print(is_presheaf(chain, twisted))        # expect False  (an identity is not sent to an identity)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Which objects represent this presheaf?

    Given `hom_presheaf(cat, A)` (the presheaf $H_A$) and `nat_transformations(cat, X, Y)` (every natural transformation $X \Rightarrow Y$, found by brute force), complete `representing_objects(cat, X)`: the list of objects $A$ for which some natural transformation $H_A \Rightarrow X$ is a natural isomorphism. Use the fact from 1D that this means every component is a bijection.
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

        def representing_objects(cat, X):
            _found = []
            for _A in cat["objects"]:
                _H = hom_presheaf(cat, _A)
                # TODO: decide whether some alpha in nat_transformations(cat, _H, X) has every
                #       component alpha[B] a bijection from _H["objects"][B] onto X["objects"][B];
                #       if so, append _A to _found
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

        triangle = graph(["v1", "v2", "v3"], {"a": ("v1", "v2"), "b": ("v2", "v3"), "c": ("v1", "v3")})
        one_edge = graph(["x", "y"], {"k": ("x", "y")})
        one_loop = graph(["x"], {"k": ("x", "x")})

        # The group Z/3 as a one-object category, and two right Z/3-sets.
        _z = ["0", "1", "2"]
        z3 = {"objects": ["*"], "arrows": {_m: ("*", "*") for _m in _z}, "identity": {"*": "0"},
              "compose": {(_g, _f): str((int(_g) + int(_f)) % 3) for _g in _z for _f in _z}}
        rotation = {"objects": {"*": ["r0", "r1", "r2"]},
                    "arrows": {_m: {f"r{_i}": f"r{(_i + int(_m)) % 3}" for _i in range(3)} for _m in _z}}
        one_point = {"objects": {"*": ["pt"]}, "arrows": {_m: {"pt": "pt"} for _m in _z}}

        # print(representing_objects(graph_cat, triangle))   # expect []
        # print(representing_objects(graph_cat, one_edge))   # expect ['E']
        # print(representing_objects(graph_cat, one_loop))   # expect []
        # print(representing_objects(z3, rotation))          # expect ['*']
        # print(representing_objects(z3, one_point))         # expect []   (compare the non-example of Section 2)

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Representing objects compute left adjoints (posets)

    In a poset $Q$, a functor $Q \to \mathbf{Set}$ taking only the values "one-element set" and "empty set" is a predicate `pred` on $Q$, and it is represented by $q$ exactly when `pred(b)` holds if and only if $q \le b$. Complete `representing_element`, returning such a $q$ or `None`.

    Then use it on Lemma 6.1. For an order-preserving map $g \colon Q \to P$ and $a \in P$, the functor $P(a, g(-))$ is the predicate $b \mapsto (a \le g(b))$. If $g$ has a left adjoint $f$, the lemma says this predicate is represented by $f(a)$. So you can compute $f$ one value at a time.
    """)
    return


@app.cell
def _():
    def _run():
        def representing_element(elements, leq, pred):
            # TODO: return an element q with  pred(b) == leq(q, b)  for every b in elements,
            #       or None if there is no such element
            _result = ...
            return _result

        # g : {0,1,2,3} -> {0,...,6},  g(b) = 2b,  both with the usual order.
        P = list(range(7))
        Q = list(range(4))

        def g(b):
            return 2 * b

        def usual(x, y):
            return x <= y

        # TODO: left_adjoint[a] = the element of Q representing the predicate  b |-> (a <= g(b))
        left_adjoint = {_a: ... for _a in P}

        # print([left_adjoint[_a] for _a in P])   # expect [0, 1, 1, 2, 2, 3, 3]

        # Divisors of 12 ordered by divisibility.
        divisors = [1, 2, 3, 4, 6, 12]

        def divides(x, y):
            return y % x == 0

        # print(representing_element(divisors, divides, lambda b: b % 2 == 0 and b % 3 == 0))   # expect 6
        # print(representing_element(divisors, divides, lambda b: b % 4 == 0 or b % 6 == 0))    # expect None

    _run()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Prove It: Proof Exercises

    | # | Brief | Type | Technique |
    |---|-------|------|-----------|
    | P01 | $H_f$ is a natural transformation: `exercises/4a/p01_hf_is_natural.md` | warm-up | dualizing a proof from the lecture |
    | P02 | Representable presheaves on a poset: `exercises/4a/p02_representables_on_a_poset.md` | warm-up | unpacking a definition |
    | P03 | Elements of order dividing $n$: `exercises/4a/p03_torsion_elements_representable.md` | core | exhibiting a representation |
    | P04 | The arrows of a category: `exercises/4a/p04_arrows_functor_representable.md` | core | exhibiting a representation |
    | P05 | A test for non-representability: `exercises/4a/p05_non_representable_functors.md` | core | proving a negative with an invariant |
    | P06 | Open sets and the Sierpinski space: `exercises/4a/p06_open_sets_sierpinski.md` | stretch | exhibiting a representation, naturality in one variable |

    **Submitting a proof.** Write your proof in `proofs/4a/pNN_<slug>.md` (the exact filename is at the bottom of each brief), then ask Claude to review it.
    The review points at gaps and asks questions; it does not hand you a model proof. Open the hints in a brief one at a time, and only after a real attempt.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    [&#8593; Course home](../) &nbsp;|&nbsp; &#8592; Prev: [3A: Sets & Size](../3a_sets_and_size/) &nbsp;|&nbsp; Next: [4B: The Yoneda Lemma](../4b_yoneda_lemma/) &#8594;
    """)
    return


if __name__ == "__main__":
    app.run()
