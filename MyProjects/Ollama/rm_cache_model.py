from sentence_transformers import SentenceTransformer
import os
import shutil

# Загрузка модели
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Получение пути к кэшу модели
cache_folder = model._modules["0"].auto_model.config._name_or_path.replace("/", os.sep)

# Возможные пути к модели
possible_cache_paths = [
    os.path.join(os.path.expanduser("~"), ".cache", "torch", "sentence_transformers", cache_folder),
    os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub", f"models--{cache_folder.replace(os.sep, '--')}")
]

# Поиск и удаление модели
model_found = False
for full_cache_path in possible_cache_paths:
    if os.path.exists(full_cache_path):
        print(f"Found model at: {full_cache_path}")
        shutil.rmtree(full_cache_path)
        print(f"Deleted cache for model: {model_name}")
        model_found = True
        break

if not model_found:
    print(f"Cache folder not found for model: {model_name}")