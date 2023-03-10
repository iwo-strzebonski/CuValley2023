from utils import read_files, parse_data, save_data
import torch

global USE_CUDA
global DEVICE


if __name__ == '__main__':
    USE_CUDA = torch.cuda.is_available()
    DEVICE = torch.device("cuda" if USE_CUDA else "cpu")

    filtered_meteo, filtered_hydro = read_files.read_files()
    data_set = parse_data.get_training_data(filtered_meteo, filtered_hydro)
    save_data.save_data(data_set, 'data_set.csv')
