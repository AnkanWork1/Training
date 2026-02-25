import subprocess
import os
import signal
import time
from typing import Literal

PORT = 8080
PROCESS = None  # Global process handle for the model server


def _absolute_path(path: str) -> str:
    """Return absolute path to avoid relative path issues."""
    return os.path.abspath(path)


def _is_port_used(port: int) -> bool:
    """Check if the given port is already in use."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def serve_model(
    model_path: str,
    model_type: Literal["vllm", "gguf"],
    llama_server_path: str = None,
    dtype: str = "float16",
    max_model_len: int = 4096,
):
    """
    Start a local model server.

    Args:
        model_path: Path to the model file/directory.
        model_type: "vllm" or "gguf".
        llama_server_path: Path to llama-server binary (required for gguf).
        dtype: Data type for vllm models (default "float16").
        max_model_len: Maximum context length (default 4096).
    """
    global PROCESS

    # Avoid duplicate server
    if _is_port_used(PORT):
        print(f"Model server already running on port {PORT}")
        return

    model_path = _absolute_path(model_path)
    if not os.path.exists(model_path):
        raise ValueError(f"Model path does not exist: {model_path}")

    if model_type == "vllm":
        cmd = [
            "vllm",
            "serve",
            model_path,
            "--port",
            str(PORT),
            "--dtype",
            dtype,
            "--max-model-length",
            str(max_model_len),
        ]

    elif model_type == "gguf":
        if not llama_server_path:
            raise ValueError("For gguf models, llama_server_path must be provided")

        llama_server_path = _absolute_path(llama_server_path)
        if not os.path.exists(llama_server_path):
            raise ValueError(
                f"llama-server not found at {llama_server_path}\nBuild llama.cpp first."
            )

        cmd = [
            llama_server_path,
            "--model",
            model_path,
            "--port",
            str(PORT),
            "--ctx-size",
            "2048",
            "--temp",
            "0.3",
            "--repeat-penalty",
            "1.1",
        ]

    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    print("\nStarting model server:")
    print(" ".join(cmd))

    PROCESS = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # Give server some time to start
    time.sleep(4)
    print("Model server launched!")


def stop_model():
    """Gracefully stop the running model server."""
    global PROCESS

    if PROCESS:
        print("Stopping model server...")
        PROCESS.send_signal(signal.SIGINT)
        PROCESS.wait()
        PROCESS = None