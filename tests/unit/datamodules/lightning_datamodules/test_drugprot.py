import pytest

# local modules
from innofw.constants import Frameworks, Stages
from innofw.utils.framework import get_datamodule
from tests.fixtures.config.datasets import drugprot_datamodule_cfg_w_target
from innofw.core.datamodules.lightning_datamodules.drugprot import DrugprotDataModule


def test_smoke():
    # create a qsar datamodule
    fw = Frameworks.torch
    task = "text-ner"
    dm: DrugprotDataModule = get_datamodule(
        drugprot_datamodule_cfg_w_target, fw, task=task
    )
    assert dm is not None

    # initialize train and test datasets
    dm.setup()

    for item in [
        dm.tokenizer,
        dm.entity_labelmapper,
        dm.model_type,
        dm.val_size,
        dm.random_seed,
        dm.collator,
        dm.train_dataset_raw,
        dm.test_dataset_raw,
        dm.train_dataset,
        dm.val_dataset,
    ]:
        assert item is not None


@pytest.mark.parametrize("stage", [Stages.train, Stages.test])
def test_train_datamodule(stage):
    # create a qsar datamodule
    fw = Frameworks.torch
    task = "text-ner"
    dm: DrugprotDataModule = get_datamodule(
        drugprot_datamodule_cfg_w_target, fw, task=task
    )
    assert dm is not None

    # initialize train and test datasets
    dm.setup(stage)

    # get dataloader by stage
    dl = dm.get_stage_dataloader(stage)
    assert dl is not None
