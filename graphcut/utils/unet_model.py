# full assembly of the sub-parts to form the complete net

from .unet_parts import *
import torch.nn as nn
import torch


class UNet(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(UNet, self).__init__()
        self.inc = Inconv(n_channels, 64)
        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        self.down4 = Down(512, 512)
        self.up1 = Up(1024, 256)
        self.up2 = Up(512, 128)
        self.up3 = Up(256, 64)
        self.up4 = Up(128, 64)
        self.outc = Outconv(64, n_classes)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.outc(x)
        return x


class UNetMultiTask(UNet):
    def __init__(self, n_channels, n_classes):
        super(UNetMultiTask, self).__init__(n_channels, n_classes)
        self.up1_boundary = Up(1024, 256)
        self.up2_boundary = Up(512, 128)
        self.up3_boundary = Up(256, 64)
        self.up4_boundary = Up(128, 64)
        self.outc_boundary = Outconv(64, n_classes)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.outc(x)
        x_boundary = self.up1_boundary(x5, x4)
        x_boundary = self.up2_boundary(x_boundary, x3)
        x_boundary = self.up3_boundary(x_boundary, x2)
        x_boundary = self.up4_boundary(x_boundary, x1)
        x_boundary = self.outc_boundary(x_boundary)
        return x, x_boundary