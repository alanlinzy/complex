import numpy
import scipy.ndimage

class Life(object):
    def __init__(self,n,mode = "wrap",random = False):
        self.n = n # num of col and raw
        self.mode = mode
        
        if random:
            self.array = numpy.random.random_integers(0,1,(n,n))
        else:
            self.array = numpy.zeros((n, n), numpy.int8)
            
        self.weights = numpy.array([[ 1, 1, 1],
                                    [ 1,10, 1],
                                    [ 1, 1, 1]])
        
    def step(self):
        con = scipy.ndimage.filters.convolve(self.array,
                                             self.weights,
                                             mode = self.mode)
        boolean = (con==3)|(con==12)|(con==13)
        self.array = numpy.int8(boolean)

    def loop(self, steps = 1):
        [self.step() for i in xrange(steps)]

    def add_glider(self,x=0,y=0):
        coords = [(0,1),(1,2),(2,0),(2,1),(2,2)]
        for i,j in coords:
            self.array[x+i,y+j] = 1


import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as pyplot
class LifeViewer(object):
    def __init__(self,life,cmap = matplotlib.cm.gray_r):
        self.life = life
        self.cmap = cmap # colormap www.scipy.org/Cookbook/Matplotlib/Show_colormaps

        self.fig = pyplot.figure()
        pyplot.axis([0,life.n,0,life.n])
        pyplot.xticks([])
        pyplot.yticks([])

        self.pcolor = None
        self.update()

    def update(self):
        if self.pcolor:
            self.pcolor.remove()

        a = self.life.array
        self.pcolor = pyplot.pcolor(a, cmap = self.cmap)
        self.fig.canvas.draw()

    def animate(self, steps = 10):
        self.steps = steps
        self.fig.canvas.manager.window.after(100,self.animate_callback)
        pyplot.show()

    def animate_callback(self):
        for i in range(self.steps):
            self.life.step()
            self.update()

    

n =100
life = Life(n,random = True)
#life.add_glider()
viewer = LifeViewer(life)
viewer.animate(steps = 1000)







