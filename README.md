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

## The Game Loop

1) **A Boss** picks a target subnet and posts a job on the **Hit Board**  
2) Boss posts **two deposits** to open the hit:
   - **MOB-α deposit** `A_boss` (Street Tax Hold + Family Vault + Washable Escrow)
   - **Target alpha deposit** `X_boss` (target subnet alpha that will be sold in the hit)
3) **Mobsters** (miners) join by depositing the target subnet’s alpha into the pool  
4) Pool fills (or the **Heat Window** ends) → the hit is armed  
5) The system executes **one batched sell** (“the hit”) of pooled *target alpha only* → **TAO proceeds**  
6) TAO proceeds split into: **Taofather Rake**, **Boss Kickback**, **Pool Payout**  
7) Consiglieres compute **Street Heat** and publish the dossier  
8) Boss MOB-α escrow is “washed” back (bounded), with a loss split **burn + blessing**  
9) Participants earn **Envelope** rewards (MOB-α) weighted by **contribution + reputation**  
10) The job becomes lore: **BOTCHED / MESSY / CLEAN / LEGENDARY**, ranks, Families, leaderboards

---

## Quick Rules (The Money)

### Two payouts, always separate

Every hit produces **two independent payouts**:

1) **TAO payout** (from selling pooled target alpha)  
   - **Strictly pro-rata by target alpha contributed to the hit**  
   - **Not** influenced by reputation, MOB-α, tags, or anything else

2) **MOB-α Envelope payout** (the “mining” reward)  
   - **Is** influenced by contribution **and** reputation (Rep)  
   - Boss gets a slight “neck bonus” weight on their target-alpha contribution  
   - Paid in MOB-α, not TAO

### What gets sold in a hit

A hit sells **only target subnet alpha**:
- Boss contributes `X_boss` target alpha (minus a small vault skim)
- Mobsters contribute `d_i` target alpha
- The protocol sells the combined inventory in one batched execution

**MOB-α is never converted** in the hit.

### TAO settlement from every hit

When a hit executes, it produces:

- `V_hit` (TAO proceeds)

From `V_hit`, the protocol takes:

- **Taofather Rake:** `t = 1.5%`
- **Boss Kickback:** `b_eff(I', ρ)` (tag-based 1–3%, improved by Boss skin)
- The rest goes to the **Pool Payout** pot (paid strictly pro-rata by target alpha)

---

## Roles

### The Taofather (Subnet Owner)
Runs the city. Sets the street rules. Collects the rake.

### Boss (Hit Sponsor)
Opens hits. Deposits MOB-α + real target alpha. Takes bounded wash risk on MOB-α. Earns kickback + TAO from their target alpha sale.

### Mobsters (Crew / Miners)
Bring inventory (target alpha). Get paid in TAO + envelopes (MOB-α). Build reputation.

### Consiglieres (Validators / Bookkeepers)
Compute Street Heat and Rep. Validate settlement math. Publish dossiers and leaderboards.

---

## MOBnet Slang (Mini Glossary)

- **Hit** — one coordinated batched sell of pooled target alpha  
- **Hit Board / Wall of Jobs** — public list of hits (open + completed)  
- **Heat Window** — time limit for a pool to fill  
- **Street Heat** — impact score (“did the streets feel it?”)  
- **Street Tax Hold** — Boss’s held tribute (max-rate hold), finalized after the hit  
- **Wash** — returning Boss MOB-α escrow (bounded)  
- **The Blessing** — Taofather’s share of escrow loss  
- **The Envelope** — MOB-α rewards paid to participants for running hits  
- **BOTCHED / MESSY / CLEAN / LEGENDARY** — hit tags based on heat/quality  
- **The Rake** — Taofather’s TAO cut from every hit (`1.5%`)  
- **Kickback** — Boss bonus from TAO proceeds (tag-based, up to `3%`)

---

## Ranks, Families, and Reputation

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

**Rep affects MOB-α Envelopes only** — never TAO.

---

## Boss “Skin Ratio” (Risk + Upside Slider)

Bosses choose how much target alpha to put up relative to their MOB-α deposit.  
The more target alpha they post, the **less risk** they take on MOB-α and the **more upside** they earn via kickback quality.

We define a **Boss Skin Ratio** using TAO-equivalent accounting comparison:

- `A_boss` = MOB-α deposit  
- `X_boss` = Boss target alpha deposit (units of `alpha_T`)  
- `P0` = pre-hit price of `alpha_T` in TAO (TAO per alpha)  
- `p_alpha` = reference street price of MOB-α in TAO (accounting only)

MOB-α notional:

$$
N_A = A_{boss}\cdot p_{\alpha}
$$

Target-alpha notional:

$$
N_X = X_{boss}\cdot P0
$$

Boss Skin Ratio:

$$
\rho = \frac{N_X}{N_A} = \frac{X_{boss}\cdot P0}{A_{boss}\cdot p_{\alpha}}
$$

### Recommended bands

- **Minimum to open a hit:** `ρ ≥ 0.50`
- **Recommended “serious boss” band:** `ρ = 1.0 – 2.0`
- **Cap benefits:** `ρ ≥ 3.0` (extra target alpha is allowed; benefit stops increasing)

Normalize:

$$
\rho_{norm}=\text{clamp}\left(\frac{\rho-0.50}{2.00-0.50},\,0,\,1\right)
$$

---

## Hit Tags (BOTCHED / MESSY / CLEAN / LEGENDARY)

Tags are primarily determined by **Street Heat** `I'_{hit}` (impact adjusted by depth).

Let `I' = I'_{hit}`:

- **BOTCHED**: `I' < 0.15`  
- **MESSY**: `0.15 ≤ I' < 0.35`  
- **CLEAN**: `0.35 ≤ I' < 0.75`  
- **LEGENDARY**: `I' ≥ 0.75`

---

## Kickback + Street Tax Schedule (Aligned to Tags)

Boss incentives have two tag-aligned levers:
1) **Kickback** (TAO, paid out of `V_hit`) rises with tag quality  
2) **Street Tax** (MOB-α) falls with tag quality  
Then **Boss Skin Ratio `ρ`** improves both (lower risk / more upside).

### Base Boss Kickback `b(I')`

| Tag | Street Heat `I'` | Boss Kickback `b(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | `1.00%` |
| MESSY | `0.15 – 0.35` | `1.00% → 2.00%` (linear) |
| CLEAN | `0.35 – 0.75` | `2.00% → 2.75%` (linear) |
| LEGENDARY | `≥ 0.75` | `3.00%` |

$$
b(I')=
\begin{cases}
0.0100 & I' < 0.15\\
0.0100 + 0.0100\cdot\frac{I' - 0.15}{0.20} & 0.15\le I' < 0.35\\
0.0200 + 0.0075\cdot\frac{I' - 0.35}{0.40} & 0.35\le I' < 0.75\\
0.0300 & I' \ge 0.75
\end{cases}
$$

### Base Street Tax `τ(I')`

| Tag | Street Heat `I'` | Street Tax `τ(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | `5.00%` |
| MESSY | `0.15 – 0.35` | `5.00% → 4.00%` (linear) |
| CLEAN | `0.35 – 0.75` | `4.00% → 3.00%` (linear) |
| LEGENDARY | `≥ 0.75` | `2.50%` |

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

## Skin Ratio Modifiers

### Street Tax discount modifier

$$
m_{\tau}(\rho)=1-0.30\cdot \rho_{norm}
$$

$$
\tau_{eff}(I',\rho)=\tau(I')\cdot m_{\tau}(\rho)
$$

### Kickback multiplier

$$
m_{b}(\rho)=0.90+0.20\cdot \rho_{norm}
$$

$$
b_{eff}(I',\rho)=\min(0.03,\; b(I')\cdot m_{b}(\rho))
$$

### Wash minimum floor (improves with `ρ`)

$$
\beta_{min}(\rho)=0.80+0.10\cdot \rho_{norm}
$$

---

## Boss Deposits (What Exactly Is Required)

### 1) MOB-α deposit `A_boss` (bounded-risk deposit)

- **Family Vault:** `v = 2.5%` of `A_boss`
- **Street Tax:** `\tau_{eff}(I',\rho)\cdot A_{boss}` (final burn)
- **Escrow (washable):** remainder, returned per wash formula (bounded by `β_min(ρ)`)

**Street Tax Hold mechanics (boss-friendly):**
- At creation, the protocol holds the **max** possible tax (5% of `A_boss`) as a temporary hold.
- After the hit, the final Street Tax burned is computed using `τ_eff(I',ρ)`.
- Any held amount above the final tax is **rebated back into escrow**.

### 2) Target alpha deposit `X_boss` (boss must be a participant)

- **Family Vault skim (target alpha):** `ν_X·X_boss` where `ν_X ∈ [0.25%, 1.00%]`
- **Sold in hit:** `X'_boss = X_boss - X_vault`

---

## Family Vault Skim (from Boss target alpha)

Vault skim (in target alpha):

$$
X_{vault}=\nu_{X}\cdot X_{boss}
$$

Recommended schedule:

| Tag | `ν_X` (Boss target alpha to vault) |
|---|---:|
| LEGENDARY | `0.25%` |
| CLEAN | `0.50%` |
| MESSY | `0.75%` |
| BOTCHED | `1.00%` |

Boss target alpha sold:

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
Vault skim:

$$
X_{vault}=\nu_{X}\cdot X_{boss}
$$

Boss sold amount:

$$
X'_{boss}=X_{boss}-X_{vault}
$$

Mobsters deposit target alpha `d_i`.

Total target alpha sold in the hit:

$$
Q_{T}=X'_{boss}+\sum_{i} d_i
$$

### 3) The hit executes
All pooled target alpha is sold in a single batched execution.

Output:
- `V_hit` TAO proceeds
- price moves from `P0` to `P1`

### 4) TAO is split and paid (strict pro-rata by target alpha)

Pool pot:

$$
V_{pool}=(1-t-b_{eff}(I',\rho))\cdot V_{hit}
$$

TAO payout:

$$
P_{k,TAO}=V_{pool}\cdot \frac{d_k}{Q_T}
$$

Boss total TAO:

$$
P_{boss,total}=b_{eff}(I',\rho)\cdot V_{hit}+P_{boss,TAO}
$$

### 5) The books close (MOB-α side + envelopes)
- Street Heat is calculated
- Street Tax is finalized
- Boss escrow is washed back (bounded)
- Envelopes are distributed (Rep-weighted)
- Dossier is published

---

## Example Hit Board Card (Dossier)

> What a public Hit Board entry could look like.  
> It reads like lore, but it still audits.

### 🧾 Case File #071 — “The Dockside Dump”
**Status:** ✅ Closed  
**Tag:** 🟢 CLEAN  
**Target:** Subnet `T=1` (`alpha_1`)  
**District:** San Taovanni — The Docks  
**Heat Window:** 2h 00m  
**Time to Fill:** 37m

#### Pool Inventory (Target Alpha)

Boss posted:
- `X_boss = 2,000 alpha_1`
- CLEAN skim `ν_X = 0.50%` → `X_vault = 10 alpha_1`
- Boss sold amount: `X'_boss = 1,990 alpha_1`

Mobsters posted:
- Alice: `5,000`
- Boris: `3,000`
- Cara: `2,000`

Total sold:
- `Q_T = 1,990 + 10,000 = 11,990 alpha_1`

---
## Settlement (TAO) — **strict pro-rata by target alpha**

**Proceeds:** `V_hit = 500 TAO`  
**Taofather Rake (1.5%):** `7.5 TAO`

**Street Heat:** `I' = 0.50` → Tag CLEAN

### Boss skin (for incentives)

Assume accounting inputs:
- `p_alpha = 0.050 TAO / MOB-α`
- `P0 = 0.080 TAO / alpha_1`
- `A_boss = 1,000 MOB-α`

Then:
- `N_A = 1000 * 0.05 = 50 TAO`
- `N_X = 2000 * 0.08 = 160 TAO`
- `ρ = 160 / 50 = 3.2` → capped benefits → `ρ_norm = 1`

### Boss kickback (tag + skin)

Base kickback at `I'=0.50` (CLEAN range):

$$
b(0.50)=0.0200 + 0.0075\cdot\frac{0.50-0.35}{0.40}=0.0228125
$$

Skin multiplier `m_b(ρ)=1.10`:

$$
b_{eff}=b\cdot m_b=0.0228125\cdot 1.10=0.02509375
$$

**Boss Kickback:** `0.02509375 * 500 = 12.546875 TAO`  
**Pool Pot:** `500 - 7.5 - 12.546875 = 479.953125 TAO`

### TAO payouts (only contribution matters)

- Boss (from pool): `479.953125 * (1990 / 11990) ≈ 79.658609 TAO`
- Alice: `≈ 200.147258 TAO`
- Boris: `≈ 120.088355 TAO`
- Cara: `≈ 80.058903 TAO`

Boss total TAO:
- **Boss total TAO = kickback + pool share ≈ 12.546875 + 79.658609 = 92.205484 TAO**

---

## Boss Tribute (MOB-α) — Street Tax + Wash (bounded)

**Boss MOB-α Deposit:** `A_boss = 1,000 MOB-α`

Base Street Tax at `I'=0.50`:

$$
\tau(0.50)=0.0400 - 0.0100\cdot\frac{0.50-0.35}{0.40}=0.03625
$$

Street Tax discount `m_τ(ρ)=0.70`:

$$
\tau_{eff}=0.03625\cdot 0.70=0.025375
$$

Street Tax burned:
- `A_tax = 0.025375 * 1000 = 25.375 MOB-α`

Family Vault (MOB-α side):
- `A_vault = 2.5% * 1000 = 25 MOB-α`

Escrow (washable):
- `A_esc = 1000 - 25 - 25.375 = 949.625 MOB-α`

Wash floor:
- `β_min(ρ) = 0.90`

Returned escrow:

$$
A_{returned}=A_{esc}\cdot\left(\beta_{min}+(1-\beta_{min})\cdot \min(1,\;I')\right)
=949.625\cdot(0.90+0.10\cdot 0.50)=949.625\cdot 0.95=902.14375
$$

Lost escrow:
- `A_lost = 47.48125 MOB-α`

Split loss (`ψ=0.5`):
- `A_wash,burn = 23.740625 MOB-α`
- `A_taofather,blessing = 23.740625 MOB-α`

---

## Envelope (MOB-α) — Rep-weighted “mining reward”

Assume the hit’s envelope pool:
- `E_hit = 4,000 MOB-α`

Assume Mobster Rep shares (normalized):
- Alice `r=0.60`, Boris `r=0.30`, Cara `r=0.10`

Boss “neck bonus” multiplier:
- `η_boss = 1.15`

Illustrative envelope weights (`γ=1`, `δ=1`):

- Boss: `w_boss = (η_boss * X'_boss) = 1.15 * 1990 = 2288.5`
- Alice: `w_A = d_A * r_A = 5000 * 0.60 = 3000`
- Boris: `w_B = 3000 * 0.30 = 900`
- Cara: `w_C = 2000 * 0.10 = 200`

Total weight `W = 6388.5`.

Envelope payouts:
- Boss: `4000 * (2288.5/6388.5) ≈ 1432.887 MOB-α`
- Alice: `≈ 1878.375 MOB-α`
- Boris: `≈ 563.513 MOB-α`
- Cara: `≈ 125.225 MOB-α`

> **Reminder:** TAO payouts ignore Rep. Rep only affects MOB-α envelopes.

### Lore (1-liner)
> “Clean work. Quiet steps. The Docks went silent.”

---

## Why be a Mobster vs just selling alpha alone?

Mobsters earn **two** payouts when they participate in a hit:

1) **TAO** from the batched sale of target alpha — **strictly pro-rata by contributed alpha**  
2) **MOB-α Envelope** — additional “mining reward”, weighted by **contribution + Rep**

### Side-by-side: Solo Sell vs Join the Hit (same inventory, same realized price)

Assume Alice owns:
- `d_A = 5,000 alpha_1`

Assume the market execution outcome is the same in both paths:
- **Realized execution price:** `P_exec = 0.040 TAO / alpha_1`

#### Option A — Sell alpha alone (no hit participation)
TAO_solo = d_A * P_exec
         = 5000 * 0.040
         = 200 TAO
MOB-α_solo = 0

#### Option B - Join the hit as a Mobster (same sale price, plus envelopes)

Because TAO payouts are strictly pro-rata and we assumed the same realized price,
Alice’s TAO from the hit sale is effectively the same:

TAO_hit_from_sale ≈ d_A * P_exec
                 ≈ 200 TAO

But as a Mobster, Alice also earns MOB-α Envelope rewards (Rep-weighted). Using the
example dossier envelope math:
MOB-α_envelope(Alice) ≈ 1,878.375 MOB-α

### Comparison:
| Alice’s choice         | TAO received |   MOB-α received | What influences it                                  |
| ---------------------- | -----------: | ---------------: | --------------------------------------------------- |
| Sell alpha alone       |    ≈ 200 TAO |          0 MOB-α | TAO only depends on sale price |
| Join the hit (Mobster) |    ≈ 200 TAO | + 1,878.38 MOB-α | TAO: pro-rata TAO only. MOB-α: contribution + Rep |

Key point: the designed extra upside for Mobsters is the MOB-α envelope.

---

# Appendix A — The Books (Math & Definitions)

## A1) Boss Deposit Rule (Sizing)

Boss MOB-α deposit can be tied to the notional hit size:

- `Q_T`: total target alpha sold in the hit
- `P0`: pre-hit target alpha price (TAO per alpha)
- `p_alpha`: MOB-α reference street price (TAO per MOB-α)
- `k`: margin factor (MOB-α per 1 TAO of notional)
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

## A2) MOB-α Deposit Split

Let `v = 0.025` be the fixed vault share.

Final tax burn:

$$
A_{tax}=\tau_{eff}(I',\rho)\cdot A_{boss}
$$

Family Vault:

$$
A_{vault}=v\cdot A_{boss}
$$

Escrow:

$$
A_{esc}=A_{boss}-A_{vault}-A_{tax}
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

## A4) TAO Settlement

Taofather rake:

$$
V_{taofather}=t\cdot V_{hit}
$$

Boss kickback:

$$
V_{boss,kick}=b_{eff}(I',\rho)\cdot V_{hit}
$$

Pool pot:

$$
V_{pool}=(1-t-b_{eff}(I',\rho))\cdot V_{hit}
$$

TAO paid to any participant `k`:

$$
P_{k,TAO}=V_{pool}\cdot \frac{d_k}{Q_T}
$$

Boss total TAO:

$$
P_{boss,total}=V_{boss,kick}+P_{boss,TAO}
$$

---

## A5) Street Heat

Price shock:

$$
\Delta P = \frac{P0 - P1}{P0}
$$

Normalized shock:

$$
I_{hit}=\min\left(1,\;\max\left(0,\;\frac{\Delta P}{\Delta P_{max}}\right)\right)
$$

Alpha-equivalent depth:

$$
L_T=\frac{R_{TAO,T}}{P0}
$$

Smoothed depth:

$$
L_T^{smooth}=EMA(L_T)
$$

Size-adjusted heat:

$$
I'_{hit}=I_{hit}\cdot \frac{Q_T}{L_T^{smooth}+\epsilon}
$$

---

## A6) The Envelope (MOB-α Rewards)

Epoch envelope pool:

$$
E_{rewards,epoch}\quad (\text{in MOB-}\alpha)
$$

Allocate to hits (example weighting):

$$
s_h=\frac{V_{hit,h}}{\sum_k V_{hit,k}}\cdot \left(1+\kappa\cdot I'_{hit,h}\right)
$$

$$
E_{hit,h}=E_{rewards,epoch}\cdot \frac{s_h}{\sum_j s_j}
$$

Within-hit weights (Rep affects MOB-α only):

$$
r_i=\frac{Rep_i}{\sum_j Rep_j}
$$

Boss weight (neck bonus):

$$
w_{boss}=\left(\eta_{boss}\cdot X'_{boss}\right)^{\gamma}
$$

Mobster weight:

$$
w_i=d_i^{\gamma}\cdot r_i^{\delta}
$$

Payout:

$$
R_{k,MOB\alpha}=E_{hit}\cdot \frac{w_k}{w_{boss}+\sum_i w_i}
$$

---

## A7) Tribute, Wash, and the Blessing

Minimum return:

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
A_{wash,burn}=\psi\cdot A_{lost}
$$

$$
A_{taofather,blessing}=(1-\psi)\cdot A_{lost}
$$

---

## Value Proposition

### For MOB-α holders
- Bosses must buy MOB-α to sponsor hits
- Street Tax burns MOB-α (tag + skin adjusted)
- Boss activity increases MOB-α utility and demand

### For Bosses
- Must post real target alpha → real participant
- Earn TAO from target alpha sale **plus** kickback
- Higher `ρ` reduces Street Tax and improves wash floor
- Street Tax Hold rebates excess hold back into escrow

### For Mobsters
- TAO payout is strict pro-rata by target alpha
- Envelopes (MOB-α) reward participation + reputation
- Rep increases envelope weight (MOB-α only)

### For Consiglieres
- Publish heat, payouts, and Rep
- Protect the streets from manipulation

---

## FAQ

**Q: Is this financial advice?**  
A: No.

**Q: Is `p_alpha` a peg?**  
A: No. It’s a reference input used for accounting examples, not a guarantee.

**Q: Does the protocol convert MOB-α to TAO?**  
A: No. Hits sell **only target subnet alpha**. MOB-α is used for deposits, burns, escrow, and envelopes.

**Q: Who can post hits or join crews?**  
A: Anyone.

**Q: Why does Street Tax depend on heat?**  
A: To incentivize Bosses to aim for **clean hits**: better heat lowers tax and increases kickback.

**Q: Does Mobster reputation affect TAO payouts?**  
A: No. TAO is strict pro-rata by target alpha. Rep only affects MOB-α envelopes.

**Q: What are the two payouts again?**  
A: **TAO** (from selling target alpha) and **MOB-α** (envelopes, Rep-weighted).

---
