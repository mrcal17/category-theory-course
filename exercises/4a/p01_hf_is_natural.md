# 4A·P01 — $H_f$ is a natural transformation

**Type:** warm-up · **Technique:** dualizing a proof from the lecture · **Unlocked by:** `4a_representables` §3, §5
**Source:** adapted from Leinster §4.1

## Statement

Let $\mathcal{A}$ be a locally small category and $f \colon A \to B$ an arrow of $\mathcal{A}$.
For each object $C$ of $\mathcal{A}$ define a function

$$(H_f)_C \colon \mathcal{A}(C, A) \to \mathcal{A}(C, B), \qquad p \mapsto f \circ p .$$

Prove that the family $\big((H_f)_C\big)_{C \in \mathcal{A}}$ is a natural transformation
$H_f \colon H_A \Rightarrow H_B$ between functors $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$.

## What you may use

- The definition of a category, and the definition of the presheaf $H_A = \mathcal{A}(-, A)$ from 4A §4,
  including its action on arrows.
- The definition of a natural transformation from 1D.
- Proposition 3.1 of 4A as a *model*. You may not quote it as a result: it is about $H^f$, and
  this statement is about $H_f$.

## What a complete proof must show

- [ ] It states the naturality equation for this situation with all quantifiers: for which arrows
      $g$, with which domain and codomain, and for which elements $p$ of which set.
- [ ] It says where each of the four functions in the naturality square goes from and to, and the
      directions are correct for functors on $\mathcal{A}^{\mathrm{op}}$.
- [ ] Both sides of the equation are computed from the definitions, one step at a time.
- [ ] The step that makes the two sides equal is justified by a named axiom.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a direct proof that two functions are equal: pick an arbitrary element of the common
domain and compute both sides. Before computing anything, write down the naturality equation.
The functors are contravariant, so decide carefully which way an arrow $g$ of $\mathcal{A}$ must
point for $H_A(g)$ to have domain $\mathcal{A}(C, A)$.

</details>

<details>
<summary>Hint 2 — draw the square</summary>

Draw the naturality square with the four hom-sets at its corners. Two of its sides are
"compose with $f$" and the other two are "compose with $g$". On which side of $p$ does each of
them compose? Write the domain and codomain of every arrow involved before you compose anything.

</details>

<details>
<summary>Hint 3 — compare with the lecture</summary>

Put your square next to the one drawn for Proposition 3.1 in 4A. What single axiom finished that
proof? Does your computation end in the same kind of expression?

</details>

## Check yourself

- Is your arrow $g$ an arrow $D \to C$ or $C \to D$? Does $H_A(g)$ then go the way you used it?
- Did you ever apply an arrow of $\mathcal{A}$ to an "element of $A$"? There are none.
- Could you now write out, without looking, why $H_\bullet$ is covariant while $H^\bullet$ is contravariant?

## Write it up

Write your proof in `proofs/4a/p01_hf_is_natural.md`, then ask Claude to review it.
