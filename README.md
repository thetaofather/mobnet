# The Taofather’s MobNet: Turning dTAO Volatility Into Mafia-Style Hits

---

## Table of Contents

- [Abstract](#abstract)
- [High-Level Overview](#high-level-overview)
  - [Roles](#roles)
  - [The MOB-α Token](#the-mob-α-token-mobnets-alpha-token)
- [Hit Mechanics](#hit-mechanics)
  - [1. Boss Deposit & Hit Creation](#1-boss-deposit--hit-creation)
  - [2. Pool Filling (Mobsters / Miners Join)](#2-pool-filling-mobsters--miners-join)
  - [3. Hit Execution (One-Shot Sell)](#3-hit-execution-one-shot-sell)
  - [4. Base Payouts & Fee](#4-base-payouts--fee)
- [Impact Scoring](#impact-scoring)
  - [Price Shock](#price-shock)
  - [Normalized Shock](#normalized-shock)
  - [Size-Adjusted Impact (Option C: Alpha-Equivalent Depth)](#size-adjusted-impact-option-c-alpha-equivalent-depth)
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
  - [Impact & Boss Collateral (80% Minimum Return)](#impact--boss-collateral-80-minimum-return)
  - [Emissions-Funded MOB-α Rewards](#emissions-funded-mob-α-rewards)
  - [Comparing Hit vs Solo Selling](#comparing-hit-vs-solo-selling)
- [Value Proposition](#value-proposition)
  - [For The Subnet Owner (“The Taofather”)](#for-the-subnet-owner-the-taofather)
  - [For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)](#for-users-bosses-mobsters--miners-consiglieres--validators)
- [FAQ](#faq)

---

## Abstract

MobNet is a **mafia-themed** subnet for Bittensor where **volatility is the product**.

Its native token, **MOB-α** (“Mob Alpha”), funds the organized underworld of **hits** on other subnets:

- **Bosses** open hits by burning and locking MOB-α.  
- **Mobsters (Miners)** join hits by contributing the **target subnet’s alpha token** into a pooled stack.  
- When the pool fills, the system executes a **single, all-at-once sell event** (“the hit”), generating a payout pot and a price shock.

An **impact score** measures how brutal the hit was and determines:

- how much of the Boss’s locked MOB-α is **washed and returned** vs **burned**,  
- how much **MOB-α and base payout** each Mobster (miner) earns,  
- and how the hit ranks on a public **Hit Board**.

MobNet dedicates a **protocol-defined rewards budget each epoch** (funded by fees and treasury flows, and optionally by validator-governed conversions of subnet reward inflows into MOB-α) to MOB-α rewards for Mobsters (miners) who participate in hits. Parameters are tuned so that:

> Over time, **Mobsters (miners) usually earn slightly more** by joining hits vs by selling alone.

**Important disclosure on MOB-α value:** Any TAO-equivalent conversions use a **reference price** \( p_\alpha \) for accounting and examples. \( p_\alpha \) is **not a promised value, peg, or guarantee**—it may be derived from an oracle, TWAP, or market, and can change.

This README describes the MobNet protocol.

---

## High-Level Overview

MobNet operates in a “Tensor City” of Bittensor subnets. Each subnet has:

- an **alpha token** (e.g. \( \alpha_1 \) for Subnet 1),  
- a **reputation**,  
- and a potential **target on its back**.

MobNet is the **underworld layer** where every subnet's alpha token becomes an instrument in a game of coordination, timing, and clout.

### Roles

- **Bosses (Hit Sponsors)**  
  Open hits on specific subnets by depositing MOB-α and defining the hit parameters.  
  **ANYONE can be a boss.**

- **Mobsters (Miners)**  
  Miners on MobNet. They join hits by depositing the target subnet’s alpha into hit pools. They are scored and rewarded by validators (Consiglieres) for effective participation in hits and for holding MOB-α.  
  **ANYONE can be a miner (no miner uid or registration required).**

  In this README, **‘Mobsters (miners)’ refers to participants in hits** (not necessarily registered Bittensor miner UIDs); rewards are paid by the MobNet distributor/treasury based on validator scoring.

- **Consiglieres (Validators)**  
  Validators on MobNet. They:
  - track internal prices and subnet size / liquidity metrics,  
  - compute impact scores for hits,  
  - score and weight Mobsters (miners),  
  - and drive consensus on how rewards budgets and collateral flows are allocated.

### The MOB-α Token (MOBnet's Alpha token)

MOB-α is the underworld’s currency:

- Bosses **must acquire and deposit MOB-α** to open hits.  
- A fixed fraction of each deposit is **burned**; another is held as **collateral**.  
- A validator-agreed **epoch rewards budget** (via a distributor/treasury mechanism) is turned into MOB-α rewards—**no miner UID is required to participate**.

The more the game is played, the more MOB-α is **burned**, while the rewards budget can keep the system **slightly +EV** for active Mobsters (miners) (depending on parameters and the reference price \( p_\alpha \)).

---

## Hit Mechanics

A Boss targets subnet \( T \) (e.g. **Subnet 1**) and defines:

- Hit pool size \( Q_T \): total units of subnet \( T \)’s alpha to be collected.  
- MOB-α deposit \( A_{\text{boss}} \).

---

### 1. Boss Deposit & Hit Creation

#### Boss Deposit Rule

To keep Bosses’ skin in the game proportional to the size and risk of the hit, MobNet can define \( A_{\text{boss}} \) as a function of:

- \( Q_T \): hit pool size (units of subnet \( T \)’s alpha),  
- \( P_0 \): pre-hit price of that alpha in TAO,  
- \( p_\alpha \): reference price of MOB-α in TAO (for accounting),  
- \( k \): “hit margin” factor (how much MOB-α per 1 TAO of hit size),  
- \( A_{\min} \): minimum Boss deposit,  
- \( \tilde{S}_T \): normalized subnet size in \([0,1]\) (optional; used only for deposit discounting).

A simple base rule (no size adjustment):

$$
A_{\text{boss}}^{\text{base}} = k \cdot \frac{Q_T \cdot P_0}{p_\alpha}
$$

with a minimum:

$$
A_{\text{boss}} = \max\left(A_{\min},\; A_{\text{boss}}^{\text{base}}\right)
$$

To **encourage hits on larger subnets**, we introduce a size factor that makes **bigger subnets cheaper per unit of notional**:

$$
g(\tilde{S}_T) = \frac{1}{1 + \lambda \cdot \tilde{S}_T}
$$

where \( \lambda \in [0,1] \) controls how strongly size matters.

The size-adjusted Boss deposit:

$$
A_{\text{boss}} = \max\left(
  A_{\min},\;
  k \cdot \frac{Q_T \cdot P_0}{p_\alpha} \cdot g(\tilde{S}_T)
\right)
$$

#### Deposit Split

$$
A_{\text{burn,instant}} = 0.20 \, A_{\text{boss}},\quad
A_{\text{esc}} = 0.70 \, A_{\text{boss}},\quad
A_{\text{treasury}} = 0.10 \, A_{\text{boss}}
$$

The hit is posted on the **Hit Board**.

---

### 2. Pool Filling (Mobsters / Miners Join)

Mobsters join by depositing the target subnet’s alpha token:

$$
Q_T = \sum_i d_i
$$

When \( Q_T \) reaches the target (or times out), the hit is armed.

---

### 3. Hit Execution (One-Shot Sell)

The entire pool \( Q_T \) is sold into **House TAO**, yielding:

$$
V_{\text{hit}} \quad \text{(in House TAO)}
$$

Price moves from \( P_0 \) to \( P_1 \).

---

### 4. Base Payouts & Fee

Fee:

$$
V_{\text{fee}} = f \cdot V_{\text{hit}}
$$

Mobster payout pool:

$$
V_{\text{mob}} = (1 - f) \cdot V_{\text{hit}}
$$

Base payout to miner \( i \):

$$
\text{Payout}_{i,\text{base}} = V_{\text{mob}} \cdot \frac{d_i}{\sum_j d_j}
$$

---

## Impact Scoring

### Price Shock

$$
\Delta P = \frac{P_0 - P_1}{P_0}
$$

### Normalized Shock

$$
I_{\text{hit}} = \min\left(1, \max\left(0, \frac{\Delta P}{\Delta P_{\max}}\right)\right)
$$

### Size-Adjusted Impact (Option C: Alpha-Equivalent Depth)

Validators compute alpha-equivalent depth:

$$
L_T = \frac{R_{\text{TAO},T}}{P_0}
$$

Use a smoothed value (EMA/TWAP):

$$
L_T^{\text{smooth}} = \text{EMA}(L_T)
$$

Size-adjusted impact:

$$
I'_{\text{hit}} = I_{\text{hit}} \cdot \frac{Q_T}{L_T^{\text{smooth}} + \epsilon}
$$

---

## Emissions & MOB-α Rewards

### Epoch Reward Budget

Define a MOB-α reward budget each epoch:

$$
E_{\text{rewards,epoch}} \quad (\text{MOB-}\alpha)
$$

### Allocating Rewards to Hits

$$
E_{\text{hit},h}
= E_{\text{rewards,epoch}} \cdot
\frac{V_{\text{hit},h}}{V_{\text{total}}}
\cdot \left( 1 + \kappa \cdot I'_{\text{hit},h} \right)
$$

### Allocating Rewards Within a Hit

Contribution:

$$
c_i = \frac{d_i}{\sum_j d_j}
$$

Loyalty:

$$
\ell_i = \frac{H_i}{\sum_j H_j}
$$

Weight:

$$
w_i = c_i^{\gamma} \cdot \ell_i^{\delta}
$$

Reward:

$$
R_i = E_{\text{hit}} \cdot \frac{w_i}{\sum_k w_k}
$$

### Making Hits Slightly +EV vs Solo Selling

$$
\text{Solo}_i \approx P_{\text{solo}} \cdot d_i
$$

$$
\text{Hit}_i \approx \text{Payout}_{i,\text{base}} + p_\alpha \cdot R_i
$$

Target:

$$
\mathbb{E}[\text{Hit}_i] \gtrsim \mathbb{E}[\text{Solo}_i]
$$

---

## Boss Collateral & Burns

Escrow:

$$
A_{\text{esc}} = 0.70 \, A_{\text{boss}}
$$

Minimum return fraction:

$$
\beta_{\min} = 0.8
$$

Returned escrow:

$$
A_{\text{returned}}
= A_{\text{esc}} \cdot
\left( \beta_{\min} + (1 - \beta_{\min}) \cdot \min(1, I'_{\text{hit}}) \right)
$$

Lost escrow:

$$
A_{\text{lost}} = A_{\text{esc}} - A_{\text{returned}}
$$

Split:

$$
A_{\text{wash,burn}} = \psi \cdot A_{\text{lost}},\quad
A_{\text{taofather}} = (1-\psi)\cdot A_{\text{lost}}
$$

Total burned:

$$
A_{\text{burn,total}}
= 0.20 A_{\text{boss}} + \psi \cdot (A_{\text{esc}} - A_{\text{returned}})
$$

Treasury intake:

$$
A_{\text{treasury,total}}
= 0.10 A_{\text{boss}} + (1-\psi)\cdot (A_{\text{esc}} - A_{\text{returned}})
$$

---

## Worked Example: “The 10k Hit on Subnet 1”

### Setup

- \( A_{\text{boss}} = 1{,}000 \) MOB-α  
- \( Q_1 = 10{,}000 \, \alpha_1 \)  
- \( f = 0.02 \)  
- \( \Delta P_{\max} = 0.5 \)  
- \( \beta_{\min} = 0.8 \)  
- \( \psi = 0.5 \)  

**Example pricing assumptions (for this example only):**

- \( P_0 = 0.08 \) TAO / \( \alpha_1 \)  
- \( p_\alpha = 0.005 \) TAO / MOB-α (**illustrative reference price only**, not a peg)

Three Mobsters:

- Alice: \( d_A = 5{,}000 \), \( H_A = 400 \)  
- Boris: \( d_B = 3{,}000 \), \( H_B = 300 \)  
- Cara: \( d_C = 2{,}000 \), \( H_C = 300 \)

$$
H_{\text{tot}} = 1{,}000 \text{ MOB-}\alpha
$$

### Boss Deposit Breakdown

$$
A_{\text{burn,instant}} = 200,\quad A_{\text{esc}} = 700,\quad A_{\text{treasury}} = 100
\quad (\text{all in MOB-}\alpha)
$$

### Pool, Price, and Base Payouts

Assume:

- Post-hit price \( P_1 = 0.036 \) TAO / \( \alpha_1 \)  
- Proceeds \( V_{\text{hit}} = 500 \) TAO (avg 0.05)

Fee:

$$
V_{\text{fee}} = 10,\quad V_{\text{mob}} = 490 \quad (\text{TAO})
$$

Base payouts:

- Alice: \( 245 \) TAO  
- Boris: \( 147 \) TAO  
- Cara: \( 98 \) TAO  

### Impact & Boss Collateral (80% Minimum Return)

$$
\Delta P = \frac{0.08 - 0.036}{0.08} = 0.55,\quad
I_{\text{hit}} = 1
$$

Assume validators observe \( R_{\text{TAO},1} = 1{,}600 \) TAO:

$$
L_1 = \frac{1{,}600}{0.08} = 20{,}000 \, \alpha_1
$$

$$
I'_{\text{hit}} \approx \frac{10{,}000}{20{,}000} = 0.5
$$

Returned escrow:

$$
A_{\text{returned}} = 700 \cdot (0.8 + 0.2\cdot 0.5) = 630
$$

Lost:

$$
A_{\text{lost}} = 70,\quad A_{\text{wash,burn}} = 35,\quad A_{\text{taofather}} = 35
$$

Totals:

- Burned: \( 235 \) MOB-α  
- Treasury from Boss side: \( 135 \) MOB-α

### Emissions-Funded MOB-α Rewards

Assume \( E_{\text{hit}} = 5{,}000 \) MOB-α.

With \( \gamma = 1.0 \), \( \delta = 0.5 \), same weights as before:

- Alice: \( R_A \approx 2{,}675 \) MOB-α  
- Boris: \( R_B \approx 1{,}395 \) MOB-α  
- Cara: \( R_C \approx 930 \) MOB-α  

TAO-equivalent (illustrative):

- Alice: \( 13.375 \) TAO  
- Boris: \( 6.975 \) TAO  
- Cara: \( 4.650 \) TAO  

### Comparing Hit vs Solo Selling

Solo baseline (avg 0.05 TAO/α):

- Alice: 250 TAO  
- Boris: 150 TAO  
- Cara: 100 TAO  

Hit outcomes:

- Alice: \( 245 + 13.375 = 258.375 \) TAO  
- Boris: \( 147 + 6.975 = 153.975 \) TAO  
- Cara: \( 98 + 4.650 = 102.650 \) TAO  

---

## Value Proposition

### For The Subnet Owner (“The Taofather”)

- Demand for MOB-α is driven by gameplay, not just yield  
- Structural burns reduce supply as usage grows  
- Treasury + fees fund events, tournaments, and buybacks/burns  
- A narrative moat: the mafia subnet where hits become lore

### For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)

- **Bosses:** sponsor hits, chase clout, escrow return 80–100%  
- **Mobsters:** base payouts + MOB-α rewards (potentially slightly +EV)  
- **Consiglieres:** define scoring, allocate rewards, validate hits

---

## FAQ

**Q: Is this financial advice?**  
A: No.

**Q: What is MOB-α “worth” in this README?**  
A: The example uses \( p_\alpha = 0.005 \) TAO/MOB-α **only** for TAO-equivalent comparisons. It is not a peg or guarantee.

**Q: What does the subnet size metric mean and how is it determined?**  
A: Validators compute alpha-equivalent depth \( L_T = R_{\text{TAO},T}/P_0 \), smooth it, then score \( I'_{\text{hit}} = I_{\text{hit}} \cdot Q_T/(L_T^{smooth}+\epsilon) \).

---
