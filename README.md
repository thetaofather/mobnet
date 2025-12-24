<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e128c303-7891-4f68-9683-4d72c89ad4c9" />

<h1 align="center">The Taofather’s MOBnet:   
 
  Turning dTAO Volatility Into Mafia-Style Hits</h1>



## Intro

Welcome to MOBnet, a mafia-themed Bittensor subnet where volatility is the product and coordination is the hustle.

Its native token, MOB-α (“Mob Alpha”), bankrolls an underworld of hits on rival subnets:

- Bosses put a job on the board by locking up MOB-α and paying the *street tax*.
- Mobsters (Miners) show up with inventory: *the target subnet’s alpha token*, pooled for one clean move.
- When the pool fills, the system executes a single, all-at-once sell (“the hit”), kicking out a payout pot and a price shock.

Each job gets an impact score  *how hard the street felt it* which determines:

- how much of the Boss’s escrow gets washed and returned vs what gets burned,
- how much MOB-α and TAO payout each Mobster (miner) earns,
- and where the job lands on the public Hit Board (the Wall of Jobs).

MOBnet funds MOB-α rewards with a protocol-defined budget (the Envelope), backed by fees and treasury flows (and optionally validator-governed conversions of subnet reward inflows into MOB-α). Parameters can be tuned so that:

> Over time, Mobsters (miners) usually do slightly better running hits than selling alone.

Important disclosure on MOB-α value: Any TAO-equivalent conversions use a reference price `p_alpha` for accounting and examples. `p_alpha` is not a peg, not a promise, and not a guarantee — it’s a “street price” input that constantly changes.

---

## Table of Contents

- [Intro](#Intro)
- [High-Level Overview](#high-level-overview)
  - [MOBnet Slang (Mini Glossary)](#MOBnet-slang-mini-glossary)
  - [Roles](#roles)
  - [The MOB-α Token](#the-mob-%CE%B1-token-MOBnets-alpha-token)
- [Hit Mechanics](#hit-mechanics)
  - [1. Boss Deposit & Hit Creation](#1-boss-deposit--hit-creation)
  - [2. Pool Filling (Mobsters / Miners Join)](#2-pool-filling-mobsters--miners-join)
  - [3. Hit Execution (One-Shot Sell)](#3-hit-execution-one-shot-sell)
  - [4. Base Payouts & Fee](#4-base-payouts--fee)
- [Impact Scoring](#impact-scoring)
  - [Price Shock](#price-shock)
  - [Normalized Shock](#normalized-shock)
  - [Size-Adjusted Impact (Option C: Alpha-Equivalent Depth)](#size-adjusted-impact-option-c-alpha-equivalent-depth)
- [Emissions & MOB-α Rewards](#emissions--mob-%CE%B1-rewards)
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
  - [Emissions-Funded MOB-α Rewards](#emissions-funded-mob-%CE%B1-rewards)
  - [Comparing Hit vs Solo Selling](#comparing-hit-vs-solo-selling)
- [Value Proposition](#value-proposition)
  - [For The Subnet Owner (“The Taofather”)](#for-the-subnet-owner-the-taofather)
  - [For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)](#for-users-bosses-mobsters--miners-consiglieres--validators)
- [FAQ](#faq)

---

## High-Level Overview

MOBnet lives in “Tensor City,” a district of Bittensor subnets. Each subnet has:

- an alpha token (example: alpha_1 for Subnet 1),
- a reputation,
- and *if the streets are talking* — a target on its back.

MOBnet is the underworld layer where alpha tokens become instruments in a game of timing, coordination, and clout.

### MOBnet Slang (Mini Glossary)

- The Taofather — Subnet owner / protocol figurehead. Runs the city, sets the tone.
- Boss — A hit sponsor. Posts jobs by depositing MOB-α and setting terms.
- Mobsters (Miners) — Hit participants. Provide target alpha to the pool and earn payouts + MOB-α rewards.
- Consiglieres (Validators) — Scorers/validators. Keep the books, compute impact, decide reward splits.
- Hit — A single coordinated, batched sell of pooled target alpha resulting in TAO.
- Hit Board / Wall of Jobs — Public listing of open and completed hits + impact scores + lore.
- Street Tax — Upfront, non-refundable burn on the Boss deposit.
- Escrow / Collateral — Boss’s locked MOB-α that gets “washed” back 80–100% depending on impact.
- Wash — Returning escrowed MOB-α; the “lost slice” becomes wash burn + blessing fee.
- Washing Fee — The portion of escrow that is burned forever (parameter `psi`).
- The Blessing — The Taofather’s cut from escrow (the remainder `1-psi`).
- Family Vault — Protocol treasury that receives the Boss treasury cut and other routed flows.
- House TAO — The settlement asset for hit proceeds (the “house” settles in TAO).
- House Cut — The protocol fee `f` taken from hit proceeds before base payouts.
- Envelope — The epoch rewards budget distributed as MOB-α to Mobsters (miners).
- Heat Window — Pool-fill timeout; if it ends, rules decide refund vs partial execution.
- Street Price / Tape — Reference price inputs used for accounting (example: `p_alpha`, `P0`); not a guarantee.

### Roles

- Bosses (Hit Sponsors)  
  Put up MOB-α, name your target, define the terms, and put the hit out.  
  ANYONE can be a boss!

- Mobsters (Miners)  
  The crew. They join hits by depositing the target subnet’s alpha into the pool.  
  They’re scored and paid by Consiglieres (validators) based on participation and MOB-α loyalty (staked MOB-α).  
  ANYONE can be a miner!

  “Mobsters (miners)” means hit participants (not necessarily registered Bittensor miner UIDs). Payouts come from the MOBnet payout desk (distributor/treasury), based on validator scoring.

- Consiglieres (Validators)  
  The accountants with the books. They:
  - track prices and liquidity/depth metrics,
  - compute impact scores and validate jobs,
  - score Mobsters (miners),
  - and decide how envelopes and collateral flows get split.

### The MOB-α Token (MOBnet's Alpha token)

MOB-α is the Family’s currency:

- Bosses must acquire and deposit MOB-α to open hits.
- A fixed fraction is burned up front (street tax), another portion is escrowed (collateral), and a portion goes to the Family Vault (treasury).
- A validator-agreed epoch envelope is converted into MOB-α rewards — no miner UID required to get paid.

The more the game is played, the more MOB-α gets burned, while the envelope can keep active Mobsters slightly +EV (depending on parameters and `p_alpha`).

---

## Hit Mechanics

A Boss targets subnet `T` and sets:

- Hit pool size `Q_T`: total units of subnet `T`’s alpha to collect.
- MOB-α deposit `A_boss`: the Boss’s skin in the game.

---

### 1. Boss Deposit & Hit Creation

#### Boss Deposit Rule

Deposit size can be tied to the notional size of the job:

- `Q_T`: pool size (units of target alpha)
- `P0`: pre-hit alpha price (TAO per alpha)
- `p_alpha`: MOB-α reference “street price” (TAO per MOB-α)
- `k`: margin factor (MOB-α per 1 TAO of hit notional)
- `A_min`: minimum deposit
- `S_tilde`: optional normalized size in [0,1] (used only to discount deposits for large targets)

Base rule:

$$
A_{boss}^{base} = k \cdot \frac{Q_T \cdot P0}{p_{\alpha}}
$$

Minimum:

$$
A_{boss} = \max\left(A_{min},\; A_{boss}^{base}\right)
$$

Optional “big-game discount”:

$$
g(\tilde{S}_T) = \frac{1}{1 + \lambda \cdot \tilde{S}_T}
$$

Size-adjusted:

$$
A_{boss} = \max\left(
  A_{min},\;
  k \cdot \frac{Q_T \cdot P0}{p_{\alpha}} \cdot g(\tilde{S}_T)
\right)
$$

#### Deposit Split

$$
A_{burn,instant} = 0.20 \, A_{boss},\quad
A_{esc} = 0.70 \, A_{boss},\quad
A_{treasury} = 0.10 \, A_{boss}
$$

The job goes up on the Hit Board.

---

### 2. Pool Filling (Mobsters / Miners Join)

Each Mobster `i` deposits:

$$
d_i \quad \text{(units of target alpha)}
$$

Total pool:

$$
Q_T = \sum_i d_i
$$

When the pool fills (or the Heat Window ends), the job is armed.

---

### 3. Hit Execution (One-Shot Sell)

The full pool is sold into House TAO as a single batched execution.

Proceeds:

$$
V_{hit} \quad \text{(in TAO)}
$$

Price moves from `P0` to `P1`.

---

### 4. Base Payouts & Fee

House cut:

$$
V_{fee} = f \cdot V_{hit}
$$

Crew payout pot:

$$
V_{mob} = (1-f)\cdot V_{hit}
$$

Base payout to Mobster `i`:

$$
Payout_{i,base} = V_{mob}\cdot \frac{d_i}{\sum_j d_j}
$$

---

## Impact Scoring

### Price Shock

$$
\Delta P = \frac{P0 - P1}{P0}
$$

### Normalized Shock

$$
I_{hit} = \min\left(1,\; \max\left(0,\; \frac{\Delta P}{\Delta P_{max}}\right)\right)
$$

Interpretation:
- If `I_hit` is near 0: the hit barely moved price.
- If `I_hit` is near 1: the hit reached the max-scored shock level.

### Size-Adjusted Impact (Option C: Alpha-Equivalent Depth)

Let `R_TAO,T` be the TAO-side reserve/depth metric for subnet `T`, and `P0` the pre-hit price.

Alpha-equivalent depth:

$$
L_T = \frac{R_{TAO,T}}{P0}
$$

If using AMM reserves, with spot `P0 = R_TAO,T / R_alpha,T`, then `L_T` equals `R_alpha,T` (alpha reserves). That’s the “alpha depth on the street.”

Smooth to reduce gamesmanship:

$$
L_T^{smooth} = EMA(L_T)
$$

Size-adjusted impact:

$$
I'_{hit} = I_{hit}\cdot \frac{Q_T}{L_T^{smooth} + \epsilon}
$$

---

## Emissions & MOB-α Rewards

### Epoch Reward Budget

Epoch envelope pool:

$$
E_{rewards,epoch}\quad (\text{in MOB-}\alpha)
$$

### Allocating Rewards to Hits

For each hit `h`:

$$
s_h = \frac{V_{hit,h}}{\sum_k V_{hit,k}}\cdot \left(1+\kappa\cdot I'_{hit,h}\right)
$$

Then allocate:

$$
E_{hit,h} = E_{rewards,epoch}\cdot \frac{s_h}{\sum_j s_j}
$$

### Allocating Rewards Within a Hit

Contribution share:

$$
c_i = \frac{d_i}{\sum_j d_j}
$$

Loyalty share:

$$
\ell_i = \frac{H_i}{\sum_j H_j}
$$

Weight:

$$
w_i = c_i^{\gamma}\cdot \ell_i^{\delta}
$$

Reward:

$$
R_i = E_{hit}\cdot \frac{w_i}{\sum_k w_k}
$$

### Making Hits Slightly +EV vs Solo Selling

Solo (approx):

$$
Solo_i \approx P_{solo}\cdot d_i
$$

Hit (approx):

$$
Hit_i \approx Payout_{i,base} + p_{\alpha}\cdot R_i
$$

Tuning target:

$$
\mathbb{E}[Hit_i] \gtrsim \mathbb{E}[Solo_i]
$$

---

## Boss Collateral & Burns

Escrow:

$$
A_{esc} = 0.70\,A_{boss}
$$

Minimum return:

$$
\beta_{min} = 0.8
$$

Returned escrow:

$$
A_{returned} = A_{esc}\cdot \left(\beta_{min} + (1-\beta_{min})\cdot \min(1,\; I'_{hit})\right)
$$

Lost escrow:

$$
A_{lost} = A_{esc} - A_{returned}
$$

Split:

$$
A_{wash,burn} = \psi\cdot A_{lost},\quad
A_{taofather} = (1-\psi)\cdot A_{lost}
$$

Totals:

$$
A_{burn,total} = 0.20\,A_{boss} + \psi\cdot (A_{esc}-A_{returned})
$$

$$
A_{treasury,total} = 0.10\,A_{boss} + (1-\psi)\cdot (A_{esc}-A_{returned})
$$

---

## Worked Example: “The 10k Hit on Subnet 1”

### Setup

- `A_boss = 1000` MOB-α
- `Q1 = 10000` alpha_1
- `f = 0.02`
- `DeltaP_max = 0.5`
- `beta_min = 0.8`
- `psi = 0.5`

Example pricing assumptions (example only):
- `P0 = 0.08` TAO per alpha_1
- `p_alpha = 0.005` TAO per MOB-α (reference price for comparisons only)

Mobsters:
- Alice: `dA = 5000`, `HA = 400`
- Boris: `dB = 3000`, `HB = 300`
- Cara: `dC = 2000`, `HC = 300`

### Boss Deposit Breakdown

$$
A_{burn,instant}=200,\quad A_{esc}=700,\quad A_{treasury}=100 \quad (\text{MOB-}\alpha)
$$

### Pool, Price, and Base Payouts

Assume:
- `P1 = 0.036` TAO per alpha_1
- `V_hit = 500` TAO (avg execution price 0.05)

$$
V_{fee} = 0.02\cdot 500 = 10,\quad V_{mob} = 490 \quad (\text{TAO})
$$

Base payouts:

$$
Payout_{A,base} = 490\cdot 0.50 = 245
$$

$$
Payout_{B,base} = 490\cdot 0.30 = 147
$$

$$
Payout_{C,base} = 490\cdot 0.20 = 98
$$

### Impact & Boss Collateral (80% Minimum Return)

$$
\Delta P = \frac{0.08-0.036}{0.08} = 0.55,\quad I_{hit}=1
$$

Assume validator-observed:
- `R_TAO,1 = 1600` TAO

$$
L_1 = \frac{1600}{0.08} = 20000
$$

$$
I'_{hit} \approx \frac{10000}{20000} = 0.5
$$

$$
A_{returned} = 700\cdot (0.8 + 0.2\cdot 0.5) = 630
$$

$$
A_{lost}=70,\quad A_{wash,burn}=35,\quad A_{taofather}=35
$$

### Emissions-Funded MOB-α Rewards

Use a clear, tunable rule tied to hit volume.

Let `r` be the fraction of hit volume returned as MOB-α incentives:

$$
E_{hit} = \frac{r\cdot V_{hit}}{p_{\alpha}}
$$

For this example: `r = 0.04`, `V_hit = 500`, `p_alpha = 0.005`:

$$
E_{hit} = \frac{0.04\cdot 500}{0.005} = \frac{20}{0.005} = 4000
$$

Now allocate within the hit (use `gamma = 1.0`, `delta = 0.5`).

Weights (approx):
- `wA = 0.50*sqrt(0.40) ≈ 0.316`
- `wB = 0.30*sqrt(0.30) ≈ 0.164`
- `wC = 0.20*sqrt(0.30) ≈ 0.110`
- `W ≈ 0.590`

Rewards (approx):

$$
R_A \approx 4000\cdot \frac{0.316}{0.590} \approx 2142
$$

$$
R_B \approx 4000\cdot \frac{0.164}{0.590} \approx 1112
$$

$$
R_C \approx 4000\cdot \frac{0.110}{0.590} \approx 746
$$

TAO-equivalent at reference `p_alpha = 0.005` (illustrative only):
- Alice: `~10.71` TAO
- Boris: `~5.56` TAO
- Cara: `~3.73` TAO

### Comparing Hit vs Solo Selling

Solo baseline at avg `0.05` TAO per alpha:
- Alice: 250
- Boris: 150
- Cara: 100

Hit outcomes (base + illustrative MOB-α bonus):
- Alice: `245 + 10.71 = 255.71`
- Boris: `147 + 5.56 = 152.56`
- Cara: `98 + 3.73 = 101.73`

---

## Value Proposition

### For The Subnet Owner (“The Taofather”)

- MOB-α demand is driven by jobs, not vibes.
- Burns scale with usage (every job pays the street).
- The Family Vault + House cut funds events, buybacks/burns, and tooling.
- Narrative moat: the subnet where volatility gets weaponized into public lore.

### For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)

Bosses:
- Pick targets, size jobs, and post them publicly on the Hit Board.
- Bounded collateral risk: escrow return is formula-driven (80–100% of escrow depending on impact).
- Clear cost: street tax is the known, non-refundable cost; the rest is transparent (wash + blessing).
- Flexible job design: pool size, Heat Window, and policy constraints.

Mobsters (miners / hit participants):
- No UID required: anyone can participate by contributing target alpha.
- Two-layer payout: (1) base TAO proceeds from the hit sale, plus (2) MOB-α “envelope” rewards.
- Loyalty matters: holding MOB-α can increase envelope share (delta-tunable).
- Reputation ladder: leaderboards, “Families,” and job history (policy choice).
- Transparent math: proportional payouts and reproducible scoring.

Consiglieres (validators):
- Define street rules: smoothing windows, depth sources, shock caps, anti-gaming checks.
- Score and settle: compute impact, validate jobs, and drive allocation consensus.
- Protect against manipulation: EMA/TWAP, min fill requirements, and reserve-source diversity.
- Run the payout desk: publish distributions, resolve disputes, and maintain the Hit Board’s credibility.

---

## FAQ

Q: Is this financial advice?  
A: No.

Q: What is MOB-α “worth” in this README?  
A: The example uses `p_alpha = 0.005` TAO/MOB-α only for TAO-equivalent comparisons. It is not a peg or guarantee.

Q: What does “envelopes” mean?  
A: “Envelopes” are MOB-α rewards paid from the epoch envelope pool to hit participants — bonus on top of base TAO proceeds.

Q: What does the subnet size metric mean and how is it determined?  
A: Validators compute alpha-equivalent depth `L_T = R_TAO,T / P0`, smooth it, then score `I'_hit = I_hit * Q_T / (L_T_smooth + epsilon)`.

---
