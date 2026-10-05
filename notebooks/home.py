import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Category Theory — A Proof-Centred Course

    A self-paced, pure-mathematics course that follows Tom Leinster's *Basic Category Theory* from the definition of a category to the adjoint functor theorems, with examples drawn from sets, monoids, groups, posets, vector spaces and topological spaces.
    Proof-writing is the centre of the course: every lecture proves its theorems step by step as models to imitate, and every module ends with proofs for you to write yourself.

    ---

    ## How to Use This Course

    - **Follow the modules in order.** The course is essentially linear, as Leinster's book is; the dependency graph below shows the two places where you have a choice.
    - **Read the lecture proofs as models.** Every proof in a lecture has the same five labelled steps — *Goal, Given, Plan, Proof, What made it work* — so that you can copy the shape before you can produce the content. Read each one with a pencil: cover the *Proof* step and try to predict it from the *Plan*.
    - **Do the "Compute It" exercises in the notebook.** Each module ends with two or three skeleton cells about finite categories. Fill in the `# TODO` lines and uncomment the checks; every claim about a small category can be tested by brute force.
    - **Write the "Prove It" proofs in `proofs/<module>/`.** Each module has six proof briefs in `exercises/<module>/` (two warm-ups, three core, one stretch) with hints that are revealed one at a time. Write your proof in `proofs/<module>/pNN_<slug>.md`, using the same filename as the brief.
    - **Ask Claude to review your proof** (for example: "review proofs/1a/p03_identities_unique.md"). Review points at gaps and asks questions. It never hands over a proof, and there are no solutions anywhere in this repository: the proofs are yours to write.
    - **Use the interactive widgets.** Each module has one: a validator, a checker or a calculator for finite examples. They are there so that you can test a definition against cases before you try to prove something about it.

    > **Prerequisite:** you are comfortable with sets and functions, and you have met groups and vector spaces before.
    > You do **not** need to be fluent at writing proofs: Part 0 rebuilds proof technique from the ground up (reading a definition, proving "for all" and "there exists", uniqueness arguments, diagram chasing) and refreshes the algebra the examples rely on.

    To open a module, run `pwsh ./launch.ps1 1a` (Windows) or `bash launch.sh 1a` (macOS / Linux) from the repository root; this opens Module 1A.
    With no argument, the same scripts open this page.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 0 — Orientation & Proof Toolkit

    > *Before any category theory: how to read a definition, how to structure a proof, and the three proof shapes this subject uses over and over.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 0A | [Orientation](/category-theory-course/0a_orientation/) | What category theory is, the "bird's-eye view", a first universal property (the one-element set, the product of two sets), how to use this course, how proof review works | "Guess the object from its maps" teaser |
    | 0B | [Proof Toolkit I: Definitions & Direct Proof](/category-theory-course/0b_proof_toolkit_definitions/) | Reading a definition as a checklist; quantifier order; proving "for all" and "there exists"; proving two functions equal; injective / surjective / bijective; composition; left and right inverses | Function-composition explorer on finite sets (injective? surjective? has a left inverse?) |
    | 0C | [Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher](/category-theory-course/0c_proof_toolkit_uniqueness/) | Existence-and-uniqueness proofs; "unique up to unique isomorphism"; commutative diagrams and diagram chasing; refresher on monoids, groups, homomorphisms, posets, vector spaces, continuous maps | Does-this-diagram-commute checker on finite sets |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — Categories, Functors, Natural Transformations

    > *Leinster Chapter 1. The three layers of the language: things, maps between things, and maps between those.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 1A | [Categories](/category-theory-course/1a_categories/) | Definition; the axioms as proof obligations; Set, Grp, Vect, Top; a monoid as a one-object category; a poset as a category; discrete categories; hom-sets | Finite-category validator (enter a composition table, see which axiom fails) |
    | 1B | [Isomorphisms, Duality & New Categories from Old](/category-theory-course/1b_isomorphisms_duality/) | Isomorphisms and uniqueness of inverses; monomorphisms and epimorphisms; the opposite category and the principle of duality; product categories; groupoids | Mono / epi / iso classifier for arrows of a finite category |
    | 1C | [Functors](/category-theory-course/1c_functors/) | Definition; forgetful and free functors; functors between monoids and between posets; contravariant functors; hom-functors $\mathcal{A}(A,-)$ and $\mathcal{A}(-,A)$; faithful, full, essentially surjective; **Cat** | Enumerate every functor between two small finite categories |
    | 1D | [Natural Transformations](/category-theory-course/1d_natural_transformations/) | Definition and the naturality square; examples (determinant, double dual, list reversal on sets); vertical and horizontal composition; functor categories; natural isomorphism | Naturality-square checker for functors between finite categories |
    | 1E | [Equivalence of Categories](/category-theory-course/1e_equivalence/) | Isomorphism vs equivalence of categories; equivalence ⇔ full, faithful and essentially surjective; skeletons; examples (finite sets vs. natural numbers, FDVect vs. matrices); duality as equivalence with an opposite | Skeleton builder: collapse a finite category along its isomorphism classes |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — Adjoints

    > *Leinster Chapter 2. The single most important idea in the subject, seen three ways.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 2A | [Adjunctions: Definition & Examples](/category-theory-course/2a_adjunctions/) | Hom-set bijection and its naturality; transposes; free ⊣ forgetful (monoids, groups, vector spaces); discrete ⊣ forgetful ⊣ indiscrete for Top; initial and terminal objects as adjoints; Galois connections between posets; currying | Galois-connection explorer between two finite posets |
    | 2B | [Units & Counits](/category-theory-course/2b_units_counits/) | Unit and counit; the triangle identities; equivalence of the hom-set and unit–counit descriptions; closure operators from Galois connections | Triangle-identity checker for a finite adjunction |
    | 2C | [Adjunctions via Initial Objects](/category-theory-course/2c_universal_arrows/) | Comma categories; slice and coslice categories; universal arrows; the unit as an initial object of a comma category; uniqueness of adjoints | Comma-category builder for functors between finite categories |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3 — Interlude on Sets

    > *Leinster Chapter 3. What we have been assuming about sets, and why "the category of all sets" needs care.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 3A | [Sets & Size](/category-theory-course/3a_sets_and_size/) | Constructions with sets: products, sums, function sets, the two-element set and subsets, equalizers, quotients; small, locally small and large categories; essentially small; why **Set** is not small (Cantor / Russell) | Counting widget: $\lvert B^A \rvert$, $\lvert A \times B \rvert$, $\lvert A + B \rvert$ and the bijection $\mathbf{Set}(A \times B, C) \cong \mathbf{Set}(A, C^B)$ on finite sets |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4 — Representables & the Yoneda Lemma

    > *Leinster Chapter 4. An object is known by the maps into it.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 4A | [Representable Functors](/category-theory-course/4a_representables/) | $H^A$ and $H_A$; representable functors and representations; examples (forgetful functors, the power-set functor, bilinear maps and the tensor product); adjunctions give representables; presheaves | Hom-functor table for a finite category |
    | 4B | [The Yoneda Lemma](/category-theory-course/4b_yoneda_lemma/) | Statement; the proof, slowly: the two maps, why they are inverse, naturality in both variables; reading the lemma in a monoid (Cayley's theorem) and in a poset | Yoneda bijection made concrete: natural transformations $H_A \Rightarrow X$ vs. elements of $X(A)$ in a finite category |
    | 4C | [Consequences of Yoneda](/category-theory-course/4c_yoneda_consequences/) | Universal elements; the Yoneda embedding is full and faithful; $H_A \cong H_B \Rightarrow A \cong B$; representations are unique up to unique iso; isomorphism of objects from isomorphism of generalized elements | Yoneda embedding of a finite poset as down-sets |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5 — Limits

    > *Leinster Chapter 5. Products, equalizers and pullbacks are one idea.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 5A | [Limits](/category-theory-course/5a_limits/) | Products, equalizers, pullbacks; cones and the general definition; limits in Set by the explicit formula; all limits from products and equalizers; monics via pullbacks | Limit calculator for finite diagrams of finite sets |
    | 5B | [Colimits](/category-theory-course/5b_colimits/) | Sums, coequalizers, pushouts; cocones; colimits in Set; epics via pushouts; duality with 5A; examples in Grp, Top, posets (joins and meets) | Colimit calculator (quotient by generated equivalence relation) |
    | 5C | [Functors & Limits](/category-theory-course/5c_functors_and_limits/) | Preserve, reflect, create; forgetful functors and limits; limits in functor categories are computed pointwise (statement here, proof in 6B); limits commute with limits | Does this functor between finite categories preserve this product? |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 6 — Adjoints, Representables & Limits Together

    > *Leinster Chapter 6, then Riehl Chapter 5. The three big ideas turn out to be one.*

    | # | Module | Topics | Interactive Elements |
    |---|--------|--------|---------------------|
    | 6A | [Limits via Representables & Adjoints](/category-theory-course/6a_limits_representables_adjoints/) | A limit is a representation of the cone functor; limits as right adjoint to the diagonal functor; representables preserve limits | Cone-counting widget: cones on a diagram vs. maps into its limit |
    | 6B | [Limits & Colimits of Presheaves](/category-theory-course/6b_presheaf_limits/) | Pointwise limits in functor categories; the category of elements; every presheaf is a colimit of representables (the density theorem) | Category of elements of a presheaf on a finite category |
    | 6C | [Adjoints & Limits](/category-theory-course/6c_adjoints_and_limits/) | Right adjoints preserve limits; left adjoints preserve colimits; the general and special adjoint functor theorems (statements, the poset case proved in full); cartesian closed categories | Poset adjoint functor theorem: build the left adjoint of a meet-preserving map |
    | 6D | [Monads](/category-theory-course/6d_monads/) *(advanced)* | Monads from adjunctions; algebras; the Eilenberg–Moore and Kleisli categories; monadic functors (statement); closure operators as monads on posets | Closure operator ↔ Galois connection round-trip on a finite poset |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 7 — Reference

    | # | Module | Description |
    |---|--------|-------------|
    | 7A | [Definition & Theorem Study Guide](/category-theory-course/7a_study_guide/) | Every definition, theorem and proof technique in the course, by module, with the statement, the picture, and where it is used later |
    | | Flashcards | Markdown decks in `flashcards/`, one per Part |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Dependency Graph

    ```
    0A → 0B → 0C → 1A → 1B → 1C → 1D → 1E
                                    │
                                    ├→ 2A → 2B → 2C
                                    │         │
                                    └→ 3A ────┤
                                              ▼
                                    4A → 4B → 4C → 5A → 5B → 5C → 6A → 6B → 6C → 6D

    all modules ───────────────────────────────────────────────────────────────→ 7A (Study Guide)
    ```

    The course is essentially linear, as Leinster's book is. Two choices are open to you:

    - **3A (Sets & Size)** can be read any time after 1E. It must be done before Part 4, where "locally small" becomes a hypothesis of nearly every theorem.
    - **6D (Monads)** needs 2B and 5A but not 6A–6C, so it can be taken early as a reward after Part 5.

    ---

    ## Study Tools

    | Tool | Where | What it is for |
    |------|-------|----------------|
    | Proof briefs | `exercises/<module>/pNN_<slug>.md` | Six per teaching module. Each has the statement, what you may use, what a complete proof must show, three or four hints revealed one at a time, and a self-check list. No solutions. |
    | Your proofs | `proofs/<module>/pNN_<slug>.md` | Where you write. The folder is gitignored, so the repository stays solution-free. Use the five-step proof anatomy from the lectures. |
    | Progress checklist | `PROGRESS.md` | One row per proof brief. A row is ticked when you have written the proof and it has been reviewed. |
    | Flashcards | `flashcards/` | One Markdown deck per Part: definitions, theorem statements, and "which technique proves this?". |
    | Study guide | [7A](/category-theory-course/7a_study_guide/) | Every definition and theorem in one place, filterable by Part, plus a catalogue of proof techniques and a table comparing the universal properties. |

    ---

    ## Textbooks

    The course is built from one book, Leinster's, and follows its chapter order: every module from 1A to 6C is one section of it. Riehl supplies extra examples and the whole of 6D. Hammack is the reference for Part 0. Perrone is a second gentle voice for anything that does not land the first time. Lectures cite these at section level.

    | Abbrev | Link | Title | Author | Role in this course | Access |
    |--------|------|-------|--------|---------------------|--------|
    | Leinster ⭐ | [arXiv:1612.09375](https://arxiv.org/abs/1612.09375) | Basic Category Theory | Tom Leinster | Primary text, Parts 1–6 | Free (CC BY-NC-SA) |
    | Riehl ⭐ | [author PDF](https://math.jhu.edu/~eriehl/context.pdf) | Category Theory in Context | Emily Riehl | Extra examples, monos and epis, diagram chasing, monads (6D) | Free (author) |
    | Hammack | [Book of Proof](https://www.people.vcu.edu/~rhammack/BookOfProof/) | Book of Proof (3e) | Richard Hammack | Proof technique, Part 0 | Free |
    | Perrone | [arXiv:1912.10642](https://arxiv.org/abs/1912.10642) | Notes on Category Theory with examples from basic mathematics | Paolo Perrone | Second gentle exposition | Free |
    | Awodey | [Oxford](https://global.oup.com/academic/product/category-theory-9780199237180) | Category Theory (2e) | Steve Awodey | Further reading | Paid / library |
    | Mac Lane | [Springer](https://link.springer.com/book/10.1007/978-1-4757-4721-8) | Categories for the Working Mathematician (2e) | Saunders Mac Lane | Further reading | Paid / library |
    """)
    return


if __name__ == "__main__":
    app.run()
