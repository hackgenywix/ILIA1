# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:14:51 2016

@author: Jonatan Hadas
"""

from PIL import Image,ImageFont,ImageDraw
import random
import polynom

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def generate_text(length):
    '''
    generates random text of length 'length'
    '''
    return ''.join([random.choice(alphabet) for i in xrange(length)])
    
def render_text(txt,font_name, font_size,img, pos = (0,0), col = (0,0,0)):
    '''
    renders txt on img 
    '''
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_name, font_size)
    draw.text(pos,txt,col,font=font)
    del draw
    del font
    
def empty(size, col = 'white'):
    '''
    Creates empty white image.
    '''
    return Image.new('L',size,col)
    
def back(img, center, c):
    '''
    Draw pattern on back
    '''
    cx,cy = center
    w,h = img.size
    draw = ImageDraw.Draw(img)
    for x in xrange(w):
        for y in xrange(h):
            draw.point((x,y),fill = c*(x-cx)*(y-cy)%256)
    del draw
    
def sec_back(img, c1,c2):
    '''
    Draw pattern on back
    '''
    w,h = img.size
    draw = ImageDraw.Draw(img)
    for x in xrange(w):
        for y in xrange(h):
            draw.point((x,y),fill = (c1*x)**(c2*y)%256)
    del draw
    
def grid(img,s):
    w,h = img.size
    draw = ImageDraw.Draw(img)
    for x in xrange(0,w,s):
        draw.line(((x,0),(x,h)),fill = 0)
    for y in xrange(0,h,s):
        draw.line(((0,y),(w,y)),fill = 0)
    del draw
    
            
def distort(img,inv_f):
    '''
    Distort image img, inverse of distortion 'inv_f' is given.
    '''
    w,h = img.size
    new_img = img.copy()
    loaded_img = img.load()
    draw = ImageDraw.Draw(new_img)
    
    for x in xrange(w):
        for y in xrange(h):
            real_x = float(x)/w
            real_y = float(y)/h
            org_x,org_y = inv_f(real_x,real_y)
            int_x, int_y = int(org_x*w), int(org_y*h)
            if int_x < 0 or int_y < 0 or int_x >= w or int_y >= h:
                col = 255
            else:
                col = loaded_img[int_x, int_y]
            draw.point((x,y),fill = col)
    
    del draw
    return new_img
    
#test
img = empty((800,400))
#back(img,(100,50),3)
#sec_back(img,random.randint(3,5),random.randint(3,5))
t = generate_text(10)
render_text(t,'arial.ttf' , 96, img,(10,80),0)
#img = empty((800,400))
grid(img,10)
nimg = distort(img,polynom.transformation)