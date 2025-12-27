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

## Quick Rules

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

Then the Boss Skin Ratio `ρ` further modifies both (below).

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

$$
X_{vault} = \nu_X \cdot X_{boss}
$$

Where:

- `ν_X ∈ [0.0025, 0.01]`

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
- Vault receives target alpha skim:

$$
X_{vault} = \nu_X\cdot X_{boss}
$$

- Boss hit contribution becomes:

$$
X'_{boss} = X_{boss}-X_{vault}
$$

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
P_{k,TAO} = V_{pool}\cdot \frac{d_k}{Q_T}
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

## Why be a Mobster (miner) instead of just selling alpha alone?

Mobsters earn **two** payouts when they participate in a hit:

1) **TAO** from the batched sale of target alpha — strict pro-rata by contributed alpha  
2) **MOB-α Envelope** — additional mining reward, weighted by contribution + Rep

To make the benefit obvious, compare a Mobster doing a **solo sell** vs joining a **hit** with the same starting inventory.

### Side-by-side: Solo Sell vs Join the Hit (same inventory)

Assume a Mobster (Alice) owns:

- `d_A = 5,000 alpha_1`

Assume the effective realized execution price in both cases is the same:

- `P_exec = 0.040 TAO / alpha_1`

So the **solo sale proceeds** would be:

```text
TAO_solo = d_A * P_exec = 5000 * 0.040 = 200 TAO
Now assume a hit occurs with:

Boss sold amount: X'_boss = 1,990 alpha_1

Mobsters: Alice 5,000, Boris 3,000, Cara 2,000

Total sold: Q_T = 11,990 alpha_1

Hit produces:

V_hit = 500 TAO

Taofather rake t = 1.5% → 7.5 TAO

Boss kickback V_boss,kick = 11.785 TAO

Pool pot:

text
Copy code
V_pool = 500 - 7.5 - 11.785 = 480.715 TAO
TAO in the hit is strict pro-rata:

text
Copy code
TAO_hit(Alice) = V_pool * (d_A / Q_T)
               = 480.715 * (5000 / 11990)
               ≈ 200.465 TAO
Hit TAO can be slightly higher or lower than solo selling depending on actual execution price, fees, and the rake/kickback.
The designed extra upside for Mobsters comes from the MOB-α Envelope.

Comparison table
Alice’s choice	TAO received	MOB-α received	What influences it
Sell alpha alone	≈ 200 TAO	0 MOB-α	TAO depends only on sale price and inventory
Join the hit (Mobster)	≈ 200.465 TAO	+ Envelope MOB-α	TAO: pro-rata by alpha only. MOB-α: contribution + Rep

The “extra” upside: MOB-α Envelope (mining reward)
Assume the hit’s envelope pool is:

E_hit = 4,000 MOB-α

And Rep scores are:

Alice Rep = 60, Boris = 30, Cara = 10

Choose γ=1, δ=1 (simple illustration)

Mobster-only contribution shares (total = 10,000):

Alice: c=0.50

Boris: c=0.30

Cara: c=0.20

Rep shares (total Rep = 100):

Alice: r=0.60

Boris: r=0.30

Cara: r=0.10

Weights w = c * r:

Alice: 0.30, Boris: 0.09, Cara: 0.02 (sum = 0.41)

Envelope payouts:

Alice MOB-α: 4000*(0.30/0.41) ≈ 2926.83 MOB-α

Boris MOB-α: ≈ 878.05 MOB-α

Cara MOB-α: ≈ 195.12 MOB-α

One-liner summary

Mobsters don’t join hits to “magically beat the market” on the TAO sale — they join to earn MOB-α mining rewards (envelopes) on top of whatever TAO they’d get from selling their alpha anyway.

Not a profit guarantee — this is incentive design.

Appendix A — The Books (Math & Definitions)
Everything below is the accounting and scoring layer.

A1) Boss Deposit Rule (Sizing)
Boss deposit can be tied to notional size:

Q_T: pool sold (units of target alpha)

P0: pre-hit alpha price (TAO per alpha)

p_alpha: MOB-α reference street price (TAO per MOB-α)

k: margin factor (MOB-α per 1 TAO of hit notional)

A_min: minimum deposit

Base:

𝐴
𝑏
𝑜
𝑠
𝑠
𝑏
𝑎
𝑠
𝑒
=
𝑘
⋅
𝑄
𝑇
⋅
𝑃
0
𝑝
𝛼
A 
boss
base
​
 =k⋅ 
p 
α
​
 
Q 
T
​
 ⋅P0
​
 
Minimum:

𝐴
𝑏
𝑜
𝑠
𝑠
=
max
⁡
(
𝐴
𝑚
𝑖
𝑛
,
  
𝐴
𝑏
𝑜
𝑠
𝑠
𝑏
𝑎
𝑠
𝑒
)
A 
boss
​
 =max(A 
min
​
 ,A 
boss
base
​
 )
A2) Boss Deposit Split (MOB-α side)
Let v = 0.025 be the fixed vault share.

Street tax burned:

𝐴
𝑡
𝑎
𝑥
=
𝜏
𝑒
𝑓
𝑓
(
𝐼
′
,
𝜌
)
⋅
𝐴
𝑏
𝑜
𝑠
𝑠
A 
tax
​
 =τ 
eff
​
 (I 
′
 ,ρ)⋅A 
boss
​
 
Family Vault:

𝐴
𝑣
𝑎
𝑢
𝑙
𝑡
=
𝑣
⋅
𝐴
𝑏
𝑜
𝑠
𝑠
A 
vault
​
 =v⋅A 
boss
​
 
Escrow:

𝐴
𝑒
𝑠
𝑐
=
𝐴
𝑏
𝑜
𝑠
𝑠
−
𝐴
𝑣
𝑎
𝑢
𝑙
𝑡
−
𝐴
𝑡
𝑎
𝑥
A 
esc
​
 =A 
boss
​
 −A 
vault
​
 −A 
tax
​
 
A3) Boss Target Alpha Vault Skim
𝑋
𝑣
𝑎
𝑢
𝑙
𝑡
=
𝜈
𝑋
⋅
𝑋
𝑏
𝑜
𝑠
𝑠
X 
vault
​
 =ν 
X
​
 ⋅X 
boss
​
 
𝑋
𝑏
𝑜
𝑠
𝑠
′
=
𝑋
𝑏
𝑜
𝑠
𝑠
−
𝑋
𝑣
𝑎
𝑢
𝑙
𝑡
X 
boss
′
​
 =X 
boss
​
 −X 
vault
​
 
Total sold:

𝑄
𝑇
=
𝑋
𝑏
𝑜
𝑠
𝑠
′
+
∑
𝑖
𝑑
𝑖
Q 
T
​
 =X 
boss
′
​
 + 
i
∑
​
 d 
i
​
 
A4) TAO Settlement (Strict pro-rata by target alpha)
From hit proceeds V_hit:

Taofather rake t = 0.015

Boss kickback b_eff(I',\rho)

𝑉
𝑡
𝑎
𝑜
𝑓
𝑎
𝑡
ℎ
𝑒
𝑟
=
𝑡
⋅
𝑉
ℎ
𝑖
𝑡
V 
taofather
​
 =t⋅V 
hit
​
 
𝑉
𝑏
𝑜
𝑠
𝑠
,
𝑘
𝑖
𝑐
𝑘
=
𝑏
𝑒
𝑓
𝑓
(
𝐼
′
,
𝜌
)
⋅
𝑉
ℎ
𝑖
𝑡
V 
boss,kick
​
 =b 
eff
​
 (I 
′
 ,ρ)⋅V 
hit
​
 
Pool payout pot:

𝑉
𝑝
𝑜
𝑜
𝑙
=
(
1
−
𝑡
−
𝑏
𝑒
𝑓
𝑓
(
𝐼
′
,
𝜌
)
)
⋅
𝑉
ℎ
𝑖
𝑡
V 
pool
​
 =(1−t−b 
eff
​
 (I 
′
 ,ρ))⋅V 
hit
​
 
Total target alpha sold:

𝑄
𝑇
=
𝑋
𝑏
𝑜
𝑠
𝑠
′
+
∑
𝑖
𝑑
𝑖
Q 
T
​
 =X 
boss
′
​
 + 
i
∑
​
 d 
i
​
 
TAO paid to any participant k:

𝑃
𝑘
,
𝑇
𝐴
𝑂
=
𝑉
𝑝
𝑜
𝑜
𝑙
⋅
𝑑
𝑘
𝑄
𝑇
P 
k,TAO
​
 =V 
pool
​
 ⋅ 
Q 
T
​
 
d 
k
​
 
​
 
Where:

d_k=X'_{boss} for the Boss

d_k=d_i for Mobster i

Boss total TAO:

𝑃
𝑏
𝑜
𝑠
𝑠
,
𝑡
𝑜
𝑡
𝑎
𝑙
=
𝑉
𝑏
𝑜
𝑠
𝑠
,
𝑘
𝑖
𝑐
𝑘
+
𝑃
𝑏
𝑜
𝑠
𝑠
,
𝑇
𝐴
𝑂
P 
boss,total
​
 =V 
boss,kick
​
 +P 
boss,TAO
​
 
A5) Street Heat (Impact Scoring)
Price shock:

Δ
𝑃
=
𝑃
0
−
𝑃
1
𝑃
0
ΔP= 
P0
P0−P1
​
 
Normalized shock:

𝐼
ℎ
𝑖
𝑡
=
min
⁡
(
1
,
  
max
⁡
(
0
,
  
Δ
𝑃
Δ
𝑃
𝑚
𝑎
𝑥
)
)
I 
hit
​
 =min(1,max(0, 
ΔP 
max
​
 
ΔP
​
 ))
Alpha-equivalent depth:

𝐿
𝑇
=
𝑅
𝑇
𝐴
𝑂
,
𝑇
𝑃
0
L 
T
​
 = 
P0
R 
TAO,T
​
 
​
 
Smoothed depth:

𝐿
𝑇
𝑠
𝑚
𝑜
𝑜
𝑡
ℎ
=
𝐸
𝑀
𝐴
(
𝐿
𝑇
)
L 
T
smooth
​
 =EMA(L 
T
​
 )
Size-adjusted heat:

𝐼
ℎ
𝑖
𝑡
′
=
𝐼
ℎ
𝑖
𝑡
⋅
𝑄
𝑇
𝐿
𝑇
𝑠
𝑚
𝑜
𝑜
𝑡
ℎ
+
𝜖
I 
hit
′
​
 =I 
hit
​
 ⋅ 
L 
T
smooth
​
 +ϵ
Q 
T
​
 
​
 
A6) The Envelope (Emissions & MOB-α Rewards) — Rep affects MOB-α only
Epoch envelope pool:

𝐸
𝑟
𝑒
𝑤
𝑎
𝑟
𝑑
𝑠
,
𝑒
𝑝
𝑜
𝑐
ℎ
(
in MOB-
𝛼
)
E 
rewards,epoch
​
 (in MOB-α)
Allocate to hits:

𝑠
ℎ
=
𝑉
ℎ
𝑖
𝑡
,
ℎ
∑
𝑘
𝑉
ℎ
𝑖
𝑡
,
𝑘
⋅
(
1
+
𝜅
⋅
𝐼
ℎ
𝑖
𝑡
,
ℎ
′
)
s 
h
​
 = 
∑ 
k
​
 V 
hit,k
​
 
V 
hit,h
​
 
​
 ⋅(1+κ⋅I 
hit,h
′
​
 )
𝐸
ℎ
𝑖
𝑡
,
ℎ
=
𝐸
𝑟
𝑒
𝑤
𝑎
𝑟
𝑑
𝑠
,
𝑒
𝑝
𝑜
𝑐
ℎ
⋅
𝑠
ℎ
∑
𝑗
𝑠
𝑗
E 
hit,h
​
 =E 
rewards,epoch
​
 ⋅ 
∑ 
j
​
 s 
j
​
 
s 
h
​
 
​
 
Allocate within a hit (mobsters only):

𝑐
𝑖
=
𝑑
𝑖
∑
𝑗
𝑑
𝑗
c 
i
​
 = 
∑ 
j
​
 d 
j
​
 
d 
i
​
 
​
 
𝑟
𝑖
=
𝑅
𝑒
𝑝
𝑖
∑
𝑗
𝑅
𝑒
𝑝
𝑗
r 
i
​
 = 
∑ 
j
​
 Rep 
j
​
 
Rep 
i
​
 
​
 
𝑤
𝑖
=
𝑐
𝑖
𝛾
⋅
𝑟
𝑖
𝛿
w 
i
​
 =c 
i
γ
​
 ⋅r 
i
δ
​
 
𝑅
𝑖
,
𝑀
𝑂
𝐵
𝛼
=
𝐸
ℎ
𝑖
𝑡
⋅
𝑤
𝑖
∑
𝑘
𝑤
𝑘
R 
i,MOBα
​
 =E 
hit
​
 ⋅ 
∑ 
k
​
 w 
k
​
 
w 
i
​
 
​
 
Constraint (intentional):

TAO payout ignores Rep

Rep only affects MOB-α envelopes

A7) Tribute, Wash, and the Blessing (Boss MOB-α Escrow Return)
Minimum return depends on Boss skin ratio:

𝛽
𝑚
𝑖
𝑛
(
𝜌
)
=
0.80
+
0.10
⋅
𝜌
𝑛
𝑜
𝑟
𝑚
β 
min
​
 (ρ)=0.80+0.10⋅ρ 
norm
​
 
Returned escrow:

𝐴
𝑟
𝑒
𝑡
𝑢
𝑟
𝑛
𝑒
𝑑
=
𝐴
𝑒
𝑠
𝑐
⋅
(
𝛽
𝑚
𝑖
𝑛
(
𝜌
)
+
(
1
−
𝛽
𝑚
𝑖
𝑛
(
𝜌
)
)
⋅
min
⁡
(
1
,
  
𝐼
ℎ
𝑖
𝑡
′
)
)
A 
returned
​
 =A 
esc
​
 ⋅(β 
min
​
 (ρ)+(1−β 
min
​
 (ρ))⋅min(1,I 
hit
′
​
 ))
Lost escrow:

𝐴
𝑙
𝑜
𝑠
𝑡
=
𝐴
𝑒
𝑠
𝑐
−
𝐴
𝑟
𝑒
𝑡
𝑢
𝑟
𝑛
𝑒
𝑑
A 
lost
​
 =A 
esc
​
 −A 
returned
​
 
Split loss:

𝐴
𝑤
𝑎
𝑠
ℎ
,
𝑏
𝑢
𝑟
𝑛
=
𝜓
⋅
𝐴
𝑙
𝑜
𝑠
𝑡
A 
wash,burn
​
 =ψ⋅A 
lost
​
 
𝐴
𝑡
𝑎
𝑜
𝑓
𝑎
𝑡
ℎ
𝑒
𝑟
,
𝑏
𝑙
𝑒
𝑠
𝑠
𝑖
𝑛
𝑔
=
(
1
−
𝜓
)
⋅
𝐴
𝑙
𝑜
𝑠
𝑡
A 
taofather,blessing
​
 =(1−ψ)⋅A 
lost
​
 
Total burn:

𝐴
𝑏
𝑢
𝑟
𝑛
,
𝑡
𝑜
𝑡
𝑎
𝑙
=
𝐴
𝑡
𝑎
𝑥
+
𝜓
⋅
(
𝐴
𝑒
𝑠
𝑐
−
𝐴
𝑟
𝑒
𝑡
𝑢
𝑟
𝑛
𝑒
𝑑
)
A 
burn,total
​
 =A 
tax
​
 +ψ⋅(A 
esc
​
 −A 
returned
​
 )
Vault total:

𝐴
𝑣
𝑎
𝑢
𝑙
𝑡
,
𝑡
𝑜
𝑡
𝑎
𝑙
=
0.025
 
𝐴
𝑏
𝑜
𝑠
𝑠
A 
vault,total
​
 =0.025A 
boss
​
 
Value Proposition
For MOB-α holders
Bosses must buy MOB-α to sponsor hits

Street Tax burns MOB-α (tag + skin adjusted)

Bosses posting hits increases MOB-α utility and demand

For Bosses
You must post real target alpha — you’re a real participant

You earn TAO from your target alpha being sold plus kickback

Higher skin ratio reduces Street Tax and improves wash floor

Kickback scales with hit quality and improves with skin

For Mobsters
TAO payout is transparent and strict pro-rata by target alpha

Envelopes (MOB-α) reward hit participation

Rep increases envelope weight over time

For Consiglieres
Publish heat, payouts, and rep

Protect the streets from manipulation

FAQ
Q: Is this financial advice?
A: No.

Q: Is p_alpha a peg?
A: No. It’s a reference input used for accounting examples (a “street price” input), not a guarantee.

Q: Who can post hits or join crews?
A: Anyone. Bosses sponsor, Mobsters contribute target alpha, Consiglieres validate.

Q: Why does Street Tax depend on heat?
A: To incentivize Bosses to aim for clean hits: better heat lowers tax and increases kickback.

Q: Does Mobster reputation affect TAO payouts?
A: No. TAO is strict pro-rata by target alpha. Rep only affects MOB-α envelopes.

Q: What are the two payouts again?
A: TAO comes from selling pooled target alpha (pro-rata). MOB-α comes from envelopes (rep-weighted mining reward).
