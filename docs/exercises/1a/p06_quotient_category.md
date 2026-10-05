# 1A·P06 — The quotient of a category by a congruence

**Type:** stretch · **Technique:** well-definedness, then verifying axioms · **Unlocked by:** `1a_categories` §1, §2
**Source:** adapted from Leinster §1.1 (the construction behind the homotopy category of spaces)

## Statement

Let $\mathcal{A}$ be a category. Suppose that for every pair of objects $A, B$ we are given an
equivalence relation $\sim$ on the hom-set $\mathcal{A}(A, B)$, and that these relations are
**compatible with composition**:

> for all objects $A, B, C$, all $f, f' \in \mathcal{A}(A, B)$ and all $g, g' \in \mathcal{A}(B, C)$:
> if $f \sim f'$ and $g \sim g'$, then $g \circ f \sim g' \circ f'$.

Write $[f]$ for the equivalence class of an arrow $f$. Define $\mathcal{A}/{\sim}$ as follows:

- objects: the objects of $\mathcal{A}$;
- arrows $A \to B$: the equivalence classes $[f]$ of arrows $f \in \mathcal{A}(A, B)$;
- composition: $[g] \circ [f] = [g \circ f]$;
- identities: $[1_A]$.

Prove that $\mathcal{A}/{\sim}$ is a category.

## What you may use

- The definition of a category, and the fact that $\mathcal{A}$ is one.
- The definition of an equivalence relation (reflexive, symmetric, transitive) and of
  equivalence classes, from your algebra course: $[f] = [f']$ if and only if $f \sim f'$.
- The compatibility hypothesis.

## What a complete proof must show

- [ ] That the rule "$[g] \circ [f] = [g \circ f]$" really defines a function on pairs of *classes*.
- [ ] That this point is settled **before** any axiom is checked.
- [ ] Associativity and both identity laws in $\mathcal{A}/{\sim}$, each reduced to the corresponding axiom in $\mathcal{A}$ with the reduction written out.
- [ ] It is stated where the compatibility hypothesis is used and where it is not needed.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

There are two separate jobs. One is the usual checklist for a category. The other comes first
and is the reason this is a stretch exercise: the composition rule is stated in terms of the
arrows $f$ and $g$, but an arrow of $\mathcal{A}/{\sim}$ is a class, and a class usually
contains many arrows. What has to be true for the rule to make sense at all?

</details>

<details>
<summary>Hint 2 — stating what must be checked</summary>

Write down, with all its quantifiers, the sentence that says the rule gives one answer and not
several. It should begin "for all ... and all ... such that ...". Then compare what you have
written with the hypotheses of the exercise.

</details>

<details>
<summary>Hint 3 — the axioms</summary>

Once the first job is done, look at an axiom, say associativity, as a statement about three
arrows of $\mathcal{A}/{\sim}$. Each of those is the class of something. Apply the definition
of composition in $\mathcal{A}/{\sim}$ as many times as needed and look at what ends up inside
the square brackets on each side.

</details>

<details>
<summary>Hint 4 — a sanity check on your argument</summary>

If your proof never mentions the compatibility hypothesis, something is missing. If it invokes
the compatibility hypothesis again while verifying associativity, something is probably being
done twice. Where is the one place it belongs?

</details>

## Check yourself

- Does your first step vary the representatives of *both* classes, or only one of them?
- Could the construction have gone wrong if $\sim$ were an equivalence relation on each hom-set that was *not* compatible with composition? Try to describe what would fail.
- Did you use reflexivity, symmetry or transitivity of $\sim$ anywhere explicitly, or only the fact about when two classes are equal?
- What is $\mathcal{A}/{\sim}$ when $\sim$ is equality? When $f \sim f'$ for all parallel $f, f'$?

## Write it up

Write your proof in `proofs/1a/p06_quotient_category.md`, then ask Claude to review it.
