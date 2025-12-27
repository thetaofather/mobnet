<img width="938" height="690" alt="image (4)" src="https://github.com/user-attachments/assets/1009e9db-96c9-4279-ace3-6544629842d3" />

<h1 align="center">The Taofather</h1>
<h3 align="center">Turning dTAO Volatility into Mob Hits</h3>

---

## Intro

Welcome to **San Taovanni** — a mob-run district inside Tensor City.

**The Taofather** is a mob-themed Bittensor subnet where volatility becomes a public game: **Bosses** post hits, **Mobsters** form crews, and **Consiglieres** keep the books.

The Family’s currency is **MOB-α** (“Mob Alpha”). Use it to sponsor jobs, earn envelopes, climb ranks, and build a reputation that lives on the **Hit Board**.

> **Important:** Any TAO-equivalent examples use a reference input `p_alpha` for accounting. It’s not a peg and not a guarantee — it’s just the “street price” input used to compare values.

---

## The Game Loop (How It Plays)

1) **A Boss** (anyone) picks a target subnet and posts a job on the **Hit Board**  
2) Boss posts **two deposits**:
   - **MOB-α Deposit** `A_boss` (Street Tax Hold + Family Vault + Washable Escrow)
   - **Target Alpha Deposit** `X_boss` (the target subnet’s alpha, used in the hit)
3) **Mobsters** (miners) join by depositing the target subnet’s alpha into the pool  
4) Pool fills (or the **Heat Window** ends) → the hit is armed  
5) The system executes **one batched sell** (“the hit”) → TAO proceeds  
6) TAO proceeds split into: **Taofather Rake**, **Boss Kickback**, **Pool Payout**  
7) Consiglieres (validators) compute **Street Heat** (impact) and publish the dossier  
8) Boss MOB-α escrow is “washed” back (bounded), with a small loss split **burn + blessing**  
9) Mobsters earn **Envelope** rewards (MOB-α) weighted by **contribution + reputation**  
10) The job becomes lore: **BOTCHED / MESSY / CLEAN / LEGENDARY**, ranks, Families, and leaderboards

---

## Quick Rules (The Money)

### TAO settlement from every hit

When a hit executes, it produces:

- `V_hit` (TAO proceeds)

From `V_hit`, the protocol takes:

- **Taofather Rake:** **1.5%**
- **Boss Kickback:** **1%–3%** (tag-based) **× a Boss Skin multiplier**
- The rest goes to the **Pool Payout** (all contributed target alpha sold in the hit)

### Boss must “show inventory” (target alpha) to open a hit

The Boss is not just a sponsor — they must put target alpha in the pool:

- Boss posts `X_boss` units of target subnet alpha (`alpha_T`)
- A small slice of `X_boss` is skimmed to the Family Vault (in target alpha)
- The remainder is sold in the hit alongside mobster deposits

This makes the Boss a real participant in the hit’s execution.

---

## Roles

### The Taofather (Subnet Owner)
Runs the city. Sets the street rules. Collects the rake.

### Boss (Hit Sponsor)
Posts jobs. Deposits MOB-α + real target alpha. Takes bounded wash risk on MOB-α. Earns kickback + pool payout (with slight weighting).

### Mobsters (Crew / Miners)
Bring inventory (target alpha). Get paid in TAO + envelopes (MOB-α). Build reputation.

### Consiglieres (Validators / Bookkeepers)
Compute Street Heat. Validate settlement math. Publish the dossier and leaderboards.

---

## MOBnet Slang (Mini Glossary)

- **Hit** — one coordinated batched sell of pooled target alpha  
- **Hit Board / Wall of Jobs** — public list of hits (open + completed)  
- **Heat Window** — time limit for a pool to fill  
- **Street Heat** — the impact score (“did the streets feel it?”)  
- **Street Tax Hold** — Boss’s held tribute; finalized and burned after the hit  
- **Wash** — returning Boss MOB-α escrow (bounded)  
- **The Blessing** — Taofather’s share of escrow loss  
- **The Envelope** — MOB-α rewards paid to crews for running hits  
- **BOTCHED / MESSY / CLEAN / LEGENDARY** — hit tags based on heat/quality  
- **The Rake** — Taofather’s TAO cut from every hit (**1.5%**)  
- **Kickback** — Boss bonus from TAO proceeds (**1–3%**, tag-based)

---

## Boss “Skin Ratio” (Risk + Upside Slider)

Bosses should be incentivized to post hits more often, with **less downside** when they put real target alpha on the line.

We define a **Boss Skin Ratio** using a TAO-equivalent accounting comparison:

- `A_boss` = MOB-α deposit
- `X_boss` = Boss target alpha deposit (units of `alpha_T`)
- `P0` = pre-hit price of `alpha_T` in TAO (TAO per alpha)
- `p_alpha` = reference street price of MOB-α in TAO (accounting only)

Notional comparisons:

- MOB-α notional:
  
  $$N_A = A_{boss}\cdot p_{\alpha}$$

- Target-alpha notional:
  
  $$N_X = X_{boss}\cdot P0$$

Boss Skin Ratio:

$$
\rho = \frac{N_X}{N_A} = \frac{X_{boss}\cdot P0}{A_{boss}\cdot p_{\alpha}}
$$

Interpretation:
- Higher `ρ` = Boss is putting more target alpha value on the line **per unit** of MOB-α deposit.
- The protocol rewards higher `ρ` with **lower effective Street Tax**, **better wash floor**, and **slightly better kickback**.

### Recommended bands

- **Minimum to open a hit:** `ρ ≥ 0.50`
- **Recommended “serious boss” band:** `ρ = 1.0 – 2.0`
- **Cap benefits:** `ρ ≥ 3.0` (extra target alpha is allowed, but risk benefits stop increasing)

Normalize:

$$
\rho_{norm}=\text{clamp}\left(\frac{\rho-0.50}{2.00-0.50},\,0,\,1\right)
$$

---

## Boss Deposits

### A) MOB-α deposit `A_boss` (Street Tax Hold + Family Vault + Washable Escrow)

The MOB-α deposit is the Boss’s **bounded-risk** component.

- **Family Vault (fixed):** **2.5%** of `A_boss`
- **Street Tax (finalized):** base `2.5%–5%` of `A_boss`, modified by `ρ`
- **Escrow (washable):** the remainder, returned 80–90% minimum (based on `ρ`) and improved by heat

### B) Target alpha deposit `X_boss` (used in the hit)

This is the Boss’s **“neck on the line”** component.

Two rules apply:

1) **Family Vault skim (in target alpha):** **0.25%–1.00%** of `X_boss`
2) The rest goes into the hit and is sold

---

## Family Vault skim from Boss target alpha

Let `ν_X` be the target-alpha skim rate:

$$
X_{vault} = \nu_X \cdot X_{boss},\quad \nu_X \in [0.0025,\;0.01]
$$

Recommended schedule (aligned with tag quality, “clean work costs less”):

| Tag | `ν_X` (Boss target alpha to vault) |
|---|---:|
| LEGENDARY | **0.25%** |
| CLEAN | **0.50%** |
| MESSY | **0.75%** |
| BOTCHED | **1.00%** |

Target alpha actually sold for the hit:

$$
X'_{boss}=X_{boss}-X_{vault}
$$

> Note: the Family Vault receives this skim **in target alpha units** (not MOB-α). It can be held, auctioned, or used for future protocol mechanics.

---

## Boss “Neck on the Line” weighting (Boss target alpha has slightly higher TAO weight)

Because the Boss is sponsoring, facing MOB-α wash risk, and publicly “calling the hit,” their target-alpha contribution gets a small **payout weight advantage** in the TAO pool payout.

Let:
- `d_i` = Mobster `i` target alpha deposit
- `X'_{boss}` = Boss target alpha sold in hit (after vault skim)
- `ω_b` = Boss weight multiplier (slightly > 1)

Recommended:

- `ω_b = 1.10` (10% higher weight)
- optional range: `1.05 – 1.20`

Weighted total:

$$
W=\omega_b\cdot X'_{boss}+\sum_i d_i
$$

Pool payout shares:

$$
P_{boss,pool} = V_{pool}\cdot \frac{\omega_b\cdot X'_{boss}}{W}
$$

$$
P_{i,TAO} = V_{pool}\cdot \frac{d_i}{W}
$$

**Anti-gaming guardrail (recommended):**  
Only apply `ω_b > 1` if the Boss is meaningfully exposed:

$$
X'_{boss} \ge 0.10\cdot\left(X'_{boss}+\sum_i d_i\right)
$$

If not, set `\omega_b = 1.0` for that hit.

---

## Hit Tags (BOTCHED / MESSY / CLEAN / LEGENDARY)

Every completed job gets a permanent **Hit Tag** on the Hit Board.  
Tags are determined primarily by **Street Heat** `I'_{hit}`.

### Tag Thresholds (based on `I'_{hit}`)

Let `I' = I'_{hit}`:

- **BOTCHED**: `I' < 0.15`  
- **MESSY**: `0.15 ≤ I' < 0.35`  
- **CLEAN**: `0.35 ≤ I' < 0.75`  
- **LEGENDARY**: `I' ≥ 0.75`

---

## Kickback + Street Tax Schedule (Aligned to Tags)

Boss incentives have three levers:
1) **Kickback** rises with tag quality  
2) **Street Tax** falls with tag quality  
3) **Boss Skin Ratio `ρ`** further improves both (and improves wash floor)

### Base Boss Kickback `b(I')` (TAO cut of `V_hit`)

| Tag | Street Heat `I'` | Boss Kickback `b(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | **1.00%** |
| MESSY | `0.15 – 0.35` | **1.00% → 2.00%** (linear) |
| CLEAN | `0.35 – 0.75` | **2.00% → 2.75%** (linear) |
| LEGENDARY | `≥ 0.75` | **3.00%** |

$$
b(I')=
\begin{cases}
0.0100 & I' < 0.15\\
0.0100 + 0.0100\cdot\frac{I' - 0.15}{0.20} & 0.15\le I' < 0.35\\
0.0200 + 0.0075\cdot\frac{I' - 0.35}{0.40} & 0.35\le I' < 0.75\\
0.0300 & I' \ge 0.75
\end{cases}
$$

### Base Street Tax `τ(I')` (MOB-α burn of `A_boss`)

| Tag | Street Heat `I'` | Street Tax `τ(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | **5.00%** |
| MESSY | `0.15 – 0.35` | **5.00% → 4.00%** (linear) |
| CLEAN | `0.35 – 0.75` | **4.00% → 3.00%** (linear) |
| LEGENDARY | `≥ 0.75` | **2.50%** |

$$
\tau(I')=
\begin{cases}
0.0500 & I' < 0.15\\
0.0500 - 0.0100\cdot\frac{I' - 0.15}{0.20} & 0.15\le I' < 0.35\\
0.0400 - 0.0100\cdot\frac{I' - 0.35}{0.40} & 0.35\le I' < 0.75\\
0.0250 & I' \ge 0.75
\end{cases}
$$

---

## Skin Ratio modifiers (how `ρ` reduces risk and increases upside)

Using `ρ_norm` from earlier:

**Street Tax discount modifier**
$$
m_{\tau}(\rho)=1-0.30\cdot \rho_{norm}
$$

$$
\tau_{eff}(I',\rho)=\tau(I')\cdot m_{\tau}(\rho)
$$

**Kickback multiplier**
$$
m_b(\rho)=0.90+0.20\cdot \rho_{norm}
$$

$$
b_{eff}(I',\rho)=\min(0.03,\; b(I')\cdot m_b(\rho))
$$

**Wash minimum floor (improves with `ρ`)**
$$
\beta_{min}(\rho)=0.80+0.10\cdot \rho_{norm}
$$

So serious Bosses (ρ near 2.0) get:
- lower effective Street Tax
- slightly higher kickback
- a better wash floor on MOB-α escrow

---

## Hit Flow (What Actually Happens)

### 1) Boss posts a hit
Boss chooses:
- Target subnet `T`
- Pool size `Q_T` (target alpha units)
- Heat Window (timeout policy)
- MOB-α deposit `A_boss`
- Boss target alpha deposit `X_boss`

### 2) Vault skim + Crew forms
- Vault receives `X_vault = ν_X·X_boss` (target alpha)
- Boss hit contribution becomes `X'_boss = X_boss - X_vault`
- Mobsters deposit target alpha `d_i`
- Total sold in hit:

$$
Q_T = X'_{boss} + \sum_i d_i
$$

### 3) The hit executes
All pooled target alpha is sold in a single batched execution.

Output:
- `V_hit` TAO proceeds
- price moves from `P0` to `P1`

### 4) TAO is split and paid
- Taofather takes rake (**1.5%**)
- Boss gets kickback `b_eff(I',ρ)` (tag + skin adjusted)
- Pool payout pot:

$$
V_{pool} = (1 - t - b_{eff}(I',\rho))\cdot V_{hit}
$$

- Pool payout distribution uses **Boss weight** `ω_b`:

$$
W=\omega_b\cdot X'_{boss}+\sum_i d_i
$$

$$
P_{boss,pool} = V_{pool}\cdot \frac{\omega_b\cdot X'_{boss}}{W}
$$

$$
P_{i,TAO} = V_{pool}\cdot \frac{d_i}{W}
$$

### 5) The books close (MOB-α side + envelopes)
- Street Heat is calculated
- Street Tax is finalized: burn `τ_eff(I',ρ)·A_boss`
- Boss MOB-α escrow is washed back (bounded by `β_min(ρ)` and improved by heat)
- Envelope rewards are distributed (rep-weighted for Mobsters)
- The dossier is published

---

## Why Mobsters can earn more in a hit than selling solo (illustrative)

If a Mobster sells target alpha solo, they get TAO — but no **Envelope** and no **Rep-weighted upside**.

In a hit, Mobsters can earn:
1) **TAO** from the pool payout  
2) **Envelope rewards (MOB-α)** for running hits (mining MOB-α emissions)  
3) Higher future envelopes via strong **Rep**

Even if hit execution pays rake + kickback, the **Envelope** can make hit participation more attractive than solo selling over time.

> Not a profit guarantee — this is incentive design.

---

## Example Hit Board Card (Dossier)

> Reads like lore, but it still audits.

### 🧾 Case File #071 — “The Dockside Dump”
**Status:** ✅ Closed  
**Tag:** 🟢 **CLEAN**  
**Target:** Subnet `T=1` (alpha_1)  
**District:** San Taovanni — The Docks  
**Heat Window:** 2h 00m  
**Time to Fill:** 37m

### Deposits
**Boss MOB-α Deposit:** `A_boss = 1,000 MOB-α`  
**Boss Target Alpha Deposit:** `X_boss = 2,000 alpha_1`

**Mobster Deposits (target alpha):**
- Alice: `5,000`
- Boris: `3,000`
- Cara: `2,000`

### Target-alpha vault skim (CLEAN → 0.50%)
$$
\nu_X = 0.005,\quad X_{vault} = 0.005\cdot 2000 = 10\;\alpha_1
$$

So Boss alpha sold:

$$
X'_{boss} = 2000 - 10 = 1990\;\alpha_1
$$

Total sold:

$$
Q_T = 1990 + (5000+3000+2000) = 11,990\;\alpha_1
$$

### Settlement (TAO)
**Proceeds:** `V_hit = 500 TAO`  
**Taofather Rake (1.5%):** `7.5 TAO`

**Street Heat:** `I' = 0.50` → Tag **CLEAN**

Base kickback at `I'=0.50`:

$$
b(0.50)=0.0200 + 0.0075\cdot\frac{0.50-0.35}{0.40}=0.0228125
$$

Assume Boss has solid skin ratio (`ρ_norm ≈ 0.67`), so:

$$
m_b(\rho)=0.90+0.20\cdot 0.67\approx 1.033
$$

$$
b_{eff}\approx 0.0228125\cdot 1.033 = 0.02357
$$

**Boss Kickback:** `0.02357 * 500 = 11.785 TAO`

Pool pot:

$$
V_{pool} = 500 - 7.5 - 11.785 = 480.715\;TAO
$$

### Boss-weighted pool payout
Use `ω_b = 1.10` and Boss eligibility holds (Boss is >10% of raw pool).

Weighted total:

$$
W = 1.10\cdot 1990 + (5000+3000+2000)=2189+10000=12189
$$

Pool payouts:

- Boss pool share: `2189 / 12189 = 17.96%`  
- Alice: `5000 / 12189 = 41.01%`  
- Boris: `3000 / 12189 = 24.61%`  
- Cara: `2000 / 12189 = 16.41%`

So:

- **Boss pool payout:** `0.1796 * 480.715 ≈ 86.38 TAO`  
- **Alice:** `≈ 197.90 TAO`  
- **Boris:** `≈ 118.30 TAO`  
- **Cara:** `≈ 78.15 TAO`

**Boss total TAO (kickback + pool payout):**
- `11.785 + 86.38 ≈ 98.17 TAO`

> This is the key Boss incentive: they earn like a participant (and get a slight weight advantage) *plus* they get kickback.

### Boss Tribute (MOB-α)
**Boss Deposit:** `A_boss = 1,000 MOB-α`  
**Family Vault (2.5%):** `25 MOB-α`

Street Tax (CLEAN at `I'=0.50`):

$$
\tau(0.50)=0.0400 - 0.0100\cdot\frac{0.50-0.35}{0.40}=0.03625
$$

Assume `ρ_norm≈0.67`:

$$
m_{\tau}(\rho)=1-0.30\cdot 0.67\approx 0.80
$$

$$
\tau_{eff}\approx 0.03625\cdot 0.80=0.029
$$

So **Street Tax burned:** `29.0 MOB-α`

**Escrow (washable):**
$$
A_{esc}=A_{boss}-A_{vault}-A_{tax}=1000-25-29=946
$$

### Wash Result (β_min improves with ρ)
$$
\beta_{min}(\rho)=0.80+0.10\cdot 0.67\approx 0.867
$$

$$
A_{returned}=A_{esc}\cdot\left(\beta_{min}+(1-\beta_{min})\cdot \min(1,I')\right)
$$

At `I'=0.50`:

$$
A_{returned}\approx 946\cdot(0.867+0.133\cdot 0.5)=946\cdot 0.9335\approx 883.7
$$

Lost:

$$
A_{lost}\approx 62.3
$$

Split loss (`ψ=0.5`):

$$
A_{wash,burn}\approx 31.15,\quad A_{taofather,blessing}\approx 31.15
$$

### Envelope (MOB-α) *(illustrative, rep-weighted)*
**Envelope Paid:** `4,000 MOB-α`

Mobsters’ envelope weights depend on:
- target alpha contribution
- reputation (Rep)

So a high-Rep mobster can earn more envelope than their raw %.

---

# Appendix A — The Books (Math & Definitions)

> Everything below is the accounting and scoring layer.

---

## A1) Boss Deposit Rule (Sizing)

Boss deposit can be tied to notional size:

- `Q_T`: pool sold (units of target alpha)
- `P0`: pre-hit alpha price (TAO per alpha)
- `p_alpha`: MOB-α reference street price (TAO per MOB-α)
- `k`: margin factor (MOB-α per 1 TAO of hit notional)
- `A_min`: minimum deposit

Base:

$$
A_{boss}^{base} = k \cdot \frac{Q_T \cdot P0}{p_{\alpha}}
$$

Minimum:

$$
A_{boss} = \max\left(A_{min},\; A_{boss}^{base}\right)
$$

---

## A2) Boss Deposit Split (MOB-α side)

Let `v = 0.025` be the fixed vault share.

Street tax burned:

$$
A_{tax} = \tau_{eff}(I',\rho)\cdot A_{boss}
$$

Family Vault:

$$
A_{vault} = v\cdot A_{boss}
$$

Escrow:

$$
A_{esc} = A_{boss}-A_{vault}-A_{tax}
$$

---

## A3) Boss Target Alpha Vault Skim

$$
X_{vault}=\nu_X\cdot X_{boss}
$$

$$
X'_{boss}=X_{boss}-X_{vault}
$$

Total sold:

$$
Q_T=X'_{boss}+\sum_i d_i
$$

---

## A4) TAO Settlement Weights (Boss-weighted pool payout)

From hit proceeds `V_hit`:
- Taofather rake `t = 0.015`
- Boss kickback `b_eff(I',\rho)`

$$
V_{taofather}=t\cdot V_{hit}
$$

$$
V_{boss,kick}=b_{eff}(I',\rho)\cdot V_{hit}
$$

Pool payout pot:

$$
V_{pool}=(1-t-b_{eff}(I',\rho))\cdot V_{hit}
$$

Boss-weighted denominator:

$$
W=\omega_b\cdot X'_{boss}+\sum_i d_i
$$

Boss pool payout:

$$
P_{boss,pool}=V_{pool}\cdot \frac{\omega_b\cdot X'_{boss}}{W}
$$

Mobster TAO payout:

$$
P_{i,TAO}=V_{pool}\cdot \frac{d_i}{W}
$$

Boss total TAO:

$$
P_{boss,total}=V_{boss,kick}+P_{boss,pool}
$$

---

## A5) Street Heat (Impact Scoring)

Price shock:

$$
\Delta P = \frac{P0 - P1}{P0}
$$

Normalized shock:

$$
I_{hit} = \min\left(1,\; \max\left(0,\; \frac{\Delta P}{\Delta P_{max}}\right)\right)
$$

Alpha-equivalent depth:

$$
L_T = \frac{R_{TAO,T}}{P0}
$$

Smoothed depth:

$$
L_T^{smooth} = EMA(L_T)
$$

Size-adjusted heat:

$$
I'_{hit} = I_{hit}\cdot \frac{Q_T}{L_T^{smooth} + \epsilon}
$$

---

## A6) The Envelope (Emissions & MOB-α Rewards) — Rep affects MOB-α only

Epoch envelope pool:

$$
E_{rewards,epoch}\quad (\text{in MOB-}\alpha)
$$

Allocate to hits:

$$
s_h=\frac{V_{hit,h}}{\sum_k V_{hit,k}}\cdot (1+\kappa\cdot I'_{hit,h})
$$

$$
E_{hit,h}=E_{rewards,epoch}\cdot \frac{s_h}{\sum_j s_j}
$$

Allocate within a hit (mobsters only):

Contribution share:

$$
c_i=\frac{d_i}{\sum_j d_j}
$$

Reputation share:

$$
r_i=\frac{Rep_i}{\sum_j Rep_j}
$$

Weight:

$$
w_i=c_i^{\gamma}\cdot r_i^{\delta}
$$

Reward:

$$
R_{i,MOB\alpha}=E_{hit}\cdot \frac{w_i}{\sum_k w_k}
$$

**Constraint (intentional):**
- TAO payout ignores Rep
- Rep only affects MOB-α envelopes

---

## A7) Tribute, Wash, and the Blessing (Boss MOB-α Escrow Return)

Minimum return depends on Boss skin ratio:

$$
\beta_{min}(\rho)=0.80+0.10\cdot \rho_{norm}
$$

Returned escrow:

$$
A_{returned}=A_{esc}\cdot\left(\beta_{min}(\rho)+(1-\beta_{min}(\rho))\cdot \min(1,\; I'_{hit})\right)
$$

Lost escrow:

$$
A_{lost}=A_{esc}-A_{returned}
$$

Split loss:

$$
A_{wash,burn}=\psi\cdot A_{lost},\quad
A_{taofather,blessing}=(1-\psi)\cdot A_{lost}
$$

Total burn:

$$
A_{burn,total}=A_{tax}+\psi\cdot (A_{esc}-A_{returned})
$$

Vault total:

$$
A_{vault,total}=0.025\,A_{boss}
$$

---

## Value Proposition

### For MOB-α holders
- Bosses must buy MOB-α to sponsor hits
- Street Tax burns MOB-α (tag + skin adjusted)
- Bosses posting hits increases MOB-α utility and demand

### For Bosses
- You must post real target alpha — you’re a real participant
- Your target alpha gets a slight payout weight advantage (`ω_b`)
- Higher skin ratio reduces Street Tax and improves wash floor
- Kickback scales with hit quality and improves with skin

### For Mobsters
- TAO payout is transparent
- Envelopes (MOB-α) reward hit participation
- Rep increases envelope weight over time

### For Consiglieres
- Publish heat, payouts, and rep
- Protect the streets from manipulation

---

## FAQ

**Q: Is this financial advice?**  
A: No.

**Q: Is `p_alpha` a peg?**  
A: No. It’s a reference input used for accounting examples.

**Q: Does Mobster reputation affect TAO payouts?**  
A: No. Rep only affects MOB-α envelopes.

**Q: Why does the Boss get a slight weight boost on their target alpha?**  
A: They’re taking extra risk (MOB-α wash exposure) and publicly sponsoring the hit. The boost is small and gated by minimum participation.

---
