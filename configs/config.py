"""Configurations for the project."""
import logging
import sys
import warnings
from pathlib import Path
from typing import Optional

import torch

# Suppress User Warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Repository's Name
AUTHOR = "Hongnan G."
REPO = "peekingduck-trainer.git"

# Torch Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Creating Directories
BASE_DIR = Path(__file__).parent.parent.absolute()

CONFIG_DIR = Path(BASE_DIR, "configs")
DATA_DIR = Path(BASE_DIR, "data")
DOCS_DIR = Path(BASE_DIR, "docs")
SRC_DIR = Path(BASE_DIR, "src")
STORES_DIR = Path(BASE_DIR, "stores")
EXAMPLES_DIR = Path(BASE_DIR, "examples")
TESTS_DIR = Path(BASE_DIR, "tests")
SCRIPTS_DIR = Path(BASE_DIR, "scripts")

## Local stores
LOGS_DIR = Path(STORES_DIR, "logs")
BLOB_STORE = Path(STORES_DIR, "blob")
FEATURE_STORE = Path(STORES_DIR, "feature")
MODEL_ARTIFACTS = Path(STORES_DIR, "model_artifacts")
TENSORBOARD = Path(STORES_DIR, "tensorboard")
WANDB_DIR = Path(STORES_DIR, "wandb")

## Create dirs
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)
EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
TESTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
STORES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
BLOB_STORE.mkdir(parents=True, exist_ok=True)
FEATURE_STORE.mkdir(parents=True, exist_ok=True)
MODEL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
WANDB_DIR.mkdir(parents=True, exist_ok=True)
TENSORBOARD.mkdir(parents=True, exist_ok=True)


# Logger
def init_logger(
    log_file: str = Path(LOGS_DIR, "info.log"),
    module_name: Optional[str] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """Initialize logger and save to file.
    Consider having more log_file paths to save, eg: debug.log, error.log, etc.
    Args:
        log_file (str): Where to save the log file. Defaults to Path(LOGS_DIR, "info.log").
        module_name (Optional[str]): Module name to be used in logger. Defaults to None.
        level (int): Logging level. Defaults to logging.INFO.
    Returns:
        logging.Logger: The logger object.
    """

    if module_name is None:
        logger = logging.getLogger(__name__)
    else:
        # get module name, useful for multi-module logging
        logger = logging.getLogger(module_name)

    logger.setLevel(level)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    )
    file_handler = logging.FileHandler(filename=log_file)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
