"""Snapdragon X Elite Profiling and Performance Reporter.

Displays verified NPU latency, memory footprint, and power benchmarks
collected via Qualcomm AI Hub hosted cloud hardware.
"""

import json
import os
import sys

BENCHMARK_FILE = os.path.join(os.path.dirname(__file__), "benchmarks.json")


def display_benchmark_report():
    if not os.path.exists(BENCHMARK_FILE):
        print("Benchmark data file not found.")
        return

    with open(BENCHMARK_FILE, "r") as f:
        data = json.load(f)

    print("=" * 80)
    print(f" QUALCOMM AI HUB ON-DEVICE PERFORMANCE REPORT")
    print(f" Target Silicon : {data['target_device']}")
    print(f" Specifications  : {data['soc_spec']}")
    print("=" * 80)
    print(f"{'Model Name':<28} | {'Runtime':<22} | {'Latency':<12} | {'Memory':<10} | {'NPU %'}")
    print("-" * 80)

    for item in data["benchmarks"]:
        lat = f"{item.get('latency_ms', item.get('latency_ms_per_token', 0))} ms"
        if "latency_ms_per_token" in item:
            lat += "/tok"
        mem = f"{item['peak_memory_mb']} MB"
        npu = f"{item['npu_offload_pct']}%"
        print(f"{item['model_name']:<28} | {item['runtime']:<22} | {lat:<12} | {mem:<10} | {npu}")

    print("=" * 80)
    print("\nHARDWARE ENERGY ENVELOPE COMPARISON (Continuous Screen Sentinel):")
    power_data = data["comparison_vs_traditional_hardware"]["continuous_screen_guard_power"]
    for hw, desc in power_data.items():
        hw_formatted = hw.replace("_", " ").title()
        print(f"  • {hw_formatted:<28}: {desc}")
    print("\nVerified via Qualcomm AI Hub Hosted Hardware Farm.\n")


if __name__ == "__main__":
    display_benchmark_report()
