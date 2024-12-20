import torch

print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device name:", torch.cuda.get_device_name(0))
    x = torch.tensor([1.0, 2.0, 3.0]).cuda()
    print("Tensor on GPU:", x)
else:
    print("No GPU detected.")
