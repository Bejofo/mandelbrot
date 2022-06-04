import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

RESOLUTION = 500

def fractal_function(c):
    ans = np.zeros(c.shape)
    z = np.zeros_like(c)
    t = 0
    max_interations = 500
    while t < max_interations:
        z = z**2 + c
        diverged = (np.abs(z) > 8)*(t+1)
        diverged = diverged * (ans == 0) 
        ans += diverged
        z[ans != 0] = 0
        t+=1
    return ans

def get_fractal(ystart,yend,xstart,xend):
    x,y = np.ogrid[ystart:yend:RESOLUTION*1j, xstart:xend:RESOLUTION*1j]
    grid = y+1j*x
    return np.sqrt(fractal_function(grid))


def rescale(x, in_min,in_max,out_min,out_max):
     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

bounding_box = [-2,2,-2,1]
l = plt.imshow( get_fractal(*bounding_box) )

def redraw(event):
    global bounding_box
    global l
    l.axes.reset_position()
    x = list(l.axes.get_xlim())
    y = list(l.axes.get_ylim())
    y.reverse()
    x[0] = rescale(x[0],0.5,RESOLUTION-.5,bounding_box[2],bounding_box[3])
    x[1] = rescale(x[1],0.5,RESOLUTION-.5,bounding_box[2],bounding_box[3])
    y[0] = rescale(y[0],0.5,RESOLUTION-.5,bounding_box[0],bounding_box[1])
    y[1] = rescale(y[1],0.5,RESOLUTION-.5,bounding_box[0],bounding_box[1])
    bounding_box = [ y[0],y[1],x[0],x[1]]
    new_fractal = get_fractal( *bounding_box )
    plt.clf()
    l = plt.imshow(new_fractal)
    add_button()

def add_button():
    redraw_button = Button(plt.axes([0.85, 0.01, 0.1, 0.075]),'Redraw')
    redraw_button.on_clicked(redraw)
    plt._hiddenbutton = redraw_button
    print('added button')

add_button()
plt.show()