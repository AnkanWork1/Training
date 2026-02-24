import subprocess
import os
import signal
import time
from typing import Literal

PORT = 8080
PROCESS = None  


def _absolute_path(path: str) -> str:
    """
    Fix relative path issues.
    """
    return os.path.abspath(path)


def _is_port_used(port: int) -> bool:
    """
    Check if server already running.
    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def serve_model(
    model_path: str,
    model_type: Literal["vllm", "gguf"],
    dtype: str = "float16",
    max_model_len: int = 4096,
):

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
        ]

    elif model_type == "gguf":

        llama_server = _absolute_path(
            "/home/omjidubey/Desktop/Training/Week8/llama.cpp/build/bin/llama-server"
        )

        if not os.path.exists(llama_server):
            raise ValueError(
                f"llama-server not found at {llama_server}\nBuild llama.cpp first."
            )

        cmd = [
            "llama.cpp/build/bin/llama-server",
            "--model", model_path,
            "--port", str(PORT),
            "--ctx-size", "2048",
            "--temp", "0.3",
            "--repeat-penalty", "1.1"
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

    # Giving server some time
    time.sleep(4)

    print("Model server launched!")


def stop_model():
    """
    Gracefully stop model server.
    """
    global PROCESS

    if PROCESS:
        print("Stopping model server...")
        PROCESS.send_signal(signal.SIGINT)
        PROCESS.wait()
        PROCESS = None