# 3A·P03 — Functions out of a sum

**Type:** core · **Technique:** explicit bijection, case analysis · **Unlocked by:** `3a_sets_and_size` §2, §3
**Source:** adapted from Leinster §3.1

## Statement

Let $A$, $B$, $C$ be sets, and let $i_1 \colon A \to A + B$ and $i_2 \colon B \to A + B$ be the
inclusions into the sum. Prove that the function
$$\Theta \colon C^{A + B} \to C^A \times C^B, \qquad \Theta(h) = (h \circ i_1,\ h \circ i_2),$$
is a bijection.

(For finite sets this is the law of exponents $c^{\,a + b} = c^{\,a} \cdot c^{\,b}$.)

## What you may use

- The definition of the sum $A + B = (A \times \{1\}) \cup (B \times \{2\})$ and of $i_1$, $i_2$ (3A §2), including: every element of $A + B$ is $i_1(a)$ for exactly one $a \in A$ or $i_2(b)$ for exactly one $b \in B$, and not both.
- The definition of a product of sets and of a function set (3A §2, §3).
- A function is a bijection if and only if it has a two-sided inverse (0B).
- You may **not** quote item 2 of the reading list in §2 (the universal property of the sum) as known: that is what this exercise proves.

## What a complete proof must show

- [ ] A function $\Psi \colon C^A \times C^B \to C^{A+B}$, defined by cases, with a sentence explaining why the definition by cases is legitimate (each element falls under exactly one case).
- [ ] $\Theta \circ \Psi$ is the identity: an equality of pairs of functions, each component checked on elements.
- [ ] $\Psi \circ \Theta$ is the identity: an equality of functions $A + B \to C$, checked at an arbitrary element of $A + B$, which means in two cases.
- [ ] No counting argument.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Same shape as Proposition 2 of the lecture: exhibit an inverse and check both composites. The
section on products in §2 ("Checking item 1") does the mirror-image statement for functions
*into* a product; read it again and note what plays the role of the projections here.

</details>

<details>
<summary>Hint 2 — the inverse</summary>

You are handed a pair $(f, g)$ with $f \colon A \to C$ and $g \colon B \to C$ and must produce
one function on $A + B$. An element of $A + B$ carries a tag. What should the function do with
the tag?

</details>

<details>
<summary>Hint 3 — where care is needed</summary>

A definition by cases is only a definition if the cases cover everything and do not overlap.
Which sentence of the definition of $A + B$ guarantees each of these? Would your $\Psi$ still be
well defined if $A \cup B$ were used in place of $A + B$ and $A$, $B$ had an element in common?

</details>

## Check yourself

- Did you check both composites, and was each check an equality of the correct kind of object?
- Where exactly did you use that the two copies of $A$ and $B$ inside $A + B$ are disjoint?
- Put $A = B = 1$. What does the bijection say, in words?

## Write it up

Write your proof in `proofs/3a/p03_functions_out_of_a_sum.md`, then ask Claude to review it.
