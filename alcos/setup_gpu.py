#!/usr/bin/env python3
"""
GPU Setup Script for ALCOS
Detects and configures GPU acceleration for local model inference.
"""

import subprocess
import sys
from pathlib import Path
from logger import get_logger

logger = get_logger("gpu_setup")


def check_cuda():
    """Check if CUDA is available."""
    try:
        import torch

        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            logger.info(f"✓ CUDA available with {device_count} device(s)")

            for i in range(device_count):
                device_name = torch.cuda.get_device_name(i)
                device_props = torch.cuda.get_device_properties(i)
                vram_gb = device_props.total_memory / 1024 / 1024 / 1024
                logger.info(f"  Device {i}: {device_name} ({vram_gb:.1f}GB VRAM)")

            return True, device_count
        else:
            logger.warning("CUDA not detected. CPU-only mode will be used.")
            return False, 0
    except Exception as e:
        logger.error(f"Error checking CUDA: {e}")
        return False, 0


def check_mps():
    """Check if Metal Performance Shaders (macOS) is available."""
    try:
        import torch

        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            logger.info("✓ Metal Performance Shaders (MPS) available on macOS")
            return True
        return False
    except Exception:
        return False


def install_torch_cuda():
    """Install PyTorch with CUDA support."""
    logger.info("Installing PyTorch with CUDA support...")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "torch",
                "torchvision",
                "torchaudio",
                "--index-url",
                "https://download.pytorch.org/whl/cu118",
            ],
            check=True,
        )
        logger.info("✓ PyTorch with CUDA installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install PyTorch: {e}")
        return False


def configure_ollama():
    """Configure Ollama for GPU support."""
    logger.info("Checking Ollama configuration...")

    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            logger.info(f"✓ Ollama found: {result.stdout.strip()}")
            logger.info("Ollama will automatically use GPU if available")
            return True
        else:
            logger.warning("Ollama not found. Install from https://ollama.ai")
            return False

    except FileNotFoundError:
        logger.warning("Ollama not found in PATH")
        return False
    except Exception as e:
        logger.error(f"Error checking Ollama: {e}")
        return False


def update_config(cuda_available: bool, device_count: int, mps_available: bool):
    """Update configuration file with GPU settings."""
    config_path = Path.home() / ".alcos" / "config.yaml"

    if not config_path.exists():
        logger.warning(f"Config file not found at {config_path}")
        return

    try:
        with open(config_path, "r") as f:
            content = f.read()

        # Update GPU settings
        if cuda_available:
            content = content.replace("enable_gpu: false", "enable_gpu: true")
            content = content.replace(
                "gpu_device: cpu",
                f"gpu_device: cuda:{0}",
            )
        elif mps_available:
            content = content.replace("enable_gpu: false", "enable_gpu: true")
            content = content.replace("gpu_device: cpu", "gpu_device: mps")

        with open(config_path, "w") as f:
            f.write(content)

        logger.info("✓ Configuration updated")

    except Exception as e:
        logger.error(f"Error updating config: {e}")


def main():
    """Main setup function."""
    logger.info("Starting GPU setup...")
    logger.info("")

    # Check for CUDA
    cuda_available, device_count = check_cuda()
    logger.info("")

    # Check for MPS (macOS)
    mps_available = check_mps()
    if mps_available:
        logger.info("✓ Metal Performance Shaders available")
        logger.info("")

    # Prompt for CUDA installation if not available
    if not cuda_available and not mps_available:
        logger.warning(
            "No GPU acceleration detected. "
            "Consider installing CUDA for better performance."
        )
        logger.info("See: https://pytorch.org/get-started/locally/")
    else:
        # Try to install/update PyTorch if CUDA is available
        if cuda_available:
            install_torch_cuda()

    # Configure Ollama
    logger.info("")
    configure_ollama()

    # Update configuration
    logger.info("")
    update_config(cuda_available, device_count, mps_available)

    logger.info("")
    logger.info("╔════════════════════════════════════════════════════════════════════╗")
    logger.info("║  GPU Setup Complete!                                               ║")
    logger.info("╚════════════════════════════════════════════════════════════════════╝")
    logger.info("")

    if cuda_available:
        logger.info(f"✓ GPU acceleration enabled with {device_count} device(s)")
    elif mps_available:
        logger.info("✓ GPU acceleration enabled (Metal Performance Shaders)")
    else:
        logger.warning("⚠ Running in CPU-only mode")

    logger.info("")


if __name__ == "__main__":
    main()
