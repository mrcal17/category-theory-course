# Category Theory — a proof-centred course

A self-study, pure-mathematics course in category theory, built as interactive
[marimo](https://marimo.io) notebooks. It follows Tom Leinster's *Basic Category Theory*
chapter by chapter, from the definition of a category to the adjoint functor theorems,
and finishes with monads from Emily Riehl's *Category Theory in Context*.

**Who it is for.** Someone who is comfortable with sets and functions, has met groups and
vector spaces, and has found proofs hard. Proof-writing is the centre of the course: Part 0
rebuilds proof technique, every lecture proves its theorems in a fixed five-step shape
(Goal / Given / Plan / Proof / What made it work), and every module ends in proofs that you
write yourself. Examples come from sets, monoids, groups, posets, vector spaces and
topological spaces.

## Structure

24 notebooks: the index, 22 content modules in 7 teaching parts, and a reference module.

| Part | Modules | Subject |
|------|---------|---------|
| 0 | 0A 0B 0C | Orientation & proof toolkit |
| 1 | 1A 1B 1C 1D 1E | Categories, functors, natural transformations |
| 2 | 2A 2B 2C | Adjoints |
| 3 | 3A | Interlude on sets and size |
| 4 | 4A 4B 4C | Representables & the Yoneda lemma |
| 5 | 5A 5B 5C | Limits and colimits |
| 6 | 6A 6B 6C 6D | Adjoints, representables & limits together; monads |
| 7 | 7A | Definition & theorem study guide |

The full syllabus, source map and dependency graph are in [`SEGMENTATION.md`](SEGMENTATION.md).
Start at [`notebooks/home.py`](notebooks/home.py).

## Running it

```bash
pip install -r requirements.txt     # marimo, numpy, matplotlib

pwsh ./launch.ps1 1a                # Windows: open Module 1A
bash launch.sh 1a                   # macOS / Linux: open Module 1A
pwsh ./launch.ps1                   # no argument: open the course home page
```

## Exercises and the review loop

Each teaching module (0B–6D) has two kinds of exercise.

- **Compute It** — two or three skeleton cells at the end of the notebook about finite
  categories. Fill in the `# TODO` lines and uncomment the checks.
- **Prove It** — six proof briefs in `exercises/<module>/pNN_<slug>.md`: two warm-ups, three
  core, one stretch. Each brief gives the statement, what you may use, what a complete proof
  must show, three or four hints revealed one at a time, and a self-check list.

The loop:

1. Read the brief; open hints one at a time, only when stuck.
2. Write your proof in `proofs/<module>/pNN_<slug>.md` (same filename as the brief).
3. Ask Claude to review it, for example `review proofs/1a/p03_identities_unique.md`.
   Review points at gaps and asks questions.
4. Revise until it holds up, then tick the row in `PROGRESS.md`.

**The repository is solution-free.** No brief, hint, notebook or flashcard contains a proof
of an exercise, and review never rewrites your proof or supplies a model one. Your own proofs
in `proofs/` are gitignored. Lectures do prove the theorems they teach, in full, as models to
imitate; a theorem proved in a lecture is never also set as an exercise.

## Layout

| Path | What |
|------|------|
| `notebooks/` | lecture notebooks (`home.py` is the index, `7a_study_guide.py` the reference) |
| `exercises/` | proof briefs, six per module, plus `TEMPLATE.md` |
| `proofs/` | your proofs (gitignored) |
| `flashcards/` | one Markdown deck per Part |
| `PROGRESS.md` | checklist of proof briefs |
| `tools/` | `check_course.py` (validator) and `diagram_helper.py` (diagram drawing) |
| `SEGMENTATION.md` | course plan, syllabus, source map, dependency graph |
| `CLAUDE.md` | authoring, build and tutoring conventions |
| `build_site.py` | export the notebooks to a WASM site in `docs/` |

## Validating and building

```bash
python tools/check_course.py          # every notebook and every proof brief
python tools/check_course.py 1a 1b    # only these modules
python build_site.py                  # export to docs/ for GitHub Pages
```

The validator runs `marimo check` on each notebook, executes it as a script, checks its
structure, and checks that each proof brief follows the template and contains no solution.

## Textbooks

No PDFs are committed; the course links to public pages and cites at section level.

| Book | Author | Role | Link |
|------|--------|------|------|
| *Basic Category Theory* | Tom Leinster | Primary text, Parts 1–6 | [arXiv:1612.09375](https://arxiv.org/abs/1612.09375) (free) |
| *Category Theory in Context* | Emily Riehl | Extra examples; monads (6D) | [author PDF](https://math.jhu.edu/~eriehl/context.pdf) (free) |
| *Book of Proof* (3e) | Richard Hammack | Proof technique, Part 0 | [book page](https://www.people.vcu.edu/~rhammack/BookOfProof/) (free) |
| *Notes on Category Theory with examples from basic mathematics* | Paolo Perrone | Second gentle exposition | [arXiv:1912.10642](https://arxiv.org/abs/1912.10642) (free) |
| *Category Theory* (2e) | Steve Awodey | Further reading | [Oxford](https://global.oup.com/academic/product/category-theory-9780199237180) (paid) |
| *Categories for the Working Mathematician* (2e) | Saunders Mac Lane | Further reading | [Springer](https://link.springer.com/book/10.1007/978-1-4757-4721-8) (paid) |
