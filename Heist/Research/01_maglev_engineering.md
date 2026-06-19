# 01 — Maglev Engineering Brief for *THE MOVING TARGET*

**Purpose:** Make the Meridian (fictional 600 km/h nonstop maglev, Lisbon→Istanbul, ~4,560 km, ~14 h, GoA4 "Conductor") factually airtight for expert readers — especially the **pod-docking (Ch11)**, the **"turn the train" routing override onto a maintenance spur (Ch37)**, and the **pod braking to a platform (Ch39)**.

**Sourcing convention:** Every claim carries a source. `[V]` = verified against a primary/manufacturer or solid secondary source this session. `[?]` = UNVERIFIED to the specific number — directionally correct engineering, but confirm against a manufacturer/JR-Central/Transrapid technical manual before it appears as hard prose. **No numbers below were fabricated.**

Primary/secondary sources used:
- S1 Maglev (overview): https://en.wikipedia.org/wiki/Maglev
- S2 Chūō Shinkansen (JR-Central specs): https://en.wikipedia.org/wiki/Ch%C5%AB%C5%8D_Shinkansen
- S3 SCMaglev (EDS mechanism): https://en.wikipedia.org/wiki/SCMaglev
- S4 Transrapid (EMS mechanism, braking, power): https://en.wikipedia.org/wiki/Transrapid
- S5 Shanghai maglev train (maintenance base, switches, speed profile): https://en.wikipedia.org/wiki/Shanghai_maglev_train
- S6 L0 Series (aero nose, bogies, induction power): https://en.wikipedia.org/wiki/L0_Series_Shinkansen
- S7 Emsland test facility (turning loops, 2006 collision): https://en.wikipedia.org/wiki/Emsland_test_facility
- S8 Magnetic levitation (physics): https://en.wikipedia.org/wiki/Magnetic_levitation
- S9 Argonne National Lab — He, Rote, Coffey (1994), *Study of Japanese Electrodynamic-Suspension Maglev Systems*, ANL/ESD-20 (primary technical): https://www.osti.gov/biblio/10150166 (DOI 10.2172/10150166)
- S10 Guardian, 21 Apr 2015 (603 km/h manned record): https://www.theguardian.com/world/2015/apr/21/japans-maglev-train-notches-up-new-world-speed-record-in-test-run

---

## VERIFIED FACTS

### 1. Levitation & Propulsion — EMS vs EDS, and which one a 600 km/h ship uses

- **Two levitation families** `[V S1 S3 S4 S8]`:
  - **EMS (Electromagnetic Suspension) = ATTRACTION.** Electromagnets on the vehicle are pulled *up* toward the underside of the guideway rail. Inherently unstable → held stable by a servo loop. Example: **Transrapid / Shanghai** (431 km/h service, 501 km/h test). Levitates from a standstill. `[V S4]`
  - **EDS (Electrodynamic Suspension) = REPULSION.** Moving superconducting (or permanent/Halbach) magnets on the vehicle induce currents in guideway coils; the induced field repels (Lenz's law). Inherently stable but **only levitates once moving** — needs wheels at low speed. Example: **JR-Maglev / SCMaglev / Chūō Shinkansen / L0 Series.** `[V S3 S9]`
- **A 600 km/h system uses EDS with superconducting magnets.** The manned rail speed record is **603 km/h (21 Apr 2015, L0 Series, 7-car set)** — an EDS/superconducting system. `[V S3 S6 S10]` EMS systems (Transrapid) top out ~500–550 km/h design. The Meridian should therefore be **EDS + superconducting magnets (SCMaglev-derived)**. `[V S3 S4]`
- **SCMaglev mechanism (the real detail that sells it):** `[V S3 S9]`
  - Onboard **superconducting magnets** in the bogies.
  - Guideway walls carry **"figure-8" null-flux coils, cross-connected underneath the track.**
  - Below ~150 km/h the train rolls on **rubber tires** (the magnets sit below coil center; no induced lift). At **~150 km/h** induced current is sufficient to **lift the train ~100 mm (≈4 in)** off the guideway; wheels retract. `[V S3 S9]`
  - The same cross-connected null-flux coils provide **lateral guidance** (push the car back to centerline if it drifts) — this is the genuine physical basis for any "the field holds it on the line" language.
- **Propulsion = a Linear Synchronous Motor (LSM).** A second set of coils in the guideway is the unrolled "stator"; the train's superconducting magnets are the "rotor." A travelling magnetic field, frequency synchronized to speed, drags the train. `[V S3]` Transrapid similarly uses a **synchronous longstator linear motor** for *both* propulsion and braking. `[V S4]`
- **Power to the vehicle is CONTACTLESS.** `[V S2 S4 S6]`
  - Chūō Shinkansen: guideway propulsion coils fed at **33 kV AC, variable frequency** (≈**51.4 Hz at 500 km/h**); vehicles draw power by **inductive coupling at ~9.8 kHz** (resonant wireless power transfer) — no pantograph. `[V S2]`
  - Earlier L0 cars used a small onboard **gas-turbine generator**; the Improved L0 (2020) switched to guideway **induction**. `[V S6]`
  - Transrapid TR08 drew onboard power from parasitic magnetic-field oscillation above 80 km/h; TR09 is fully contactless at all speeds; on backup batteries it can keep levitating down to ~10 km/h. `[V S1 S4]`
- **Other handy verified numbers:** Chūō Shinkansen **max gradient 4%** (vs 3% classic Shinkansen) `[V S2]`; ~86–90% of the Tokyo–Nagoya alignment is in tunnel `[V S2]`; relative passing-speed record **1,026 km/h** (two MLX01 trains, Nov 2004) `[V S3]`; L0 **15 m-long nose** is specifically for "better aerodynamics and reduced noise in tunnels" `[V S6]`; L0 uses **Jacobs bogies** (shared between cars → the train is semi-rigid/short-coupled, which matters for articulation — see Corrections). `[V S6]`

### 2. Switching / Turnouts (the heart of the "turn")

- **A maglev cannot use an ordinary railway switch.** The guideway *is* the motor (coils/stator built into the beam), so branching means physically redirecting a load-bearing, coil-embedded structure. `[V S4 ("the track being a part of the engine… the highly complicated crossings and switches")]`
- **Real maglev switches are MOVABLE GUIDEWAY BEAMS** — long sections of the running beam that physically bend/pivot sideways to align with the diverging route, then re-lock. `[V S1 S5]` This is qualitatively verified; **the exact actuation time and beam length are `[?]`** — directionally they are slow, civil-engineering objects (tens of seconds to well over a minute for a full-speed turnout), not the sub-second "throw a switch" of a model railway. **Confirm exact figures against a Transrapid/JR-Central turnout spec before quoting a number.**
- **Switches do exist on real lines.** Shanghai Transrapid was built with **"several switches"** plus a **maintenance facility and vehicle yard** off the main line `[V S1]`, and a **separate spur track to the Maglev Maintenance Base** near Pudong Airport `[V S5]`. So a "maintenance spur / depot turnout" is a real, legitimate concept for the Meridian. `[V S1 S5]`
- **Maglev test lines reverse trains with TURNING LOOPS, not switches.** Emsland has a turning loop at each end (Y-shaped balloon) on a single elevated track. `[V S7]` Useful for how the Meridian is turned/stored at terminals.
- **Branching at 600 km/h is essentially impossible.** `[physics, see Math section]` A high-speed turnout requires a *huge* diverging radius; you cannot flick a train onto a tight spur at cruise. Real systems slow dramatically first. This is the single most important correction for Ch37.
- **EDS nuance worth using:** because the null-flux guidance coils are continuous and the "motor" is the guideway, an EDS switch cannot simply be "rewired" by flipping a coil — the geometry of the beam itself must change. So a "legacy routing override" would realistically **(a) pre-position the movable switch-beam minutes ahead, and (b) command a deceleration profile** so the train can actually take the branch. That is exactly the kind of thing a hijacked GoA4 automation layer would do — drama preserved, physics saved. `[V S3 S4 S9]`

### 3. Real curve geometry (Chūō Shinkansen)

- **Minimum curve radius: 8,000 m** at a design/operating speed of **500–505 km/h**, max gradient 4%. `[V S2]`
- That radius is dictated by lateral-acceleration comfort limits (see Math). A 600 km/h ship needs an **even larger** radius than 8,000 m. `[physics]`

### 4. Braking

- **Primary brake = regenerative, via the linear motor run in reverse**, feeding energy back to the grid. `[V S1 S4]` ("the propulsion system is also capable of functioning in reverse, energy is transferred back into the electrical grid during braking" `[S4]`).
- **Emergency / last-resort = mechanical.** Transrapid carries **emergency landing skids** beneath the vehicle that drop onto the guideway; intended only if levitation can't be sustained on backup batteries to a natural stop. `[V S4]` EDS systems add **eddy-current / linear-generator braking**. `[V S1 S8]` (Eddy-current braking is verified as a maglev concept; **the exact emergency decel rate is `[?]`.**)
- **Normal deceleration ≈ 1 m/s²** (Transrapid 09, designed for cruise 505 km/h, "acceleration and deceleration of approximately 1 m/s²"). `[V S4]` Maglevs decelerate "faster than mechanical systems regardless of… grade, because they are non-contact." `[V S1]`
- Stopping-distance math from these figures is in the Math section.

### 5. Noise / Vibration / Sensory profile

- **Maglev is quieter than conventional rail at a given speed** (no wheel–rail contact roar, no rolling resistance). `[V S1]` At 500–600 km/h the dominant noise is **aerodynamic** (boundary-layer hiss, nose compression), not mechanical. `[V S1 S6]`
- **Tunnel sonic-boom (micro-pressure wave) is a real, designed-around problem** at these speeds — it is precisely why the L0 nose is **15 m long** and why entrance hoods are engineered. `[V S6]` Excellent atmospheric detail for tunnel scenes.
- **Inside the cabin:** notably smooth — no vibration from wheel contact, "frictionless magnetic cushion." `[V S4]` EMS control samples the gap **100,000×/second** (Transrapid) — i.e., levitation is an aggressively servo'd thing, which is good tension material (it can fail). `[V S4]`
- **Exact dB(A) figures inside/outside: `[?]`** — not verified this session; get a JR/Transrapid measurement if a hard decibel number must appear. Qualitative profile above is sourced.

### 6. Maintenance spurs / yards

- **Confirmed concept:** Shanghai Transrapid has a **maintenance facility + vehicle yard + several switches + a spur to the Maglev Maintenance Base** off the main elevated line. `[V S1 S5]` A "maintenance spur / depot turnout / runaway/braking siding" is therefore authentic for the Meridian.
- Test facilities (Emsland) are **elevated viaducts** with **turning loops** at each end; piers are closely spaced (Shanghai used **25 m pier spacing**, piles driven to **70 m** in soft soil) to hold the mm-scale alignment tolerance the active control needs. `[V S5 S7]` Great detail: a maglev guideway is a precision structure, which a saboteur could threaten by misaligning a pier/beam.
- The **2006 Lathen collision** (23 dead): a Transrapid hit a maintenance vehicle at **170 km/h** on the test track — proves maintenance vehicles *do* operate on the guideway and that collision at speed is catastrophic. `[V S4 S7]` Directly relevant to pod-docking and any "something on the guideway" beat.

---

## SWITCHING & THE "TURN" (Ch37 deep-dive)

**What the manuscript currently implies:** a "legacy routing override" that "throws a switch onto a maintenance spur," shown as the maglev field realigning and guideway "handposts" redirecting momentum, with a "two-degree bank to starboard" and articulated cars flowing through "like a snake" — all within roughly the final 9 minutes.

**What is physically true and should be kept:**
- A routing override **can** reroute the ship — but via a **movable guideway beam** (a heavy, coil-embedded beam that bends sideways and re-locks), not a rail switch `[V S4]`.
- The "field realigning to hold the line" is a *legitimate* image: the **null-flux guidance coils** really do generate the lateral centering force on an EDS maglev `[V S3 S9]`. So you can honestly say the guideway's fields are what *guide* the ship through the curve.
- A maintenance **spur / depot turnout is real** `[V S1 S5]`.

**What an expert will reject (must fix):**
1. **No sharp branch at 600 km/h.** A spur is a *tight* radius; physics forbids entering one at cruise (see Math — a 500 m spur at 600 km/h demands ~5.7 g lateral). The ship **must decelerate first.**
2. **A switch is not instantaneous.** The movable beam is a slow, pre-set civil object; it is positioned and locked **before** the ship arrives, and the ship is many km away (10 km per minute at 600 km/h). "Throw a switch" 30 s before arrival is not how it works.
3. **"Two-degree bank" is far too shallow** to be a perceptible high-speed curve (see Math). Real high-speed banks are ~8–15°.
4. **"Snake-like articulation" is wrong for these trains.** L0/SCMaglev cars share **Jacobs bogies** and are short-coupled/semi-rigid `[V S6]`; they don't slither like hinged coaches. They follow a curve as a near-rigid body riding the banked beam.
5. **The 9-minute window is fine *only if* the override is really a pre-planned deceleration + switch-throw sequence** baked into the automation — which is precisely what a hijacked GoA4 "Conductor" layer would do. Reframe the override as: it silently **reprograms the stopping profile and locks the diverging beam kilometers ahead**, so by the time anyone notices, the ship is already committed and braking for the branch.

**Plausible reframing (keeps the drama):** The override doesn't "turn a speeding train" — it **traps the Conductor's automation into a doomed timetable**: command a regenerative deceleration from 600 → ~200 km/h over ~13 km (≈2.1 min) `[math]`, pre-set the movable switch-beam on the spur while the ship is still 15+ km out, then take the tighter spur curve at the lower speed. The tension becomes *can the crew reverse/override the override and re-accelerate before the beam commits*, racing the geometry — which is more "competence porn" and more correct than a magic mid-air swerve.

---

## CURVE / BANK / BRAKING MATH

Constants: g = 9.81 m/s². Speeds: 600 km/h = 166.67 m/s; 500 km/h = 138.89 m/s; 200 km/h = 55.56 m/s; 150 km/h = 41.67 m/s; 100 km/h = 27.78 m/s.

### A. Lateral acceleration and bank
Centripetal accel needed: **a = v² / R**. On a banked (canted) guideway the gravity component **g·sin θ** supplies part of it; what passengers *feel* is the **cant deficiency** ≈ (v²/R − g·sin θ).

**Sanity check against the real Chūō Shinkansen** `[V S2]`: R = 8,000 m at 500 km/h → a = 138.89²/8000 = **2.41 m/s² = 0.246 g**. Balance bank angle: tan θ = 0.246 → **θ ≈ 13.8°**. So the world's only near-600-class line banks its minimum-radius curves on the order of **~14°**, not 2°. `(Derivation; source for the 8000 m / 500 km/h inputs: S2.)`

**The manuscript's "2-degree bank" at 600 km/h:** balance radius = v²/(g·tan 2°) = 166.67²/(9.81·0.0349) = **≈81,000 m (81 km)**. A 2° bank at cruise is an essentially-straight, imperceptible alignment — it cannot read as a dramatic "turn to starboard." Off by roughly **5–7×** vs a real high-speed bank.

**Realistic 600 km/h curve radius:**
- Comfortable (cant deficiency ≤ 0.10 g, bank 12°): g·sin12° = 2.04 m/s²; allowable total = 2.04 + 0.98 = 3.02 → **R ≥ 166.67²/3.02 ≈ 9,200 m (~9.2 km).**
- Very comfortable (cant deficiency ≤ 0.05 g, bank 10°): total = 1.70 + 0.49 = 2.19 → **R ≥ ~12,700 m (~12.7 km).**

**Bottom line:** at 600 km/h the minimum curve radius is **~9–13 km**; the bank is **~10–15°**. Any "turn" must be on that scale or the ship must slow down first.

### B. Can you "turn within 9 minutes at 600 km/h"?
9 min at 600 km/h = **90 km** of travel. Time to change heading by angle φ on radius R: t = R·φ/v.
- Deflect **30° (0.524 rad)** on R = 9 km: arc = 4.7 km, **t ≈ 28 s**. So a *gentle* curve is quick in time — **but only if the ship is already on a ~9–13 km-radius banked alignment.** You cannot *enter* such a curve at 600 km/h from straight track without a transition (spiral) and you absolutely cannot take a tight spur at speed.

### C. Braking distances (regenerative, a ≈ 1 m/s² normal `[V S4]`; emergency `[?]`)
- **600 → 0 at 1 m/s²:** distance = v²/2a = 166.67²/2 = **13.9 km**, time **≈2.8 min.**
- **600 → 0 at 2 m/s² (emergency, est.):** **6.9 km**, ~1.4 min. (at 3 m/s²: **4.6 km**, ~56 s.)
- **500 → 0 at 1 m/s²:** **9.6 km.**
- **600 → 150 (spur speed) at 1 m/s²:** Δv=125 m/s → **≈2.1 min**, distance ≈ (166.67² − 41.67²)/2 = **≈13.0 km.**
- **150 → 0 at 1.5 m/s²:** **≈257 m** (short platform). **100 → 0 at 1.5 m/s²:** **≈115 m.**

So slowing from cruise to spur-entry speed consumes most of a multi-minute window and ~13 km — entirely consistent with a 9-minute climax **if the deceleration is pre-programmed**. `[math; source for 1 m/s²: S4]`

### D. Pod braking (Ch39) — a detached pod from ~600 km/h to a platform
- A separate EDS maglev pod can brake via its own **linear-generator + eddy-current braking + emergency skids** `[V S1 S4 S8]`.
- From 600 km/h at ~2 m/s²: **~6.9 km** to stop; at ~3 m/s²: **~4.6 km.** A "platform" the pod rolls onto is therefore preceded by a **multi-kilometre braking/deceleration lane**, not a short bay. `(math; pod-specific decel rate `[?]`.)`
- **Implication for staging:** the pod detaches, runs the field down over several km of guideway, and only then meets a platform/stop-beam. If the manuscript has the pod stopping in a short distance at 600 km/h, it must either (a) show a long braking run-out, or (b) give the pod an aggressive brake + a long landing zone.

### E. Pod docking at 600 km/h (Ch11)
- An EDS pod only levitates **above ~150 km/h** `[V S3]`, so it must **boost itself to match-velocity on a parallel/converging guideway** before clamping — it can't taxi up from rest. Matching 600 km/h and "clamping to the hull" is plausible only if the pod is a self-propelled maglev vehicle running its own guideway that converges and parallels the Meridian, then locks on. A great grounding beat: the pod must already be at cruise on its own beam; the docking is a *convergence + magnetic capture*, not a chase from behind.

---

## EXPERT TELLS (8–12 details a rail engineer will clock as authentic)

1. **Runs on rubber tires below ~150 km/h, then lifts ~100 mm off the guideway** once EDS induction takes over — wheels retract. `[V S3]`
2. **Superconducting magnets in the bogies + figure-8 null-flux coils in the guideway walls, cross-connected beneath the track** — the actual SCMaglev architecture. `[V S3 S9]`
3. **Contactless power: no pantograph** — vehicle draws via ~9.8 kHz inductive coupling; guideway coils fed 33 kV variable-frequency AC (≈51.4 Hz at 500 km/h). `[V S2]`
4. **The guideway IS the motor** (unrolled longstator linear synchronous motor); "the motor is in the track," which is exactly why switches and crossings are "highly complicated" and why you can't just re-route at speed. `[V S3 S4]`
5. **Switches are movable guideway beams that bend and re-lock** — slow, pre-set civil objects, positioned while the ship is still 10+ km away (10 km/min at cruise). `[V S1 S4 S5]`
6. **Curves are enormous and steeply banked: ~8,000 m radius at 500 km/h (~14° balance bank)** — a 600 km/h ship needs ~9–13 km radius. `[V S2 + math]`
7. **Regenerative braking** feeds the grid; emergency is eddy-current/skids, with the ship able to hold levitation on batteries down to ~10 km/h. `[V S1 S4]`
8. **The 15 m nose** exists to cut aerodynamic drag and **tunnel sonic-boom (micro-pressure wave)** — the signature high-speed-maglev engineering tell. `[V S6]`
9. **Jacobs (shared) bogies** make the trainset a semi-rigid, short-coupled body — it does **not** snake like hinged coaches. `[V S6]`
10. **Precision guideway: ~25 m pier spacing, deep piles**, because the active levitation needs mm-scale alignment — a fragility a saboteur can threaten (beam/pier misalignment). `[V S5 S7]`
11. **Maintenance vehicles do run on the guideway** — the 2006 Lathen collision (Transrapid vs maintenance vehicle, 170 km/h, 23 dead) is the real-world precedent for catastrophic at-speed contact. `[V S4 S7]`
12. **Termini use turning loops**, not reversing switches; depots sit on spurs off the main line (Shanghai's Maglev Maintenance Base). `[V S1 S5 S7]`

---

## GROUNDING OPPORTUNITIES (chapter → insert)

- **Ch11 (pod docking):** Show the pod already at cruise on its **own parallel guideway**, levitated (>150 km/h), then **converging and magnetically capturing** the hull — not a from-behind chase. Plant the "guideway is the motor" idea here (it pays off in Ch37). `[V S3 S4]`
- **Ch11 / general:** A beat where, below a certain speed, the Meridian **drops onto its rubber tires** (e.g., during any low-speed emergency) — authentic EDS behaviour and a strong sensory shift (the sudden *return* of mechanical contact/vibration). `[V S3]`
- **Ch37 (the "turn"):** Reframe the override as a **pre-programmed deceleration + locked movable switch-beam** committed kilometers ahead. Show the **regenerative braking dumping megawatts to the grid**, speed bleeding 600→~200 over ~13 km, then the tighter banked spur curve at lower speed. The Conductor's automation is the thing being subverted. `[math; V S1 S4 S5]`
- **Ch37:** Drop the "two-degree bank" and "snake" language. Use the real **~9–13 km radius / 10–15° bank** at cruise, and describe the cars as a **near-rigid body on a banked beam**, held by the **null-flux guidance field** (the honest version of "the field holds it on the line"). `[V S3 S6 + math]`
- **Ch39 (pod braking):** Give the pod a **multi-kilometre braking/deceleration lane** before the platform (≈5–7 km from 600 km/h at realistic emergency decel); show linear-generator/eddy-current braking + a final skid/stop-beam drop. `[math; V S1 S4]`
- **Atmosphere (any tunnel scene):** The **15 m nose** and the **tunnel micro-pressure wave (sonic-boom)** are the signature sounds/pressures of a 600 km/h ship in a tube — use them for dread. `[V S6]`
- **Sabotage seed:** The **mm-scale guideway alignment** (25 m piers, deep piles) is a precision structure; threatening to misalign a beam/pier is a credible, engineer-respectable hazard. `[V S5 S7]`
- **Real-world precedent drop:** Reference-class detail that an EDS maglev hit a maintenance vehicle at 170 km/h (Lathen, 2006) — establishes that anything on the guideway at speed is fatal, raising pod/docking stakes. `[V S4 S7]`

---

## CORRECTIONS NEEDED (explicit)

| # | Manuscript claim | Problem | Fix |
|---|---|---|---|
| 1 | "Throws a switch onto a maintenance spur" ~at speed / near-instant | Maglev switches are **movable guideway beams**, slow & pre-set km ahead; cannot be thrown moments before arrival at 600 km/h `[V S4]` | Override **pre-locks the beam + pre-programs deceleration** many km/min ahead; drama = racing the committed geometry |
| 2 | Diverts onto a spur **at 600 km/h** within ~9 min | Physics forbids a tight branch at cruise (~5.7 g on a 500 m spur — lethal) `[math]` | Ship **decelerates 600→~200 (~13 km, ~2.1 min)** before the branch; takes the tighter spur curve at low speed `[V S4 + math]` |
| 3 | "Two-degree bank to starboard" as a noticeable turn | 2° bank balances only an ~81 km radius — imperceptible; real high-speed banks are ~10–15° `[math; S2]` | Use **~10–15° bank on a ~9–13 km radius** at cruise (or a steeper bank at the lower spur speed) |
| 4 | Articulated cars flow through the curve "like a snake" | L0/SCMaglev use **Jacobs bogies** → short-coupled, near-rigid; they don't slither `[V S6]` | Describe a **near-rigid body settling onto a banked beam**, held laterally by the **null-flux guidance field** |
| 5 | Pod detaches & brakes to a platform over a short distance from ~600 km/h | Even aggressive emergency braking needs **~5–7 km** `[math]` | Give the pod a **multi-km braking lane/run-out** before the platform; linear-generator + eddy + skids `[V S1 S4]` |
| 6 | Pod "clamps to the hull" after catching up from behind | An EDS pod must be **levitating (>150 km/h) on its own guideway** to exist at all `[V S3]` | Pod is **already at cruise on a converging/parallel beam**; docking = magnetic capture at match-velocity |

**Items still to verify before they become hard prose `[?]`:** exact maglev switch-beam actuation time and beam length; exact emergency deceleration rate (m/s²) for EDS/Transrapid; exact cabin/trackside noise levels in dB(A). Directionally the brief above is correct; do not print a specific figure for these until confirmed against a JR-Central/Transrapid turnout or braking spec.

---

## ONE-LINE SOURCE INDEX
S1 https://en.wikipedia.org/wiki/Maglev · S2 https://en.wikipedia.org/wiki/Ch%C5%AB%C5%8D_Shinkansen · S3 https://en.wikipedia.org/wiki/SCMaglev · S4 https://en.wikipedia.org/wiki/Transrapid · S5 https://en.wikipedia.org/wiki/Shanghai_maglev_train · S6 https://en.wikipedia.org/wiki/L0_Series_Shinkansen · S7 https://en.wikipedia.org/wiki/Emsland_test_facility · S8 https://en.wikipedia.org/wiki/Magnetic_levitation · S9 https://www.osti.gov/biblio/10150166 (Argonne, He/Rote/Coffey 1994) · S10 https://www.theguardian.com/world/2015/apr/21/japans-maglev-train-notches-up-new-world-speed-record-in-test-run
