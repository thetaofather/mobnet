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
- **Cap benefits:** `ρ ≥ 3.0` (extra target alpha is allowed, but risk benefits stop increasing)

Normalize:

$$
\rho_{norm}=\text{clamp}\left(\frac{\rho-0.50}{2.00-0.50},\,0,\,1\right)
$$

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

Boss incentives have two tag-aligned levers:
1) **Kickback** rises with tag quality  
2) **Street Tax** falls with tag quality  

Then the Boss Skin Ratio `ρ` further modifies both (below).

### Base Boss Kickback `b(I')`

| Tag | Street Heat `I'` | Boss Kickback `b(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | **1.00%** |
| MESSY | `0.15 – 0.35` | **1.00% → 2.00%** |
| CLEAN | `0.35 – 0.75` | **2.00% → 2.75%** |
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

### Base Street Tax `τ(I')`

| Tag | Street Heat `I'` | Street Tax `τ(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | **5.00%** |
| MESSY | `0.15 – 0.35` | **5.00% → 4.00%** |
| CLEAN | `0.35 – 0.75` | **4.00% → 3.00%** |
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

---

## Boss Deposits (What Exactly Is Required)

### 1) MOB-α deposit `A_boss`
- Family Vault: `v = 2.5%` of `A_boss`
- Street Tax burned: `τ_eff(I',ρ)·A_boss`
- Escrow (washable): remainder, returned per wash formula

### 2) Target alpha deposit `X_boss`
- Family Vault skim (target alpha): `ν_X·X_boss` where `ν_X ∈ [0.25%, 1.00%]`
- Sold in hit: `X'_boss = X_boss - X_vault`

---

## Family Vault skim from Boss target alpha

$$
X_{vault} = \nu_X \cdot X_{boss},\quad \nu_X \in [0.0025,\;0.01]
$$

| Tag | `ν_X` |
|---|---:|
| LEGENDARY | **0.25%** |
| CLEAN | **0.50%** |
| MESSY | **0.75%** |
| BOTCHED | **1.00%** |

$$
X'_{boss}=X_{boss}-X_{vault}
$$

---

## Hit Flow (What Actually Happens)

### 1) Boss posts a hit
Boss chooses:
- Target subnet `T`
- Heat Window
- `A_boss` (MOB-α deposit)
- `X_boss` (target alpha deposit)

### 2) Crew forms
Vault skim:

$$
X_{vault}=\nu_X\cdot X_{boss}
$$

Boss sold amount:

$$
X'_{boss}=X_{boss}-X_{vault}
$$

Mobsters deposit `d_i`, total sold:

$$
Q_T = X'_{boss} + \sum_i d_i
$$

### 3) The hit executes
Produces `V_hit` TAO.

### 4) TAO is split and paid (strict pro-rata by target alpha)

Pool pot:

$$
V_{pool} = (1 - t - b_{eff}(I',\rho))\cdot V_{hit}
$$

TAO payout to any participant `k`:

$$
P_{k,TAO}=V_{pool}\cdot \frac{d_k}{Q_T}
$$

### 5) The books close (MOB-α + envelopes)
- Burn `τ_eff(I',ρ)·A_boss`
- Wash boss escrow (bounded by `β_min(ρ)`)
- Distribute MOB-α envelopes (rep-weighted)
- Publish dossier

---

## Example Hit Board Card (Dossier)

> **Two payouts:** TAO (pro-rata) + MOB-α Envelope (rep-weighted).

### 🧾 Case File #071 — “The Dockside Dump”
**Status:** ✅ Closed  
**Tag:** 🟢 **CLEAN**  
**Target:** Subnet `T=1` (alpha_1)

**Boss:** `A_boss=1000 MOB-α`, `X_boss=2000 alpha_1`  
**Mobsters:** Alice 5000, Boris 3000, Cara 2000 `alpha_1`

Vault skim:

$$
\nu_X=0.005,\quad X_{vault}=10,\quad X'_{boss}=1990
$$

Total sold:

$$
Q_T=11{,}990\;\alpha_1
$$

TAO settlement:

$$
V_{hit}=500,\quad V_{rake}=7.5
$$

At `I'=0.50`:

$$
b(0.50)=0.0228125,\quad b_{eff}\approx 0.02357
$$

Boss kickback:

$$
V_{boss,kick}=11.785\;TAO
$$

Pool pot:

$$
V_{pool}=480.715\;TAO
$$

**TAO payouts (strict pro-rata by target alpha)**

- Boss pool TAO ≈ 79.785  
- Alice TAO ≈ 200.465  
- Boris TAO ≈ 120.279  
- Cara TAO ≈ 80.186  

**MOB-α Envelope (separate)**  
Assume `E_hit = 4000 MOB-α`, `γ=1`, `δ=1`, and Rep: Alice 60, Boris 30, Cara 10.

Envelope payouts (illustrative):
- Alice ≈ 2926.83 MOB-α  
- Boris ≈ 878.05 MOB-α  
- Cara ≈ 195.12 MOB-α  

---

## FAQ

**Q: Does Rep affect TAO payouts?**  
A: No. TAO is strict pro-rata by target alpha. Rep only affects MOB-α envelopes.

**Q: Is `p_alpha` a peg?**  
A: No.

**Q: Is this financial advice?**  
A: No.

---
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
- **Cap benefits:** `ρ ≥ 3.0` (extra target alpha is allowed, but risk benefits stop increasing)

Normalize:

$$
\rho_{norm}=\text{clamp}\left(\frac{\rho-0.50}{2.00-0.50},\,0,\,1\right)
$$

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

Boss incentives have two tag-aligned levers:
1) **Kickback** rises with tag quality  
2) **Street Tax** falls with tag quality  

Then the Boss Skin Ratio `ρ` further modifies both (below).

### Base Boss Kickback `b(I')`

| Tag | Street Heat `I'` | Boss Kickback `b(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | **1.00%** |
| MESSY | `0.15 – 0.35` | **1.00% → 2.00%** |
| CLEAN | `0.35 – 0.75` | **2.00% → 2.75%** |
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

### Base Street Tax `τ(I')`

| Tag | Street Heat `I'` | Street Tax `τ(I')` |
|---|---:|---:|
| BOTCHED | `< 0.15` | **5.00%** |
| MESSY | `0.15 – 0.35` | **5.00% → 4.00%** |
| CLEAN | `0.35 – 0.75` | **4.00% → 3.00%** |
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

---

## Boss Deposits (What Exactly Is Required)

### 1) MOB-α deposit `A_boss`
- Family Vault: `v = 2.5%` of `A_boss`
- Street Tax burned: `τ_eff(I',ρ)·A_boss`
- Escrow (washable): remainder, returned per wash formula

### 2) Target alpha deposit `X_boss`
- Family Vault skim (target alpha): `ν_X·X_boss` where `ν_X ∈ [0.25%, 1.00%]`
- Sold in hit: `X'_boss = X_boss - X_vault`

---

## Family Vault skim from Boss target alpha

$$
X_{vault} = \nu_X \cdot X_{boss},\quad \nu_X \in [0.0025,\;0.01]
$$

| Tag | `ν_X` |
|---|---:|
| LEGENDARY | **0.25%** |
| CLEAN | **0.50%** |
| MESSY | **0.75%** |
| BOTCHED | **1.00%** |

$$
X'_{boss}=X_{boss}-X_{vault}
$$

---

## Hit Flow (What Actually Happens)

### 1) Boss posts a hit
Boss chooses:
- Target subnet `T`
- Heat Window
- `A_boss` (MOB-α deposit)
- `X_boss` (target alpha deposit)

### 2) Crew forms
Vault skim:

$$
X_{vault}=\nu_X\cdot X_{boss}
$$

Boss sold amount:

$$
X'_{boss}=X_{boss}-X_{vault}
$$

Mobsters deposit `d_i`, total sold:

$$
Q_T = X'_{boss} + \sum_i d_i
$$

### 3) The hit executes
Produces `V_hit` TAO.

### 4) TAO is split and paid (strict pro-rata by target alpha)

Pool pot:

$$
V_{pool} = (1 - t - b_{eff}(I',\rho))\cdot V_{hit}
$$

TAO payout to any participant `k`:

$$
P_{k,TAO}=V_{pool}\cdot \frac{d_k}{Q_T}
$$

### 5) The books close (MOB-α + envelopes)
- Burn `τ_eff(I',ρ)·A_boss`
- Wash boss escrow (bounded by `β_min(ρ)`)
- Distribute MOB-α envelopes (rep-weighted)
- Publish dossier

---

## Example Hit Board Card (Dossier)

> **Two payouts:** TAO (pro-rata) + MOB-α Envelope (rep-weighted).

### 🧾 Case File #071 — “The Dockside Dump”
**Status:** ✅ Closed  
**Tag:** 🟢 **CLEAN**  
**Target:** Subnet `T=1` (alpha_1)

**Boss:** `A_boss=1000 MOB-α`, `X_boss=2000 alpha_1`  
**Mobsters:** Alice 5000, Boris 3000, Cara 2000 `alpha_1`

Vault skim:

$$
\nu_X=0.005,\quad X_{vault}=10,\quad X'_{boss}=1990
$$

Total sold:

$$
Q_T=11{,}990\;\alpha_1
$$

TAO settlement:

$$
V_{hit}=500,\quad V_{rake}=7.5
$$

At `I'=0.50`:

$$
b(0.50)=0.0228125,\quad b_{eff}\approx 0.02357
$$

Boss kickback:

$$
V_{boss,kick}=11.785\;TAO
$$

Pool pot:

$$
V_{pool}=480.715\;TAO
$$

**TAO payouts (strict pro-rata by target alpha)**

- Boss pool TAO ≈ 79.785  
- Alice TAO ≈ 200.465  
- Boris TAO ≈ 120.279  
- Cara TAO ≈ 80.186  

**MOB-α Envelope (separate)**  
Assume `E_hit = 4000 MOB-α`, `γ=1`, `δ=1`, and Rep: Alice 60, Boris 30, Cara 10.

Envelope payouts (illustrative):
- Alice ≈ 2926.83 MOB-α  
- Boris ≈ 878.05 MOB-α  
- Cara ≈ 195.12 MOB-α  

---

## FAQ

**Q: Does Rep affect TAO payouts?**  
A: No. TAO is strict pro-rata by target alpha. Rep only affects MOB-α envelopes.

**Q: Is `p_alpha` a peg?**  
A: No.

**Q: Is this financial advice?**  
A: No.

---
