# 5C·P02 — A functor that does not preserve products

**Type:** warm-up · **Technique:** counterexample to preservation · **Unlocked by:** `5c_functors_and_limits` §2
**Source:** adapted from Leinster §5.3

## Statement

Let $C$ be a set with at least two elements. Define a functor $F \colon \mathbf{Set} \to \mathbf{Set}$ by

$$F(X) = X \times C, \qquad F(f)(x, c) = (f(x), c) \quad\text{for } f \colon X \to Y .$$

(You may take for granted that $F$ is a functor.) Prove:

1. $F$ does not preserve terminal objects;
2. $F$ does not preserve binary products.

## What you may use

- The definition of "preserves limits of shape $\mathbf{I}$" (5C §2), for the empty shape and for
  the two-object discrete shape.
- Products and terminal objects in $\mathbf{Set}$ (5A §1), and the uniqueness of limits
  (5A §5) if you want it.
- Elementary facts about functions between sets.

## What a complete proof must show

- [ ] For part 1: a terminal object of $\mathbf{Set}$ is named, its image under $F$ is computed,
      and it is *proved* that the image is not terminal.
- [ ] For part 2: specific sets $X$ and $Y$ and a specific product cone on them are named; the
      image cone (vertex and both legs) is computed.
- [ ] For part 2: a specific test cone is exhibited for which the image cone fails the
      universal property, and it is said which half fails (existence or uniqueness) and why.
- [ ] The argument works for every $C$ with at least two elements, including infinite $C$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

To refute "for every limit cone, the image is a limit cone" you need one limit cone whose image
is not a limit cone. And to show a cone is not a limit cone you need one test cone for which
the mediating map fails to exist or fails to be unique. So each part ends with a very concrete
object: a set and one or two functions.

</details>

<details>
<summary>Hint 2 — keep it small</summary>

You are free to choose $X$ and $Y$. The smaller they are, the easier the image cone is to
describe. What are the smallest non-empty sets? Write down the image cone for your choice:
what is its vertex, up to an evident bijection, and what do its two legs do?

</details>

<details>
<summary>Hint 3 — which half fails?</summary>

Look at the two legs of the image cone you found in Hint 2. If a map $g$ into the vertex
satisfies both equations of the universal property, what does that force about the two legs of
the test cone? Now choose a test cone that violates this. Where do you use that $C$ has two
different elements?

</details>

## Check yourself

- Did you show the image *cone* fails, or only that two sets have different sizes? A counting
  argument does not cover infinite $C$: there $C$ and $C \times C$ have the same cardinality.
- In part 2, which half of the universal property failed?
- Describe the comparison map $F(X \times Y) \to F(X) \times F(Y)$ of 5C §1 for this $F$. Is it
  injective? Surjective?

## Write it up

Write your proof in `proofs/5c/p02_product_with_c_fails.md`, then ask Claude to review it.
