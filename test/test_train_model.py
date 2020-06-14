import pytest
import pandas as pd
from models.train_model import *


# def test_trainmodel():
#     df = make_iterations()
#     assert not df.empty

def test_generate_delay_features():
    d = {'MONTH': [1, 2], 'DAY_OF_WEEK': [3, 4], 'OP_UNIQUE_CARRIER': [5,6], 'ORIGIN_AIRPORT_ID': [3, 4], 'DEST_STATE_ABR': [5,6],'ARR_DELAY': [5,6],'Test': [1, 2], 'Telephone': [3, 4], 'Banana': [5,6], 'Orange': [3, 4], 'Table': [5,6],'Banana2': [5,6]}
    df = pd.DataFrame(data=d)
    cols = len(generate_delay_features(df))
    
    assert cols == 4

def test_generate_cancel_features():
    d = {'MONTH': [1, 2], 'DAY_OF_WEEK': [3, 4], 'OP_UNIQUE_CARRIER': [5,6], 'ORIGIN_AIRPORT_ID': [3, 4], 'DEST_STATE_ABR': [5,6],'CANCELLED': [5,6],'Test': [1, 2], 'Telephone': [3, 4], 'Banana': [5,6], 'Orange': [3, 4], 'Table': [5,6],'Banana2': [5,6]}
    df = pd.DataFrame(data=d)
    cols = len(generate_cancel_features(df))
    
    assert cols == 4

def test_generate_delay_features_fails():
    with pytest.raises(KeyError):
        d = {'MONTH': [1, 2], 'DAY_OF_WEEK': [3, 4], 'OP_UNIQUE_CARRIER': [5,6],'Test': [1, 2], 'Telephone': [3, 4], 'Banana': [5,6], 'Orange': [3, 4], 'Table': [5,6],'Banana2': [5,6]}
        df = pd.DataFrame(data=d)
        generate_delay_features(df)
    

def test_generate_cancel_features_fails():
    with pytest.raises(KeyError):
        d = {'Test': [1, 2], 'Telephone': [3, 4], 'Banana': [5,6], 'Orange': [3, 4], 'Table': [5,6],'Banana2': [5,6]}
        df = pd.DataFrame(data=d)
        generate_cancel_features(df)
