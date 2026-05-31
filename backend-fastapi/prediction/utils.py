import os
import matplotlib.pyplot as plt
from pathlib import Path

MEDIA_ROOT = Path(__file__).resolve().parents[1] / "media"
MEDIA_URL = "/media/"


def save_plot(filename: str) -> str:
    """
    Replaces Django api/utils.save_plot().
    Saves the current matplotlib figure and returns a URL path.
    """
    MEDIA_ROOT.mkdir(exist_ok=True)
    image_path = MEDIA_ROOT / filename
    plt.savefig(str(image_path))
    plt.close()
    return MEDIA_URL + filename
