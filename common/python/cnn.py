import torch.nn as nn

class SmallCNN(nn.Module):
    """
    Input:  (batch, in_channels, H, W) image, H and W divisible by 8.
    Output: (batch, out_features) numbers, e.g. out_features=1 for a
            single regression target (ball position, steering angle...).
    """

    def __init__(self, in_channels: int = 3, out_features: int = 1, image_size: int = 64):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                      # image_size / 2

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                      # image_size / 4

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                      # image_size / 8
        )

        reduced = image_size // 8
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * reduced * reduced, 64),
            nn.ReLU(),
            nn.Linear(64, out_features),
        )

    def forward(self, x):
        x = self.features(x)
        return self.head(x)
