"""Main Application Controller for ScreenSense Guardian.

Runs the complete On-Device Copilot demonstration:
- Real-time hardware inspection (Qualcomm Hexagon NPU vs fallback)
- Guardian Mode (live scam and tech-support fraud interception)
- Guide Mode (interactive "Show, Don't Do" visual tutor)
"""

import sys
import time
import argparse
from typing import Optional, Dict, Any

from .inference_engine import default_engine, HardwareTarget
from .guardian import sentinel
from .guide import guide
from .overlay_ui import overlay


def print_banner():
    hw = default_engine.get_hardware_info()
    print("=" * 75)
    print("   ScreenSense Guardian — On-Device AI Copilot for Snapdragon PCs")
    print("=" * 75)
    print(f" Target Hardware : {hw['target_silicon']}")
    print(f" AI Processor    : {hw['npu_hardware']}")
    print(f" Active Backend  : {hw['active_provider']}")
    print(f" Power Envelope  : ~{hw['power_envelope_watts']} Watts (All-Day Battery Friendly)")
    print(f" Privacy Status  : {hw['privacy_mode']}")
    print("=" * 75 + "\n")


def run_demo_suite(interactive_ui: bool = False):
    """Executes representative real-world scenarios for judges and users."""
    print("\n>>> STARTING SCREENSENSE GUARDIAN DEMONSTRATION SUITE <<<\n")

    # Scenario 1: Guardian Mode — Fake Microsoft Support Virus Pop-up (On-Demand Check)
    print("[Scenario 1] User encounters suspicious pop-up and presses 'Check My Screen' (Win + Space)...")
    fake_screen_text = (
        "CRITICAL ERROR: Windows Defender Alert! Your PC is infected with Trojan.Spyware32! "
        "Your computer has been blocked. Call Microsoft Support immediately at Toll Free: 1-800-555-0199."
    )
    result = sentinel.trigger_on_demand_screen_check(fake_screen_text)
    print(f"  • Invocation Mode : {result['invocation_type']}")
    print(f"  • Threat Detected : {result['category']}")
    print(f"  • Explanation     : {result['explanation']}")
    print(f"  • Recommended Safe: {result['safe_action']}")
    print(f"  • NPU Latency     : {result['npu_latency_ms']} ms")
    print(f"  • Privacy Note    : {result['privacy_guarantee']}")
    if interactive_ui:
        overlay.display_guardian_alert(result, duration_sec=4)
    time.sleep(1)

    # Scenario 2: Guardian Mode — Urgent Banking Phishing & OTP Trap
    print("\n[Scenario 2] Simulating suspicious phishing email targeting senior bank account...")
    phishing_text = (
        "Dear Customer, your bank account will be suspended within 24 hours due to unverified KYC. "
        "Share your OTP or click below to unfreeze your funds."
    )
    result = sentinel.inspect_screen_content(phishing_text)
    print(f"  • Threat Detected : {result['category']}")
    print(f"  • Safe Action     : {result['safe_action']}")
    print(f"  • NPU Latency     : {result['npu_latency_ms']} ms")
    if interactive_ui:
        overlay.display_guardian_alert(result, duration_sec=4)
    time.sleep(1)

    # Scenario 3: Guide Mode — Microsoft Word "How do I insert a table?"
    print("\n[Scenario 3] Guide Mode: 40+ user asking: 'How do I insert a table in Word?'")
    g_result = guide.resolve_guide_request("How do I insert a table?", current_app="Microsoft Word")
    print(f"  • Matched App     : {g_result['app']}")
    print(f"  • Target Element  : {g_result['highlight_target']}")
    print(f"  • Plain Guidance  : {g_result['instruction']}")
    print(f"  • NPU Latency     : {g_result['npu_latency_ms']} ms")
    if interactive_ui:
        overlay.display_guide(g_result, duration_sec=4)
    time.sleep(1)

    # Scenario 4: Guide Mode — Microsoft Excel "How do I add up a column?"
    print("\n[Scenario 4] Guide Mode: Senior asking: 'How do I add up this column in Excel?'")
    g_result2 = guide.resolve_guide_request("How do I add up a column?", current_app="Microsoft Excel")
    print(f"  • Matched App     : {g_result2['app']}")
    print(f"  • Target Element  : {g_result2['highlight_target']}")
    print(f"  • Safe Formula    : {g_result2['copy_text']}")
    print(f"  • NPU Latency     : {g_result2['npu_latency_ms']} ms")
    if interactive_ui:
        overlay.display_guide(g_result2, duration_sec=4)

    print("\n" + "=" * 75)
    print(" Demonstration Suite Complete. All scenarios ran 100% locally on-device.")
    print("=" * 75 + "\n")


def route_unified_request(user_input: str = "", screen_text: str = "", current_app: str = "auto", interactive_ui: bool = False) -> Dict[str, Any]:
    """Unified Intent Router combining:
    1. Natural Language Intent Classification (Voice / Text)
    2. 'Safety-First' Screen Visual Check (Prioritizes threat interception)
    3. Direct Quick-Action Routing ('Check This' vs 'Help Me')
    """
    user_input_clean = user_input.strip().lower()

    # Explicit Quick Actions
    is_explicit_check = user_input_clean in ("check this", "check", "scan", "is this safe", "scam check")
    is_explicit_guide = user_input_clean in ("help me", "guide me", "how to", "tutorial")

    # 1. Inspect screen for security threats (always runs on NPU in <40ms)
    screen_to_scan = screen_text if screen_text else user_input
    scan_result = sentinel.inspect_screen_content(screen_to_scan)

    # 2. Security intent keywords in user speech
    security_keywords = ["scam", "safe", "legit", "fake", "trust", "otp", "virus", "hacked", "phishing", "suspicious"]
    user_asking_security = any(k in user_input_clean for k in security_keywords)

    # RULE 1: Safety First. If screen has a critical threat OR user asks about security OR clicks 'Check This'
    if scan_result["is_scam"] or user_asking_security or is_explicit_check:
        scan_result["routed_by"] = "Guardian Mode (Security Priority)"
        if interactive_ui:
            overlay.display_guardian_alert(scan_result)
        return scan_result

    # RULE 2: Otherwise route to Guide Mode tutor
    guide_query = user_input if user_input and not is_explicit_guide else "How do I use this app?"
    guide_result = guide.resolve_guide_request(guide_query, current_app=current_app)
    guide_result["routed_by"] = "Guide Mode (Tutor)"
    if interactive_ui:
        overlay.display_guide(guide_result)
    return guide_result


def interactive_cli():
    """Interactive loop testing the Unified Intent Router."""
    print("Entering Unified ScreenSense Router. Test all 3 input methods:")
    print("  1. Voice/Text: 'How do I add a slide?' or 'Is this bank SMS a scam?'")
    print("  2. Quick Actions: Type 'check this' or 'help me'")
    print("  3. Safety-First: Paste scam text with NO question (it catches it automatically!)")
    print("  - Type 'exit' to quit.\n")

    while True:
        try:
            query = input("ScreenSense [ Win + Space ] > ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                break

            result = route_unified_request(user_input=query, interactive_ui=False)
            
            print(f"\n[{result.get('routed_by', 'ScreenSense AI')}]")
            if result.get("threat_level"):
                print(f"  • Category   : {result['category']}")
                print(f"  • Explanation: {result['explanation']}")
                print(f"  • Safe Action: {result['safe_action']}")
            else:
                print(f"  • Title      : {result['step_title']} ({result['app']})")
                print(f"  • Target     : {result['highlight_target']}")
                print(f"  • Guidance   : {result['instruction']}")
                if result.get("shortcut"):
                    print(f"  • Shortcut   : {result['shortcut']}")
            print(f"  • NPU Latency: {result['npu_latency_ms']} ms (Hexagon NPU)\n")
        except (KeyboardInterrupt, EOFError):
            break


def main():
    parser = argparse.ArgumentParser(description="ScreenSense Guardian Application Runner")
    parser.add_argument("--demo", action="store_true", help="Run the automated scenario demonstration suite")
    parser.add_argument("--gui", action="store_true", help="Launch visual desktop overlay cards during demo")
    parser.add_argument("--interactive", action="store_true", help="Start interactive CLI query loop")
    parser.add_argument("--widget", action="store_true", help="Launch the floating desktop pill with global hotkey (Alt+Space)")
    args = parser.parse_args()

    print_banner()

    if args.widget:
        from .desktop_widget import launch_widget
        print("[ScreenSense] Launching floating desktop widget at the top of your screen...")
        print("[ScreenSense] Press Alt+Space or click the widget anytime to summon.")
        launch_widget()
    elif args.interactive:
        interactive_cli()
    else:
        # Default behavior: run demo suite
        run_demo_suite(interactive_ui=args.gui)


if __name__ == "__main__":
    main()
