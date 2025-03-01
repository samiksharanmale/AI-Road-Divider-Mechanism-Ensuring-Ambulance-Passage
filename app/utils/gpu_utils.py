import torch
import subprocess

def is_gpu_available():
    """Check if a CUDA-capable GPU is available."""
    return torch.cuda.is_available()

def get_available_gpus():
    """
    Get details of available GPUs using PyTorch and nvidia-smi.
    Returns a list of GPUs with their name, total memory, and free memory.
    """
    if not is_gpu_available():
        return []

    # Get GPU information using nvidia-smi
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=index,name,memory.total,memory.free", "--format=csv,noheader,nounits"],
            universal_newlines=True
        )

        gpus = []
        for line in result.strip().split("\n"):
            gpu_index, gpu_name, total_memory, free_memory = line.split(", ")
            gpus.append({
                "index": int(gpu_index),
                "name": gpu_name,
                "total_memory": int(total_memory),
                "free_memory": int(free_memory)
            })
        return gpus

    except FileNotFoundError:
        print("nvidia-smi not found. Please ensure NVIDIA drivers are installed properly.")
        return []

def select_best_gpu():
    """
    Select the GPU with the most available memory.
    Returns the device string (e.g., 'cuda:0') for the selected GPU.
    """
    gpus = get_available_gpus()
    if not gpus:
        return "cpu"

    # Sort GPUs by free memory in descending order
    best_gpu = max(gpus, key=lambda x: x["free_memory"])
    print(f"Selected GPU: {best_gpu['name']} with {best_gpu['free_memory']} MB free memory.")
    return f"cuda:{best_gpu['index']}"

def print_gpu_info():
    """
    Print details of all available GPUs.
    """
    gpus = get_available_gpus()
    if not gpus:
        print("No GPUs available.")
    else:
        print("Available GPUs:")
        for gpu in gpus:
            print(f"GPU {gpu['index']}: {gpu['name']}, Total Memory: {gpu['total_memory']} MB, Free Memory: {gpu['free_memory']} MB")

def monitor_gpu_usage(interval=5):
    """
    Continuously monitor and log GPU usage.
    Press Ctrl+C to stop monitoring.
    """
    try:
        print("Monitoring GPU usage. Press Ctrl+C to stop.")
        while True:
            result = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=index,utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                universal_newlines=True
            )
            print("\nCurrent GPU Usage:")
            for line in result.strip().split("\n"):
                gpu_index, utilization, memory_used, memory_total = line.split(", ")
                print(f"GPU {gpu_index}: {utilization}% utilization, {memory_used}/{memory_total} MB memory used.")
            
            # Wait before refreshing the usage stats
            import time
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

# Example Usage
if __name__ == "__main__":
    print_gpu_info()
    device = select_best_gpu()
    print(f"Using device: {device}")
