from matplotlib import pyplot
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import numpy as np

a, b, c, d = [np.random.randint(10, size = 4) for _ in range(4)]
grid = ((a,b),(c,d))
grid = np.array(grid)

fig = plt.figure(figsize=(7,5))
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.15, bottom=0.25)   

words = ['Sample1']

data_start = 0.5
dataSlider_ax  = fig.add_axes([0.15, 0.1, 0.7, 0.05])
dataSlider = Slider(dataSlider_ax, 'value', 0, 1, valinit=data_start)

image = ax.imshow(grid[0], interpolation='none', aspect='auto')
texts = [[ax.text(i,j,words[0])
          for i in range(grid.shape[2])]
         for j in range(grid.shape[1])]

def update(val):
    global image, texts
    ref = int(dataSlider.val * 2)    
    print (ref)
    image.set_data(grid[ref])
    for (j,i),label in np.ndenumerate(grid[ref]):
        texts[j][i].set_text(words[ref])
    print(ax.get_children())  # if this list keeps getting longer, you are leaking objects

dataSlider.on_changed(update)
pyplot.show()