import numpy as np
import torch
import torch.utils.data as Data


def txt_to_numpy(filename, row, colu):
    """
        filename:是txt文件路径
        row:txt文件中数组的行数
        colu:txt文件中数组的列数
        """
    datamat = np.zeros((row, colu))
    row_count = 0
    with open(filename, 'r') as f:
        for line in f:
            # 写入datamat
            line = line.strip().split(' ')
            datamat[row_count, :] = line[:]
            row_count += 1
    return datamat


def train(model, iterator, optimizer, crit, device):
    epoch_loss = 0.
    iter_len = len(iterator)
    model.train()
    for (train_x, train_y) in iterator:
        train_x, train_y = train_x.to(device), train_y.to(device)
        preds = model(train_x)
        loss = crit(preds, train_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    return epoch_loss / iter_len


def evaluate(model, iterator, crit, device):
    epoch_loss = 0
    iter_len = len(iterator)
    model.eval()
    for (test_x, test_y) in iterator:
        with torch.no_grad():
            test_x, test_y = test_x.to(device), test_y.to(device)
            preds = model(test_x)
            loss = crit(preds, test_y)
            epoch_loss += loss.item()
    model.train()

    return epoch_loss / iter_len


def load_data(X, Y, batch_size):
    dataset = Data.TensorDataset(X, Y)
    loader = Data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4
    )
    return loader
