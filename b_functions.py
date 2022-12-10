import numpy as np
from abc import ABC, abstractmethod
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt


# class function(ABC):
#     @abstractmethod
#     def eval(task):
#         #return y
#         pass
#     @abstractmethod
#     def spawn():
#         return children
#         pass
#     @abstractmethod
#     def params():
#         pass
    
# All functions expect to take in a numpy array, with first dimension being batch dim

def show_function(fn, name, dim = 1):
    if dim == 1:
        x = np.linspace(-100, 100, 1000)
        x = x[:, np.newaxis]
        # print(x)
        plt.plot(x, fn(x))
        # print(x.shape)
        plt.title(name)
        plt.show()
    elif dim == 2:
        space = np.linspace(-100, 100, 1000)
        x, y = np.meshgrid(space, space)
        xy = np.stack((x, y), axis = -1)

        z = fn(xy)
        fig = plt.figure()
        # syntax for 3-D plotting
        ax = plt.axes(projection ='3d')
        # syntax for plotting
        ax.plot_surface(x, y, z, cmap='plasma')
        plt.title(name)
        plt.show()

def _parabola(x):
    x = x/10
    return np.power(x, 2)

def parabola(x):
    '''Parabola of any dimension, dimension depends on x'''
    return np.sum(_parabola(x), axis=-1)

def _spikey_parabola(x):
    return x**2 - 10*np.cos(2*3.14*x)

def spikey_parabola(x):
    x = x/10
    return 20 + np.sum(_spikey_parabola(x), axis=-1)

def cosine(x):
    x = x/10
    return np.sum(np.cos(x), axis=-1)

def _local_minima(x):
#     x += 4 
    # print(x.shape)
    # print(x[0], x[1:])
    # x = np.multiply(x[0], 7/100)
    # x[0] *= (7/100)
    v =  .1*np.sum(np.power(x, 4)) - 8*np.sum(np.power(x[0]*1.1, 2)) + 5*x[0]
    # print("v: ", v)
    return v

def local_minima(x):
    x = x/10
    _x = x.copy()
    # print("_x: ", _x.shape)
    z = np.apply_along_axis(_local_minima , axis=-1, arr= _x)
    # print("z: ",z.shape)
    return z

def show_all():
    for k, v in func_list.items():
        show_function(v, k, dim=2)
        show_function(v, k, dim=1)

func_list = {
    "parabola"          : parabola,
    "spikey_parabola"   : spikey_parabola,
    "cosine"            : cosine,
    "local_minima"      : local_minima
}
