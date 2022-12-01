"""CIFAR10 configurations."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import torch

from configs import config
from src.utils.general_utils import generate_uuid4


@dataclass(frozen=False, init=True)
class Data:
    """Class for data related params."""

    root_dir: Optional[Path] = config.DATA_DIR  # data/
    url: Optional[
        str
    ] = "https://github.com/gao-hongnan/peekingduck-trainer/releases/download/v0.0.1-alpha/cifar10.zip"
    blob_file: Optional[str] = "cifar10.zip"
    train_csv: Union[str, Path] = field(init=False)
    test_csv: Union[str, Path] = field(init=False)
    train_dir: Union[str, Path] = field(init=False)
    test_dir: Union[str, Path] = field(init=False)
    data_dir: Union[str, Path] = field(init=False)
    image_col_name: str = "image_id"
    image_path_col_name: str = "image_path"
    target_col_name: str = "class_id"
    image_extension: str = ".png"
    class_name_to_id: Optional[Dict[str, int]] = field(
        default_factory=lambda: {
            "airplane": 0,
            "automobile": 1,
            "bird": 2,
            "cat": 3,
            "deer": 4,
            "dog": 5,
            "frog": 6,
            "horse": 7,
            "ship": 8,
            "truck": 9,
        }
    )
    class_id_to_name: Optional[Dict[int, str]] = field(init=False)

    def __post_init__(self) -> None:
        """Post init method for dataclass."""
        self.data_dir = Path(config.DATA_DIR) / "cifar10"
        self.train_dir = self.data_dir / "train"
        self.test_dir = self.data_dir / "test"
        self.train_csv = self.train_dir / "train.csv"
        self.test_csv = self.test_dir / "test.csv"
        self.class_id_to_name = {v: k for k, v in self.class_name_to_id.items()}

    @property
    def download(self) -> bool:
        """Return True if data is not downloaded."""
        return not Path(self.data_dir).exists()


@dataclass(frozen=False, init=True)
class DataModuleParams:
    """Class to keep track of the data loader parameters."""

    debug: bool = True

    test_loader: Optional[Dict[str, Any]] = None

    debug_loader: Dict[str, Any] = field(
        default_factory=lambda: {
            "batch_size": 4,
            "num_workers": 0,
            "pin_memory": True,
            "drop_last": False,
            "shuffle": False,
            "collate_fn": None,
        }
    )

    train_loader: Dict[str, Any] = field(
        default_factory=lambda: {
            "batch_size": 32,
            "num_workers": 0,
            "pin_memory": True,
            "drop_last": False,
            "shuffle": True,
            "collate_fn": None,
        }
    )
    valid_loader: Dict[str, Any] = field(
        default_factory=lambda: {
            "batch_size": 32,
            "num_workers": 0,
            "pin_memory": True,
            "drop_last": False,
            "shuffle": False,
            "collate_fn": None,
        }
    )


@dataclass(frozen=False, init=True)
class AugmentationParams:
    """Class to keep track of the augmentation parameters."""

    image_size: int = 224
    pre_center_crop: int = 256
    mean: List[float] = field(default_factory=lambda: [0.485, 0.456, 0.406])
    std: List[float] = field(default_factory=lambda: [0.229, 0.224, 0.225])

    mixup: bool = False
    mixup_params: Optional[Dict[str, Any]] = None


@dataclass(frozen=False, init=True)
class ModelParams:
    """Class to keep track of the model parameters."""

    # TODO: well know backbone models are usually from torchvision or timm.
    # model_name: str = "resnet18"
    # adaptor: str = "torchvision/timm"
    # pretrained: bool = True
    num_classes: int = 10  # 2
    dropout: float = 0.3  # 0.5


@dataclass(frozen=False, init=True)
class Stores:
    """A class to keep track of model artifacts."""

    project_name: str = "MNIST"
    unique_id: str = field(default_factory=generate_uuid4)
    logs_dir: Path = field(init=False)
    artifacts_dir: Path = field(init=False)

    def __post_init__(self) -> None:
        """Create the logs directory."""
        self.logs_dir = Path(config.LOGS_DIR) / self.project_name / self.unique_id
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.artifacts_dir = (
            Path(config.MODEL_ARTIFACTS) / self.project_name / self.unique_id
        )
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=False, init=True)
class CriterionParams:
    """A class to track loss function parameters."""

    train_criterion_name: str = "CrossEntropyLoss"
    valid_criterion_name: str = "CrossEntropyLoss"
    train_criterion_params: Dict[str, Any] = field(
        default_factory=lambda: {
            "weight": None,
            "size_average": None,
            "ignore_index": -100,
            "reduce": None,
            "reduction": "mean",
            "label_smoothing": 0.0,
        }
    )
    valid_criterion_params: Dict[str, Any] = field(
        default_factory=lambda: {
            "weight": None,
            "size_average": None,
            "ignore_index": -100,
            "reduce": None,
            "reduction": "mean",
            "label_smoothing": 0.0,
        }
    )


@dataclass(frozen=False, init=True)
class OptimizerParams:
    """A class to track optimizer parameters."""

    # batch size increase 2, lr increases a factor of 2 as well.
    optimizer_name: str = "AdamW"
    optimizer_params: Dict[str, Any] = field(
        default_factory=lambda: {
            "lr": 1e-4,
            "betas": (0.9, 0.999),
            "amsgrad": False,
            "weight_decay": 1e-6,
            "eps": 1e-08,
        }
    )


@dataclass(frozen=False, init=True)
class SchedulerParams:
    """A class to track Scheduler Params."""

    scheduler_name: str = "CosineAnnealingWarmRestarts"  # Debug
    scheduler_params: Dict[str, Any] = field(
        default_factory=lambda: {
            "T_0": 10,
            "T_mult": 1,
            "eta_min": 1e-6,
            "last_epoch": -1,
            "verbose": False,
        }
    )

    def __post_init__(self) -> None:
        """Initialize the scheduler params based on some choices given."""


@dataclass(frozen=False, init=True)
class GlobalTrainParams:
    """Train params, a lot of overlapping.
    FIXME: overlapping with other params.
    """

    debug: bool = False
    debug_multiplier: int = 128
    epochs: int = 3  # 10 when not debug
    use_amp: bool = True
    mixup: bool = False
    patience: int = 3
    model_name: str = "custom"
    num_classes: int = 10
    classification_type: str = "multiclass"


@dataclass(frozen=False, init=True)
class CallbackParams:
    """Callback params."""

    callbacks: List[str]  # = ["EarlyStopping", "ModelCheckpoint", "LRScheduler"]


@dataclass(frozen=False, init=True)
class PipelineConfig:
    """Pipeline config."""

    data: Data = Data()
    datamodule: DataModuleParams = DataModuleParams()
    augmentation: AugmentationParams = AugmentationParams()
    model: ModelParams = ModelParams()
    stores: Stores = Stores()
    global_train_params: GlobalTrainParams = GlobalTrainParams()
    optimizer_params: OptimizerParams = OptimizerParams()
    scheduler_params: SchedulerParams = SchedulerParams()
    criterion_params: CriterionParams = CriterionParams()

    device: str = "cuda" if torch.cuda.is_available() else "cpu"  # see utils.set_device
