# 03 — Train Control, Safety Architecture & OT/ICS Security

**Purpose.** Make the Meridian / CONDUCTOR cyber-plot airtight for expert readers (rail-signal engineers, OT/ICS-security professionals). Every factual claim is sourced; claims I could not verify against a primary source this session are **flagged [UNVERIFIED]**. This brief follows the project rule: it *describes in detail what is real* and what the fiction must do to sit on top of the real; it does not hand out opinions or scores.

**Method note.** Sources fetched live this session are listed inline as URLs. Wikipedia is treated as a *secondary* pointer; where it cites a primary spec/standard (IEC, ERA, CENELEC, IEEE, UITP, CEPT), that standard is named so an expert can open it. The few standards I name but did **not** open the primary text of this session are **flagged [UNVERIFIED — standard exists, primary not opened]**.

---

## Modern Train Control (ERTMS / ETCS / ATO)

### The umbrella and its parts
**ERTMS** (European Rail Traffic Management System) is the EU standards umbrella run by the European Union Agency for Railways (ERA). It bundles two separately-managed parts:
- **ETCS** — the signalling/train-control component.
- **GSM-R** — the radio communication component (now being replaced by **FRMCS**).

Source: https://en.wikipedia.org/wiki/European_Rail_Traffic_Management_System

### ETCS levels (the spec backbone a "Conductor" would be built on)
ETCS is specified at numbered **levels**. The authoritative descriptors (from the ETCS article, citing ERA SUBSET-026 and the CCS TSI):

| Level | What it is |
|---|---|
| **Level 0** | ETCS-fitted vehicle on a non-ETCS route; on-board max-speed supervision only, driver obeys lineside signals. |
| **Level 1** | Spot data from track to train via **Eurobalises/Euroloops** superimposed on legacy signalling. |
| **Level 2** | **Radio-based (GSM-R)** continuous movement authority from a **Radio Block Centre (RBC)**; balises only for precise position; track circuits/axle counters still detect train integrity. |
| **Level 3** | **Moving block**: train location and **train-integrity supervision no longer rely on trackside equipment** (no track circuits/axle counters). *Note: Levels 2 and 3 were merged as an extended Level 2 in the CCS TSI 2023.* |

Key on-board/trackside components an expert expects named: **European Vital Computer (EVC)**, **Euroradio**, **Balise Transmission Module**, **Juridical Recording Unit (black-box)**, **RBC**, **Eurobalise**, **DMI (Driver Machine Interface)**.

Source: https://en.wikipedia.org/wiki/European_Train_Control_System

> **Fiction alignment.** A god-like autonomous "Conductor" is most credibly a **Level 3 / extended-Level-2 moving-block** system with **ATO up to GoA4** (see below), using **FRMCS** radio. Moving block is what you want: the protected zone *moves with the train*, and the system knows train position to high resolution without track circuits — perfect for a single, dedicated, never-stopping maglev guideway.

### ATO and Grades of Automation (GoA0–GoA4)
**ATO (Automatic Train Operation)** is the *non-safety* layer that drives the train (station stops, traction/braking, doors) **on top of** the safety layer (ATP — Automatic Train Protection). Grades of Automation are defined in **IEC 62290-1** (UITP):

- **GoA0** – on-sight, no automation.
- **GoA1** – manual driving, train-protection system (e.g. ETCS L1) supervises.
- **GoA2** – semi-automatic (STO): start/stop automated, driver handles doors + emergencies.
- **GoA3** – driverless (DTO): automated run, on-board attendant for doors/emergencies.
- **GoA4** – **unattended (UTO/MTO): fully automated, no on-board staff required for safe operation.** This is the "driverless" grade. **CBTC is considered a basic enabler technology for GoA4.**

Real GoA4 systems exist: Singapore Thomson–East Coast Line, Vancouver SkyTrain, Delhi/Bangalore Metro, etc. Critically for the fiction: **in October 2021, Hamburg launched the pilot of the "world's first automated, driverless train on regular tracks shared with other rail traffic"** — i.e., GoA4 is now demonstrable on *mainline, mixed-traffic* track, not just isolated metro guideways.

Source: https://en.wikipedia.org/wiki/Automatic_train_operation

**ATO over ETCS (up to GoA4)** is an active standardisation programme (ERA / X2Rail). The 2017 ERA deck "X2Rail-1 ATO over ETCS (up to GoA4)" is a citable primary pointer.

Source (cited via ATO article ref 13): https://web.archive.org/web/20220718154845/https://www.era.europa.eu/sites/default/files/events-news/docs/ccrcc_2017_ato_era_en.pdf

### GSM-R and its successor FRMCS
- **GSM-R** is the dedicated railway radio carrying ETCS movement authorities today.
- **FRMCS (Future Railway Mobile Communication System)** is its successor, standardised by the **UIC**, built on **5G NR** (it deliberately leapfrogs LTE-R). GSM-R approaches **end-of-life ~2030**.
- **CEPT ECC Decision (20)02** allocated the railway mobile radio (RMR) bands (paired 874.4–880.0 / 919.4–925.0 MHz; unpaired 1900–1910 MHz).

Sources: https://en.wikipedia.org/wiki/FRMCS ; CEPT decision: https://docdb.cept.org/download/4039

> **Expert tell to use:** Have the Meridian run **ATO GoA4 over an extended-Level-2/Level-3 moving-block ETCS backbone on FRMCS (5G)**. That is exactly where the real industry is heading, and it is *defensible in 2025*.

### Maglev-specific reality (because the Meridian is a maglev)
- Maglev vehicles are **levitated by magnets, not rolled on wheels**; propulsion is by a **linear motor** (long-stator in the guideway for high-speed EMS types like Transrapid/SCMaglev). There is **no wheel/rail adhesion** — braking, traction and guidance are all electromagnetic and trackside-driven.
- Speed record: **603 km/h** (JR-Maglev L0, 2015); operational record **431 km/h** (Shanghai Transrapid). The book's **600 km/h** is therefore at the *absolute proven ceiling*, not fantasy.
- Because propulsion/braking live in the guideway and the vehicle has no conventional adhesion-limited braking, **the "control" of a maglev is more centralised in the wayside/guideway systems than on a conventional train** — which *strengthens* the fiction's premise that a god-like wayside/Conductor governs the vehicle. (Consequence to exploit: a runaway maglev cannot simply "brake" like a steel-wheel train; it is governed by the guideway's electromagnetic state.)

Source: https://en.wikipedia.org/wiki/Maglev

> **Caveat / nuance [flag for the writer].** Real high-speed maglevs (Transrapid, SCMaglev) are on **dedicated, segregated guideways** with their own proprietary train-control schemes — they do **not** run ETCS as-is. So in the fiction the "Conductor" is a maglev-native control system *architected in the spirit of* ETCS-L3 + ATO-GoA4, not literally ETCS. That is a reasonable and common authorial licence; just **don't claim the Meridian runs stock ETCS** unless you want a maglev engineer to object. Frame it as "ETCS-grade moving-block + GoA4 ATO, adapted to a long-stator maglev guideway."

---

## Safety Architecture (SIL / fail-safe / redundancy / segregation)

### Safety Integrity Levels (SIL)
SIL is defined in **IEC 61508** (functional safety of electrical/electronic/programmable safety-related systems). Four levels, SIL4 most dependable. Railway-specific application standards (cited in the SIL article):
- **EN 50128** — software for railway control and protection.
- **EN 50129** — safety-related electronic systems for **signalling** (the one a signal engineer will quote for the SIL-4 interlocking/ATP).
- **EN 50657** — software on board rolling stock.

Quantitative targets (IEC 61508, continuous/high-demand via PFH = probability of dangerous failure per hour; RRF = risk-reduction factor):

| SIL | PFH (/hr) | RRF |
|---|---|---|
| 1 | 10⁻⁵–10⁻⁶ | 10⁵–10⁶ |
| 2 | 10⁻⁶–10⁻⁷ | 10⁶–10⁷ |
| 3 | 10⁻⁷–10⁻⁸ | 10⁷–10⁸ |
| **4** | **10⁻⁸–10⁻⁹** | **10⁸–10⁹** |

So a **SIL-4** signalling function tolerates a dangerous failure only on the order of **once per 10,000–100,000 years** per channel — the bar the train-control/routing layer sits at. (Low-demand PFD table also exists; for a continuously-operating control system the **PFH** row is the relevant one.)

Source: https://en.wikipedia.org/wiki/Safety_integrity_level

> **Expert tells:** Signalling/ATP/movement-authority logic is **SIL-4**. The *ATO* (driving) and *ATS* (supervision) layers are typically **lower SIL (often SIL-2 or non-safety)** — see CBTC section — **because they sit downstream of ATP, which always retains the final, vital veto.** This separation is the single most important architectural fact for the heist.

### Fail-safe principle
Fail-safe = a design where, on failure, the system degrades to its safest state. Railway instances an expert will recognise:
- **Track circuits** are designed so a broken rail / lost power / cut wire makes the block show **occupied/restrictive** (fail to danger = the safe direction). A signal that loses power drops to **stop**.
- **Air brakes** (rail): brakes are held *off* by air pressure; loss of pressure **applies** the brakes. (Maglev analogues: fail-safe = de-energise → guideway no longer propels/suspends → controlled set-down.)
- **Dead man's switch** (driver vigilance).
- **Conflicting-signal detection** drops an intersection to **all-flashing / all-red**.
- A confusing/contradictory/unfamiliar signal aspect **must be treated as "danger"** by the driver (procedural fail-safe).

Source: https://en.wikipedia.org/wiki/Fail-safe

### Redundancy: 2-of-3 voting (TMR)
To beat single-point-of-failure, safety computers use **triple modular redundancy (TMR / 2oo3 voting)**: three independent channels compute the same function; a **majority voter** takes the result agreed by ≥2 of 3. One channel can fail and the output stays correct; the failed channel is *masked and reported*. Reliability: RTMR = Rv·(3Rm² − 2Rm³). To eliminate even the voter as a single point, the voters themselves can be triplicated (FTMR). TMR is standard in avionics (INS, pitot) and in **railway vital/safety computers**.

Source: https://en.wikipedia.org/wiki/Triple_modular_redundancy

> **[UNVERIFIED — standard practice, primary not opened this session]** That **2oo3 voting is used inside railway vital interlockings / EVCs / RBCs** is industry-standard and widely published (e.g. MEN Mikro Elektronik "Ready for SIL 4" whitepaper referenced in the Fail-safe article). Treat as reliable, but if you quote a specific vendor's architecture, open their SIL-4 safety case rather than citing this brief.

### Segregation of safety from non-safety (CBTC architecture — the cleanest description)
From the **CBTC** article (IEEE 1474 standard), the logical layers are explicitly split:
- **Onboard ATP (safety-critical / vital)** — continuously supervises speed against the safe braking curve; **applies brake if violated**; exchanges position + receives the **Limit of Movement Authority (LMA)**.
- **Onboard ATO (non-safety)** — drives traction/braking *within* the ATP-permitted envelope; can run fully automatically.
- **Wayside ATP (vital)** — manages comms with trains and **calculates the LMA every train must respect** ("this task is therefore critical for the operation safety").
- **Wayside ATO (non-safety)** — destinations, dwell times, and explicitly **"auxiliary and non-safety related tasks, for instance alarm/event communication and management, or handling skip/hold station commands."** ← This is a *direct, citable* real-world hook for "the ATO layer listens to events and can skip/hold stations."
- **ATS (supervision)** — operator/system interface, traffic regulation.
- **Interlocking (vital)** — controls switches/signals; can be a fallback.

Crucially: **"ATO is the 'non-safety' part of train operation."** The **safety envelope is always owned by ATP**, and ATO may only operate *inside* the ATP-permitted LMA. On **loss of communication**, CBTC enters a **fail-safe / degraded state** (reduce speed, stop, or manual fallback) until comms are restored.

Sources: https://en.wikipedia.org/wiki/Communications-based_train_control ; https://en.wikipedia.org/wiki/Automatic_train_operation (for "ATO is the non-safety part")

> **This is the architecture the whole heist must respect.** "Routing" / "turning the train" lives at the **vital ATP + interlocking + RBC** layer (SIL-4, 2oo3, fail-safe). The "speech/glyph interface layer" and "medical bus" are **non-safety zones**. The heist's entire trick is bridging from a non-safety zone into a safety function *through an authorised pathway* rather than by defeating the safety function outright.

---

## Why Legacy Overrides Survive (grounding the 15-year-old credential)

This is the section that makes the *oldest* plot device defensible. Real reasons certified safety systems carry decades-old code/credentials:

1. **Recertification cost is enormous and recurring.** Upgrading even a *baseline* of a certified system forces **re-certification of every vehicle**. The ETCS article gives a hard number: moving a fleet to **Baseline 3 costs at least €100k per vehicle** for recertification — *before* any hardware. National fleets run to **billions** (Switzerland's SBB: ~6.1 bn CHF just for the Level-2 changeover; full transition estimated to ~2060). No operator volunteers to re-touch a working SIL-4 artefact.
   Source: https://en.wikipedia.org/wiki/European_Train_Control_System

2. **"If it works, don't touch it" / fear of bricking a SIL-4 system.** Certified safety code is frozen precisely *because* changing it is expensive and risky. A dormant override that has never misbehaved is, in cost/risk terms, cheaper to leave than to remove. Removing it also requires re-proving the safety case for everything around it.

3. **Legacy code is endemic in critical systems.** Safety-critical and OT systems routinely run code and credentials that are 15–30+ years old; the security debt is well documented across ICS/SCADA (see next section, Stuxnet).

4. **Removing it would mean admitting a design flaw.** This is the book's own line and it is *psychologically and procedurally realistic*: deleting the override produces a paper trail ("one credential could turn the train"). In a certified safety culture, *documenting a latent hazard you then chose not to engineer out* is a liability and an audit finding. Easier to let it persist as an "authorised emergency function" nobody talks about — which is exactly how the book frames it.

5. **Overrides/maintenance modes are legitimately sanctioned** (see next section), so a legacy override *blends in* with normal authorised functions rather than standing out as a backdoor.

> **Verdict.** A 15-year-old, sanctioned "emergency-reroute credential" buried in the interface layer is **plausible**, *provided* it is framed as an **authorised maintenance/emergency function that was certified once and never re-certified-out** — not as a secret hacker backdoor. The realism lives in the **recertification economics**, not in the code.

---

## Emergency-Reroute Realism

Do real systems have sanctioned "reroute / divert / override" functions? **Yes, in several forms.** Each is a legitimate, certified feature the fiction can model:

1. **Movement Authority as the prime control object (PTC/ETCS).** In **Positive Train Control** (US), "PTC restricts the train movement to an **explicit allowance; movement is halted upon invalidation**." A train "receives a *movement authority* containing information about its location and where it is allowed to safely travel." PTC's declared functions include **temporary speed restriction enforcement**, **rail-worker wayside safety**, and **wayside device interface (switch position) control**. A *new/changed movement authority* is precisely a "reroute."
   Source: https://en.wikipedia.org/wiki/Positive_train_control

2. **Engineering / maintenance / degraded modes.** CBTC explicitly provides **graceful degradation**: a **secondary signalling method** can keep a reduced service running when the primary is unavailable (e.g. NYC Canarsie kept an automatic-block fallback). Maintenance/possession working, **temporary speed restrictions**, and **shunting/emergency modes** are all standard. These are the real "authorised to do something abnormal" channels.
   Source: https://en.wikipedia.org/wiki/Communications-based_train_control

3. **Skip/hold-station commands** exist as a *real ATO function* (cited above from the CBTC article). A "hold at / divert to" command is not science fiction; it is a feature.

4. **Centralised vital computers can issue movement authorities directly** (PTC architecture): "a set of vital computer systems at a central location … can keep track of trains and issue movement authorities to them directly via a wireless data network." This is *literally* the architectural slot a "Conductor" occupies.
   Source: https://en.wikipedia.org/wiki/Positive_train_control

> **Most realistic version of the book's override.** Don't call it a "backdoor that turns the train." Call it a **sanctioned emergency-reroute / quarantine-spur movement-authority credential** — the kind of thing written for "a faulty spur must be quarantined / an engineering possession must be set up / a train must be diverted to a siding." It survived 15 years because it is *indistinguishable from legitimate maintenance/emergency function*, and because purging it meant recertification (above). **Crucially, it should only ever *request/authorise* a reroute that ATP still validates** (see Stress Test) — it must not *bypass* ATP.

---

## The Medical-Bus → Routing Seam (THE KEY FIX)

**Status of the book's current claim.** "A life-support/medical subsystem can REACH the routing/interface layer because medical emergencies are authorised to reroute." As stated, this is the **softest, most objectionable** claim to any SIL-trained engineer, because a *properly segmented* system does **not** let a non-safety (medical) zone issue commands to a SIL-4 safety/routing zone. This is exactly the kind of cross-zone coupling **IEC 62443 zones-and-conduits** is designed to prevent (see below).

### The candidate framings, evaluated

| Option | Realism | Notes |
|---|---|---|
| (a) Shared situational-awareness / event backplane | **High** | Real: SCADA/ATS aggregate alarms/events across zones *read-only*, with tightly controlled *upward* triggers. |
| (b) A genuine built-in ATO "medical auto-divert" function (ambulance-to-nearest-station) | **Highest** | Real & foreseeable for a GoA4/unattended train with no driver to make a judgement call. |
| (c) A maintenance/diagnostic bus that bridges segments | Medium | Real, but diagonstic buses are usually read-only one-way; using one for control is the weak part. |
| (d) A human-factors override path | Medium | Real (attendant/remote operator), but the book wants an *autonomous* path, not a human one. |

### THE SINGLE BEST FIX (recommended)
**Reframe the seam as an *event*, not a *command*.** Combine (a) + (b):

1. **The medical bus does not "command routing."** The hacker's neural implant **speaks the medical-bus protocol** (an HL7/FHIR-style or building-automation-style health-device bus) and **injects a falsified "patient in distress" *event*** into the medical/life-support zone.
2. That event propagates **read-only, upward** through a sanctioned **conduit** onto a shared **situational-awareness/event backplane** (the ATS/operations zone) — exactly as alarm/event aggregation works in real SCADA. (An *event* crossing a zone boundary is normal and safe; a *control command* crossing it is not.)
3. Because a GoA4 train has **no driver** to decide, the system **must itself** be able to respond to a declared medical emergency — so a **genuine, certified, SIL-rated ATO "emergency-medical-divert" function** exists: auto-divert to the **nearest equipped station/depot**. This is a *real, foreseeable* ATO capability for an unattended train, and it is *authorised* to consume the medical-distress event.
4. **The 12-second "privileged override window"** = the **emergency-preemption interval**: the period during which a highest-priority medical alarm pre-empts other logic **before corroboration/timeout cancels it.** That is a realistic alarm-timer mechanic, not magic.
5. **The 7-digit legacy override** then does the *one* thing the ATO function can't do alone: it lets the human **select the *destination*** (the quarantine spur) instead of accepting the ATO's auto-computed nearest station. So the override is a **destination-authorisation credential**, not a "steer the train" key.

**Net result.** "Turning the train" is achieved by **abusing three individually-legitimate, individually-authorised features in series** — a falsified medical event + a certified medical-auto-divert ATO function + a legacy destination-authorisation credential. That is a **Stuxnet-style subversion of legitimate functionality**, not a hole punched through the control plane. ATP/SIL-4 integrity is *never defeated*: the diverted movement authority is still validated against the safe braking curve and interlocking.

### Why this threads the SIL needle (cite this to an OT reviewer)
- **IEC 62443** (ANSI/ISA-62443) defines OT security via **zones** (assets with a common security level) and **conduits** (controlled communication paths between zones), with **Security Levels SL0–SL4** (SL4 = nation-state-grade) and an explicit **least-privilege** principle. The fix is *exactly* a sanctioned conduit carrying an *event* from a lower-trust medical zone to a higher-trust operations zone, consumed by an authorised function. That is textbook-compliant *structure*; the *vulnerability* is that the event source is spoofable and the consuming function trusts it.
  Source: https://en.wikipedia.org/wiki/IEC_62443
- **[UNVERIFIED — standard exists, primary not opened this session]** The **railway-sector** cybersecurity standard is **CENELEC TS 50701 (2019) → adopted as EN 50701 (2021)**, which is the rail application profile of IEC 62443. Open the primary before naming it on the page.

---

## Event-Triggered Directives Realism ("a will executing without its author")

The book's **dormant, event-triggered, self-executing directives** ("compiled 7 years ago, wake on conditions") should **not** be framed as "magic AI." Frame them as a **conditional autonomous code layer** with a *trigger grammar* — which has many real analogs:

- **Trigger-Action Programming (TAP) / IFTTT-style rules in OT.** Condition→action rules are mundane in automation.
- **Scheduled/conditional maintenance routines that run unattended.** The CBTC article explicitly assigns the wayside ATO layer **"auxiliary and non-safety related tasks, alarm/event communication and management, or handling skip/hold station commands."** Those are autonomous, event-driven behaviours already resident in the non-safety layer.
  Source: https://en.wikipedia.org/wiki/Communications-based_train_control
- **Smart-contract / daemon semantics.** "A will executing without its author" maps precisely onto a **deterministic, compiled, state-machine daemon**: dormant until a boolean over its trigger predicates becomes true, then it runs its pre-compiled action set. It does not "think"; it *fires*.
- **SCADA alarm/event logic and PTC movement-authority logic** are themselves event-condition-action machines.

### How to frame the directives realistically
- Give them a **trigger grammar**: named predicates such as *"interface language spoken aboard"*, *"manifest under threat"*, *"routing queried by unauthorised hand"*. Each predicate is a **verifiable signal** from a sensor/bus, not a judgement.
- They are **compiled once and certified** (7 years ago), then frozen — so they survive in the same "don't-touch-certified-code" limbo as the legacy override (see *Why Legacy Overrides Survive*). This is *why* they persist and *why* nobody audited them: editing them = recertification.
- They are **dormant**: they consume negligible resources and produce no output until a predicate fires — i.e., a real daemon/cron/edge-rule engine, not an always-on "AI."
- Their **action set should stay within the non-safety (ATO/ATS) + event layer**; they orchestrate the *chain* of legitimate features above, they do **not** themselves bypass ATP.

> **One sentence for the book's bible:** the directives are a **certified, frozen, event-condition-action state machine** — "a compiled will that waits for its conditions the way a relay waits for current."

---

## Red-Team Stress Test (why one credential normally *can't* turn a train, and how the fiction survives)

**The objection an expert raises first:** *"In a SIL-4, 2oo3, fail-safe system, no single credential can turn a train. Routing lives behind ATP/movement-authority integrity; one key can't punch through that."* That objection is **correct as stated**, and the fiction must not pretend otherwise. The book's exception works **only** because it never claims the credential *defeats* the safety layer — it claims the crew **chains legitimate features** so the safety layer *cooperates*.

The chain, link by link, with the realistic guarantee each link relies on:

1. **ATP/movement-authority integrity is never bypassed.** The final movement authority is still validated against the safe braking curve and the interlocking. The train is "turned," but it is turned **onto a route that is, mechanically, safe to run.** (That is *why* a quarantine spur exists — the destination must be a genuinely reachable, interlocked route, or the whole thing fails safe.)
2. **2oo3 / TMR is not broken — it is *outvoted by truth*.** All three channels agree because the inputs they are given are *consistent and valid-looking*. This is the Stuxnet lesson (next): you don't defeat the voter, you feed all channels the same lie.
3. **Fail-safe is preserved, not defeated.** Nothing holds a relay energised against a fault; if anything upstream breaks, the train still fails to its safe state. The exploit depends on the inputs being *plausible*, not on suppressing fail-safe.
4. **The credential is necessary but not sufficient.** Alone it requests a destination; it needs (a) the medical event to arm the divert path and (b) the directives to supply the autonomous execution. Any single leg is benign; the *combination* is the weapon. (This is a classic privilege-escalation-by-composition / confused-deputy pattern.)
5. **The spoof is at the *event source*, not the control plane.** The medical bus is the lowest-trust, least-hardened sensor zone — exactly where a real attacker would aim (sensors are the soft underbelly of OT; Stuxnet attacked sensor/signals, not the PLC logic directly).
6. **Time-boxing is realistic.** The 12-second window is an alarm-preemption timer, not an arbitrary "god mode." The crew must complete the chain inside it or the event times out and the divert self-cancels — a clean, fail-safe ticking clock for the set-piece.

**The precedent that makes this believable — Stuxnet (2010).** Stuxnet is the canonical case of *subverting legitimate functionality across an air gap*:
- It crossed an **air gap via infected removable media (USB)** — proving air gaps are not absolute.
- It installed **the first documented PLC rootkit**, and performed a **man-in-the-middle attack that faked industrial sensor/process readings** so the system *"does not shut down due to detected abnormal behavior"* while it altered outputs.
- It **subverted Siemens Step7/WinCC** (including a **hard-coded database password**) to reprogram PLCs unnoticed, returning a "loop of normal operation values" to monitoring.
- It was *promiscuous in spread but surgical in payload*: it became inert unless specific target configuration criteria were met — exactly the "**fire only on condition**" pattern the book's directives use.
- It catalysed **DHS ICS-CERT / control-system-security** as a discipline.

Sources: https://en.wikipedia.org/wiki/Stuxnet ; https://en.wikipedia.org/wiki/Air_gap_(networking)

> **Red-team verdict.** The plot is **survivable** for an expert reader *if and only if*: (i) ATP/SIL-4 is never said to be "broken" — only *fed consistent, valid-looking inputs*; (ii) the medical bus supplies an **event**, never a **command**; (iii) every leg is a **legitimate feature** being abused; (iv) the destination is a real, interlocked, safe-to-run route. Violate any of these and a signal engineer will close the book.

---

## Expert Tells (details a signal engineer / OT pro will clock as authentic)

Drop these as texture; an expert will recognise each.

1. **"ATO GoA4 over an extended-Level-2/Level-3 moving-block backbone on FRMCS (5G)."** — exactly where real mainline automation is going; Hamburg 2021 = first driverless on shared mainline track.
2. **SIL-4 (PFH 10⁻⁸–10⁻⁹ /hr; RRF 10⁸–10⁹) for the movement-authority/routing logic; ATO/ATS at lower SIL because ATP owns the final veto.** — the ATP-vs-ATO SIL split is the architecture's spine.
3. **2oo3 / triple modular redundancy** with a majority voter in the vital computers; voters triplicated to kill the single point of failure.
4. **Movement Authority / End-of-Authority / Limit of Movement Authority** as the actual control objects (ETCS SUBSET-026 / IEEE 1474 CBTC vocabulary).
5. **Radio Block Centre (RBC)** issuing authorities over **GSM-R/FRMCS**; **Eurobalises** for position referencing; **European Vital Computer (EVC)** + **Juridical Recording Unit** (the on-board black box) on the vehicle.
6. **Fail-safe primitives:** loss-of-power → brakes applied / signal drops to stop; track circuit fails to occupied; contradictory aspect treated as danger; dead-man's vigilance.
7. **FRMCS replaces GSM-R (~2030 EOL); CEPT ECC Decision (20)02 RMR bands; UIC-led 5G NR.**
8. **IEC 62443 zones & conduits, Security Levels SL0–SL4, least privilege, defence-in-depth** — and (verify) **EN/TS 50701** as the rail profile.
9. **Recertification economics:** Baseline-3 recert ≈ €100k/vehicle; national changeovers in the **billions** and **decades** — the real reason certified code is frozen.
10. **Maglev physics:** linear-motor (long-stator) propulsion/braking in the guideway, EMS/EDS levitation, no wheel adhesion; **600 km/h is at the proven L0/Transrapid ceiling (record 603 km/h, 2015)** — so the Conductor's authority is *wayside-centralised*, strengthening the premise.
11. **Stuxnet playbook as the in-universe model:** USB-over-air-gap + PLC rootkit + **sensor-signal MITM** (feed the safety loop "normal" values) + **payload gated on target config** + stolen/hard-coded credentials.
12. **Event-vs-command discipline:** alarms/events aggregate *upward* across zone conduits (safe); control commands must never cross a SIL boundary without a certified function on the receiving end.

---

## Corrections Needed (weakest claims → most plausible reframing)

1. **WORST: "the medical bus can REACH the routing/interface layer because medical emergencies are authorised to reroute."**
   - *Problem:* Implies a non-safety zone issues commands to a SIL-4 zone — the cardinal sin in segmented OT design.
   - *Fix:* It is an **event**, not a command. The implant spoofs a "patient in distress" *event* on the medical zone; it propagates *read-only upward* through a sanctioned conduit to the ATS/event backplane; a **genuine certified ATO "medical auto-divert" function** (a real GoA4 necessity) consumes it. (See *The Medical-Bus → Routing Seam*.)

2. **"A single 7-digit credential can turn the train."**
   - *Problem:* Overstated; no single key should ever punch through ATP.
   - *Fix:* The credential is a **destination-authorisation** key, *necessary but not sufficient*. It needs the medical event (to arm the divert) + the directives (to execute). The train is "turned" by **chaining three legitimate features** (a confused-deputy / composition attack), never by defeating ATP.

3. **"The speech/glyph INTERFACE LAYER holds routing."**
   - *Problem:* A presentation/voice layer should hold no control authority.
   - *Fix:* The interface layer **holds the legacy credential** (a destination-authorisation artefact frozen there 15 yrs ago) and is the **trigger surface** for the directives (e.g., "interface language spoken aboard"). It does **not** hold routing logic; it holds a *key into a certified function* plus a *trigger grammar*. Routing stays in ATP/RBC/interlocking.

4. **(Minor) "magic AI" framing of the directives.**
   - *Fix:* Reframe as a **certified, frozen, event-condition-action state machine** (compiled once, dormant, fires on boolean predicates over real sensor signals). No cognition, no "deciding."

5. **(Minor, for authenticity) Don't claim the maglev "runs ETCS."**
   - *Fix:* Say it is an **ETCS-grade / GoA4 moving-block control scheme adapted to a long-stator maglev guideway**. Real maglevs use segregated, proprietary control; ETCS is the *spirit*, not the letter.

---

## Source list (all fetched live this session)

- ERTMS (umbrella): https://en.wikipedia.org/wiki/European_Rail_Traffic_Management_System
- ETCS (levels 0–3, baselines, RBC, EVC, TSI 2023 merge): https://en.wikipedia.org/wiki/European_Train_Control_System
- ATO / GoA0–4 / IEC 62290-1 / Hamburg 2021: https://en.wikipedia.org/wiki/Automatic_train_operation
- X2Rail-1 ATO-over-ETCS up to GoA4 (ERA): https://web.archive.org/web/20220718154845/https://www.era.europa.eu/sites/default/files/events-news/docs/ccrcc_2017_ato_era_en.pdf
- FRMCS (5G successor to GSM-R, CEPT ECC Decision (20)02): https://en.wikipedia.org/wiki/FRMCS ; https://docdb.cept.org/download/4039
- SIL / IEC 61508 / EN 50128 / EN 50129 / EN 50657 (PFH table): https://en.wikipedia.org/wiki/Safety_integrity_level
- CBTC (IEEE 1474; ATP vs ATO vs ATS; wayside-ATO event/skip-hold; degradation): https://en.wikipedia.org/wiki/Communications-based_train_control
- Fail-safe (track circuit, air brake, dead-man, 2oo3/TMR avionics): https://en.wikipedia.org/wiki/Fail-safe
- Triple modular redundancy (2oo3 voter, RTMR formula): https://en.wikipedia.org/wiki/Triple_modular_redundancy
- Stuxnet (PLC rootkit, sensor MITM, USB air-gap, hard-coded creds, ICS-CERT): https://en.wikipedia.org/wiki/Stuxnet
- Air gap (limitations, sneakernet, data diodes): https://en.wikipedia.org/wiki/Air_gap_(networking)
- IEC 62443 (zones & conduits, SL0–SL4, least privilege): https://en.wikipedia.org/wiki/IEC_62443
- Positive Train Control (movement authority, wayside switch control, vital central computers, SIL4/GNSS caveat): https://en.wikipedia.org/wiki/Positive_train_control
- Maglev (linear motor, EMS/EDS, 603 km/h record, Shanghai 431 km/h): https://en.wikipedia.org/wiki/Maglev

**Flagged for primary verification before going on the page:**
- **EN / CENELEC TS 50701 → EN 50701 (railway cybersecurity profile of IEC 62443).** [UNVERIFIED — standard exists, primary not opened this session.]
- **2oo3 voting specifically inside railway vital interlockings/EVCs/RBCs.** [Standard practice; open a vendor SIL-4 safety case before quoting specific architecture.]
- **Exact €100k/vehicle Baseline-3 recert figure and the SBB 6.1 bn CHF number** — both from the ETCS article; fine as order-of-magnitude, confirm against an SBB/BAV or ERA source if quoted precisely.
