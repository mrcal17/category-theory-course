# 4C·P05 — An exponent law by a Yoneda-style proof

**Type:** core · **Technique:** comparing hom-functors · **Unlocked by:** `4c_yoneda_consequences` §3, §5
**Source:** adapted from Leinster §4.3 and Riehl §2.3

## Statement

For sets $B$ and $C$ write $C^B$ for the set $\mathbf{Set}(B, C)$ of functions from $B$ to $C$.
Let $A$, $B$, $C$ be sets. Prove that

$$(C^B)^A \;\cong\; (C^A)^B$$

by a **Yoneda-style argument**: show that

$$\mathbf{Set}\big(D, (C^B)^A\big) \;\cong\; \mathbf{Set}\big(D, (C^A)^B\big) \qquad \text{naturally in } D \in \mathbf{Set},$$

and then apply a result from the lecture. Do not write down a bijection between $(C^B)^A$ and
$(C^A)^B$ directly.

## What you may use

- From 2A and 3A: for every set $B$ there is a bijection
  $\mathbf{Set}(D \times B, C) \cong \mathbf{Set}(D, C^B)$, natural in $D$ (and in $C$). This is the
  adjunction $(- \times B) \dashv (-)^B$.
- Corollary 3.2 / Corollary 3.3(a) of 4C.
- From 1D: composites and inverses of natural isomorphisms are natural isomorphisms.
- Elementary bijections between products of sets, provided you write them down and check what you
  claim about them.

## What a complete proof must show

- [ ] A chain of bijections from $\mathbf{Set}(D, (C^B)^A)$ to $\mathbf{Set}(D, (C^A)^B)$, with each
      link named.
- [ ] For **each** link, a reason why it is natural in $D$. For links that are instances of the
      adjunction, say what is being substituted for what. For any link that is not, state the
      naturality equation and verify it.
- [ ] A clear statement of which two functors $\mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$ have been
      shown isomorphic.
- [ ] The final step cites a specific corollary and says what it gives.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Follow the recipe in 4C §5. You are comparing the sets of generalized elements of shape $D$ of the
two objects. Each side can be simplified, using the adjunction you are allowed to quote, until no
exponential is left. Simplify both ends towards the middle and see what remains to be bridged.

</details>

<details>
<summary>Hint 2 — using the adjunction twice</summary>

The adjunction turns "a function from $D$ into an exponential" into "a function out of a product
of $D$ with something". After one use, the codomain is still an exponential. What happens to the
domain when you use the adjunction a second time, and what must you substitute for "$D$" in the
quoted bijection when you do?

</details>

<details>
<summary>Hint 3 — the bridge in the middle</summary>

After simplifying both ends you have two hom-sets into $C$ whose domains are two different triple
products built from $D$, $A$ and $B$. There is an evident bijection between those two products.
A bijection between domains induces a bijection between hom-sets by composition. The thing to
check is that this is natural in $D$: write down what a function $g \colon D' \to D$ does to each
triple product, and verify one square.

</details>

<details>
<summary>Hint 4 — naturality of a link that substitutes for $D$</summary>

When you apply "natural in $D$" with $D \times A$ in place of $D$, the function
$g \colon D' \to D$ acts through $g \times 1_A$. Naturality of the quoted bijection holds for
*every* function between the sets substituted, in particular for those of the form $g \times 1_A$.
Say this explicitly at the link where you need it.

</details>

## Check yourself

- Is every functor in your chain contravariant in $D$? (Compare common mistake 5 of the lecture.)
- Did you verify naturality of the middle link, or did you write "this is natural"?
- Unwind your chain for $D = 1$: which explicit bijection $(C^B)^A \to (C^A)^B$ did the Yoneda
  argument produce? Is it the one you would have guessed?

## Write it up

Write your proof in `proofs/4c/p05_exponent_law_by_yoneda.md`, then ask Claude to review it.
