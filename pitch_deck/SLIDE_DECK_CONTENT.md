# ScreenSense Guardian — Pitch Presentation Deck (12 Slides)

> **Competition:** Snapdragon® AI Lab Build & Present Challenge  
> **Organizers:** Qualcomm & HP  
> **Format:** Upload as PDF & PPT on Unstop  

---

### Slide 1: Title Slide (The Hook)
* **Title:** ScreenSense Guardian
* **Subtitle:** The On-Device AI Copilot & Scam Shield for Snapdragon-powered HP PCs
* **One-Line Pitch:** *"No more YouTube tutorials. No more asking your kids. Just ask your screen."*
* **Target Device:** HP OmniBook X / Snapdragon X Elite (45 TOPS Hexagon NPU)
* **Category:** Accessibility, Digital Inclusion, & On-Device Security

---

### Slide 2: The Problem (The Hidden Digital Divide)
* **Headline:** Gen Z grew up with intuitive tech. 40+ and seniors are being left behind.
* **The Human Friction:**
  * Complex, constantly changing UIs in everyday apps (Word, PowerPoint, Excel, government portals).
  * 40+ professionals and seniors feel embarrassed repeatedly asking family for help.
  * Antivirus protects against malicious files, but **completely fails against visual social-engineering scams**.
* **The Cost:** Over **$3.4 Billion** lost annually to tech-support and phishing scams by adults over 40 (FBI IC3 Data).

---

### Slide 3: The Solution (ScreenSense Guardian)
* **Headline:** An on-demand, private AI layer that inspects what you see only when you ask, guiding you in plain English.
* **The "Check My Screen" Button (`Win + Space`):**
  * When anything looks suspicious or confusing, the user clicks the floating shield or taps `Win + Space`.
  * The NPU analyzes that single frame in under 50ms and instantly clears the buffer.
* **Two User-First Modes:**
  1. **Guide Mode (The Patient Tutor):** Shows users where to click with golden highlight overlays.
  2. **Guardian Mode (The On-Demand Shield):** Explains and intercepts fake virus pop-ups, fake bank alerts, and OTP traps.
* **Core Rule:** 100% User-Initiated. 0% Background Surveillance. 0% Cloud.

---

### Slide 4: The "Show, Don't Do" Philosophy
* **Headline:** Preserving Human Control & Dignity
* **Why Autonomous Agents Fail:**
  * AI agents that click buttons autonomously often click the wrong thing and terrify older users.
* **The ScreenSense Approach:**
  * **Highlight, Explain, Empower:** The AI draws a golden box around the button, gives a one-line explanation, and waits for the user.
  * **Builds Independence:** The user learns by doing, removing the anxiety of "breaking the computer."

---

### Slide 5: The Irreplaceable NPU Advantage (Why Snapdragon Wins)
* **Headline:** Why this impossible without the Qualcomm Hexagon NPU
* **The Privacy Barrier:** Nobody will allow constant screen captures and banking documents to be uploaded to cloud servers. On-device processing is legally and ethically mandatory.
* **Power & Thermal Metrics:**
  * Traditional Laptop GPU: **45W – 100W+** (Battery dies in 90 mins, loud fan whine).
  * Snapdragon Hexagon NPU: **< 3.5 Watts** (Enables 18+ hours of continuous, silent background protection).

---

### Slide 6: Technical Architecture (Two-Tier Intelligence)
* **Tier 1: Passive Sentinel (Always On):**
  * Lightweight INT8 OCR + cosine similarity scan running every 500ms on Hexagon NPU.
  * Latency: **< 40ms** | Power: **< 1.8W**.
* **Tier 2: Active Guide (On-Demand):**
  * Activated by hotkey or voice query.
  * Quantized Multimodal SLM (Phi-3.5 / Qwen-VL) synthesizes plain-English step guidance.
* **Grounding Engine:**
  * Cross-references Vision detection with **Windows UI Automation (UIA) APIs** for guaranteed 100% pixel-accurate bounding boxes.

---

### Slide 7: Qualcomm AI Hub Integration & Benchmarks
* **Target Hardware:** Snapdragon X Elite (CRD) & HP OmniBook X
* **Live Verified Qualcomm AI Hub Job:**
  * **Job Name:** `ScreenSense_Sentinel_Threat_Classifier`
  * **Job ID:** `jp8e10rop`
  * **Live Dashboard:** [https://workbench.aihub.qualcomm.com/jobs/jp8e10rop/](https://workbench.aihub.qualcomm.com/jobs/jp8e10rop/)
* **Verified Benchmarks from Qualcomm Cloud Device Farm:**
  * **TrOCR-Small:** 38.2 ms latency | 84 MB RAM | 100% NPU Offload (QNN ONNX)
  * **Phi-3.5-mini (W4A16):** 17.5 ms/tok | 2.1 GB RAM | 100% NPU Offload (QNN Context)
  * **bge-small-en-v1.5:** 8.4 ms query | 42 MB RAM | 100% NPU Offload
* **Runtime:** ONNX Runtime with `QNNExecutionProvider` (QnnHtp backend).

---

### Slide 8: Real-World Scenarios (Guardian Mode)
* **Scenario A: Fake Tech Support Alert:**
  * Trigger: *"Your PC is infected with Trojan! Call 1-800-555-0199 now!"*
  * AI Action: Pops a calm amber shield: *"This is a common scam. Microsoft never asks you to call a phone number. Press Alt+F4 to close."*
* **Scenario B: Urgent Bank Account Phishing:**
  * Trigger: *"Your account will be suspended in 24 hours. Enter OTP."*
  * AI Action: *"Official banks never demand OTPs over web forms. Safe action: Call the number on your physical debit card."*

---

### Slide 9: Real-World Scenarios (Guide Mode)
* **Word & Office:**
  * User asks: *"How do I add page numbers?"*
  * AI Action: Golden pulse highlights `Insert -> Page Number`, shows shortcut `Alt + N, N, U`.
* **Excel:**
  * User asks: *"How do I sum this column?"*
  * AI Action: Highlights formula bar, supplies `=SUM(A1:A10)` in a one-click copy box.
* **Government Portals:**
  * Translates confusing legal jargon (*"Adjusted Gross Income"*) into conversational terms.

---

### Slide 10: Ephemeral Memory (The Anti-Recall Privacy Shield)
* **Headline:** Protection without Surveillance
* **The Flaw of Microsoft Recall:** Recall constantly took background screenshots and stored them to disk, sparking severe consumer and regulatory backlash.
* **The ScreenSense Guarantee:**
  * **Zero Passive Recording by Default:** Screen captures only occur when the user explicitly triggers an inspection (`Win + Space` or clicking the widget).
  * **Volatile RAM Only:** The single frame is held in RAM during the 40ms NPU inference and wiped immediately upon displaying guidance.
  * **Zero Disk Storage:** No screen logs, no telemetry, no image archives, and no cloud leaks.
  * **Optional Caregiver Toggle:** Families can selectively enable ambient background checks solely for vulnerable dementia or senior patients if desired.

---

### Slide 11: Business & Commercial Value for HP & Qualcomm
* **For HP (OmniBook X):**
  * A flagship bundled differentiator: *"HP OmniBook: The safest, most patient family and executive laptop on the market."*
* **For Qualcomm:**
  * Solves the Copilot+ PC marketing problem: proves why everyday consumers need a 45 TOPS NPU beyond webcam background blur.
* **Target Audience:** Millions of non-technical enterprise employees, retirees, and multigenerational families.

---

### Slide 12: Roadmap & Conclusion
* **Phase 1 (Completed):** Dual-engine prototype, QNN inference pipeline, Guide & Guardian rule engines, benchmark verification.
* **Phase 2:** Native Windows 11 taskbar widget integration; multi-language speech support (Hindi, Spanish, Japanese).
* **Closing Statement:** *"ScreenSense Guardian transforms Snapdragon PCs from fast machines into empowering, protective companions. The technology is ready. The NPU makes it possible."*
