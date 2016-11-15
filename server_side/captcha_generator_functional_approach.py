# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 17:46:06 2016

@author: Jonatan Hadas
"""
import random
from math import sin,cos,pi

class distortion_randomizer:
    '''
    given function 'func' and a list of randomizers 'param_randomizers'
    returns value of function 'func' with random parameters randomized by 'param_randomizers' upon calling.
    '''
    def __init__(me, func, param_randomizers = []):
        me.func = func
        me.param_rand = param_randomizers
        
    def __call__(me):
        '''
        returns value of function 'func' with random parameters randomized by 'param_randomizers'
        '''
        p = [randomizer() for randomizer in me.param_rand]
        print p
        return me.func(*p)
        
#simple randomizer generators
randint = lambda n: lambda: random.randint(1,n)
rand_around0 = lambda x: lambda: (random.random()-0.5)*2*x
rand_around0_far = lambda x: lambda: x*sin(0.5*pi*(rand_around0(1)()))

# distortion - a reversible continous function from [0,1]x[0,1] to itself
base_distortion = lambda x,y: (x,y)
#list of distortion randomizers
distortion_types = [
    distortion_randomizer(
        lambda num_x, num_y, inten_x, inten_y: lambda x,y: (x+inten_x*sin(pi*num_x*(x-0.5))/pi/num_x,y+inten_y*sin(0.5*pi*num_y*(y-0.5))/pi/num_y),
        [randint(10), randint(10), rand_around0(0.5), rand_around0(0.5)]),
#    distortion_randomizer(
#        lambda a,b: lambda x,y: (x+sin(2*pi*y)*a*sin(pi*x)*(2*y*b*sin(2*pi*x) + (1-2*y)*b**2*sin(2*pi*x)**2)*(1 - 2*y*b*sin(2*pi*x) - (1-2*y)*b**2*sin(2*pi*x)**2),2*y*b*sin(2*pi*x) + (1-2*y)*b**2*sin(2*pi*x)**2),
#        [rand_around0(1), rand_around0(1)]
#        )
    ]
    
def fix(probs):
    '''
    normalizes probs to sum of 1 (a list of probabilities)
    '''
    s = float(sum(probs))
    return [p/s for p in probs]
def random_distortion(probs):
    '''
    randomizes distortion using list of distortion randomizers.
    method:
     at probability prob[0] returns identity.
     at probability prob[i+1] returns composition of:
     1. a distortion randomized by distortion_types[i]
     2. another distortion randomized by a recursive call to this function
    '''
    rand = random.random()
    for i,p in enumerate(probs):
        if rand < p:
            if i == 0:
                return base_distortion
            else:
                print i-1
                dist1 = random_distortion(probs)
                dist2 = distortion_types[i-1]()
                return lambda x,y: dist2(*dist1(x,y))
        else:
            rand -= p
            
#temp
import pygame          
def show(f):
     pygame.init()
     s = pygame.display.set_mode((600,600))
     s.fill((255,255,255))
     n = 150
     fn = float(n)
     for x in xrange(n):
         for y in xrange(n):
             xx,yy = f(x/fn, y/fn)
             xxx,yyy = f((x+1)/fn, y/fn)
             xxxx,yyyy = f(x/fn, (y+1)/fn)
             pygame.draw.line(s,(0,0,0),(int(xx*600),int(yy*600)),(int(xxxx*600),int(yyyy*600)))
             pygame.draw.line(s,(0,0,0),(int(xx*600),int(yy*600)),(int(xxx*600),int(yyy*600)))
     pygame.display.flip()
     while True:
         if pygame.event.poll().type == pygame.QUIT:
             pygame.quit()
             return