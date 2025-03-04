from abc import ABCMeta

import torch
from mgds.MGDS import MGDS

from modules.util.TrainProgress import TrainProgress
from modules.util.args.TrainArgs import TrainArgs
from modules.util.dtype_util import allow_mixed_precision


class DataLoaderMgdsMixin(metaclass=ABCMeta):

    def _create_mgds(
            self,
            args: TrainArgs,
            concepts: list[dict],
            definition: list,
            train_progress: TrainProgress,
    ):
        settings = {
            "enable_random_circular_mask_shrink": args.circular_mask_generation,
            "enable_random_mask_rotate_crop": args.random_rotate_and_crop,
            "target_resolution": args.resolution,
        }

        ds = MGDS(
            torch.device(args.train_device),
            args.train_dtype.torch_dtype(),
            allow_mixed_precision(args),
            concepts,
            settings,
            definition,
            batch_size=args.batch_size,
            initial_epoch=train_progress.epoch,
            initial_epoch_sample=train_progress.epoch_sample,
        )

        return ds
