from utils import read_files
import torch

global USE_CUDA
global DEVICE

USE_CUDA = torch.cuda.is_available()
DEVICE = torch.device("cuda" if USE_CUDA else "cpu")

filtered_meteo, filtered_hydro = read_files.read_files()

print(f'Using device: {DEVICE}')
print()
print(filtered_meteo)
print()
print(filtered_hydro)
