# 6C·P05 — The opposite of Set is not cartesian closed

**Type:** core · **Technique:** dualizing, then a preservation argument · **Unlocked by:** `6c_adjoints_and_limits` §7
**Source:** adapted from Leinster §6.3

## Statement

Prove that the category $\mathbf{Set}^{\mathrm{op}}$ has finite products but is not cartesian closed.

## What you may use

- The descriptions of products, sums, the terminal object and the initial object of $\mathbf{Set}$ (3A, 5A, 5B).
- The principle of duality (1B): a limit in $\mathcal{A}^{\mathrm{op}}$ is a colimit in $\mathcal{A}$, and conversely.
- Proposition 1 of the lecture.
- That $P$ and $Q$ are isomorphic in $\mathcal{A}^{\mathrm{op}}$ exactly when they are isomorphic in $\mathcal{A}$.

## What a complete proof must show

- [ ] A dictionary: the binary product, terminal object and initial object of $\mathbf{Set}^{\mathrm{op}}$, each described as a construction in $\mathbf{Set}$.
- [ ] The statement that Proposition 1 would force, written in $\mathbf{Set}^{\mathrm{op}}$ and then translated into $\mathbf{Set}$.
- [ ] A specific set for which the translated statement is false, with the reason.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a proof by contradiction that follows the lecture's argument for $\mathbf{Vect}_k$. The
new difficulty is bookkeeping: every word (product, initial, terminal) must be translated from
$\mathbf{Set}^{\mathrm{op}}$ to $\mathbf{Set}$. Make the dictionary before arguing.

</details>

<details>
<summary>Hint 2 — what Proposition 1 gives</summary>

Proposition 1 has a consequence about the initial object and products. Write that consequence
for $\mathbf{Set}^{\mathrm{op}}$, using the symbols $0$ and $\times$ *of that category*. Only then
replace each symbol using your dictionary.

</details>

<details>
<summary>Hint 3 — finding the contradiction</summary>

After translation you have a claimed isomorphism between two sets built from an arbitrary set $B$.
Count elements. For which $B$ does the count fail?

</details>

## Check yourself

- Did you at any point use the initial object of $\mathbf{Set}$ where you needed the initial object of $\mathbf{Set}^{\mathrm{op}}$?
- Does your argument show that *no* object $B$ has an exponential functor, or only that some do not? Which did you need?
- The same argument shows something about any cartesian closed category whose opposite is also cartesian closed. What?

## Write it up

Write your proof in `proofs/6c/p05_set_op_not_cartesian_closed.md`, then ask Claude to review it.
