import os
import zipfile
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")


def preprocess_dataset(zip_path, extract_to=None):
    if extract_to is None:
        extract_to = os.path.join(DATA_DIR, "processed")

    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

    # Generate dataset.yaml
    dataset_yaml = {
        "train": os.path.join(DATA_DIR, "processed", "train"),
        "val": os.path.join(DATA_DIR, "processed", "val"),
        "nc": 1,
        "names": ["object"]  # later linked with labels_registry.yaml
    }

    yaml_path = os.path.join(DATA_DIR, "processed", "dataset.yaml")
    with open(yaml_path, "w") as f:
        yaml.safe_dump(dataset_yaml, f)

    return yaml_path
