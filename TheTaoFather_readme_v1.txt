<img width="938" height="690" alt="image (4)" src="https://github.com/user-attachments/assets/1009e9db-96c9-4279-ace3-6544629842d3" />

<h1 align="center">Turning dTAO Volatility into Mob Hits</h1>

## Intro

Welcome to **The Taofather** — a mob-themed Bittensor subnet in the city of **San Taovanni**.

Its native token, **MOB-α** (“Mob Alpha”), bankrolls an underworld of public “hits” on rival subnets:

- **Bosses** post hits by depositing MOB-α and paying the **Street Tax**.
- **Mobsters (Miners)** show up with inventory: the **target subnet’s alpha token**, pooled for one coordinated move.
- When the pool fills, the system executes a single, all-at-once sell (**the hit**), creating a TAO payout pot and a price shock.
- **Street Heat** (impact score) determines how the job is remembered — and how collateral and rewards get distributed.

### The Game Loop (10 lines)

1) Boss picks a target subnet and posts a job on the **Hit Board**  
2) Boss deposits MOB-α (Street Tax + Escrow + Vault)  
3) Mobsters join by depositing target alpha into the pool  
4) Pool fills (or Heat Window ends) → hit is armed  
5) Protocol executes a one-shot batched sell → TAO proceeds  
6) TAO proceeds are split: **Taofather Rake**, **Boss Kickback**, **Crew Payout**  
7) Validators compute **Street Heat** (impact) using robust price/depth rules  
8) Boss escrow is **washed** back (bounded return), with a small “wash loss” split burn/blessing  
9) Crew receives **Envelope** rewards (MOB-α) on top of TAO payouts  
10) Job is written into lore: ranks, leaderboards, Families, and “Clean/Botched/Legendary” tags

> Important note on MOB-α value: Any TAO-equivalent conversions use a reference input `p_alpha` for accounting and examples. `p_alpha` is **not a peg**, not a promise, and not a guarantee; it’s a “street price” input that constantly changes.

---

## Table of Contents

- [Intro](#intro)
- [High-Level Overview](#high-level-overview)
  - [MOBnet Slang (Mini Glossary)](#mobnet-slang-mini-glossary)
  - [Roles](#roles)
  - [The MOB-α Token](#the-mob-%CE%B1-token-mobnets-alpha-token)
  - [Ranks, Families, and Reputation](#ranks-families-and-reputation)
- [Hit Mechanics](#hit-mechanics)
  - [1. Boss Deposit & Hit Creation](#1-boss-deposit--hit-creation)
  - [2. Pool Filling (Mobsters / Miners Join)](#2-pool-filling-mobsters--miners-join)
  - [3. Hit Execution (One-Shot Sell)](#3-hit-execution-one-shot-sell)
  - [4. Settlement, Rake, and Kickbacks](#4-settlement-rake-and-kickbacks)
- [Street Heat (Impact Scoring)](#street-heat-impact-scoring)
  - [Price Shock](#price-shock)
  - [Normalized Shock](#normalized-shock)
  - [Size-Adjusted Heat (Alpha-Equivalent Depth)](#size-adjusted-heat-alpha-equivalent-depth)
- [The Envelope (Emissions & MOB-α Rewards)](#the-envelope-emissions--mob-%CE%B1-rewards)
  - [Epoch Reward Budget](#epoch-reward-budget)
  - [Allocating Envelopes to Hits](#allocating-envelopes-to-hits)
  - [Allocating Envelopes Within a Hit](#allocating-envelopes-within-a-hit)
  - [Making Crew Runs Slightly +EV vs Solo Selling](#making-crew-runs-slightly-ev-vs-solo-selling)
- [Tribute, Wash, and the Blessing (Boss Collateral)](#tribute-wash-and-the-blessing-boss-collateral)
- [Worked Example: “The 10k Hit on Subnet 1”](#worked-example-the-10k-hit-on-subnet-1)
  - [Setup](#setup)
  - [Boss Deposit Breakdown](#boss-deposit-breakdown)
  - [Pool, Price, and TAO Settlement](#pool-price-and-tao-settlement)
  - [Street Heat & Boss Wash (80% Minimum Return)](#street-heat--boss-wash-80-minimum-return)
  - [Envelope Rewards](#envelope-rewards)
  - [Crew Run vs Solo Sell](#crew-run-vs-solo-sell)
- [Value Proposition](#value-proposition)
  - [For The Taofather](#for-the-taofather)
  - [For Bosses, Mobsters, and Consiglieres](#for-bosses-mobsters-and-consiglieres)
- [FAQ](#faq)

---

## High-Level Overview

MOBnet lives in “Tensor City,” a district of Bittensor subnets. Each subnet has:

- an alpha token (example: `alpha_1` for Subnet 1),
- a reputation,
- and if the streets are talking — a target on its back.

MOBnet is the underworld layer where alpha tokens become instruments in a game of timing, coordination, and clout.

### MOBnet Slang (Mini Glossary)

- **The Taofather** — Subnet owner / protocol figurehead. Runs the city, sets the tone.
- **Boss** — A hit sponsor. Posts jobs by depositing MOB-α and setting terms.
- **Mobsters (Miners)** — Hit participants. Provide target alpha to the pool and earn TAO payouts + MOB-α envelopes.
- **Consiglieres (Validators)** — The bookkeepers. Compute Street Heat, validate hits, and publish settlements.
- **Hit** — A single coordinated, batched sell of pooled target alpha resulting in TAO.
- **Hit Board / Wall of Jobs** — Public listing of open and completed hits + heat scores + lore.
- **Street Tax** — Upfront, non-refundable burn paid by the Boss.
- **Escrow** — Boss’s locked MOB-α that gets “washed” back (bounded return).
- **Wash** — Returning escrowed MOB-α; the “lost slice” becomes wash burn + blessing.
- **Washing Fee** — The portion of escrow loss that is burned forever (parameter `psi`).
- **The Blessing** — The Taofather’s cut from escrow loss (the remainder `1-psi`).
- **Family Vault** — Protocol treasury that receives Boss vault flows and other routed flows.
- **House TAO** — The settlement asset for hit proceeds.
- **The Rake** — The Taofather’s TAO cut from every hit (set to **5%**).
- **Kickback** — Boss bonus from TAO proceeds (**1–3%** depending on success).
- **The Envelope** — Epoch reward budget distributed as MOB-α to Mobsters.
- **Heat Window** — Pool-fill timeout; if it ends, rules decide refund vs execution policy.
- **Street Price / Tape** — Reference price inputs used for accounting (example: `p_alpha`, `P0`); not a guarantee.

### Roles

- **Bosses (Hit Sponsors)**  
  Put up MOB-α, name your target, define terms, and put the hit out.  
  **ANYONE can be a Boss.**

- **Mobsters (Miners / Crew)**  
  They join hits by depositing the target subnet’s alpha into the pool.  
  **ANYONE can be a Mobster.**  
  (“Mobsters (miners)” means hit participants — not necessarily registered Bittensor miner UIDs.)

- **Consiglieres (Validators / Bookkeepers)**  
  They:
  - track prices and liquidity/depth metrics,
  - compute Street Heat and validate jobs,
  - publish settlements and leaderboards.

> **Consiglieres Fee Policy (current):** **0%** of the TAO rake.  
> Compensation (if any) is via reputation, governance influence, or optional future envelope routing.

### The MOB-α Token (MOBnet's Alpha token)

MOB-α is the Family’s currency:

- Bosses must acquire and deposit MOB-α to open hits.
- A slice is burned up front (Street Tax), most is escrowed (washable), and a slice goes to the Family Vault.
- A protocol-defined epoch Envelope can pay MOB-α rewards to active Mobsters.

### Ranks, Families, and Reputation

To make MOBnet feel like a game (not just math), the protocol leans into **identity and history**:

**Boss Ranks (by successful sponsorship):**  
Associate → Capo → Underboss → Don

**Mobster Ranks (by successful crew runs):**  
Runner → Soldier → Made → Enforcer

**Consigliere Titles (by accuracy/uptime):**  
Accountant → Consigliere → The Commission

**Families (teams):**
- Mobsters may affiliate with a Family (tag / registry / optional on-chain mapping).
- Families have leaderboards (volume, heat, win-rate).
- Optional: a small portion of the Envelope can go to top Families (purely tunable).

**Hit Board “After-Action Dossier”:**
- Tags: **CLEAN / MESSY / BOTCHED / LEGENDARY**
- Heat level, witnesses (participants), payout summary, and lore lines.

---

## Hit Mechanics

A Boss targets subnet `T` and sets:

- Hit pool size `Q_T`: total units of subnet `T`’s alpha to collect.
- MOB-α deposit `A_boss`: Boss skin in the game.
- Heat Window: time allowed for pool fill.

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

#### Updated Deposit Split (Street Tax = 5%)

**Street Tax (burn):** 5%  
**Escrow (washable):** 85%  
**Family Vault:** 10%

$$
A_{burn,instant} = 0.05 \, A_{boss},\quad
A_{esc} = 0.85 \, A_{boss},\quad
A_{vault} = 0.10 \, A_{boss}
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

### 4. Settlement, Rake, and Kickbacks

**Updated TAO weights (from proceeds `V_hit`):**
- **Taofather Rake:** **5%**
- **Consiglieres:** **0%**
- **Boss Kickback:** **1%–3%** depending on success
- Remaining goes to the **Crew (Mobsters)**

Let:
- `t = 0.05` (Taofather)
- `c = 0.00` (Consiglieres)
- `b(I'_{hit}) ∈ [0.01, 0.03]` (Boss kickback schedule)

Then:

$$
V_{taofather} = t \cdot V_{hit}
$$

$$
V_{boss} = b(I'_{hit}) \cdot V_{hit}
$$

Crew payout pot:

$$
V_{mob} = (1 - t - c - b(I'_{hit}))\cdot V_{hit}
= (0.95 - b(I'_{hit}))\cdot V_{hit}
$$

Base payout to Mobster `i`:

$$
Payout_{i,base} = V_{mob}\cdot \frac{d_i}{\sum_j d_j}
$$

#### Kickback schedule (1% → 3% by success)

Use Street Heat `I'_{hit}` to scale kickback.

Choose thresholds:
- `I_{success}` (where kickback starts ramping)
- `I_{legend}` (where kickback maxes)

A simple linear ramp with a **minimum 1%**:

$$
b(I')=
\begin{cases}
0.01 & I' < I_{success}\\
0.01 + 0.02\cdot\frac{I' - I_{success}}{I_{legend}-I_{success}} & I_{success}\le I' \le I_{legend}\\
0.03 & I' > I_{legend}
\end{cases}
$$

**Interpretation:** bosses always get *some* kickback (1%), but truly successful hits push it toward 3%.

> If you prefer “no kickback on botched hits,” set the first branch to `0` instead of `0.01`. Current policy is **1–3%** as requested.

---

## Street Heat (Impact Scoring)

### Price Shock

$$
\Delta P = \frac{P0 - P1}{P0}
$$

### Normalized Shock

$$
I_{hit} = \min\left(1,\; \max\left(0,\; \frac{\Delta P}{\Delta P_{max}}\right)\right)
$$

Interpretation:
- `I_hit ≈ 0`: the streets barely noticed.
- `I_hit ≈ 1`: max-scored shock.

### Size-Adjusted Heat (Alpha-Equivalent Depth)

Let `R_{TAO,T}` be the TAO-side reserve/depth metric for subnet `T`.

Alpha-equivalent depth:

$$
L_T = \frac{R_{TAO,T}}{P0}
$$

Smooth to reduce gamesmanship:

$$
L_T^{smooth} = EMA(L_T)
$$

Size-adjusted heat:

$$
I'_{hit} = I_{hit}\cdot \frac{Q_T}{L_T^{smooth} + \epsilon}
$$

---

## The Envelope (Emissions & MOB-α Rewards)

### Epoch Reward Budget

Epoch envelope pool:

$$
E_{rewards,epoch}\quad (\text{in MOB-}\alpha)
$$

### Allocating Envelopes to Hits

For each hit `h`:

$$
s_h = \frac{V_{hit,h}}{\sum_k V_{hit,k}}\cdot \left(1+\kappa\cdot I'_{hit,h}\right)
$$

Then allocate:

$$
E_{hit,h} = E_{rewards,epoch}\cdot \frac{s_h}{\sum_j s_j}
$$

### Allocating Envelopes Within a Hit

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

### Making Crew Runs Slightly +EV vs Solo Selling

Solo (approx):

$$
Solo_i \approx P_{solo}\cdot d_i
$$

Crew run (hit) (approx):

$$
Hit_i \approx Payout_{i,base} + p_{\alpha}\cdot R_i
$$

Tuning target:

$$
\mathbb{E}[Hit_i] \gtrsim \mathbb{E}[Solo_i]
$$

---

## Tribute, Wash, and the Blessing (Boss Collateral)

Escrow:

$$
A_{esc} = 0.85\,A_{boss}
$$

Minimum escrow return:

$$
\beta_{min} = 0.8
$$

Returned escrow (wash curve):

$$
A_{returned} = A_{esc}\cdot \left(\beta_{min} + (1-\beta_{min})\cdot \min(1,\; I'_{hit})\right)
$$

Lost escrow:

$$
A_{lost} = A_{esc} - A_{returned}
$$

Split the loss into burn + blessing:

$$
A_{wash,burn} = \psi\cdot A_{lost},\quad
A_{taofather,blessing} = (1-\psi)\cdot A_{lost}
$$

Totals:

$$
A_{burn,total} = 0.05\,A_{boss} + \psi\cdot (A_{esc}-A_{returned})
$$

$$
A_{vault,total} = 0.10\,A_{boss} \quad (\text{plus optional routed flows})
$$

> **Boss incentive design:** Bosses always pay the Street Tax (5%). But successful hits (high heat) increase escrow return **and** increase their TAO kickback from **1% → 3%**.

---

## Worked Example: “The 10k Hit on Subnet 1”

### Setup

- `A_boss = 1000` MOB-α
- `Q1 = 10000` alpha_1
- `DeltaP_max = 0.5`
- `beta_min = 0.8`
- `psi = 0.5`

Updated TAO weights:
- Taofather: `t=0.05`
- Consiglieres: `c=0.00`
- Boss kickback: `b(I') ∈ [0.01,0.03]`

Example pricing assumptions (example only):
- `P0 = 0.08` TAO per alpha_1
- `p_alpha = 0.005` TAO per MOB-α (reference input for comparisons only)

Mobsters:
- Alice: `dA = 5000`, `HA = 400`
- Boris: `dB = 3000`, `HB = 300`
- Cara: `dC = 2000`, `HC = 300`

### Boss Deposit Breakdown

$$
A_{burn,instant}=50,\quad A_{esc}=850,\quad A_{vault}=100 \quad (\text{MOB-}\alpha)
$$

### Pool, Price, and TAO Settlement

Assume:
- `P1 = 0.036` TAO per alpha_1
- `V_hit = 500` TAO

Assume `I'_{hit}` qualifies as a strong success (so kickback near max).  
Let `b(I') = 0.03` for illustration.

Taofather rake:

$$
V_{taofather} = 0.05\cdot 500 = 25
$$

Boss kickback:

$$
V_{boss} = 0.03\cdot 500 = 15
$$

Crew pot:

$$
V_{mob} = (0.95 - 0.03)\cdot 500 = 460
$$

Base payouts:

$$
Payout_{A,base} = 460\cdot 0.50 = 230
$$

$$
Payout_{B,base} = 460\cdot 0.30 = 138
$$

$$
Payout_{C,base} = 460\cdot 0.20 = 92
$$

(If the hit were weaker and `b(I')=0.01`, the crew pot would be `470` instead of `460`.)

### Street Heat & Boss Wash (80% Minimum Return)

$$
\Delta P = \frac{0.08-0.036}{0.08} = 0.55,\quad I_{hit}=1
$$

Assume validator-observed:
- `R_{TAO,1} = 1600` TAO

$$
L_1 = \frac{1600}{0.08} = 20000
$$

$$
I'_{hit} \approx 1\cdot \frac{10000}{20000} = 0.5
$$

$$
A_{returned} = 850\cdot (0.8 + 0.2\cdot 0.5) = 850\cdot 0.9 = 765
$$

$$
A_{lost}=85,\quad A_{wash,burn}=42.5,\quad A_{taofather,blessing}=42.5
$$

### Envelope Rewards

Use a tunable envelope rule tied to hit volume:

Let `r` be the fraction of hit volume returned as MOB-α incentives:

$$
E_{hit} = \frac{r\cdot V_{hit}}{p_{\alpha}}
$$

For this example: `r = 0.04`, `V_hit = 500`, `p_alpha = 0.005`:

$$
E_{hit} = \frac{0.04\cdot 500}{0.005} = 4000
$$

Allocate within the hit (use `gamma = 1.0`, `delta = 0.5`).

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

### Crew Run vs Solo Sell

Solo baseline at avg `0.05` TAO per alpha:
- Alice: 250
- Boris: 150
- Cara: 100

Crew run outcomes (base + illustrative MOB-α bonus):
- Alice: `230 + 10.71 = 240.71`
- Boris: `138 + 5.56 = 143.56`
- Cara: `92 + 3.73 = 95.73`

> The “slightly +EV” property is achieved by tuning the Envelope (`r`, `E_epoch`, and allocation weights).  
> The TAO rake (5%) + kickback (1–3%) reduce base TAO, but the Envelope is designed to more than compensate for active crews.

---

## Value Proposition

### For The Taofather

**The Rackets (explicit revenue streams):**
1) **The Rake (TAO):** `5%` of every hit’s TAO proceeds  
2) **The Blessing (MOB-α):** `(1-ψ)` of Boss escrow loss  
3) **Family Vault (MOB-α):** `10%` of every Boss deposit  
4) **Street Tax (burn):** 5% burn scales with usage (scarcity + lore)

**Narrative moat:** volatility gets weaponized into public lore — a Hit Board people watch.

### For Bosses, Mobsters, and Consiglieres

**Bosses**
- Clear cost: **Street Tax** is known (5% burn).
- Bounded risk: escrow return is formula-driven (**80–100% of escrow** depending on heat).
- **Enticed upside:** Boss earns a TAO **Kickback** (**1–3% of `V_hit`**) that increases with success.

**Mobsters (Crew)**
- No UID required: anyone can participate by contributing target alpha.
- Two-layer payout: (1) proportional TAO from the crew pot, plus (2) Envelope rewards (MOB-α).
- Loyalty matters: holding MOB-α can increase Envelope share (delta-tunable).
- Clout system: ranks, Families, job history, “made man” progression.

**Consiglieres (Validators / Bookkeepers)**
- Define street rules: smoothing windows, depth sources, shock caps, anti-gaming checks.
- Score and publish: compute Street Heat, validate hits, and publish settlements + leaderboards.
- Current fee policy: **0% of TAO rake** (compensation is optional via future governance or envelope routing).

---

## FAQ

**Q: Is this financial advice?**  
A: No.

**Q: What is MOB-α “worth” in this README?**  
A: The example uses `p_alpha` only for TAO-equivalent comparisons. It is not a peg or guarantee.

**Q: Why would a Boss post hits?**  
A: Bosses have skin in the game (Street Tax + wash risk), but successful hits increase escrow return and unlock a higher TAO kickback (1–3% of proceeds).

**Q: How is Street Heat computed?**  
A: Validators compute a normalized shock `I_hit`, then scale it by size vs smoothed depth:  
`I' = I_hit * Q_T / (L_smooth + eps)`.

**Q: What prevents gamesmanship?**  
A: Smoothing (EMA/TWAP), reserve-source diversity, min-fill and anti-sybil rules (policy choice), and public auditability of hit settlement math.

---

