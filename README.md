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
- [License / Use](#license--use)

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

MobNet funds MOB-α rewards with a **protocol-defined epoch budget** (the **Envelope**), backed by fees and treasury flows (and optionally validator-governed conversions of subnet reward inflows into MOB-α). Parameters can be tuned so that:

> Over time, **Mobsters usually do slightly better (in expectation)** running hits than dumping alone.

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

- **The Taofather** — Subnet owner / protocol figurehead. Runs the city, sets the tone.  
- **Boss** — A hit sponsor. Posts jobs by depositing MOB-α and setting terms.  
- **Mobsters (Miners)** — Hit participants. Provide target alpha to the pool and earn payouts + MOB-α rewards.  
- **Consiglieres (Validators)** — Scorers/validators. Keep the books, compute impact, decide reward splits.  
- **Hit** — A single coordinated, batched sell of pooled target alpha into TAO.  
- **Hit Board / Wall of Jobs** — Public listing of open and completed hits + impact scores and lore.  
- **Street Tax** — Upfront, non-refundable burn on the Boss deposit.  
- **Escrow / Collateral** — Boss’s locked MOB-α that gets “washed” back 80–100% depending on impact.  
- **Wash** — The process of returning escrowed MOB-α to the Boss. The “lost slice” becomes wash burn + blessing fee.  
- **Washing Fee** — The portion of lost escrow that is burned forever (parameter \( \psi \)).  
- **The Blessing** — The Taofather’s extra cut from lost escrow (the remainder \( 1-\psi \)).  
- **Family Vault** — Protocol treasury that receives the Boss treasury cut and other routed flows.  
- **House TAO** — The settlement asset for hit proceeds (the “house” settles in TAO).  
- **House Cut** — The protocol fee \( f \) taken from hit proceeds before base payouts.  
- **Envelope** — The epoch rewards budget distributed as MOB-α to Mobsters (miners).  
- **Heat Window** — The pool-fill timeout; if it ends, rules decide refund vs partial execution.  
- **Street Price / Tape** — Reference price inputs used for accounting (e.g., \( p_\alpha \), \( P_0 \)); not a guarantee.

### Roles

- **Bosses (Hit Sponsors)**  
  Put up MOB-α, name the target, set the terms, and light the fuse.  
  **ANYONE can be a boss.**

- **Mobsters (Miners)**  
  The crew. They join hits by depositing the target subnet’s alpha into the pool.  
  They’re scored and paid by Consiglieres based on participation and MOB-α loyalty.  
  **ANYONE can be a miner (no miner uid or registration required).**

  In this README, **‘Mobsters (miners)’** means hit participants (not necessarily registered Bittensor miner UIDs). Payouts come from the MobNet payout desk (distributor/treasury), based on validator scoring.

- **Consiglieres (Validators)**  
  The accountants with the books. They:
  - track prices and liquidity/depth metrics,  
  - compute impact scores and validate jobs,  
  - score Mobsters (miners),  
  - and decide how envelopes and collateral flows get split.

### The MOB-α Token (MOBnet's Alpha token)

MOB-α is the Family’s currency:

- Bosses **must acquire and deposit MOB-α** to open hits.  
- A fixed fraction is **burned** up front (street tax), another portion is **escrowed** (collateral), and a portion goes to the **Family Vault** (treasury).  
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
- \( k \): margin factor (MOB-α per 1 TAO of hit notional)  
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

To make big targets cheaper per unit notional (encourage big-game hunting), apply:

$$
g(\tilde{S}_T) = \frac{1}{1 + \lambda \cdot \tilde{S}_T}
$$

with \( \lambda \in [0,1] \), then:

$$
A_{\text{boss}} = \max\left(
  A_{\min},\;
  k \cdot \frac{Q_T \cdot P_0}{p_\alpha} \cdot g(\tilde{S}_T)
\right)
$$

#### Deposit Split

The Boss deposit is split three ways:

- **Street tax (instant burn):** 20%  
- **Escrow (collateral):** 70%  
- **Family Vault (treasury):** 10%

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

Pick a max meaningful drop \( \Delta P_{\max} \) (e.g. 0.3–0.5):

$$
I_{\text{hit}} = \min\left(1, \max\left(0, \frac{\Delta P}{\Delta P_{\max}}\right)\right)
$$

- \( I_{\text{hit}} \approx 0 \): no real move.  
- \( I_{\text{hit}} \approx 1 \): “maxed out” shock for scoring purposes.

### Size-Adjusted Impact (Option C: Alpha-Equivalent Depth)

To compare hits across subnets fairly, validators compute **alpha-equivalent depth** from liquidity.

Let:

- \( R_{\text{TAO},T} \): TAO-side reserve / depth metric for subnet \( T \)’s alpha market (from on-chain liquidity data).  
- \( P_0 \): pre-hit price in TAO per alpha.

Define the alpha-equivalent depth:

$$
L_T = \frac{R_{\text{TAO},T}}{P_0}
$$

**Interpretation:** if the market is an AMM with reserves \( (R_{\text{TAO},T}, R_{\alpha,T}) \) and spot price \( P_0 = \frac{R_{\text{TAO},T}}{R_{\alpha,T}} \), then:

$$
L_T = \frac{R_{\text{TAO},T}}{P_0} = R_{\alpha,T}
$$

So \( L_T \) lines up with “how much alpha sits on the street,” expressed in alpha units.

Validators use a smoothed value to reduce gamesmanship:

$$
L_T^{\text{smooth}} = \text{EMA}(L_T)
$$

Size-adjusted impact:

$$
I'_{\text{hit}} = I_{\text{hit}} \cdot \frac{Q_T}{L_T^{\text{smooth}} + \epsilon}
$$

where \( \epsilon > 0 \) prevents division by zero.

---

## Emissions & MOB-α Rewards

### Epoch Reward Budget

Each epoch, MobNet sets an envelope:

$$
E_{\text{rewards,epoch}} \quad (\text{MOB-}\alpha)
$$

This is the **Envelope Pool** used to reward hit participation. (Governance can set this as a share of subnet inflows/emissions, plus fees/treasury policies.)

### Allocating Rewards to Hits

For each hit \( h \) in an epoch:

- \( V_{\text{hit},h} \): hit volume (TAO)  
- \( I'_{\text{hit},h} \): size-adjusted impact  
- \( V_{\text{total}} = \sum_k V_{\text{hit},k} \)

Define a raw score per hit:

$$
s_h = \frac{V_{\text{hit},h}}{V_{\text{total}}} \cdot \left( 1 + \kappa \cdot I'_{\text{hit},h} \right)
$$

with \( \kappa \in [0, 0.3] \) controlling how much impact boosts rewards.

Normalize to allocate the envelope:

$$
E_{\text{hit},h} = E_{\text{rewards,epoch}} \cdot \frac{s_h}{\sum_j s_j}
$$

This guarantees:

$$
\sum_h E_{\text{hit},h} = E_{\text{rewards,epoch}}
$$

### Allocating Rewards Within a Hit

For a specific hit with reward pool \( E_{\text{hit}} \) MOB-α:

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

with:

- \( \gamma \in [0.8, 1.2] \): emphasizes contribution size  
- \( \delta \in [0.3, 1.0] \): emphasizes MOB-α loyalty

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

Target tuning goal:

$$
\mathbb{E}[\text{Hit}_i] \gtrsim \mathbb{E}[\text{Solo}_i]
$$

“+EV” here means **positive expected value** relative to solo selling—**not guaranteed**, but tunable via \( f \), the envelope budget, and allocation rules.

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

Returned escrow (washed back based on impact):

$$
A_{\text{returned}}
= A_{\text{esc}} \cdot
\left( \beta_{\min} + (1 - \beta_{\min}) \cdot \min(1, I'_{\text{hit}}) \right)
$$

Lost escrow:

$$
A_{\text{lost}} = A_{\text{esc}} - A_{\text{returned}}
$$

Split the lost slice between wash burn and the Taofather’s blessing:

$$
A_{\text{wash,burn}} = \psi \cdot A_{\text{lost}},\quad
A_{\text{taofather}} = (1-\psi)\cdot A_{\text{lost}}
$$

Total burned MOB-α per hit:

$$
A_{\text{burn,total}}
= A_{\text{burn,instant}} + A_{\text{wash,burn}}
= 0.20 A_{\text{boss}} + \psi \cdot (A_{\text{esc}} - A_{\text{returned}})
$$

Total treasury intake from the Boss side:

$$
A_{\text{treasury,total}}
= A_{\text{treasury}} + A_{\text{taofather}}
= 0.10 A_{\text{boss}} + (1-\psi)\cdot (A_{\text{esc}} - A_{\text{returned}})
$$

---

## Worked Example: “The 10k Hit on Subnet 1”

This example is **illustrative** and uses a **reference price** for MOB-α.

### Setup

- \( A_{\text{boss}} = 1{,}000 \) MOB-α  
- \( Q_1 = 10{,}000 \, \alpha_1 \)  
- \( f = 0.02 \)  
- \( \Delta P_{\max} = 0.5 \)  
- \( \beta_{\min} = 0.8 \)  
- \( \psi = 0.5 \)

**Example pricing assumptions (example only):**

- \( P_0 = 0.08 \) TAO / \( \alpha_1 \)  
- \( p_\alpha = 0.005 \) TAO / MOB-α (reference price for comparisons only)

Mobsters:

- Alice: \( d_A = 5{,}000 \), \( H_A = 400 \)  
- Boris: \( d_B = 3{,}000 \), \( H_B = 300 \)  
- Cara: \( d_C = 2{,}000 \), \( H_C = 300 \)

Total holdings:

$$
H_{\text{tot}} = 1{,}000 \text{ MOB-}\alpha
$$

### Boss Deposit Breakdown

$$
A_{\text{burn,instant}} = 200,\quad A_{\text{esc}} = 700,\quad A_{\text{treasury}} = 100
\quad (\text{all in MOB-}\alpha)
$$

### Pool, Price, and Base Payouts

Assume post-hit price and realized proceeds:

- \( P_1 = 0.036 \) TAO / \( \alpha_1 \)  
- \( V_{\text{hit}} = 500 \) TAO (avg execution price \( 0.05 \) TAO/\( \alpha_1 \))

Fee and payout pool:

$$
V_{\text{fee}} = 0.02 \cdot 500 = 10 \text{ TAO},\quad
V_{\text{mob}} = 500 - 10 = 490 \text{ TAO}
$$

Contribution shares:

$$
c_A = 0.50,\quad c_B = 0.30,\quad c_C = 0.20
$$

Base payouts:

$$
\text{Payout}_{A,\text{base}} = 490 \cdot 0.50 = 245 \text{ TAO}
$$

$$
\text{Payout}_{B,\text{base}} = 490 \cdot 0.30 = 147 \text{ TAO}
$$

$$
\text{Payout}_{C,\text{base}} = 490 \cdot 0.20 = 98 \text{ TAO}
$$

Mental solo baseline at avg \( 0.05 \) TAO/\( \alpha_1 \):

- Alice: 250 TAO  
- Boris: 150 TAO  
- Cara: 100 TAO  

So on base payout alone, each Mobster is ~2% worse due to the House cut.

### Impact & Boss Collateral (80% Minimum Return)

Price drop:

$$
\Delta P = \frac{0.08 - 0.036}{0.08} = 0.55
$$

Normalized shock:

$$
I_{\text{hit}} = \min\left(1, \frac{0.55}{0.5}\right) = 1
$$

Assume validators observe TAO-side reserve depth:

- \( R_{\text{TAO},1} = 1{,}600 \) TAO

Then alpha-equivalent depth:

$$
L_1 = \frac{1{,}600}{0.08} = 20{,}000 \, \alpha_1
$$

Size-adjusted impact:

$$
I'_{\text{hit}} \approx 1 \cdot \frac{10{,}000}{20{,}000} = 0.5
$$

Returned escrow:

$$
A_{\text{returned}} = 700 \cdot (0.8 + 0.2 \cdot 0.5) = 630 \text{ MOB-}\alpha
$$

Lost escrow:

$$
A_{\text{lost}} = 700 - 630 = 70 \text{ MOB-}\alpha
$$

Split (with \( \psi = 0.5 \)):

$$
A_{\text{wash,burn}} = 35,\quad A_{\text{taofather}} = 35 \quad (\text{MOB-}\alpha)
$$

Totals:

- Burned: \( A_{\text{burn,total}} = 200 + 35 = 235 \) MOB-α  
- Treasury from Boss side: \( A_{\text{treasury,total}} = 100 + 35 = 135 \) MOB-α  

### Emissions-Funded MOB-α Rewards

Instead of arbitrarily “assuming” a reward pool, tie it to hit volume with a clear, tunable rule.

Let \( r \) be the fraction of hit volume (in TAO) returned as MOB-α incentives:

$$
E_{\text{hit}} = \frac{r \cdot V_{\text{hit}}}{p_\alpha}
$$

For this example, take \( r = 0.04 \) (4% of hit volume), \( V_{\text{hit}} = 500 \) TAO, \( p_\alpha = 0.005 \) TAO/MOB-α:

$$
E_{\text{hit}} = \frac{0.04 \cdot 500}{0.005} = \frac{20}{0.005} = 4{,}000 \text{ MOB-}\alpha
$$

> This is **illustrative** and tunable. Governance can cap \( E_{\text{hit}} \) per hit or per epoch.

Now allocate within the hit.

Loyalty shares:

$$
\ell_A = 0.40,\quad \ell_B = 0.30,\quad \ell_C = 0.30
$$

Use \( \gamma = 1.0 \), \( \delta = 0.5 \):

$$
w_A = 0.50 \cdot \sqrt{0.40} \approx 0.316,\quad
w_B = 0.30 \cdot \sqrt{0.30} \approx 0.164,\quad
w_C = 0.20 \cdot \sqrt{0.30} \approx 0.110
$$

$$
W = w_A + w_B + w_C \approx 0.590
$$

Rewards:

$$
R_A = 4{,}000 \cdot \frac{0.316}{0.590} \approx 2{,}142 \text{ MOB-}\alpha
$$

$$
R_B = 4{,}000 \cdot \frac{0.164}{0.590} \approx 1{,}112 \text{ MOB-}\alpha
$$

$$
R_C = 4{,}000 \cdot \frac{0.110}{0.590} \approx 746 \text{ MOB-}\alpha
$$

TAO-equivalent (illustrative at \( p_\alpha = 0.005 \)):

- Alice: \( 2{,}142 \cdot 0.005 \approx 10.71 \) TAO  
- Boris: \( 1{,}112 \cdot 0.005 \approx 5.56 \) TAO  
- Cara: \( 746 \cdot 0.005 \approx 3.73 \) TAO  

### Comparing Hit vs Solo Selling

Solo baseline (avg \( 0.05 \) TAO/\( \alpha_1 \)):

- Alice: 250 TAO  
- Boris: 150 TAO  
- Cara: 100 TAO  

Hit outcomes (base payout + MOB-α bonus at reference price):

- Alice: \( 245 + 10.71 = 255.71 \) TAO  
- Boris: \( 147 + 5.56 = 152.56 \) TAO  
- Cara: \( 98 + 3.73 = 101.73 \) TAO  

So the envelope offsets the House cut and makes hit participation slightly +EV **in this example**.

---

## Value Proposition

### For The Subnet Owner (“The Taofather”)

- **MOB-α demand is gameplay-driven:** bosses need MOB-α to post jobs; loyalty weighting rewards holders; activity creates demand.
- **Burns scale with usage:** every hit pays the street tax and (optionally) wash burn—supply reduction tied to protocol activity.
- **Family Vault grows with the game:** treasury flows and fees fund events, tournaments, buybacks/burns, and ecosystem tooling.
- **Narrative moat:** you’re not just a subnet—you’re the mafia district where volatility becomes spectacle and every job becomes lore.

### For Users (Bosses, Mobsters / Miners, Consiglieres / Validators)

**Bosses (Hit Sponsors)**
- **Target selection + clout:** choose a subnet, size the job \( Q_T \), and post it publicly on the Hit Board.
- **Bounded collateral risk:** escrow return is formula-driven—Boss gets at least \( \beta_{\min} \) of escrow back and up to 100% on strong impact.
- **Clear “cost of doing business”:** the street tax is the known, non-refundable cost; any additional loss is transparent (wash + blessing).
- **Flexible job design:** set pool size, timing (Heat Window), and optional constraints; governance can support private jobs, whitelists, or staged hits.

**Mobsters (Miners / Hit Participants)**
- **No UID required:** anyone can participate by contributing target alpha to a job.
- **Two-layer payout:** (1) **base TAO proceeds** from the hit sale, plus (2) **MOB-α envelope rewards** from the epoch pool.
- **Loyalty matters:** holding MOB-α can increase envelope share via \( \ell_i \) weighting (tunable by \( \delta \)).
- **Reputation and laddering:** consistent participation earns leaderboard rank, “Family” status, and priority access to future jobs (policy choice).
- **Transparency:** payout math is proportional and auditable; impact scoring is validator-published and reproducible from on-chain data.

**Consiglieres (Validators)**
- **Define the rules of the street:** set smoothing windows, depth sources, \( \Delta P_{\max} \), and anti-gaming checks.
- **Score and settle jobs:** compute \( I'_{\text{hit}} \), validate executions, and drive consensus on allocations.
- **Protect against manipulation:** smoothing, TWAP/EMA, reserve-source diversity, and minimum fill requirements reduce “fake hits.”
- **Run the payout desk:** publish distributions, resolve disputes, and maintain credibility of the Hit Board.

---

## FAQ

**Q: Is this financial advice?**  
A: No. This is a protocol/game-mechanics description, not investment advice.

**Q: What is MOB-α “worth” in this README?**  
A: The example uses a reference price \( p_\alpha = 0.005 \) TAO/MOB-α **only** for TAO-equivalent comparisons. It is not a peg or guarantee.

**Q: What does “envelopes” mean?**  
A: “Envelopes” are MOB-α rewards paid from the epoch envelope pool to hit participants—bonus on top of base TAO proceeds.

**Q: What does the subnet size metric mean and how is it determined?**  
A: Validators compute alpha-equivalent depth \( L_T = R_{\text{TAO},T}/P_0 \), smooth it, then score \( I'_{\text{hit}} = I_{\text{hit}} \cdot Q_T/(L_T^{\text{smooth}}+\epsilon) \). In an AMM, \( L_T \) corresponds to alpha reserves at the spot price.

---
