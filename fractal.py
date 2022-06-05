from math import nan
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from multiprocessing import Pool

RESOLUTION = 800
MAX_ITERS = 512
USE_MULTIPROCESSING = True
NUM_PROCESS = 8
NUM_CHUNKS = 8

def mandelbrot(c):
    ans = np.zeros(c.shape,dtype=int)
    z = np.zeros_like(c)
    for t in range(1,MAX_ITERS+1):
        m = ans == 0
        z[m] = z[m]*z[m] + c[m]
        ans[m] = (np.abs(z[m]) > 2)*(t+1)
        t+=1
    return ans

def job_processer(args) :
    return mandelbrot(args[0]),args[1]

def get_fractal(ystart,yend,xstart,xend,multiprocess=False):
    x,y = np.ogrid[ystart:yend:RESOLUTION*1j, xstart:xend:RESOLUTION*1j]
    grid = y+1j*x
    ans = None

    if multiprocess:
        jobs = []
        step_size = RESOLUTION//NUM_CHUNKS
        for i in range(NUM_CHUNKS):
            for j in range(NUM_CHUNKS):
                sl = np.index_exp[i*step_size: (i+1)*step_size ,j*step_size:(j+1)*step_size]
                jobs.append( (grid[sl],sl))
        pool = Pool(NUM_PROCESS).map(job_processer, jobs)
        for fractal_slice, sl in pool:
            grid[sl] = fractal_slice
        ans = grid.astype(float)
    else:
        ans = job_processer((grid,0))[0]

    ans[ans==0] = nan
    return ans

def rescale(x, in_min,in_max,out_min,out_max):
     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def redraw(event):
    global bounding_box
    global l

    if l:
        x,y =l.axes.get_xlim(),l.axes.get_ylim()
    else:
        x,y = (0.5,RESOLUTION-.5),(0.5,RESOLUTION-.5)

    bounding_box = (
        rescale(y[1],0.5,RESOLUTION-.5,bounding_box[0],bounding_box[1]),
        rescale(y[0],0.5,RESOLUTION-.5,bounding_box[0],bounding_box[1]),
        rescale(x[0],0.5,RESOLUTION-.5,bounding_box[2],bounding_box[3]),
        rescale(x[1],0.5,RESOLUTION-.5,bounding_box[2],bounding_box[3]),
    )

    new_fractal = get_fractal(*bounding_box,USE_MULTIPROCESSING)
    plt.clf()
    l = plt.imshow(new_fractal,**imshow_options)
    add_button()

def add_button():
    redraw_button = Button(plt.axes([0.85, 0.01, 0.1, 0.075]),'Redraw')
    redraw_button.on_clicked(redraw)
    plt._hiddenbutton = redraw_button

if __name__ == '__main__':
    bounding_box = (-2,2,-2,1)
    cmap = mpl.cm.get_cmap("twilight_shifted")
    cmap.set_bad(color='black')
    imshow_options = {'cmap':cmap,'vmin':0,'vmax':MAX_ITERS}
    l = None

    redraw(None)
    plt.show()
