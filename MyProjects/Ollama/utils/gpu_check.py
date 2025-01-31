import torch

# Проверка наличия GPU
if torch.cuda.is_available():
    print("GPU доступен!")
    print(f"Количество доступных GPU: {torch.cuda.device_count()}")
    print(f"Имя GPU: {torch.cuda.get_device_name(0)}")
else:
    print("GPU недоступен. Используется CPU.")