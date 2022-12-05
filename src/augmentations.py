"""Transforms for data augmentation."""
from abc import ABC, abstractmethod
from typing import Any

import torchvision.transforms as T

from configs.base_params import PipelineConfig


class Transforms(ABC):
    """Create a Transforms class that can take in albumentations
    and torchvision transforms.
    """

    def __init__(self, pipeline_config: PipelineConfig) -> None:
        self.pipeline_config = pipeline_config

    @property
    @abstractmethod
    def train_transforms(self):
        """Get the training transforms."""

    @property
    @abstractmethod
    def valid_transforms(self):
        """Get the validation transforms."""

    @property
    def test_transforms(self):
        """Get the test transforms."""

    @property
    def gradcam_transforms(self):
        """Get the gradcam transforms."""

    @property
    def debug_transforms(self):
        """Get the debug transforms."""

    @property
    def test_time_augmentations(self):
        """Get the test time augmentations."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the transforms."""


class ImageClassificationTransforms(Transforms):
    """General Image Classification Transforms."""

    def __init__(self, pipeline_config: PipelineConfig) -> None:
        super().__init__(pipeline_config)
        self.pipeline_config = pipeline_config

    @property
    def train_transforms(self) -> T.Compose:
        return self.pipeline_config.augmentation.train_transforms

    @property
    def valid_transforms(self) -> T.Compose:
        return self.pipeline_config.augmentation.valid_transforms

    @property
    def test_transforms(self):
        return self.pipeline_config.augmentation.test_transforms

    @property
    def debug_transforms(self) -> T.Compose:
        return self.pipeline_config.augmentation.debug_transforms
