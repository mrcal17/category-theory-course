# 1E·P06 — Equivalent skeletal categories are isomorphic

**Type:** stretch · **Technique:** building an inverse functor · **Unlocked by:** `1e_equivalence` §3, §4, §6
**Source:** adapted from Riehl §1.5

## Statement

Let $\mathcal{A}$ and $\mathcal{B}$ be **skeletal** categories (in each, isomorphic objects are
equal), and let $F \colon \mathcal{A} \to \mathcal{B}$ be an equivalence. Prove that $F$ is an
isomorphism of categories: there is a functor $G \colon \mathcal{B} \to \mathcal{A}$ with
$G \circ F = 1_{\mathcal{A}}$ and $F \circ G = 1_{\mathcal{B}}$ (equalities, not natural
isomorphisms).

## What you may use

- Theorem 2, "only if" direction (1E §4): an equivalence is full, faithful and essentially surjective on objects.
- Lemma 1 of the lecture (full and faithful functors reflect isomorphisms).
- The definition of skeletal (1E §6) and of isomorphism of categories (1E §1).
- Do **not** assume that the functor $G$ which comes with the equivalence $F$ is the inverse you need; it need not be.

## What a complete proof must show

- [ ] $F$ is injective on objects, with the place where skeletality of $\mathcal{A}$ is used.
- [ ] $F$ is surjective on objects, with the place where skeletality of $\mathcal{B}$ is used.
- [ ] A definition of $G$ on objects and on arrows that leaves no choice to be made.
- [ ] A proof that $G$ is a functor (identities and composition).
- [ ] Both equations $G \circ F = 1_{\mathcal{A}}$ and $F \circ G = 1_{\mathcal{B}}$, each checked on objects and on arrows.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

In 0B, a function has a two-sided inverse exactly when it is a bijection. Aim for the analogous
statement here: show that $F$ is a bijection on objects and a bijection on each hom-set, and
then build $G$ from the inverse bijections. The second part resembles Section 5 of the lecture,
but is simpler, and should need no choices.

</details>

<details>
<summary>Hint 2 — objects</summary>

Essential surjectivity gives "isomorphic to something in the image", and Lemma 1(b) gives
"isomorphic images come from isomorphic objects". Each statement is about isomorphism. What
does the word "skeletal" do to such statements?

</details>

<details>
<summary>Hint 3 — arrows</summary>

Once every object of $\mathcal{B}$ is $F$ of exactly one object of $\mathcal{A}$, an arrow of
$\mathcal{B}$ is an arrow between two objects in the image of $F$. What does "full and
faithful" say about such an arrow?

</details>

<details>
<summary>Hint 4 — functoriality of $G$</summary>

You defined $G(g)$ by a property involving $F$. To show that two arrows built from $G$ are
equal, compare them after applying $F$, as in Step 3 of Section 5. State why the two arrows are
parallel before you conclude.

</details>

## Check yourself

- Did you use the axiom of choice anywhere? You should not have needed it. If you did, find the step and look for the uniqueness statement that removes it.
- Why does this result imply that any two skeletons of the same category are isomorphic? (Which other exercises do you need for that?)
- Where does your argument fail for the equivalence between the walking isomorphism $\mathcal{I}$ and $\mathbf{1}$?

## Write it up

Write your proof in `proofs/1e/p06_skeletal_equivalent_isomorphic.md`, then ask Claude to review it.
