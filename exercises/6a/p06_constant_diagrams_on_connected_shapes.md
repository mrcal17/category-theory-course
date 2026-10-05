# 6A·P06 — Constant diagrams on a connected shape

**Type:** stretch · **Technique:** induction along a zigzag, then re-expressing a universal property · **Unlocked by:** `6a_limits_representables_adjoints` §1, §6
**Source:** adapted from Leinster §6.1 and Riehl §3.4

## Statement

A small category $\mathbf{I}$ is **connected** if it has at least one object and, for every pair of
objects $I, J$, there is a finite sequence of objects $I = I_0, I_1, \ldots, I_n = J$ such that for
each $k = 1, \ldots, n$ there is a map $I_{k-1} \to I_k$ or a map $I_k \to I_{k-1}$ (a *zigzag*; the
maps may point either way).

Let $\mathbf{I}$ be a connected small category, $\mathcal{A}$ a category, and
$\Delta \colon \mathcal{A} \to [\mathbf{I}, \mathcal{A}]$ the diagonal functor.

1. Let $A, B$ be objects of $\mathcal{A}$ and $(f_I \colon B \to A)_{I \in \mathbf{I}}$ a cone on the
   constant diagram $\Delta A$. Prove that $f_I = f_J$ for all objects $I, J$ of $\mathbf{I}$.
2. Prove that the cone on $\Delta A$ with vertex $A$ and every component equal to $1_A$ is a limit
   cone.
3. Prove that $\Delta$ is full and faithful.
4. Show that neither half of "connected" can be dropped: take $\mathcal{A} = \mathbf{Set}$ and find a
   set $A$ for which the cone of part 2 is not a limit cone when $\mathbf{I}$ is the discrete
   category with two objects, and say what goes wrong in part 2 when $\mathbf{I}$ is empty.

## What you may use

- Lemma 1 of the lecture (cones are natural transformations out of a constant functor) and the definition of $\Delta$ on objects and maps; brief P01 (that $\Delta$ is a functor).
- The definition of a limit cone (5A) and of full and faithful (1C).
- Induction on the length of a zigzag.
- For part 4, the description of products and of the terminal object in $\mathbf{Set}$ (5A).

## What a complete proof must show

- [ ] In part 1: what the cone condition says for a single map $u$ of $\mathbf{I}$ when the diagram is constant, and an induction (or an equally explicit argument) that carries this along a zigzag whose maps point in both directions.
- [ ] In part 2: existence and uniqueness of the mediating map, with the place where "at least one object" is used pointed out in each half where it is needed.
- [ ] In part 3: for arbitrary objects $B, A$, that $g \mapsto \Delta g$ is injective and surjective from $\mathcal{A}(B, A)$ to the natural transformations $\Delta B \Rightarrow \Delta A$.
- [ ] In part 4: a specific set, a specific cone with no mediating map or with more than one, and a separate sentence for the empty shape.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is the engine and the other parts are read off from it. Before thinking about zigzags,
write down the cone condition on $\Delta A$ at one map $u \colon I \to J$. What does $\Delta A$ do
to $u$?

</details>

<details>
<summary>Hint 2 — the zigzag</summary>

A zigzag has maps pointing forwards and backwards. Does the conclusion you drew in Hint 1 care
which way the map points? State the claim you will prove by induction on $n$ so that it mentions
only the two ends of the zigzag.

</details>

<details>
<summary>Hint 3 — parts 2 and 3</summary>

After part 1, a cone on $\Delta A$ with vertex $B$ carries much less information than a family of
maps. How much? Compare that with the set of maps $B \to A$, and with what a natural
transformation $\Delta B \Rightarrow \Delta A$ is by Lemma 1. Where do you need $\mathbf{I}$ to have
an object in order to name a map at all?

</details>

<details>
<summary>Hint 4 — part 4</summary>

For the two-object discrete shape, what is a cone on $\Delta A$ with vertex $B$, with no
conditions to satisfy? You already know what the limit of that diagram is in $\mathbf{Set}$; count
elements. For the empty shape, ask which object a limit of the empty diagram must be.

</details>

## Check yourself

- Did your induction handle a step in which the map points from $I_k$ back to $I_{k-1}$?
- Parts 2 and 3 are two ways of saying one thing. Can you derive part 3 from part 2 using Theorem 1 of the lecture?
- When $\mathcal{A}$ has limits of shape $\mathbf{I}$, what does part 2 say about the unit of the adjunction $\Delta \dashv \lim$?
- A group regarded as a one-object category is connected. What does part 3 say about sets with trivial action?

## Write it up

Write your proof in `proofs/6a/p06_constant_diagrams_on_connected_shapes.md`, then ask Claude to review it.
