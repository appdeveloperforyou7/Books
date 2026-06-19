# 04 · Neural Implants & Medical-Device Interop — Research Brief for JAE

**Purpose:** Make JAE's neural implant and the "medical-bus bridge" factually airtight for neurologists, biomedical engineers, and epileptologists.
**Method:** Every claim below is tied to a primary source (peer-reviewed, manufacturer, or regulator). Items not independently verified this pass are flagged `[VERIFY]` or `[DESIGN CHOICE]`. Nothing is invented beyond the flagged fiction seam.

> **Two headline fixes (details in the relevant sections):**
> 1. **Cost mechanism:** Replace "the medical-bus current flows through his implant and stops his heart" (cardiogenic/electrical conduction — the *wrong* mechanism) with a **neurogenic autonomic storm**: sustained overstimulation drives vagal/limbic overdrive → AV-nodal block/asystole (the documented VNS pathway) and/or the **SUDEP pathway** (postictal bradycardia → brainstem cardiorespiratory collapse). The lethal, countable cost survives; the mechanism becomes medically honest.
> 2. **Protocol seam:** An implant cannot natively talk to a train's wired medical bus. The most defensible seam is an **inductive (near-field) / MICS-MedRadio (402–405 MHz) handshake** against the train's onboard **IMD-interrogation gateway** (IEEE 11073, cardiac-implant nomenclature) — JAE pressing his retroauricular coil module against the port's induction surface.

---

## Real Seizure Implants (VNS / RNS / DBS)

There are three FDA-accepted neurostimulation approaches for drug-resistant epilepsy. **The one that "senses and responds in real time" is RNS.**

### 1. Vagus Nerve Stimulation (VNS) — LivaNova
- **What it stimulates:** the **left cervical vagus nerve** (in the neck, carotid sheath), *not* the brain directly. The pulse generator sits in a subcutaneous pocket, classically **infraclavicular (upper chest)**. *(NeuroPace RNS-vs-VNS comparison; LivaNova VNS Therapy System Epilepsy Physician's Manual, May 2020, cited therein.)*
- **What it senses:** Traditionally **open-loop** (no seizure sensing) — it cycles on/off on a fixed schedule. Newer generations add **cardiac-based seizure detection**: the SenTiva "AutoStim" feature detects ictal tachycardia and triggers on-demand stimulation. So "senses and responds" is *partially* true of modern VNS, but via heart-rate, not brain signals. *(Manufacturer feature — `[VERIFY]` against current LivaNova labeling.)*
- **Typical pulse parameters (verified):** **output current ~0.8–3.0 mA** (super-responders as low as 0.84 mA; refractory cases pushed to ~3.0 mA mean; device ceiling ~3.5 mA). **Duty cycle** is the key tuning knob — Normal (OFF ≥1.1 min), Rapid (OFF <1.1 min), **Ultra-Rapid (ON 7 s / OFF ~12 s)**. Higher output + higher duty cycle → better seizure control **but shorter battery life**. **Pulse width** (130–1000 µs, typical 250–500) and **frequency** (1–30 Hz, typical 20–30) — these specific sub-ranges are standard but `[VERIFY]` against the manual. *(Tamura 2025, PMID 41128704 — "Low-Charge Density" super-responders, 0.84 vs 1.91 mA; Haddad 2023, PMID 37611408 — URDC, 3.025 mA tolerated, battery change sooner; Bansal 2026, PMID 41217293.)*
- **Known stimulation side effects (real, cited):** hoarseness/voice change, cough, sore throat, shortness of breath — *exactly* the contrast NeuroPace uses to market RNS. *(NeuroPace; Spregnero et al., Cochrane, 2017.)*

### 2. Responsive Neurostimulation (RNS) — NeuroPace RNS® System  ← **closest match to "an implant that senses and responds in real time"**
- **What it senses:** continuous **intracranial EEG (iEEG)** via depth and/or strip leads placed *at the seizure focus*, anywhere in the brain (flexible lead placement).
- **What it stimulates:** it is **closed-loop** — "recognizes a person's unique seizure patterns, and automatically responds… before they start," delivering brief pulses to disrupt the activity. Compared with VNS/DBS it is "the only FDA-approved epilepsy device that recognizes and responds to what's happening in the brain in real time." *(NeuroPace — manufacturer; Razavi 2020, Epilepsia; Nair 2020, Neurology.)*
- **Total stimulation delivered:** on average **~3 minutes per day** total. *(NeuroPace, citing Nair 2020.)*
- **Stimulation side effects:** none of the VNS chronic effects — **"imperceptible stimulation with no chronic side effects."** *(NeuroPace.)*
- **Battery life:** **RNS-320 neurostimulator ≈ 10.8 years** (FDA labeling, medium settings). *(NeuroPace.)*
- **Packaging (anatomy, important for JAE):** the neurostimulator is **housed in a recessed craniotomy in the skull** (low-profile, skull-mounted) — *not* a chest generator and *not* natively "behind the ear." See §Overuse Symptoms for a `[DESIGN CHOICE]` that keeps "heat behind the ear" honest.
- **Pulse parameters (RNS-specific):** commonly cited maxima — output current up to ~12 mA, pulse width 40–1000 µs, frequency 1–333 Hz, delivered in short responsive bursts. **`[VERIFY]` against the current NeuroPace Physician Product Manual** — I did not pull these exact numbers from the manual this pass. For a verified, in-range comparator: a 2026 cortical-stimulation systematic review reports **frequency 2–130 Hz, pulse width 90–450 µs, amplitude up to 7 V or 4 mA** for chronic cortical stimulation (Turk 2026, PMID 41964625). RNS programming is an **iterative, patient-specific** process tuning detection biomarkers to stimulation parameters (McCarthy & Burdette 2026, PMID 42302539).
- **Mortality angle (use this):** long-term RNS patients show a **significantly lower SUDEP rate** — a credible reason for JAE to *have* the device (it was put in to keep him alive), and a thread that ties directly to the cardiac-cost fix in the next section. *(NeuroPace, citing Nair 2020, Neurology.)*

### 3. Deep Brain Stimulation (DBS) — anterior nucleus of thalamus (ANT), Medtronic
- **What it stimulates:** the **anterior thalamic nucleus**, via leads stereotactically placed in the thalamus; an extension cable tunnels subcutaneously to a pulse generator (chest or abdomen). **Open-loop** (scheduled/cyclic), fixed anatomical target.
- **Status:** FDA-approved for drug-resistant focal epilepsy. *(de Oliveira & Cukiert 2025, PMID 40991616.)*
- **Typical parameters (`[VERIFY]` against Medtronic labeling):** ~5 V, ~145 Hz, ~90 µs pulse width, cyclic (e.g., 1 min ON / 5 min OFF). Rechargeable battery options exist.

### Quick comparison table (for internal reference)

| | VNS | **RNS** | DBS (ANT) |
|---|---|---|---|
| Target | Left vagus nerve (neck) | **Seizure focus (brain)** | Anterior thalamus (brain) |
| Sensing | Open-loop (+ ictal-tachycardia AutoStim) | **Closed-loop iEEG** | Open-loop |
| "Senses & responds in real time" | Partial (heart-rate) | **Yes (brain)** | No |
| Generator site | Upper chest | Skull (cranial) | Chest/abdomen |
| Chronic stim side effects | Hoarseness, cough, dyspnea | ~None | Varies |
| Cardiac involvement risk | **Yes (vagal → AV block/asystole)** | Indirect (autonomic/SUDEP) | Indirect |

---

## Realistic Physiological Cost (the key fix)

**The book's current mechanism:** *"the medical bus carried current… twelve seconds of his own nervous system conducting a current built to restart a stopped heart… Hold it too long and… it would stop it."*

**The problem:** This is a **cardiogenic / galvanic-current** mechanism — it implies defibrillator-class electrical energy literally flows *through* Jae's body via the implant and arrests his heart by direct electrical effect. That is not how implant telemetry works (inductive/MedRadio links transfer *data and tiny RF power*, not a galvanic current path — see §Medical-Device Comms Protocols), and it is not how cardiac arrest in neurostimulation patients actually happens. The medically honest version is **neurogenic, not cardiogenic**.

### The honest mechanism (pick / blend these — all are sourced)

**(A) Vagal overdrive → AV-nodal block / asystole (the single best-documented lethal cost).**
Left VNS can cause **complete heart block and transient ventricular asystole** that is *temporally correlated with seizure activity and resultant VNS activation*, and that **resolves when the device is deactivated**. *(Warnock et al. 2024, Cureus, PMID 38435952 — "Complete Heart Block and Ventricular Asystole Caused by Vagus Nerve Stimulation Therapy"; PMCID PMC10906750.)* The mechanism is **excess parasympathetic (vagal) tone dominating cardiac rhythm** — the same reason asystole occurs at the start of electrical stimulus during ECT: it is "most likely caused by vagal nerve stimulation, affecting autonomic cardiac tone." *(Hartnett et al. 2023, J ECT, PMID 35700970.)* Reflex bradycardia progressing to cardiac arrest from cranial-nerve stimulation is well established (e.g., the trigeminocardiac reflex during neurointerventional procedures). *(Sun et al. 2021, Am J Case Rep, PMID 34077403; PMCID PMC8183304.)*
→ **This makes the book's "his heart finds the wrong rhythm / briefly stops" medically defensible — but the cause is the implant overdriving his vagus/autonomic system, not a current passing through his chest.**

**(B) The SUDEP pathway — neurogenic cardiorespiratory collapse (use this for the 40-second, near-fatal escalation).**
In monitored fatal cases, SUDEP follows a **consistent pattern of postictal bradycardia with rapid collapse of brainstem cardiorespiratory pacemaking within minutes after a generalized tonic-clonic seizure**. Critically: **"SUDEP is a neurogenic, not cardiogenic, event and brainstem involvement is both necessary and sufficient."** Spreading depolarization silences critical brainstem networks. *(Noebels JL, "Genetic and Cellular Mechanisms Underlying SUDEP Risk," in Jasper's Basic Mechanisms of the Epilepsies, 5th ed., 2024, PMID 39637214.)*
→ **The 40-second hold pushing Jae into near-fatal collapse is best framed as driving his brain toward a SUDEP-type neurogenic arrest** — sustained overstimulation tips him into a self-sustaining seizure/autonomic storm whose endgame is brainstem shutdown. This is *exactly* the death his implant was put in to prevent, which makes the cost thematically vicious.

**(C) Seizure induction / status epilepticus (the "kindling" risk of electrode overstimulation).**
Overdriving an epileptogenic focus can **kindle / precipitate seizures**, potentially escalating to **status epilepticus** — itself a cause of autonomic instability, bradycardia, and respiratory compromise. This is the bridge between "too much stimulation" and (A)/(B). *(General epileptology principle — `[VERIFY]` for a specific citation if a reviewer pushes; the de Oliveira & Cukiert 2025 review, PMID 40991616, covers neuromodulation limits.)*

### Recommended rewrite (preserves drama, fixes mechanism)

> The bridge doesn't electrocute him — it makes **his own implant turn on him.** To spoof the handshake, the implant must clamp and echo a sustained, high-duty-cycle authentication burst, dumping stimulation into his vagus/limbic system far past therapeutic charge density. The longer he holds the port, the deeper the parasympathetic overdrive: first the heat, then the tremor, then his heart slowing into AV block, then the wrong rhythm — the same neurogenic collapse the thing was bolted into his skull to prevent. Hold it long enough and it isn't a seizure that kills him. It's the silence after.

- **Keep:** the countable, escalating, lethal cost; the "wrong rhythm / briefly stops" beat; the Osaka prior-incident foreshadowing.
- **Change:** "current flowing through him" → "the implant overdriving his autonomic/vagal system into AV block / a SUDEP-type collapse." The lethality is real and well-sourced; it just arrives via his *nervous system*, not via a galvanic shock.
- **Note on the defibrillator line:** "enough to fire a defibrillator" is fine as **atmosphere** for what the *train's* medical bus can do, but Jae is never on the receiving end of that energy — he's on the receiving end of his *own implant's* overstimulation. Don't let the reader think the defib joules pass through him.

---

## Overuse Symptoms ("heat behind his ear" / tremor)

### Real implant-overuse / malfunction phenomena (sourced)
- **Electrode-tissue safety is governed by charge density (µC/cm²/phase), not raw current.** Charge density drives tissue injury: in a controlled STN-HFS study, Pt/Ir electrodes at **3 µC/cm²/phase over 3 days produced no relevant damage**, while higher charge densities (up to 26 µC/cm²/phase) and certain electrode materials did. *(Harnack et al. 2004, J Neurosci Methods, PMID 15325129.)* "Low-charge density" is also recognized clinically as the favorable VNS operating regime. *(Tamura 2025, PMID 41128704.)* → Sustained overdrive = **charge density far exceeding safe limits** = local tissue/electrode stress.
- **Impedance rise / electrode heating** is a real, monitored failure signature in implantable stimulators; overdriving a lead raises current density and local heating at the electrode–tissue interface, with potential for thermal/micro-injury and rising impedance (which in turn demands more voltage for the same current — a vicious spiral).
- **Battery drain** under high duty cycle / output is real and clinically relevant: high-output URDC patients "required a battery change sooner." *(Haddad 2023, PMID 37611408.)* → An overdrive bridge would crater Jae's battery and force erratic, sputtering stimulation as voltage sags.
- **Tremor/myoclonus** is consistent with (a) spread of current to adjacent motor cortex / cranial-nerve territories, and (b) seizure kindling toward status epilepticus (see §Cost).
- **VNS-specific side-effect palette** he could be hiding: hoarseness/voice change, cough, dyspnea — credible "tells" a crewmate might notice. *(NeuroPace.)*

### Is "heat behind the ear" anatomically sensible? — Yes, **with one `[DESIGN CHOICE]`**
- For a **pure VNS**, "behind the ear" is *wrong*: the generator is infraclavicular (upper chest) and the lead is on the cervical vagus (neck). Heat would be felt at the **chest pocket or along the neck**, not behind the ear.
- The **retroauricular (behind-the-ear) subcutaneous pocket is the classic, iconically-recognizable implant site** — it's where cochlear-implant receiver/stimulators sit (mastoid region), and it is a standard thin-skin location for an **induction-coupling/telemetry coil** that must link to an external wand.
- **Recommended `[DESIGN CHOICE]` (ties everything together):** Frame Jae's device as an **RNS-class closed-loop cranial implant** *whose battery + inductive telemetry coil are seated in a retroauricular subcutaneous pocket behind his ear*. This is defensible (thin skin = good coil coupling; retroauricular pocket is established surgical anatomy) and makes every detail consistent: "heat behind the ear" = the coil/battery module overheating under overdrive; **the same module is what he presses against the port** to inductively couple (see §The Seam). It also keeps the "senses and responds in real time" RNS DNA.

→ So: **keep "heat behind his ear" — it's honest** if the battery/telemetry coil lives there. Just don't call the device a VNS (which would put the hardware in his chest).

---

## Medical-Device Comms Protocols

### IEEE 11073 (the medical-device interoperability family)
- **CEN ISO/IEEE 11073** is the joint ISO/IEEE/CEN standard family for **communication between medical devices and external computer systems** — automatic, plug-and-play exchange of vital-signs and device-operational data. *(Wikipedia "ISO/IEEE 11073" → IEEE/ISO/CEN.)*
- It spans **point-of-care devices** (ventilators, infusion pumps, ECG) and **personal health devices** (glucose monitors, pulse oximeters, BP cuffs, scales). It uses an **Agent/Manager model**: the device (agent) holds the data; the host (manager) mirrors it and can trigger/control it.
- **Relevant part for the seam:** the nomenclature explicitly includes **"Implantable device, cardiac" (11073-10103)** — i.e., the standard family *already contemplates interrogating implanted cardiac devices*. *(Wikipedia "ISO/IEEE 11073", nomenclature list.)* Android's `BluetoothHealth` historically implemented 11073, and ZigBee carries a Health Care Profile built on it — i.e., 11073 is routinely carried over **BLE / ZigBee / wired** transports.
- IEEE 11073 also defines an **SDC (Service-oriented Device Connectivity)** profile for real-time, networked medical devices (OR/ICU-grade).

### Implant telemetry bands (MICS / MedRadio) — the physical layer implants actually use
- **MICS (Medical Implant Communication Service):** created by an FCC rule in response to **Medtronic's 1999 petition**, allocating the **402–405 MHz** band — **10 channels of 300 kHz each**, low power (**EIRP = 25 µW**), giving roughly a **~2-meter** range, specifically to let implants talk to an external programmer *without* requiring skin contact. *(FCC; Wikipedia "Medical Device Radiocommunications Service".)*
- **MedRadio (Medical Device Radiocommunications Service):** the FCC's 2009 expansion of MICS — **401–406 MHz** — plus later additions at **413–419, 426–432, 438–444, 451–457 MHz**, and a separate **MBAN** allocation at **2360–2400 MHz** for body-area networks. Devices covered explicitly include **cardiac pacemakers, defibrillators, neuromuscular stimulators, and drug-delivery systems.** *(FCC; Wikipedia "Medical Device Radiocommunications Service".)*
- **Inductive (near-field) telemetry:** the older/parallel method — a coil in the implant couples to a coil in an external **"wand"/clinician programmer** at very short range (a few cm), historically **requiring the external transceiver to touch the skin**. This is how implants are **programmed and charged** in clinic. The MICS rules were *motivated precisely* to escape this skin-touch requirement. *(FCC 03-32, cited via Wikipedia.)*

### HL7 / FHIR
- HL7 and FHIR are the **application-layer healthcare data standards** (records, observations, orders) that sit *above* device-transport standards. A realistic onboard gateway would speak **IEEE 11073 at the device layer** and bridge to **HL7/FHIR** for the train's medical record/log. IEEE 11073 explicitly defines interworking to HL7/DICOM. *(Wikipedia "ISO/IEEE 11073".)*

### Bluetooth LE (BLE)
- Modern implants and consumer medical devices increasingly add **BLE** as a transport (11073 runs over BLE; there are BLE health-device profiles). BLE is **plausible but optional** for the seam; MICS/MedRadio + inductive are the *more* implant-authentic physical layers. `[VERIFY]` a specific "MEDIS"/BLE-medical profile citation if a reviewer wants it — the *defensible* core of the seam does not depend on BLE.

---

## The Implant↔Train Seam (the key fix)

**Honest premise:** A seizure implant **cannot natively speak to a train's wired medical subsystem.** Real trains do not interrogate passenger implants. So the seam is **deliberate world-building** — but it can be built *entirely from real standards and bands* so an expert reads it as "near-future, but the engineering checks out."

### The most defensible seam (recommended)

**The train is a high-end medical/rescue-configured variant with an onboard IMD-interrogation gateway.** The gateway exists to read **passenger pacemakers/ICDs/neurostimulators in a medical emergency** over the same bands those implants already use: **MICS/MedRadio (402–405 MHz)** RF plus a short-range **inductive (near-field) coil** for wand-style coupling. It presents the data on the train's medical bus using **IEEE 11073** (including the **"Implantable device, cardiac" nomenclature, 11073-10103**), bridged to **HL7/FHIR** for the onboard record.

**Jae's exploit:** his implant is an IMD-class device that speaks the same baseband protocol on the same bands. By pressing his **retroauricular telemetry coil** flat against the port's **induction surface** (a few-cm coupling window), he masquerades as a **"distressed passenger IMD"** and completes the gateway's authentication handshake — which the train treats as an **authorized medical-override / patient-in-distress** event, opening privileged access to the medical bus for the session window (see §12-sec Window).

**Why this is the best pick:**
- **Real bands** (MICS/MedRadio 402–405 MHz) + **real standard** (IEEE 11073, cardiac-implant nomenclature) + **real mechanism** (inductive coil coupling, skin-touch-to-cm range). Nothing here is magic.
- The **port has a concrete, physical identity**: an **induction-coupling / IMD-interrogation receptacle** (like a programming-wand dock) built into a medical panel. Jae must **press his head to it** — vivid, countable, and physically honest (inductive coupling needs alignment + proximity).
- It sidesteps the fatal flaw of the current draft: inductive/MedRadio links transfer **data and micro-power**, *not* a galvanic current path — which is exactly why the "defib current flows through him" line must go (see §Cost). The port exchanges *telemetry*, not joules.

### The runner-up seams (weaker; note why)
- **Shared BLE-medical profile:** plausible and modern, but BLE isn't the classic implant-authentic layer, and the "press it to a port" physicality is weaker (BLE is RF, not contact). Keep BLE as an *optional fallback transport*, not the core.
- **"AED/defib telemetry matches the implant's programmer band":** partly true (programmers use inductive + MICS), but AEDs in service don't broadcast an interrogation service an implant could exploit; the IMD-gateway framing above is cleaner.

### What is fictional vs. factual (flag for yourself)
- **Factual:** MICS/MedRadio 402–405 MHz; IEEE 11073 + cardiac-implant nomenclature; inductive wand programming; implants' Agent/Manager model.
- **Fictional `[DESIGN CHOICE]`:** that a *train* ships an IMD-interrogation gateway and that Jae's seizure implant can spoof a "distressed IMD" handshake to it. This is the deliberate, defensible near-future leap — frame it explicitly as a specialized/flagship train feature, and it will read as credible to an engineer.

---

## The 12-sec Window Realism

"12 seconds, then the system adapts and never falls for the same handshake twice" maps cleanly onto real authentication/security primitives:

- **Challenge–response with a per-session nonce.** The gateway issues a one-time challenge; Jae's implant answers with a valid response (e.g., a replayed/cloned token). The handshake is honored only **for one finite session window** — roughly an **AED-style rhythm-analysis window (~5–15 s)** — after which the nonce is **retired** (replay protection: the same handshake can never authenticate again). This is the literal meaning of "never falls for the same handshake twice."
- **IEEE 11073 session state machine.** 11073 associations move through a finite state machine (disconnected → associating → **configuring → configured** → disconnecting). Sessions are bounded; a malformed or incomplete "configuring" transition can be torn down on timeout — a natural 12-second window. *(Wikipedia "ISO/IEEE 11073", Agent/Manager + finite-state machine.)*
- **Anomaly detection.** Even with a valid token, the gateway's monitor sees no corroborating vitals (no real ECG/SpO₂ rhythm consistent with a human patient, or an **impedance/ID signature that matches no registered passenger IMD**). After the analysis window it flags the session as anomalous and quarantines that signature — so a second identical attempt is rejected.
- **Regulatory/operational timeout.** Medical-override sessions are short by design; a stale or unverified override auto-revokes (failsafe). 12 s is a believable hard cap.

→ The "never falls for the same handshake twice" is essentially **nonce-based replay protection + signature blacklisting** — accurate and easy to dramatize (Jae gets exactly one 12-second shot per port/handshake).

---

## Expert Tells (details a neurologist / biomedical engineer will clock)

1. **RNS = the only closed-loop "senses & responds" epilepsy device** (continuous iEEG → responsive pulses), vs VNS (vagus nerve, ~open-loop) and ANT-DBS (scheduled). Naming RNS/VNS/NeuroPace correctly is the first credibility gate.
2. **Charge density (µC/cm²/phase)** as the electrode-safety metric — not raw current — and the Pt/Ir-vs-stainless-steel / 3-µC safety floor. *(Harnack 2004, PMID 15325129.)*
3. **VNS output currents ~0.8–3.0 mA**, duty-cycling (Normal/Rapid/**Ultra-Rapid ON 7 s / OFF ~12 s**), and the **battery-life trade-off** of high output/duty. *(Tamura 2025; Haddad 2023.)*
4. **The vagal-cardiac link is real and can be lethal:** VNS → **complete AV block / ventricular asystole**, reversible on deactivation. *(Warnock 2024, PMID 38435952.)*
5. **SUDEP is neurogenic, not cardiogenic** — postictal bradycardia → brainstem cardiorespiratory collapse; "neurogenic, not cardiogenic… brainstem necessary and sufficient." *(Noebels 2024, PMID 39637214.)*
6. **RNS lowers SUDEP risk** and delivers only **~3 min/day** total stimulation; **~10.8-year battery** (RNS-320). *(NeuroPace.)*
7. **MICS 402–405 MHz** (Medtronic's 1999 FCC petition; 10×300 kHz; **25 µW EIRP**; ~2 m), expanded into **MedRadio (401–406 MHz)** + 413–419/426–432/438–444/451–457 MHz + **MBAN 2360–2400 MHz**.
8. **Inductive/wand telemetry requires skin-contact proximity (few cm)**; implants are **programmed/charged** by an external wand — this is the physical basis for "press the implant to the port."
9. **IEEE 11073** as the medical-device interop family (Agent/Manager; PoC + Personal Health Devices; **"Implantable device, cardiac" nomenclature 11073-10103**), bridging to **HL7/FHIR**.
10. **VNS chronic side-effect palette** (hoarseness, cough, dyspnea) — credible tells a crewmate might catch Jae hiding.
11. **Impedance rise / electrode heating / battery sag** as overuse signatures; **seizure kindling → status epilepticus** as the escalation risk of overstimulation.
12. **Nonce-based replay protection** + signature blacklisting as the honest reason a handshake works "once, for 12 seconds, then never again."

---

## Corrections Needed

### 1. Replace/augment "current stops his heart" (the key medical fix)
- **Drop:** the cardiogenic / galvanic-current framing — implant telemetry does not pass a defibrillator-class current through the body, and that is not how cardiac arrest occurs in neurostimulation patients.
- **Use instead (neurogenic):** the bridge forces the implant to dump sustained, over-charge-density stimulation into Jae's **vagus/limbic system**, producing **parasympathetic/vagal overdrive → AV-nodal block → asystole** (Warnock 2024), and at the 40-second extreme a **SUDEP-type neurogenic cardiorespiratory collapse** (Noebels 2024). The lethal, escalating, countable cost is fully preserved — it just arrives through his *nervous system*, which is both medically honest and thematically sharper (his implant was put in to prevent exactly this).
- **Keep "his heart finds the wrong rhythm / briefly stops"** — it matches documented VNS-induced AV block/asystole.
- **Optional texture:** hoarseness/cough/dyspnea (VNS tells), tremor/myoclonus (motor-cortex spread / kindling), electrode heat + battery sag (engineering tells).

### 2. The most defensible protocol seam (the key engineering fix)
- **Use:** Jae presses his **retroauricular induction coil** against the train's onboard **IMD-interrogation port**; they couple on the **inductive / MICS-MedRadio (402–405 MHz)** band and exchange an **IEEE 11073** (cardiac-implant nomenclature) handshake bridged to **HL7/FHIR**. He spoofs a **distressed-passenger IMD** → authorized medical override → 12-second privileged window.
- **Explicitly flag as world-building:** trains don't currently ship IMD-interrogation gateways; frame it as a specialized/flagship-train medical feature built from *real* bands and standards.
- **Why this matters:** it removes the "defib current flows through him" physics error *and* gives the port a concrete, physical, tactile identity (press head-to-panel, align coil, few-cm coupling).

---

## Sources

**Manufacturer / device**
- NeuroPace RNS System (how it works, ~3 min/day stimulation, **~10.8-yr battery RNS-320**, lower SUDEP): https://www.neuropace.com/the-rns-system/ , https://www.neuropace.com/patients/rns-vs-vns-epilepsy-treatment/ , https://www.neuropace.com/providers/rns-system-neuromodulation/
- LivaNova VNS Therapy System Epilepsy Physician's Manual, May 2020 (cited via NeuroPace).

**Peer-reviewed (PubMed)**
- Warnock et al., *Cureus* 2024 — **Complete Heart Block and Ventricular Asystole Caused by VNS Therapy** (PMID 38435952; PMCID PMC10906750). https://pubmed.ncbi.nlm.nih.gov/38435952/
- Hartnett et al., *J ECT* 2023 — Asystole during ECT; **vagal mechanism** (PMID 35700970). https://pubmed.ncbi.nlm.nih.gov/35700970/
- Sun et al., *Am J Case Rep* 2021 — Trigeminocardiac reflex → bradycardia/ cardiac arrest (PMID 34077403; PMCID PMC8183304). https://pubmed.ncbi.nlm.nih.gov/34077403/
- Noebels JL, *Jasper's Basic Mechanisms of the Epilepsies* 5e, 2024 — **SUDEP is neurogenic, not cardiogenic; postictal bradycardia → brainstem collapse** (PMID 39637214). https://pubmed.ncbi.nlm.nih.gov/39637214/
- Harnack et al., *J Neurosci Methods* 2004 — **Electrode material, charge density & duration → tissue damage** (3 vs 26 µC/cm²/phase; Pt/Ir) (PMID 15325129). https://pubmed.ncbi.nlm.nih.gov/15325129/
- Tamura et al., *Neuromodulation* 2025 — VNS "super responders," **low charge density**, output current 0.84 vs 1.91 mA (PMID 41128704). https://pubmed.ncbi.nlm.nih.gov/41128704/
- Haddad et al., *Pediatr Neurol* 2023 — Ultra-Rapid Duty Cycling VNS, **3.025 mA tolerated, battery sooner** (PMID 37611408). https://pubmed.ncbi.nlm.nih.gov/37611408/
- Bansal et al., *Epilepsia* 2026 — VNS outcomes, higher duty cycle/output → better control (PMID 41217293). https://pubmed.ncbi.nlm.nih.gov/41217293/
- McCarthy & Burdette, *Neurotherapeutics* 2026 — **RNS programming is iterative** (PMID 42302539). https://pubmed.ncbi.nlm.nih.gov/42302539/
- Turk et al., *Neuromodulation* 2026 — Cortical stimulation params **2–130 Hz, 90–450 µs, ≤7 V / 4 mA** (PMID 41964625). https://pubmed.ncbi.nlm.nih.gov/41964625/
- de Oliveira & Cukiert, *Stereotact Funct Neurosurg* 2025 — Neuromodulation landscape (VNS/DBS/RNS incl. ANT-DBS) (PMID 40991616). https://pubmed.ncbi.nlm.nih.gov/40991616/

**Regulator / standards**
- FCC — Medical Device Radiocommunications Service (MedRadio) (402–405 MHz MICS origin; 401–406 MHz + expansions): https://www.fcc.gov/general/medical-device-radiocommunications-service-medradio
- ISO/IEEE 11073 standards overview (incl. "Implantable device, cardiac" nomenclature 11073-10103; Agent/Manager; HL7/DICOM interwork): https://en.wikipedia.org/wiki/ISO/IEEE_11073
- Medical Device Radiocommunications Service (MedRadio/MICS, Medtronic 1999 petition, 25 µW EIRP, inductive skin-contact history): https://en.wikipedia.org/wiki/Medical_Implant_Communication_Service

**Flagged for follow-up verification (not independently fetched this pass — do not present to a reviewer as confirmed)**
- RNS exact pulse-parameter maxima (current/PW/frequency) — verify against the current **NeuroPace Physician Product Manual**.
- ANT-DBS exact parameters and the 2018 FDA epilepsy approval — verify against **Medtronic** labeling.
- BLE "MEDIS"/medical-device profile specifics — verify a primary citation if BLE is used in the seam (the seam stands without it).
- Surgical-anatomy specifics of the **retroauricular coil/battery pocket** as a `[DESIGN CHOICE]` — confirm against otologic/cochlear-implant surgical anatomy if challenged.
