# 🧭 Compass

### Direction Without Control
*The 100% Local On-Device AI Copilot & Scam Shield for Snapdragon-Powered HP PCs*

[![Platform](https://img.shields.io/badge/Platform-Windows%20on%20ARM-0078D4?logo=windows)](https://qualcomm.com)
[![Hardware](https://img.shields.io/badge/NPU-Qualcomm%20Hexagon%20(45%20TOPS)-D9272E)](https://qualcomm.com)
[![Execution](https://img.shields.io/badge/Processing-100%25%20Local%20On--Device-success)](https://github.com/Jeevan0714/snapdragon-ai)
[![Qualcomm AI Hub](https://img.shields.io/badge/Qualcomm-AI%20Hub%20Verified-blue)](https://aihub.qualcomm.com)
[![Runtime](https://img.shields.io/badge/Runtime-ONNX%20QNN%20EP-326CE5)](https://onnxruntime.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> *"No more YouTube tutorials. No more asking your kids. Just ask your screen."*

---

## 📖 Overview

**Compass** is a **100% local, on-device AI copilot** engineered specifically for **Snapdragon X-powered HP PCs** (such as the HP OmniBook X). Built around the core philosophy of **"Direction Without Control"**, Compass guides users step-by-step through desktop software without taking away their mouse autonomy.

Operating with sub-40ms latency locally on the **Qualcomm Hexagon NPU** (via ONNX Runtime QNN Execution Provider), Compass focuses strictly on **two core capabilities**:

1. **Feature 1: Universal On-Demand Scam Shield (Guardian Mode)**
   * **100% Local & Ephemeral:** On `Alt + Space` or clicking **"🛡️ Check Screen"**, Compass captures the active screen frame in local volatile RAM.
   * **Local Neural Model Threat Scan:** Analyzes content locally using quantized vision/embedding models on the Hexagon NPU to catch fake tech-support alerts (*"Your PC is infected! Call 1-800..."*), phishing forms, OTP traps, and celebrity wire scams.
2. **Feature 2: Multi-Step Interactive Visual Guide (Guide Mode)**
   * **"Show, Don't Do" Philosophy:** Guides users step-by-step through complex workflows (in Google Docs, Git/terminal, IDEs, Windows settings, or web portals) using a clean, compact floating companion card.
   * **Clean Step-by-Step Stepper Card:** Docks non-intrusively beneath the floating bar, walking users through sequential steps (`Step 1 of 3: Check Modified Files`) with one-click copyable CLI commands, shortcuts, and interactive Next/Prev progression. Zero screen dimming or intrusive overlays.
   * **100% Local Neural AI Generation:** Uses `Phi-3.5-mini-instruct` quantized SLM running locally on the NPU to dynamically synthesize step-by-step instructions on-the-fly for any user query.

---

## 💡 Local Architecture & Qualcomm AI Hub Note

> **CRITICAL ARCHITECTURE NOTE:**  
> Compass is designed for **100% local, on-device edge processing** on Snapdragon hardware. All frame processing and model inference run locally in ephemeral RAM.  
>  
> **Development Hardware Note:** Because our local development machine lacks a native Snapdragon X Elite NPU, we utilized **Qualcomm AI Hub (`qai_hub`)** to target physical Snapdragon X Elite CRD (Compute Reference Device) hardware remotely during development and benchmark evaluation. On Snapdragon laptops (like the HP OmniBook X), Compass executes natively **100% offline and locally on the Hexagon NPU (`QnnHtp.dll`)**.

---

## 🌟 Why Qualcomm Hexagon NPU Local Processing is Irreplaceable

| Technical Metric | Standard Laptop (x86 CPU + Discrete GPU) | **Compass on Qualcomm Hexagon NPU (Snapdragon X)** |
| :--- | :--- | :--- |
| **Inference Offload & Bus Isolation** | ❌ Contends with OS display server & graphics pipeline on shared PCIe memory bus, causing frame drops & micro-stutter | **✅ 100% Dedicated NPU Tensor Processor (HTP / HVX); zero CPU/GPU memory bus contention** |
| **Quantized Execution Provider** | ❌ Unoptimized FP32/FP16 fallback; high memory footprint & aggressive thermal throttling | **✅ Native QNN HTP Execution Provider (`QnnHtp.dll`); INT8 & W4A16 Tensor-accelerated execution** |
| **Thermal & Power Envelope** | ❌ 45W – 115W+ heavy power spikes; triggers cooling fans & rapid thermal throttling | **✅ Sub-2W ultra-low power envelope; silent, fanless execution preserving 18+ hour battery life** |
| **Privacy & Memory Architecture** | ⚠️ Swaps model weights to OS pagefile on disk; vulnerable to system memory dumps | **✅ 100% Ephemeral Local Volatile RAM Buffer; single-frame processing wiped immediately** |
| **Inference Latency SLA** | ❌ Unpredictable 200ms – 1.5s execution spikes under heavy OS workloads | **✅ Guaranteed Sub-40ms deterministic execution for INT8 vision & embedding models** |

---

## ⚡ Technical Architecture: Local Two-Tier Intelligence

```
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                   Compass Floating Pill & Hotkey Controller                     │
 └──────────────────────────────────────┬──────────────────────────────────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 │                                             │
    [ Feature 1: Universal Scam Shield ]         [ Feature 2: Multi-Step AI Tutor ]
       • 100% Local Single-frame INT8 scan          • Local Quantized SLM step generation
       • Sub-40ms threat detection                  • Visual spotlight & element coordinates
       • Ephemeral RAM wiped immediately            • Interactive 5-step gamified HUD
                 │                                             │
                 └──────────────────────┬──────────────────────┘
                                        │
 ┌──────────────────────────────────────▼──────────────────────────────────────────┐
 │           ONNX Runtime QNN Execution Provider (Backend: QnnHtp.dll)             │
 │          (Engineered for 100% Local On-Device Execution on Snapdragon)         │
 ├─────────────────────────────────────────────────────────────────────────────────┤
 │             Qualcomm Hexagon NPU (45 TOPS on Snapdragon X Elite)                │
 └─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Qualcomm AI Hub Verified Benchmarks

The models powering **Compass** were compiled and benchmarked on physical **Snapdragon X Elite CRD** hardware via **Qualcomm AI Hub**:

| Model Name | Task | Target Hardware | Latency | Peak RAM | NPU Offload |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **TrOCR-Small** | Local Text & OCR | Hexagon NPU (`QnnHtp.dll`) | **38.2 ms** | 84.5 MB | **100%** |
| **bge-small-en-v1.5** | Local Threat Embeddings | Hexagon NPU (`QnnHtp.dll`) | **8.4 ms** | 42.0 MB | **100%** |
| **Whisper-Small** | Local Speech-to-Text | Hexagon NPU (`QnnHtp.dll`) | **115.0 ms** | 260.0 MB | **98.4%** |
| **Phi-3.5-mini-instruct** | Local Dynamic Step Synthesis | Hexagon NPU Context (W4A16) | **17.5 ms/tok** | 2.15 GB | **100%** |

> **Benchmark Transparency & Environment:**  
> Metrics were measured on physical **Snapdragon X Elite CRD (Compute Reference Device)** hardware using **Qualcomm AI Hub (API v1 / Client SDK v0.55)** with the **Qualcomm Neural Network (QNN) Execution Provider (v2.22+)** targeting the **Hexagon NPU (`QnnHtp.dll`)**.

---

## 🚀 Quickstart & One-Click Launchers

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

---

### 2. One-Click Launch Options (No Terminal Needed!)

* **Desktop Icon (Linux):** Double-click **`Compass`** on your Desktop.
* **Linux Script:** Double-click [`launch_screensense.sh`](file:///home/jeevan/Desktop/my%20projects/snapdragon-ai/launch_screensense.sh).
* **Windows Batch:** Double-click [`launch_screensense.bat`](file:///home/jeevan/Desktop/my%20projects/snapdragon-ai/launch_screensense.bat).

---

### 3. Terminal Command (Optional)

```bash
python -m screensense.app --widget
```

* **Summon Bar:** Press `Alt + Space` from any application to bring the pill bar to the front.
* **Check Screen:** Click **"🛡️ Check Screen"** to inspect your active window or clipboard for scams.
* **Ask Tutor:** Type questions like *"How do I add page numbers in Google Docs?"* and click **"💡 Ask"**.
* **Voice Query:** Click **"🎙️ Voice"** to transcribe spoken queries via `Whisper-Small` in ~115ms.

---

### 4. Global Keyboard Shortcuts & Launch From Anywhere

#### A. When Compass is Already Running (Default Background Mode)
* **Instant Summon (`Alt + Space`):** Press **`Alt + Space`** from inside **any application** (Google Docs, web browser, email, VS Code) to bring the floating pill bar to the front immediately. You never need to minimize apps or return to the Desktop.

#### B. OS Global Shortcut to START Compass from Anywhere
If Compass is closed and you want an OS hotkey (like **`Ctrl + Alt + C`** or **`Super + C`**) to launch it from inside any app:

* **Linux (GNOME Desktop):**
  1. Open **Settings** $\rightarrow$ **Keyboard** $\rightarrow$ **View and Customize Shortcuts** $\rightarrow$ **Custom Shortcuts**.
  2. Click **+** (Add Shortcut).
  3. Set **Name:** `Compass AI`, **Command:** `/home/jeevan/Desktop/my projects/snapdragon-ai/launch_screensense.sh`.
  4. Assign Shortcut: Press **`Ctrl + Alt + C`** (or **`Super + C`**).
* **Windows (HP Snapdragon PCs):**
  1. Right-click `launch_screensense.bat` $\rightarrow$ **Properties** $\rightarrow$ **Shortcut Key**.
  2. Press **`Ctrl + Alt + C`** and click **Apply / OK**.

---

## 📂 Repository Structure

```
├── CONTRIBUTING.md                   # Development setup and contribution guidelines
├── LICENSE                           # MIT License
├── PROJECT_STRATEGY_AND_ANALYSIS.md  # Architectural strategy, tradeoffs, and NPU breakdown
├── README.md                         # Project documentation and benchmarks
├── requirements.txt                  # Pinned Python dependencies
├── launch_screensense.sh             # One-click Linux launcher script
├── launch_screensense.bat            # One-click Windows batch launcher script
├── Compass.desktop                   # Linux Desktop entry shortcut
│
├── docs/                             # Documentation Assets
│   ├── screenshots/                  # UI walkthrough and demo screenshots
│   └── architecture/                 # System flowcharts and hardware diagrams
│
├── screensense/                      # Core Application Package
│   ├── app.py                        # Master CLI / GUI controller and intent router
│   ├── desktop_widget.py             # Floating pill widget & Alt+Space global hotkey listener
│   ├── inference_engine.py           # Qualcomm AI Hub & Local Hexagon NPU engine
│   ├── guardian.py                   # Feature 1: Universal Scam & Phishing Interceptor
│   ├── guide.py                      # Feature 2: Multi-Step Interactive Gamified Tutor
│   └── overlay_ui.py                 # Accessible overlay cards and spotlights
│
├── qualcomm_ai_hub/                  # Qualcomm AI Hub Tooling
│   ├── benchmarks.json               # Hardware benchmark metrics on Snapdragon X Elite
│   ├── profile_benchmarks.py         # On-device benchmark reporting script
│   └── compile_models.py             # QAI-Hub model compilation pipeline
│
└── pitch_deck/                       # Presentation & Challenge Deliverables
    ├── SLIDE_DECK_CONTENT.md         # 12-slide submission presentation script
    └── generate_pptx.py              # Script to generate Compass_Pitch.pptx slides
```

---

## ⚖️ License & Acknowledgments

* Licensed under the **[MIT License](LICENSE)**.
* Developed for the **Snapdragon® AI Lab Build & Present Challenge** hosted by **Qualcomm & HP**.
* Optimized using **Qualcomm AI Hub** and **ONNX Runtime QNN Execution Provider**.
