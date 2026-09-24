# Contributing to ScreenSense Guardian

Thank you for your interest in contributing to ScreenSense Guardian! This guide walks you through setting up your development environment, testing code changes, and submitting pull requests.

---

## 🛠️ Development Setup

### Prerequisites
* Python 3.10 or later
* Git
* (Optional) Windows on ARM device with Snapdragon X Elite/Plus for native QNN Hexagon NPU execution. On Linux/macOS/x86_64, ScreenSense runs seamlessly via CPU/DirectML fallback.

### Clone and Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jeevan0714/snapdragon-ai.git
   cd snapdragon-ai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 🧪 Running Tests & Demonstrations

Before submitting any code changes, verify that the test and demo suites execute cleanly:

1. **Run the automated verification suite:**
   ```bash
   python -m screensense.app --demo
   ```

2. **Run the visual desktop overlay test:**
   ```bash
   python -m screensense.app --demo --gui
   ```

3. **Run the floating desktop widget:**
   ```bash
   python -m screensense.app --widget
   ```

4. **Verify Qualcomm AI Hub profiling script:**
   ```bash
   python qualcomm_ai_hub/profile_benchmarks.py
   ```

---

## 📐 Code Style & Architecture Guidelines

To keep the codebase maintainable, secure, and fast on low-power NPU hardware, please adhere to these standards:

1. **Privacy-First (Non-Negotiable):**
   * Never store, log, or transmit raw screen frames or user queries to external servers.
   * All frame processing must remain in volatile, ephemeral memory buffers.

2. **Dual-Engine Compatibility:**
   * Any NPU-optimized model logic in `inference_engine.py` must include a clean CPU fallback so contributors without Snapdragon hardware can run and test code.

3. **Python Standards:**
   * Follow [PEP 8](https://peps.python.org/pep-0008/) naming conventions and layout.
   * Include type hints (`typing.Dict`, `typing.List`, `typing.Optional`) on all public functions.
   * Write clear, non-alarmist UI copy aimed at senior and non-technical users.

---

## 🚀 Submitting Changes

1. **Create a topic branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
   *(or `fix/issue-description` for bug fixes)*

2. **Commit your changes:**
   * Write concise, descriptive commit messages:
     ```text
     feat(guardian): add romance scam detection signature
     fix(widget): prevent search bar override on clipboard scan
     docs: update benchmark hardware configuration notes
     ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request:**
   * Provide a clear description of the problem solved or feature added.
   * Include reproduction steps or CLI output verifying your changes.
