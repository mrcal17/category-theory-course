# 2C·P05 — Universal arrows compose

**Type:** core · **Technique:** initial-object argument · **Unlocked by:** `2c_universal_arrows` §3
**Source:** adapted from Leinster §2.3

## Statement

Let $G \colon \mathcal{B} \to \mathcal{A}$ and $G' \colon \mathcal{C} \to \mathcal{B}$ be
functors, and let $A$ be an object of $\mathcal{A}$. Suppose

- $(B, u)$ is an initial object of $(A \Rightarrow G)$, so $u \colon A \to G(B)$; and
- $(C, v)$ is an initial object of $(B \Rightarrow G')$, so $v \colon B \to G'(C)$.

Prove that $(C,\; G(v) \circ u)$ is an initial object of $(A \Rightarrow G G')$, where
$G G' \colon \mathcal{C} \to \mathcal{A}$ is the composite functor.

Do **not** assume that $G$ or $G'$ has a left adjoint: only the two universal arrows above are
given.

## What you may use

- The definition of $(A \Rightarrow G)$ and of an initial object in it (2C §3).
- Functoriality of $G$ and $G'$.

## What a complete proof must show

- [ ] $G(v) \circ u$ is checked to be an arrow $A \to GG'(C)$, so that the pair is an object of $(A \Rightarrow GG')$.
- [ ] The goal is unpacked: for every object $C'$ of $\mathcal{C}$ and every $f \colon A \to GG'(C')$, there is exactly one $r \colon C \to C'$ in $\mathcal{C}$ with a stated property.
- [ ] **Existence:** an $r$ is produced, and the stated property is verified for it.
- [ ] **Uniqueness:** any two arrows with the property are shown equal.
- [ ] Each use of initiality names the comma category, the initial object, and the target object (including its arrow component).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Existence and uniqueness of a factorisation, for an arbitrary $(C', f)$. You have two
universal properties to use and they must be used in a particular order, because the output
of one is the input of the other.

</details>

<details>
<summary>Hint 2 — existence: the first step</summary>

The arrow $f \colon A \to GG'(C')$ can be read as an arrow from $A$ to $G$ of *something*.
Of what? That makes a certain pair an object of $(A \Rightarrow G)$. What does initiality of
$(B, u)$ then give you, and in which category does the resulting arrow live?

</details>

<details>
<summary>Hint 3 — existence: the second step</summary>

The arrow you just obtained has domain $B$ and its codomain is $G'$ of something. So it is
the arrow component of an object of which comma category? Use the second universal property,
then verify the required equation using functoriality of $G$.

</details>

<details>
<summary>Hint 4 — uniqueness</summary>

Suppose $r'$ also has the property. To show $r' = r$ you want to use the uniqueness clause
for $(C, v)$, which requires knowing an equation about $G'(r') \circ v$. You know an equation
about $G$ applied to that. Which uniqueness clause lets you remove the $G$?

</details>

## Check yourself

- In the uniqueness part, did you use *both* uniqueness clauses? In which order?
- Did you ever write "the object $G'(C')$ of $(A \Rightarrow G)$"? An object is a pair.
- If $G$ and $G'$ do have left adjoints $F$ and $F'$, what does this result say about $F'F(A)$, and how does it compare with 2A·P04 and 2B·P05?
- In posets: if $b$ is least with $a \le g(b)$ and $c$ is least with $b \le g'(c)$, what does the result claim about $c$? Can you check it by hand?

## Write it up

Write your proof in `proofs/2c/p05_universal_arrows_compose.md`, then ask Claude to review it.
