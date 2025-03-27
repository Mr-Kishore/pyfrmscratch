import atexit
import torch

atexit.register(torch.cuda.empty_cache)  # Clears GPU memory (if used)
