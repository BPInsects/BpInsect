import os
from sklearn.externals import joblib


def save_model(model,name):
    joblib.dump(model, name)

def load_model(name):
    model = joblib.load(name)
    return model

def find_model(lcbm,kind):
    name = lcbm + '_' + kind + '.model'
    return load_model(name)