# 2B·P04 — Inverse image has a right adjoint

**Type:** core · **Technique:** unit–counit criterion in a poset · **Unlocked by:** `2b_units_counits` §6
**Source:** adapted from Leinster §2.2

## Statement

Let $h \colon K \to L$ be a function between sets. Regard the power sets $\mathscr{P}(K)$ and
$\mathscr{P}(L)$ as posets under $\subseteq$, and let
$h^{*} \colon \mathscr{P}(L) \to \mathscr{P}(K)$ be inverse image,
$h^{*}(T) = \{k \in K : h(k) \in T\}$. Define

$$\forall_h \colon \mathscr{P}(K) \to \mathscr{P}(L), \qquad
\forall_h(S) = \{\, l \in L : \text{every } k \in K \text{ with } h(k) = l \text{ belongs to } S \,\}.$$

Prove that $\forall_h$ is order-preserving and that $h^{*} \dashv \forall_h$, by verifying the unit
and counit inequalities of 2B §6.

(2A showed that direct image is *left* adjoint to $h^{*}$. So $h^{*}$ sits in the middle of a
chain of three, like $U \colon \mathbf{Top} \to \mathbf{Set}$.)

## What you may use

- The boxed criterion of 2B §6: order-preserving maps $f$, $g$ satisfy $f \dashv g$ if and only
  if $a \le g(f(a))$ for all $a$ and $f(g(b)) \le b$ for all $b$.
- That $h^{*}$ is order-preserving (2A §5).
- Elementary set theory: to prove $X \subseteq Y$, take an arbitrary element of $X$ and show it
  lies in $Y$.

## What a complete proof must show

- [ ] It identifies which map plays the role of $f$ (the left adjoint) and which plays $g$, and so which poset each of the two inequalities lives in.
- [ ] $\forall_h$ is shown to be order-preserving.
- [ ] The unit inequality is stated as an inclusion of subsets of the correct set, and proved elementwise.
- [ ] The counit inequality is stated as an inclusion of subsets of the correct set, and proved elementwise.
- [ ] Elements $l \in L$ that are not in the image of $h$ are handled correctly.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Three inclusions between sets, each proved by chasing an element. Before starting, write out
the criterion with $f = h^{*}$ and $g = \forall_h$: the unit inequality is an inclusion between
two subsets of one of $K$, $L$, and the counit inequality an inclusion between two subsets of
the other. Which is which?

</details>

<details>
<summary>Hint 2 — unpacking membership</summary>

Everything rests on being able to say, in one sentence each, what "$k \in h^{*}(T)$" means and
what "$l \in \forall_h(S)$" means. The second is a "for all" statement. To *use* a "for all"
statement you pick an instance; to *prove* one you take an arbitrary instance.

</details>

<details>
<summary>Hint 3 — the two inclusions</summary>

For one of the two inclusions you start with an element $l$ of some $T$ and must prove a "for
all $k$ with $h(k) = l$" statement. For the other you start with an element $k$ and know a
"for all" statement about the point $h(k)$. In the second case, which instance of that "for
all" is the useful one?

</details>

## Check yourself

- If $l \in L$ is not $h(k)$ for any $k$, does $l$ belong to $\forall_h(S)$? Does your proof agree with your answer?
- Is $\forall_h(\emptyset) = \emptyset$ in general? Compute it for $h \colon \{1\} \to \{x, y\}$, $h(1) = x$.
- Describe the closure operator $\forall_h \circ h^{*}$ on $\mathscr{P}(L)$ in words. When is every subset of $L$ closed?
- Compare $\forall_h(S)$ with the direct image of $S$. For which functions $h$ do they always agree?

## Write it up

Write your proof in `proofs/2b/p04_inverse_image_right_adjoint.md`, then ask Claude to review it.
