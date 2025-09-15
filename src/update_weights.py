import os
from .s3_utils import upload_to_s3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "models")


def upload_new_weights(new_weights_path):
    if not os.path.exists(new_weights_path):
        raise FileNotFoundError(f"Weights not found: {new_weights_path}")

    # always keep latest weights in models/best.pt
    local_best = os.path.join(MODELS_DIR, "best.pt")
    os.replace(new_weights_path, local_best)

    # also upload to S3
    upload_to_s3(local_best, "best.pt")
    print("✅ Updated weights uploaded to S3 and saved locally.")
