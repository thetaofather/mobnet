# The Taofather’s MobNet: Turning dTAO Volatility Into Mafia-Style Hits

---

## Table of Contents

- [Abstract](#abstract)
- [High-Level Overview](#high-level-overview)
  - [MobNet Slang (Mini Glossary)](#mobnet-slang-mini-glossary)
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

MobNet is a **mafia-themed** Bittensor subnet where **volatility is the product** and coordination is the hustle.

Its native token, **MOB-α** (“Mob Alpha”), bankrolls an underworld of **hits** on other subnets:

- **Bosses** put a job on the board by locking up MOB-α and paying the street tax.  
- **Mobsters (Miners)** show up with inventory: the **target subnet’s alpha token**, pooled for one clean move.  
- When the pool fills, the system executes a **single, all-at-once sell** (“the hit”), kicking out a payout pot and a price shock.

Each job gets an **impact score**—how hard the street felt it—which determines:

- how much of the Boss’s escrow gets **washed and returned** vs what gets **burned**,  
- how much **MOB-α and base payout** each Mobster earns,  
- and where the job lands on the public **Hit Board** (the Wall of Jobs).

MobNet funds MOB-α rewards with a **protocol-defined epoch budget** (the **Envelope**), backed by fees and treasury flows. Parameters are tuned so that:

> Over time, **Mobsters usually do slightly better** running hits than dumping alone.

**Important disclosure on MOB-α value:** Any TAO-equivalent conversions use a **reference price** \( p_\alpha \) for accounting and examples. \( p_\alpha \) is **not a peg, not a promise, and not a guarantee**—it’s a “street price” input that can change.

---

## High-Level Overview

MobNet lives in “Tensor City,” a district of Bittensor subnets. Each subnet has:

- an **alpha token** (e.g. \( \alpha_1 \) for Subnet 1),  
- a **reputation**,  
- and—if the streets are talking—a **target on its back**.

MobNet is the **underworld layer** where alpha tokens become instruments in a game of timing, coordination, and clout.

### MobNet Slang (Mini Glossary)

A quick guide to the lingo used throughout this README:

- **The Taofather**: Subnet owner / protocol figurehead. Runs the city, sets the tone.  
- **Boss**: A hit sponsor. Posts jobs by depositing MOB-α and setting terms.  
- **Mobsters (Miners)**: Hit participants. Provide target alpha to the pool and earn payouts + MOB-α rewards.  
- **Consiglieres (Validators)**: Scorers/validators. Keep the books, compute impact, decide reward splits.  
- **Hit**: A single coordinated, batched sell of pooled target alpha into TAO.  
- **Hit Board / Wall of Jobs**: Public listing of open and completed hits + their impact scores.  
- **Street Tax**: The upfront, non-refundable burn on the Boss deposit (20% in this spec).  
- **Escrow / Collateral**: The Boss’s locked MOB-α (70% in this spec) that gets “washed” back 80–100% depending on impact.  
- **Wash**: The process of returning escrowed MOB-α to the Boss; the “lost” slice is split between wash burn and Taofather fee.  
- **Washing Fee**: The part of lost escrow that is burned forever (parameter \( \psi \)).  
- **The Blessing**: The Taofather’s extra cut from lost escrow (the remainder \( 1-\psi \)).  
- **Family Vault**: Protocol treasury that receives the Boss treasury cut (10%) and other routed flows.  
- **House TAO**: The destination asset for hit execution proceeds (the “house” holds/settles in TAO).  
- **House Cut**: The protocol fee \( f \) taken from hit proceeds before base payouts.  
- **Envelope**: The epoch rewards budget distributed as MOB-α to Mobsters (miners).  
- **Heat Window**: Timeout period for filling a hit pool; if it ends, the job is refunded or executed at partial size (governance choice).  
- **Street Price / Tape**: The reference price inputs used for accounting (e.g., \( p_\alpha \), \( P_0 \)); not a guarantee.

---

### Roles

- **Bosses (Hit Sponsors)**  
  Put up MOB-α, name the target, set the terms, and light the fuse.  
  **ANYONE can be a boss.**

- **Mobsters (Miners)**  
  The crew. They join hits by depositing the target subnet’s alpha into the pool.  
  They’re scored and paid by Consiglieres based on participation and MOB-α loyalty.  
  **ANYONE can be a miner!**

  In Mobnet **‘Mobsters (miners)’** means hit participants (not necessarily registered Bittensor miner UIDs). Payouts come from the MobNet payout desk (distributor/treasury), based on validator scoring.

- **Consiglieres (Validators)**  
  The accountants with the books. They:
  - track prices and liquidity depth,  
  - compute impact scores and validate jobs,  
  - score Mobsters (miners),  
  - and decide how envelopes and collateral flows get split.

### The MOB-α Token (MOBnet's Alpha token)

MOB-α is the Family’s currency:

- Bosses **must acquire and deposit MOB-α** to open hits.  
- A fixed fraction is **burned** up front (the street tax), another portion is **escrowed** (collateral), and a portion goes to the **Family Vault** (treasury).  
- A validator-agreed **epoch envelope** is converted into MOB-α rewards—**no miner UID required** to get paid.

The more the game is played, the more MOB-α gets **burned**, while the envelope can keep active Mobsters **slightly +EV** (depending on parameters and \( p_\alpha \)).

---

## Hit Mechanics

A Boss targets subnet \( T \) and sets:

- Hit pool size \( Q_T \): total units of subnet \( T \)’s alpha to collect.  
- MOB-α deposit \( A_{\text{boss}} \): the Boss’s skin in the game.

---

### 1. Boss Deposit & Hit Creation

#### Boss Deposit Rule

To keep Bosses honest, deposit size can be tied to the notional size of the job:

- \( Q_T \): pool size (units of \( T \)’s alpha)  
- \( P_0 \): pre-hit alpha price (TAO per alpha)  
- \( p_\alpha \): MOB-α reference “street price” (TAO per MOB-α)  
- \( k \): margin factor (MOB-α per 1 TAO of hit size)  
- \( A_{\min} \): minimum deposit  
- \( \tilde{S}_T \): optional normalized size in \([0,1]\) (used only to discount deposits for large targets)

Base rule:

$$
A_{\text{boss}}^{\text{base}} = k \cdot \frac{Q_T \cdot P_0}{p_\alpha}
$$

Minimum:

$$
A_{\text{boss}} = \max\left(A_{\min},\; A_{\text{boss}}^{\text{base}}\right)
$$

To **make big targets cheaper per unit notional** (encourage big-game hunting), apply:

$$
g(\tilde{S}_T) = \frac{1}{1 + \lambda \cdot \tilde{S}_T}
$$

with \( \lambda \in [0,1] \). Then:

$$
A_{\text{boss}} = \max\left(
  A_{\min},\;
  k \cdot \frac{Q_T \cdot P_0}{p_\alpha} \cdot g(\tilde{S}_T)
\right)
$$

#### Deposit Split

The Boss deposit is split three ways:

- **Street tax (instant burn):** \( 20\% \)  
- **Escrow (collateral):** \( 70\% \)  
- **Family Vault (treasury):** \( 10\% \)

$$
A_{\text{burn,instant}} = 0.20 \, A_{\text{boss}},\quad
A_{\text{esc}} = 0.70 \, A_{\text{boss}},\quad
A_{\text{treasury}} = 0.10 \, A_{\text{boss}}
$$

The job goes up on the **Hit Board**: target \( T \), pool size \( Q_T \), terms, timing, and the Boss’s signature.

---

### 2. Pool Filling (Mobsters / Miners Join)

Mobsters join the job by depositing target alpha.

Each Mobster \( i \) posts:

- \( d_i \): units of subnet \( T \)’s alpha

Total pool:

$$
Q_T = \sum_i d_i
$$

When \( Q_T \) hits the mark (or the **Heat Window** ends), the job is armed.

> **Heat Window:** if the hit times out, governance chooses whether the pool is refunded pro-rata or the job executes at the collected size.

---

### 3. Hit Execution (One-Shot Sell)

When the job goes down:

- The full pool \( Q_T \) is sold into **House TAO** as a single batched execution.  
- Proceeds:

$$
V_{\text{hit}} \quad \text{(in House TAO)}
$$

- Price moves from \( P_0 \) to \( P_1 \).

That batched sale is the **hit**.

---

### 4. Base Payouts & Fee

The House takes a cut: \( f \in [0.01, 0.03] \).

House cut:

$$
V_{\text{fee}} = f \cdot V_{\text{hit}}
$$

Crew payout pot:

$$
V_{\text{mob}} = (1 - f) \cdot V_{\text{hit}}
$$

Each Mobster \( i \) gets paid pro-rata:

$$
\text{Payout}_{i,\text{base}} = V_{\text{mob}} \cdot \frac{d_i}{\sum_j d_j}
$$

On base payout alone, Mobsters can do slightly worse than an ideal solo sell due to the House cut and slippage—so the envelope (MOB-α rewards) is designed to make the job worth it.

---

## Impact Scoring

Impact scoring is how the Consiglieres tell legend from noise.

### Price Shock

$$
\Delta P = \frac{P_0 - P_1}{P_0}
$$

### Normalized Shock

Pick a max meaningful drop \( \Delta P_{\max} \) (e.g. 0.3–0.5).

$$
I_{\text{hit}} = \min\left(1, \max\left(0, \frac{\Delta P}{\Delta P_{\max}}\right)\right)
$$

### Size-Adjusted Impact (Option C: Alpha-Equivalent Depth)

To compare hits across subnets fairly, validators compute **alpha-equivalent depth**:

- \( R_{\text{TAO},T} \): TAO reserve / TAO depth in subnet \( T \)’s alpha market (from on-chain liquidity data)  
- \( P_0 \): pre-hit price (TAO per alpha)

Size metric (in alpha units):

$$
L_T = \frac{R_{\text{TAO},T}}{P_0}
$$

Validators use a smoothed value to reduce gamesmanship:

$$
L_T^{\text{smooth}} = \text{EMA}(L_T)
$$

Size-adjusted impact:

$$
I'_{\text{hit}} = I_{\text{hit}} \cdot \frac{Q_T}{L_T^{\text{smooth}} + \epsilon}
$$

High \( I'_{\text{hit}} \) means the crew moved real weight relative to the street’s depth.

---

## Emissions & MOB-α Rewards

### Epoch Reward Budget

Each epoch, MobNet sets an envelope:

$$
E_{\text{rewards,epoch}} \quad (\text{MOB-}\alpha)
$$

This is the **Envelope Pool** used to reward hit participation.

### Allocating Rewards to Hits

For each hit \( h \):

- \( V_{\text{hit},h} \): hit volume (TAO)  
- \( I'_{\text{hit},h} \): size-adjusted impact  
- \( V_{\text{total}} = \sum_k V_{\text{hit},k} \)

Allocation:

$$
E_{\text{hit},h}
= E_{\text{rewards,epoch}} \cdot
\frac{V_{\text{hit},h}}{V_{\text{total}}}
\cdot \left( 1 + \kappa \cdot I'_{\text{hit},h} \right)
$$

### Allocating Rewards Within a Hit

Contribution share:

$$
c_i = \frac{d_i}{\sum_j d_j}
$$

Loyalty share (MOB-α holdings):

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

Solo:

$$
\text{Solo}_i \approx P_{\text{solo}} \cdot d_i
$$

Hit:

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

Minimum return:

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

Split the lost part between the wash and the blessing:

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

**Example pricing assumptions (example only):**

- \( P_0 = 0.08 \) TAO / \( \alpha_1 \)  
- \( p_\alpha = 0.005 \) TAO / MOB-α (**reference price for comparisons only**)

Mobsters:

- Alice: \( d_A = 5{,}000 \), \( H_A = 400 \)  
- Boris: \( d_B = 3{,}000 \), \( H_B = 300 \)  
- Cara: \( d_C = 2{,}000 \), \( H_C = 300 \)

### Boss Deposit Breakdown

$$
A_{\text{burn,instant}} = 200,\quad A_{\text{esc}} = 700,\quad A_{\text{treasury}} = 100
\quad (\text{MOB-}\alpha)
$$

### Pool, Price, and Base Payouts

Assume:

- \( P_1 = 0.036 \) TAO / \( \alpha_1 \)  
- \( V_{\text{hit}} = 500 \) TAO (avg 0.05)

$$
V_{\text{fee}} = 10,\quad V_{\text{mob}} = 490 \quad (\text{TAO})
$$

Base payouts:

- Alice: 245 TAO  
- Boris: 147 TAO  
- Cara: 98 TAO

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

$$
A_{\text{returned}} = 700 \cdot (0.8 + 0.2\cdot 0.5) = 630
$$

$$
A_{\text{lost}} = 70,\quad A_{\text{wash,burn}} = 35,\quad A_{\text{taofather}} = 35
$$

### Emissions-Funded MOB-α Rewards

Assume \( E_{\text{hit}} = 5{,}000 \) MOB-α.

Rewards (same weight scheme as earlier):

- Alice: \( R_A \approx 2{,}675 \) MOB-α  
- Boris: \( R_B \approx 1{,}395 \) MOB-α  
- Cara: \( R_C \approx 930 \) MOB-α

TAO-equivalent (illustrative at \( p_\alpha = 0.005 \)):

- Alice: 13.375 TAO  
- Boris: 6.975 TAO  
- Cara: 4.650 TAO

### Comparing Hit vs Solo Selling

Solo baseline (avg 0.05 TAO/α):

- Alice: 250 TAO  
- Boris: 150 TAO  
- Cara: 100 TAO

Hit outcomes:

- Alice: 258.375 TAO  
- Boris: 153.975 TAO  
- Cara: 102.650 TAO

---

## Value Proposition

### For The Subnet Owner (“The Taofather”)

- MOB-α demand comes from **jobs**, not vibes  
- Burns scale with activity (every job pays the street)  
- The Family Vault + House cut funds events, buybacks, and more lore  
- A narrative moat: the subnet where volatility gets weaponized

### For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)

- **Bosses:** post jobs, chase clout, escrow returns 80–100%  
- **Mobsters:** run hits for base TAO + envelopes (potentially +EV)  
- **Consiglieres:** keep the books, score the jobs, protect the rules

---

## FAQ

**Q: Is this financial advice?**  
A: No.

**Q: What is MOB-α “worth” in this README?**  
A: The example uses \( p_\alpha = 0.005 \) TAO/MOB-α **only** for TAO-equivalent comparisons. It is not a peg or guarantee.

**Q: What does the subnet size metric mean and how is it determined?**  
A: Validators compute alpha-equivalent depth \( L_T = R_{\text{TAO},T}/P_0 \), smooth it, then score \( I'_{\text{hit}} = I_{\text{hit}} \cdot Q_T/(L_T^{smooth}+\epsilon) \).

---
