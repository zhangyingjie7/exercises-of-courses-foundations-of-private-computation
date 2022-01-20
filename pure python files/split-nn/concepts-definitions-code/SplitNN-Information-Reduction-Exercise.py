'''
Created on 20211214

@author: Yingjie zhang
'''
import torch
from torch import nn


from lenet_5 import LeNet5_5
from torchvision.datasets.mnist import MNIST
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import numpy as np

import sys
sys.path.insert(1,'./ite-repo')
import ite
    

#####################################Load data#####################################
BATCH_SIZE = 256
BATCH_TEST_SIZE = 1024
data_train = MNIST('./data/mnist',
                   download=True,
                   transform=transforms.Compose([
                       transforms.Resize((32, 32)),
                       transforms.ToTensor()]))
data_test = MNIST('./data/mnist',
                  train=False,
                  download=True,
                  transform=transforms.Compose([
                      transforms.Resize((32, 32)),
                      transforms.ToTensor()]))
data_train_loader = DataLoader(data_train, batch_size = BATCH_SIZE , shuffle=True, num_workers=8)
data_test_loader = DataLoader(data_test,  batch_size = BATCH_TEST_SIZE, num_workers=8)
data_test_loader2 = DataLoader(data_test,  batch_size = 1, num_workers=0)

TRAIN_SIZE = len(data_train_loader.dataset) # 60000
TEST_SIZE = len(data_test_loader.dataset) # 10000
NUM_BATCHES = len(data_train_loader) # 235 
NUM_TEST_BATCHES = len(data_test_loader) # 10

#####################################Load pre-trained model#####################################
model_loaded = LeNet5_5()
model_loaded.load_state_dict(torch.load("./LeNet-saved-5"))
criterion = nn.NLLLoss()


#####################################Validate#####################################
def validate (net, criterion):
    net.eval()
    total_correct = 0
    avg_loss = 0.0
    for i, (images, labels) in enumerate(data_test_loader):
        labels = (labels > 5).long()
        output = net(images)
        avg_loss += criterion(output, labels).sum() 
        pred = output.detach().max(1)[1]
        total_correct += pred.eq(labels.view_as(pred)).sum()

    avg_loss /= len(data_test)
    print('Test Avg. Loss: %f, Accuracy: %f' % (avg_loss.detach().cpu().item(), float(total_correct) / len(data_test)))
    return 



def main(argv=None):
    #####################################Run validate to check the accuracy of the pretrained model#####################################
    validate (model_loaded, criterion)


    #####################################Splitting and measuring information content#####################################
    # At this point, we want to split the network to two parts, and observe 
    # how different the information content of the original images and 
    # the intermediate activations are. 
    # We chose the last convolution layer of the pre-trained 
    # model we had as the splitting point. 
    # We will feed all the test data to the convolutions, 
    # and save their outputs so that we can later use them to quantitatively measure the bits of information.
    
    #####################################Save the raw images and the intermediate activations#####################################
    imgs = []
    intermediate_activations = []
    total_correct = 0
    
    model_loaded.eval()
    for i, (images, labels) in enumerate(data_test_loader2):
        imgs.append(((np.reshape(np.squeeze(images.detach().numpy()), (1,-1)) )))
        x = images
        x = model_loaded.convnet(x)      
        
        intermediate_activations.append(((np.reshape(np.squeeze(x.detach().numpy()), (1,-1)) )))
        
        np.save("images", np.array(imgs).squeeze(1))
        np.save("intermediate_act", np.array(intermediate_activations).squeeze(1))
    
    #####################################Load the Information Toolbox#####################################
    #Then we'll load the raw images and intermediate activations as Numpy arrays.
    images_raw=np.load("images.npy")
    print(images_raw.shape) # (10000, 1024)
    intermediate_activation=np.load("intermediate_act.npy")
    print(intermediate_activation.shape) # (10000, 120)
    
    
    #####################################Mutual Information function#####################################
    co = ite.cost.MIShannon_DKL()
    # Here we'll calculate the self-information of the raw images.
    ds = np.array([1024, 1024])
    y = np.concatenate((images_raw, images_raw),axis=1)
    print(y.shape) # (10000, 2048)
    i = co.estimation(y, ds) 
    print(i) # 725.9145621068219
    # Then we'll calculate the mutual information between the raw images and the intermediate activations.
    ds = np.array([1024, 120])
    y = np.concatenate((images_raw, intermediate_activation),axis=1)
    print(y.shape) #(10000, 1144)
    i = co.estimation(y, ds) 
    print(i) # 297.6859119070511

    

if __name__=='__main__':
    sys.exit(main())
    