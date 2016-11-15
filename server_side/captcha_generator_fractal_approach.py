# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 20:18:22 2016

@author: Jonatan Hadas
"""

import random
import numpy as np
from math import floor


unit_sqr = ((0,0),(0,1),(1,0),(1,1))

class ProjectiveTransform:
    def __init__(me,sqr,us):
        '''
        Projective transformation that matches vertices of square sqr to u[0],u[1],u[2],u[3] respectivly
        sqr is represented as (x,y,size)
        '''
        #bas eof square- minimal corner (1 added to end)
        b = np.array([sqr[0],sqr[1],1])
        #positions on square's point of view
        ps = [(0,0,0),(0,1,0),(1,0,0),(1,1,0)]
        #vertices of square
        vs = [np.array(p)*sqr[2] + b for p in ps]
        # (v1,v2,v3)*v = v4
        A = np.array(vs[:3]).T
        v = np.dot(np.linalg.inv(A),vs[3])
        #Matrix that transforms v1,v2,v3,v4 to 1,0,0 0,1,0 0,0,1 1,1,1 respectivly
        A = np.dot(A,np.diag(v))
        # (u1,u2,u3)*u = u4
        us = np.array([tuple(u)+(1,) for u in us])
        B = np.array(us[:3]).T
        u = np.dot(np.linalg.inv(B),us[3])
        #Matrix that transforms u1,u2,u3,u4 to 1,0,0 0,1,0 0,0,1 1,1,1 respectivly
        B = np.dot(B,np.diag(u))
        #Matrix of transform
        me.mat = np.dot(np.linalg.inv(A),B)
        #print me.mat
    def __call__(me, v):
        '''
        Calculate transform of given vector v
        '''
        print
        print v
        v = np.array(tuple(v)+(1,))
        print v
        v = np.dot(me.mat,v)
        print v
        return (v/v[2])[:2]

def split(proj,sqr):
    '''
    splits square sqr projected py proj to 4 randomly projected squares that fill the previous one
    '''
    #square minimum point
    b = np.array([sqr[0],sqr[1]])
    size = sqr[2]

    #points from squares point of view
    sqps = [np.array(p) for p in unit_sqr] 
    
    x,y,z,w = random.random(),random.random(),random.random(),random.random()
    ps = [np.array(p) for p in ((0,x),(y,0),(1,z),(w,1))]
    
    #randomize wheights
    ws = [random.random() for _ in xrange(4)]
    sws = float(sum(ws))
    ws = [w/sws for w in ws]
    #middle point
    mid = sum(p*w for w,p in zip(ps,ws))
    
    #division of original square
    places = [[sqps[1],ps[0]  ,sqps[0]],
              [ps[1]  ,mid    ,ps[3]  ],
              [sqps[2],ps[2]  ,sqps[3]]]
    #projected division      
    proj_places = [[proj(size*p+b) for p in l] for l in places]
    
    proj_list = [[None]*2]*2
    for x,y in unit_sqr:
        #calculate subprojections
        sqr2 = tuple(b+np.array([x,y])*size*0.5)+ (0.5*size,)
        proj_list[x][y] = ProjectiveTransform(sqr2, [proj_places[x+dx][y+dy] for dy,dx in unit_sqr])
    return proj_list

def fractal_transform(times):
    '''
    creates a random transformation created from tiled projective transform,
    method is fractal, uses split repeatitively.
    returns matrix of transforms
    '''
    #initial list of transforms
    l = [[ProjectiveTransform((0,0,1), unit_sqr)]]
    size = 1.0
    for i in xrange(times):
        #new list
        s = len(l)
        new_l = [[None]*s*2]*s*2
        for x in xrange(s):
            for y in xrange(s):
                sub_list = split(l[x][y],(x*size,y*size,size))
                for dx,dy in unit_sqr:
                    new_l[2*x+dx][2*y+dx] = sub_list[dx][dy]
        l = new_l
        size /= 2
    return l, size

def call_tiled(l,v, size):
    '''
    aplies tiled transforms in matrix l of grid sized size on vector v
    '''
    x,y = v
    int_x = int(floor((x/size)))
    int_y = int(floor((y/size)))
    if int_x >= len(l):
        int_x = len(l)-1
    if int_y >= len(l[0]):
        int_y = len(l[0])-1
    return l[int_x][int_y](v)
        
def functionalize(l,size):
    return lambda x,y: call_tiled(l,(x,y),size)
#temp
import pygame          
def show(f):
     pygame.init()
     size = 600
     s = pygame.display.set_mode((size,size))
     s.fill((255,255,255))
     n = 150
     size = 100
     fn = float(n)
     for x in xrange(n):
         for y in xrange(n):
             xx,yy = f(x/fn, y/fn)
             xxx,yyy = f((x+1)/fn, y/fn)
             xxxx,yyyy = f(x/fn, (y+1)/fn)
             pygame.draw.line(s,(0,0,0),(int(xx*size),int(yy*size)),(int(xxxx*size),int(yyyy*size)))
             pygame.draw.line(s,(0,0,0),(int(xx*size),int(yy*size)),(int(xxx*size),int(yyy*size)))
     pygame.display.flip()
     while True:
         if pygame.event.poll().type == pygame.QUIT:
             pygame.quit()
             return
    
    