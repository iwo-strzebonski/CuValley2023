import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np


class HydroDataset(Dataset):

    def __init__(self, hydro_file):
        xy = np.loadtxt(hydro_file, delimiter=',', dtype=np.float32, skiprows=1)
        self.x = torch.from_numpy(xy[:, 1:])
        self.y = torch.from_numpy(xy[:, [0]])
        self.n_samples = xy.shape[0]
        self.n_features = xy.shape[1] - 1

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples


class LogisticRegression(nn.Module):
    def __init__(self, n_input_features):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(n_input_features, 1)

    def forward(self, x):
        y_pred = torch.sigmoid(self.linear(x))
        return y_pred


dataset = HydroDataset('wine.csv')

# training parameters
batch_size = 4
number_of_epochs = 10000
learning_rate = 0.001
n_features = dataset.n_features

# model
model = LogisticRegression(n_features)

# Loss and optimizer classes for training purposes
criterion = nn.BCELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
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
