# 5C·P06 — Creation gives existence, preservation and reflection

**Type:** stretch · **Technique:** chaining universal properties · **Unlocked by:** `5c_functors_and_limits` §2–§4
**Source:** adapted from Leinster §5.3

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor and $\mathbf{I}$ a small category. Suppose
$F$ **creates** limits of shape $\mathbf{I}$, in the sense of the definition in 5C §4.

1. Prove that $F$ reflects limits of shape $\mathbf{I}$.

Suppose in addition that $\mathcal{B}$ **has** limits of shape $\mathbf{I}$.

2. Prove that $\mathcal{A}$ has limits of shape $\mathbf{I}$.
3. Prove that $F$ preserves limits of shape $\mathbf{I}$.

## What you may use

- The definitions of preserves, reflects and creates (5C §2–§4), exactly as stated there. In
  particular, creation says the lift is **unique** among cones on $D$ with $F(A) = B$ and
  $F(p_I) = q_I$ for all $I$.
- Proof 1 of 5C (the image of a cone is a cone) and Proof 2 of 5C (to verify preservation for a
  diagram it suffices to find one limit cone whose image is a limit cone).
- The uniqueness of limits (5A §5, Proofs 5 and 6).

## What a complete proof must show

- [ ] Part 1: an arbitrary cone $(p_I \colon A \to D(I))$ on $D$ whose image is a limit cone is
      fixed; creation is applied to a named limit cone in $\mathcal{B}$; and it is explained why
      the cone produced by creation **is** $(p_I)$.
- [ ] Part 2: for an arbitrary diagram $D \colon \mathbf{I} \to \mathcal{A}$, a limit cone on $D$
      is produced, and it is said where each hypothesis is used.
- [ ] Part 3: for an arbitrary diagram $D$ and an **arbitrary** limit cone on $D$, its image is
      shown to be a limit cone (not only the image of the particular limit cone built in
      part 2).
- [ ] No step assumes that $F$ is injective on objects, faithful, or full.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

All three parts are direct proofs in which the definition of creation is applied once to a
well-chosen limit cone in $\mathcal{B}$. Before starting, write the definition of creation as
three separate promises: a lift exists; it is the only lift; it is a limit cone. Each part uses
a different combination of the three.

</details>

<details>
<summary>Hint 2 — part 1</summary>

You are handed a cone in $\mathcal{A}$ and told its image is a limit cone in $\mathcal{B}$.
Apply creation to that image. Creation promises a cone upstairs with certain properties and
says there is only one such. Do you already know a cone upstairs with those properties?

</details>

<details>
<summary>Hint 3 — part 2</summary>

Given $D$, you need a limit cone on $D$, and creation manufactures limit cones upstairs out of
limit cones downstairs. Where does a limit cone downstairs come from?

</details>

<details>
<summary>Hint 4 — part 3</summary>

The limit cone built in part 2 has an image that you know explicitly. But the definition of
preservation quantifies over *all* limit cones on $D$, and a given one need not be the one you
built. Which result from the lecture closes exactly this gap?

</details>

## Check yourself

- In part 1, did you use the uniqueness promise? Did you need $\mathcal{B}$ to have limits?
- In part 3, did you treat an arbitrary limit cone, or only the one from part 2?
- The lecture shows that $U \colon \mathbf{Top} \to \mathbf{Set}$ preserves limits but does not
  reflect them. What does part 1 then tell you about $U$, and does that agree with 5C §4?

## Write it up

Write your proof in `proofs/5c/p06_creation_lemma.md`, then ask Claude to review it.
