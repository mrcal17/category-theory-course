# CLAUDE.md — authoring, build and tutoring conventions for `category-theory-course`

The course plan, syllabus, per-module source map and exercise conventions live in
`SEGMENTATION.md` — read it first for any content work. This course mirrors
`info-theory-course` (marimo lectures, `home.py`, WASM site) with one deliberate
addition: **proof exercises**, handled like the solution-free briefs of `gpu-kernels`.

> **Teaching-mode rule (non-negotiable).** The learner writes every proof and every
> line of exercise code. Never put a worked solution to an exercise anywhere in this
> repo — not in a brief, not in a hint, not in a `<details>` block, not in a notebook.
> Hints are conceptual and escalate; the last hint still leaves the proof to write.
> When reviewing a proof in `proofs/`, point at the gap and ask a question; do not
> rewrite the proof. Lectures *do* prove the theorems they teach, in full — those are
> models to imitate, and a theorem proved in a lecture is never set as an exercise.

---

## Module order (single source of truth for filenames and nav links)

| ID | File | Title |
|----|------|-------|
| — | `home.py` | Course home |
| 0A | `0a_orientation.py` | Orientation |
| 0B | `0b_proof_toolkit_definitions.py` | Proof Toolkit I: Definitions & Direct Proof |
| 0C | `0c_proof_toolkit_uniqueness.py` | Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher |
| 1A | `1a_categories.py` | Categories |
| 1B | `1b_isomorphisms_duality.py` | Isomorphisms, Duality & New Categories from Old |
| 1C | `1c_functors.py` | Functors |
| 1D | `1d_natural_transformations.py` | Natural Transformations |
| 1E | `1e_equivalence.py` | Equivalence of Categories |
| 2A | `2a_adjunctions.py` | Adjunctions: Definition & Examples |
| 2B | `2b_units_counits.py` | Units & Counits |
| 2C | `2c_universal_arrows.py` | Adjunctions via Initial Objects |
| 3A | `3a_sets_and_size.py` | Sets & Size |
| 4A | `4a_representables.py` | Representable Functors |
| 4B | `4b_yoneda_lemma.py` | The Yoneda Lemma |
| 4C | `4c_yoneda_consequences.py` | Consequences of Yoneda |
| 5A | `5a_limits.py` | Limits |
| 5B | `5b_colimits.py` | Colimits |
| 5C | `5c_functors_and_limits.py` | Functors & Limits |
| 6A | `6a_limits_representables_adjoints.py` | Limits via Representables & Adjoints |
| 6B | `6b_presheaf_limits.py` | Limits & Colimits of Presheaves |
| 6C | `6c_adjoints_and_limits.py` | Adjoints & Limits |
| 6D | `6d_monads.py` | Monads *(advanced)* |
| 7A | `7a_study_guide.py` | Definition & Theorem Study Guide |

Prev / next in the nav footer follow this table top to bottom (0A's prev is home; 7A has no next).

---

## Notebook conventions (copy these exactly)

**Standard header** — every notebook starts with:
```python
import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)
```
and ends with:
```python
if __name__ == "__main__":
    app.run()
```

**Rules of the road:**
1. **First cell** is the bare `import marimo as mo`. Import `numpy` / `matplotlib` /
   `itertools` **locally inside each code cell that uses them**.
2. **Second cell** (only in notebooks that draw diagrams) is a `hide_code=True` cell
   that defines `draw_diagram` — pasted verbatim from `tools/diagram_helper.py` — and
   returns `(draw_diagram,)`. Later cells take `draw_diagram` as a cell argument.
   This is the one helper allowed to be shared across cells. (`marimo check --fix`
   rewrites that cell as `@app.function(hide_code=True)`, after which later cells
   call `draw_diagram` directly; both forms are fine.)
3. **Markdown cells** use `mo.md(r"""...""")` — always raw triple-quoted strings, never
   f-strings. Use `@app.cell(hide_code=True)` for pure-prose cells.
4. **Math** is LaTeX rendered by KaTeX: inline `$f \colon A \to B$`, display `$$ ... $$`.
   Box key results with `$$\boxed{...}$$`. KaTeX has **no** `tikz-cd` and no `xymatrix`:
   short chains are written inline (`$A \xrightarrow{f} B \xrightarrow{g} C$`), anything
   with a shape (triangles, squares, cones) is drawn with `draw_diagram`.
5. **Demo code cells** wrap everything in a local `def _run(): ...; _run()` and prefix
   locals with `_`. Never redeclare a variable across cells; never use `global`.
6. **Plots:** matplotlib only; the figure is the last expression — never `plt.show()`.
7. **Interactivity:** define a `mo.ui.*` element in one cell and display it; read
   `.value` in a **separate, later** cell.
8. **Pyodide-safe:** standard library, `numpy`, `matplotlib`. Nothing else. No file or
   network access. Keep every brute-force enumeration under about a second.
9. **Last cell** is a `hide_code=True` nav footer:
   `[&#8593; Course home](../) | &#8592; Prev: [1A: Categories](../1a_categories/) | Next: [1C: Functors](../1c_functors/) &#8594;`
10. After authoring, run `python tools/check_course.py <id>` (it runs `marimo check`,
    executes the notebook as a script, and checks structure).

**Lesson skeleton** (teaching modules 0B–6D):

1. `# <ID>: <Title>` + an epigraph blockquote + 2–3 paragraphs: what question this module
   answers, what the learner will be able to *prove* by the end.
2. Numbered concept sections `## 1. ...`, `## 2. ...` (typically 5–8). Each has, in order:
   motivation in plain words → the **definition** in a blockquote, followed by a
   "**Reading the definition**" list that restates it as a checklist of things to verify →
   two or more pure-math examples and at least one non-example → where there is a result,
   a full proof in **proof anatomy** form (below) → a `>` reference blockquote citing
   Leinster / Riehl at section granularity with the public links from `SEGMENTATION.md`.
3. Diagrams via `draw_diagram` wherever a statement has a shape.
4. At least one `mo.ui` interactive element (the one named in the syllabus table).
5. `## Common Proof Mistakes` — three to five specific errors for this module's material
   (e.g. "proving uniqueness by exhibiting one map", "using a map before showing it is
   well defined") with a one-line diagnosis each.
6. `## Why This Matters` — where this module is used later in the course.
7. `## Compute It: Finite-Category Exercises` — 2–3 skeleton cells (see below).
8. `## Prove It: Proof Exercises` — a table of this module's six briefs
   (`# | Brief | Type | Technique`) with the path of each file in code font, plus the
   two-line reminder of how to submit a proof for review.
9. Nav footer.

0A (orientation), 7A (study guide) and `home.py` follow the info-theory equivalents instead.

**Proof anatomy.** Every proof shown in a lecture uses the same five labelled steps, so the
learner can copy the *shape*:

- **Goal.** The statement, with its quantifiers written out.
- **Given.** Exactly which definitions and hypotheses are available.
- **Plan.** One or two sentences: the shape of the argument (direct / uniqueness /
  diagram chase / "follow the identity" / dualize an earlier proof).
- **Proof.** Every step justified by name ("by associativity", "by naturality of
  $\alpha$ at $f$", "because $g$ is monic").
- **What made it work.** The one idea to remember, and when to reach for it again.

**Tone.** Second person, concrete, unhurried. The learner knows what a group and a
vector space are, and has found proofs hard: never write "clearly", "obviously" or
"it is easy to see"; say what must be checked and check it. Pure-math examples only —
no programming analogies (no "types", "Haskell", "monads are burritos").

**Mathematical conventions** (Leinster's):
- Categories $\mathcal{A}, \mathcal{B}, \mathcal{C}$ (`\mathcal`); named categories bold:
  $\mathbf{Set}, \mathbf{Grp}, \mathbf{Ab}, \mathbf{Mon}, \mathbf{Vect}_k, \mathbf{Top}, \mathbf{Cat}$.
- Hom-sets $\mathcal{A}(A, B)$; identities $1_A$; composition $g \circ f$ ("$g$ after $f$"), also $gf$.
- Functor categories $[\mathcal{A}, \mathcal{B}]$; opposite $\mathcal{A}^{\mathrm{op}}$.
- $H^A = \mathcal{A}(A, -)$ covariant, $H_A = \mathcal{A}(-, A)$ contravariant.
- Adjunctions $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$ left adjoint,
  transposes written $\bar{f}$, unit $\eta$, counit $\varepsilon$.
- Products $X \times Y$, sums (coproducts) $X + Y$, terminal object $1$, initial object $0$.

**Finite-category encoding** (use this everywhere a small category is computed with):
```python
cat = {
    "objects": ["A", "B"],
    "arrows": {"1A": ("A", "A"), "1B": ("B", "B"), "f": ("A", "B")},   # name -> (domain, codomain)
    "identity": {"A": "1A", "B": "1B"},
    "compose": {("1B", "f"): "f", ("f", "1A"): "f", ("1A", "1A"): "1A", ("1B", "1B"): "1B"},
    # compose[(g, f)] = g∘f, defined exactly when cod(f) == dom(g)
}
```
A functor is `{"objects": {A: FA, ...}, "arrows": {f: Ff, ...}}`; a natural transformation is
`{A: name_of_component_arrow, ...}`. Posets and monoids are converted to this encoding by a
few lines of code in the cell that needs them.

---

## Exercise conventions

**Compute It** (in the notebook). A `mo.md` cell with `### Exercise N: <title>` and the task,
then a code cell with a skeleton: scaffolding done, the essential lines left as `# TODO`
with `...` placeholders, and commented-out `print` checks carrying the expected values.
The cell must run without error as shipped. No solution cell, no solution in `<details>`.

**Prove It** (in `exercises/<module>/pNN_<slug>.md`). Follow `exercises/TEMPLATE.md`
exactly — the validator checks the section headings. Six per module: two warm-ups, three
core, one stretch. Rules for hints:
- three or four, each in its own `<details>` so they are revealed one at a time;
- hint 1 names the *kind* of proof and what must be shown; later hints narrow where to look;
- no hint writes out a step of the proof, an equation chain, or the key construction in
  final form. If a construction is the whole difficulty, the hint asks the question whose
  answer is the construction.

Exercises are adapted from Leinster and Riehl; cite the section, not an exercise number.

**Learner's proofs** go in `proofs/<module>/pNN_<slug>.md` (gitignored). `PROGRESS.md` is
the checklist; update a row when the learner says a proof is done and it has been reviewed.

---

## Flashcards

`flashcards/<N> - <Part name>.md`, first line `#flashcards/part<N>`, then `## <ID>: <Title>`
sections of cards in the form *prompt / `?` / answer*, separated by blank lines. They mirror
module content — update them when a module changes. Cards cover definitions, statements and
"what technique proves this?"; they never contain a proof of an exercise.

---

## Build & run

- **Open a lecture:** `pwsh ./launch.ps1 1a` or `bash launch.sh 1a`
- **Validate:** `python tools/check_course.py` (all) or `python tools/check_course.py 1a 1b`
- **Build the WASM site:** `python build_site.py` → `docs/`
