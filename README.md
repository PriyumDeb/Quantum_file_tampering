# ⚛️ Quantum File Tampering Detector (Quantum Fingerprint)
> **A quantum content-integrity engine using 3-qubit SWAP Tests, binary phase-encoding, and depolarizing noise simulation to detect and pinpoint digital tampering.**

- **Author:** Priyum Deb ([@PriyumDeb](https://github.com/PriyumDeb))
- **Engine:** Qiskit, Qiskit Aer (`AerSimulator`), Streamlit

---

## 💡 The Problem & The Quantum Solution
Can a quantum circuit detect if a digital file has been modified or tampered with?

Classical hashing (like SHA-256) tells you if an entire file changed, but it cannot tell you *where* or *how much* without extensive diffing. 

**Quantum File Tampering Detector** takes raw digital files, maps individual bytes into quantum state rotation angles on the Bloch Sphere, and executes a **3-Qubit SWAP Test (Fidelity Test)** under realistic **depolarizing hardware noise** to catch and pinpoint single modified bytes.

---

## 🚨 The ASCII vs. Raw Bytes Architecture Pivot

Originally, the system read text characters and converted their **ASCII values** into rotation angles.

While this worked for basic English words, testing with emojis (e.g., `😎`) caused character code values to jump way past 255 (reaching 1583+), causing the rotation angle to blow past $\pi$ and loop around the Bloch sphere multiple times.

### 💡 The Fix:
Modern digital files contain emojis, code, formatting, or binary data. The engine was refactored to read raw **binary bytes** (`rb`):
- Every byte in computing is strictly bounded between **0 and 255**.
- By mapping $\theta = \left(\frac{\text{byte}}{255}\right) \times \pi$, every byte maps smoothly to an angle in $[0, \pi]$.
- No phase overflow or round-off bugs—the engine can reliably fingerprint **any digital file** (text, markdown, code, logs, and binary media).

---

## 🔬 How the Quantum Circuit Works (The 3-Qubit SWAP Test)

1. **Qubit 0 (The Ancilla / Observer):** Initialized in superposition using a Hadamard (`H`) gate.
2. **Qubit 1 (Original Byte):** Prepared by rotation $R_y(\theta_1)$ where $\theta_1 = (\text{byte}_1 / 255) \times \pi$.
3. **Qubit 2 (Received Byte):** Prepared by rotation $R_y(\theta_2)$ where $\theta_2 = (\text{byte}_2 / 255) \times \pi$.
4. **Controlled-SWAP (Fredkin Gate):** Controlled by Qubit 0, conditionally swaps Qubit 1 and Qubit 2.
5. **Interference & Measurement:** A second Hadamard on Qubit 0 measures the state overlap:
   - **If the bytes are tampered:** The fidelity drops and the observer qubit starts measuring `1`!

---

## 🌪️  Noise Model & Statistical Filter

Physical quantum processors are noisy. To simulate real quantum hardware rather than ideal math:
- **Depolarizing Noise (`qiskit_aer.noise`):** Added a 1-qubit depolarizing error ($1\%$) to `H` gates and a 3-qubit depolarizing error ($1.1\%$) to `CSWAP` gates.
- **2% Statistical Threshold:** Due to depolarizing noise, even matching bytes produce small background 1-counts (~70 out of 5000 shots). We introduced a statistical decision threshold:
  $$\text{Threshold} = 2\% \text{ of } 5000 \text{ shots} = 100 \text{ counts}$$
  - $\le 100 \text{ ones} \implies$ **MATCH (Verified under noise)**
  - $> 100 \text{ ones} \implies$ **TAMPERED (Detected modification)**

---

## 🛡️ Verification Modes

- **Strict Mode (`S`):** Enforces strict file length parity. If lengths differ, it instantly flags the size anomaly.
- **Adaptive Mode (`A`):** Tolerant mode that scans the common length of both files byte-by-byte and pinpoints the exact locations of altered content while reporting length differences.

---

## 🚀 Quickstart & Demo

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Terminal Engine (CLI)
```bash
python thing.py
```
*When prompted, enter:*
- Reference file: `file.txt`
- Received file: `file1.txt`
- Mode: `A` (Adaptive) or `S` (Strict)

#### Sample Output with Included Demo Files:
```text
file.txt:  "Hello Quantum"
file1.txt: "Hello Q.antum!"

Byte 00 | Original: H | Received: H | Ones:   68 | ✅ MATCH
Byte 01 | Original: e | Received: e | Ones:   68 | ✅ MATCH
Byte 02 | Original: l | Received: l | Ones:   86 | ✅ MATCH
Byte 03 | Original: l | Received: l | Ones:   92 | ✅ MATCH
Byte 04 | Original: o | Received: o | Ones:   61 | ✅ MATCH
Byte 05 | Original:   | Received:   | Ones:   65 | ✅ MATCH
Byte 06 | Original: Q | Received: Q | Ones:   62 | ✅ MATCH
Byte 07 | Original: u | Received: . | Ones:  499 | 🚨 TAMPERED
Byte 08 | Original: a | Received: a | Ones:   75 | ✅ MATCH
Byte 09 | Original: n | Received: n | Ones:   88 | ✅ MATCH
Byte 10 | Original: t | Received: t | Ones:   81 | ✅ MATCH
Byte 11 | Original: u | Received: u | Ones:   87 | ✅ MATCH
Byte 12 | Original: m | Received: m | Ones:   86 | ✅ MATCH

Adaptive scan completed across common bytes (1 byte(s) length difference).
1 tampered byte(s) located in files.
```

### 3. Launch the Streamlit Interactive UI
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to upload files, compare byte angles, and visualize quantum comparison tables in real time!

---

## 📁 Supported File Formats
- Text files (`.txt`, `.log`, `.md`)
- Code and data files (`.py`, `.json`, `.csv`, `.sh`)
## Can handel if upgraded
- any binary format (png,jpef,etc)
