import pytest
import pandas as pd
from src.make_predictions import *


def test_make_iterations():
    df = make_iterations()
    assert not df.empty

def test_makepredictions():
    df = make_iterations()
    cols = len(df.columns)
    preds_cols = len(makepredictions(df).columns)
    
    assert preds_cols == 2 + cols
