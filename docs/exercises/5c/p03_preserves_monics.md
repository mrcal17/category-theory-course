# 5C·P03 — Pullback-preserving functors preserve monics

**Type:** core · **Technique:** converting a property into a limit · **Unlocked by:** `5c_functors_and_limits` §2; `5a_limits` §8
**Source:** adapted from Leinster §5.3

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor that preserves pullbacks (that is,
preserves limits of the shape $\bullet \to \bullet \leftarrow \bullet$). Prove that $F$ preserves
monics: if $m \colon X \to Y$ is monic in $\mathcal{A}$, then $F m \colon F X \to F Y$ is monic in
$\mathcal{B}$.

## What you may use

- The definition of "preserves limits of shape $\mathbf{I}$" (5C §2).
- The statement of 5A·P04, in both directions: a map $f$ is monic if and only if the square with
  $1, 1$ on two sides and $f, f$ on the other two is a pullback.
- The description of a pullback as a limit (5A §4): a cone on $X \xrightarrow{s} Z \xleftarrow{t} Y$
  has three legs, and the leg to $Z$ is determined by either of the other two.
- Functors preserve identities and composites (1C).

## What a complete proof must show

- [ ] A specific pullback square in $\mathcal{A}$ is named, with a reason why it is a pullback.
- [ ] The hypothesis on $F$ is applied to it, and the image square in $\mathcal{B}$ is written
      out with every object and arrow identified.
- [ ] It is explained why the image square is the *particular* square that 5A·P04 is about (this
      needs a fact about what $F$ does to identities).
- [ ] The conclusion is drawn using the correct direction of 5A·P04.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

"Monic" is defined by a quantifier over all pairs of maps into $X$, and a functor gives you no
direct handle on maps into $F X$ that do not come from $\mathcal{A}$. So do not attack the
definition of monic head on. The hypothesis on $F$ is about limits; is there a way to say
"$m$ is monic" as a statement about a limit?

</details>

<details>
<summary>Hint 2 — the chain</summary>

The proof is a chain of three implications: a fact about $m$ in $\mathcal{A}$, then a fact
about a square in $\mathcal{A}$, then a fact about a square in $\mathcal{B}$, then a fact about
$F m$ in $\mathcal{B}$. Write the four statements down before justifying the arrows between
them.

</details>

<details>
<summary>Hint 3 — squares versus cones</summary>

The definition of preservation is phrased with cones (one leg for each of the three objects of
the shape), while 5A·P04 is phrased with squares (two projections). Be explicit about how you
pass between the two descriptions, in $\mathcal{A}$ and again in $\mathcal{B}$.

</details>

## Check yourself

- Where did you use $F(1_X) = 1_{FX}$?
- State the dual result. Which exercise of 5B does its proof quote?
- The forgetful functor $\mathbf{Grp} \to \mathbf{Set}$ preserves limits. What does your theorem
  then say about monics in $\mathbf{Grp}$?

## Write it up

Write your proof in `proofs/5c/p03_preserves_monics.md`, then ask Claude to review it.
