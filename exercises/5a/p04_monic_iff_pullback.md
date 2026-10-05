# 5A·P04 — Monic if and only if a square is a pullback

**Type:** core · **Technique:** translating between two definitions · **Unlocked by:** `5a_limits` §3, §8
**Source:** adapted from Leinster §5.1

## Statement

Let $f \colon X \to Y$ be a map in a category $\mathcal{A}$. Prove that $f$ is monic if and only
if the square

```
X --1_X--> X
|          |
1_X        f
v          v
X ---f---> Y
```

is a pullback square. In the notation of 5A §3: the two maps being pulled back are
$s = f$ and $t = f$, the candidate pullback object is $P = X$, and the candidate projections are
$p_1 = p_2 = 1_X$.

## What you may use

- The definition of a pullback (5A §3) and of monic (1B).
- The axioms of a category.
- Nothing about elements, and not Proof 9 of the lecture (it is about a different square).

## What a complete proof must show

- [ ] Two directions, each under its own heading.
- [ ] In "monic $\Rightarrow$ pullback": the square commutes; for arbitrary test data
      $(A, f_1, f_2)$ with $f f_1 = f f_2$, existence of a mediating map and its uniqueness are
      each proved.
- [ ] In "pullback $\Rightarrow$ monic": arbitrary $h, k \colon A \to X$ with $f h = f k$ are
      fixed, and the pullback property is applied to explicitly named test data.
- [ ] Every use of an identity law is justified by name.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Write the definition of "this square is a pullback" with $p_1 = p_2 = 1_X$ substituted in and
every identity simplified away. Do the same for the definition of monic. Put the two side by
side before proving anything. Most of the work is in seeing how similar they are.

</details>

<details>
<summary>Hint 2 — monic implies pullback</summary>

The test data are $f_1, f_2 \colon A \to X$ with $f f_1 = f f_2$. What does the hypothesis on
$f$ tell you about $f_1$ and $f_2$? Once you know that, what do the two equations
$1_X \circ \bar{f} = f_1$ and $1_X \circ \bar{f} = f_2$ leave you free to choose?

</details>

<details>
<summary>Hint 3 — pullback implies monic</summary>

You are given $h, k$ with $f h = f k$. Test data for the pullback are an object and two maps
into $X$ satisfying one equation. What do you already have that fits? The pullback property
then hands you a map satisfying two equations. Read those two equations slowly.

</details>

<details>
<summary>Hint 4 — a common slip</summary>

In the direction "pullback $\Rightarrow$ monic", which half of the universal property did you
use: existence or uniqueness? Make sure your write-up names the right one. In the other
direction you need both.

</details>

## Check yourself

- In $\mathbf{Set}$, the pullback of $f$ along itself is $\{(x, x') : f(x) = f(x')\}$. What does
  your theorem say about this set when $f$ is injective?
- Did the direction "pullback $\Rightarrow$ monic" need uniqueness of the mediating map?
- This result is used in 5C·P03. Can you guess the statement?

## Write it up

Write your proof in `proofs/5a/p04_monic_iff_pullback.md`, then ask Claude to review it.
