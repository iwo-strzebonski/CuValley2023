import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from datetime import datetime

class HydroDataset(Dataset):

    def __init__(self, hydro_file):
        xy = np.loadtxt(hydro_file, delimiter=',', dtype=np.float32, skiprows=1, encoding='utf-8')
        self.x = torch.from_numpy(xy[:, 1:])
        self.y = torch.from_numpy(xy[:, [0]])
        self.n_samples = xy.shape[0]
        self.n_features = xy.shape[1] - 1

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples


dataset = HydroDataset('utils/out/data_set.csv')

# training parameters
batch_size = 1
number_of_epochs = 10000
learning_rate = 0.00001
n_features = dataset.n_features
output_size = 1

# model
model = nn.Linear(n_features, output_size)

# Loss and optimizer classes for training purposes
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)


def training():
    """
    Train model Linear model for hydro forecast

    :return:
    """
    for epoch in range(number_of_epochs):
        for i, (X_train, y_train) in enumerate(dataloader):
            # forward pass
            y_predicted = model(X_train)
            loss = criterion(y_predicted, y_train)

            # backward
            loss.backward()

            # updates
            optimizer.step()
            optimizer.zero_grad()

        if (epoch + 1) % 10 == 0:
            print(f'epoch: {epoch + 1}, loss = {loss.item():.4f}')
        torch.save(model.state_dict(), 'utils/out/model.pth')


def predict_forecast(dataset_file, is_file = True) -> dict:
    """
    Predict height of Odra river on daily basis based on provided datetime range

    :return:
    """
    # Upload model and datasets
    hydro_model = nn.Linear(n_features, output_size)
    hydro_model.load_state_dict(torch.load('utils/out/model.pth'))
    
    if not is_file:
        with open('utils/out/data.csv', 'w', encoding='utf-8') as file:
            file.write(dataset_file)
            dataset_file = 'utils/out/data.csv'
    
    hydro_dataset = HydroDataset(dataset_file)
    hydro_data_loader = DataLoader(dataset=hydro_dataset, batch_size=batch_size, shuffle=False)

    # Predict
    with torch.no_grad():
        hydro_forecast = {}
        for feature, date in hydro_data_loader:
            output = hydro_model(feature)
            hydro_forecast[date.item()] = [x.item() for x in output]
    return hydro_forecast


if __name__ == "__main__":
    training()
    predict_forecast()
