import numpy as np


def make_targets():
    M = 4
    N = M
    dev = 0.6 / M
    xs = np.linspace(0,1, M+1)
    ys = 1j*np.linspace(0,1, N+1)
    xs = np.outer(xs, np.ones(N+1))
    ys = np.outer(np.ones(M+1), ys)
    src = xs+ys
    target = src.copy()
    for i in range(1,M):
        for j in range(1,N):
            target[i,j] = np.random.standard_normal() + 1j*np.random.standard_normal()
    return src, target

def prep_poly(src, tar):
    poly = np.polyfit(src.flatten(), tar.flatten(),(1+len(src))*(1+len(tar))-1 if 1  else 15)
    return poly

poly = prep_poly(*make_targets())

def transformation(x,y):
    cin = x+1j*y
    cin = 0.5+0.5j+(cin-0.5-0.5j)*2
    cret = np.polyval(poly, cin)
    return (cret.real, cret.imag)
