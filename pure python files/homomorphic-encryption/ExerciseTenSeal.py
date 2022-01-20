# coding:utf-8
'''
Created on 20220112

@author: Yingjie Zhang
'''

import tenseal as ts
import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

th.manual_seed(73)

# load data
train_X = th.load("data/train_X.pt")
train_y = th.load("data/train_y.pt")
test_X = th.load("data/test_X.pt")
test_y = th.load("data/test_y.pt")

# Training dataset
train_dataset = TensorDataset(train_X, train_y)
train_loader = DataLoader(train_dataset, batch_size=64)
# Test dataset
test_dataset = TensorDataset(test_X, test_y)
test_loader = DataLoader(test_dataset, batch_size=1)

# PyTorch model
# consisting of 2 linear layers, and a square activation function between them
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(1024, 128)
        self.fc2 = nn.Linear(128, 12)
        
    def forward(self, x):
        out = self.fc1(x)
        out = out * out # activation function
        out = self.fc2(out)
        return out

# train model with plaintexts
def train(model, device, train_loader, optimizer, criterion, epochs):
    losses = []
    for epoch in range(1, epochs + 1):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        
        model.eval()
        print('Train Epoch: {:2d}   Avg Loss: {:.6f}'.format(epoch, th.mean(th.tensor(losses))))
    return model

model = Model()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)
device = th.device("cuda" if th.cuda.is_available() else "cpu")

model = train(model, device, train_loader, optimizer, criterion, 30)

def compute_labels(out):
    out = th.sigmoid(out)
    return (out >= 0.5).int()

# compute accuracy using hamming loss
def accuracy(output, target):
    # convert to labels
    out = compute_labels(output)
    # flatten and compute hamming loss
    flat_out = out.flatten()
    flat_target = target.flatten()
    incorrect = th.logical_xor(flat_out, flat_target).sum().item()
    hamming_loss = incorrect / len(flat_out)
    return 1 - hamming_loss

print("Accuracy on test set: {:.2f}".format(accuracy(model(test_X), test_y)))

class HEModel:
    def __init__(self, fc1, fc2):
        self.fc1_weight = fc1.weight.t().tolist()
        self.fc1_bias = fc1.bias.tolist()
        self.fc2_weight = fc2.weight.t().tolist()
        self.fc2_bias = fc2.bias.tolist()
        
    def forward(self, encrypted_vec):
        # first fc layer + square activation function
        encrypted_vec = encrypted_vec.mm(self.fc1_weight) + self.fc1_bias
        encrypted_vec *= encrypted_vec
        # second fc layer
        encrypted_vec = encrypted_vec.mm(self.fc2_weight) + self.fc2_bias
        return encrypted_vec
    
    def __call__(self, x):
        return self.forward(x)

# Choose parameters
bits_scale = 25
# 3 multiplications, one for the square activation, and two for the matmul operation
coeff_mod_bit_sizes = [26, bits_scale, bits_scale, bits_scale, 26]
# Here, we need to put 1024 values, and anything above 2048 should make it,
# but only 8192 (and above) meet the security requirement(128-bits security).
polynomial_modulus_degree = 8192 

# Create context
context = ts.context(ts.SCHEME_TYPE.CKKS, polynomial_modulus_degree, coeff_mod_bit_sizes=coeff_mod_bit_sizes)
# Set global scale
context.global_scale = 2 ** bits_scale
# Generate galois keys required for matmul in ckks_vector
context.generate_galois_keys()

he_model = HEModel(model.fc1, model.fc2)

# how many labels in the encrypted evaluation are the same as in the plain evaluation?
match = 0
he_outs = []
for data, _ in test_loader:
    # remove batch axis, we only need a flat vector
    vec = data.flatten()
    # encryption
    encrypted_vec = ts.ckks_vector(context, vec)
    # encrypted evaluation
    encrypted_out = he_model(encrypted_vec)
    # decryption
    he_out = th.tensor(encrypted_out.decrypt())
    he_outs.append(he_out.tolist())
    out = model(data)
    # how many labels match
    he_labels = compute_labels(he_out)
    plain_labels = compute_labels(out)
    match += (he_labels == plain_labels).sum().item()
    print(match)

print("Accuracy on test set (encrypted evaluation): {:.2f}".format(accuracy(th.tensor(he_outs), test_y)))
print("Encrypted evaluation matched {:.1f}% of the labels from the plain evaluation".format(match / (12 * len(test_loader)) * 100))