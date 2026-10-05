# 6D·P01 — The power set monad is a monad

**Type:** warm-up · **Technique:** verifying axioms with elements · **Unlocked by:** `6d_monads` §1
**Source:** adapted from Riehl §5.1

## Statement

On $\mathbf{Set}$, let $\mathscr{P}(X)$ be the set of subsets of $X$ and, for $f \colon X \to Y$, let
$\mathscr{P}(f) \colon \mathscr{P}(X) \to \mathscr{P}(Y)$ be direct image,
$S \mapsto \{ f(x) : x \in S \}$. Define
$$\eta_X \colon X \to \mathscr{P}(X), \quad x \mapsto \{x\}, \qquad
\mu_X \colon \mathscr{P}(\mathscr{P}(X)) \to \mathscr{P}(X), \quad \mathcal{S} \mapsto \bigcup \mathcal{S}.$$

Prove that $(\mathscr{P}, \eta, \mu)$ is a monad on $\mathbf{Set}$.

## What you may use

- The definition of a monad.
- Elementary set theory: two sets are equal when they have the same elements; two functions are equal when they agree on every input (0B).

## What a complete proof must show

- [ ] $\mathscr{P}$ is a functor (identities and composites).
- [ ] $\eta$ and $\mu$ are natural: one square each, checked on an arbitrary element.
- [ ] Associativity, checked on an arbitrary element of $\mathscr{P}(\mathscr{P}(\mathscr{P}(X)))$.
- [ ] Both unit laws, checked on an arbitrary $S \in \mathscr{P}(X)$.
- [ ] Each equality of sets proved by showing the two sides have the same elements.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Everything here is an equation between functions on sets, so everything is checked by feeding in
an arbitrary input. Start by listing the seven things to verify, with the domain of each function
involved.

</details>

<details>
<summary>Hint 2 — the levels</summary>

For associativity the input is a set of sets of subsets of $X$. Describe in words what each of
the two routes does to it: which level of brackets does $\mu_{\mathscr{P}X}$ remove, and which does
$\mathscr{P}(\mu_X)$ remove?

</details>

<details>
<summary>Hint 3 — direct images of the structure maps</summary>

$\mathscr{P}(\mu_X)$ and $\mathscr{P}(\eta_X)$ are direct-image functions. Write out
$\mathscr{P}(\eta_X)(S)$ as a set of sets, for a subset $S$ of $X$, before taking any union.

</details>

<details>
<summary>Hint 4 — when is an element in a union?</summary>

Every step reduces to the definition: $x \in \bigcup \mathcal{S}$ exactly when $x \in S$ for some
$S \in \mathcal{S}$. For the associativity law, chase "$x$ is in the left side" and "$x$ is in the
right side" down to statements with existential quantifiers and compare.

</details>

## Check yourself

- Did the empty set need separate treatment anywhere?
- The lecture's non-example replaces $\eta_X(x) = \{x\}$ by $\eta_X(x) = \emptyset$. At which exact step would your proof break?
- Would the same proof work with "finite subsets" in place of "subsets"? With "non-empty subsets"?

## Write it up

Write your proof in `proofs/6d/p01_powerset_monad_axioms.md`, then ask Claude to review it.
