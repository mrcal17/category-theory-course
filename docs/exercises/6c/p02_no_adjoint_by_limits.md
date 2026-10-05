# 6C·P02 — A functor with no adjoint on either side

**Type:** warm-up · **Technique:** counterexample via a preservation theorem · **Unlocked by:** `6c_adjoints_and_limits` §3
**Source:** adapted from Leinster §6.3

## Statement

Let $B$ be a non-empty set, and let $S \colon \mathbf{Set} \to \mathbf{Set}$ be the functor
$S(X) = X + B$, $S(f) = f + 1_B$ (disjoint union with $B$).

1. Prove that $S$ has no left adjoint.
2. Prove that $S$ has no right adjoint.
3. What happens when $B$ is empty?

## What you may use

- Theorem 1 of the lecture (right adjoints preserve limits, left adjoints preserve colimits).
- The description of terminal and initial objects of $\mathbf{Set}$ (3A, 5A, 5B), and that isomorphic sets have the same cardinality.

## What a complete proof must show

- [ ] For each part, the contrapositive of Theorem 1 stated in the correct form: which kind of adjoint is excluded by the failure of which kind of preservation.
- [ ] A specific limit, and a specific colimit, that $S$ does not preserve, with a reason why the image is not a limit (colimit).
- [ ] Part 3 answered with a reason.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Each part is a contrapositive. Before looking for examples, write down two sentences of the form
"if $S$ had a ... adjoint, then $S$ would be a ... adjoint, so it would preserve ...". Getting
the left/right bookkeeping correct is most of the exercise.

</details>

<details>
<summary>Hint 2 — look for the smallest diagrams</summary>

The simplest limit and the simplest colimit are those of the empty diagram. What are they in
$\mathbf{Set}$, and what does $S$ do to them?

</details>

<details>
<summary>Hint 3 — proving something is not a limit</summary>

To show that a set is not terminal (or not initial) in $\mathbf{Set}$ it is enough to count its
elements. Why is that enough?

</details>

## Check yourself

- If you swapped the words "left" and "right" throughout your answer, would you notice? Test each sentence against a functor you know, such as the forgetful functor from groups to sets.
- Does $S$ preserve binary products? Binary sums? Neither was needed, but it is worth knowing.
- Is "does not preserve the terminal object" the same as "does not preserve limits"? Say why one implies the other.

## Write it up

Write your proof in `proofs/6c/p02_no_adjoint_by_limits.md`, then ask Claude to review it.
