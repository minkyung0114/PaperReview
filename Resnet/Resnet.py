import torch
import torch.nn as nn

import os
from torchsummary import summary

class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()

        self.residual_function = nn.Sequential( nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
                                                nn.BatchNorm2d(out_channels),
                                                nn.ReLU(),
                                                nn.Conv2d(out_channels, out_channels * BasicBlock.expansion, kernel_size=3, stride=1, padding=1, bias=False),
                                                nn.BatchNorm2d(out_channels * BasicBlock.expansion),
        )
        self.shortcut = nn.Sequential()
        self.relu = nn.ReLU()

        if stride != 1 or in_channels != BasicBlock.expansion* out_channels:
            self.shortcut = nn.Sequential(nn.Conv2d(in_channels, out_channels*BasicBlock.expansion, kernel_size=1,stride=stride, bias=False),
                                          nn.BatchNorm2d(out_channels*BasicBlock.expansion)
                                          )

    def forward(self,x):

        x = self.residual_function(x) + self.shortcut(x)
        x = self.relu
        return x


class BottleNeck(nn.Module):
    expansion = 4

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()

        self.residual_function = nn.Sequential( nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False),
                                                nn.BatchNorm2d(out_channels),
                                                nn.ReLU(),
                                                nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
                                                nn.BatchNorm2d(out_channels),
                                                nn.ReLU(),
                                                nn.Conv2d(out_channels, out_channels * BottleNeck.expansion, kernel_size=1, stride=1, bias=False),
                                                nn.BatchNorm2d(out_channels * BottleNeck.expansion),
                                                )

        self.shortcut = nn.Sequential()
        self.relu = nn.ReLU()

        if stride != 1 or in_channels != out_channels * BottleNeck.expansion:

            self.shortcut = nn.Sequential(  nn.Conv2d(in_channels, out_channels*BottleNeck.expansion, kernel_size=1, stride=stride, bias=False),
                                            nn.BatchNorm2d(out_channels*BottleNeck.expansion)
                                        )

    def forward(self,x):

        x = self.residual_function(x) + self.shortcut(x)
        x = self.relu(x)
        return x


class Resnet(nn.Module):

    def __init__(self, block, num_block, num_classes =10, init_weights=True):
        super().__init__()
        self.in_channels = 64
        self.conv1 = nn.Sequential( nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False),
                                    nn.BatchNorm2d(64),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
                                    )

        self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        self.conv3_x = self._make_layer(block, 128, num_block[1], 2)
        self.conv4_x = self._make_layer(block, 256, num_block[2], 2)
        self.conv5_x = self._make_layer(block, 512, num_block[3], 2)

        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        # weights inittialization
        if init_weights:
            self._initialize_weights()




    def _make_layer(self, block, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)

        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block.expansion

        return nn.Sequential(*layers)

    def forward(self,x):

        output =self.conv1(x)
        output = self.conv2_x(output)
        x = self.conv3_x (output)
        x = self.conv4_x (x)
        x = self.conv5_x (x)
        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x =self.fc(x)

        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

def resnet18():
    return Resnet(BasicBlock, [2, 2, 2, 2])

def resnet34():
    return Resnet(BasicBlock, [3, 4, 6, 3])

def resnet50():
    return Resnet(BottleNeck, [3, 4, 6, 3])

def resnet101():
    return Resnet(BottleNeck, [3, 4, 23, 3])

def resnet152():
    return Resnet(BottleNeck, [3, 8, 36, 3])




'''
gpu 장치 1번 할당
'''
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= "1"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print('Device:', device)
print('Current cuda device:', torch.cuda.current_device())
print('Count of using GPUs:', torch.cuda.device_count())



model = resnet50().to(device)
x = torch.randn(3, 3, 224, 224).to(device)
output = model(x)
print(output.size())
summary(model, (3,224,224), device=device.type)
