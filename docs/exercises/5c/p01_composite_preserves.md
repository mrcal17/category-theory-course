# 5C·P01 — Composites of limit-preserving functors

**Type:** warm-up · **Technique:** unpacking a definition twice · **Unlocked by:** `5c_functors_and_limits` §1, §2
**Source:** adapted from Leinster §5.3

## Statement

Let $\mathbf{I}$ be a small category and let $F \colon \mathcal{A} \to \mathcal{B}$ and
$G \colon \mathcal{B} \to \mathcal{C}$ be functors, each of which preserves limits of shape
$\mathbf{I}$. Prove that the composite $G \circ F \colon \mathcal{A} \to \mathcal{C}$ preserves
limits of shape $\mathbf{I}$.

## What you may use

- The definition of "preserves limits of shape $\mathbf{I}$" (5C §2).
- The definition of the composite of two functors (1C), including how it acts on arrows.
- Proof 1 of the lecture (functors send cones to cones), if you need it.

## What a complete proof must show

- [ ] The statement to be proved is written out with its quantifiers: which diagram, which cone,
      what is assumed about the cone, what must be concluded.
- [ ] It is said explicitly which diagram in $\mathcal{B}$ the hypothesis on $G$ is applied to,
      and why that diagram has shape $\mathbf{I}$.
- [ ] It is said explicitly which cone the hypothesis on $G$ is applied to, and why that cone is
      a limit cone.
- [ ] The cone obtained at the end is identified with the cone the definition asks about
      (same vertex, same legs, same diagram).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

A direct proof by unpacking. Start with "Let $D \colon \mathbf{I} \to \mathcal{A}$ be a diagram
and let $(p_I)$ be a limit cone on $D$", and finish with a sentence of the form "so ... is a
limit cone on ...". Fill in the conclusion before you fill in the middle.

</details>

<details>
<summary>Hint 2 — two applications</summary>

You have two hypotheses and each is an implication of the form "if this cone is a limit cone,
then that cone is a limit cone". The output of one should be the input of the other. In which
order?

</details>

<details>
<summary>Hint 3 — the bookkeeping</summary>

The definition of preservation for $G \circ F$ talks about the diagram $(G \circ F) \circ D$ and
the legs $(G \circ F)(p_I)$. Your argument will naturally produce the diagram
$G \circ (F \circ D)$ and the legs $G(F(p_I))$. Say why these are the same.

</details>

## Check yourself

- Did you use any property of limits at all, or only the two hypotheses? (Which should it be?)
- Does the same argument show that a composite of functors that *reflect* limits reflects
  limits? In which order would the two hypotheses be used?
- Is the identity functor limit-preserving? Where would you use that fact together with this one?

## Write it up

Write your proof in `proofs/5c/p01_composite_preserves.md`, then ask Claude to review it.
