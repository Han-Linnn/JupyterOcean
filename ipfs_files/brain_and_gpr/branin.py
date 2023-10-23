#
# Copyright 2022 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import matplotlib
import numpy
from matplotlib import cm, pyplot
from sklearn import gaussian_process

matplotlib.use("agg")


def branin_mesh(X0, X1):
    # b,c,t = 5.1/(4.*(pi)**2), 5./pi, 1./(8.*pi)
    b, c, t = 0.12918450914398066, 1.5915494309189535, 0.039788735772973836
    u = X1 - b * X0**2 + c * X0 - 6
    r = 10.0 * (1.0 - t) * numpy.cos(X0) + 10
    Z = u**2 + r

    return Z


def create_mesh(npoints):
    X0_vec = numpy.linspace(-5.0, 10.0, npoints)
    X1_vec = numpy.linspace(0.0, 15.0, npoints)
    X0, X1 = numpy.meshgrid(X0_vec, X1_vec)
    Z = branin_mesh(X0, X1)

    return X0, X1, Z


def arff_string(title, name, X, y):
    """
    Inputs:
      title - string
      name - string (no spaces)
      X - float array [npoints, ndim] - inputs
      y - float array [npoints] - output
    Outputs:
      s - string
    """
    assert X.shape[0] == y.shape[0]
    npoints, ndim = X.shape

    s = ""

    s += "% 1. Title: "
    s += "%s\n" % title

    s += "% 3. Number of instances: "
    s += "%s\n" % npoints

    s += "% 6. Number of attributes: "
    s += "%s\n" % ndim
    s += "\n"

    s += "@relation %s\n" % name
    s += "\n"

    for dim_i in range(ndim):
        s += "@attribute 'x%s' numeric\n" % dim_i

    s += "@attribute 'y' numeric\n"
    s += "\n"

    s += "@data\n"
    for point_i in range(npoints):
        for dim_i in range(ndim):
            s += "%0.4f," % X[point_i, dim_i]
        s += "%0.4f" % y[point_i]
        s += "\n"

    return s


def model_sin_1d():
    # not branin, but useful for testing plotting and gpr

    # create data
    npoints = 20
    xvec = numpy.linspace(0.0, 10.0, npoints)
    X = numpy.reshape(xvec, (npoints, 1))
    y = numpy.sin(xvec)

    # build model
    model = gaussian_process.GaussianProcessRegressor()
    model.fit(X, y)
    yhat = model.predict(X, return_std=False)

    # plot
    fig, ax = pyplot.subplots()
    (line1,) = ax.plot(xvec, y, label="y")
    (line2,) = ax.plot(xvec, yhat, label="yhat", linestyle="dashed", marker="o")
    ax.legend()
    pyplot.show()


def model_branin_2d():
    # create data
    npoints = 15
    X0, X1, Z = create_mesh(npoints)

    # shape data for modeling
    X = numpy.empty((X0.shape[0] * X0.shape[1], 2))
    X[:, 0] = numpy.ravel(X0)
    X[:, 1] = numpy.ravel(X1)
    y = numpy.ravel(Z)

    # surface plot - just data
    if False:
        fig, ax = pyplot.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(X0, X1, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        pyplot.title("Data")
        pyplot.show()

    # output arff file
    s = arff_string("Branin Function", "branin", X, y)
    f = open("branin.arff", "w")
    f.write(s)
    f.close()


if __name__ == "__main__":
    model_branin_2d()
    # model_sin_1d()
