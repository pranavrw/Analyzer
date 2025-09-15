import os
import yaml
from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "train_config.yaml")
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "models")

with open(CONFIG_PATH, "r") as f:
    train_config = yaml.safe_load(f)


def train_yolo():
    model_path = os.path.join(MODELS_DIR, "best.pt")
    model = YOLO(model_path)

    model.train(
        data=os.path.join(os.path.dirname(BASE_DIR), "data", "processed", "dataset.yaml"),
        epochs=train_config["epochs"],
        imgsz=train_config["imgsz"],
        batch=train_config["batch"],
        project=os.path.join(MODELS_DIR, "runs"),
        name="exp"
    )

    return os.path.join(MODELS_DIR, "runs", "exp", "weights", "best.pt")
