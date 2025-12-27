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
- The rest goes to the **Pool Payout** (sold target alpha → TAO)

### Boss must “show inventory” (target alpha) to open a hit

The Boss is not just a sponsor — they must put target alpha in the pool:

- Boss posts `X_boss` units of target subnet alpha (`alpha_T`)
- A small slice of `X_boss` is skimmed to the Family Vault (in target alpha)
- The remainder is sold in the hit alongside mobster deposits

This makes the Boss a real participant in the hit’s execution.

### Critical payout separation

Every hit produces **two** independent payouts:

1) **TAO payout**: from selling pooled target alpha  
   - **Only** proportional to how much target alpha you contributed to the pool  
   - **Not** influenced by reputation, MOB-α, or anything else  
2) **MOB-α Envelope payout**: the “mining” reward  
   - **Is** influenced by contribution **and** reputation (Rep)  
   - Paid in MOB-α, not TAO

---

## Roles

### The Taofather (Subnet Owner)
Runs the city. Sets the street rules. Collects the rake.

### Boss (Hit Sponsor)
Posts jobs. Deposits MOB-α + real target alpha. Takes bounded wash risk on MOB-α. Earns kickback + TAO from their target alpha sale.

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

## Ranks, Families, and Reputation

This is a game. Your history matters.

### Boss Ranks (by successful sponsorship)
Associate → Capo → Underboss → Don

### Mobster Ranks (by successful crew runs)
Runner → Soldier → Made → Enforcer

### Families (Teams)
Mobsters can affiliate with a **Family** (tag/registry). Families have:
- leaderboards (volume, heat, win-rate)
- “made men” lists
- rivalries (optional narrative layer)

### Mobster Reputation (Rep)
Reputation is a rolling score (validators compute & publish it) that reflects:
- participation volume and consistency  
- quality outcomes (CLEAN/LEGENDARY bias)  
- penalties for griefing/aborts/bad behavior  

**Rep affects MOB-α Envelopes only** — not TAO.

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

## Hit Tags (BOTCHED / MESSY / CLEAN / LEGENDARY)

Every completed job gets a permanent **Hit Tag** on the Hit Board.  
Tags are determined primarily by **Street Heat** `I'_{hit}` (impact adjusted by depth), plus basic execution checks.

### Tag Thresholds (based on `I'_{hit}`)

Let `I' = I'_{hit}`:

- **BOTCHED**: `I' < 0.15`  
  *“The streets barely noticed.”*

- **MESSY**: `0.15 ≤ I' < 0.35`  
  *“A move happened, but it didn’t land clean.”*

- **CLEAN**: `0.35 ≤ I' < 0.75`  
  *“Solid impact. Efficient execution.”*

- **LEGENDARY**: `I' ≥ 0.75`  
  *“Everybody felt it. This one goes on the wall.”*

---

## Kickback + Street Tax Schedule (Aligned to Tags)

Boss incentives have two tag-aligned levers:
1) **Kickback** (TAO, paid out of `V_hit`) rises with tag quality  
2) **Street Tax** (MOB-α, burned out of `A_boss`) falls with tag quality  

Then the Boss Skin Ratio `ρ` further modifies both (see below).

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

Using `ρ_norm`:

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

## Boss Deposits (What Exactly Is Required)

### 1) MOB-α deposit `A_boss`
The MOB-α deposit is the Boss’s bounded-risk component:

- **Family Vault:** `v = 2.5%` of `A_boss`
- **Street Tax burned:** `τ_eff(I',ρ)·A_boss` (tag + skin adjusted)
- **Escrow (washable):** remainder, returned per wash formula (bounded by `β_min(ρ)`)

### 2) Target alpha deposit `X_boss`
The Boss must post real target alpha, which is used in the hit:

- **Family Vault skim (target alpha):** `ν_X·X_boss` where `ν_X ∈ [0.25%, 1.00%]`
- **Sold in hit:** `X'_boss = X_boss - X_vault`

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

Target alpha sold for the hit:

$$
X'_{boss}=X_{boss}-X_{vault}
$$

---

## Hit Flow (What Actually Happens)

### 1) Boss posts a hit
Boss chooses:
- Target subnet `T`
- Heat Window (timeout policy)
- MOB-α deposit `A_boss`
- Boss target alpha deposit `X_boss`

### 2) Crew forms (pool builds)
- Vault receives target alpha skim `X_vault = ν_X·X_boss`
- Boss hit contribution becomes `X'_boss = X_boss - X_vault`
- Mobsters deposit target alpha `d_i`

Total target alpha sold in the hit:

$$
Q_T = X'_{boss} + \sum_i d_i
$$

### 3) The hit executes
All pooled target alpha is sold in a single batched execution.

Output:
- `V_hit` TAO proceeds
- price moves from `P0` to `P1`

### 4) TAO is split and paid (TAO is strict pro-rata by target alpha)
- Taofather takes rake `t = 1.5%`
- Boss gets kickback `b_eff(I',ρ)` (tag + skin adjusted)
- Remaining TAO goes to the pool pot:

$$
V_{pool} = (1 - t - b_{eff}(I',\rho))\cdot V_{hit}
$$

Then TAO is paid **purely** proportional to target alpha contributed to the hit:

$$
P_{k,TAO}=V_{pool}\cdot \frac{d_k}{Q_T}
$$

Where:
- For Boss, `d_k = X'_boss`
- For Mobster `i`, `d_k = d_i`

### 5) The books close (MOB-α side + envelopes)
- Street Heat is calculated
- Street Tax is finalized: burn `τ_eff(I',ρ)·A_boss`
- Boss MOB-α escrow is washed back (bounded by `β_min(ρ)` and improved by heat)
- Envelope rewards are distributed (rep-weighted for Mobsters)
- The dossier is published

---

## Why Mobsters can earn more in a hit than selling solo (illustrative)

If a Mobster sells target alpha solo, they get TAO — but no **Envelope** and no **Rep-weighted upside**.

In a hit, Mobsters earn:
1) **TAO** from the pool sale (strict pro-rata by target alpha)  
2) **MOB-α Envelopes** for running hits (mining rewards)  
3) Increasing future envelopes if they maintain strong **Rep**

Even if hit execution pays rake + kickback, the **Envelope** can make hit participation more attractive than solo selling over time.

> Not a profit guarantee — this is incentive design.

---

## Example Hit Board Card (Dossier)

> Reads like lore, but it still audits.  
> **Important:** This example shows **two separate payouts**:
> 1) **TAO payout** from selling pooled target alpha — **purely pro-rata by contributed target alpha**.  
> 2) **MOB-α Envelope payout** — paid in MOB-α and **rep-weighted**.

### 🧾 Case File #071 — “The Dockside Dump”
**Status:** ✅ Closed  
**Tag:** 🟢 **CLEAN**  
**Target:** Subnet `T=1` (alpha_1)  
**District:** San Taovanni — The Docks  
**Heat Window:** 2h 00m  
**Time to Fill:** 37m

---

### Deposits (what gets sold)
**Boss MOB-α Deposit:** `A_boss = 1,000 MOB-α` *(used for tax/vault/escrow only — not converted)*  
**Boss Target Alpha Deposit:** `X_boss = 2,000 alpha_1`

**Mobster Target Alpha Deposits:**
- Alice: `5,000 alpha_1`
- Boris: `3,000 alpha_1`
- Cara: `2,000 alpha_1`

---

### Boss Target-Alpha Vault Skim (CLEAN → 0.50%)
$$
\nu_X = 0.005,\quad X_{vault} = 0.005\cdot 2000 = 10\;\alpha_1
$$

Boss alpha sold in the hit:

$$
X'_{boss} = X_{boss}-X_{vault} = 2000-10 = 1990\;\alpha_1
$$

Total target alpha sold:

$$
Q_T = X'_{boss} + (5000+3000+2000) = 11{,}990\;\alpha_1
$$

---

## Settlement Part A — TAO (from the batched sell)

**Hit Proceeds:** `V_hit = 500 TAO`  
**Taofather Rake (1.5%):** `7.5 TAO`  

**Street Heat:** `I' = 0.50` → Tag **CLEAN**

Base kickback at `I'=0.50`:

$$
b(0.50)=0.0200 + 0.0075\cdot\frac{0.50-0.35}{0.40}=0.0228125
$$

Assume Boss has solid skin (`\rho_{norm}\approx 0.67`), so:

$$
m_b(\rho)=0.90+0.20\cdot 0.67\approx 1.033
$$

$$
b_{eff}\approx \min(0.03,\;0.0228125\cdot 1.033)=0.02357
$$

**Boss Kickback (TAO):**  
`V_boss,kick = 0.02357 * 500 = 11.785 TAO`

**Pool TAO pot:**
$$
V_{pool} = 500 - 7.5 - 11.785 = 480.715\;TAO
$$

### TAO payouts (strict pro-rata by target alpha)
- **Boss pool TAO:**  
  $$P_{boss,pool}=480.715\cdot\frac{1990}{11990}\approx 79.785\;TAO$$
- **Alice TAO:**  
  $$P_{Alice,TAO}=480.715\cdot\frac{5000}{11990}\approx 200.465\;TAO$$
- **Boris TAO:**  
  $$P_{Boris,TAO}=480.715\cdot\frac{3000}{11990}\approx 120.279\;TAO$$
- **Cara TAO:**  
  $$P_{Cara,TAO}=480.715\cdot\frac{2000}{11990}\approx 80.186\;TAO$$

**Boss total TAO:**  
`Boss TAO = kickback + pool payout = 11.785 + 79.785 ≈ 91.57 TAO`

---

## Settlement Part B — MOB-α (Envelope “mining” rewards)

This is a **separate payout** denominated in **MOB-α**, allocated by contribution + reputation.

Assume:

**Envelope Pool (MOB-α):** `E_hit = 4,000 MOB-α`

Mobster envelope allocation (mobsters only):

$$
c_i=\frac{d_i}{\sum_j d_j},\quad r_i=\frac{Rep_i}{\sum_j Rep_j},\quad
w_i=c_i^{\gamma}\cdot r_i^{\delta},\quad
R_{i,MOB\alpha}=E_{hit}\cdot\frac{w_i}{\sum_k w_k}
$$

### Example Rep-weighted envelope outcome (illustrative)
Let Rep be:
- Alice Rep = 60
- Boris Rep = 30
- Cara Rep = 10

Choose `γ=1`, `δ=1` for illustration.

Mobster contributions (mobsters total = 10,000):
- Alice: `c=0.50`
- Boris: `c=0.30`
- Cara: `c=0.20`

Rep shares (total Rep=100):
- Alice: `r=0.60`
- Boris: `r=0.30`
- Cara: `r=0.10`

Weights `w=c·r`:
- Alice: `0.30`
- Boris: `0.09`
- Cara: `0.02`
Sum = `0.41`

Envelope payouts:
- **Alice MOB-α:** `4000*(0.30/0.41) ≈ 2926.83 MOB-α`
- **Boris MOB-α:** `4000*(0.09/0.41) ≈ 878.05 MOB-α`
- **Cara MOB-α:** `4000*(0.02/0.41) ≈ 195.12 MOB-α`

> Notice: TAO payouts stayed purely pro-rata by target alpha, but the MOB-α envelope favors high-Rep mobsters. That’s the intended design: **TAO is simple and fair; MOB-α is the incentive/behavior layer.**

---

### Boss MOB-α (Tax + Vault + Wash) *(illustrative)*
**Boss MOB-α Deposit:** `A_boss = 1,000 MOB-α`  
**Family Vault (2.5%):** `25 MOB-α`

Street Tax (CLEAN at `I'=0.50`):

$$
\tau(0.50)=0.0400 - 0.0100\cdot\frac{0.50-0.35}{0.40}=0.03625
$$

Assume `\rho_{norm}\approx 0.67`:

$$
m_{\tau}(\rho)=1-0.30\cdot 0.67\approx 0.80
$$

$$
\tau_{eff}\approx 0.03625\cdot 0.80=0.029
$$

**Street Tax burned:** `29.0 MOB-α`

Escrow:

$$
A_{esc}=A_{boss}-A_{vault}-A_{tax}=1000-25-29=946
$$

Wash floor:

$$
\beta_{min}(\rho)=0.80+0.10\cdot 0.67\approx 0.867
$$

Returned escrow at `I'=0.50`:

$$
A_{returned}\approx 946\cdot(0.867+0.133\cdot 0.5)=946\cdot 0.9335\approx 883.7
$$

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

## A4) TAO Settlement (Strict pro-rata by target alpha)

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

Total target alpha sold:

$$
Q_T=X'_{boss}+\sum_i d_i
$$

TAO paid to any participant `k`:

$$
P_{k,TAO}=V_{pool}\cdot \frac{d_k}{Q_T}
$$

Where:
- `d_k=X'_{boss}` for the Boss  
- `d_k=d_i` for Mobster `i`

Boss total TAO:

$$
P_{boss,total}=V_{boss,kick}+P_{boss,TAO}
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

$$
c_i=\frac{d_i}{\sum_j d_j},\quad
r_i=\frac{Rep_i}{\sum_j Rep_j},\quad
w_i=c_i^{\gamma}\cdot r_i^{\delta},\quad
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
- You earn TAO from your target alpha being sold **plus** kickback
- Higher skin ratio reduces Street Tax and improves wash floor
- Kickback scales with hit quality and improves with skin

### For Mobsters
- TAO payout is transparent and strict pro-rata by target alpha
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

**Q: What are the two payouts again?**  
A: **TAO** comes from selling pooled target alpha (pro-rata). **MOB-α** comes from envelopes (rep-weighted).

---
