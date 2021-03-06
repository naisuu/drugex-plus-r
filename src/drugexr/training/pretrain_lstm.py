import logging
from pathlib import Path

import mlflow
import pytorch_lightning as pl
from dotenv import load_dotenv

from drugexr.config.constants import MODEL_PATH, PROC_DATA_PATH
from drugexr.data.chembl_corpus import ChemblCorpus
from drugexr.data_structs.vocabulary import Vocabulary
from drugexr.models.generator import Generator
from drugexr.utils.tensor_ops import print_auto_logged_info


def main(
    epochs: int = 50,
    dev: bool = False,
    n_workers: int = 4,
    n_gpus: int = 1
):
    load_dotenv()

    vocabulary = Vocabulary(
        vocabulary_path=Path(PROC_DATA_PATH / "chembl_voc.txt")
    )

    output_dir = MODEL_PATH / "output/rnn"
    if not Path.exists(output_dir):
        logging.info(
            f"Creating directories to store pretraining output @ '{output_dir}'"
        )
        Path(output_dir).mkdir(parents=True)

    pretrained_lstm_path = output_dir / "pretrained_lstm.ckpt"

    prior = Generator(vocabulary=vocabulary)

    logging.info("Initiating ML Flow tracking...")
    mlflow.set_tracking_uri("https://dagshub.com/naisuu/drugex-plus-r.mlflow")
    mlflow.pytorch.autolog()

    chembl_dm = ChemblCorpus(vocabulary=vocabulary, n_workers=n_workers)
    logging.info("Setting up ChEMBL Data Module...")
    chembl_dm.setup(stage="fit")

    logging.info("Creating Trainer...")
    pretrainer = pl.Trainer(
        gpus=n_gpus,
        log_every_n_steps=1 if dev else 50,
        max_epochs=epochs,
        fast_dev_run=dev,
        default_root_dir=output_dir,
    )

    logging.info("Starting main pretraining run...")
    with mlflow.start_run() as run:
        pretrainer.fit(model=prior, datamodule=chembl_dm)

    print_auto_logged_info(mlflow.get_run(run_id=run.info.run_id))
    logging.info("Training finished, saving pretrained LSTM checkpoint...")
    pretrainer.save_checkpoint(filepath=pretrained_lstm_path)


if __name__ == "__main__":
    main(dev=True)
