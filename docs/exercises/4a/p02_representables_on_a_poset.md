# 4A·P02 — Representable presheaves on a poset

**Type:** warm-up · **Technique:** unpacking a definition · **Unlocked by:** `4a_representables` §4
**Source:** adapted from Riehl §2.1

## Statement

Let $P$ be a poset, regarded as a category with exactly one arrow $b \to a$ when $b \le a$ and no
arrow otherwise. Let $X \colon P^{\mathrm{op}} \to \mathbf{Set}$ be a presheaf on $P$, and suppose
that $X$ is representable, say $X \cong H_a$ for an element $a \in P$.

Prove:

1. for every $b \in P$, the set $X(b)$ has at most one element;
2. $\{\, b \in P : X(b) \neq \varnothing \,\} = \{\, b \in P : b \le a \,\}$;
3. consequently the set $\{\, b \in P : X(b) \neq \varnothing \,\}$ has a greatest element.

Then give an example of a presheaf on the two-element poset $\{0 \le 1\}$ that is not representable,
and say which of 1–3 it violates.

## What you may use

- The definition of $H_a$ and of a representable presheaf from 4A §4.
- From 1D: every component of a natural isomorphism is an isomorphism; an isomorphism in
  $\mathbf{Set}$ is a bijection.
- The definition of a poset, and of "greatest element" of a subset.

## What a complete proof must show

- [ ] It describes the set $H_a(b)$ for an arbitrary $b$, with a reason.
- [ ] It says exactly which part of the hypothesis $X \cong H_a$ is used, and that only the
      components (not naturality) are needed for 1 and 2, if that is the case in your proof.
- [ ] For 3, it names the greatest element and checks both halves of the definition of "greatest":
      it belongs to the set, and everything in the set is below it.
- [ ] The example is a complete presheaf (two sets and one function), not just two sets.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Nothing here needs a construction. Unpack "$X \cong H_a$" into a statement about each set $X(b)$
separately, and then read off what you know about $H_a(b)$ in a poset.

</details>

<details>
<summary>Hint 2 — what a bijection preserves</summary>

If two sets are in bijection, which properties do they share? In particular: number of elements,
and being empty or not.

</details>

<details>
<summary>Hint 3 — the greatest element</summary>

For part 3 you need an element of the set that is above all the others. Part 2 has already
rewritten the set in a form where one candidate stands out. Which property of $\le$ shows that the
candidate lies in the set?

</details>

## Check yourself

- Did you use reflexivity of $\le$ anywhere? You should have.
- Is the converse true: if every $X(b)$ has at most one element, must $X$ be representable?
  Does your example answer this?
- Compare part 3 with the remark in 4A §4 that $H_A(A)$ is never empty.

## Write it up

Write your proof in `proofs/4a/p02_representables_on_a_poset.md`, then ask Claude to review it.
