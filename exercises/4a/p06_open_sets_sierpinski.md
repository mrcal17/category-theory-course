# 4A·P06 — Open sets and the Sierpiński space

**Type:** stretch · **Technique:** exhibiting a representation; naturality in one variable · **Unlocked by:** `4a_representables` §4
**Source:** adapted from Leinster §4.1

## Statement

For a topological space $S$, let $\mathscr{O}(S)$ be the set of open subsets of $S$. For a continuous
map $g \colon S' \to S$, let $\mathscr{O}(g) \colon \mathscr{O}(S) \to \mathscr{O}(S')$ send an open
set $W \subseteq S$ to its preimage $g^{-1}(W)$.

1. Check that $\mathscr{O}$ is a presheaf on $\mathbf{Top}$, that is, a functor
   $\mathbf{Top}^{\mathrm{op}} \to \mathbf{Set}$.
2. Find a topology on the two-element set $\{0, 1\}$ such that the resulting space $\mathbb{S}$
   represents $\mathscr{O}$, and prove that it does:
   $$\mathscr{O} \cong \mathbf{Top}(-, \mathbb{S}).$$

## What you may use

- The definition of a topology and of a continuous map (0C refresher): a function is continuous
  when the preimage of every open set is open.
- Proposition 4.1 of 4A, the representation $\mathscr{P} \cong \mathbf{Set}(-, 2)$, both as a model
  and as a result: you may quote the bijection between subsets and characteristic functions.
- The definition of a representable presheaf (4A §4).

## What a complete proof must show

- [ ] Part 1 says why $g^{-1}(W)$ is open, and checks both functor axioms in the contravariant form.
- [ ] The topology on $\{0, 1\}$ is stated by listing its open sets, and it is checked to be a topology.
- [ ] For every space $S$, a function $\mathbf{Top}(S, \mathbb{S}) \to \mathscr{O}(S)$ is defined and
      its values are shown to be *open* subsets.
- [ ] Bijectivity: in particular, for every open $W \subseteq S$ the function you produce
      $S \to \mathbb{S}$ is shown to be continuous, by examining every open set of $\mathbb{S}$.
- [ ] Naturality is stated and verified for an arbitrary continuous map $g \colon S' \to S$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is Proposition 4.1 of 4A with topology added. The underlying bijection between subsets and
functions into a two-element set is unchanged. What is new is a matching of *conditions*: on one
side "the subset is open", on the other "the function is continuous". Your topology must make
those two conditions equivalent.

</details>

<details>
<summary>Hint 2 — let the requirement choose the topology</summary>

There are only four topologies on a two-element set; consider what each would force. For a function $\chi \colon S \to \{0, 1\}$, continuity is a list of demands, one
for each open set of the target. Which subsets of $\{0, 1\}$ do you want on that list so that the
demands add up to exactly "$\chi^{-1}\{1\}$ is open", no more and no less?

</details>

<details>
<summary>Hint 3 — test your candidate both ways</summary>

With your topology fixed, ask two questions. If $\chi$ is continuous, why is $\chi^{-1}\{1\}$ open?
If $W \subseteq S$ is open, what are the preimages under its characteristic function of *each*
open set of your space, and is each of them open in $S$? If either question fails, the topology
has too few or too many open sets.

</details>

<details>
<summary>Hint 4 — naturality</summary>

Once the components are in place, naturality is the same identity about preimages that finished
Proposition 4.1. State it for a continuous $g \colon S' \to S$ and verify it by taking an arbitrary
point of $S'$.

</details>

## Check yourself

- Would the discrete topology on $\{0, 1\}$ work? What functor on $\mathbf{Top}$ does the discrete
  two-point space represent instead?
- Is your space symmetric in $0$ and $1$? Should it be?
- Which functor does the two-point space with the *indiscrete* topology represent?

## Write it up

Write your proof in `proofs/4a/p06_open_sets_sierpinski.md`, then ask Claude to review it.
