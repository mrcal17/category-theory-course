# Category Theory — Course Segmentation

The plan that drives notebook construction. Mirrors the structure and conventions of
`mrcal17/info-theory-course` (marimo reactive notebooks → WASM HTML, a syllabus `home.py`,
per-module exercises, a local `textbooks/` folder) and takes its exercise discipline from
`mrcal17/gpu-kernels-course` (solution-free briefs with layered hints).

**Owner decisions baked in:** (1) pure-math flavor — examples come from sets, monoids, groups,
posets, vector spaces and topological spaces, not from programming; (2) the course is built
from one textbook, Leinster's *Basic Category Theory*, and follows its chapter order; (3) the
learner has some abstract algebra but found proofs hard, so **proof-writing is the centre of the
course**: Part 0 is a proof toolkit, every lecture models its proofs step by step, and every
module ends in proof exercises with layered hints and no solutions; (4) marimo notebooks, as in
the earlier courses; (5) the whole course is authored up front.

---

## 1. Textbook Reference Table

⭐ = primary anchor. Filenames are the suggested local names under `textbooks/`.

| Abbrev | Filename | Title | Authors | Level | Free? (legal) |
|--------|----------|-------|---------|-------|---------------|
| **Leinster** ⭐ | `Leinster.pdf` | Basic Category Theory | Tom Leinster | Gentle | **Free** (CC BY-NC-SA) — [arXiv:1612.09375](https://arxiv.org/abs/1612.09375) |
| **Riehl** ⭐ | `Riehl.pdf` | Category Theory in Context | Emily Riehl | Advanced | **Free** (author) — [math.jhu.edu/~eriehl/context.pdf](https://math.jhu.edu/~eriehl/context.pdf) |
| Hammack | `Hammack.pdf` | Book of Proof (3e) | Richard Hammack | Gentle | **Free** — [people.vcu.edu/~rhammack/BookOfProof](https://www.people.vcu.edu/~rhammack/BookOfProof/) |
| Perrone | `Perrone.pdf` | Notes on Category Theory with examples from basic mathematics | Paolo Perrone | Gentle | **Free** — [arXiv:1912.10642](https://arxiv.org/abs/1912.10642) |
| Awodey | `Awodey.pdf` | Category Theory (2e) | Steve Awodey | Mixed | Paid (Oxford) |
| Mac Lane | `MacLane.pdf` | Categories for the Working Mathematician (2e) | Saunders Mac Lane | Advanced | Paid (Springer) |

**Leinster does almost all the work.** Every module from 1A to 6C is one section of Leinster, in
order. Riehl supplies extra examples, the early treatment of monos and epis (1B), the diagram-chase
viewpoint, and the whole of 6D (monads), which Leinster omits. Hammack is the reference for Part 0
only. Perrone is a second gentle voice for anything that does not land the first time.

References are cited at section granularity (`Leinster §2.2`, `Riehl §4.2`) and linked to the
public URLs above. No page numbers, and no exercise numbers unless checked against the PDF.

---

## 2. Course Syllabus

22 content modules across 7 teaching parts, plus a reference part.

### Part 0 — Orientation & Proof Toolkit
> *Before any category theory: how to read a definition, how to structure a proof, and the three
> proof shapes this subject uses over and over.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 0A | Orientation | What category theory is, the "bird's-eye view", a first universal property (the one-element set, the product of two sets), how to use this course, how proof review works | "Guess the object from its maps" teaser |
| 0B | Proof Toolkit I: Definitions & Direct Proof | Reading a definition as a checklist; quantifier order; proving "for all" and "there exists"; proving two functions equal; injective / surjective / bijective; composition; left and right inverses | Function-composition explorer on finite sets (injective? surjective? has a left inverse?) |
| 0C | Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher | Existence-and-uniqueness proofs; "unique up to unique isomorphism"; commutative diagrams and diagram chasing; refresher on monoids, groups, homomorphisms, posets, vector spaces, continuous maps | Does-this-diagram-commute checker on finite sets |

### Part 1 — Categories, Functors, Natural Transformations
> *Leinster Chapter 1. The three layers of the language: things, maps between things, and maps
> between those.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 1A | Categories | Definition; the axioms as proof obligations; Set, Grp, Vect, Top; a monoid as a one-object category; a poset as a category; discrete categories; hom-sets | Finite-category validator (enter a composition table, see which axiom fails) |
| 1B | Isomorphisms, Duality & New Categories from Old | Isomorphisms and uniqueness of inverses; monomorphisms and epimorphisms; the opposite category and the principle of duality; product categories; groupoids | Mono / epi / iso classifier for arrows of a finite category |
| 1C | Functors | Definition; forgetful and free functors; functors between monoids and between posets; contravariant functors; hom-functors $\mathcal{A}(A,-)$ and $\mathcal{A}(-,A)$; faithful, full, essentially surjective; **Cat** | Enumerate every functor between two small finite categories |
| 1D | Natural Transformations | Definition and the naturality square; examples (determinant, double dual, list reversal on sets); vertical and horizontal composition; functor categories; natural isomorphism | Naturality-square checker for functors between finite categories |
| 1E | Equivalence of Categories | Isomorphism vs equivalence of categories; equivalence ⇔ full, faithful and essentially surjective; skeletons; examples (finite sets vs. natural numbers, FDVect vs. matrices); duality as equivalence with an opposite | Skeleton builder: collapse a finite category along its isomorphism classes |

### Part 2 — Adjoints
> *Leinster Chapter 2. The single most important idea in the subject, seen three ways.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 2A | Adjunctions: Definition & Examples | Hom-set bijection and its naturality; transposes; free ⊣ forgetful (monoids, groups, vector spaces); discrete ⊣ forgetful ⊣ indiscrete for Top; initial and terminal objects as adjoints; Galois connections between posets; currying | Galois-connection explorer between two finite posets |
| 2B | Units & Counits | Unit and counit; the triangle identities; equivalence of the hom-set and unit–counit descriptions; closure operators from Galois connections | Triangle-identity checker for a finite adjunction |
| 2C | Adjunctions via Initial Objects | Comma categories; slice and coslice categories; universal arrows; the unit as an initial object of a comma category; uniqueness of adjoints | Comma-category builder for functors between finite categories |

### Part 3 — Interlude on Sets
> *Leinster Chapter 3. What we have been assuming about sets, and why "the category of all sets"
> needs care.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 3A | Sets & Size | Constructions with sets: products, sums, function sets, the two-element set and subsets, equalizers, quotients; small, locally small and large categories; essentially small; why **Set** is not small (Cantor / Russell) | Counting widget: $|B^A|$, $|A \times B|$, $|A + B|$ and the bijection $\mathbf{Set}(A \times B, C) \cong \mathbf{Set}(A, C^B)$ on finite sets |

### Part 4 — Representables & the Yoneda Lemma
> *Leinster Chapter 4. An object is known by the maps into it.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 4A | Representable Functors | $H^A$ and $H_A$; representable functors and representations; examples (forgetful functors, the power-set functor, bilinear maps and the tensor product); adjunctions give representables; presheaves | Hom-functor table for a finite category |
| 4B | The Yoneda Lemma | Statement; the proof, slowly: the two maps, why they are inverse, naturality in both variables; reading the lemma in a monoid (Cayley's theorem) and in a poset | Yoneda bijection made concrete: natural transformations $H_A \Rightarrow X$ vs. elements of $X(A)$ in a finite category |
| 4C | Consequences of Yoneda | Universal elements; the Yoneda embedding is full and faithful; $H_A \cong H_B \Rightarrow A \cong B$; representations are unique up to unique iso; isomorphism of objects from isomorphism of generalized elements | Yoneda embedding of a finite poset as down-sets |

### Part 5 — Limits
> *Leinster Chapter 5. Products, equalizers and pullbacks are one idea.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 5A | Limits | Products, equalizers, pullbacks; cones and the general definition; limits in Set by the explicit formula; all limits from products and equalizers; monics via pullbacks | Limit calculator for finite diagrams of finite sets |
| 5B | Colimits | Sums, coequalizers, pushouts; cocones; colimits in Set; epics via pushouts; duality with 5A; examples in Grp, Top, posets (joins and meets) | Colimit calculator (quotient by generated equivalence relation) |
| 5C | Functors & Limits | Preserve, reflect, create; forgetful functors and limits; limits in functor categories are computed pointwise (statement here, proof in 6B); limits commute with limits | Does this functor between finite categories preserve this product? |

### Part 6 — Adjoints, Representables & Limits Together
> *Leinster Chapter 6, then Riehl Chapter 5. The three big ideas turn out to be one.*

| # | Module | Topics | Interactive Elements |
|---|--------|--------|----------------------|
| 6A | Limits via Representables & Adjoints | A limit is a representation of the cone functor; limits as right adjoint to the diagonal functor; representables preserve limits | Cone-counting widget: cones on a diagram vs. maps into its limit |
| 6B | Limits & Colimits of Presheaves | Pointwise limits in functor categories; the category of elements; every presheaf is a colimit of representables (the density theorem) | Category of elements of a presheaf on a finite category |
| 6C | Adjoints & Limits | Right adjoints preserve limits; left adjoints preserve colimits; the general and special adjoint functor theorems (statements, the poset case proved in full); cartesian closed categories | Poset adjoint functor theorem: build the left adjoint of a meet-preserving map |
| 6D | Monads *(advanced)* | Monads from adjunctions; algebras; the Eilenberg–Moore and Kleisli categories; monadic functors (statement); closure operators as monads on posets | Closure operator ↔ Galois connection round-trip on a finite poset |

### Part 7 — Reference

| # | Module | Description |
|---|--------|-------------|
| 7A | Definition & Theorem Study Guide | Every definition, theorem and proof technique in the course, by module, with the statement, the picture, and where it is used later |
| | Flashcards | Markdown decks in `flashcards/`, one per Part |

---

## 3. Per-Module Source Map

| Module | Primary source(s) | Proof techniques practised |
|--------|-------------------|----------------------------|
| 0A | Leinster Ch 0 | — |
| 0B | Hammack Ch 4–6, 12; Leinster §3.1 (functions) | Direct proof, unpacking definitions, equality of functions, counterexamples |
| 0C | Hammack Ch 7 (existence & uniqueness), Ch 11; Riehl §1.6 (diagram chase) | Uniqueness arguments, diagram chasing |
| 1A | Leinster §1.1; Riehl §1.1 | Verifying axioms, "is this a category?" |
| 1B | Leinster §1.1; Riehl §1.1–1.2 | Uniqueness of inverses, cancellation, dualizing a proof |
| 1C | Leinster §1.2; Riehl §1.3 | Verifying functoriality, "functors preserve isos", counterexamples to full / faithful |
| 1D | Leinster §1.3; Riehl §1.4 | Naturality squares, pasting squares |
| 1E | Leinster §1.3; Riehl §1.5 | Building an inverse up to isomorphism; a proof that uses choice |
| 2A | Leinster §2.1; Riehl §4.1 | Naturality of a bijection, working with transposes |
| 2B | Leinster §2.2; Riehl §4.2 | Triangle identities, translating between two definitions |
| 2C | Leinster §2.3; Riehl §2.4, §4.6 (comma categories) | Initial-object arguments, uniqueness up to unique iso |
| 3A | Leinster §3.1–3.3; Riehl §1.1 (size remarks) | Explicit bijections, diagonal arguments |
| 4A | Leinster §4.1; Riehl §2.1 | Exhibiting a representation, checking naturality in one variable |
| 4B | Leinster §4.2; Riehl §2.2 | "Follow the identity" arguments |
| 4C | Leinster §4.3; Riehl §2.3 | Yoneda-style proofs: prove objects isomorphic by comparing their hom-functors |
| 5A | Leinster §5.1; Riehl §3.1–3.2 | Universal-property proofs: existence and uniqueness of the mediating map |
| 5B | Leinster §5.2; Riehl §3.1, §3.5 | Dualizing; quotient constructions |
| 5C | Leinster §5.3; Riehl §3.3, §3.8 | Preservation proofs and counterexamples |
| 6A | Leinster §6.1; Riehl §3.4 | Re-expressing one universal property as another |
| 6B | Leinster §6.2; Riehl §3.3, §2.4 | Pointwise arguments in functor categories |
| 6C | Leinster §6.3, Appendix A; Riehl §4.5–4.6 | One-line Yoneda proofs; the poset case as a complete worked AFT |
| 6D | Riehl §5.1–5.3 | Checking algebra axioms; building a comparison functor |
| 7A | All of the above | — |

---

## 4. Dependency Graph

```
0A → 0B → 0C → 1A → 1B → 1C → 1D → 1E
                                │
                                ├→ 2A → 2B → 2C
                                │         │
                                └→ 3A ────┤
                                          ▼
                                4A → 4B → 4C → 5A → 5B → 5C → 6A → 6B → 6C → 6D
```

The course is essentially linear, as Leinster is. 3A can be read any time after 1E. 6D needs 2B and
5A but not 6A–6C, so it can be taken early as a reward after Part 5.

---

## 5. Exercise Conventions (new for this course)

The earlier courses only had code exercises. This one has two kinds.

**Prove It — proof briefs.** Six per teaching module, in `exercises/<module>/pNN_<slug>.md`:
two warm-ups (unpack a definition or verify an example), three core, one stretch. Each brief has
the statement, what may be assumed, what a complete proof must show, three or four hints revealed
one at a time, and a self-check list. **No solutions exist anywhere in the repo.** The learner
writes proofs in `proofs/<module>/pNN_<slug>.md` (gitignored) and asks Claude to review them;
review points at gaps and asks questions, it does not supply a model proof. Template:
`exercises/TEMPLATE.md`.

**Compute It — finite-category code exercises.** Two or three per module, at the end of the
notebook, in the info-theory "Code It" style: a skeleton cell with a `# TODO` and commented
`print` checks carrying expected values. Finite categories use one shared encoding (see
`CLAUDE.md`), so every claim about a small category can be checked by brute force.

A theorem proved in a lecture is never also set as an exercise. Lectures model proofs with a
fixed five-step "proof anatomy" (Goal / Given / Plan / Proof / What made it work), which is what
the learner is asked to imitate.

---

## 6. Build Notes

- Notebooks are pyodide-safe: `numpy` and `matplotlib` only, plus the standard library
  (`itertools` does most of the work).
- Diagrams are drawn with `draw_diagram` (canonical source in `tools/diagram_helper.py`,
  pasted into each notebook's second cell). No TikZ, no images checked in.
- `python tools/check_course.py [module ...]` validates notebooks (marimo check, runs as a
  script, structure) and proof briefs (required sections, no solutions).
- `python build_site.py` exports to `docs/` for GitHub Pages at `/category-theory-course/`.
- No Manim animations, quiz app or games in this course.

---

## 7. Authoring Status

| Part | Modules | Status |
|------|---------|--------|
| 0 | 0A 0B 0C | authored, reviewed |
| 1 | 1A 1B 1C 1D 1E | authored, reviewed |
| 2 | 2A 2B 2C | authored, reviewed |
| 3 | 3A | authored, reviewed |
| 4 | 4A 4B 4C | authored, reviewed |
| 5 | 5A 5B 5C | authored, reviewed |
| 6 | 6A 6B 6C 6D | authored, reviewed |
| 7 | 7A | authored, reviewed |
