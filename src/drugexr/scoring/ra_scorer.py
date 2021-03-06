# --TODO: Extract root logger to some kind of config file.--
import logging
import sys
from typing import Optional, Union, List

import numpy as np
import rdkit
from RAscore import RAscore_NN, RAscore_XGB

from drugexr.config.constants import MODEL_PATH

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
# ----------------------------------------------------------

NN_MODEL_PATH = MODEL_PATH / "rascore/DNN_chembl_fcfp_counts/model.h5"
XGB_MODEL_PATH = MODEL_PATH / "rascore/XGB_chembl_ecfp_counts/model.pkl"


def calculate_score(mol: str, use_xgb_model: bool = False) -> Optional[float]:
    """
    Given a SMILES string, returns a score in [0-1] that indicates how
    likely RA Score predicts it is to find a synthesis route.
    Args:
        mol (str): a SMILES string representing a molecule.
        use_xgb_model (bool): Determines if the XGB-based model for RA Score
                              should be used instead of NN-based. False by default.

    Returns: A score between 0 and 1 indicating how likely a synthesis route is to be found by the underlying CASP tool (AiZynthFinder).
    """
    scorer = (
        RAscore_XGB.RAScorerXGB(model_path=XGB_MODEL_PATH)
        if use_xgb_model
        else RAscore_NN.RAScorerNN(model_path=NN_MODEL_PATH)
    )

    score = scorer.predict(smiles=mol)
    return score


class RetrosyntheticAccessibilityScorer:
    def __init__(self, use_xgb_model: bool = False):
        self.scorer = (
            RAscore_XGB.RAScorerXGB(model_path=XGB_MODEL_PATH)
            if use_xgb_model
            else RAscore_NN.RAScorerNN(model_path=NN_MODEL_PATH)
        )

    def __call__(self, mols: List[str]):
        scores = np.zeros(shape=len(mols), dtype="float64")
        for i, mol in enumerate(mols):
            if mol is None:
                scores[i] = .0
                continue

            if not isinstance(mol, str):
                mol = rdkit.Chem.MolToSmiles(mol)

            scores[i] = self.scorer.predict(mol)
        return scores


# TODO: Extract to dedicated test module
def test_calc_ra_score():
    omeprazole = "CC1=CN=C(C(=C1OC)C)CS(=O)C2=NC3=C(N2)C=C(C=C3)OC"
    score = calculate_score(mol=omeprazole)
    assert 0 <= score <= 1
