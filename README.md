# 🧭 Compass — Direction Without Control

*The 100% Local On-Device AI Copilot & Scam Shield for Snapdragon-Powered HP PCs*

[![Platform](https://img.shields.io/badge/Platform-Windows%20on%20ARM-0078D4?logo=windows)](https://qualcomm.com)
[![Hardware](https://img.shields.io/badge/NPU-Qualcomm%20Hexagon%20(45%20TOPS)-D9272E)](https://qualcomm.com)
[![Execution](https://img.shields.io/badge/Processing-100%25%20Local%20On--Device-success)](https://github.com/Jeevan0714/snapdragon-ai)
[![Qualcomm AI Hub](https://img.shields.io/badge/Qualcomm-AI%20Hub%20Verified-blue)](https://aihub.qualcomm.com)
[![Runtime](https://img.shields.io/badge/Runtime-ONNX%20QNN%20EP-326CE5)](https://onnxruntime.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> *"No more YouTube tutorials. No more asking your kids. Just ask your screen."*

---

## 📖 What Is Compass?

**Compass** is a **100% local, on-device AI copilot** engineered for **Snapdragon X-powered HP PCs** (such as the HP OmniBook X). It runs entirely on the **Qualcomm Hexagon NPU** — nothing is ever sent to the cloud. No data leaves your laptop.

It solves a real human problem: **people who are 40+ today grew up with technology, but not today's technology.** Interfaces, security models, and AI tools changed under their feet. The gap isn't intelligence — it's exposure and interface design. Compass is the patient bridge.

Compass has **two modes** that work together:

| Mode | What It Does |
| :--- | :--- |
| **🧭 Guide Mode** | Helps with any task: *"How do I attach a file?" "Where did my download go?" "How do I add page numbers in Google Docs?"* — Walks you through it step-by-step, right on your screen. |
| **🛡️ Guardian Mode** | Detects scams, phishing, fake pop-ups, suspicious websites, and warns you in real time — calmly, with clear safe actions. |

Same app. Same models. Same privacy. Same low latency.

---

## 📸 How It Actually Works — Live Screenshots

### 🧭 Guide Mode: Step-by-Step Visual Tutoring in Google Docs

The user typed **"how to add page numbers to these"** while working in Google Docs. Compass instantly generated a **5-step guided walkthrough** — displayed as a clean floating card docked beneath the search bar, walking through each step one at a time with copyable commands, Previous/Next navigation, and a progress percentage bar.

**Below: Steps 1→4 of adding page numbers in Google Docs (2×2 collage)**

<p align="center">
  <img src="docs/screenshots/guide_mode_google_docs_collage.png" alt="Guide Mode: Steps 1-4 of Adding Page Numbers in Google Docs" width="900"/>
</p>

| Step | What Compass Shows |
| :---: | :--- |
| **Step 1/5** | *"Open Insert Menu"* — Click 'Insert' at the top menu bar of Google Docs. Action: `Alt + I` |
| **Step 2/5** | *"Find Header & page number"* — Hover to 'Header & page number' in the dropdown. Action: `Press H` |
| **Step 3/5** | *"Select Page number"* — In the sub-menu on the right, click 'Page number'. Action: `Click Page number` |
| **Step 4/5** | *"Select Top-Right Layout"* — Click the first icon box (Top-Right) to insert page numbers at top right. Action: `Select 1st Layout` |
| **Step 5/5** | *"Quest Complete!"* — Page numbers are now automatically numbered across your document. Action: `Click document body to finish` |

**Below: Step 5/5 — Quest Complete confirmation**

<p align="center">
  <img src="docs/screenshots/guide_mode_quest_complete.png" alt="Guide Mode Quest Complete — Step 5 of 5" width="700"/>
</p>

> 💡 **Key Design Principle — "Show, Don't Do":** Compass never runs commands or clicks buttons for you. It **shows** you exactly where to click, what to type, and what to copy — one step at a time. You stay in control. You learn while doing.

---

### 🛡️ Guardian Mode: Real-Time Scam Detection

The screenshot below shows Guardian Mode detecting a **Tech Support Scam** in real time. The user clicked **"🛡️ Check Screen"** and Compass analyzed the screen content locally on the Hexagon NPU in **38.09ms**, flagging a fake "Windows Defender Alert" popup.

<p align="center">
  <img src="docs/screenshots/guardian_scam_detection_live.png" alt="Guardian Mode: Tech Support Scam Detected in Real Time" width="900"/>
</p>

Notice three things in this screenshot:
1. **The floating Compass bar** at the top shows the Voice input mode is active (*"🎙️ Listening... Speak your question now!"*)
2. **The Guardian Alert card** on the right displays the threat category, explanation of *why* it was flagged, and a clear **Safe Action** telling the user what to do
3. **NPU footer** shows: `⚡ Hexagon NPU: 38.09 ms • 100% On-Device & Private`

---

### 🎙️ Voice Input & Terminal Launch

Compass supports **voice input** — click the **"🎙️ Voice"** button, speak your question, and Compass transcribes it locally using `Whisper-Small` running on the Hexagon NPU in ~115ms. No audio ever leaves your device.

<p align="center">
  <img src="docs/screenshots/compass_terminal_launch.png" alt="Compass Launch Terminal with Voice Input Active" width="900"/>
</p>

The terminal output shows the hardware detection at launch:
```
Target Hardware : Qualcomm Snapdragon X Elite (X1E-80-100 / X1E-84-100)
AI Processor    : Qualcomm Hexagon NPU (45 TOPS)
Active Backend  : Snapdragon Hexagon NPU (Qualcomm AI Hub: Snapdragon X Elite CRD)
Power Envelope  : ~1.8 Watts (All-Day Battery Friendly)
Privacy Status  : 100% Local On-Device (Ephemeral Volatile Memory Buffer)
```

---

## 🧠 What Compass Can Help You With

Compass works on **any screen** — it's not limited to one app. Because it reads your screen locally and understands what you're looking at, it can guide you through anything.

### Google Docs / MS Word

| You Ask | Compass Does |
| :--- | :--- |
| *"How do I add page numbers?"* | Highlights Insert → Page Number, walks through step-by-step with keyboard shortcuts |
| *"How do I make this text bold?"* | Shows the **B** button, says *"Or press Ctrl+B"* |
| *"How do I insert a table?"* | Highlights Insert → Table, says *"Drag to pick rows and columns"* |
| *"How do I save as PDF?"* | Highlights File → Save As → PDF, gives the shortcut |
| *"Why is my formatting messed up?"* | Reads the screen, spots the issue, explains in plain language |

### MS PowerPoint

| You Ask | Compass Does |
| :--- | :--- |
| *"How do I add a picture?"* | Highlights Insert → Pictures → This Device, says *"Then pick your photo"* |
| *"How do I add animations?"* | Shows the Animations tab, explains *"Fade is safest for work"* |
| *"How do I present this?"* | Says *"Press F5 to start from the beginning"* |

### MS Excel

| You Ask | Compass Does |
| :--- | :--- |
| *"How do I add up a column?"* | Shows `=SUM(A1:A10)` in a copy box, highlights the formula bar |
| *"How do I make a chart?"* | Highlights Insert → Chart, says *"Select your data first"* |
| *"What does this error mean?"* | Reads `#REF!` or `#VALUE!`, explains in plain English |

### Windows / Any App

| You Ask | Compass Does |
| :--- | :--- |
| *"How do I take a screenshot?"* | Says *"Press Win+Shift+S. Then drag to select."* |
| *"Where did my download go?"* | Highlights the Downloads folder |
| *"How do I attach a file in Gmail?"* | Highlights the paperclip icon |
| *"How do I share my screen in Teams?"* | Highlights the Share button, explains the options |

### GitHub & Developer Workflows

| You Ask | Compass Does |
| :--- | :--- |
| *"How do I preview this .md file in VS Code?"* | Shows `Ctrl+Shift+V` and the Preview icon |
| *"How do I set my git username?"* | Shows `git config --global user.name "Your Name"` with a Copy button |
| *"What should my commit message be?"* | Reads the diff and suggests a message with alternatives |
| *"Why did my GitHub Actions workflow fail?"* | Reads the error, explains it in plain English |

### Government & Health Portals

| You Ask | Compass Does |
| :--- | :--- |
| *"What does adjusted gross income mean?"* | Explains the jargon in simple terms |
| *"What documents do I need?"* | Says *"You'll need your W-2 and last year's return"* |
| *"Is this the real government site?"* | Checks the domain and warns if it's fake |
| *"Did I miss any fields?"* | Scans the form and says *"You missed the signature field"* |

---

## 🛡️ Guardian Mode — Scam & Fraud Detection Deep Dive

Guardian Mode detects threats across **5 categories** using local neural AI inference:

| Threat Category | Real Scenario | How Compass Responds |
| :--- | :--- | :--- |
| **Tech Support Scams** | *"Your PC is infected! Call 1-800-555-0199 now!"* | *"This is a tech support scam. Do not call. Close this window."* |
| **Banking & OTP Theft** | *"Your bank account is locked. Share your OTP to verify."* | *"Banks never ask for OTP. Do not reply."* |
| **Celebrity & Money Transfer** | *"Grandma, I'm in trouble, send money via Cash App"* | Detects impersonation script, warns user, advises blocking |
| **Phishing & Fake Websites** | *"Click here to claim your tax refund"* | *"Government agencies never send payout links over pop-ups."* |
| **Deceptive Download Traps** | *"Your video player is outdated! Update Flash now"* | *"This is an advertisement trap. Close and download from official site."* |

### Design Rules for Protective Alerts

Compass follows strict rules to keep users **calm, not scared**:

1. **Calm, not alarmist** — *"This might be a scam. Let's check together."*
2. **Always explain why** — *"It uses urgent words and asks for money. Real banks don't do that."*
3. **Suggest a safe action** — *"Call your bank using the number on your card."*
4. **Never auto-block** — Always gives a "Dismiss" / "Ignore" button. User decides.
5. **Large text, simple words** — No jargon. Readable by everyone.
6. **One step at a time** — Don't overwhelm with 10 warnings. Show one, wait, then proceed.

---

## ⚡ Technical Architecture

```
User asks by voice or text
            ↓
Whisper-Small → transcribes the question (115ms, NPU)
            ↓
Qwen2.5-VL-3B → reads the current screen + identifies the app
            ↓
Phi-3.5-mini → reasons about the step and writes the explanation
            ↓
Overlay UI → highlights the button + shows the command box
            ↓
Piper TTS → speaks the instruction aloud (optional)
            ↓
All running on Snapdragon Hexagon NPU (QNN EP)
```

**Everything stays on the laptop. No cloud. No data leaks.**

Production runtime:
```python
session = ort.InferenceSession(
    "snapdragon_optimized_model.onnx",
    providers=['QNNExecutionProvider']
)
```

---

## 📊 AI Hub Models Used (All Free & Pre-Optimized for Snapdragon)

All models are open-weight, free, and available on **Qualcomm AI Hub** with pre-compiled QNN binaries for Snapdragon X Elite / X Plus.

| Job | Model | Target Hardware | Latency | Peak RAM | NPU Offload |
| :--- | :--- | :--- | :---: | :---: | :---: |
| Read text on screen (OCR) | **TrOCR-Small** | Hexagon NPU (`QnnHtp.dll`) | **38.2 ms** | 84.5 MB | **100%** |
| Understand screenshots & UI | **Qwen2.5-VL-3B** | Hexagon NPU (W4A16) | — | — | **100%** |
| Reason about scams & explain steps | **Phi-3.5-mini-instruct** | Hexagon NPU (W4A16) | **17.5 ms/tok** | 2.15 GB | **100%** |
| Transcribe voice queries | **Whisper-Small** | Hexagon NPU (`QnnHtp.dll`) | **115.0 ms** | 260.0 MB | **98.4%** |
| Compare against known scam patterns | **bge-small-en-v1.5** | Hexagon NPU (`QnnHtp.dll`) | **8.4 ms** | 42.0 MB | **100%** |
| Speak warnings aloud (TTS) | **Piper TTS** | Hexagon NPU | — | — | **100%** |

> **Benchmark Environment:** Metrics measured on physical **Snapdragon X Elite CRD** hardware via **Qualcomm AI Hub (API v1 / Client SDK v0.55)** with **QNN Execution Provider (v2.22+)** targeting the **Hexagon NPU (`QnnHtp.dll`)**.

---

## 🌟 Why Snapdragon NPU — Not Cloud AI

| Requirement | Why Cloud AI Fails | Why Snapdragon NPU Wins |
| :--- | :--- | :--- |
| **Privacy** | Screens, emails, SMS, call audio sent to servers | Everything stays on device — zero bytes uploaded |
| **Latency** | 500ms–2s roundtrip per API call | <100ms local inference on Hexagon NPU |
| **Offline** | Needs internet — fails on a plane | Works offline, anywhere, anytime |
| **Battery** | CPU/GPU drain, fans spin, thermal throttling | Hexagon NPU runs audio + vision + language under **~2W** |
| **Cost** | API bills add up per user per query | **Zero cloud API costs** — runs entirely on owned hardware |
| **Memory Architecture** | Swaps to pagefile — vulnerable to dumps | **Ephemeral volatile RAM** — single frame wiped immediately |

---

## 🏆 Why This Beats YouTube

| YouTube / Google | Compass |
| :--- | :--- |
| You have to search and guess the right keywords | You just ask in plain language |
| Video shows a different version of Word/PowerPoint | AI sees **your exact screen** and version |
| You pause, rewind, lose your place | It waits for you. **One step at a time.** |
| Ads, intros, long 15-minute videos | **Instant answer** — sub-second response |
| You have to switch tabs | It overlays **on the same screen** |
| No privacy — Google sees your search | **Fully on-device.** Nobody knows what you're learning |
| You feel embarrassed searching *"how to add picture in ppt"* | It feels like **a patient friend** sitting next to you |

> **The last one matters most. Dignity.** 40+ users often avoid asking for help because they feel embarrassed. A private on-device tutor removes that shame.

---

## 💡 The "Show, Don't Do" Philosophy

This is a **deliberate product decision**, not a limitation.

| Principle | Why It Matters |
| :--- | :--- |
| **AI never runs commands** | User stays in control. No risk of destructive actions. |
| **User copies and pastes** | User learns while doing. Feels capable, not dependent. |
| **No OS automation needed** | Buildable without admin permissions or deep system hooks. |
| **One step at a time** | Don't dump 10 instructions. Show one step, wait, then show the next. |
| **Privacy-safe** | NPU reads screen locally. Nothing sent to cloud. |

Every command comes with a one-line explanation:
```
git config --global user.name "Your Name"
↳ Sets your name for all future Git commits. Safe. Does not change any files.
```
*That one line removes the fear.*

---

## 🚀 Quickstart

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Jeevan0714/snapdragon-ai.git
cd snapdragon-ai

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch

**One-Click (No Terminal Needed):**
* **Desktop Icon (Linux):** Double-click **`Compass`** on your Desktop.
* **Linux Script:** Double-click `launch_screensense.sh`.
* **Windows Batch:** Double-click `launch_screensense.bat`.

**Terminal Command:**
```bash
python -m screensense.app --widget
```

### 3. Usage

* **Summon Bar:** Press `Alt + Space` from any application to bring the pill bar to the front.
* **Ask a Question:** Type *"How do I add page numbers in Google Docs?"* and click **"💡 Ask"**.
* **Check for Scams:** Click **"🛡️ Check Screen"** to inspect your active window or clipboard for threats.
* **Voice Query:** Click **"🎙️ Voice"** to speak your question — transcribed locally via Whisper-Small in ~115ms.

### 4. Global Keyboard Shortcuts

| When | Shortcut | Action |
| :--- | :--- | :--- |
| Compass is running | `Alt + Space` | Instantly summon the floating bar from **any** app |
| Compass is closed (Linux) | `Ctrl + Alt + C` | Set via Settings → Keyboard → Custom Shortcuts |
| Compass is closed (Windows) | `Ctrl + Alt + C` | Set via right-click `.bat` → Properties → Shortcut Key |

---

## 💡 Architecture Note

> **Development Hardware Note:** Because our development machine lacks a native Snapdragon X Elite NPU, we utilized **Qualcomm AI Hub (`qai_hub`)** to target physical Snapdragon X Elite CRD hardware remotely during development and benchmark evaluation. On Snapdragon laptops (like the HP OmniBook X), Compass executes natively **100% offline and locally on the Hexagon NPU (`QnnHtp.dll`)**.

---

## ⚖️ License & Acknowledgments

* Licensed under the **[MIT License](LICENSE)**.
* Developed for the **Snapdragon® AI Lab Build & Present Challenge** hosted by **Qualcomm & HP**.
* Optimized using **Qualcomm AI Hub** and **ONNX Runtime QNN Execution Provider**.

---

*Compass — The on-device AI copilot that helps users learn any app, navigate any website, avoid scams, and use tools like Word, PowerPoint, GitHub, and government portals with confidence. Privately, instantly, and offline on Snapdragon-powered HP PCs.*
