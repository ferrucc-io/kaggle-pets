import pytest
import pandas as pd
import numpy as np
import os
import sys

def getXY():
    """helper to get X, Y
    
    loads data from local /data folder and add basic cleaning
    """
    # this is run from /models/KNN from pytest so the the path is correct
    os.listdir('../../data')
    assert 'out_breed.csv' in os.listdir('../../data') # this assert breaks if the data is configured uncorrectly

    breeds = pd.read_csv('../../data/out_breed.csv')
    colors = pd.read_csv('../../data/out_color.csv')
    states = pd.read_csv('../../data/out_state.csv')
    train  = pd.read_csv('../../data/out_train.csv')
    test   = pd.read_csv('../../data/out_test.csv')
    sub    = pd.read_csv('../../data/out_submission.csv')

    dogs = train[train['Type'] == 1].drop('Type',axis=1)
    cats = train[train['Type'] == 2].drop('Type',axis=1)
    X = dogs.reset_index().drop('index',axis=1)
    Y = dogs['AdoptionSpeed'].reset_index().drop('index',axis=1)['AdoptionSpeed']

    assert X.shape[0] == Y.shape[0]
    
    return X, Y


def test_run():
    """
    this test just runs the load-train-predict workflow

    the code is just a script of 
    85f7ec7c8c0581c347a5b8034139a9ad3a6c3352:./../kNN.ipynb
    """
    # this sys.path.append are used to import knnModel inside /models/KNN
    sys.path.append(".")
    sys.path.append("../")
    from knnDogs20 import PredictiveModel

    ###########################################################
    #### this can be used as an example usage of the model ####
    ###########################################################

    X, Y = getXY() # get dogs

    train_size = int(len(X)*0.8)

    # split in train and validation data
    train_X, train_Y = X[:train_size], Y[:train_size]
    validation_X, validation_Y = X[train_size:], Y[train_size:]

    assert train_X.shape[0] == train_Y.shape[0]
    assert validation_X.shape[0] == validation_Y.shape[0]

    model = PredictiveModel("KNN_run_by_pytest")
    model.train(train_X, train_Y, verbose=True)
    predictions = model.predict(validation_X, verbose=True)
    score = model.evaluate(validation_Y)

    import pdb;pdb.set_trace()
    assert score > 0 # score is less then zero means something is wrong 


def test_validation():
    """
    test cross-validation
    """
    # this sys.path.append are used to import knnModel inside /models/KNN
    sys.path.append(".")
    sys.path.append("../")
    from knnDogs20 import PredictiveModel

    X, Y = getXY()
    model = PredictiveModel("KNN_run_by_pytest")
    assert model.validation(X, Y) > 0.2
    assert model.validation(X, Y, method = 1) > 0.2
    assert model.validation(X, Y, method = 2) > 0.2

    # if this model doesn't get more then 0.20 score means something is wrong

    # method 3 is LeaveOneOut: too costly, DEPRECATED
    # assert model.validation(X, Y, method = 3) > 0
