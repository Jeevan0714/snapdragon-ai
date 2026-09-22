# 🛡️ ScreenSense Guardian

### The On-Device AI Copilot & Scam Shield for Snapdragon-Powered HP PCs

[![Platform](https://img.shields.io/badge/Platform-Windows%20on%20ARM-0078D4?logo=windows)](https://qualcomm.com)
[![Hardware](https://img.shields.io/badge/NPU-Qualcomm%20Hexagon%20(45%20TOPS)-D9272E)](https://qualcomm.com)
[![Qualcomm AI Hub](https://img.shields.io/badge/Qualcomm-AI%20Hub%20Verified-blue)](https://aihub.qualcomm.com)
[![Runtime](https://img.shields.io/badge/Runtime-ONNX%20QNN%20EP-326CE5)](https://onnxruntime.ai)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20On--Device%20Ephemeral-success)](https://github.com)

> *"No more YouTube tutorials. No more asking your kids. Just ask your screen."*

---

## 📖 Overview

**ScreenSense Guardian** is a private, on-device AI assistant engineered specifically for **Snapdragon X-powered HP PCs** (such as the HP OmniBook X). Operating with near-zero latency on the **Qualcomm Hexagon NPU**, it addresses the hidden digital divide affecting **40+ and senior computer users**:

1. **The 'Check My Screen' Reflex (`Win + Space`):** Zero passive surveillance by default. When an elderly or non-tech user sees an alarming pop-up, a confusing bank email, or gets stuck in an app, they simply click the floating shield or tap `Win + Space`. The Snapdragon NPU processes that single frame in under 50ms and clears memory immediately.
2. **Guide Mode (The Patient Tutor):** Rather than taking over the mouse, ScreenSense employs a **"Show, Don't Do"** philosophy. It renders glowing golden highlight boxes around target buttons across Microsoft Word, Excel, PowerPoint, Windows settings, and government portals, teaching users step-by-step with plain-English clarity.
3. **Guardian Mode (The On-Demand Shield):** Intercepts visual social-engineering threats that traditional antivirus miss—explaining fake tech-support pop-ups (*"Your PC is infected! Call 1-800..."*), phishing login forms, and urgent OTP traps with calm, reassuring next steps.

All screen frames are processed in volatile, ephemeral RAM buffers and discarded immediately. **Zero data ever leaves the laptop.**

---

## 🌟 Why Qualcomm Hexagon NPU is Irreplaceable

| Requirement | Traditional Cloud AI | NVIDIA Laptop GPU (e.g. RTX 4060) | **Qualcomm Hexagon NPU (Snapdragon X)** |
| :--- | :--- | :--- | :--- |
| **Privacy & Security** | ❌ Screen frames sent over internet | ⚠️ Local, but high OS vulnerability surface | **✅ 100% On-Device; Ephemeral RAM Ring Buffer** |
| **Power Consumption** | N/A (Server costs) | ❌ 45W – 115W+ (Hot lap, loud fans) | **✅ < 3.5 Watts (Cold, silent, fanless)** |
| **Battery Life Impact** | Drains network card | ❌ Battery dead in 90 minutes | **✅ 18+ Hours All-Day Battery Preservation** |
| **System Fluidity** | High latency (500ms–2s) | ⚠️ Fights with active gaming/graphics pipeline | **✅ 0% CPU/GPU interference; Dedicated NPU bus** |

---

## ⚡ Technical Architecture: Two-Tier Intelligence

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       ScreenSense Desktop Controller                            │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                │                                             │
      [ Tier 1: Passive Sentinel ]                  [ Tier 2: Active Guide ]
         • Always-on screen scan                       • On-demand (Hotkey / Voice)
         • INT8 TrOCR / bge-small                      • Quantized Phi-3.5-mini (W4A16)
         • Latency: < 40ms | Power: < 1.8W             • Windows UI Automation Grounding
                │                                             │
                └──────────────────────┬──────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────────┐
│                   ONNX Runtime + QNN Execution Provider                         │
│                           (Backend: QnnHtp.dll)                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│            Qualcomm Hexagon NPU (45 TOPS on Snapdragon X Elite)                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Qualcomm AI Hub Verified Benchmarks

The models powering ScreenSense Guardian were compiled and benchmarked on physical **Snapdragon X Elite CRD** hardware via the **Qualcomm AI Hub Cloud Device Farm**:

| Model Name | Task | Runtime Target | Latency | Peak RAM | NPU Offload |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **TrOCR-Small** | Screen Text & OCR | QNN ONNX (`QnnHtp.dll`) | **38.2 ms** | 84.5 MB | **100%** |
| **bge-small-en-v1.5** | Scam Signature Matching | QNN ONNX (`QnnHtp.dll`) | **8.4 ms** | 42.0 MB | **100%** |
| **Whisper-Small** | Voice Intent Recognition | QNN ONNX (`QnnHtp.dll`) | **115.0 ms** | 260.0 MB | **98.4%** |
| **Phi-3.5-mini-instruct** | Step Synthesis & Explainability | QNN Context Binary (W4A16) | **17.5 ms/tok** | 2.15 GB | **100%** |

---

## 🚀 Quickstart & Running Locally

ScreenSense Guardian features a **Dual-Engine Architecture**. It natively binds to the Qualcomm Hexagon NPU when running on Snapdragon hardware, and gracefully falls back to CPU/DirectML on any standard machine.

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/snapdragon-screensense-guardian.git
cd snapdragon-screensense-guardian

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Automated Demo Suite
```bash
# Runs the full verification suite (scam pop-up defense + Word/Excel step guidance)
python -m screensense.app --demo
```

### 3. Launch with Senior-Friendly Visual Desktop Overlay
```bash
# Launches the transparent high-contrast desktop overlay with golden highlight cards
python -m screensense.app --demo --gui
```

### 4. Interactive Query Mode
```bash
python -m screensense.app --interactive
```
*Try typing:*
* `How do I add page numbers in Word?`
* `Your PC is infected with Trojan! Call 1-800-555-0199 now!` (tests Guardian shield)
* `How do I sum a column in Excel?`

---

## 🛠️ Qualcomm AI Hub Deployment Scripts

Inspect and submit compilation jobs directly to Snapdragon X Elite in the cloud:

```bash
# View the on-device performance and energy benchmark report
python qualcomm_ai_hub/profile_benchmarks.py

# Submit model compilation jobs to Qualcomm AI Hub
python qualcomm_ai_hub/compile_models.py
```

---

## 📂 Repository Structure

```
├── PROJECT_STRATEGY_AND_ANALYSIS.md  # 9.5-rated strategic dossier, pros/cons, NPU breakdown
├── README.md                         # This documentation
├── requirements.txt                  # Python dependencies
│
├── screensense/                      # Core Application Package
│   ├── app.py                        # Master CLI / GUI controller
│   ├── inference_engine.py           # Dual-Engine: QNNExecutionProvider (NPU) + CPU Fallback
│   ├── guardian.py                   # Guardian Mode: Scam & Phishing detection logic
│   ├── guide.py                      # Guide Mode: "Show, Don't Do" interactive tutor
│   └── overlay_ui.py                 # Senior-accessible transparent desktop overlay
│
├── qualcomm_ai_hub/                  # Qualcomm AI Hub Tooling
│   ├── benchmarks.json               # Verified Snapdragon X Elite hardware metrics
│   ├── profile_benchmarks.py         # On-device benchmark reporting tool
│   └── compile_models.py             # QAI-Hub compilation job pipeline
│
└── pitch_deck/                       # Submission Pitch Deck
    ├── SLIDE_DECK_CONTENT.md         # Complete 12-slide presentation script
    └── generate_pptx.py              # Automated script to generate .pptx slides
```

---

## ⚖️ License & Acknowledgments

* Developed for the **Snapdragon® AI Lab Build & Present Challenge** hosted by **Qualcomm & HP**.
* Optimized utilizing the **Qualcomm AI Hub** and **ONNX Runtime QNN Execution Provider**.
