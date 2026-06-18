# Research Report: RSA Encryption, Prime Factorization & Cybersecurity Threats
## For Thriller Novel Use

---

# PART 1: RSA ENCRYPTION — HOW IT WORKS (FOR THRILLER READERS)

## What is RSA?

RSA is a public-key cryptosystem invented in **1977** by three MIT computer scientists: **Ron Rivest, Adi Shamir, and Leonard Adleman**. The name comes from their initials. It was publicly described in Martin Gardner's *Mathematical Games* column in *Scientific American* in August 1977.

**Secret history:** An equivalent system was developed secretly in **1973** by English mathematician **Clifford Cocks** at GCHQ (Britain's signals intelligence agency), but this was classified until **1997**.

RSA is built on a beautifully simple asymmetry:
- **Multiplying two large prime numbers is easy** — a computer can do it in microseconds.
- **Factoring the product back into those two primes is astronomically hard** — for a 2048-bit key, it would take the world's fastest supercomputers billions of years.

## How Public-Key Cryptography Works (In Simple Terms)

Think of it like a padlock and key:
1. **Your public key** is like an open padlock. You give copies to everyone. Anyone can use it to lock a message.
2. **Your private key** is the only key that opens that padlock. You keep it secret.
3. When someone sends you a message, they "lock" it with your public padlock. Only your private key can unlock it.

In RSA specifically:
- You pick two enormous prime numbers, **p** and **q** (each roughly 300+ digits long for a 2048-bit key).
- You multiply them to get **n = p × q**. This number **n** becomes part of your public key.
- The security relies on the fact that given **n**, no one can efficiently figure out what **p** and **q** were.

**The math in one sentence:** RSA uses the fact that `(message^public_key) mod n` creates ciphertext, and only `(ciphertext^private_key) mod n` reverses it — and the private key can only be calculated if you know the original prime factors.

## What Is Prime Factorization?

**Prime factorization** is the process of breaking down a composite number into its prime number building blocks.

- Example: 15 = 3 × 5 (easy)
- Example: 3233 = 61 × 53 (still easy for computers)
- Example: A 617-digit number used in RSA-2048 = ? × ? (**effectively impossible** with current technology)

The largest RSA number ever factored is **RSA-250** (829 bits, 250 decimal digits), factored in **February 2020** using ~2,700 core-years of computing on the General Number Field Sieve algorithm.

## Key Sizes Used Today

| Key Size | Status | Time to Break (Classical) |
|----------|--------|--------------------------|
| 1024-bit | **Deprecated** — considered insecure since 2010 | Feasible with nation-state resources (~500× the effort of RSA-240) |
| 2048-bit | **Standard** — minimum recommended | Billions of years with current technology |
| 4096-bit | **High security** — used for sensitive applications | Effectively impossible with current technology |

The most commonly chosen public exponent is **65537** (2^16 + 1).

## How Long Would It Take to Break RSA With Current Computers?

- A **2048-bit RSA key**: Estimates range from **10^15 to 10^20 years** using the best known classical algorithm (General Number Field Sieve).
- The best known classical factoring algorithm, GNFS, runs in **sub-exponential time**: O(e^(1.9 (log n)^(1/3) (log log n)^(2/3))).
- **No polynomial-time classical algorithm** for factoring has ever been discovered. This is one of the most important unsolved problems in computer science.
- It has **not been proven** that such an algorithm doesn't exist.

## What Systems Depend on RSA?

RSA and related public-key cryptography (Diffie-Hellman, elliptic curve) are the foundation of virtually ALL secure digital communication:

1. **HTTPS/SSL/TLS** — Every secure website (banking, shopping, email) uses RSA or similar algorithms for key exchange
2. **Banking & Financial Systems** — SWIFT transfers, ATM networks, credit card processing
3. **Email Encryption** — PGP, S/MIME
4. **VPNs** — All major VPN protocols use public-key cryptography
5. **Digital Signatures** — Software updates, legal documents, certificate authorities
6. **Government Communications** — Diplomatic cables, military communications, intelligence
7. **Cryptocurrency** — Bitcoin and other cryptocurrencies use elliptic curve cryptography (also vulnerable to quantum attacks)
8. **SSH** — Server administration worldwide
9. **Code Signing** — Verifying that software hasn't been tampered with
10. **Certificate Authorities** — The entire trust infrastructure of the internet (Verisign, DigiCert, etc.)

**The bottom line:** If RSA falls, the entire digital security infrastructure of modern civilization collapses. Every HTTPS connection, every bank transaction, every encrypted email becomes readable.

---

# PART 2: THE THREAT LANDSCAPE

## Quantum Computing Threat to RSA (Shor's Algorithm)

In **1994**, mathematician **Peter Shor** at Bell Labs published an algorithm that can factor integers in **polynomial time** on a quantum computer.

**What this means:** A sufficiently powerful quantum computer running Shor's algorithm could break RSA in hours or days instead of billions of years.

Key facts about Shor's algorithm:
- It runs in **O((log N)^3)** time — polynomial, meaning it scales manageably with key size
- It requires roughly **2n + 3** qubits to factor an n-bit number
- For a 2048-bit RSA key: roughly **4,096+ logical qubits** are needed
- With quantum error correction overhead: **millions of physical qubits** may be required
- Shor's algorithm also breaks Diffie-Hellman and elliptic curve cryptography

## Current State of Quantum Computing (As of 2026)

| Milestone | Status |
|-----------|--------|
| Largest quantum computer | IBM has demonstrated ~1,000+ physical qubits |
| Shor's algorithm demonstrated | Factored 15 (= 3 × 5) in 2001 (IBM, 7 qubits) and 21 in 2012 |
| Error-corrected logical qubits | Still in early stages — small numbers demonstrated |
| Breaking RSA-2048 | Estimated to need **20 million+ physical qubits** |
| "Q-Day" (when RSA becomes practically breakable) | Estimates range from **2030 to never** — most experts say 10-20+ years away |

**Reality check as of 2026:** Quantum computers lack the processing power to break widely used cryptographic algorithms. The high error rates and limited number of physical qubits mean we are still far from cryptographically relevant quantum computers.

However, the threat is taken seriously because of:
1. **"Harvest Now, Decrypt Later"** — Adversaries (especially China and Russia) are reportedly collecting and storing encrypted traffic NOW, planning to decrypt it once quantum computers become available
2. **Mosca's Theorem** — If (time to migrate) + (time data must remain secret) > (time to quantum threat), you're already vulnerable
3. **Secret breakthroughs** — Intelligence agencies don't publish their capabilities. We wouldn't necessarily know if a major advance happened behind closed doors

## Post-Quantum Cryptography — What Governments Are Doing

### NIST Post-Quantum Cryptography Standards (2024)

The U.S. National Institute of Standards and Technology (NIST) ran a multi-year competition starting in **2016** to develop quantum-resistant algorithms.

**On August 13, 2024, NIST released the first three finalized Post-Quantum Cryptography Standards:**

1. **FIPS 203 (ML-KEM, based on CRYSTALS-Kyber)** — Lattice-based key encapsulation. Primary standard for general encryption.
2. **FIPS 204 (ML-DSA, based on CRYSTALS-Dilithium)** — Lattice-based digital signatures. Primary standard for digital signatures.
3. **FIPS 205 (SLH-DSA, based on SPHINCS+)** — Hash-based digital signatures. Backup standard.

In **March 2025**, NIST selected **HQC** (code-based) as a fifth backup algorithm for key encapsulation.

### Other Government Actions

- **NSA** issued guidance in 2015 advising U.S. government agencies to begin transitioning
- **China** is investing heavily in quantum computing AND post-quantum cryptography
- **EU** published coordinated roadmaps for PQC adoption
- **Google, Apple, Signal, Cloudflare** have already begun implementing PQC in their products
- **Open Quantum Safe (OQS) project** provides open-source implementations of PQC algorithms

## How Long Would the World Take to Transition Away from RSA?

**Realistic timeline: 10-15 years MINIMUM**

Challenges:
1. **Legacy systems** — Billions of devices running older software that can't be easily updated
2. **Embedded systems** — ATMs, medical devices, industrial control systems, cars
3. **Key size increases** — Many PQC algorithms have larger keys (ML-KEM: ~1,568 bytes vs RSA-2048: 256 bytes)
4. **Performance overhead** — PQC algorithms are generally slower
5. **Standardization lag** — Even after NIST finalized standards, adoption takes years
6. **Supply chain** — Every certificate authority, every browser, every server needs updating
7. **The "long tail"** — Small organizations and developing nations will take much longer

**Historical precedent:** The transition from SHA-1 to SHA-256 took approximately **10 years** despite being much simpler. The PQC transition is far more complex.

## What Would Happen If RSA Was Broken Tomorrow?

### Immediate Consequences (Hours to Days)
- **Global financial panic** — Every bank transaction would be theoretically interceptable
- **Stock market crash** — Uncertainty about financial system integrity
- **Government emergency meetings** — National security implications worldwide
- **Internet commerce freezes** — HTTPS becomes unreliable
- **Intelligence暴露** — Previously captured encrypted communications become decryptable

### Short-term Consequences (Weeks to Months)
- **Emergency migration** to post-quantum algorithms (already developed but not widely deployed)
- **Economic disruption** — Trillions in financial transactions potentially compromised
- **Cyber attacks** — State actors and criminals exploit the vulnerability before transition completes
- **Loss of trust** — Digital signatures on software updates become meaningless until new systems are in place
- **Diplomatic crises** — If a single nation-state discovered the break, accusations of secretly exploiting it

### Long-term Consequences (Years)
- Complete overhaul of internet security infrastructure
- New cryptographic standards become mandatory
- Massive investment in cybersecurity
- Some data (previously captured) permanently compromised

---

# PART 3: HISTORICAL PRIME FACTORIZATION METHODS

## Ancient Mathematical Methods

### The Sieve of Eratosthenes (~240 BCE)

The earliest known systematic method for finding prime numbers, attributed to **Eratosthenes of Cyrene** (276–194 BCE), a Greek mathematician. The earliest known reference is in **Nicomachus of Gerasa's** *Introduction to Arithmetic* (early 2nd century CE).

**How it works:** List all numbers, then systematically cross out multiples of each prime (2, 3, 5, 7, ...). The remaining numbers are prime.

**Key insight for the novel:** This is a method for FINDING primes, not factoring. But it demonstrates that the study of prime numbers is ancient.

### Indian Mathematics and Prime Numbers

Indian mathematicians made extraordinary contributions that are directly relevant:

1. **Aryabhata (476–550 CE)** — In his *Aryabhatiya* (499 CE), presented work on number theory, place-value system, and algebra. He gave algorithms for finding square and cube roots, and worked with indeterminate equations (Diophantine equations).

2. **Brahmagupta (598–668 CE)** — Wrote the *Brahmasphutasiddhanta* (628 CE), containing the first systematic treatment of zero as a number, rules for arithmetic with negative numbers, and the **Brahmagupta-Fibonacci identity** about products of sums of squares. He developed methods for solving indeterminate equations of the form Nx² + 1 = y² (Pell's equation), which is deeply connected to factorization.

3. **Bhaskara II (1114–1185 CE)** — His *Lilavati* and *Bijaganita* advanced algebra, included the **Chakravala method** for solving indeterminate equations — one of the most sophisticated algorithms of the medieval world.

4. **The Kerala School (14th–16th centuries)** — **Madhava of Sangamagrama** (~1340–1425) and his followers developed infinite series expansions for trigonometric functions (sine, cosine, arctangent) two centuries before Newton and Leibniz invented calculus in Europe.

### The AKS Primality Test (2002)

On **August 6, 2002**, three computer scientists at **IIT Kanpur** — **Manindra Agrawal, Neeraj Kayal, and Nitin Saxena** — published "PRIMES is in P," proving that determining whether a number is prime can be done in polynomial time **without relying on any unproven conjectures**.

**Why this matters for the novel:**
- It was created by **Indian computer scientists**, connecting to the novel's theme of Indian mathematical heritage
- It proved something the entire cryptography community had been working toward for decades
- The proof was stunningly elegant and simple — the original paper was only 9 pages
- It won the **Gödel Prize** (2006) and **Fulkerson Prize** (2006)
- It's a PRIMALITY test, not a FACTORIZATION algorithm — but it demonstrates that breakthroughs in number theory can come from unexpected directions
- Crucially: AKS tells you IF a number is prime, but NOT what its factors are. The gap between "knowing something is composite" and "finding its factors" is exactly where RSA's security lives.

**The key mathematical identity behind AKS:** A number n is prime if and only if `(X + a)^n ≡ X^n + a (mod n)` for all integers a coprime to n.

### Is There Historical Precedent for an "Ancient" Factorization Algorithm?

**In reality: No.** No ancient civilization is known to have discovered an efficient factorization algorithm. The problem has resisted solution for millennia.

**However, for the novel's fiction, these facts provide plausible grounding:**
1. Indian mathematics was **centuries ahead** of European mathematics in many areas (zero, negative numbers, infinite series, algebra)
2. The **Kerala School's** infinite series were lost to history for centuries — their work was not transmitted outside Kerala
3. Indian mathematical knowledge was transmitted through **compressed sutras** designed for memorization — some knowledge could easily be lost or misunderstood
4. The **Bakhshali Manuscript** (7th century CE, discovered 1881) shows that significant mathematical texts can remain buried for over a millennium
5. The AKS test itself shows that **simple, elegant approaches to number theory problems can remain undiscovered for thousands of years**

---

# PART 4: THE REALISTIC SCENARIO FOR THE NOVEL

## If an Ancient Algorithm Existed That Was Fundamentally Different From Modern Approaches

### What Would Make It Dangerous?

Modern factorization algorithms attack the problem through increasingly complex algebra:
- **General Number Field Sieve** — Uses algebraic number theory, builds enormous "factor bases"
- **Quadratic Sieve** — Finds smooth numbers, builds matrices
- **Elliptic Curve Method** — Uses the mathematics of elliptic curves

An ancient algorithm could be dangerous if it:
1. **Approached factorization from a completely different angle** — not brute force, not algebraic number theory, but perhaps geometric or recursive
2. **Had a fundamentally different time complexity** — say, polynomial instead of sub-exponential
3. **Exploited a mathematical structure that modern approaches overlooked** — perhaps connected to modular arithmetic patterns, continued fractions, or properties that the ancients studied but modern mathematicians dismissed
4. **Was simple enough to implement efficiently on modern computers** — an elegant O(n^3) algorithm could factor a 2048-bit RSA key in minutes on a standard laptop

### Could an Ancient Algorithm Be Adapted to Modern Computing?

**Absolutely yes.** This is one of the most plausible elements:
1. **Algorithms are implementation-independent** — A mathematical procedure from 800 CE can be coded in Python today
2. **The AKS test is the perfect precedent** — Three Indian computer scientists discovered an elegant polynomial-time primality test. A fictional ancient factorization method could follow the same pattern
3. **The Chakravala method** is a real example of a sophisticated Indian algorithm that can be directly implemented on computers
4. **Many modern algorithms have ancient roots** — The Euclidean algorithm (300 BCE) is still one of the most important algorithms in cryptography

### What Would "Releasing" Such an Algorithm Actually Look Like?

**Phase 1: Academic Publication**
- A paper appears on **arXiv.org** (the preprint server where AKS was first posted)
- The cryptographic community is initially skeptical but intrigued
- Mathematicians begin verifying the proof — this takes days to weeks

**Phase 2: Verification and Panic**
- Independent researchers confirm the algorithm works
- Someone implements it and factors a small RSA key (say, 512-bit) in seconds
- The cybersecurity community recognizes the implications
- The paper goes viral in academic circles

**Phase 3: Global Response**
- Governments convene emergency meetings
- NIST and other standards bodies accelerate PQC deployment
- Financial markets react
- Tech companies scramble to patch systems

### How Would Governments React?

**Based on historical precedent (e.g., the discovery of cryptanalysis techniques during WWII):**
1. **Immediate classification attempts** — Governments would try to suppress the algorithm (but this is nearly impossible in the internet age)
2. **NSA/GCHQ involvement** — Intelligence agencies would want to determine: (a) is it real? (b) has anyone else discovered it? (c) can we use it before others?
3. **Diplomatic pressure** — Nations would accuse each other of prior knowledge
4. **Emergency legislation** — Laws requiring rapid adoption of post-quantum cryptography
5. **Military posturing** — If one nation had the algorithm secretly before public release, they'd have a devastating intelligence advantage

### How Would Financial Markets React?

**Likely scenario:**
- **Day 1-2:** Confusion, moderate sell-off as analysts assess impact
- **Day 3-5:** Panic selling if the algorithm is confirmed, especially in tech and financial sectors
- **Week 2:** Central banks issue emergency statements, markets stabilize somewhat
- **Month 1-3:** Major disruption as banks and financial institutions emergency-migrate systems
- **Long-term:** Massive investment in cybersecurity, new companies emerge, old ones fail

**Historical analog:** The discovery of the Heartbleed bug in 2014 caused significant market disruption, and that was a far more limited vulnerability.

### Timeline: Algorithm Published → Global Encryption Compromised

| Time | Event |
|------|-------|
| Day 0 | Paper published on arXiv |
| Days 1-3 | Initial verification by mathematicians |
| Days 4-7 | Implementation confirms small keys broken |
| Week 2 | Full cryptographic community aware; 1024-bit keys fall |
| Week 3-4 | 2048-bit keys demonstrated broken; global emergency declared |
| Month 2-3 | Emergency PQC deployment begins for critical systems |
| Month 6-12 | Major tech companies deploy PQC; financial systems migrate |
| Year 1-2 | Most critical infrastructure updated |
| Year 3-5 | The "long tail" — smaller organizations, developing nations, embedded systems still vulnerable |
| Year 5-10 | Near-complete transition (some legacy systems never updated) |

---

# PART 5: THE PHASED RELEASE CONCEPT

## Is It Realistic That the World Could Prepare for RSA Being Broken?

**Yes, with caveats.** This is actually the current real-world strategy for quantum computing threats:

1. **NIST has been working on this since 2016** — 8+ years of preparation
2. **Standards are ready** — FIPS 203, 204, 205 were finalized in August 2024
3. **Early adoption has begun** — Google, Apple, Signal, Cloudflare already testing PQC
4. **The framework exists** — "crypto-agility" is now a design requirement for new systems

**The problem:** Full deployment takes 10-15 years, and much of the world's infrastructure is NOT crypto-agile.

## How Long Would a Transition to Post-Quantum Cryptography Take?

**Best case (with advance warning):** 3-5 years for critical systems
**Realistic case:** 10-15 years for comprehensive deployment
**Worst case (surprise break):** Years of chaos, with critical systems patched in months but long-tail vulnerability for a decade

## What Would a "Responsible Disclosure" of Such an Algorithm Look Like?

**In cybersecurity, "responsible disclosure" is a well-established practice:**

1. **The discoverer privately notifies** key stakeholders (NIST, major tech companies, intelligence agencies) before public release
2. **A grace period** (typically 90 days) allows for patching
3. **Then full public disclosure** ensures the knowledge isn't monopolized by bad actors

**For a world-breaking algorithm, this process would be much longer:**
- Private notification to governments: **Weeks to months**
- Grace period for critical infrastructure: **6-12 months minimum**
- Staged public disclosure: **With increasing detail over time**

**The novel's phased release concept is brilliantly realistic.** It mirrors exactly how responsible disclosure works in cybersecurity, scaled up to an existential threat.

## Historical Precedents for Controlled Disclosure of Dangerous Knowledge

1. **The atomic bomb (Manhattan Project):** Scientific knowledge was classified, then gradually declassified
2. **Enigma decryption:** British intelligence kept the fact that they'd broken Enigma secret for **30 years** after WWII, using the knowledge covertly
3. **Diffie-Hellman key exchange:** Was actually discovered at GCHQ years before the public discovery, but kept classified
4. **RSA itself:** Clifford Cocks discovered it at GCHQ in 1973, four years before Rivest, Shamir, and Adleman — but it was classified until 1997
5. **Logjam attack (2015):** Researchers disclosed a vulnerability in Diffie-Hellman key exchange responsibly, giving time for patches before full publication
6. **Heartbleed (2014):** Responsible disclosure process was followed, with patches prepared before announcement
7. **SIDH/SIKE break (2022):** When Ward Beullens and others broke the SIKE post-quantum algorithm, the cryptographic community handled it through normal academic channels

---

# PART 6: FOR DIALOGUE — HOW CHARACTERS WOULD DISCUSS THIS

## How a Cryptographer Explains the Threat (Simple Terms)

**The "Combination Lock" Analogy:**

> "Imagine every bank vault in the world uses the same type of combination lock. The lock manufacturer says the lock is unbreakable because the combination has more possible combinations than there are atoms in the universe. And that's true — if you try every combination one by one. But what if someone discovered a mathematical shortcut? What if you could listen to the sound of the lock and figure out the combination in seconds? That's what this algorithm does. It doesn't try every possibility. It finds a shortcut through the mathematics."

**The "Skeleton Key" Analogy:**

> "RSA is like a system where every person in the world has a unique padlock. You give your open padlock to anyone who wants to send you a message — they lock it, and only you have the key. Now imagine someone found a way to create a master key that opens ALL padlocks. Not by trying every key, but by understanding a fundamental flaw in how the locks are manufactured."

**The "Mixed Paint" Analogy (actually used to explain Diffie-Hellman):**

> "Mixing two colors of paint is easy. Anyone can mix blue and yellow to get green. But given a pot of green paint, separating it back into blue and yellow is essentially impossible. RSA works on the same principle — multiplying two prime numbers is trivial, but factoring the product back is exponentially harder. Unless someone finds a way to 'unmix the paint' efficiently."

## What Questions Would a Smart Non-Expert (Like Meera) Ask?

1. **"Why can't we just use bigger keys?"**
   → Response: "We can, and we should as a stopgap. But if this algorithm is polynomial-time, doubling the key size only doubles the attacker's work. With classical attacks, doubling the key size squares the work. This is fundamentally different."

2. **"How is this different from quantum computers breaking RSA?"**
   → Response: "Quantum computers need massive physical infrastructure — cryogenic cooling, billions of dollars. This algorithm runs on a laptop. Anyone with a computer could use it."

3. **"Can't we just switch to a different encryption system?"**
   → Response: "Yes, and we have alternatives ready. But deploying them across the entire internet, every bank, every government, every device... that takes years. And during those years, everything is vulnerable."

4. **"Who would this hurt the most?"**
   → Response: "Everyone. But especially anyone who stored encrypted data assuming it would stay secret. That's every government's classified communications, every corporation's trade secrets, every person's private messages."

5. **"Why would someone release this? What's the motive?"**
   → Response: "That's the terrifying part. An activist might release it to force the world to adopt better security. A government might suppress it to maintain an intelligence advantage. Or someone might just believe knowledge should be free."

6. **"How do we know someone hasn't already discovered this and kept it secret?"**
   → Response: "We don't. The NSA, GCHQ, or Chinese intelligence could have had this for years. We'd never know. That's the nature of cryptographic breaks — the most valuable ones are the ones nobody talks about."

## What Would a Cybersecurity Expert's Nightmare Scenario Look Like?

> "The worst case isn't that someone publishes the algorithm. The worst case is that someone discovered it five years ago and told no one. Every encrypted communication for the last five years — diplomatic cables, military orders, corporate secrets, personal messages — has been silently collected and decrypted. We'd never know until it was too late. The information would already be out there, the damage already done. That's the 'harvest now, decrypt later' scenario, except instead of a future quantum computer, they had a mathematical shortcut all along."

**Another nightmare:**

> "Imagine this gets out on a Monday. By Tuesday, every script kiddie with a Python script is breaking HTTPS connections. By Wednesday, automated tools are available on the dark web. By Thursday, your grandmother's banking app is compromised. By Friday, the global financial system is in freefall. And the experts are screaming, 'We told you to migrate to post-quantum cryptography!' but it's too late."

---

# PART 7: ADDITIONAL TECHNICAL DETAILS FOR AUTHENTICITY

## The Largest Numbers Ever Factored (Publicly)

| Number | Bits | Digits | Year | Method |
|--------|------|--------|------|--------|
| RSA-250 | 829 | 250 | 2020 | GNFS (~2,700 core-years) |
| RSA-240 | 795 | 240 | 2019 | GNFS (~900 core-years) |
| RSA-768 | 768 | 232 | 2009 | GNFS (~2,000 core-years) |

## Current Quantum Computing Milestones

| Year | Achievement | Organization |
|------|-------------|--------------|
| 2001 | Factored 15 (= 3 × 5) using Shor's algorithm | IBM (7-qubit NMR) |
| 2012 | Factored 21 using Shor's algorithm | Multiple groups |
| 2019 | 53-qubit quantum computer | Google (claimed quantum supremacy) |
| 2023 | 1,000+ qubit processor | IBM (Condor) |
| 2024 | Error-corrected logical qubit demonstrations | Multiple (Harvard, QuEra, etc.) |

## NIST PQC Standards Summary (For Authenticity)

| Standard | Algorithm | Type | Use | Released |
|----------|-----------|------|-----|----------|
| FIPS 203 | ML-KEM (Kyber) | Lattice-based | Key encapsulation | Aug 2024 |
| FIPS 204 | ML-DSA (Dilithium) | Lattice-based | Digital signatures | Aug 2024 |
| FIPS 205 | SLH-DSA (SPHINCS+) | Hash-based | Digital signatures | Aug 2024 |
| FIPS 206 | FN-DSA (Falcon) | Lattice-based | Digital signatures | Draft |
| (Selected) | HQC | Code-based | Key encapsulation (backup) | Mar 2025 |

## Key Technical Terms to Use in Dialogue

- **Semiprime** — A number that is the product of exactly two primes (what RSA keys are)
- **Key encapsulation mechanism (KEM)** — Modern way to exchange encryption keys
- **Crypto-agility** — The ability to quickly switch cryptographic algorithms
- **Forward secrecy** — Property where compromising one session doesn't compromise past sessions
- **Harvest now, decrypt later** — Collecting encrypted data now to decrypt when technology catches up
- **Y2Q / Q-Day** — The hypothetical day quantum computers break current encryption
- **Mosca's Theorem** — Framework for assessing quantum risk: if X + Y > Z (migration time + data sensitivity window > time to quantum threat), you're vulnerable
- **General Number Field Sieve (GNFS)** — Current best classical factoring algorithm
- **Logical vs. physical qubits** — Physical qubits are error-prone; many physical qubits make one error-corrected logical qubit

## The Mathematical Heart of RSA (For the Technically Curious)

1. Choose two large primes: p and q
2. Compute n = p × q (the "modulus")
3. Compute λ(n) = lcm(p-1, q-1) (Carmichael's totient function)
4. Choose e such that 1 < e < λ(n) and gcd(e, λ(n)) = 1 (typically e = 65537)
5. Compute d such that d × e ≡ 1 (mod λ(n))

**Public key:** (n, e)
**Private key:** (d)

**Encrypt:** c = m^e mod n
**Decrypt:** m = c^d mod n

The security depends entirely on the difficulty of factoring n back into p and q.

---

# PART 8: FACT-CHECKING NOTES FOR THE AUTHOR

## Things That Are TRUE
- RSA was invented in 1977 by Rivest, Shamir, and Adleman ✓
- Clifford Cocks at GCHQ discovered the same system in 1973 (classified until 1997) ✓
- Shor's algorithm (1994) can break RSA on a quantum computer ✓
- NIST released PQC standards in August 2024 ✓
- AKS primality test was created by Indian scientists at IIT Kanpur in 2002 ✓
- The largest RSA number factored is RSA-250 (829 bits, 2020) ✓
- Indian mathematicians (Kerala School) discovered infinite series before Newton ✓
- "Harvest now, decrypt later" is a real concern ✓
- Brahmagupta, Aryabhata, and Bhaskara II were real Indian mathematicians ✓

## Things That Are FICTIONAL (For the Novel)
- Any ancient Indian (or any other) factorization algorithm that breaks RSA ✓ FICTIONAL
- The specific plot elements of the novel ✓ FICTIONAL
- The idea that an ancient civilization discovered polynomial-time factorization ✓ FICTIONAL

## Plausibility Notes
- An ancient mathematical manuscript being discovered is **very plausible** (Bakhshali Manuscript is real)
- A breakthrough factorization algorithm coming from an unexpected direction is **somewhat plausible** (AKS showed this can happen)
- The world being unprepared despite warnings is **extremely plausible** (Y2K, COVID, climate change show this pattern)
- A phased responsible disclosure process is **very plausible** and mirrors real cybersecurity practice
- The discovery causing global panic is **very plausible**

---

*Report compiled from: Wikipedia (RSA, Shor's Algorithm, Integer Factorization, Post-Quantum Cryptography, AKS Primality Test, Sieve of Eratosthenes, Indian Mathematics, NIST PQC Standardization), plus synthesized knowledge from the field of cryptography.*
