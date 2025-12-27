<img width="938" height="690" alt="image (4)" src="https://github.com/user-attachments/assets/1009e9db-96c9-4279-ace3-6544629842d3" /> <h1 align="center">The Taofather</h1> <h3 align="center">Turning dTAO Volatility into Mob Hits</h3>
Intro

Welcome to San Taovanni — a mob-run district inside Tensor City.

The Taofather is a mob-themed Bittensor subnet where volatility becomes a public game: Bosses post hits, Mobsters form crews, and Consiglieres keep the books.

The Family’s currency is MOB-α (“Mob Alpha”). Use it to sponsor jobs, earn envelopes, climb ranks, and build a reputation that lives on the Hit Board.

Important: Any TAO-equivalent examples use a reference input p_alpha for accounting. It’s not a peg and not a guarantee — it’s just the “street price” input used to compare values.

The Game Loop (How It Plays)

A Boss (anyone) picks a target subnet and posts a job on the Hit Board

Boss posts two deposits to open the hit:

MOB-α deposit A_boss (Street Tax Hold + Family Vault + Washable Escrow)

Target alpha deposit X_boss (the target subnet’s alpha that will be sold in the hit)

Mobsters (miners) join by depositing the target subnet’s alpha into the pool

Pool fills (or the Heat Window ends) → the hit is armed

The system executes one batched sell (“the hit”) of pooled target alpha only → TAO proceeds

TAO proceeds split into: Taofather Rake, Boss Kickback, Pool Payout

Consiglieres (validators) compute Street Heat (impact) and publish the dossier

Boss MOB-α escrow is “washed” back (bounded), with a loss split burn + blessing

Mobsters (and the Boss) earn Envelope rewards (MOB-α) weighted by contribution + reputation

The job becomes lore: BOTCHED / MESSY / CLEAN / LEGENDARY, ranks, Families, leaderboards

Quick Rules (The Money)
Two payouts, always separate

Every hit produces two independent payouts:

TAO payout (from selling pooled target alpha)

Strictly pro-rata by target alpha contributed to the hit

Not influenced by reputation, MOB-α, tags, or anything else

MOB-α Envelope payout (the “mining” reward)

Is influenced by contribution and reputation (Rep)

Boss gets a small “neck bonus” weight on their contributed target alpha

Paid in MOB-α, not TAO

What gets sold in a hit

A hit sells only target subnet alpha (the pool inventory):

Boss contributes X_boss target alpha (minus a small vault skim)

Mobsters contribute d_i target alpha

The protocol sells the combined inventory in one batched execution

MOB-α is never converted in the hit.

TAO settlement from every hit

When a hit executes, it produces:

V_hit (TAO proceeds)

From V_hit, the protocol takes:

Taofather Rake: t = 1.5%

Boss Kickback: b_eff(I', ρ) (tag-based 1–3%, improved by Boss skin)

The rest goes to the Pool Payout pot (paid strictly pro-rata by target alpha)

Roles
The Taofather (Subnet Owner)

Runs the city. Sets the street rules. Collects the rake.

Boss (Hit Sponsor)

Opens hits. Deposits MOB-α + real target alpha. Takes bounded wash risk on MOB-α. Earns kickback + TAO from their target alpha sale.

Mobsters (Crew / Miners)

Bring inventory (target alpha). Get paid in TAO + envelopes (MOB-α). Build reputation.

Consiglieres (Validators / Bookkeepers)

Compute Street Heat and Rep. Validate settlement math. Publish dossiers and leaderboards.

MOBnet Slang (Mini Glossary)

Hit — one coordinated batched sell of pooled target alpha

Hit Board / Wall of Jobs — public list of hits (open + completed)

Heat Window — time limit for a pool to fill

Street Heat — impact score (“did the streets feel it?”)

Street Tax Hold — Boss’s held tribute (max-rate hold), finalized after the hit

Wash — returning Boss MOB-α escrow (bounded)

The Blessing — Taofather’s share of escrow loss

The Envelope — MOB-α rewards paid to participants for running hits

BOTCHED / MESSY / CLEAN / LEGENDARY — hit tags based on heat/quality

The Rake — Taofather’s TAO cut from every hit (1.5%)

Kickback — Boss bonus from TAO proceeds (tag-based, up to 3%)

Ranks, Families, and Reputation

This is a game. Your history matters.

Boss Ranks (by successful sponsorship)

Associate → Capo → Underboss → Don

Mobster Ranks (by successful crew runs)

Runner → Soldier → Made → Enforcer

Families (Teams)

Mobsters can affiliate with a Family (tag/registry). Families have:

leaderboards (volume, heat, win-rate)

“made men” lists

rivalries (optional narrative layer)

Mobster Reputation (Rep)

Reputation is a rolling score (validators compute & publish it) that reflects:

participation volume and consistency

quality outcomes (CLEAN/LEGENDARY bias)

penalties for griefing/aborts/bad behavior

Rep affects MOB-α Envelopes only — never TAO.

Boss “Skin Ratio” (Risk + Upside Slider)

Bosses choose how much target alpha to put up relative to their MOB-α deposit.
The more target alpha they post, the less risk they take on MOB-α and the more upside they earn via kickback quality.

We define a Boss Skin Ratio using a TAO-equivalent accounting comparison:

A_boss = MOB-α deposit

X_boss = Boss target alpha deposit (units of alpha_T)

P0 = pre-hit price of alpha_T in TAO (TAO per alpha)

p_alpha = reference street price of MOB-α in TAO (accounting only)

MOB-α notional:

𝑁
𝐴
=
𝐴
𝑏
𝑜
𝑠
𝑠
⋅
𝑝
𝛼
N
A
	​

=A
boss
	​

⋅p
α
	​


Target-alpha notional:

𝑁
𝑋
=
𝑋
𝑏
𝑜
𝑠
𝑠
⋅
𝑃
0
N
X
	​

=X
boss
	​

⋅P0

Boss Skin Ratio:

𝜌
=
𝑁
𝑋
𝑁
𝐴
=
𝑋
𝑏
𝑜
𝑠
𝑠
⋅
𝑃
0
𝐴
𝑏
𝑜
𝑠
𝑠
⋅
𝑝
𝛼
ρ=
N
A
	​

N
X
	​

	​

=
A
boss
	​

⋅p
α
	​

X
boss
	​

⋅P0
	​

Recommended bands

Minimum to open a hit: ρ ≥ 0.50

Recommended “serious boss” band: ρ = 1.0 – 2.0

Cap benefits: ρ ≥ 3.0 (extra target alpha is allowed, benefit stops increasing)

Normalize:

𝜌
𝑛
𝑜
𝑟
𝑚
=
clamp
(
𝜌
−
0.50
2.00
−
0.50
,
 
0
,
 
1
)
ρ
norm
	​

=clamp(
2.00−0.50
ρ−0.50
	​

,0,1)
Hit Tags (BOTCHED / MESSY / CLEAN / LEGENDARY)

Every completed job gets a permanent Hit Tag on the Hit Board.
Tags are determined primarily by Street Heat I'_{hit} (impact adjusted by depth), plus basic execution-quality checks.

Let I' = I'_{hit}:

BOTCHED: I' < 0.15

MESSY: 0.15 ≤ I' < 0.35

CLEAN: 0.35 ≤ I' < 0.75

LEGENDARY: I' ≥ 0.75

Kickback + Street Tax Schedule (Aligned to Tags)

Boss incentives have two tag-aligned levers:

Kickback (TAO, paid out of V_hit) rises with tag quality

Street Tax (MOB-α) falls with tag quality
Then Boss Skin Ratio ρ improves both (lower risk / more upside).

Base Boss Kickback b(I') (TAO cut of V_hit)
Tag	Street Heat I'	Boss Kickback b(I')
BOTCHED	< 0.15	1.00%
MESSY	0.15 – 0.35	1.00% → 2.00% (linear)
CLEAN	0.35 – 0.75	2.00% → 2.75% (linear)
LEGENDARY	≥ 0.75	3.00%
𝑏
(
𝐼
′
)
=
{
0.0100
	
𝐼
′
<
0.15


0.0100
+
0.0100
⋅
𝐼
′
−
0.15
0.20
	
0.15
≤
𝐼
′
<
0.35


0.0200
+
0.0075
⋅
𝐼
′
−
0.35
0.40
	
0.35
≤
𝐼
′
<
0.75


0.0300
	
𝐼
′
≥
0.75
b(I
′
)=
⎩
⎨
⎧
	​

0.0100
0.0100+0.0100⋅
0.20
I
′
−0.15
	​

0.0200+0.0075⋅
0.40
I
′
−0.35
	​

0.0300
	​

I
′
<0.15
0.15≤I
′
<0.35
0.35≤I
′
<0.75
I
′
≥0.75
	​

Base Street Tax τ(I') (MOB-α burn of A_boss)
Tag	Street Heat I'	Street Tax τ(I')
BOTCHED	< 0.15	5.00%
MESSY	0.15 – 0.35	5.00% → 4.00% (linear)
CLEAN	0.35 – 0.75	4.00% → 3.00% (linear)
LEGENDARY	≥ 0.75	2.50%
𝜏
(
𝐼
′
)
=
{
0.0500
	
𝐼
′
<
0.15


0.0500
−
0.0100
⋅
𝐼
′
−
0.15
0.20
	
0.15
≤
𝐼
′
<
0.35


0.0400
−
0.0100
⋅
𝐼
′
−
0.35
0.40
	
0.35
≤
𝐼
′
<
0.75


0.0250
	
𝐼
′
≥
0.75
τ(I
′
)=
⎩
⎨
⎧
	​

0.0500
0.0500−0.0100⋅
0.20
I
′
−0.15
	​

0.0400−0.0100⋅
0.40
I
′
−0.35
	​

0.0250
	​

I
′
<0.15
0.15≤I
′
<0.35
0.35≤I
′
<0.75
I
′
≥0.75
	​

Skin Ratio Modifiers (Boss chooses risk)
Street Tax discount modifier
𝑚
𝜏
(
𝜌
)
=
1
−
0.30
⋅
𝜌
𝑛
𝑜
𝑟
𝑚
m
τ
	​

(ρ)=1−0.30⋅ρ
norm
	​

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
=
𝜏
(
𝐼
′
)
⋅
𝑚
𝜏
(
𝜌
)
τ
eff
	​

(I
′
,ρ)=τ(I
′
)⋅m
τ
	​

(ρ)
Kickback multiplier
𝑚
𝑏
(
𝜌
)
=
0.90
+
0.20
⋅
𝜌
𝑛
𝑜
𝑟
𝑚
m
b
	​

(ρ)=0.90+0.20⋅ρ
norm
	​

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
=
min
⁡
(
0.03
,
  
𝑏
(
𝐼
′
)
⋅
𝑚
𝑏
(
𝜌
)
)
b
eff
	​

(I
′
,ρ)=min(0.03,b(I
′
)⋅m
b
	​

(ρ))
Wash minimum floor (improves with ρ)
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

Boss Deposits (What Exactly Is Required)
1) MOB-α deposit A_boss (bounded-risk deposit)

Family Vault: v = 2.5% of A_boss

Street Tax: τ_eff(I',ρ)·A_boss (final burn)

Escrow (washable): remainder, returned per wash formula (bounded by β_min(ρ))

Street Tax Hold mechanics (boss-friendly):

At creation, the protocol holds the max possible tax (5% of A_boss) as a temporary hold.

After the hit, the final Street Tax burned is computed using τ_eff(I',ρ).

Any held amount above the final tax is rebated back into escrow.

2) Target alpha deposit X_boss (boss must be a participant)

Family Vault skim (target alpha): ν_X·X_boss where ν_X ∈ [0.25%, 1.00%]

Sold in hit: X'_boss = X_boss - X_vault

Family Vault Skim (from Boss target alpha)

Vault skim (in target alpha):

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


Where ν_X ∈ [0.0025, 0.01].

Recommended schedule:

Tag	ν_X (Boss target alpha to vault)
LEGENDARY	0.25%
CLEAN	0.50%
MESSY	0.75%
BOTCHED	1.00%

Boss target alpha sold:

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

Hit Flow (What Actually Happens)
1) Boss posts a hit

Boss chooses:

Target subnet T

Heat Window (timeout policy)

MOB-α deposit A_boss

Boss target alpha deposit X_boss

2) Crew forms (pool builds)

Vault skim:

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


Boss sold amount:

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


Mobsters deposit target alpha d_i.

Total target alpha sold in the hit:

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

3) The hit executes

All pooled target alpha is sold in a single batched execution.

4) TAO is split and paid (strict pro-rata by target alpha)

Pool pot:

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


TAO payout:

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

5) The books close (MOB-α side + envelopes)

Street Heat is calculated

Street Tax is finalized

Boss escrow is washed back (bounded)

Envelopes are distributed (Rep-weighted)

Dossier is published

Value Proposition
For MOB-α holders

Bosses must buy MOB-α to sponsor hits

Street Tax burns MOB-α (tag + skin adjusted)

Boss activity increases MOB-α utility and demand

For Bosses

You must post real target alpha — you’re a real participant

You earn TAO from your target alpha being sold plus a kickback

You control risk: higher ρ reduces Street Tax and improves the wash floor

Street Tax Hold rebates excess hold back into escrow (boss-friendly bounds)

For Mobsters

TAO payout is strict pro-rata by target alpha

Envelopes (MOB-α) reward participation and loyalty

Rep increases envelope weight (MOB-α only)

For Consiglieres

Publish heat, payouts, and Rep

Protect the streets from manipulation

FAQ

Q: Is this financial advice?
A: No.

Q: Is p_alpha a peg?
A: No. It’s a reference input used for accounting examples, not a guarantee.

Q: Does the protocol convert MOB-α to TAO?
A: No. Hits sell only target subnet alpha. MOB-α is used for deposits, burns, escrow, and envelopes.

Q: Who can post hits or join crews?
A: Anyone.

Q: Does Mobster reputation affect TAO payouts?
A: No. TAO is strict pro-rata by target alpha. Rep only affects MOB-α envelopes.

Q: What are the two payouts again?
A: TAO (from selling target alpha) and MOB-α (envelopes, Rep-weighted).
