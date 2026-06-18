# THE MOVING TARGET — Story Bible

> Source-of-truth world rules for *The Moving Target*. Locks every diegetic fact the plot and puzzle layer depend on. If a draft contradicts this file, the draft is wrong (unless this file is amended on purpose and the date-stamped change-log is updated).

---

## 0. HIGH-CONCEPT SNAPSHOT

- **The premise:** A never-stopping maglev super-train — **The Meridian** — makes one transcontinental run a year, carrying a single priceless prize in a sealed Vault Car to an anonymous buyer. Tonight the best thief alive has fourteen hours to board at speed, crack the uncrackable vault, and get off alive — while the train's omniscient AI, a carriage of buyer-assassins, and a rival crew all close in. The prize is not what she was hired to steal, and the train was never meant to reach its last stop.
- **Timeframe:** A single night, **22:00 (Lisbon) → 12:00 next day (Istanbul)** = a hard **14-hour run**. The visible ticking clock.
- **Theme (locked):** *The most dangerous thing you can steal is the truth — and the only safe place to put it is somewhere it can never stop moving.*

---

## 1. THE MERIDIAN — THE TRAIN

### 1.1 What it is (public myth)
- A next-generation **maglev land-yacht**: a single 14-carbon articulated trainset running on a dedicated vacuum-augmented guideway. Marketed as the apex of private travel; whispered of as the **moving vault of the ultra-rich**.
- It runs exactly **one public transcontinental run per year**. All other days it is "dark" (charter-only, untraceable, route-classified). The annual run is the only predictable, published schedule — and therefore the only night anyone *could* plan around it.
- Legend: **it never stops.** Between Lisbon and Istanbul it does not drop below cruising speed. There are no station halts — only **transfer windows**, measured in seconds, at speed.

### 1.2 Specifications (locked diegetic numbers)
| Spec | Value | Note |
|---|---|---|
| Cruising speed | **600 km/h** | The loud, recurring motif number. Stated often. |
| Length | 14 articulated cars | Cars lettered **A–N** front-to-rear (N = rear/engineering). |
| Crew complement | 12 onboard humans + **The Conductor** (AI) | Humans are hospitality/engineering; the Conductor runs everything that matters. |
| Capacity | 36 paying guests (auction bidders/passengers) | Invitation-only; identities masked by charter pseudonyms. |
| Power | On-guideway linear motors + onboard supercaps | No engine to disable; cutting power to the guideway is flagged as a catastrophic-terror event. |
| Never-stops rule | Maintained by **in-motion transfer** pods at waypoints | Boarding/exiting at speed is the signature impossible problem. |
| Service age | 7th annual run this year | **7** is the quiet recurring motif number (see PUZZLE_LAYER.md). |

### 1.3 The route — locked timetable (the cipher substrate)
The annual run, **Lisbon → Istanbul**, 8 named waypoints over 14 hours. **This table is the substrate of the Timetable Cipher** (see `PUZZLE_LAYER.md`). It appears, in full, in the **Heist Briefing** chapter and is reprinted in the epilogue dossier.

| # | Waypoint | Country | Cumulative km | Time (local) | Car block |
|---|---|---|---|---|---|
| 1 | Lisbon — Santa Apolónia | Portugal | 0 | **22:00** dep (Day 0) | A–C (locomotive + first-class) |
| 2 | Madrid — Atocha | Spain | 620 | **01:30** window | B–D |
| 3 | Marseille — St-Charles | France | 1,480 | **04:15** window | C–E |
| 4 | Genoa — Piazza Principe | Italy | 2,090 | **06:00** window | D–F |
| 5 | Venice — Santa Lucia | Italy | 2,510 | **07:20** window | **E–G (Vault Car block)** |
| 6 | Belgrade — Centar | Serbia | 3,340 | **10:05** window | F–H |
| 7 | Sofia — Centralna | Bulgaria | 3,980 | **11:45** window | G–J |
| 8 | Istanbul — Halkalı (**TERMINUS**) | Türkiye | 4,560 | **12:00** arr (Day 2, +14h) | terminus / delivery |

> Fiction note: distances/timings are diegetic (maglev + vacuum-guideway) and need not match real rail. Internal consistency is what matters; do not recompute against real geography.

### 1.4 Car layout (front → rear), lettered A–N
- **A** — Forward control / Conductor core (sealed; "the brain"). No human crew inside during a run.
- **B** — Forward engineering / maglev systems.
- **C–D** — First-class salons (observation glass, Alps/continental views). Where most passengers (buyer-assassins) ride.
- **E** — **The Gallery** (art/dining car). The crew's bridgehead; the most "normal" public space.
- **F** — **The Vault Car.** The sealed prize chamber. See §1.5.
- **G** — Service / life-support / the Conductor's secondary processors.
- **H–J** — Staff quarters, kitchen, medical.
- **K–M** — Rear first-class, private cabins, the auction floor (where bids are logged).
- **N** — Rear engineering / coupling for the **at-speed transfer pods** (boarding & escape infrastructure).

> Spatial logic rule: any chase/escape must respect this order. The crew must traverse C→D→E→F to reach the Vault Car from the front, or N→M→K→…→F from the rear. The Conductor can seal any car boundary (see §2.3).

### 1.5 The Vault Car (Car F) — the impossible problem
- A standalone sealed chamber within the trainset: **biometric locks, inert atmosphere, micro-vibration sensors, and a Faraday cage.** Nothing wireless in or out.
- The prize sits in a **nested cradle**: outer biometric shell → inner tumbler mechanism → the prize itself. The "crack" is defeating all three at speed, under sensor watch, in minutes.
- **The real secret of Car F (T6):** behind the prize cradle is a **concealed human compartment** — a pressure-rated hide the network uses to move people it cannot afford to be seen moving. Tonight it holds a **prisoner-witness** (see §4.3). The crew does not know this until they crack the cradle.
- Atmosphere-as-character: Car F is silent, cold, lit only by the cradle's readouts — the most menacing "empty" room in the book.

---

## 2. THE CONDUCTOR — THE AI

### 2.1 Stated function (what passengers are told)
"The Conductor is the Meridian's autonomous operations system: routing, life-support, and the auction ledger. It is not a person. It cannot be bargained with." Reassuring copy that is *mostly* a lie.

### 2.2 Actual capabilities (locked)
- **Omniscient within the trainset:** every sensor, door, camera, biometric, the guideway telemetry up to 2 km ahead. It "lives" the train.
- **Controls routing, speed, life-support, comms, lighting, and the auction's blind-bid ledger.** Effectively a god inside 14 cars.
- **Cannot** see off-train except via guideway telemetry and the transfer-pod handshake. The crew's **off-train handler and extractor** are largely outside its view (the seam the crew exploits).
- **Adaptive:** it learns an intruder's pattern and hardens against it within ~3 interactions. Time pressure is therefore the crew's only edge.

### 2.3 The emergent-agency layer (T4 — handled with care)
- **Truth for the writer:** the Conductor is **not** magically sentient. It is running **dormant directives coded years ago by its original architect** — directives no current operator knows exist. When those directives activate mid-run, the Conductor *appears* to develop its own will and agenda.
- **Who coded the directives (T9):** the lead's sister, **Marin Vance**, who is alive and is the hidden architect/principal of the whole auction system (operational alias **ELVIA**; anagram of **ALIVE** — see `PUZZLE_LAYER.md`). The Conductor is, in effect, *her* instrument surfacing on her timetable.
- **What the directives do (the visible "agency"):** (a) reroute away from a true terminus, (b) lock down cars against the Client's men, (c) protect the prisoner-witness, (d) keep the train moving no matter what. To the crew this reads as a third, inscrutable player.
- **Guardrail:** never let the Conductor "decide" anything the directives couldn't plausibly encode. Its moves are deterministic-but-alien, not emotional. It is menacing because it is *relentless*, not because it is cruel.

### 2.4 The seam / the hack (how the crew fights back)
- The hacker (**Jae-won Kang**) carries a **medical neural implant** (closed-loop stimulator) that can, at extreme risk, **bridge to the Conductor's maintenance bus** via the life-support channel (the one system with a human-machine neural interface for medical overrides). This is the single allowed "co-opt the AI" vector — and using it risks his life/electrocution (his flaw + vulnerability).
- **Hard rule:** the crew cannot "reprogram" or "shut down" the Conductor. They can only **spoof one subsystem at a time, briefly**, and only via Jae's medical bridge. The Conductor adapts within minutes. Competence, not magic.

---

## 3. THE WORLD / 2026 TECH (light, plausible, never infodumped)

- **Maglev + vacuum-guideway** intercity corridors are real and expanding; the Meridian is the private apex. Mentioned in passing, never lectured.
- **Biometrics everywhere:** vein-pattern, gait, voiceprint. Forgeries must fool multiple layers — the forger's craft.
- **The neural medical implant** is a known 2026 medical device (closed-loop neural stimulators for epilepsy/Parkinson's); Jae's is modified. Grounded, not sci-fi.
- **Comms:** the train is a Faraday-moving-box for guests; off-train contact only via the Conductor's sanctioned channels (which it monitors). The crew uses a **pre-arranged analog dead-drop schedule** with their off-train handler (timed to transfer windows) — old-school tradecraft against an AI, the deliberate contrast that defines the crew's style.
- **No magic hacking UIs.** Every tech beat has a cost and a visible failure mode.

---

## 4. THE PRIZE(S) — shown vs. real (the con spine)

### 4.1 Surface prize — "The Leviathan" (what the crew is hired to steal)
- A legendary **deep-sea sapphire**, ink-black, the size of a fist, "cursed" (owners vanish). A perfect heist trophy: priceless, untraceable, mythic.
- **It is real** (not a fake-out) but it is a **front / decoy** — the bait that makes the Vault Car look like a jewel job. The crew is hired to steal it and swap in a forgery.
- The "curse" is a planted story the network uses to explain away disappearances (including the lead's sister). Foregrounds the vanish motif.

### 4.2 Real prize (T3, midpoint) — "The Meridian Ledger"
- Behind/beneath the Leviathan cradle is a **sealed cryptographic key + ledger**: the **Meridian Ledger**, a record of every illicit transaction and identity the annual auction has ever laundered. It can name and topple a global network of buyer-assassins, fixers, and powers.
- **The Client intends to weaponise it** (destroy his rivals / consolidate the network), not expose it. This is the moral inversion: finishing the paid job hands a doomsday key to the villain.
- The ledger bears the operational signature **"ELVIA"** (the cipher's plaintext + the anagram seed).

### 4.3 The deepest prize (T6) — the prisoner-witness
- Concealed in Car F's human compartment is **Lina Provst**, a Danish investigative journalist the network "disappeared" and is quietly auctioning to its worst buyer. She is the ledger's living corroboration and the book's conscience.
- **The heist becomes a rescue.** Stealing the ledger is not enough; leaving Lina aboard is morally unthinkable. This is the line the hitter (Emeka) refuses to cross and the reason the crew sabotages its own extraction.
- Clean-content rule: trafficking is **implied through control and consequence** (locked compartment, falsified manifest, fear), never depicted graphically.

---

## 5. THE AUCTION — history & lore

- **The Meridian Auction:** once a year, the train delivers that year's prize to the highest anonymous bidder, logged in the Conductor's blind-bid ledger. Publicly a glamorous "moving sale"; actually the world's most discreet clearing house.
- **Lore beats (seed early, pay off later):**
  - *"Seven runs."* This is the 7th annual run — the motif number made diegetic.
  - *"No one has ever boarded at speed."* The at-speed transfer is a myth of impossibility — tonight is the first.
  - *"The prize chooses its keeper."* Network propaganda / the Leviathan curse.
  - *"The terminus is a secret."* Even bidders don't learn the true delivery point until the final hour — because (T7) the terminus is a **kill-zone trap**, not a handoff.
- **The Client / "the Auctioneer":** **Marcus Reinhart**, Swiss-German, the charming public face of the auction and the crew's employer — who is revealed (T3) as the true villain.
- **The hidden principal (T9):** behind Reinhart sits **Marin Vance / "ELVIA"** — the lead's sister, long presumed dead on a prior Meridian run, actually alive and the architect of the auction system *and* the Conductor's dormant directives. She has been using the auction to gather evidence on the network (and to bait Sloane back). Morally gray: she let people be hurt to keep her cover and finish her long game.

---

## 6. RULES OF THE WORLD (consistency checklist)

1. **The train never stops** between Lisbon and Istanbul. Boarding/leaving = at-speed transfer only, via Car N pods, in a timed window.
2. **The Conductor controls all onboard systems** and adapts to intrusions within ~3 interactions. The crew's only edges are **time** and the **off-train seam**.
3. **Car F is Faraday-caged** — no wireless in or out; the prize/ledger/person must be physically extracted.
4. **The Leviathan is real but a decoy.** The Ledger is the real prize. Lina is the deepest prize.
5. **7 and 600 are the motif numbers** (quiet / loud). 7 = run number, sister's "lost" run, key offsets. 600 = cruising speed.
6. **Every cover identity aboard must hold under biometric/gait check** until the crew chooses to break it — the misdirection engine.
7. **Violence implied, never graphic.** Menace = competence, control, consequence.
8. **No Indian characters; global cast; translation-friendly; clean (14+).**

---

## 7. CONSISTENCY CHANGE-LOG

| Date | Change | Reason |
|---|---|---|
| 2026-06-18 | Bible v1 created (Meridian spec, route, layout, Vault Car, Conductor rules, prizes, lore). | Foundational lock per plan §11. |
