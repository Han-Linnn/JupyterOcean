#!/usr/bin/env python3
# coding: utf-8

import os
import json

import arff
import matplotlib
import numpy
from matplotlib import pyplot
from sklearn import gaussian_process

matplotlib.use("agg")


def get_input(local=False):
    if local:
    
        print(' ')
    
        return filename

    dids = os.getenv('DIDS', None)

    if not dids:
        print("No DIDs found in environment. Aborting.")
        return

    dids = json.loads(dids)
    
    for did in dids:
        filename = Path(f'/data/inputs/{did}/0')  # 0 for metadata service
        return filename



def run_model(local=False):
    filename = get_input(local)
    if not filename:
        print("Could not retrieve filename.")
        return

    with open(filename) as datafile:
        datafile.seek(0)
        res = arff.load(datafile)
    
    
    npoints = 15

print("Stacking data.")
mat = numpy.stack(res["data"])
[X, y] = numpy.split(mat, [2], axis=1)

print("Building Gaussian Process Regressor (GPR) model")
model = gaussian_process.GaussianProcessRegressor()
model.fit(X, y)
yhat = model.predict(X, return_std=False)
Zhat = numpy.reshape(yhat, (npoints, npoints))
    




if __name__ == "__main__":
    run_model(local)