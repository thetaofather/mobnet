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
2) Boss deposits **MOB-α** (Street Tax Hold + Washable Escrow + Family Vault)  
3) **Mobsters** (miners) join by depositing the target subnet’s alpha into the pool  
4) Pool fills (or the **Heat Window** ends) → the hit is armed  
5) The system executes **one batched sell** (“the hit”) → TAO proceeds  
6) TAO proceeds split into: **Taofather Rake**, **Boss Kickback**, **Crew Payout**  
7) Consiglieres (validators) compute **Street Heat** (impact) and publish the dossier  
8) Boss escrow is “washed” back (bounded), with a small loss split **burn + blessing**  
9) The crew earns **Envelope** rewards (MOB-α) on top of TAO payouts  
10) The job becomes lore: **BOTCHED / MESSY / CLEAN / LEGENDARY**, ranks, Families, and leaderboards

---

## Quick Rules (The Money)

### TAO settlement from every hit

When a hit executes, it produces:

- `V_hit` (TAO proceeds)

From `V_hit`, the protocol takes:

- **Taofather Rake:** **1.5%**
- **Boss Kickback:** **1%–3%** depending on how clean the hit was
- The rest goes to the **Crew (Mobsters)**

So Mobsters receive **95.5%–97.5%** of hit TAO proceeds.

### Boss deposit (MOB-α) — Street Tax gets cheaper when the hit is clean

To post a hit, the Boss deposits `A_boss` MOB-α. The Street Tax is **not a fixed burn**, it’s a **Street Tax Hold** that is finalized after the hit based on Street Heat:

- **Effective Street Tax:** **2.5%–5%** of `A_boss` (burned)
- **Better Street Heat → lower Street Tax**
- Anything held above the final tax is rebated back into escrow (i.e., you get it back unless your wash loss takes it later)

The Boss deposit always allocates a fixed slice to the vault:

- **Family Vault:** **2.5%** of `A_boss`
- The remainder (after finalized Street Tax) becomes **Escrow (washable)**.

---

## Roles

### The Taofather (Subnet Owner)
Runs the city. Sets the street rules. Collects the rake.

### Boss (Hit Sponsor)
Posts jobs. Pays Street Tax (cheaper on clean hits). Takes wash risk. Earns kickbacks on clean hits.

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
- **Street Tax Hold** — Boss’s held tribute; finalized and burned after the hit (2.5–5%)  
- **Wash** — returning Boss escrow (bounded)  
- **The Blessing** — Taofather’s share of escrow loss  
- **The Envelope** — MOB-α rewards paid to crews for running hits  
- **BOTCHED / MESSY / CLEAN / LEGENDARY** — hit tags based on heat/quality  
- **The Rake** — Taofather’s TAO cut from every hit (**1.5%**)  
- **Kickback** — Boss bonus from TAO proceeds (**1–3%** depending on tag)

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

### The Hit Dossier (every completed hit)
Each job gets a permanent “case file”:
- Target, pool size, time to fill, execution proceeds  
- Tag: **BOTCHED / MESSY / CLEAN / LEGENDARY**  
- Street Heat score + how it was computed  
- Witness list (participants) + payouts  
- A short lore line

---

## Hit Tags (BOTCHED / MESSY / CLEAN / LEGENDARY)

Every completed job gets a permanent **Hit Tag** on the Hit Board.  
Tags are determined primarily by **Street Heat** `I'_{hit}` (impact adjusted by depth), plus a couple of basic execution-quality checks so the streets can’t be gamed.

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

Boss incentives have two levers:
1) **Kickback** (TAO, paid out of `V_hit`) rises with tag quality  
2) **Street Tax** (MOB-α, burned out of `A_boss`) falls with tag quality

### Boss Kickback `b(I')` (TAO cut of `V_hit`)

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

### Effective Street Tax `τ(I')` (MOB-α burn of `A_boss`)

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

**How “Street Tax Hold” works in practice:**
- At creation, the protocol earmarks up to the **max** tax (5%) as a held tribute.
- After the hit, the final Street Tax burned is `τ(I') * A_boss`.
- Any held amount above the final tax is **rebated back into escrow** (so clean hits reduce your effective tax).

---

## Hit Flow (What Actually Happens)

### 1) Boss posts a hit
Boss chooses:
- Target subnet `T`
- Pool size `Q_T` (target alpha units)
- Heat Window (timeout policy)
- Boss deposit `A_boss` (MOB-α)

### 2) Crew forms
Mobsters deposit target alpha:
- Each Mobster `i` deposits `d_i`
- When the pool fills: `Q_T = Σ d_i`

### 3) The hit executes
All pooled target alpha is sold in a **single batched execution**.

Output:
- `V_hit` TAO proceeds
- price moves from `P0` to `P1`

### 4) TAO is split and paid
- Taofather takes rake (**1.5%**)
- Boss gets kickback (tag-aligned, **1–3%**)
- Crew gets the rest, paid pro-rata by contribution

### 5) The books close
- Street Heat is calculated
- Street Tax is finalized (burn `τ(I')*A_boss`, rebate the rest into escrow)
- Boss escrow is washed back (80–100% of escrow based on heat)
- Envelope rewards are distributed
- The dossier is published

---

## Example Hit Board Card (Dossier)

> What a public Hit Board entry could look like.  
> It reads like lore, but it still audits.

### 🧾 Case File #071 — “The Dockside Dump”
**Status:** ✅ Closed  
**Tag:** 🟢 **CLEAN**  
**Target:** Subnet `T=1` (alpha_1)  
**District:** San Taovanni — The Docks  
**Heat Window:** 2h 00m  
**Time to Fill:** 37m

**Pool Size:** `Q_T = 10,000 alpha_1`  
**Witnesses (Crew):** 3 Mobsters  
- Alice: 5,000 (50%)  
- Boris: 3,000 (30%)  
- Cara: 2,000 (20%)

### Settlement (TAO)
**Proceeds:** `V_hit = 500 TAO`  
**Taofather Rake (1.5%):** `7.5 TAO`

**Street Heat:** `I' = 0.50` → Tag **CLEAN**

Kickback in CLEAN range is `2.00% → 2.75%`.  
At `I'=0.50`:

$$
b(0.50)=0.0200 + 0.0075\cdot\frac{0.50-0.35}{0.40}=0.0228125
$$

**Boss Kickback:** `0.0228125 * 500 = 11.40625 TAO`  
**Crew Pot:** `500 - 7.5 - 11.40625 = 481.09375 TAO`

**Crew Payouts (base):**
- Alice: `240.546875 TAO`  
- Boris: `144.328125 TAO`  
- Cara: `96.21875 TAO`

### Boss Tribute (MOB-α)
**Boss Deposit:** `A_boss = 1,000 MOB-α`

**Street Tax (finalized):** `τ(0.50)` is in CLEAN range:

$$
\tau(0.50)=0.0400 - 0.0100\cdot\frac{0.50-0.35}{0.40}=0.03625
$$

So **Street Tax burned:** `36.25 MOB-α` (3.625%)

**Family Vault (2.5%):** `25 MOB-α`

**Escrow (washable):**
$$
A_{esc} = A_{boss}\cdot(1 - 0.025 - \tau(I')) = 1000\cdot(0.93875)=938.75
$$

### Street Heat (Impact)
**Pre / Post Price:** `P0=0.080 → P1=0.036`  
**Shock:** `ΔP = 55%` → `I_hit = 1.0`  
**Depth (smoothed):** `L_smooth = 20,000 alpha`  
**Street Heat:** `I' = 0.50` → 🟢 **CLEAN**

### Wash Result (β_min=0.8, ψ=0.5)
$$
A_{returned} = 938.75\cdot (0.8 + 0.2\cdot 0.5)=938.75\cdot 0.9=844.875
$$

$$
A_{lost}=93.875,\quad A_{wash,burn}=46.9375,\quad A_{taofather,blessing}=46.9375
$$

### Envelope (MOB-α) *(illustrative)*
**Envelope Paid:** `4,000 MOB-α`  
- Alice: `2,142`  
- Boris: `1,112`  
- Cara: `746`

### Lore (1-liner)
> “Clean work. Quiet steps. The Docks went silent.”

---

# Appendix A — The Books (Math & Definitions)

> Everything below is the accounting and scoring layer. The gameplay above is the “what it feels like.” This appendix is the “how it’s enforced.”

---

## A1) Boss Deposit Rule (Sizing)

Boss deposit can be tied to notional size:

- `Q_T`: pool size (units of target alpha)
- `P0`: pre-hit alpha price (TAO per alpha)
- `p_alpha`: MOB-α reference street price (TAO per MOB-α)
- `k`: margin factor (MOB-α per 1 TAO of hit notional)
- `A_min`: minimum deposit
- `S_tilde`: optional normalized size in [0,1] (discount for large targets)

Base:

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

---

## A2) Boss Deposit Split (Street Tax depends on heat)

Let `v = 0.025` be the fixed vault share.

Street tax burned:

$$
A_{tax} = \tau(I'_{hit})\cdot A_{boss}
$$

Family Vault:

$$
A_{vault} = v\cdot A_{boss}
$$

Escrow:

$$
A_{esc} = \left(1 - v - \tau(I'_{hit})\right)\cdot A_{boss}
$$

---

## A3) TAO Settlement Weights (Updated)

From hit proceeds `V_hit`:

- Taofather rake `t = 0.015`
- Boss kickback `b(I'_{hit})` (tag-aligned, 1–3%)

$$
V_{taofather} = t \cdot V_{hit}
$$

$$
V_{boss} = b(I'_{hit}) \cdot V_{hit}
$$

$$
V_{mob} = (1 - t - b(I'_{hit}))\cdot V_{hit}
= (0.985 - b(I'_{hit}))\cdot V_{hit}
$$

Mobster `i` base payout:

$$
Payout_{i,base} = V_{mob}\cdot \frac{d_i}{\sum_j d_j}
$$

---

## A4) Street Heat (Impact Scoring)

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

## A5) The Envelope (Emissions & MOB-α Rewards)

Epoch envelope pool:

$$
E_{rewards,epoch}\quad (\text{in MOB-}\alpha)
$$

Allocate to hits:

$$
s_h = \frac{V_{hit,h}}{\sum_k V_{hit,k}}\cdot \left(1+\kappa\cdot I'_{hit,h}\right)
$$

$$
E_{hit,h} = E_{rewards,epoch}\cdot \frac{s_h}{\sum_j s_j}
$$

Allocate within a hit:

Contribution share:

$$
c_i = \frac{d_i}{\sum_j d_j}
$$

Loyalty share:

$$
\ell_i = \frac{H_i}{\sum_j H_j}
$$

Weights:

$$
w_i = c_i^{\gamma}\cdot \ell_i^{\delta}
$$

Reward:

$$
R_i = E_{hit}\cdot \frac{w_i}{\sum_k w_k}
$$

---

## A6) Tribute, Wash, and the Blessing (Boss Escrow Return)

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

Split loss:

$$
A_{wash,burn} = \psi\cdot A_{lost},\quad
A_{taofather,blessing} = (1-\psi)\cdot A_{lost}
$$

Totals (burn + vault):

$$
A_{burn,total} = \tau(I'_{hit})\,A_{boss} + \psi\cdot (A_{esc}-A_{returned})
$$

$$
A_{vault,total} = 0.025\,A_{boss}
$$

---

## Value Proposition

### For The MOB-α holders
- **Bosses** must buy (MOB-α) to put out hits
- **Street Tax (burn):** `2.5%–5%` burn 

### For Bosses
- Known bounds: Street Tax is always between **2.5% and 5%**.
- Strong incentive: **clean hits reduce Street Tax** and increase kickback.
- Bounded risk: escrow return is formula-driven (80–100% of escrow based on heat).
- Upside: kickback (1–3% of proceeds) increases with tag quality.

### For Mobsters
- Crew payouts are proportional and transparent.
- Envelope rewards (MOB-α) can make crew runs slightly +EV vs solo selling.
- Ranks, Families, and dossier history make it a real game.

### For Consiglieres
- Keep the books. Publish the truth. Protect the street from manipulation.
- Optional future: governance-defined compensation via envelopes or vault tooling budgets.

---

## FAQ

**Q: Is this financial advice?**  
A: No.

**Q: Is `p_alpha` a peg?**  
A: No. It’s a reference input used for accounting examples.

**Q: Who can post hits or join crews?**  
A: Anyone. Bosses sponsor, Mobsters contribute target alpha, Consiglieres validate.

**Q: Why does Street Tax depend on heat?**  
A: To incentivize Bosses to aim for **clean hits**: better heat lowers tax and increases kickback.

---
