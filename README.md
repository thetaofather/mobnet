# The Taofather’s MobNet: Turning dTAO Volatility Into a Mafia-Style Hit
---

## Table of Contents

- [Abstract](#abstract)
- [High-Level Overview](#high-level-overview)
  - [Roles](#roles)
  - [The MOB-α Token](#the-mob-α-token)
- [Hit Mechanics](#hit-mechanics)
  - [1. Boss Deposit & Hit Creation](#1-boss-deposit--hit-creation)
  - [2. Pool Filling (Mobsters / Miners Join)](#2-pool-filling-mobsters--miners-join)
  - [3. Hit Execution (One-Shot Sell)](#3-hit-execution-one-shot-sell)
  - [4. Base Payouts & Fee](#4-base-payouts--fee)
- [Impact Scoring](#impact-scoring)
  - [Price Shock](#price-shock)
  - [Normalized Shock](#normalized-shock)
  - [Size-Adjusted Impact](#size-adjusted-impact)
- [Emissions & MOB-α Rewards](#emissions--mob-α-rewards)
  - [Epoch Reward Budget](#epoch-reward-budget)
  - [Allocating Rewards to Hits](#allocating-rewards-to-hits)
  - [Allocating Rewards Within a Hit](#allocating-rewards-within-a-hit)
  - [Making Hits Slightly +EV vs Solo Selling](#making-hits-slightly-ev-vs-solo-selling)
- [Boss Collateral & Burns](#boss-collateral--burns)
- [Worked Example: “The 10k Hit on Subnet 1”](#worked-example-the-10k-hit-on-subnet-1)
  - [Setup](#setup)
  - [Boss Deposit Breakdown](#boss-deposit-breakdown)
  - [Pool, Price, and Base Payouts](#pool-price-and-base-payouts)
  - [Impact & Boss Collateral](#impact--boss-collateral)
  - [Emissions-Funded MOB-α Rewards](#emissions-funded-mob-α-rewards)
  - [Comparing Hit vs Solo Selling](#comparing-hit-vs-solo-selling)
- [Value Proposition](#value-proposition)
  - [For The Subnet Owner (“The Taofather”)](#for-the-subnet-owner-the-taofather)
  - [For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)](#for-users-bosses-mobsters--miners-consiglieres--validators)
- [FAQ](#faq)
- [License / Use](#license--use)

---

## Abstract

MobNet is a **mafia-themed** subnet concept for Bittensor where **volatility is the product**.

Its native token, **MOB-α** (“Mob Alpha”), powers an underworld of **hits** on other subnets:

- **Bosses** open hits by burning and locking MOB-α.  
- **Mobsters (Miners)** join hits by contributing the **target subnet’s alpha token** into a pooled stack.  
- When the pool fills, the system executes a **single, all-at-once sell event** (“the hit”), generating a payout pot and a price shock.

An **impact score** measures how brutal the hit was and determines:

- how much of the Boss’s locked MOB-α is **washed and returned** vs **burned**,  
- how much **MOB-α and base payout** each Mobster / miner earns,  
- and how the hit ranks on a public **Hit Board**.

Critically, MobNet assumes the subnet dedicates **100% of its miner emissions share** (e.g. the full 41% miner allocation) to **MOB-α rewards for miners (Mobsters) who participate in hits**. Parameters are tuned so that:

> Over time, **Mobsters / miners usually earn slightly more** by joining hits than by selling alone.

This README describes the MobNet idea as **fictional game design**, not as a real protocol.

---

## High-Level Overview

MobNet lives in an imagined “Tensor City” of Bittensor subnets. Each subnet has:

- an **alpha token** (e.g. `α₁` for Subnet 1),  
- a **reputation**,  
- and a **target on its back**.

MobNet is the **underworld layer** where those alpha tokens become instruments in a game of coordination, timing, and clout.

### Roles

- **Bosses (Hit Sponsors)**  
  Open hits on specific subnets by depositing MOB-α and defining the hit parameters.

- **Mobsters (Miners)**  
  Miners on MobNet. They join hits by depositing the target subnet’s alpha into hit pools. They are scored and rewarded by validators (Consiglieres) for effective participation in hits and for holding MOB-α.

- **Consiglieres (Validators)**  
  Validators on MobNet. They:
  - track internal prices and subnet sizes,  
  - compute impact scores for hits,  
  - score and weight miners (Mobsters),  
  - and drive consensus on how emissions and collateral are allocated.

There is no external “oracle layer” in this document; all measurement and scoring is conceptually handled by the **validator set (Consiglieres)**.

### The MOB-α Token

MOB-α is the underworld’s currency:

- Bosses **must acquire and deposit MOB-α** to open hits.  
- A fixed fraction of each deposit is **burned**; another is held as **collateral**.  
- The subnet’s **miner emissions** are recycled into MOB-α rewards for **miners (Mobsters)** who participate in hits.

The more the game is played, the more MOB-α is **burned**, while emissions keep the system **slightly +EV** for active miners.

---

## Hit Mechanics

### 1. Boss Deposit & Hit Creation

A Boss targets subnet \(T\) (e.g. **Subnet 1**) and defines:

- Hit pool size \(Q_T\): total units of subnet \(T\)’s alpha to be collected.  
- MOB-α deposit \(A_{\text{boss}}\).

The Boss’s deposit is split:

- **Instant burn (20%)**

  $$
  A_{\text{burn,instant}} = 0.20 \, A_{\text{boss}}
  $$

- **Collateral / Escrow (70%)**

  $$
  A_{\text{esc}} = 0.70 \, A_{\text{boss}}
  $$

- **Treasury (10%)**

  $$
  A_{\text{treasury}} = 0.10 \, A_{\text{boss}}
  $$

The hit is posted on the **Hit Board** as an open contract: target subnet \(T\), pool size \(Q_T\), Boss, timing, etc.

---

### 2. Pool Filling (Mobsters / Miners Join)

Mobsters (the subnet’s **miners**) join by depositing the target subnet’s alpha token.

For Mobster / miner \(i\):

- Deposit:

  $$
  d_i \quad \text{(units of subnet } T \text{ alpha)}
  $$

The total pool:

$$
Q_T = \sum_i d_i
$$

When \(Q_T\) reaches the Boss’s specified pool size (or a timeout), the hit is **armed**.

---

### 3. Hit Execution (One-Shot Sell)

When the hit fires (as validated and executed under the validators’ rules):

- The entire pool \(Q_T\) of subnet \(T\)’s alpha is sold in one atomic operation into **House TAO** (the quote asset in this model).
- The operation yields total proceeds:

  $$
  V_{\text{hit}} \quad \text{(in House TAO)}
  $$

- The internal price of subnet \(T\)’s alpha moves from \(P_0\) (before) to \(P_1\) (after).

This atomic sale is the **hit**.

---

### 4. Base Payouts & Fee

A protocol fee \(f \in [0.01, 0.03]\) is applied:

- **Fee:**

  $$
  V_{\text{fee}} = f \cdot V_{\text{hit}}
  $$

- **Payout pool for Mobsters / miners:**

  $$
  V_{\text{mob}} = (1 - f) \cdot V_{\text{hit}}
  $$

Mobster / miner \(i\)’s share of the pool is proportional to their contribution:

$$
\text{Payout}_{i,\text{base}} = V_{\text{mob}} \cdot \frac{d_i}{\sum_j d_j}
$$

On base payouts alone, miners may receive **slightly less** than an ideal, fee-free solo sell due to:

- protocol fee \(f\), and  
- slippage from a big one-shot sale.

This is intentionally offset by emissions-funded MOB-α rewards.

---

## Impact Scoring

Impact scoring turns a mechanical sell into a **ranked event**. Validators (Consiglieres) are responsible for computing and agreeing on these metrics.

### Price Shock

Before vs after the hit:

- Pre-hit price: \(P_0\)  
- Post-hit price: \(P_1\)

Relative price drop:

$$
\Delta P = \frac{P_0 - P_1}{P_0}
$$

---

### Normalized Shock

Define a **max meaningful drop** \(\Delta P_{\max}\) (e.g. 0.3–0.5).

Normalized shock:

$$
I_{\text{hit}} = \min\left(1, \max\left(0, \frac{\Delta P}{\Delta P_{\max}}\right)\right)
$$

- \(I_{\text{hit}} \approx 0\): negligible move.  
- \(I_{\text{hit}} \approx 1\): at or beyond the modeled maximum.

---

### Size-Adjusted Impact

Let \(S_T\) represent the **size** of subnet \(T\) (liquidity, market cap proxy, etc.), as tracked/estimated by validators.

The size-adjusted impact score:

$$
I'_{\text{hit}} = I_{\text{hit}} \cdot \frac{Q_T}{S_T + \epsilon}
$$

where \(\epsilon > 0\) avoids division by zero.

- Large pool vs small subnet → high \(I'_{\text{hit}}\).  
- Small pool vs huge subnet → low \(I'_{\text{hit}}\).

Validators use \(I'_{\text{hit}}\) as the main metric to:

- rank hits on the Hit Board, and  
- resolve Boss collateral and emission allocations.

---

## Emissions & MOB-α Rewards

### Epoch Reward Budget

Assume MobNet receives miner emissions each epoch and dedicates **100% of its miner share** to rewarding its own miners (Mobsters) for hit participation.

Let:

- \(E_{\text{miner,epoch}}\) be the subnet’s miner emissions in TAO-equivalent.  
- After conversion / accounting, define a **MOB-α reward budget**:

  $$
  E_{\text{rewards,epoch}} \quad (\text{MOB-}\alpha)
  $$

This is the epoch’s **Hit Rewards Pool**, governed by validators.

---

### Allocating Rewards to Hits

For each hit \(h\) in an epoch:

- Hit volume in TAO: \(V_{\text{hit},h}\)  
- Impact score: \(I'_{\text{hit},h}\)  
- Total epoch volume: \(V_{\text{total}} = \sum_k V_{\text{hit},k}\)

A simple allocation (chosen by validator logic / governance):

$$
E_{\text{hit},h}
= E_{\text{rewards,epoch}} \cdot
\frac{V_{\text{hit},h}}{V_{\text{total}}}
\cdot \left( 1 + \kappa \cdot I'_{\text{hit},h} \right)
$$

where \(\kappa \in [0, 0.3]\) boosts rewards for high-impact hits.

Normalize if necessary so:

$$
\sum_h E_{\text{hit},h} = E_{\text{rewards,epoch}}
$$

---

### Allocating Rewards Within a Hit

For a specific hit with reward pool \(E_{\text{hit}}\) MOB-α:

- Contribution share of miner \(i\):

  $$
  c_i = \frac{d_i}{\sum_j d_j}
  $$

- Loyalty share based on MOB-α holdings \(H_i\):

  $$
  \ell_i = \frac{H_i}{\sum_j H_j}
  $$

Define weight (validators can tune \(\gamma,\delta\)):

$$
w_i = c_i^{\gamma} \cdot \ell_i^{\delta}
$$

with exponents:

- \(\gamma \in [0.8, 1.2]\): how strongly to reward **bigger contributors**.  
- \(\delta \in [0.3, 1.0]\): how strongly to reward **MOB-α holders**.

Miner \(i\)’s MOB-α reward:

$$
R_i = E_{\text{hit}} \cdot \frac{w_i}{\sum_k w_k}
$$

---

### Making Hits Slightly +EV vs Solo Selling

Compare:

- **Solo selling**: Miner \(i\) sells \(d_i\) of target alpha at effective solo price \(P_{\text{solo}}\):

  $$
  \text{Solo}_i \approx P_{\text{solo}} \cdot d_i
  $$

- **Joining a hit**: Miner \(i\) receives:

  $$
  \text{Hit}_i \approx \text{Payout}_{i,\text{base}} + p_\alpha \cdot R_i
  $$

  where \(p_\alpha\) is a notional TAO value per MOB-α.

Validator/governance choices over:

- fee \(f\),  
- emission budget \(E_{\text{rewards,epoch}}\), and  
- allocation schemes,

can aim for:

$$
\mathbb{E}[\text{Hit}_i] \gtrsim \mathbb{E}[\text{Solo}_i]
$$

i.e. **joining hits is slightly better (in expectation) than selling solo**, especially for miners who hold MOB-α.

---

## Boss Collateral & Burns

Recall:

- Collateral (escrow): \(A_{\text{esc}} = 0.70 A_{\text{boss}}\).

Define a **minimum return fraction** \(\beta_{\min} \in [0.3, 0.6]\).

Boss collateral returned:

$$
A_{\text{returned}}
= A_{\text{esc}} \cdot
\left( \beta_{\min} + (1 - \beta_{\min}) \cdot \min(1, I'_{\text{hit}}) \right)
$$

- If \(I'_{\text{hit}} \approx 0\): Boss recovers about \(\beta_{\min} A_{\text{esc}}\).  
- If \(I'_{\text{hit}} \approx 1\): Boss recovers nearly all of \(A_{\text{esc}}\).

Remainder:

$$
A_{\text{burn/treasury}} = A_{\text{esc}} - A_{\text{returned}}
$$

can be split between burns and treasury (as decided via validator/governance).

**Total MOB-α burned per hit** (if all remainder is burned):

$$
A_{\text{burn,total}}
= A_{\text{burn,instant}} + (A_{\text{esc}} - A_{\text{returned}})
= 0.20 A_{\text{boss}} + (A_{\text{esc}} - A_{\text{returned}})
$$

Every hit:

- Always burns at least 20% of Boss deposit.  
- Burns **extra** when hits are underpowered (low \(I'_{\text{hit}}\)).

---

## Worked Example: “The 10k Hit on Subnet 1”

This example uses **Subnet 1** with alpha token \(\alpha_1\).

### Setup

- Target subnet: **Subnet 1**, token \(\alpha_1\).  
- Boss deposit: \(A_{\text{boss}} = 1{,}000\) MOB-α.  
- Hit pool size: \(Q_{1} = 10{,}000\) \(\alpha_1\).  
- Protocol fee: \(f = 0.02\) (2%).  
- Subnet size parameter: \(S_{1} = 20{,}000\) \(\alpha_1\).  
- Maximum meaningful drop: \(\Delta P_{\max} = 0.5\) (50%).  
- Minimum Boss return fraction: \(\beta_{\min} = 0.4\).  
- Notional MOB-α value: \(p_\alpha = 0.1\) TAO per MOB-α (for intuition).

Three **Mobsters / miners**:

- Alice:  
  - Deposit \(d_A = 5{,}000\) \(\alpha_1\)  
  - Holdings \(H_A = 400\) MOB-α  
- Boris:  
  - Deposit \(d_B = 3{,}000\) \(\alpha_1\)  
  - Holdings \(H_B = 300\) MOB-α  
- Cara:  
  - Deposit \(d_C = 2{,}000\) \(\alpha_1\)  
  - Holdings \(H_C = 300\) MOB-α  

Total holdings:

$$
H_{\text{tot}} = H_A + H_B + H_C = 1{,}000 \text{ MOB-}\alpha
$$

---

### Boss Deposit Breakdown

Boss deposits \(1{,}000\) MOB-α:

- Instant burn:

  $$
  A_{\text{burn,instant}} = 0.20 \cdot 1{,}000 = 200 \text{ MOB-}\alpha
  $$

- Escrow:

  $$
  A_{\text{esc}} = 0.70 \cdot 1{,}000 = 700 \text{ MOB-}\alpha
  $$

- Treasury:

  $$
  A_{\text{treasury}} = 0.10 \cdot 1{,}000 = 100 \text{ MOB-}\alpha
  $$

---

### Pool, Price, and Base Payouts

Total pool:

$$
Q_1 = d_A + d_B + d_C = 10{,}000 \, \alpha_1
$$

Assume:

- Pre-hit price: \(P_0 = 0.20\) TAO / \(\alpha_1\).  
- After the big sell, price drops to \(P_1 = 0.09\) TAO / \(\alpha_1\).  
- Actual proceeds (slippage etc): \(V_{\text{hit}} = 1{,}000\) TAO (avg price 0.10).

Fee:

$$
V_{\text{fee}} = f \cdot V_{\text{hit}} = 0.02 \cdot 1{,}000 = 20 \text{ TAO}
$$

Payout pool:

$$
V_{\text{mob}} = (1 - f) \cdot V_{\text{hit}} = 980 \text{ TAO}
$$

Contribution shares:

- Alice: \(c_A = 5{,}000 / 10{,}000 = 0.50\)  
- Boris: \(c_B = 3{,}000 / 10{,}000 = 0.30\)  
- Cara: \(c_C = 2{,}000 / 10{,}000 = 0.20\)

Base payouts:

- Alice:

  $$
  \text{Payout}_{A,\text{base}} = 0.50 \cdot 980 = 490 \text{ TAO}
  $$

- Boris:

  $$
  \text{Payout}_{B,\text{base}} = 0.30 \cdot 980 = 294 \text{ TAO}
  $$

- Cara:

  $$
  \text{Payout}_{C,\text{base}} = 0.20 \cdot 980 = 196 \text{ TAO}
  $$

Mental “solo baseline” at 0.10 TAO / \(\alpha_1\):

- Alice solo: \(5{,}000 \cdot 0.10 = 500\) TAO  
- Boris solo: \(3{,}000 \cdot 0.10 = 300\) TAO  
- Cara solo: \(2{,}000 \cdot 0.10 = 200\) TAO  

On base payout alone, each miner is **~2% worse** than that simple solo baseline due to the fee.

---

### Impact & Boss Collateral

Price drop:

$$
\Delta P = \frac{P_0 - P_1}{P_0}
= \frac{0.20 - 0.09}{0.20} = 0.55
$$

Normalized shock:

$$
I_{\text{hit}} = \min\left(1, \frac{0.55}{0.5}\right) = 1
$$

Size-adjusted impact:

$$
I'_{\text{hit}} = 1 \cdot \frac{Q_1}{S_1 + \epsilon}
\approx \frac{10{,}000}{20{,}000} = 0.5
$$

Boss collateral returned:

$$
A_{\text{returned}}
= A_{\text{esc}} \cdot
\left( \beta_{\min} + (1 - \beta_{\min}) \cdot I'_{\text{hit}} \right)
= 700 \cdot (0.4 + 0.6 \cdot 0.5)
= 700 \cdot 0.7 = 490 \text{ MOB-}\alpha
$$

Escrow lost (burn/treasury):

$$
A_{\text{esc}} - A_{\text{returned}}
= 700 - 490 = 210 \text{ MOB-}\alpha
$$

If all of this 210 is burned, total burnt MOB-α:

$$
A_{\text{burn,total}} = 200 + 210 = 410 \text{ MOB-}\alpha
$$

---

### Emissions-Funded MOB-α Rewards

Assume MobNet allocates a hit reward pool of:

$$
E_{\text{hit}} = 400 \text{ MOB-}\alpha
$$

from miner emissions (≈ 40 TAO of value at \(p_\alpha = 0.1\) TAO / MOB-α; ~4% of hit volume).

Loyalty shares:

- Alice: \(\ell_A = 400 / 1{,}000 = 0.40\)  
- Boris: \(\ell_B = 300 / 1{,}000 = 0.30\)  
- Cara: \(\ell_C = 300 / 1{,}000 = 0.30\)

Use \(\gamma = 1.0\), \(\delta = 0.5\).

Approximate:

- \(\sqrt{0.40} \approx 0.632\)  
- \(\sqrt{0.30} \approx 0.548\)

Weights:

- Alice:

  $$
  w_A = c_A^\gamma \ell_A^\delta
  = 0.50 \cdot 0.632 \approx 0.316
  $$

- Boris:

  $$
  w_B = 0.30 \cdot 0.548 \approx 0.164
  $$

- Cara:

  $$
  w_C = 0.20 \cdot 0.548 \approx 0.110
  $$

Total:

$$
W = w_A + w_B + w_C \approx 0.316 + 0.164 + 0.110 = 0.59
$$

Rewards:

- Alice:

  $$
  R_A = E_{\text{hit}} \cdot \frac{w_A}{W}
  \approx 400 \cdot 0.535 \approx 214 \text{ MOB-}\alpha
  $$

- Boris:

  $$
  R_B \approx 400 \cdot 0.279 \approx 112 \text{ MOB-}\alpha
  $$

- Cara:

  $$
  R_C \approx 400 \cdot 0.186 \approx 74 \text{ MOB-}\alpha
  $$

TAO-equivalent at \(p_\alpha = 0.1\):

- Alice bonus: \(\approx 21.4\) TAO  
- Boris bonus: \(\approx 11.2\) TAO  
- Cara bonus: \(\approx 7.4\) TAO  

---

### Comparing Hit vs Solo Selling

Solo baseline (mental):

- Alice: 500 TAO  
- Boris: 300 TAO  
- Cara: 200 TAO  

Hit outcomes:

- **Alice**

  $$
  \text{Hit}_A \approx 490 + 21.4 = 511.4 \text{ TAO}
  $$

  vs 500 → **~+2.3%**

- **Boris**

  $$
  \text{Hit}_B \approx 294 + 11.2 = 305.2 \text{ TAO}
  $$

  vs 300 → **~+1.7%**

- **Cara**

  $$
  \text{Hit}_C \approx 196 + 7.4 = 203.4 \text{ TAO}
  $$

  vs 200 → **~+1.7%**

All three miners end up **slightly ahead** vs solo selling because emissions-funded MOB-α rewards **overcompensate** the fee and slippage.

Meanwhile, the system:

- Burned **410 MOB-α**,  
- Added **100 MOB-α** to treasury,  
- Collected **20 TAO** in fees,  
- Logged a high-impact hit on **Subnet 1** on the Hit Board.

---

## Value Proposition

### For The Subnet Owner (“The Taofather”)

- **Demand for MOB-α** is driven by gameplay (hits, clout), not just passive yield.  
- **Structural burns** link usage directly to supply reduction.  
- **Treasury + fees** provide a budget for events, tournaments, and further burns.  
- A **narrative moat**: you’re not just “Subnet 1” — you’re **the mafia subnet** where miners are Mobsters and validators are Consiglieres.

### For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)

- **Bosses**  
  - Orchestrate high-impact hits.  
  - Risk MOB-α for clout and big operations.  
  - Recover more collateral when hits land hard.

- **Mobsters (Miners)**  
  - Get base payouts similar to large exits.  
  - Receive extra MOB-α, making hits slightly +EV over solo selling in most cases.  
  - Build reputation via leaderboards, Families, and historic hits.

- **Consiglieres (Validators)**  
  - Define and enforce the scoring rules.  
  - Compute impact and allocate emissions.  
  - Coordinate which hits are valid and how miners are rewarded.

---

## FAQ

**Q: Is this financial advice?**  
A: No. Nothing here is financial, investment, or trading advice. It does not recommend any real-world behavior.

**Q: Why would miners join hits instead of just selling?**  
A: Because the subnet recycles **100% of its miner emissions share** into MOB-α rewards for miners (Mobsters) who participate in hits. Those rewards are tuned so that **joining hits is usually slightly better than solo selling**, especially for miners who hold MOB-α.

**Q: Why the mafia theme?**  
A: It turns dry mechanics (burns, fees, emissions, miner/validator scoring) into a story:
- Hits = coordinated operations  
- Burns = cost of doing business  
- Families = miner factions  
- Hit Board = public legend of validator-approved jobs

Narrative makes people care about more than just numbers.
