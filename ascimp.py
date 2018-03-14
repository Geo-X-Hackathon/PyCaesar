from osgeo import gdal
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

f = open('files.txt', 'r')

numlist=[]
for line in f:
	num=line[8:].split('.')[0],
	if num[0]=='0' or num[0]=='':
		continue
	numlist.append(int(num[0]))
f.close()
sortedlist=sorted(numlist)

first=True

#Make smaller for testing
numImages=240

#Get First Image and check dimensions
filename='../CAESAR_data/D4/elev.dat'+str(sortedlist[0])+'.txt'
dataset=gdal.Open(filename, gdal.GA_ReadOnly)
print("Size of one DTM is {} x {} x {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
print("There are {} time steps".format(len(sortedlist)))
ns=dataset.RasterXSize
nl=dataset.RasterYSize
array=np.empty([nl,ns,numImages],dtype=np.float)
print("Array size is {}".format(array.shape))
dataset=None

#Cycle through all images and append to array
#for i in range(0,len(sortedlist)):
if False: #run only once
  for i in range(0,numImages):
	num=sortedlist[i]
	name='../CAESAR_data/D4/elev.dat'+str(num)+'.txt'
	ds=gdal.Open(name, gdal.GA_ReadOnly)	
	a=ds.GetRasterBand(1).ReadAsArray()
	array[:,:,i]=a
	array[:,:,i][a<-999]=np.nan
	ds = None
  np.save('elev.npy',array)
else:
  array = np.load('elev.npy')

min=np.nanmin(array)
max=np.nanmax(array)
heightFactor=1.
normarray=(array-min)*heightFactor/(max-min)
min=np.nanmin(normarray)
max=np.nanmax(normarray)

diff=np.absolute(np.diff(array,axis=2))
diff[diff > .001] = np.log10(diff[diff > .001])-np.nanmin(np.log10(diff[diff > .001]))
diff=diff/np.nanmax(diff)
diff[diff < .001] = 0.

colors=np.zeros([nl,ns,4],dtype=float)

a=np.squeeze(diff[:,:,0])
colors[:,:,1]=a
colors[:,:,0]=a
colors[colors<0.001]=1.

## Create a GL View widget to display data
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('PyCAESAR: GLSurfacePlot')
w.setCameraPosition(distance=50)

#plot diffs
#win = pg.GraphicsWindow(title="Basic plotting examples")
#win.resize(1000,600)
#win.setWindowTitle('pyqtgraph example: Plotting')
#p1 = win.addPlot(title="Basic array plotting", y=diff[:,:,0].flatten())

## Add a grid to the view
g = gl.GLGridItem()
g.scale(2,2,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
w.addItem(g)

z = np.squeeze(normarray[:,:,0])
p1 = gl.GLSurfacePlotItem(z=z, shader='shaded', colors=colors.reshape(ns*nl,4), computeNormals=True, smooth=False)
p1.scale(1./50., 1./50., 2.)
w.addItem(p1)

index = 0
def update():
	global colors,normarray, p1, z, index
	if index<numImages-2:
		index += 1
	else:
		index=0
	#print index
	a=np.squeeze(diff[:,:,index])
	colors[...]=0.
	colors[:,:,1]=a
	colors[:,:,0]=a
	colors[colors<0.001]=1.
	p1.setData(z=np.squeeze(normarray[:,:,index]), colors=colors.reshape(ns*nl,4))

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)

QtGui.QApplication.instance().exec_()
