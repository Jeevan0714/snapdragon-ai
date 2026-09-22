"""Export ScreenSense Sentinel Classifier to ONNX and submit live compile job to Qualcomm AI Hub.
Target Hardware: Snapdragon X Elite CRD (Qualcomm Hexagon NPU).
"""

import os
import onnx
from onnx import helper, TensorProto
import numpy as np
import qai_hub as hub

def create_screensense_sentinel_onnx(output_path="screensense_sentinel.onnx"):
    """Creates a fast screen threat classifier ONNX model (Embedding -> Logits)."""
    # Inputs & Outputs
    input_tensor = helper.make_tensor_value_info('embedding_input', TensorProto.FLOAT, [1, 384])
    output_tensor = helper.make_tensor_value_info('threat_logits', TensorProto.FLOAT, [1, 4])

    # Weights for Layer 1 (384 -> 128)
    w1_val = np.random.randn(384, 128).astype(np.float32) * 0.05
    b1_val = np.zeros(128, dtype=np.float32)
    w1_tensor = helper.make_tensor('W1', TensorProto.FLOAT, [384, 128], w1_val.flatten())
    b1_tensor = helper.make_tensor('B1', TensorProto.FLOAT, [128], b1_val.flatten())

    # Weights for Layer 2 (128 -> 4)
    w2_val = np.random.randn(128, 4).astype(np.float32) * 0.05
    b2_val = np.zeros(4, dtype=np.float32)
    w2_tensor = helper.make_tensor('W2', TensorProto.FLOAT, [128, 4], w2_val.flatten())
    b2_tensor = helper.make_tensor('B2', TensorProto.FLOAT, [4], b2_val.flatten())

    # Nodes: MatMul -> Add -> Relu -> MatMul -> Add
    gemm1_node = helper.make_node('Gemm', ['embedding_input', 'W1', 'B1'], ['h1'], alpha=1.0, beta=1.0)
    relu_node = helper.make_node('Relu', ['h1'], ['h1_relu'])
    gemm2_node = helper.make_node('Gemm', ['h1_relu', 'W2', 'B2'], ['threat_logits'], alpha=1.0, beta=1.0)

    # Graph & Model
    graph = helper.make_graph(
        [gemm1_node, relu_node, gemm2_node],
        'ScreenSense_Sentinel',
        [input_tensor],
        [output_tensor],
        [w1_tensor, b1_tensor, w2_tensor, b2_tensor]
    )

    model = helper.make_model(graph, producer_name='ScreenSense_AI')
    onnx.save(model, output_path)
    print(f"Generated ONNX model: {output_path}")
    return output_path


def submit_to_snapdragon_x_elite(model_path):
    print("\nConnecting to Qualcomm AI Hub Cloud...")
    device = hub.Device("Snapdragon X Elite CRD")
    print(f"Selected Device: {device.name}")

    print("Submitting compile job to Qualcomm Hexagon NPU...")
    compile_job = hub.submit_compile_job(
        model=model_path,
        device=device,
        name="ScreenSense_Sentinel_Threat_Classifier",
        options="--target_runtime onnx"
    )

    print("\n" + "=" * 70)
    print("🚀 QUALCOMM AI HUB COMPILE JOB SUBMITTED SUCCESSFULLY!")
    print("=" * 70)
    print(f" Job Name  : {compile_job.name}")
    print(f" Job ID    : {compile_job.job_id}")
    print(f" Status    : {compile_job.get_status()}")
    print(f" Live URL  : {compile_job.url}")
    print("=" * 70)
    print("\nYou can view your live compile job on Qualcomm AI Hub at:")
    print(f"👉 {compile_job.url}\n")
    return compile_job


if __name__ == "__main__":
    onnx_file = create_screensense_sentinel_onnx()
    submit_to_snapdragon_x_elite(onnx_file)
