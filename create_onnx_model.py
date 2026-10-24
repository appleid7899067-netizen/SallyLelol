#!/usr/bin/env python3
"""
สร้างโมเดล ONNX ง่าย ๆ — MLP 2 เลเยอร์ (เขียนด้วย pure Python)
ไม่ต้อง PyTorch/TensorFlow/ONNX Runtime
เรียก: python3 create_onnx_model.py
"""

import subprocess
import sys
import os
import numpy as np
from datetime import datetime

def install_onnx():
    """ติดตั้ง onnx library"""
    try:
        import onnx
        print("✓ onnx already installed")
        return True
    except ImportError:
        print("📦 Installing onnx...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "onnx", "-q"])
        print("✓ onnx installed")
        return True

def onnx_export(input_dim=4, hidden_units=16, output_dim=2, model_name="MLP2Layer.onnx"):
    # ต้อง import หลัง install
    from onnx import helper, numpy_helper
    from onnx import TensorProto

    print("🚀 Creating ONNX model (pure Python + ONNX)...")

    # 1. สร้างโมเดล: MLP (Linear → ReLU → Linear → Softmax)
    inputs = [helper.make_tensor_value_info("x", TensorProto.FLOAT, [None, input_dim])]
    outputs = [helper.make_tensor_value_info("y", TensorProto.FLOAT, [None, output_dim])]

    # Linear (fc1): input_dim → hidden_units
    W1 = numpy_helper.from_array(np.random.randn(input_dim, hidden_units).astype(np.float32), name="W1")
    b1 = numpy_helper.from_array(np.random.randn(hidden_units).astype(np.float32), name="b1")
    fc1_w = helper.make_tensor("fc1_weight", TensorProto.FLOAT, [input_dim, hidden_units], W1.float_data)
    fc1_b = helper.make_tensor("fc1_bias", TensorProto.FLOAT, [hidden_units], b1.float_data)
    fc1 = helper.make_node("MatMul", ["x", "fc1_weight"], ["fc1_out"], name="fc1")
    fc1_add = helper.make_node("Add", ["fc1_out", "fc1_bias"], ["fc1_out"], name="fc1_add")

    # ReLU
    relu = helper.make_node("Relu", ["fc1_out"], ["relu_out"], name="relu")

    # Linear (fc2): hidden_units → output_dim
    W2 = numpy_helper.from_array(np.random.randn(hidden_units, output_dim).astype(np.float32), name="W2")
    b2 = numpy_helper.from_array(np.random.randn(output_dim).astype(np.float32), name="b2")
    fc2_w = helper.make_tensor("fc2_weight", TensorProto.FLOAT, [hidden_units, output_dim], W2.float_data)
    fc2_b = helper.make_tensor("fc2_bias", TensorProto.FLOAT, [output_dim], b2.float_data)
    fc2 = helper.make_node("MatMul", ["relu_out", "fc2_weight"], ["fc2_out"], name="fc2")
    fc2_add = helper.make_node("Add", ["fc2_out", "fc2_bias"], ["fc2_out"], name="fc2_add")

    # Softmax
    softmax = helper.make_node("Softmax", ["fc2_out"], ["y"], name="softmax")

    graph = helper.make_graph(
        [fc1, fc1_add, relu, fc2, fc2_add, softmax],
        "MLP2Layer",
        inputs,
        outputs,
        [fc1_w, fc1_b, fc2_w, fc2_b]
    )

    model = helper.make_model(graph, opset_imports=[helper.make_operatorsetid("", 18)])
    onnx.save(model, model_name)

    print(f"✓ Exported to ONNX: {model_name}")

    # 2. ทดสอบ logic ด้วย Python ธรรมดา (ไม่ใช้ ONNX Runtime)
    print("\nTesting model with Python...")
    W1_data = W1.as_numpy()
    b1_data = b1.as_numpy()
    W2_data = W2.as_numpy()
    b2_data = b2.as_numpy()

    def relu_numpy(x):
        return np.maximum(0.0, x, dtype=np.float32)

    def softmax_numpy(x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    test_input = np.random.randn(2, input_dim).astype(np.float32)
    print(f"  Input shape: {test_input.shape}")

    # Forward
    h = relu_numpy(np.dot(test_input, W1_data) + b1_data)
    logit = np.dot(h, W2_data) + b2_data
    output = softmax_numpy(logit)
    print(f"  Output shape: {output.shape}")
    print(f"  Output sample: {output[0]}")

    # Summary
    print("\n" + "="*50)
    print("Summary:")
    print("="*50)
    print(f"Model: MLP (2 hidden units)")
    print(f"  Input: {input_dim} features")
    print(f"  Hidden: {hidden_units} neurons")
    print(f"  Output: {output_dim} classes")
    print(f"  Layers: Linear → ReLU → Linear → Softmax")
    print()

    model_path = os.path.abspath(model_name)
    file_size = os.path.getsize(model_path) / 1024
    print(f"File path: {model_path}")
    print(f"File size: {file_size:.2f} KB")
    print("="*50)

    # Save metadata
    import json
    metadata_path = model_name.replace(".onnx", "_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump({
            "model_type": "MLP2Layer",
            "input_dim": input_dim,
            "hidden_units": hidden_units,
            "output_dim": output_dim,
            "created_at": datetime.now().isoformat()
        }, f, indent=2)
    print(f"Meta{metadata_path}")

    return model_name

if __name__ == "__main__":
    print("🚀 Starting ONNX model creation...\n")
    install_onnx()
    onnx_export()
    print("\n✅ Done! File ready to use with ONNX Runtime 🚀")