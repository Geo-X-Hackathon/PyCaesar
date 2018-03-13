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

#Make smaller to reduce waiting time
numImages=240

#Get First Image and check dimensions
filename='../CAESAR_data/D4/elev.dat'+str(sortedlist[0])+'.txt'
dataset=gdal.Open(filename, gdal.GA_ReadOnly)
print("Size of one DTM is {} x {} x {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
print("There are {} time steps".format(len(sortedlist)))
#Build n-dimensional array (currently 3)
#array=np.empty([dataset.RasterYSize,dataset.RasterXSize,len(sortedlist)],dtype=np.float)
array=np.empty([dataset.RasterYSize,dataset.RasterXSize,numImages],dtype=np.float)
print("Array size is {}".format(array.shape))

#Cycle through all images and append to array
#for i in range(0,len(sortedlist)):
for i in range(0,numImages):
	num=sortedlist[i]
	name='../CAESAR_data/D4/elev.dat'+str(num)+'.txt'
	ds=gdal.Open(name, gdal.GA_ReadOnly)	
	a=ds.GetRasterBand(1).ReadAsArray()
	array[:,:,i]=a
	array[:,:,i][a<-999]=np.nan
	ds = None

min=np.nanmin(array)
max=np.nanmax(array)
heightFactor=3.
normarray=(array-min)*heightFactor/(max-min)
min=np.nanmin(normarray)
max=np.nanmax(normarray)
print min,max

## Create a GL View widget to display data
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('PyCAESAR: GLSurfacePlot')
w.setCameraPosition(distance=50)

## Add a grid to the view
g = gl.GLGridItem()
g.scale(2,2,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
w.addItem(g)

## Simple surface plot example
## x, y values are not specified, so assumed to be 0:50
z = np.squeeze(normarray[:,:,0])
p1 = gl.GLSurfacePlotItem(z=z, shader='heightColor', computeNormals=False)
p1.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
p1.scale(1./50., 1./50., 1.)
#p1.translate(-18, 2, 0)
w.addItem(p1)

index = 0
def update():
	global normarray, p1, z, index
	if index<numImages-1:
		index += 1
	else:
		index=0
	#print("Array size is {}".format(np.squeeze(normarray[:,:,index]).shape))
	print("Time index: {}".format(index))
	p1.setData(z=np.squeeze(normarray[:,:,index]))

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)



QtGui.QApplication.instance().exec_()
