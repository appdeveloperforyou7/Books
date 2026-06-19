# THE MOVING TARGET — Puzzle Layer

> The embedded, **solvable** interactive layer. Designed and locked **before** the beat sheet so clues plant honestly chapter-by-chapter. Every puzzle here is fair-play, self-contained (no required external links/app), and documented with its plaintext, ciphertext, key, and planting locations so `BEAT_SHEET.md` can seed it precisely.
>
> **Design principle:** the reader who is sharp can solve each layer *before* the crew does. That is the book's interactive promise ("the reader as the 8th crew member"). Layers stack; each is rewarding alone.

---

## 1. LAYER INVENTORY

| # | Layer | What it is | Where solved | Surfaces which twist |
|---|---|---|---|---|
| 1 | **Timetable Cipher** | Vigenère ciphertext naming the mastermind | Recovered at T3; decodable any time after | T3 → T9 |
| 2 | **ELVIA / ALIVE anagram** | The hidden principal's signature is an anagram | T3 (signature) → Epilogue (T9) | T9 |
| 3 | **Timestamp acrostic** | Minutes of 5 chapters → A1Z26 → "GHOST" | Epilogue reveal | T9 (theme) |
| 4 | **Motif numbers (7 & 600)** | Recurring numbers threaded as clues | Throughout; pays off at the climax | T5, T8 |
| 5 | **Shown-Plan vs. Real-Plan map** | The briefing the reader holds deviates from execution | The deviation *is* the plot | T3, T7, T8 |
| 6 | **Heist Phase frames** | Five act-opening frames; their order is a clue | Epilogue re-read | T8 (turn-the-train) |
| 7 | **The "ghost headcount"** | A 37th passenger nobody can place | T6 → T9 | T6, T9 |

---

## 2. THE TIMETABLE CIPHER (Layer 1 — the flagship puzzle)

- **Type:** **Vigenère cipher** (polyalphabetic, A=0…Z=25). Solvable with pencil, paper, and the table in the Heist Briefing chapter.
- **Plaintext (locked):** `ELVIA BUILT THE CONDUCTOR`
- **Key (locked):** `MERIDIAN` — the train's own name, printed on every page of the briefing and on the side of the train. *The key was in front of the reader the entire time.* (Fair-play elegance: the "key hidden earlier" is the title of the book's setting.)
- **Ciphertext (locked, verified):** `QPMQDJUVXXKPHKOAPYTBRZ`
- **Where the ciphertext is found:** inscribed/encoded in the **Meridian Ledger** recovered from Car F at the T3 midpoint (Ch21). The crew stares at it; only the reader (with the key) can solve it immediately.
- **Where the key is established:** the train's name is named in the prologue and on every chapter's phase-frame header.
- **Reader solve moment:** a sharp reader who tries the obvious key ("MERIDIAN") cracks it in the midpoint chapter, ~17 chapters before the crew confirms it in the epilogue → the "I beat the thief" shareability hook.

### 2.1 Worked example (printed in the appendix dossier; shown here for the writer)
Encryption: ciphertext letter = (plaintext + key) mod 26, with A=0.
- `E`(4) + `M`(12) = 16 → **Q**
- `L`(11) + `E`(4) = 15 → **P**
- `V`(21) + `R`(17) = 38 → 12 → **M**
- …continuing for all 22 letters yields **QPMQDJUVXXKPHKOAPYTBRZ**.
Decoding reverses it: plaintext = (cipher − key) mod 26.

### 2.2 Full verification table (writer reference — do not print in full in-novel)

| Pos | Plain | Key | (+) mod26 | Cipher |
|---:|:---:|:---:|:---:|:---:|
| 1 | E(4) | M(12) | 16 | Q |
| 2 | L(11) | E(4) | 15 | P |
| 3 | V(21) | R(17) | 12 | M |
| 4 | I(8) | I(8) | 16 | Q |
| 5 | A(0) | D(3) | 3 | D |
| 6 | B(1) | I(8) | 9 | J |
| 7 | U(20) | A(0) | 20 | U |
| 8 | I(8) | N(13) | 21 | V |
| 9 | L(11) | M(12) | 23 | X |
| 10 | T(19) | E(4) | 23 | X |
| 11 | T(19) | R(17) | 10 | K |
| 12 | H(7) | I(8) | 15 | P |
| 13 | E(4) | D(3) | 7 | H |
| 14 | C(2) | I(8) | 10 | K |
| 15 | O(14) | A(0) | 14 | O |
| 16 | N(13) | N(13) | 0 | A |
| 17 | D(3) | M(12) | 15 | P |
| 18 | U(20) | E(4) | 24 | Y |
| 19 | C(2) | R(17) | 19 | T |
| 20 | T(19) | I(8) | 1 | B |
| 21 | O(14) | D(3) | 17 | R |
| 22 | R(17) | I(8) | 25 | Z |

> **Invariance rule:** if any plaintext/key/ciphertext element changes, recompute this table and update both this file and the appendix dossier. The puzzle must always verify.

---

## 3. THE ELVIA / ALIVE ANAGRAM (Layer 2 — the deepest reveal)

- **The signature:** the Ledger and the Conductor's dormant directives are authored/signed **"ELVIA."**
- **The anagram:** **ELVIA → ALIVE.** (Exact 5-letter anagram; A-L-I-V-E.)
- **Who ELVIA is:** **Marin Vance**, Sloane's sister — long presumed dead on a prior Meridian run, actually alive and the hidden architect of the auction + the Conductor's directives. (See `CHARACTER_BIBLE.md` B5, `STORY_BIBLE.md` §2.3.)
- **Where planted:**
  - Ch21 — the Ledger bears the signature "ELVIA" (same moment as the cipher recovery — double hook).
  - Ch24 — the Conductor's dormant-directive log is authored by "ELVIA," no further ID.
  - Ch4 — the Leviathan "curse" is tied to disappearances including "the Vance girl" (Marin), seeding that a Vance "died" on this train.
- **Reader solve:** a reader who anagrams ELVIA → ALIVE predicts, chapters early, that the mastermind is *someone presumed dead* → Marin. Pairs with the cipher (which says "ELVIA built the Conductor").
- **Epilogue payoff:** the two layers converge — the cipher names ELVIA as the Conductor's builder; the anagram says ELVIA is "alive"; Marin steps forward.

---

## 4. THE TIMESTAMP ACROSTIC (Layer 3 — hidden in the countdown)

- **Mechanism:** every chapter header carries a **station timestamp** (the 14-hour countdown, e.g., `22:07 — LISBON`). The **minutes** of **five designated chapters**, read as **A1Z26** (1=A … 26=Z), spell a message.
- **The message (locked):** `GHOST` — chosen because the whole book is about the disappeared (the vanished sister, the trafficked witness, the "ghost headcount") and ELVIA is, literally, a ghost who is alive.
- **The five chapters (locked minutes):**

| Chapter | Timestamp minutes | A1Z26 | Letter |
|---|---:|---:|:---:|
| Ch4 | :07 | 7 | **G** |
| Ch12 | :08 | 8 | **H** |
| Ch17 | :15 | 15 | **O** |
| Ch23 | :19 | 19 | **S** |
| Ch24 | :20 | 20 | **T** |

> The specific chapter numbers are assigned in `BEAT_SHEET.md` (§"Puzzle seeding") so the minutes align with the countdown's natural progression — **and appear in correct G-H-O-S-T order** (chapter order = minute order). **Constraint:** the chosen minutes must remain plausible as real station-window timestamps (single minutes within an hour) — all five values qualify.
- **Where revealed:** the Epilogue dossier explicitly maps the five timestamps to GHOST, the thematic capstone.

---

## 5. MOTIF NUMBERS (Layer 4)

- **The LOUD motif — 600:** the Meridian's cruising speed. Stated constantly; the diegetic constant that makes "at-speed" everything. Mostly atmosphere, partly a clue to the *scale* of the impossible problem.
- **The QUIET motif — 7:** threads as a clue:
  - This is the **7th annual run**.
  - Marin "died" on a Meridian run **7 years ago**.
  - Car **F** is reached via a **7**-step sensor bypass (Jae's bridge sequence).
  - The "ghost headcount" passenger is the **37th** (3…7).
  - Culmination (T8): the routing-override code Sloane still remembers is a **7**-digit legacy key — her old access literally turns the train.
- **Rule:** never let 7 feel arbitrary; each instance should be *plausible in context* (a run number, a year, a count) so the pattern only emerges on reread.

---

## 6. SHOWN-PLAN vs. REAL-PLAN MAP (Layer 5 — the con spine)

The reader is handed the **shown Plan** in the Heist Briefing (Ch3) and watches execution deviate. The deviation *is* the plot.

| Layer | The Plan | Truth / deviation | Revealed |
|---|---|---|---|
| **Audience (shown) plan** | Board at speed → swap the Leviathan for a forgery → extract at speed at the terminus → deliver, get paid. | A jewel heist. Clean. | Ch3 (given) |
| **Contingency** | If the Vault Car resists, abandon the swap and grab the jewel raw. | Still treats it as a jewel. | Ch11–13 (stress) |
| **Real objective (crew, post-T3)** | The Leviathan is bait; the real prize is the **Ledger**; Reinhart will weaponise it → **sabotage the job, secure the Ledger, rescue the person.** | The heist becomes a heist-of-the-heist + a rescue. | Ch21 (T3) |
| **Deepest objective (ELVIA)** | Marin engineered the whole run to force this confrontation and get Lina out + the Ledger into the light. | The crew (and Sloane) were pieces in a grief-driven long game. | Epilogue (T9) |

- **Reader-as-solver:** the shown Plan contains one **untested assumption** (clean extraction at the terminus) that a careful reader can flag in Ch3. That assumption is the fuse for T7 (the kill-zone). Flagging it early = early-solver reward.

---

## 7. HEIST PHASE FRAMES (Layer 6 — act-openers as clues)

Each Act opens with a **Heist Phase frame** (a one-line title card before the chapter). The five phases are the classic con stages; the **clue** is that the **real execution inverts them** — the crew does **The Wire (delivery) first** (they pre-seed the escape/route hack), and **The Mark (the true target) last** (the real "mark" is Reinhart, revealed at the climax).

| Phase frame | Opens | Shown meaning | Real (inverted) meaning |
|---|---|---|---|
| **THE MARK** | Act I | The Leviathan is the target. | The real mark is Reinhart (revealed last). |
| **THE BOARD** | Act IIa | Board the train. | Board the *system* (Jae's bridge). |
| **THE CRACK** | Act IIb | Crack the Vault Car. | Crack the *truth* (the Ledger / Lina). |
| **THE SWAP** | Act III | Swap the forgery. | Swap *who controls the train* (turn-the-train, T8). |
| **THE WIRE** | (re-ordered payoff) | Wire the payment. | The Wire is done *first* — the delivery route is pre-hacked. |

- **Where revealed:** the Epilogue dossier shows the shown-order vs. real-order side by side — the inversion is the reread reward.

---

## 8. THE "GHOST HEADCOUNT" (Layer 7)

- **The clue:** the Conductor's manifest lists **37 passengers**; only **36** are accounted for among bidders/crew. The 37th is the "ghost."
- **What it is:** **Lina Provst** in Car F's hidden compartment (T6) — *and*, on reread, a second ghost: **ELVIA/Marin**, the architect who is "aboard" the system if not the seats.
- **Where planted:** Ch17 (manifest discrepancy), Ch21 (Lina found), Ch34 (the second ghost hinted), Epilogue (resolved to Marin).
- **Reader solve:** the 37th-headcount thread lets a reader anticipate T6 (a hidden person) and, with the ELVIA layer, T9 (a hidden architect).

---

## 9. TRANSLATION-FRIENDLINESS (the puzzle must survive FR/DE/ES)

- **Numbers are universal:** the Timetable Cipher (letters-as-numbers via Vigenère), the GHOST acrostic (A1Z26 on minutes), and the motif numbers (7/600) are **language-independent** — they survive translation intact.
- **The English-anchored anagram (ELVIA→ALIVE) is the one translation-sensitive layer.** Handling:
  - The **solve is demonstrated diegetically in-text**: a character spells it out ("E-L-V-I-A. Rearrange the letters. *Alive.*"). The *scene* survives translation even if the native anagram doesn't.
  - **Translator note** in the front matter flags the one English-dependent puzzle and permits a localized equivalent anagram where one exists naturally; otherwise the in-scene explanation carries it (per `ProjectGuidelines.md` §3 translation rule).
  - The **Meridian** key word is a proper noun (the train's name) — left untranslated — so the Vigenère solve works identically in every language.
- **Net:** in any language, a reader can solve the cipher, the GHOST acrostic, and the number motifs unaided; the anagram is carried by the scene. The book fully works without the companion dossier.

---

## 10. SOLVER'S CHECK (fair-play audit)

For each layer, confirm before lock:
1. **All evidence on the page before the reveal?** ✓ (ledger §2; ELVIA §3; minutes §4; numbers §5; plan §6; frames §7; headcount §8).
2. **No narrator lie required?** ✓ (tight 3rd-person; misdirection is omission/structure, never deception).
3. **Solves without external tools/links?** ✓ (pencil + the in-book timetable only).
4. **Each twist foreshadowed ≥2×?** ✓ (cross-checked in `TWIST_MAP.md` ledger).
5. **Resolves honestly (no cheated red herrings)?** ✓ (cross-checked in `TWIST_MAP.md` Red Herring Register).

---

## CONSISTENCY CHANGE-LOG

| Date | Change | Reason |
|---|---|---|
| 2026-06-18 | Puzzle Layer v1: 7 layers locked, Vigenère cipher verified char-by-char (QPMQDJUVXXKPHKOAPYTBRZ), ELVIA/ALIVE + GHOST acrostic + 7/600 motifs + plan-map + phase frames + ghost-headcount; translation plan set. | Must precede `BEAT_SHEET.md` so clues seed correctly (plan §6, §11). |
