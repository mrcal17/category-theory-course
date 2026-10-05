# 0C·P01 — Equations in a group have exactly one solution

**Type:** warm-up · **Technique:** existence and uniqueness · **Unlocked by:** `0c_proof_toolkit_uniqueness` §1, §2
**Source:** standard group theory; technique from Hammack Ch 7

## Statement

Let $(G, \cdot, e)$ be a group and let $a, b \in G$. Prove that there exists a unique $x \in G$
such that $a \cdot x = b$.

## What you may use

- The definition of a group: associativity, the identity laws, and the existence of an inverse
  $a^{-1}$ for each $a$, with $a \cdot a^{-1} = e = a^{-1} \cdot a$ (0C §2).
- You may **not** use commutativity: a group need not be commutative.

## What a complete proof must show

- [ ] The proof is split into an existence part (E) and a uniqueness part (U), labelled.
- [ ] (E) A specific element of $G$ is named, and the equation $a \cdot x = b$ is *verified* for
      it, with each step justified by a group axiom.
- [ ] (U) The argument begins with elements known only to satisfy the equation, and ends with
      their equality.
- [ ] No step moves an element past another (no hidden use of commutativity), and every
      re-bracketing is attributed to associativity.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

"There exists a unique" is two statements (0C §1), so two proofs. (E) is a "there exists":
name a witness and check it. (U) is a "for all ... if ... then": let two elements both satisfy
the equation, and show they are equal.

</details>

<details>
<summary>Hint 2 — finding the witness</summary>

On scratch paper, pretend $x$ is a solution and manipulate the equation until $x$ stands alone.
Be careful which side you multiply on. That scratch work is how you *find* the witness; it is
not the proof of (E). The proof of (E) starts from the witness and verifies the equation.

</details>

<details>
<summary>Hint 3 — uniqueness</summary>

If $x$ and $x'$ are both solutions, you have two expressions equal to $b$, hence equal to each
other. What can you do to both sides of that equation to make $a$ disappear? Three axioms are
needed to finish, in a definite order; name each as you use it.

</details>

## Check yourself

- Is your scratch work for finding the witness the same calculation as your uniqueness proof?
  What does that tell you about the "forced value" method of 0C §1?
- What is the unique solution of $x \cdot a = b$? Is it the same element?
- Where does your proof break in the monoid $(\mathbb{Z}, \times, 1)$? Find $a, b$ there for which
  existence fails, and $a, b$ for which uniqueness fails.

## Write it up

Write your proof in `proofs/0c/p01_unique_solution_in_a_group.md`, then ask Claude to review it.
